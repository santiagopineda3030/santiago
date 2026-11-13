"""Estilo REFERENTE R2 de noticias (13 nov, v9 · Santi: "copiar la edición de ese man, lo más exacto posible", EN ROJO).

Ficha: contexto/referentes-edicion.md › Noticias › ref2. Se usa con `--estilo r2` en editar_v2.py:
- Subtítulos de 2 pisos (frase chica blanca + palabra clave grande roja con brillo), van en editar_v2.ass_v2 (op "dos_pisos").
- Tarjetas oscuras redondeadas que se llenan paso a paso (arriba, sin tapar la cara): r2_estado, r2_barra, r2_ficha, r2_gauge.
- Pantallas completas: fondo oscuro con objeto "3D" (emoji grande con brillo) r2_objeto; fondo claro con logos en tarjetas
  blancas que entran uno a uno r2_logos.
- Transición: destello de luz cálida (r2_destello) en cada cambio de noticia.
"""
import math

from PIL import Image, ImageDraw, ImageFilter

import animaciones as A

W, H = A.W, A.H
ROJO = (255, 48, 58)
ROJO_OSC = (120, 14, 20)
VERDE = (52, 211, 120)
BLANCO = (255, 255, 255)
GRIS = (160, 160, 170)
TARJETA = (18, 14, 16, 238)


def _sans(t, tam, color=BLANCO, negra=True):
    return A._texto_img_base(t, tam, color, negra)


def _ajustar(img, ancho):
    return img if img.width <= ancho else A.escalar(img, ancho / img.width)


def _tarjeta(w, h, titulo=None):
    """Tarjeta oscura con esquinas redondas, borde rojo fino y brillo suave (como las del referente, en rojo)."""
    pad = 40
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((pad, pad, pad + w, pad + h), 40, outline=ROJO + (170,), width=6)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), 40, fill=TARJETA, outline=(255, 80, 90, 120), width=2)
    # degradado rojo muy suave abajo
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dg = ImageDraw.Draw(grad)
    for i in range(h):
        a = int(70 * (i / h) ** 2)
        dg.line((0, i, w, i), fill=ROJO_OSC + (a,))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=255)
    grad.putalpha(Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(grad.getchannel("A")), __import__("numpy").array(m))))
    im.alpha_composite(grad, (pad, pad))
    if titulo:
        im.alpha_composite(_sans(titulo, 30, GRIS, False), (pad + 34, pad + 22))
    return im, pad


def _check(ok, tam=56):
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = VERDE if ok else ROJO
    d.ellipse((2, 2, tam - 2, tam - 2), outline=col + (255,), width=5)
    if ok:
        d.line([(tam * 0.28, tam * 0.52), (tam * 0.44, tam * 0.68), (tam * 0.74, tam * 0.34)], fill=col + (255,), width=6, joint="curve")
    else:
        d.line((tam * 0.32, tam * 0.32, tam * 0.68, tam * 0.68), fill=col + (255,), width=6)
        d.line((tam * 0.68, tam * 0.32, tam * 0.32, tam * 0.68), fill=col + (255,), width=6)
    return im


def _pop(t, t0, d=0.28):
    return A.ease_out_back(A.clamp((t - t0) / d))


CAJA = (60, 250, 960, 600)  # arriba, sin tapar la cara


