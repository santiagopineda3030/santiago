"""Música ORIGINAL estilo synthwave / cyberpunk (sintetizada aquí, sin derechos de terceros). 9 nov, v5.
Bajo pulsante en corcheas, arpegio de sierra en semicorcheas, pad oscuro, bombo en negras, caja con eco.
Uso: python3 musica_cyber.py salida.wav <segundos> [bpm=112]"""
import sys
import wave

import numpy as np
from scipy.signal import butter, lfilter

SR = 48000
ruta, dur = sys.argv[1], float(sys.argv[2])
bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 112
beat = 60 / bpm
n = int(dur * SR) + SR
out = np.zeros((n, 2))
rng = np.random.default_rng(11)


def nota(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR
    s = 2 * ((t * f) % 1) - 1
    if det:
        s = 0.5 * s + 0.5 * (2 * ((t * f * (1 + det)) % 1) - 1)
    return s


def env(d, a=0.005, r=0.2, sus=0.0):
    k = np.arange(int(d * SR)) / SR
    return np.minimum(1, k / a) * (sus + (1 - sus) * np.exp(-k / r))


def lp(x, fc, orden=2):
    b, a = butter(orden, min(0.99, fc / (SR / 2)))
    return lfilter(b, a, x)


def hp(x, fc):
    b, a = butter(2, fc / (SR / 2), "high")
    return lfilter(b, a, x)


def poner(sig, ini, pan=0.0, g=1.0):
    i = int(ini * SR)
    j = min(n, i + len(sig))
    if i >= n or j <= i:
        return
    s = sig[: j - i] * g
    out[i:j, 0] += s * (1 - pan)
    out[i:j, 1] += s * (1 + pan)


# Am – F – C – G (menor, oscuro), 1 compás cada acorde
acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
bajos = [33, 29, 36, 31]
compas = 4 * beat
ncomp = int(dur / compas) + 1
for c in range(ncomp):
    t0 = c * compas
    k = c % 4
    # pad (sierra desafinada, filtrada)
    pad = sum(saw(nota(m), compas, 0.006) for m in acordes[k]) / 3
    pad = lp(pad, 900) * env(compas, 0.25, 9, 0.85)
    poner(pad, t0, 0.0, 0.16)
    # bajo en corcheas
    for e in range(8):
        b = lp(saw(nota(bajos[k]), beat / 2 * 0.9), 380) * env(beat / 2 * 0.9, 0.003, 0.12, 0.3)
        poner(b, t0 + e * beat / 2, 0.0, 0.42)
    # arpegio en semicorcheas (entra desde el compás 2)
    if c >= 1:
        arp = [acordes[k][0] + 12, acordes[k][1] + 12, acordes[k][2] + 12, acordes[k][1] + 24]
        for s in range(16):
            m = arp[s % 4]
            x = lp(saw(nota(m), beat / 4 * 0.8), 2600) * env(beat / 4 * 0.8, 0.002, 0.06)
            pan = 0.35 if s % 2 else -0.35
            poner(x, t0 + s * beat / 4, pan, 0.11)
            poner(x, t0 + s * beat / 4 + beat * 0.75, -pan, 0.045)  # eco
    # batería
    for b in range(4):
        tb = t0 + b * beat
        kk = int(0.3 * SR)
        tt = np.arange(kk) / SR
        f = 45 + 110 * np.exp(-tt * 28)
        kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
        poner(kick, tb, 0, 0.75)
        if b in (1, 3):
            m = int(0.25 * SR)
            sn = hp(rng.standard_normal(m), 900) * env(0.25, 0.001, 0.07)
            sn += 0.3 * np.sin(2 * np.pi * 190 * np.arange(m) / SR) * env(0.25, 0.001, 0.05)
            poner(sn, tb, 0, 0.32)
            poner(sn, tb + beat * 0.5, 0.3, 0.07)
        for h in (0.5,):
            m = int(0.05 * SR)
            hh = hp(rng.standard_normal(m), 7000) * env(0.05, 0.001, 0.015)
            poner(hh, tb + h * beat, 0.2, 0.16)

# entrada y salida suaves
fade = int(1.0 * SR)
out[:fade] *= np.linspace(0, 1, fade)[:, None]
out = out[: int(dur * SR)]
out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out /= np.abs(out).max() / 0.8
with wave.open(ruta, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", ruta, dur, "s")
