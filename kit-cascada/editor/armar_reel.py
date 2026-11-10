"""Arma un reel vertical a partir de una grabación de Meet y una especificación JSON.

Uso: python3 armar_reel.py spec.json

La spec trae: video, words (json de faster-whisper con tiempos sobre el video), tramos [ini, fin] en
segundos del video, la caja de la cámara de quien presenta, correcciones de palabras, palabras clave y escenas
(tiempos relativos al tramo: {"tramo": i, "at": seg} o absolutos en el reel con "start"/"end").
"alumno": índices de los tramos en que habla un estudiante: su voz sale distorsionada, su cámara difuminada
y aparece la nota de privacidad.
Salida: el mp4 en la ruta "salida".
La marca (colores, etiqueta, fuente) sale de reglas.json en la raíz del kit.
"""
import json, os, subprocess, sys, tempfile

FPS = 24
AQUI = os.path.dirname(os.path.abspath(__file__))
REGLAS = os.environ.get("CASCADA_REGLAS", os.path.join(AQUI, "..", "reglas.json"))
MARCA = json.load(open(REGLAS)).get("marca", {}) if os.path.exists(REGLAS) else {}
FONDO = MARCA.get("colores", {}).get("fondo", "#16170F").lstrip("#")


def sh(cmd):
    subprocess.run(cmd, check=True)


def redondear(r):
    """Filtro ffmpeg que vuelve transparentes las esquinas (radio r) para pegar el recuadro redondeado."""
    dx, dy = f"max(max({r}-X\\,X-(W-1-{r}))\\,0)", f"max(max({r}-Y\\,Y-(H-1-{r}))\\,0)"
    return (f"format=yuva420p,geq=lum='p(X,Y)':cb='p(X,Y)':cr='p(X,Y)':"
            f"a='if(lte(pow({dx},2)+pow({dy},2),{r * r}),255,0)'")