def _grafico_tarjeta(dur, dibujar, sonido="pop", caja=CAJA):
    x, y, w, h = caja

    def cuadro(t):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        e = A.ease_out(A.clamp(t / 0.3)) * A.clamp((dur - t) / 0.22)
        dibujar(im, t)
        if e < 1:
            s = 0.9 + 0.1 * e
            im2 = A.escalar(im, s)
            out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            out.alpha_composite(im2, ((w - im2.width) // 2, int((h - im2.height) / 2 + (1 - e) * 40)))
            im = A.con_alfa(out, e)
        return im

    return A.Grafico(dur, caja, cuadro, sonido)


# --------------------------------------------------------------------------- tarjetas
def g_estado(dur, titulo="Estado del servicio", items=(("Outlook", False), ("Teams", False), ("Copilot", False)), logos=()):
    """Lista que se marca paso a paso (✓ verde / ✗ rojo), como 'Cómo se arma' del referente."""
    n = len(items)

    def dib(im, t):
        card, pad = _tarjeta(880, 120 + 120 * n, titulo)
        for i, (nom, ok) in enumerate(items):
            y = pad + 90 + i * 120
            ImageDraw.Draw(card).ellipse((pad + 40, y + 8, pad + 110, y + 78), outline=(255, 255, 255, 90), width=3)
            if i < len(logos) and logos[i]:
                lg = A.logo_blanco(logos[i], 40, 50)
                card.alpha_composite(lg, (int(pad + 75 - lg.width / 2), int(y + 43 - lg.height / 2)))
            card.alpha_composite(_sans(nom, 46), (pad + 140, y + 14))
            k = _pop(t, 0.35 + i * 0.32)
            if k > 0:
                c = A.escalar(_check(ok, 64), max(0.05, k))
                card.alpha_composite(c, (int(pad + 800 - c.width / 2), int(y + 43 - c.height / 2)))
        A.pegar_centro(im, card, im.width / 2, card.height / 2 + 10)

    return _grafico_tarjeta(dur, dib, "pop")


def g_barra(dur, titulo="OpenAI · 3 meses", antes="+10.000 M", despues="-11.000 M", et_antes="Facturó", et_despues="Perdió"):
    """Barra que sube en verde y cae a rojo (pérdida)."""

    def dib(im, t):
        card, pad = _tarjeta(880, 420, titulo)
        d = ImageDraw.Draw(card)
        k1 = A.ease_out(A.clamp((t - 0.2) / 0.7))
        cambio = dur * 0.5
        k2 = A.ease_out(A.clamp((t - cambio) / 0.5))
        x0, y0, ww = pad + 50, pad + 260, 780
        d.rounded_rectangle((x0, y0, x0 + ww, y0 + 46), 23, fill=(50, 44, 48, 255))
        if k2 <= 0:
            d.rounded_rectangle((x0, y0, x0 + max(46, ww * k1), y0 + 46), 23, fill=VERDE + (255,))
            card.alpha_composite(_sans(et_antes, 36, GRIS, False), (x0, pad + 90))
            card.alpha_composite(A._brillo(_sans(antes, 96, VERDE), 10, 1.4), (x0 - 20, pad + 120))
        else:
            d.rounded_rectangle((x0, y0, x0 + max(46, ww * (1 - 0.85 * k2)), y0 + 46), 23, fill=ROJO + (255,))
            card.alpha_composite(_sans(et_despues, 36, GRIS, False), (x0, pad + 90))
            card.alpha_composite(A._brillo(_sans(despues, 96, ROJO), 10, 1.4), (x0 - 20, pad + 120))
        A.pegar_centro(im, card, im.width / 2, card.height / 2 + 10)

    return _grafico_tarjeta(dur, dib, "alerta")


def g_ficha(dur, titulo="Ficha del paciente", items=(("Nombre", True), ("Medicamentos", True), ("Examen del azúcar", False)), cifra="25 %", sub="de los casos"):
    def dib(im, t):
        card, pad = _tarjeta(880, 520, titulo)
        for i, (nom, ok) in enumerate(items):
            y = pad + 80 + i * 105
            card.alpha_composite(_sans(nom, 42, BLANCO if ok else ROJO), (pad + 50, y + 12))
            k = _pop(t, 0.3 + i * 0.35)
            if k > 0:
                c = A.escalar(_check(ok, 60), max(0.05, k))
                card.alpha_composite(c, (int(pad + 800 - c.width / 2), int(y + 38 - c.height / 2)))
        kc = _pop(t, 0.3 + len(items) * 0.35 + 0.1, 0.35)
        if kc > 0:
            num = A.escalar(A._brillo(_sans(cifra, 96, ROJO), 10, 1.4), max(0.05, kc))
            card.alpha_composite(num, (pad + 50, pad + 400))
            card.alpha_composite(_sans(sub, 36, GRIS, False), (pad + 60 + num.width, pad + 440))
        A.pegar_centro(im, card, im.width / 2, card.height / 2 + 10)

    return _grafico_tarjeta(dur, dib, "pop")


def g_gauge(dur, titulo="Empresas que ganan con IA", valor="95 %", sub="no ganó nada", segundo=None):
    """Velocímetro (rojo-amarillo-verde) cuya aguja cae al rojo, como el de 'Motivación' del referente."""

    def dib(im, t):
        card, pad = _tarjeta(880, 470, titulo)
        d = ImageDraw.Draw(card)
        cx, cy, r = pad + 300, pad + 330, 210
        for a0, a1, col in ((180, 240, ROJO), (240, 300, (255, 170, 40)), (300, 360, VERDE)):
            d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col + (255,), width=36)
        k = A.ease_in_out(A.clamp((t - 0.3) / 0.9))
        ang = math.radians(330 - 145 * k)  # de verde a rojo
        d.line((cx, cy, cx + (r - 50) * math.cos(ang), cy + (r - 50) * math.sin(ang)), fill=BLANCO + (255,), width=12)
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=BLANCO + (255,))
        kv = _pop(t, 1.1, 0.35)
        if kv > 0:
            card.alpha_composite(A.escalar(A._brillo(_sans(valor, 96, ROJO), 10, 1.4), max(0.05, kv)), (pad + 560, pad + 160))
            card.alpha_composite(_sans(sub, 34, GRIS, False), (pad + 566, pad + 290))
        if segundo and t > dur * 0.62:
            q = A.clamp((t - dur * 0.62) / 0.3)
            card.alpha_composite(A.con_alfa(_sans(segundo, 40, BLANCO), q), (pad + 566, pad + 350))
        A.pegar_centro(im, card, im.width / 2, card.height / 2 + 10)

    return _grafico_tarjeta(dur, dib, "alerta")


