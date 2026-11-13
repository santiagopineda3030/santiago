"""Sonidos de transición extra (13 nov, E1: Santi pidió variar los sonidos). Sintetizados aquí, sin derechos."""
import numpy as np


def sonidos_extra(sr=48000, base=None):
    rng = np.random.default_rng(13)

    def env(n, ataque=0.02, caida=4.0):
        t = np.linspace(0, 1, n)
        return np.minimum(1, t / max(ataque, 1e-3)) * np.exp(-caida * t)

    # swipe: ruido filtrado que sube de tono (barrido rápido)
    n = int(0.28 * sr)
    ruido = rng.standard_normal(n)
    f = np.linspace(800, 6000, n)
    fase = 2 * np.pi * np.cumsum(f) / sr
    swipe = (0.6 * ruido * np.sin(fase) + 0.4 * np.sin(fase)) * np.hanning(n)
    # boom: golpe grave que decae + clic
    n = int(0.6 * sr)
    t = np.arange(n) / sr
    boom = np.sin(2 * np.pi * (55 - 20 * t) * t) * np.exp(-6 * t)
    boom[: int(0.004 * sr)] += rng.standard_normal(int(0.004 * sr)) * 0.6
    # brillo: campanitas agudas
    n = int(0.5 * sr)
    t = np.arange(n) / sr
    brillo = sum(np.sin(2 * np.pi * fr * t) * np.exp(-(7 + k) * t) for k, fr in enumerate((1760, 2640, 3520, 4400))) / 3
    # whoosh al revés (sube y corta)
    reves = base["whoosh"][::-1].copy() if base and "whoosh" in base else swipe[::-1].copy()
    out = {"swipe": swipe, "boom": boom, "brillo": brillo, "reves": reves}
    return {k: (v / (np.abs(v).max() + 1e-9)).astype(np.float32) for k, v in out.items()}
