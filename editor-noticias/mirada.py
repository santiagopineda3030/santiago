"""Mide, cuadro a cuadro (10 por segundo), si la persona mira a la cámara.
Usa YuNet (OpenCV): ojos, nariz y boca → giro (yaw) e inclinación (pitch) de la cabeza.
Uso: python3 mirada.py crudos/clip.MP4 salida/mirada-clip.json"""
import json, subprocess, sys
import cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
FPS = 10
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from editar import probar
_info = probar(src)  # ancho/alto ya girados según la rotación del celular
W, H = (960, 540) if _info["w"] >= _info["h"] else (540, 960)  # respeta vertical u horizontal
det = cv2.FaceDetectorYN.create(str(__import__('pathlib').Path(__file__).with_name('modelos') / 'yunet.onnx'), '', (W, H), 0.6)
rangos = json.loads(sys.argv[3]) if len(sys.argv) > 3 else [[0, None]]  # opcional: [[desde, hasta], ...] en segundos
res = []
for a, b in rangos:
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a), "-i", src] + (["-t", str(b - a)] if b else []) + [
        "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    i = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        t = round(a + i / FPS, 2)
        _, caras = det.detect(f)
        if caras is None:
            res.append({"t": t, "cara": False})
        else:
            c = max(caras, key=lambda c: c[2] * c[3])
            ojo_d, ojo_i, nariz, boca_d, boca_i = c[4:14].reshape(5, 2)
            ojos = (ojo_d + ojo_i) / 2; boca = (boca_d + boca_i) / 2
            de = np.linalg.norm(ojo_d - ojo_i)
            res.append({"t": t, "cara": True, "yaw": float((nariz[0] - ojos[0]) / de),
                        "pitch": float((nariz[1] - ojos[1]) / max(1e-3, boca[1] - ojos[1])), "conf": float(c[14])})
        i += 1
i = len(res)
json.dump(res, open(out, "w"))
print(f"{i} cuadros · cara en {sum(r['cara'] for r in res)}")