def alumnos(video, sp, fps=6):
    """Tramos (s) en que el cuadro de cámara NO muestra a quien presenta. Meet pone ahí a quien habla; si quien
    presenta usa un fondo fijo, su color se mide en dos zonas (spec "cam_ref_zonas", lo calcula preparar_tramo.py)."""
    # Dos zonas del fondo (ventana a la izquierda y techo a la derecha): solo es otra persona si cambian
    # las dos, así una mano de quien presenta tapando una zona no difumina nada.
    zonas = sp.get("cam_ref_zonas")
    if not zonas:
        return []
    difs = []
    for (rx, ry, rw, rh), ref in zonas:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", video, "-vf",
                              f"fps={fps},crop={rw}:{rh}:{rx}:{ry},scale=1:1", "-f", "rawvideo",
                              "-pix_fmt", "rgb24", "-"], check=True, capture_output=True).stdout
        difs.append([sum(abs(raw[3 * i + k] - ref[k]) for k in range(3)) > 30 for i in range(len(raw) // 3)])
    malos = [i / fps for i in range(min(map(len, difs))) if all(d[i] for d in difs)]
    tramos = []
    for t in malos:                      # agrupa cuadros seguidos, con medio segundo de margen
        if tramos and t - tramos[-1][1] <= 0.5:
            tramos[-1][1] = t
        else:
            tramos.append([t, t])
    return [(max(0, a - 0.4), b + 0.5) for a, b in tramos]


def caras_alumno(video, cam, tramos, fps=3):
    """Caja de la cara del estudiante (en coordenadas del video) para cada tramo en que se ve: así se difumina
    solo la carita y no toda la cámara. None si no se encuentra la cara (entonces se difumina toda la cámara)."""
    import cv2
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    x, y, w, h = cam
    cajas = []
    for a, b in tramos:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{max(0, a):.2f}", "-t", f"{b - max(0, a):.2f}",
                              "-i", video, "-vf", f"fps={fps},crop={w}:{h}:{x}:{y},format=gray", "-f", "rawvideo", "-"],
                             check=True, capture_output=True).stdout
        import numpy as np
        caras = []
        for i in range(len(raw) // (w * h)):
            img = np.frombuffer(raw[i * w * h:(i + 1) * w * h], np.uint8).reshape(h, w)
            caras += [tuple(c) for c in det.detectMultiScale(img, 1.1, 5, minSize=(h // 5, h // 5))]
        if not caras:
            cajas.append(None)
            continue
        med = lambda k: sorted(c[k] for c in caras)[len(caras) // 2]     # cara típica (no la suma de todas)
        cx, cy, cw, chh = med(0), med(1), med(2), med(3)
        bx0, by0 = max(0, int(cx - cw * 0.15)), max(0, int(cy - chh * 0.2))    # margen corto: pelo y mentón
        bx1, by1 = min(w, int(cx + cw * 1.15)), min(h, int(cy + chh * 1.15))
        cajas.append([bx0 // 2 * 2, by0 // 2 * 2, (bx1 - bx0) // 2 * 2, (by1 - by0) // 2 * 2])
    return cajas


def main(spec_path):
    sp = json.load(open(spec_path))
    tmp = tempfile.mkdtemp(prefix="reel_")
    tramos, cola = sp["tramos"], sp.get("cola", 1.5)
    alumno = set(sp.get("alumno", []))
    sr = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate",
                             "-of", "csv=p=0", sp["video"]], check=True, capture_output=True, text=True).stdout.strip())

    # 1) Cortes pegados, con fundido corto de audio para que no se oigan saltos.
    f, parts, offs, t = [], "", [], 0.0
    for i, (a, b) in enumerate(tramos):
        d = b - a
        f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
        # Voz del estudiante: más grave y con un leve temblor, a la misma velocidad (no se reconoce, se entiende).
        voz = f",asetrate={sr * 0.8:.0f},aresample={sr},atempo=1.25,vibrato=f=6:d=0.15" if i in alumno else ""
        f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS{voz},afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06[a{i}]")
        parts += f"[v{i}][a{i}]"
        offs.append(t)
        t += d
    total = t + cola
    f.append(f"{parts}concat=n={len(tramos)}:v=1:a=1[vc][ac]")
    f.append(f"[vc]tpad=stop_mode=clone:stop_duration={cola}[v]")
    f.append(f"[ac]apad=pad_dur={cola}[a]")
    corte = os.path.join(tmp, "corte.mp4")
    sh(["ffmpeg", "-loglevel", "error", "-y", "-i", sp["video"], "-filter_complex", ";".join(f),
        "-map", "[v]", "-map", "[a]", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-c:a", "aac", corte])

    # 2) Palabras del reel con tiempos nuevos.
    fix, keys = sp.get("correcciones", {}), {k.lower() for k in sp.get("clave", [])}
    words = []
    for w in json.load(open(sp["words"])):
        for i, (a, b) in enumerate(tramos):
            if w["start"] >= a - 0.05 and w["end"] <= b + 0.15:
                txt = fix.get(f'{w["start"]}', w["w"])
                if not txt:
                    continue
                words.append({"w": txt, "start": round(w["start"] - a + offs[i], 2),
                              "end": round(min(w["end"], b) - a + offs[i], 2),
                              "key": txt.lower().strip(".,:;¿?¡!") in keys, "al": i in alumno})
    words.sort(key=lambda w: w["start"])
    for i in range(len(words) - 1, 0, -1):   # whisper parte "e-commerce" en "e" + "-commerce"
        if words[i]["w"].startswith("-"):
            words[i - 1]["w"] += words[i]["w"]
            words[i - 1]["end"] = words[i]["end"]
            words[i - 1]["key"] = words[i - 1]["key"] or words[i]["key"]
            del words[i]

    # 3) Escenas: "tramo"+"at" se vuelve tiempo absoluto del reel.
    def abs_t(v):
        return offs[v["tramo"]] + v["at"] if isinstance(v, dict) else v
    scenes = []
    for s in sp["escenas"]:
        s = dict(s)
        s["start"] = abs_t(s["start"])
        if "end" in s:
            s["end"] = abs_t(s["end"])
        scenes.append(s)
    priv = [(offs[i], offs[i] + tramos[i][1] - tramos[i][0]) for i in sorted(alumno)]
    tl = os.path.join(tmp, "tl.json")
    # Diseño con presentación: (gancho fijo) + diapositivas + quien presenta + tarjeta + subtítulos, todo dentro de la
    # zona segura de Instagram (x 120–960, y 250–1500). Cámara y presentación con esquinas redondeadas y borde.
    pres = sp.get("presentacion")       # [x, y, w, h] de las diapositivas dentro del cuadro de Meet
    enc = sp.get("encuadres")           # videos de YouTube: [{"desde": t, "caja": [x, y, w, h]}] del video original
    fijo = any(e["type"] == "hook" and e.get("fixed") for e in scenes)
    extra = {}
    if enc:
        # Un recuadro de 840 de ancho (máx. 760 de alto) centrado en la franja y 420–1180; cada encuadre dura
        # hasta que empieza el siguiente. Debajo, tarjeta y subtítulos.
        cajas = []
        for i, e in enumerate(enc):
            t0 = abs_t(e["desde"])
            t1 = abs_t(enc[i + 1]["desde"]) if i + 1 < len(enc) else total
            cx, cy, cw, ch = e["caja"]
            bw, bh = 840, 840 * ch / cw
            if bh > 760:
                bw, bh = 760 * cw / ch, 760
            bw, bh = int(round(bw / 2) * 2), int(round(bh / 2) * 2)
            cajas.append([(1080 - bw) // 2, 420 + (760 - bh) // 2, bw, bh, round(t0, 3), round(t1, 3)])
        card_top, subs_top = 1192, 1350
        extra = {"cajas": cajas, "subsGroup": 3}
    elif pres:
        x, y, w, h = sp["camara"]
        pres_w = sp.get("pres_w", 840)
        pres_h = int(round(pres_w * pres[3] / pres[2] / 2) * 2)
        pres_y = 414 if fijo else 260
        cw = sp.get("cam_w", 600 if fijo else 720)
        ch = int(round(cw * h / w / 2) * 2)
        cam_y = pres_y + pres_h + 16
        card_top = cam_y + ch + 12
        subs_top = card_top + 166
        cajas = [[(1080 - pres_w) // 2, pres_y, pres_w, pres_h], [(1080 - cw) // 2, cam_y, cw, ch]]
        extra = {"presTop": pres_y, "presH": pres_h, "cajas": cajas, "subsGroup": 3 if fijo else 4}
    else:
        x, y, w, h = sp["camara"]
        if sp.get("cam_y", "centro") == "centro":    # cámara centrada en la pantalla (diseño por defecto, 5-nov)
            sp["cam_y"] = (1920 - int(round(1080 * h / w / 2) * 2)) // 2 // 2 * 2
        card_top, subs_top = 270, None
        if fijo:    # el gancho fijo ocupa arriba: tarjeta y subtítulos van debajo de la cámara
            ch = int(round(1080 * h / w / 2) * 2)
            card_top = sp.get("cam_y", 600) + ch + 12
            subs_top = card_top + 166
            extra = {"subsGroup": 3, "hookBottom": 1920 - sp.get("cam_y", 600) + 26}   # gancho pegado a la cámara
    if priv and not enc:   # nota de privacidad sobre el borde inferior de la cámara
        extra["privTop"] = (cam_y + ch - 58) if pres else sp.get("cam_y", 600) + int(round(1080 * h / w / 2) * 2) - 70
    scenes += [{"type": "priv", "start": a, "end": b} for a, b in priv]
    json.dump({"duration": total, "words": words, "scenes": scenes, "cardTop": card_top, "subsTop": subs_top,
               "marca": MARCA, **extra}, open(tl, "w"), ensure_ascii=False)
    frames = os.path.join(tmp, "frames")
    sh(["node", os.path.join(AQUI, "render", "render.js"), tl, frames, str(FPS)])

    # 4) Composición vertical: fondo difuminado + cámara + animaciones encima.
    # Si la spec marca dónde habla el estudiante, eso manda (la detección por color se pasa con el cambio de cámara).
    blur = [(a - 0.1, b + 0.1) for a, b in priv] if priv else alumnos(corte, sp)
    if blur:
        print("alumno en cámara (se difumina):", blur)
    en = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in blur)
    caras = f",boxblur=40:6:enable='{en}'" if blur else ""
    # Solo la cara del estudiante: se difumina un recuadro sobre su carita; si no se encuentra, toda la cámara.
    zonas = caras_alumno(corte, sp["camara"], blur) if blur and not enc else []
    def cara_borrosa(src):
        """Cadena que recorta la cámara de src y difumina la cara en cada tramo; devuelve (filtros, etiqueta)."""
        x, y, w, h = sp["camara"]
        out = f"{src}crop={w}:{h}:{x}:{y}[q0];"
        for i, ((a, b), (bx, by, bw, bh)) in enumerate(zip(blur, zonas)):
            out += (f"[q{i}]split[q{i}a][q{i}b];[q{i}b]crop={bw}:{bh}:{bx}:{by},boxblur=22:4[z{i}];"
                    f"[q{i}a][z{i}]overlay={bx}:{by}:enable='between(t,{a:.2f},{b:.2f})'[q{i + 1}];")
        return out, f"[q{len(zonas)}]"
    solo_cara = bool(zonas) and all(zonas)
    if solo_cara:
        caras = ""
        print("cara del estudiante (se difumina solo ahí):", zonas)
    # El fondo sale de la cámara ampliada: mientras se ve a un estudiante se tapa con el color base de la marca.
    fondo = f",drawbox=x=0:y=0:w=iw:h=ih:color=0x{FONDO}@1:t=fill:enable='{en}'" if blur else ""
    if sp.get("fondo", "negro") == "negro":     # fondo negro liso todo el video (diseño por defecto, 5-nov)
        fondo = ",drawbox=x=0:y=0:w=iw:h=ih:color=black@1:t=fill"
    if enc:
        r = redondear(26)
        comp = (f"[0:v]split={len(enc) + 1}[s0]{''.join(f'[s{i + 1}]' for i in range(len(enc)))};"
                f"[s0]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.35[b0];")
        for i, (e, (bx, by, bw, bh, t0, t1)) in enumerate(zip(enc, cajas)):
            cx, cy, cw, ch = e["caja"]
            sale = "b" if i == len(enc) - 1 else f"b{i + 1}"
            comp += (f"[s{i + 1}]crop={cw}:{ch}:{cx}:{cy},scale={bw}:{bh}:flags=lanczos,{r}[k{i}];"
                     f"[b{i}][k{i}]overlay={bx}:{by}:enable='gte(t,{t0})*lt(t,{t1})'[{sale}];")
    elif pres:
        px, py, pw, ph = pres
        r = redondear(26)
        comp = (f"[0:v]split=3[s1][s2][s3];"
                f"[s1]crop={w}:{h}:{x}:{y},scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.35{fondo}[bg];"
                f"[s2]crop={pw}:{ph}:{px}:{py},scale={pres_w}:{pres_h}:flags=lanczos,{r}[pr];"
                + (cara_borrosa("[s3]")[0] + cara_borrosa("[s3]")[1] if solo_cara else f"[s3]crop={w}:{h}:{x}:{y},") +
                f"scale={cw}:{ch}:flags=lanczos,unsharp=5:5:0.6{caras},{r}[cam];"
                f"[bg][pr]overlay={(1080 - pres_w) // 2}:{pres_y}[b0];"
                f"[b0][cam]overlay={(1080 - cw) // 2}:{cam_y}[b];")
    else:
        ch = int(round(1080 * h / w / 2) * 2)
        comp = ((cara_borrosa("[0:v]")[0] + cara_borrosa("[0:v]")[1] if solo_cara else f"[0:v]crop={w}:{h}:{x}:{y},") +
                f"split[c1][c2];"
                f"[c1]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.25{fondo}[bg];"
                f"[c2]scale=1080:{ch}:flags=lanczos,unsharp=5:5:0.6{caras}[cam];"
                f"[bg][cam]overlay=0:{sp.get('cam_y', 600)}[b];")
    comp += (f"[1:v]format=rgba[ov];[b][ov]overlay=0:0:shortest=1,format=yuv420p[v];"
             f"[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    sh(["ffmpeg", "-loglevel", "error", "-y", "-i", corte, "-framerate", str(FPS),
        "-i", os.path.join(frames, "f%05d.png"), "-filter_complex", comp, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", sp["salida"]])
    print("listo:", sp["salida"], f"({total:.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
