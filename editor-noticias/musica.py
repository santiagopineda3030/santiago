"""Música de fondo ORIGINAL (sintetizada aquí, sin derechos de terceros): lo-fi tranquilo e informativo.
Acordes suaves + arpegio tipo pluck + bajo + ritmo ligero, ~88 BPM.
Uso: python3 musica.py salida.wav 80   (segundos)"""
import sys, wave
import numpy as np
SR = 48000
ruta, dur = sys.argv[1], float(sys.argv[2])
bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 88
ENERGIA = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0  # >1: bombo/aro/hi-hat más marcados
beat = 60 / bpm; n = int(dur * SR)
t = np.arange(n) / SR
rng = np.random.default_rng(3)
out = np.zeros((n, 2))

def nota(m): return 440 * 2 ** ((m - 69) / 12)
def env(d, a=0.01, r=0.3):
    k = np.arange(int(d * SR)) / SR
    return np.minimum(1, k / a) * np.exp(-k / r)
def poner(sig, ini, pan=0.0, g=1.0):
    i = int(ini * SR); j = min(n, i + len(sig))
    if i >= n: return
    s = sig[: j - i] * g
    out[i:j, 0] += s * (1 - pan) ; out[i:j, 1] += s * (1 + pan)

# progresión: Fmaj7 – Em7 – Dm7 – Cmaj7 (4 tiempos cada uno)
acordes = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
bajos = [41, 40, 38, 36]
compas = 4 * beat
for c in range(int(dur / compas) + 1):
    t0 = c * compas
    ac, ba = acordes[c % 4], bajos[c % 4]
    # pad: senos suaves con leve desafinación (coro)
    d = compas + 0.6
    k = np.arange(int(d * SR)) / SR
    e = np.minimum(1, k / 0.6) * np.minimum(1, np.maximum(0, (d - k) / 0.6))
    pad = sum(np.sin(2 * np.pi * nota(m) * k) + 0.5 * np.sin(2 * np.pi * nota(m) * 1.003 * k) for m in ac)
    poner(pad * e * 0.05, t0, 0.0)
    # bajo
    kb = np.arange(int(beat * 2 * SR)) / SR
    poner(np.sin(2 * np.pi * nota(ba) * kb) * env(beat * 2, 0.01, 0.5) * 0.22, t0)
    poner(np.sin(2 * np.pi * nota(ba) * kb) * env(beat * 2, 0.01, 0.5) * 0.16, t0 + 2 * beat)
    # arpegio pluck (corcheas), alterna izquierda/derecha
    seq = [ac[0] + 12, ac[1] + 12, ac[2] + 12, ac[3] + 12, ac[2] + 12, ac[1] + 12, ac[3] + 12, ac[2] + 24]
    for i, m in enumerate(seq):
        kp = np.arange(int(0.45 * SR)) / SR
        f = nota(m)
        pl = (np.sin(2 * np.pi * f * kp) + 0.3 * np.sin(4 * np.pi * f * kp)) * env(0.45, 0.003, 0.16)
        poner(pl * 0.06 * (1 + 0.4 * (ENERGIA - 1)), t0 + i * beat / 2, -0.4 if i % 2 else 0.4)
    # ritmo: bombo suave en 1 y 3, aro en 2 y 4, hi-hat en corcheas
    for b in range(4):
        tb = t0 + b * beat
        if b in (0, 2):
            kk = np.arange(int(0.25 * SR)) / SR
            poner(np.sin(2 * np.pi * (55 + 60 * np.exp(-kk * 30)) * kk) * env(0.25, 0.002, 0.08) * 0.35 * ENERGIA, tb)
        else:
            m = int(0.12 * SR)
            poner(rng.standard_normal(m) * env(0.12, 0.001, 0.03) * 0.06 * ENERGIA ** 1.5, tb)
        for h in ((0, 0.25, 0.5, 0.75) if ENERGIA > 1 else (0, 0.5)):
            m = int(0.04 * SR)
            hh = np.diff(rng.standard_normal(m + 1)) * env(0.04, 0.001, 0.012) * 0.025 * ENERGIA ** 1.5
            poner(hh, tb + h * beat, 0.3)
# filtro paso bajo suave (calidez lo-fi) y entrada/salida
a = np.exp(-2 * np.pi * 4500 / SR)
for ch in range(2):
    y = np.zeros(n); prev = 0.0
    x = out[:, ch]
    for i in range(0, n, 4800):  # vectorizado por bloques con lfilter manual
        pass
    from scipy.signal import lfilter
    out[:, ch] = lfilter([1 - a], [1, -a], x)
fade = np.minimum(1, t / 1.5) * np.minimum(1, np.maximum(0, (dur - t) / 2.0))
out *= fade[:, None]
out /= np.abs(out).max() * 1.12
with wave.open(ruta, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", ruta)
