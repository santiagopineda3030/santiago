"""Mide, cuadro a cuadro (10 por segundo), si la persona mira a la cámara.
Usa YuNet (OpenCV): ojos, nariz y boca → giro (yaw) e inclinación (pitch) de la cabeza.
Uso: python3 mirada.py crudos/clip.MP4 salida/mirada-clip.json"""
import json, subprocess, sys
import cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
W, H, FPS = 960, 540, 10
det = cv2.FaceDetectorYN.create(str(__import__('pathlib').Path(__file__).with_name('modelos') / 'yunet.onnx'), '', (W, H), 0.6)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo",
                      "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
res, i = [], 0
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    _, caras = det.detect(f)
    if caras is None:
        res.append({"t": i / FPS, "cara": False})
    else:
        c = max(caras, key=lambda c: c[2] * c[3])
        ojo_d, ojo_i, nariz, boca_d, boca_i = c[4:14].reshape(5, 2)
        ojos = (ojo_d + ojo_i) / 2; boca = (boca_d + boca_i) / 2
        de = np.linalg.norm(ojo_d - ojo_i)
        res.append({"t": i / FPS, "cara": True, "yaw": float((nariz[0] - ojos[0]) / de),
                    "pitch": float((nariz[1] - ojos[1]) / max(1e-3, boca[1] - ojos[1])), "conf": float(c[14])})
    i += 1
json.dump(res, open(out, "w"))
print(f"{i} cuadros · cara en {sum(r['cara'] for r in res)}")
