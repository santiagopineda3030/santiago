"""Mirada con IRIS (MediaPipe FaceLandmarker): detecta si los ojos miran a la cámara o al guion,
aunque la cabeza no se mueva. Guarda por cuadro: v (iris arriba/abajo dentro del ojo), h (izq/der),
pitch y yaw de la cabeza. Uso: python3 mirada_iris.py <video> <salida.json> '[[desde,hasta],...]'"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
sys.path.insert(0, str(Path(__file__).parent))
from editar import probar
src, out = sys.argv[1], sys.argv[2]
rangos = json.loads(sys.argv[3]) if len(sys.argv) > 3 else [[0, None]]
PRE = sys.argv[4] + "," if len(sys.argv) > 4 else ""  # filtro previo (ej. el encuadre del editor) para que la cara salga grande
info = probar(src)
W, H = (960, 540) if info["w"] >= info["h"] else (540, 960)
FPS = 10
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(Path(__file__).with_name("modelos") / "face_landmarker.task")),
    running_mode=vision.RunningMode.IMAGE, num_faces=1, output_facial_transformation_matrixes=True))

def ratio(l, iris, arriba, abajo, a, b):
    v = (l[iris].y - l[arriba].y) / max(1e-6, l[abajo].y - l[arriba].y)
    h = (l[iris].x - l[a].x) / max(1e-6, l[b].x - l[a].x)
    return v, h

res = []
for a, b in rangos:
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a), "-i", src] + (["-t", str(b - a)] if b else []) + [
        "-vf", f"fps={FPS},{PRE}scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    i = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy())
        r = det.detect(img)
        t = round(a + i / FPS, 2); i += 1
        if not r.face_landmarks:
            res.append({"t": t, "cara": False}); continue
        l = r.face_landmarks[0]
        v1, h1 = ratio(l, 468, 159, 145, 33, 133)
        v2, h2 = ratio(l, 473, 386, 374, 362, 263)
        m = np.array(r.facial_transformation_matrixes[0])
        pitch = float(np.degrees(np.arcsin(-m[1, 2])))
        yaw = float(np.degrees(np.arcsin(m[0, 2])))
        abierto = ((l[145].y - l[159].y) + (l[374].y - l[386].y)) / 2 / max(1e-6, abs(l[152].y - l[10].y))
        res.append({"t": t, "cara": True, "v": (v1 + v2) / 2, "h": (h1 + h2) / 2, "pitch": pitch, "yaw": yaw,
                    "abierto": float(abierto)})
json.dump(res, open(out, "w"))
print(f"{len(res)} cuadros · cara en {sum(r['cara'] for r in res)}")