# --------------------------------------------------------------------------- pantallas completas
_cache = {}


def _fondo_oscuro():
    if "o" not in _cache:
        import numpy as np
        y, x = np.mgrid[0:H, 0:W]
        d = np.sqrt(((x - W / 2) / (W * 0.7)) ** 2 + ((y - H * 0.48) / (H * 0.5)) ** 2)
        g = np.clip(1 - d, 0, 1) ** 1.4
        arr = np.zeros((H, W, 3), np.float32)
        arr[..., 0] = 14 + 30 * g
        arr[..., 1] = 18 + 22 * g
        arr[..., 2] = 22 + 24 * g
        _cache["o"] = Image.fromarray(arr.astype("uint8"), "RGB").convert("RGBA")
    return _cache["o"].copy()


def _fondo_claro():
    if "c" not in _cache:
        import numpy as np
        y = np.linspace(0, 1, H)[:, None, None]
        arr = (np.array((246, 242, 236))[None, None, :] * (1 - y) + np.array((232, 226, 218))[None, None, :] * y).repeat(W, 1)
        _cache["c"] = Image.fromarray(arr.astype("uint8"), "RGB").convert("RGBA")
    return _cache["c"].copy()


def _pantalla(dur, fondo, dib, sonido="whoosh"):
    def cuadro(t):
        im = fondo()
        dib(im, t)
        return A.con_alfa(im, A.clamp(t / 0.18) * A.clamp((dur - t) / 0.18))

    return A.Grafico(dur, (0, 0, W, H), cuadro, sonido)


def g_objeto(dur, emojis=("🌍",), puntos=0, texto_arriba="", texto_abajo=""):
    """Fondo oscuro con un objeto grande tipo 3D (emoji con sombra y brillo) que flota; opcional: puntos rojos que se apagan."""
    grandes = [A.emoji(e, 520 if i == 0 else 300) for i, e in enumerate(emojis)]

    def dib(im, t):
        flot = 14 * math.sin(t * 2.2)
        k = A.ease_out_back(A.clamp(t / 0.45))
        base = grandes[0]
        sombra = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).ellipse((W / 2 - 230, 60, W / 2 + 230, 140), fill=(0, 0, 0, 150))
        im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(24)), (0, 1180))
        A.pegar_centro(im, A.escalar(base, max(0.05, 0.85 + 0.15 * k)), W / 2, 900 + flot)
        for i, g in enumerate(grandes[1:]):
            kk = A.ease_out_back(A.clamp((t - 0.25 - i * 0.15) / 0.4))
            if kk > 0:
                A.pegar_centro(im, A.escalar(g, max(0.05, kk)), W / 2 + 230 - i * 40, 1080 + flot * 0.6 + i * 30)
        if puntos:
            d = ImageDraw.Draw(im)
            import random
            rnd = random.Random(5)
            for j in range(puntos):
                a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(40, 200)
                x, y = W / 2 + rr * math.cos(a), 900 + flot + rr * math.sin(a) * 0.9
                on = t < 0.4 + j * (dur * 0.6 / puntos)
                col = ROJO if on else (60, 60, 60)
                d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=col + (255,))
        if texto_arriba:
            im.alpha_composite(_sans(texto_arriba, 54, BLANCO, False), (90, 430))
        if texto_abajo and t > 0.5:
            q = A.clamp((t - 0.5) / 0.3)
            im.alpha_composite(A.con_alfa(A._brillo(_sans(texto_abajo, 92, ROJO), 10, 1.4), q), (80, 1330))

    return _pantalla(dur, _fondo_oscuro, dib)


