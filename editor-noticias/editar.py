#!/usr/bin/env python3
"""
Editor automático · Noticias IA
================================
Edita los videos crudos siguiendo el guión y la "Guía de edición · Noticias IA",
sin plataformas externas: transcribe con Whisper (local), encuentra cada parte
del guión en los clips, corta silencios, arma el video vertical 9:16 con zooms,
subtítulos, títulos por noticia, gancho y CTA, normaliza la voz a −14 LUFS y
exporta en H.264 por debajo de 30 MB.

Uso:
    python3 editar.py --videos crudos/ --guion guion.md
    python3 editar.py --videos crudos/ --guion guion.md --solo-plan   # sin render

Resultado (carpeta --salida, por defecto ./salida):
    v1 1.0 noticias-dia-1.mp4   video final
    resumen.md                  qué toma se usó para cada parte y con qué precisión
    plan.json                   lista de cortes (para revisar o corregir a mano)
    transcripciones/            transcripción de cada clip (se reutiliza)
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

from rapidfuzz import fuzz

W, H, FPS = 1080, 1920, 30

# Nombres que Whisper suele escribir mal → forma correcta (guía, sección 4)
GLOSARIO = {
    "anthropic": "Anthropic", "antropic": "Anthropic", "andropic": "Anthropic", "anthropik": "Anthropic",
    "claude": "Claude", "clod": "Claude", "cloud": "Claude", "clode": "Claude",
    "seti": "SETI", "setti": "SETI", "sety": "SETI", "cety": "SETI",
    "gemini": "Gemini", "geminis": "Gemini", "yemini": "Gemini",
    "revolut": "Revolut", "revolute": "Revolut", "revolud": "Revolut",
    "siri": "Siri", "google": "Google", "apple": "Apple", "uber": "Uber",
}
PROMPT_WHISPER = "Noticias de IA: Anthropic, Claude, SETI, Google, Gemini, Apple, Siri, Revolut, Uber."

# Colores ASS (&HAABBGGRR). La guía pide acento rojo para palabras clave.
BLANCO, NEGRO, ACENTO = "&H00FFFFFF", "&H00000000", "&H002020E0"


# --------------------------------------------------------------------------- utilidades
def sh(cmd, capture=False):
    r = subprocess.run(cmd, check=True, text=True, capture_output=capture)
    return r.stdout if capture else None


def ffmpeg(*args):
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])


def probar(path):
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height:stream_tags=rotate:stream_side_data=rotation:format=duration",
              "-of", "json", str(path)], capture=True)
    d = json.loads(out)
    st = d["streams"][0]
    w, h = st["width"], st["height"]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    rot = rot or int(st.get("tags", {}).get("rotate", 0) or 0)
    if abs(rot) % 180 == 90:
        w, h = h, w
    return {"w": w, "h": h, "dur": float(d["format"]["duration"])}


def normalizar(s):
    s = s.lower().replace("%", " por ciento ")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9ñ ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def corregir_palabra(palabra):
    """Corrige nombres propios mal transcritos conservando la puntuación."""
    m = re.match(r"^(\W*)([\w%]+)(\W*)$", palabra, re.UNICODE)
    if not m:
        return palabra
    pre, nucleo, post = m.groups()
    clave = normalizar(nucleo).replace(" ", "")
    if clave in GLOSARIO:
        return pre + GLOSARIO[clave] + post
    for k, v in GLOSARIO.items():
        if len(clave) >= 5 and fuzz.ratio(clave, k) >= 84:
            return pre + v + post
    return palabra


def ass_tiempo(t):
    t = max(0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ass_texto(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")")


# --------------------------------------------------------------------------- guión
def leer_guion(path):
    """Devuelve las secciones del guión en orden: gancho, noticias y CTA."""
    texto = Path(path).read_text(encoding="utf-8")
    partes = re.split(r"^##\s+", texto, flags=re.M)[1:]
    secciones = []
    for p in partes:
        lineas = p.strip().splitlines()
        titulo = re.sub(r"[*_#]", "", lineas[0]).strip()
        cuerpo = " ".join(lineas[1:])
        cuerpo = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cuerpo)  # links markdown
        cuerpo = re.sub(r"[*_{}]", "", cuerpo).strip()
        t = titulo.lower()
        if t.startswith("fuentes") or not cuerpo:
            continue
        if t.startswith("gancho"):
            tipo, etiqueta = "gancho", ""
        elif t.startswith("cta"):
            tipo, etiqueta = "cta", ""
        else:
            tipo = "noticia"
            cat = re.split(r"[\s\d—–-]+", titulo)[0].upper()
            nombre = re.split(r"\s[—–-]\s", titulo, maxsplit=1)[-1].upper()
            etiqueta = f"{cat} · {nombre}"
        secciones.append({"titulo": titulo, "tipo": tipo, "etiqueta": etiqueta, "texto": cuerpo,
                          "tokens": normalizar(cuerpo).split()})
    return secciones


# --------------------------------------------------------------------------- transcripción
def audio_16k(clip):
    """Audio del clip en mono 16 kHz (lo que usa Whisper), extraído con ffmpeg."""
    import numpy as np

    pcm = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(clip), "-vn",
                          "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], check=True, capture_output=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def transcribir(clips, carpeta, modelo):
    carpeta.mkdir(parents=True, exist_ok=True)
    resultado, pendientes = {}, []
    for c in clips:
        cache = carpeta / f"{c.stem}.json"
        if cache.exists():
            resultado[c.name] = json.loads(cache.read_text())
        else:
            pendientes.append(c)
    if pendientes:
        from faster_whisper import WhisperModel

        print(f"· Cargando Whisper ({modelo})…", flush=True)
        wm = WhisperModel(modelo, device="cpu", compute_type="int8")
        for c in pendientes:
            print(f"· Transcribiendo {c.name}…", flush=True)
            segs, _ = wm.transcribe(audio_16k(c), language="es", word_timestamps=True,
                                    initial_prompt=PROMPT_WHISPER, condition_on_previous_text=False,
                                    vad_filter=False, beam_size=5)
            palabras = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)}
                        for s in segs for w in (s.words or []) if w.word.strip()]
            (carpeta / f"{c.stem}.json").write_text(json.dumps(palabras, ensure_ascii=False, indent=0))
            resultado[c.name] = palabras
    return resultado


# --------------------------------------------------------------------------- búsqueda de tomas
def buscar_tomas(seccion, clips, transcripciones, margen=3.0, minimo=55):
    """Busca la sección en todos los clips. Si hay varias tomas buenas
    (a ≤ `margen` puntos de la mejor), usa la ÚLTIMA grabada: suele ser la buena."""
    objetivo = " ".join(seccion["tokens"])
    n = len(seccion["tokens"])
    largos = sorted({max(2, round(n * f)) for f in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35)})
    candidatos = []
    for ci, clip in enumerate(clips):
        pal = transcripciones[clip.name]
        tok = [normalizar(p["w"]) for p in pal]
        for a in range(len(pal)):
            for L in largos:
                b = a + L
                if b > len(pal):
                    break
                txt = " ".join(t for t in tok[a:b] if t)
                candidatos.append((fuzz.ratio(txt, objetivo), ci, a, b))
    if not candidatos:
        return None
    candidatos.sort(reverse=True)
    # Tomas distintas (sin solaparse)
    tomas = []
    for sc, ci, a, b in candidatos:
        if sc < candidatos[0][0] - margen:
            break
        if all(not (ci == t[1] and a < t[3] and b > t[2]) for t in tomas):
            tomas.append((sc, ci, a, b))
    sc, ci, a, b = max(tomas, key=lambda t: (t[1], t[2]))  # la última grabada
    # Ajuste fino de los bordes
    pal = transcripciones[clips[ci].name]
    tok = [normalizar(p["w"]) for p in pal]
    mejor = (sc, a, b)
    for da in range(-4, 5):
        for db in range(-4, 5):
            aa, bb = a + da, b + db
            if 0 <= aa < bb <= len(pal):
                s2 = fuzz.ratio(" ".join(t for t in tok[aa:bb] if t), objetivo)
                if s2 > mejor[0]:
                    mejor = (s2, aa, bb)
    sc, a, b = mejor
    if sc < minimo:
        return None
    return {"clip": ci, "a": a, "b": b, "puntaje": round(sc, 1), "tomas_encontradas": len(tomas)}


# --------------------------------------------------------------------------- cortes
def armar_cortes(palabras, pausa_max=0.30, pieza_max=4.5):
    """Agrupa palabras en tramos sin silencios largos y los parte en piezas
    de máximo `pieza_max` s (cada pieza lleva un zoom distinto)."""
    tramos, actual = [], [palabras[0]]
    for p in palabras[1:]:
        if p["s"] - actual[-1]["e"] > pausa_max:
            tramos.append(actual)
            actual = [p]
        else:
            actual.append(p)
    tramos.append(actual)

    piezas = []

    def partir(ws):
        dur = ws[-1]["e"] - ws[0]["s"]
        if dur <= pieza_max or len(ws) < 4:
            piezas.append(ws)
            return
        # cortar en la pausa más grande cerca del centro
        mitad = ws[0]["s"] + dur / 2
        idx = min(range(1, len(ws)), key=lambda i: (-(ws[i]["s"] - ws[i - 1]["e"]) * 2 + abs(ws[i]["s"] - mitad) / dur))
        partir(ws[:idx])
        partir(ws[idx:])

    for t in tramos:
        partir(t)
    return piezas


# --------------------------------------------------------------------------- subtítulos
def es_clave(palabra, claves):
    n = normalizar(palabra)
    return bool(re.search(r"\d", palabra)) or n in claves


def generar_ass(plan, secciones, gancho_texto, ruta):
    claves = {"anthropic", "claude", "seti", "google", "gemini", "apple", "siri", "revolut", "ia", "uber"}
    eventos = []

    # Subtítulos: grupos de 2–4 palabras
    palabras = [w for pz in plan for w in pz["palabras_salida"]]
    grupos, actual = [], []
    for i, w in enumerate(palabras):
        actual.append(w)
        fin_frase = re.search(r"[.,;:?!…]$", w["w"])
        siguiente = palabras[i + 1] if i + 1 < len(palabras) else None
        hueco = siguiente and siguiente["s"] - w["e"] > 0.35
        largo = len(" ".join(x["w"] for x in actual))
        no_cabe = siguiente and largo + 1 + len(siguiente["w"]) > 17  # una sola línea en 1080 px
        if len(actual) >= 4 or no_cabe or (len(actual) >= 2 and (fin_frase or hueco)) or not siguiente:
            grupos.append(actual)
            actual = []
    if actual:
        grupos.append(actual)
    for gi, g in enumerate(grupos):
        ini = g[0]["s"]
        fin = grupos[gi + 1][0]["s"] if gi + 1 < len(grupos) else g[-1]["e"] + 0.3
        fin = min(fin, g[-1]["e"] + 0.6)
        partes = []
        for w in g:
            txt = ass_texto(w["w"])
            partes.append(f"{{\\c{ACENTO}}}{txt}{{\\c{BLANCO}}}" if es_clave(w["w"], claves) else txt)
        eventos.append(("Sub", ini, max(fin, ini + 0.3), " ".join(partes)))

    # Gancho, títulos de noticia y CTA
    for s in secciones:
        if "salida_ini" not in s:
            continue
        if s["tipo"] == "gancho" and gancho_texto:
            eventos.append(("Gancho", s["salida_ini"], min(s["salida_ini"] + 3.0, s["salida_fin"]),
                            ass_texto(gancho_texto.upper())))
        elif s["tipo"] == "noticia":
            eventos.append(("Titulo", s["salida_ini"], min(s["salida_ini"] + 2.4, s["salida_fin"]),
                            ass_texto(s["etiqueta"])))
        elif s["tipo"] == "cta":
            eventos.append(("CTA", s["salida_ini"], s["salida_fin"] + 0.6, ass_texto(s["texto"])))

    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Black,92,{BLANCO},{BLANCO},{NEGRO},{NEGRO},0,0,0,0,100,100,0,0,1,7,0,2,80,80,400,1
Style: Titulo,Inter Black,66,{BLANCO},{BLANCO},{ACENTO},{ACENTO},0,0,0,0,100,100,1,0,3,18,0,8,80,80,260,1
Style: Gancho,Inter Black,104,{BLANCO},{BLANCO},{NEGRO},{NEGRO},0,0,0,0,100,100,0,0,1,9,0,8,70,70,330,1
Style: CTA,Inter Black,72,{BLANCO},{BLANCO},{ACENTO},{ACENTO},0,0,0,0,100,100,0,0,3,22,0,8,90,90,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lineas = [f"Dialogue: {1 if e[0] != 'Sub' else 0},{ass_tiempo(e[1])},{ass_tiempo(e[2])},{e[0]},,0,0,0,,{e[3]}"
              for e in sorted(eventos, key=lambda e: e[1])]
    Path(ruta).write_text(cab + "\n".join(lineas) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- render
CENTRO_X = 0.5  # dónde está la persona en el cuadro (0 = izquierda, 1 = derecha)


def filtro_encuadre(info, zoom):
    """Escala y recorta a 9:16 alrededor de CENTRO_X con el zoom indicado."""
    if info["w"] / info["h"] >= W / H:  # más ancho que 9:16 → ajustar alto
        esc = f"scale=-2:{int(H * zoom) // 2 * 2}"
    else:
        esc = f"scale={int(W * zoom) // 2 * 2}:-2"
    x = f"max(0\\,min(iw-{W}\\,iw*{CENTRO_X}-{W}/2))"
    return f"{esc}:flags=lanczos,crop={W}:{H}:{x}:(ih-{H})/2,setsar=1,fps={FPS},format=yuv420p"


def congelar(pz, dur):
    """Sostiene el primer/último cuadro bueno (mirando a cámara) mientras sigue el audio."""
    c0, c1 = pz.get("congelar", (0.0, 0.0))
    if c0 <= 0 and c1 <= 0:
        return ""
    return (f"trim=start={c0:.3f}:end={max(c0 + 0.05, dur - c1):.3f},setpts=PTS-STARTPTS,"
            f"tpad=start_mode=clone:start_duration={c0:.3f}:stop_mode=clone:stop_duration={c1 + 0.3:.3f},")


def render(plan, clips, infos, tmp):
    tmp.mkdir(parents=True, exist_ok=True)
    lista = []
    for i, pz in enumerate(plan):
        out = tmp / f"pieza_{i:03d}.mp4"
        # Duración redondeada a cuadros enteros e IGUAL para video y audio:
        # así no se acumula desfase al unir las piezas.
        n = max(1, round((pz["fin"] - pz["ini"]) * FPS))
        dur = n / FPS
        fade = min(0.02, dur / 4)
        ffmpeg("-ss", f"{pz['ini']:.3f}", "-t", f"{dur + 0.1:.3f}", "-i", str(clips[pz["clip"]]),
               "-map", "0:v:0", "-map", "0:a:0",
               "-vf", congelar(pz, dur) + filtro_encuadre(infos[pz["clip"]], pz["zoom"]), "-frames:v", str(n),
               "-af", f"aresample=48000,apad,atrim=0:{dur:.6f},afade=t=in:d={fade:.3f},"
                      f"afade=t=out:st={max(0, dur - fade):.4f}:d={fade:.3f}",
               "-ac", "2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
               "-c:a", "pcm_s16le", "-f", "mov", str(out))
        pz["dur_real"] = dur
        lista.append(out)
    lst = tmp / "lista.txt"
    lst.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in lista))
    base = tmp / "base.mov"
    ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base))
    return base


def exportar(base, ass, destino, max_mb=30.0):
    dur = probar(base)["dur"]
    # Medir volumen (loudnorm en dos pasadas → −14 LUFS exactos)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(base), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       text=True, capture_output=True)
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    audio_f = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
               f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    vf = []
    if ass:
        ass_esc = str(ass).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        vf = ["-vf", f"ass='{ass_esc}'"]
    objetivo = max_mb * 0.93
    for intento in range(3):
        v_kbps = int(min(9000, objetivo * 8192 / dur - 160))
        log = destino.parent / "pass"
        comunes = ["-i", str(base), *vf, "-c:v", "libx264", "-preset", "medium",
                   "-profile:v", "high", "-pix_fmt", "yuv420p", "-b:v", f"{v_kbps}k",
                   "-maxrate", f"{int(v_kbps * 1.6)}k", "-bufsize", f"{v_kbps * 2}k", "-r", str(FPS),
                   "-passlogfile", str(log)]
        ffmpeg(*comunes, "-pass", "1", "-an", "-f", "null", "/dev/null")
        ffmpeg(*comunes, "-pass", "2", "-af", audio_f, "-ar", "48000", "-c:a", "aac", "-b:a", "160k",
               "-movflags", "+faststart", str(destino))
        mb = destino.stat().st_size / 1048576
        if mb <= max_mb:
            break
        objetivo *= 0.9
    for f in destino.parent.glob("pass*"):
        f.unlink()
    return dur, mb


# --------------------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--videos", required=True, help="carpeta con los clips crudos")
    ap.add_argument("--guion", required=True, help="guión en Markdown (secciones con ##)")
    ap.add_argument("--salida", default="salida")
    ap.add_argument("--nombre", default="v1 1.0 noticias-dia-1.mp4")
    ap.add_argument("--gancho-texto", default="Google amenaza a los colegios",
                    help="texto grande de los primeros 3 s (guía, sección 3)")
    ap.add_argument("--modelo", default="small", help="modelo de Whisper: base, small, medium")
    ap.add_argument("--pausa", type=float, default=0.30, help="silencio máximo que se deja (s)")
    ap.add_argument("--centro-x", type=float, default=0.5, help="posición horizontal de la persona (0–1)")
    ap.add_argument("--solo-plan", action="store_true", help="solo transcribir y armar el plan, sin render")
    a = ap.parse_args()
    global CENTRO_X
    CENTRO_X = a.centro_x

    clips = sorted(p for p in Path(a.videos).iterdir() if p.suffix.lower() in {".mp4", ".mov", ".m4v"})
    if not clips:
        sys.exit("No encontré videos en " + a.videos)
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)
    secciones = leer_guion(a.guion)
    print(f"· {len(clips)} clips · {len(secciones)} partes del guión", flush=True)

    infos = [probar(c) for c in clips]
    trans = transcribir(clips, salida / "transcripciones", a.modelo)

    plan, avisos, t = [], [], 0.0
    zoom_alterno = [1.0, 1.12, 1.05, 1.15]
    for s in secciones:
        toma = buscar_tomas(s, clips, trans)
        if not toma:
            avisos.append(f"No encontré «{s['titulo']}» en los clips (¿no se grabó?).")
            continue
        s["toma"] = toma
        palabras = trans[clips[toma["clip"]].name][toma["a"]:toma["b"]]
        for k, ws in enumerate(armar_cortes(palabras, a.pausa)):
            ini = max(0.0, ws[0]["s"] - 0.06)
            fin = min(infos[toma["clip"]]["dur"], ws[-1]["e"] + 0.12)
            plan.append({"seccion": s["titulo"], "clip": toma["clip"], "ini": round(ini, 3), "fin": round(fin, 3),
                         "zoom": 1.0 if k == 0 else zoom_alterno[len(plan) % len(zoom_alterno)],
                         "palabras": [dict(w, w=corregir_palabra(w["w"])) for w in ws]})

    resumen_plan = [{k: v for k, v in pz.items() if k != "palabras"} | {"clip": clips[pz["clip"]].name,
                     "texto": " ".join(w["w"] for w in pz["palabras"])} for pz in plan]
    (salida / "plan.json").write_text(json.dumps(resumen_plan, ensure_ascii=False, indent=2))

    if not a.solo_plan and plan:
        print(f"· Renderizando {len(plan)} cortes…", flush=True)
        tmp = salida / "_tmp"
        base = render(plan, clips, infos, tmp)
        # Línea de tiempo de salida (para subtítulos y títulos)
        t = 0.0
        for pz in plan:
            pz["palabras_salida"] = [dict(w, s=t + w["s"] - pz["ini"], e=t + w["e"] - pz["ini"]) for w in pz["palabras"]]
            pz["salida_ini"], t = t, t + pz["dur_real"]
            pz["salida_fin"] = t
        for s in secciones:
            pzs = [p for p in plan if p["seccion"] == s["titulo"]]
            if pzs:
                s["salida_ini"], s["salida_fin"] = pzs[0]["salida_ini"], pzs[-1]["salida_fin"]
        ass = salida / "subtitulos.ass"
        generar_ass(plan, secciones, a.gancho_texto, ass)
        print("· Exportando (subtítulos, −14 LUFS, H.264 ≤ 30 MB)…", flush=True)
        dur, mb = exportar(base, ass, salida / a.nombre)
        shutil.rmtree(tmp, ignore_errors=True)
        if not 45 <= dur <= 75:
            avisos.append(f"Duración {dur:.0f} s: la guía pide 45–75 s.")
    else:
        dur, mb = sum(p["fin"] - p["ini"] for p in plan), 0

    # Resumen legible
    lin = [f"# Resumen de edición · {a.nombre}", "",
           f"- Duración: **{dur:.1f} s**" + (f" · Tamaño: **{mb:.1f} MB**" if mb else " (estimada)"),
           f"- Cortes: {len(plan)} · Clips crudos: {len(clips)}", "",
           "| Parte del guión | Clip usado | Desde → hasta | Coincidencia | Tomas |", "|---|---|---|---|---|"]
    for s in secciones:
        tm = s.get("toma")
        if tm:
            pal = trans[clips[tm["clip"]].name]
            lin.append(f"| {s['titulo']} | {clips[tm['clip']].name} | {pal[tm['a']]['s']:.1f}s → "
                       f"{pal[tm['b'] - 1]['e']:.1f}s | {tm['puntaje']}% | {tm['tomas_encontradas']} |")
        else:
            lin.append(f"| {s['titulo']} | — | — | no encontrada | 0 |")
    if avisos:
        lin += ["", "## Avisos", *[f"- {x}" for x in avisos]]
    (salida / "resumen.md").write_text("\n".join(lin) + "\n", encoding="utf-8")
    print("\n".join(lin))


if __name__ == "__main__":
    main()
