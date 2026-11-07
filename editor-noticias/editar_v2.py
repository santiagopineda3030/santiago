#!/usr/bin/env python3
"""
Edición v2 · Noticias IA: cortes ajustados + animaciones + efectos de sonido.

- Cortes: 0,06 s de aire antes/después de cada frase y sin pausas internas
  (silencios > 0,16 s detectados en el audio).
- Gráficos anclados a palabras ("en": "Revolut") o a segundos del clip crudo
  ("cubrir": {...}) para tapar momentos en que se mira a otro lado.
- Subtítulos con efecto "pop", títulos numerados por noticia, transiciones,
  efectos de sonido sintetizados, −14 LUFS y H.264 ≤ 30 MB.

Uso:
    python3 editar_v2.py --videos crudos --edl edl-dia-1-v2.json --trozos salida/trozos --assets assets
"""
import argparse
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

import animaciones as A
import editar
from editar import ffmpeg, normalizar, probar

PRE, POST = 0.06, 0.07
SIL_DB, SIL_MIN, SIL_MARGEN = -34, 0.16, 0.05
GRUPO_MAX = 4.0          # cada ~4 s cambia el zoom
COLA_CTA = 3.0
SR = 48000
CLAVES_EXTRA = set()   # palabras clave en rojo que agrega cada EDL ("claves": [...])
GANANCIA_SFX = {"whoosh": 0.32, "pop": 0.28, "ding": 0.22, "golpe": 0.42, "alerta": 0.22, "teclas": 0.3}


# --------------------------------------------------------------------------- audio
def voz_vad(clip):
    """Tramos donde hay VOZ (detector Silero de faster-whisper), en segundos del clip."""
    from faster_whisper.vad import VadOptions, get_speech_timestamps

    pcm = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(clip), "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    ts = get_speech_timestamps(audio, VadOptions(threshold=0.45, min_silence_duration_ms=130, speech_pad_ms=30))
    return [(t["start"] / 16000, t["end"] / 16000) for t in ts]


def tramos_con_voz(a, b, voz, antes=0.04, despues=0.06, unir=0.10):
    """Deja solo los momentos con voz dentro de [a, b] (con un poquito de aire) y une los muy cercanos."""
    tr = [(max(a, s - antes), min(b, e + despues)) for s, e in voz if e > a and s < b]
    out = []
    for x, y in tr:
        if out and x - out[-1][1] < unir:
            out[-1] = (out[-1][0], max(out[-1][1], y))
        elif y - x > 0.08:
            out.append((x, y))
    return out or [(a, b)]


