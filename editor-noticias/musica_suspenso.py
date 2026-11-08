"""Música de SUSPENSO original (sintetizada aquí, sin derechos de terceros) para el gancho.
Zumbido grave + latido + tic-tac + cuerdas tensas que suben + subida de tensión al final.
Uso: python3 musica_suspenso.py salida.wav 14"""
import sys, wave
import numpy as np
from scipy.signal import lfilter
SR = 48000
ruta, dur = sys.argv[1], float(sys.argv[2])
n = int(dur * SR); t = np.arange(n) / SR
rng = np.random.default_rng(4)
out = np.zeros((n, 2))
# zumbido grave (re menor) con batido lento
dr = (np.sin(2 * np.pi * 36.7 * t) + 0.6 * np.sin(2 * np.pi * 55.0 * t) + 0.3 * np.sin(2 * np.pi * 73.4 * 1.004 * t))
dr *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.25 * t)
out += (dr * 0.22)[:, None]
# cuerdas tensas: segunda menor aguda que sube de volumen
cu = np.sin(2 * np.pi * 587.3 * t) + np.sin(2 * np.pi * 622.3 * t)
cu = lfilter([0.05], [1, -0.95], cu) * 6
out += (cu * 0.05 * (t / dur) ** 1.5)[:, None] * np.array([[1.0, 0.8]])
# latido (doble golpe) cada 0,85 s, acelerando
tb = 0.4
while tb < dur - 0.3:
    for off, g in ((0, 1.0), (0.17, 0.7)):
        i = int((tb + off) * SR); k = np.arange(int(0.25 * SR)) / SR
        s = np.sin(2 * np.pi * (48 + 40 * np.exp(-k * 25)) * k) * np.exp(-k * 14) * 0.55 * g
        j = min(n, i + len(s)); out[i:j] += s[: j - i, None]
    tb += max(0.5, 0.85 - 0.025 * tb)
# tic-tac de reloj
for k in range(int(dur * 2)):
    i = int((0.2 + k * 0.5) * SR); m = int(0.015 * SR)
    if i + m < n:
        c = rng.standard_normal(m) * np.exp(-np.arange(m) / (0.003 * SR)) * (0.07 if k % 2 else 0.05)
        out[i:i + m, 0 if k % 2 else 1] += c
# subida de tensión (ruido que sube) los últimos 2,5 s
r0 = max(0, n - int(2.5 * SR)); rr = rng.standard_normal(n - r0)
f = np.linspace(0, 1, n - r0)
rr = lfilter([1], [1, -0.98], rr) * 0.02 * f ** 2
out[r0:] += rr[:, None]
fade = np.minimum(1, t / 0.6)
out *= fade[:, None]
out /= np.abs(out).max() * 1.1
with wave.open(ruta, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", ruta)