def g_logos(dur, arriba="", grande="", items=(), martillo=True, assets="assets-v2"):
    """Fondo claro con tarjetas blancas (logo o nombre) que entran una a una; texto arriba con palabra grande en rojo."""
    def tarjeta(it):
        c = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        s = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        ImageDraw.Draw(s).rounded_rectangle((20, 30, 280, 290), 40, fill=(0, 0, 0, 60))
        c.alpha_composite(s.filter(ImageFilter.GaussianBlur(12)))
        ImageDraw.Draw(c).rounded_rectangle((20, 20, 280, 280), 40, fill=(255, 255, 255, 255))
        ruta = f"{assets}/logo_{it}.png"
        import os
        if os.path.exists(ruta):
            lg = A.logo(ruta, 130, 200)
            A.pegar_centro(c, lg, 150, 150)
        else:
            A.pegar_centro(c, _ajustar(_sans(it.upper(), 44, (30, 30, 36)), 220), 150, 150)
        return c

    cards = [tarjeta(i) for i in items]
    pos = [(W / 2 - 170, 760), (W / 2 + 170, 760), (W / 2 - 170, 1090), (W / 2 + 170, 1090), (W / 2, 1400)][: len(cards)]
    mart = A.emoji("⚖️", 200) if martillo else None

    def dib(im, t):
        if arriba:
            A.pegar_centro(im, _sans(arriba, 50, (40, 40, 46), False), W / 2, 340)
        if grande:
            A.pegar_centro(im, _ajustar(_sans(grande, 96, ROJO), 960), W / 2, 440)
        for i, (c, (x, y)) in enumerate(zip(cards, pos)):
            k = _pop(t, 0.15 + i * 0.22, 0.3)
            if k > 0:
                A.pegar_centro(im, A.escalar(c, max(0.05, k)), x, y)
        if mart is not None and t > 0.15 + len(cards) * 0.22:
            k = _pop(t, 0.15 + len(cards) * 0.22, 0.3)
            A.pegar_centro(im, A.escalar(mart, max(0.05, k)).rotate(-15 * (1 - k), resample=Image.BICUBIC, expand=True), W / 2 + 330, 1500)

    return _pantalla(dur, _fondo_claro, dib, "pop")


def g_destello(dur=0.5):
    """Destello de luz cálida (naranja) que entra por un lado y se va: transición entre partes."""
    def cuadro(t):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        k = math.sin(math.pi * A.clamp(t / dur))
        d = ImageDraw.Draw(im)
        cx = W * (0.15 + 0.7 * A.clamp(t / dur))
        d.ellipse((cx - 700, H * 0.3, cx + 700, H * 0.8), fill=(255, 140, 40, int(200 * k)))
        im = im.filter(ImageFilter.GaussianBlur(160))
        capa = Image.new("RGBA", (W, H), (255, 190, 120, int(70 * k)))
        im.alpha_composite(capa)
        return im

    return A.Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def aplicar():
    A.aplicar_estilo("ia")
    A.g_transicion = g_destello


def construir(g, dur, assets):
    t = g["tipo"]
    if t == "r2_estado":
        return g_estado(dur, g.get("titulo", "Estado del servicio"), [tuple(x) for x in g.get("items", [])] or (("Outlook", False), ("Teams", False), ("Copilot", False)),
                        [f"{assets}/logo_{x}.png" if x else None for x in g.get("logos", [])])
    if t == "r2_barra":
        return g_barra(dur, g.get("titulo", "OpenAI · 3 meses"), g.get("antes", "+10.000 M"), g.get("despues", "-11.000 M"),
                       g.get("et_antes", "Facturó"), g.get("et_despues", "Perdió"))
    if t == "r2_ficha":
        return g_ficha(dur, g.get("titulo", "Ficha del paciente"), [tuple(x) for x in g.get("items", [])] or (("Nombre", True), ("Medicamentos", True), ("Examen del azúcar", False)),
                       g.get("cifra", "25 %"), g.get("sub", "de los casos"))
    if t == "r2_gauge":
        return g_gauge(dur, g.get("titulo", "Empresas que ganan con IA"), g.get("valor", "95 %"), g.get("sub", "no ganó nada"), g.get("segundo"))
    if t == "r2_objeto":
        return g_objeto(dur, tuple(g.get("emojis", ["🌍"])), g.get("puntos", 0), g.get("arriba", ""), g.get("abajo", ""))
    if t == "r2_logos":
        return g_logos(dur, g.get("arriba", ""), g.get("grande", ""), tuple(g.get("items", [])), g.get("martillo", True), assets)
    return None