def musica_de_fondo(ruta, voz, db=-21.0, bajar=6.0):
    """Música bajita bajo la voz: a `db` dB de la voz, y `bajar` dB menos mientras se habla (ducking)."""
    with wave.open(str(ruta)) as f:
        m = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    n = len(voz)
    m = np.tile(m, (n // len(m) + 1, 1))[:n]
    rms = lambda x: float(np.sqrt(np.mean(x ** 2)) + 1e-9)
    hablando = np.abs(voz).mean(1)
    win = int(0.05 * SR)
    e = np.convolve(hablando, np.ones(win) / win, "same")
    umbral = np.percentile(e, 60) * 0.35
    activo = (e > umbral).astype(np.float32)
    suave = int(0.25 * SR)
    activo = np.convolve(activo, np.ones(suave) / suave, "same")
    v_rms = rms(voz[e > umbral]) if (e > umbral).any() else rms(voz)
    g = v_rms / rms(m) * 10 ** (db / 20)
    gan = g * (10 ** (-bajar / 20) * activo + (1 - activo))
    fade = np.minimum(1, np.arange(n) / (1.0 * SR)) * np.minimum(1, (n - np.arange(n)) / (2.0 * SR))
    return m * (gan * fade)[:, None]


def mirada_mala(m, umbral=1.6, minimo=0.2, rangos=None):
    """Tramos (s, e) en que la persona NO mira a la cámara (cabeza girada o mirando las notas).
    La postura "mirando a cámara" es la mediana dentro de los rangos usados (las tomas elegidas)."""
    ok = [r for r in m if r["cara"] and (not rangos or any(a <= r["t"] <= b for a, b in rangos))]
    Y = float(np.median([r["yaw"] for r in ok]))
    P = float(np.median([r["pitch"] for r in ok]))
    malos, cur = [], None
    for r in m:
        mal = (not r["cara"]) or max(abs(r["yaw"] - Y) / 0.12, abs(r["pitch"] - P) / 0.10) >= umbral
        if mal:
            cur = [r["t"], r["t"] + 0.1] if cur is None else [cur[0], r["t"] + 0.1]
        elif cur:
            malos.append(tuple(cur))
            cur = None
    if cur:
        malos.append(tuple(cur))
    return [(a, b) for a, b in malos if b - a >= minimo - 1e-6]


def recortar_mirada(tramos, palabras, malos, aire=0.03):
    """Quita de los bordes de cada tramo los momentos en que no mira a cámara, sin comerse palabras."""
    out = []
    for x, y in tramos:
        ws = [w for w in palabras if w["e"] > x and w["s"] < y]
        p0 = min((w["s"] for w in ws), default=y)
        p1 = max((w["e"] for w in ws), default=x)
        for a, b in malos:
            if a <= x + 0.05 and b > x:      # mira a otro lado al empezar
                x = min(max(x, b), max(x, p0 - aire))
            if b >= y - 0.05 and a < y:      # mira a otro lado al terminar
                y = max(min(y, a), min(y, p1 + aire))
        if y - x > 0.08:
            out.append((x, y))
    return out or tramos


def silencios(clip):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(clip), "-vn", "-af",
                          f"silencedetect=noise={SIL_DB}dB:d={SIL_MIN}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(ini, fin))


def sin_pausas(a, b, sil):
    """Quita los silencios internos de [a, b] y devuelve los tramos con voz."""
    tramos, t = [], a
    for s, e in sil:
        if s > a + SIL_MARGEN and e < b - SIL_MARGEN and s < e:
            if s + SIL_MARGEN - t > 0.08:
                tramos.append((t, s + SIL_MARGEN))
            t = e - SIL_MARGEN
    tramos.append((t, b))
    return [(x, y) for x, y in tramos if y - x > 0.06]


# --------------------------------------------------------------------------- subtítulos (ASS v2)
def ass_v2(palabras, secciones, gancho, cta, ruta):
    claves = {"anthropic", "claude", "seti", "google", "gemini", "apple", "siri", "revolut", "ia", "ias", "uber"} | CLAVES_EXTRA
    grupos, actual = [], []
    for i, w in enumerate(palabras):
        actual.append(w)
        sig = palabras[i + 1] if i + 1 < len(palabras) else None
        largo = len(" ".join(x["w"] for x in actual))
        if (len(actual) >= 4 or (sig and largo + 1 + len(sig["w"]) > 17) or not sig
                or re.search(r"[.?!…]$", w["w"]) or (len(actual) >= 2 and (re.search(r"[,;:]$", w["w"]) or sig["s"] - w["e"] > 0.35))):
            grupos.append(actual)
            actual = []
    ev = []
    for gi, g in enumerate(grupos):
        ini = g[0]["s"]
        fin = min(grupos[gi + 1][0]["s"] if gi + 1 < len(grupos) else g[-1]["e"] + 0.4, g[-1]["e"] + 0.6)
        txt = " ".join((f"{{\\c{editar.ACENTO}}}{editar.ass_texto(w['w'])}{{\\c{editar.BLANCO}}}"
                        if editar.es_clave(w["w"], claves) else editar.ass_texto(w["w"])) for w in g)
        ev.append((0, "Sub", ini, max(fin, ini + 0.3), "{\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}" + txt))
    pop = "{\\fad(60,160)\\fscx70\\fscy70\\t(0,140,\\fscx108\\fscy108)\\t(140,240,\\fscx100\\fscy100)}"
    noticias = [s for s in secciones if s["tipo"] == "noticia"]
    for s in secciones:
        if s["tipo"] == "gancho" and gancho:
            ev.append((1, "Gancho", s["ini"], min(s["ini"] + 2.7, s["fin"]), pop + editar.ass_texto(gancho.upper())))
        elif s["tipo"] == "noticia":
            n = noticias.index(s) + 1
            ev.append((1, "Titulo", s["ini"] + 0.15, min(s["ini"] + 2.4, s["fin"]),
                       pop + f"{n}/{len(noticias)} · " + editar.ass_texto(s["etiqueta"])))
    ev.append((1, "CTA", cta[0], cta[1], pop + editar.ass_texto(cta[2])))
    cab = Path(__file__).with_name("estilos.ass").read_text(encoding="utf-8")
    lineas = [f"Dialogue: {c},{editar.ass_tiempo(a)},{editar.ass_tiempo(b)},{st},,0,0,0,,{t}"
              for c, st, a, b, t in sorted(ev, key=lambda e: e[2])]
    Path(ruta).write_text(cab + "\n".join(lineas) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- gráficos
def construir(g, dur, assets):
    t = g["tipo"]
    if t == "logo":
        return A.g_logo(f"{assets}/logo_{g['logo']}.png", dur, cy=g.get("y", 560), texto=g.get("texto"))
    if t == "emoji":
        return A.g_emoji(g["ch"], dur, g.get("x", 880), g.get("y", 830), g.get("tam", 190))
    if t == "texto":
        return A.g_texto(g["lineas"], dur, cy=g.get("y", 560), ch=g.get("ch"))
    if t == "contador":
        return A.g_contador(g["desde"], g["hasta"], g["formato"], g["etiqueta"], dur, cy=g.get("y", 560))
    if t == "barra":
        return A.g_barra(g["texto"], dur, cy=g.get("y", 560))
    if t == "sello":
        return A.g_sello(g["texto"], dur, cy=g.get("y", 600))
    if t == "buscador":
        return A.g_buscador(g["texto"], dur, cy=g.get("y", 560))
    if t == "telefono":
        return A.g_telefono(dur, g.get("x", A.W / 2), g.get("y", 520))
    if t == "alerta":
        return A.g_advertencia(g["texto"], dur, cy=g.get("y", 560))
    if t == "cambio":
        return A.g_cambio(g["antes"], g["despues"], dur, cy=g.get("y", 560), ch=g.get("ch", "⏱️"))
    if t == "foto":
        return A.g_foto(f"{assets}/{g['foto']}", dur, etiqueta=g.get("etiqueta"), foco=tuple(g.get("foco", (0.5, 0.5))))
    if t == "comparacion":
        return A.g_comparacion(("🚕", "Pagar Uber", "cada vez que lo usas"), ("🚗", "Carro propio", "pagas una sola vez"),
                               dur, f"{assets}/logo_uber.png")
    if t == "iaia":
        return A.g_ia_crea_ia(dur)
    if t == "hacker":
        return A.g_hacker(dur, g.get("total", 81), g.get("etiqueta", "fallas graves encontradas"), g.get("titulo", "IA HACKER"),
                          f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None)
    if t == "fuga":
        return A.g_fuga(dur, f"{assets}/logo_{g['de']}.png", f"{assets}/logo_{g['a']}.png", g.get("personas", 3), g["texto"], g["titulo"])
    if t == "versus":
        lado = lambda l: (l[0], f"{assets}/logo_{l[1]}.png" if l[1] else None, l[2] if len(l) > 2 else None)
        return A.g_versus(dur, lado(g["izq"]), lado(g["der"]), g["sello"], g.get("titulo", "DEMANDA"))
    if t == "lluvia":
        return A.g_lluvia(dur, g["total"], g["etiqueta"], g["titulo"])
    if t == "carrera":
        return A.g_carrera(dur, g["a"], g["b"], g["pregunta"])
    if t == "precio":
        return A.g_precio(dur, g["precio"], g["sub"], f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None)
    if t == "billetes":
        return A.g_billetes(dur, g.get("hasta", 3000), g.get("titulo", "LO QUE PIDEN LAS DISQUERAS"))
    if t == "anuncio":
        return A.g_anuncio(dur, f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None, g.get("titulo", "YA ESTÁ EN GOOGLE ADS"))
    if t == "igual":
        return A.g_igual(dur, g.get("izq", "☕"), g.get("der", "🎬"), g["texto"], g["sub"])
    if t == "hack_banco":
        return A.g_hack_banco(dur, g.get("hasta", 1_000_000), g.get("titulo", "IAs ATACANDO BANCOS"))
    if t == "swat":
        return A.g_swat(dur, g.get("titulo", "EL SWAT DE LA IA"), g.get("sub", "Estados Unidos"))
    if t == "paises":
        return A.g_paises(dur, g.get("titulo", "ALERTA EN LOS BANCOS"))
    if t == "itinerario":
        return A.g_itinerario(dur, f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None, g.get("titulo", "TU AGENTE DE VIAJES CON IA"))
    if t == "resumen_ia":
        return A.g_resumen_ia(dur, g.get("porcentaje", -7.4), g.get("titulo", "LA IA DE GOOGLE VS. USA TODAY"))
    if t == "app":
        return A.g_app(dur, g.get("titulo", "CURSOR CREA LA APP COMPLETA"), g.get("pedido", "Hazme una app de reservas"))
    if t == "transicion":
        return A.g_transicion(dur)
    raise ValueError(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", required=True)
    ap.add_argument("--edl", required=True)
    ap.add_argument("--trozos", required=True)
    ap.add_argument("--assets", required=True)
    ap.add_argument("--salida", default="salida")
    ap.add_argument("--nombre", default="v1 1.1 noticias-dia-1.mp4")
    ap.add_argument("--mirada", help="JSON de mirada.py: recorta los bordes donde no se mira a cámara")
    ap.add_argument("--umbral-mirada", type=float, default=1.0)
    ap.add_argument("--congelar-max", type=float, default=0.5, help="máx. s de imagen sostenida en cada borde")
    ap.add_argument("--musica", help="WAV de música de fondo (48 kHz estéreo)")
    ap.add_argument("--musica-db", type=float, default=-21.0, help="nivel de la música bajo la voz (dB)")
    ap.add_argument("--centro-y", type=float, default=0.5)
    ap.add_argument("--zoom-base", type=float, default=1.0)
    ap.add_argument("--centro-x", type=float, default=0.53)
    a = ap.parse_args()
    editar.CENTRO_X = a.centro_x
    editar.CENTRO_Y = a.centro_y
    editar.ZOOM_BASE = a.zoom_base

    edl = json.loads(Path(a.edl).read_text(encoding="utf-8"))
    CLAVES_EXTRA.update(normalizar(c) for c in edl.get("claves", []))
    clips = sorted(p for p in Path(a.videos).iterdir() if p.suffix.lower() == ".mp4")
    cod = {re.search(r"_(\d{4})_", c.name).group(1): i for i, c in enumerate(clips)}
    infos = [probar(c) for c in clips]
    trozos = {i: json.loads((Path(a.trozos) / f"{c.stem}.json").read_text()) for i, c in enumerate(clips)}
    print("· Detectando voz en cada clip…", flush=True)
    vad = {i: voz_vad(c) for i, c in enumerate(clips)}
    mir_json = json.loads(Path(a.mirada).read_text()) if a.mirada else None
    rangos = [(c["desde"], c["hasta"]) for s_ in edl["secciones"] for c in s_["cortes"]]
    mir = mirada_mala(mir_json, a.umbral_mirada, 0.1, rangos) if mir_json else None
    salida = Path(a.salida)
    tmp = salida / "_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    # ---------------------------------------------------------------- 1. plan de cortes
    from editar_edl import alinear, palabras_de
    zooms = [1.0, 1.1, 1.04, 1.15]
    plan, secs = [], []
    for s in edl["secciones"]:
        sec = {"titulo": s["titulo"], "tipo": s["tipo"], "etiqueta": s.get("etiqueta", ""), "piezas": []}
        secs.append(sec)
        for k, c in enumerate(s["cortes"]):
            ci = cod[c["clip"]]
            ini, fin = max(0.0, c["desde"] - PRE), min(infos[ci]["dur"], c["hasta"] + POST)
            ws = alinear(c["texto"], palabras_de(trozos[ci], c["desde"], c["hasta"]), c["desde"], c["hasta"])
            acum, zoom = 0.0, 1.0 if k == 0 else zooms[len(plan) % len(zooms)]
            tramos = tramos_con_voz(ini, fin, vad[ci])
            if mir is not None:
                tramos = recortar_mirada(tramos, palabras_de(trozos[ci], c["desde"], c["hasta"]), mir)
            # cada palabra va al tramo más cercano (ninguna se pierde) y se ajusta a sus bordes
            asignadas = {i: [] for i in range(len(tramos))}
            for w in ws:
                m = (w["s"] + w["e"]) / 2
                i = min(range(len(tramos)), key=lambda i: 0 if tramos[i][0] <= m <= tramos[i][1]
                        else min(abs(m - tramos[i][0]), abs(m - tramos[i][1])))
                x, y = tramos[i]
                asignadas[i].append(dict(w, s=min(max(w["s"], x), y - 0.05), e=max(min(w["e"], y), x + 0.05)))
            for i, (x, y) in enumerate(tramos):
                if acum > GRUPO_MAX:
                    zoom, acum = zooms[(zooms.index(zoom) + 1) % len(zooms)], 0.0
                pz = {"seccion": s["titulo"], "clip": ci, "ini": round(x, 3), "fin": round(y, 3), "zoom": zoom,
                      "palabras": asignadas[i]}
                plan.append(pz)
                sec["piezas"].append(pz)
                acum += y - x
    if mir:
        for pz in plan:
            c0 = c1 = 0.0
            for x, y in mir:
                if x <= pz["ini"] + 0.05 and y > pz["ini"]:
                    c0 = max(c0, y - pz["ini"])
                if y >= pz["fin"] - 0.05 and x < pz["fin"]:
                    c1 = max(c1, pz["fin"] - x)
            largo = pz["fin"] - pz["ini"]
            c0 = c0 if c0 <= a.congelar_max else 0.0
            c1 = c1 if c1 <= a.congelar_max else 0.0
            if c0 + c1 < largo - 0.3 and (c0 or c1):
                pz["congelar"] = (round(c0, 3), round(c1, 3))
        print(f"· {sum('congelar' in p for p in plan)} bordes con imagen sostenida (mirada)", flush=True)
    print(f"· {len(plan)} piezas · {sum(p['fin'] - p['ini'] for p in plan):.1f} s", flush=True)

    # ---------------------------------------------------------------- 2. video base
    base = editar.render(plan, clips, infos, tmp / "piezas")
    base_cola = tmp / "base_cola.mov"
    # cola del CTA: congela un cuadro de ~0,35 s antes del final (mirando a cámara), no el último
    total_base = sum(p["dur_real"] for p in plan)
    foto = tmp / "cola.png"
    ffmpeg("-ss", f"{max(0, total_base - 0.35):.3f}", "-i", str(base), "-frames:v", "1", str(foto))
    ffmpeg("-i", str(base), "-loop", "1", "-t", f"{COLA_CTA}", "-framerate", str(editar.FPS), "-i", str(foto),
           "-f", "lavfi", "-t", f"{COLA_CTA}", "-i", "anullsrc=r=48000:cl=stereo",
           "-filter_complex", "[1:v]format=yuv420p,setsar=1[f];[0:v][0:a][f][2:a]concat=n=2:v=1:a=1[v][a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
           "-c:a", "pcm_s16le", str(base_cola))

    # ---------------------------------------------------------------- 3. línea de tiempo
    t = 0.0
    for pz in plan:
        pz["o_ini"] = t
        pz["palabras_o"] = [dict(w, s=t + max(0.0, w["s"] - pz["ini"]), e=t + min(pz["fin"], w["e"]) - pz["ini"])
                            for w in pz["palabras"]]
        t += pz["dur_real"]
        pz["o_fin"] = t
    total = t
    for sec in secs:
        sec["ini"], sec["fin"] = sec["piezas"][0]["o_ini"], sec["piezas"][-1]["o_fin"]
        sec["palabras"] = [w for p in sec["piezas"] for w in p["palabras_o"]]

    def mapear(ci, ts):
        """Segundo del clip crudo → segundo del video final."""
        cand = [p for p in plan if p["clip"] == ci and p["fin"] >= ts]
        p = min(cand, key=lambda p: p["ini"]) if cand else None
        return p["o_ini"] + max(0.0, ts - p["ini"]) if p else None

    # ---------------------------------------------------------------- 4. gráficos
    eventos, sfx = [], []
    for sec, s in zip(secs, edl["secciones"]):
        if sec["tipo"] == "noticia":
            eventos.append((sec["ini"] - 0.16, 0.32, {"tipo": "transicion"}))
        for g in s.get("graficos", []):
            if "cubrir" in g:
                cu = g["cubrir"]
                t0, t1 = mapear(cod[cu["clip"]], cu["desde"]), mapear(cod[cu["clip"]], cu["hasta"])
                eventos.append((t0, max(0.8, t1 - t0), g))
                continue
            objetivo = normalizar(g["en"])
            hits = [w for w in sec["palabras"] if normalizar(w["w"]) == objetivo]
            if len(hits) < g.get("n", 1):
                print(f"  ! no encontré «{g['en']}» (n={g.get('n', 1)}) en {sec['titulo']}")
                continue
            eventos.append((hits[g.get("n", 1) - 1]["s"] + g.get("offset", 0.0), g["dur"], g))
    cta_ini = total - 0.1  # la pregunta aparece justo cuando termina de hablar
    eventos.append((cta_ini + 0.15, COLA_CTA - 0.1, {"tipo": "emoji", "ch": edl.get("cta_emoji", "💬"), "x": 870, "y": 840,
                                                    "tam": 200}))
    graficos = []
    for i, (t0, dur, g) in enumerate(sorted(eventos, key=lambda e: e[0])):
        t0 = max(0.0, t0)
        gr = construir(g, dur, a.assets)
        x, y, w, h = gr.caja
        if w < A.W:  # no es pantalla completa → dentro de la zona segura de Instagram
            m = 0.12  # las cajas traen margen transparente alrededor del dibujo
            x = int(min(max(x, 120 - w * m), 960 - w * (1 - m)))
            y = int(min(max(y, 250 - h * m), 1500 - h * (1 - m)))
            gr.caja = (x, y, w, h)
        ruta = gr.render(tmp / f"graf_{i:02d}.mov")
        graficos.append((t0, gr.caja, ruta))
        if gr.sonido:
            sfx.append((t0, gr.sonido))
    print(f"· {len(graficos)} gráficos animados", flush=True)

    # ---------------------------------------------------------------- 5. subtítulos
    ass = salida / "subtitulos_v2.ass"
    palabras = [w for p in plan for w in p["palabras_o"]]
    ass_v2(palabras, secs, edl.get("gancho_texto"), (cta_ini, total + COLA_CTA, edl["cta"]), ass)

    # ---------------------------------------------------------------- 6. audio: voz + efectos
    pcm = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(base_cola), "-vn", "-ac", "2",
                          "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    voz = np.frombuffer(pcm, np.int16).astype(np.float32).reshape(-1, 2) / 32768
    mezcla = voz.copy()
    if a.musica:
        mezcla += musica_de_fondo(a.musica, voz, a.musica_db)
    banco = A.sonidos(SR)
    for t0, nombre in sfx:
        s = banco[nombre] * GANANCIA_SFX.get(nombre, 0.3)
        i0 = int(t0 * SR)
        i1 = min(len(mezcla), i0 + len(s))
        if i0 < i1:
            mezcla[i0:i1] += s[: i1 - i0, None]
    mezcla = np.clip(mezcla, -1, 1)
    wav = tmp / "mezcla.wav"
    with wave.open(str(wav), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((mezcla * 32767).astype(np.int16).tobytes())

    # ---------------------------------------------------------------- 7. composición
    entradas = ["-i", str(base_cola)]
    filtros, ult = [], "[0:v]"
    for k, (t0, (x, y, w, h), ruta) in enumerate(graficos, start=1):
        entradas += ["-i", str(ruta)]
        filtros.append(f"[{k}:v]setpts=PTS-STARTPTS+{t0:.3f}/TB[g{k}]")
        filtros.append(f"{ult}[g{k}]overlay={x}:{y}:eof_action=pass:format=auto[v{k}]")
        ult = f"[v{k}]"
    ass_esc = str(ass).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    filtros.append(f"{ult}ass='{ass_esc}',format=yuv420p[vout]")
    entradas += ["-i", str(wav)]
    script = tmp / "filtros.txt"
    script.write_text(";\n".join(filtros))
    compuesto = tmp / "compuesto.mov"
    print("· Componiendo…", flush=True)
    ffmpeg(*entradas, "-filter_complex_script", str(script), "-map", "[vout]", "-map", f"{len(graficos) + 1}:a",
           "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-c:a", "pcm_s16le", "-t", f"{total + COLA_CTA:.3f}",
           str(compuesto))

    # ---------------------------------------------------------------- 8. exportar
    print("· Exportando…", flush=True)
    dur, mb = editar.exportar(compuesto, None, salida / a.nombre)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ {a.nombre}: {dur:.1f} s · {mb:.1f} MB · {len(plan)} cortes · {len(graficos)} gráficos")
    for sec in secs:
        print(f"  {sec['ini']:5.1f}s  {sec['titulo']}")


if __name__ == "__main__":
    main()
