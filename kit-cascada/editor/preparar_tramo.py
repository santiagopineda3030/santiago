"""Prepara un tramo de una grabación de Meet para armar un reel.

Uso: .venv/bin/python cortes/preparar_tramo.py VIDEO INICIO FIN CARPETA
     (INICIO y FIN en hh:mm:ss o segundos)

Deja en CARPETA: seg.mp4 (el tramo), words.json (palabras con tiempos relativos al tramo),
camara.png (cuadro para revisar el encuadre) y base.json (camara + cam_ref_zonas para la spec).
Imprime la transcripción con tiempos para escoger los cortes.
"""
import json, os, statistics, subprocess, sys

REGLAS = os.environ.get("CASCADA_REGLAS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reglas.json"))
IDIOMA = (json.load(open(REGLAS)).get("grabaciones", {}).get("idioma", "es")) if os.path.exists(REGLAS) else "es"


def seg(v):
    if ":" in str(v):
        h, m, s = (list(map(float, v.split(":"))) + [0, 0])[:3] if v.count(":") == 2 else [0, *map(float, v.split(":"))]
        return h * 3600 + m * 60 + s
    return float(v)


def pixeles(video, vf):
    return subprocess.run(["ffmpeg", "-loglevel", "error", "-i", video, "-vf", vf, "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], check=True, capture_output=True).stdout


def cuadro_camara(video):
    """Cuadro de la cámara de quien habla: el rectángulo con imagen a la derecha del fondo negro de Meet."""
    raw = pixeles(video, "select=eq(n\\,240),scale=1920:1080")[:1920 * 1080 * 3]
    lum = lambda x, y: sum(raw[3 * (y * 1920 + x):3 * (y * 1920 + x) + 3]) / 3
    xs = [x for x in range(1200, 1920) if lum(x, 540) > 25]
    if not xs:
        return None
    cx = (xs[0] + xs[-1]) // 2
    ys = [y for y in range(1080) if lum(cx, y) > 25]
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]
    w, h = x1 - x0, y1 - y0
    # quita la franja izquierda donde Meet escribe el nombre y deja la cara centrada
    cw = int(w * 0.69) // 2 * 2
    # solo la parte de arriba (cara y hombros): así cámara + subtítulos caben en la zona segura de Instagram
    return [x1 - cw, y0 + 10, cw, int(h * 0.78) // 2 * 2], [x0, y0, w, h]


def presentacion(video, x_cam):
    """Diapositivas que comparte quien presenta: la ventana del navegador a la izquierda de su cámara, sin la barra
    de pestañas. Devuelve [x, y, w, h] o None si no está compartiendo pantalla."""
    raw = pixeles(video, "select=eq(n\\,240),scale=1920:1080")[:1920 * 1080 * 3]
    lum = lambda x, y: sum(raw[3 * (y * 1920 + x):3 * (y * 1920 + x) + 3]) / 3
    xs = [x for x in range(0, x_cam - 20) if lum(x, 540) > 6]
    if len(xs) < 600:
        return None
    barra = next((y for y in range(0, 1000) if lum(700, y) > 30), None)     # empieza la barra del navegador
    if barra is None:
        return None
    ys = [y for y in range(barra, 1070) if all(lum(700, y + k) < 20 for k in range(6))]
    if not ys:
        return None
    y_top = ys[0]
    return [40, y_top, (x_cam - 83) // 2 * 2, min(730, 1080 - y_top) // 2 * 2]


def zona_ref(video, zona):
    rx, ry, rw, rh = zona
    raw = pixeles(video, f"fps=1,crop={rw}:{rh}:{rx}:{ry},scale=1:1")
    return [int(statistics.median(raw[k::3])) for k in range(3)]


def main(video, ini, fin, out):
    os.makedirs(out, exist_ok=True)
    a, b = seg(ini), seg(fin)
    s = os.path.join(out, "seg.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-i", video, "-t", str(b - a),
                    "-c", "copy", s], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", s, "-vn", "-ac", "1", "-ar", "16000",
                    os.path.join(out, "seg.wav")], check=True)

    camara, tile = cuadro_camara(s)
    x0, y0, w, h = tile
    zonas = [[x0 + 10, y0 + 24, 60, 150], [x0 + w - 146, y0 + 10, 140, 50]]   # ventana y techo del fondo
    base = {"video": s, "words": os.path.join(out, "words.json"), "camara": camara,
            "cam_ref_zonas": [[z, zona_ref(s, z)] for z in zonas]}
    pres = presentacion(s, x0)
    if pres:
        base["presentacion"] = pres
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "10", "-i", s, "-frames:v", "1", "-vf",
                        "crop={2}:{3}:{0}:{1}".format(*pres), os.path.join(out, "presentacion.png")], check=True)
    json.dump(base, open(os.path.join(out, "base.json"), "w"), indent=1)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "10", "-i", s, "-frames:v", "1", "-vf",
                    f"crop={camara[2]}:{camara[3]}:{camara[0]}:{camara[1]}", os.path.join(out, "camara.png")],
                   check=True)

    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(os.path.join(out, "seg.wav"), language=IDIOMA, word_timestamps=True, vad_filter=True)
    W = [{"w": x.word.strip(), "start": round(x.start, 2), "end": round(x.end, 2)} for sg in segs for x in sg.words]
    json.dump(W, open(base["words"], "w"), ensure_ascii=False)
    print(json.dumps(base))
    print(" ".join(f"[{x['start']:.2f}]{x['w']}" for x in W))


if __name__ == "__main__":
    main(*sys.argv[1:5])
