"""Estilo CYBERPUNK (v5, 9 nov · pedido de Santi): neón magenta/cian/amarillo, glitch, HUD y escenas nuevas.

Se usa con `--estilo cyber` en editar_v2.py: aplica el estilo 'ia' de animaciones.py y encima cambia la transición
por un glitch con separación RGB, y agrega escenas: espia, valor, marcha, ley, veneno, puerta, hud.
Todo dibujado aquí (sin imágenes externas salvo los logos de assets-v2).
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import animaciones as A

W, H = A.W, A.H
CIAN, MAGENTA = (0, 240, 255), (255, 40, 200)
AMARILLO = (255, 236, 30)
ROJO_N = (255, 40, 70)


# --------------------------------------------------------------------------- utilidades
def _glitch(im, t, fuerza=1.0, semilla=0):
    """Separación RGB + franjas desplazadas. fuerza 0..1."""
    if fuerza <= 0.02:
        return im
    rnd = random.Random(int(t * 30) * 7 + semilla)
    arr = np.array(im)
    d = int(6 + 22 * fuerza)
    out = arr.copy()
    out[..., 0] = np.roll(arr[..., 0], d, axis=1)
    out[..., 2] = np.roll(arr[..., 2], -d, axis=1)
    out[..., 3] = np.maximum(arr[..., 3], np.maximum(np.roll(arr[..., 3], d, 1), np.roll(arr[..., 3], -d, 1)))
    for _ in range(int(3 + 8 * fuerza)):
        y0 = rnd.randint(0, im.height - 20); hh = rnd.randint(6, int(20 + 60 * fuerza))
        out[y0:y0 + hh] = np.roll(out[y0:y0 + hh], rnd.randint(-int(80 * fuerza) - 5, int(80 * fuerza) + 5), axis=1)
    return Image.fromarray(out, "RGBA")


def _parpadeo(t, ini=0.0, dur=0.35):
    """Fuerza de glitch al entrar (fuerte al inicio, se apaga)."""
    k = (t - ini) / dur
    return 0.0 if k < 0 or k > 1 else (1 - k) ** 1.5


def _neon_txt(texto, tam, color=AMARILLO, negra=True):
    base = A._texto_img_base(texto, tam, color, negra)
    return A._brillo(base, max(6, tam // 8), 1.5)


def _ajustar(img, ancho):
    return img if img.width <= ancho else A.escalar(img, ancho / img.width)


def _hud(im, t, color=CIAN):
    """Esquinas de visor + línea de escaneo."""
    d = ImageDraw.Draw(im)
    L, g = 90, 6
    for (x, y, sx, sy) in ((60, 420, 1, 1), (W - 60, 420, -1, 1), (60, 1330, 1, -1), (W - 60, 1330, -1, -1)):
        d.line((x, y, x + sx * L, y), fill=color + (220,), width=g)
        d.line((x, y, x, y + sy * L), fill=color + (220,), width=g)
    yy = 420 + (910 * ((t * 0.7) % 1))
    d.line((70, yy, W - 70, yy), fill=color + (70,), width=3)


def _escena(dur, dibujar, sonido="golpe", glitch_entrada=True):
    fondo = A._fondo_oscuro()

    def cuadro(t):
        a, _ = A._entrada_salida(t, dur)
        im = fondo.copy()
        _hud(im, t)
        dibujar(im, t)
        if glitch_entrada:
            im = _glitch(im, t, max(_parpadeo(t), 0.5 * _parpadeo(t, dur - 0.25, 0.25) if t > dur - 0.25 else 0))
        return A.con_alfa(im, a)

    return A.Grafico(dur, (0, 0, W, H), cuadro, sonido)


def _logo(ruta, alto, ancho):
    return A.logo_blanco(ruta, alto, ancho) if ruta else None


def _titulo(im, texto, y=470, color=AMARILLO):
    if texto:
        A.pegar_centro(im, _ajustar(_neon_txt(texto, 66, color), 900), W / 2, y)


# --------------------------------------------------------------------------- escenas
def g_espia(dur, ruta_logo=None, titulo="¿UNA ESPÍA DE CHINA?", objetivo="OBJETIVO: JEFE DE NVIDIA"):
    """Silueta de espía en sombra; una mira roja se fija en el logo de Nvidia; texto de HUD que se escribe."""
    lg = _logo(ruta_logo, 130, 420)
    sil = Image.new("RGBA", (360, 620), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sil)
    col = (8, 6, 18, 255)
    ds.ellipse((40, 40, 320, 110), fill=col)                    # ala del sombrero
    ds.rounded_rectangle((100, 0, 260, 80), 30, fill=col)       # copa
    ds.ellipse((120, 70, 240, 200), fill=col)                   # cabeza
    ds.polygon([(60, 620), (90, 260), (180, 200), (270, 260), (300, 620)], fill=col)  # abrigo
    ds.polygon([(150, 215), (210, 215), (180, 300)], fill=(30, 10, 40, 255))
    borde = sil.filter(ImageFilter.MaxFilter(9))
    neon = Image.new("RGBA", sil.size, MAGENTA + (0,)); neon.putalpha(borde.getchannel("A"))
    neon = neon.filter(ImageFilter.GaussianBlur(6))
    sil2 = Image.new("RGBA", sil.size, (0, 0, 0, 0)); sil2.alpha_composite(neon); sil2.alpha_composite(sil)

    def dib(im, t):
        _titulo(im, titulo)
        kx = A.ease_out(A.clamp(t / 0.5))
        im.alpha_composite(sil2, (int(-360 + 400 * kx), 700))
        if lg:
            A.pegar_centro(im, lg, 680, 860)
        k = A.ease_out(A.clamp((t - 0.35) / 0.6))
        cx, cy = 680, 860
        r = 260 - 120 * k
        d = ImageDraw.Draw(im)
        c = ROJO_N + (int(255 * A.clamp(t / 0.3)),)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=6)
        d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), outline=c, width=3)
        for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            d.line((cx + sx * (r + 40), cy + sy * (r + 40), cx + sx * (r - 30), cy + sy * (r - 30)), fill=c, width=6)
        if k >= 1 and int(t * 6) % 2 == 0:
            A.pegar_centro(im, _neon_txt("FIJADO", 40, ROJO_N), cx, cy + r + 70)
        n = int(len(objetivo) * A.clamp((t - 0.4) / 0.9))
        A.pegar_centro(im, _ajustar(A._texto_img_base(objetivo[:n] + ("_" if int(t * 4) % 2 else " "), 44, CIAN), 900),
                       W / 2, 1230)

    return _escena(dur, dib, "alerta")


def g_valor(dur, ruta_logo=None, cifra="1,25 BILLONES", sub="de dólares"):
    """Logo de OpenAI y los doce ceros de 1.250.000.000.000 apareciendo uno a uno; al final la cifra en grande."""
    lg = _logo(ruta_logo, 140, 420)
    num = "1.250.000.000.000"

    def dib(im, t):
        if lg:
            A.pegar_centro(im, lg, W / 2, 620)
        A.pegar_centro(im, _neon_txt("VALE", 54, CIAN), W / 2, 760)
        k = A.clamp((t - 0.1) / (dur * 0.3))
        n = 1 + int((len(num) - 1) * k)
        A.pegar_centro(im, _ajustar(A._texto_img_base(num[:n], 96, (255, 255, 255)), 960), W / 2, 900)
        k2 = A.ease_out_back(A.clamp((t - dur * 0.42) / 0.3))
        if k2 > 0:
            A.pegar_centro(im, A.escalar(_ajustar(_neon_txt(cifra, 120, AMARILLO), 980), k2), W / 2, 1080)
            A.pegar_centro(im, A._texto_img_base(sub, 46, (220, 220, 240), False), W / 2, 1210)

    return _escena(dur, dib, "ding")


def g_marcha(dur, titulo="MARCHAS EN CANADÁ", firmas=24000, monto="10.000 MILLONES"):
    """Pancartas que suben y bajan + contador de firmas + monto del centro de datos."""
    carteles = ["NO AL CENTRO", "DE DATOS", "¡FRENEN LA IA!", "⚡ ENERGÍA"]
    imgs = []
    for i, tx in enumerate(carteles):
        p = Image.new("RGBA", (300, 380), (0, 0, 0, 0))  # cartel
        d = ImageDraw.Draw(p)
        d.rectangle((140, 170, 160, 380), fill=(120, 90, 60, 255))
        d.rectangle((10, 10, 290, 190), fill=(240, 240, 235, 255), outline=(MAGENTA if i % 2 else CIAN) + (255,), width=8)
        t_ = A.texto_emoji("⚡", "ENERGÍA", 38, (20, 20, 30)) if "⚡" in tx else A._texto_img_base(tx, 40, (20, 20, 30))
        A.pegar_centro(p, _ajustar(t_, 260), 150, 100)
        imgs.append(p.resize((256, 324), Image.LANCZOS))

    def dib(im, t):
        _titulo(im, titulo)
        for i, p in enumerate(imgs):
            ky = A.ease_out(A.clamp((t - 0.1 * i) / 0.4))
            y = 1240 - 520 * ky + 18 * math.sin(t * 6 + i * 1.7)
            im.alpha_composite(p.rotate(6 * math.sin(t * 4 + i), resample=Image.BICUBIC, expand=False), (int(18 + i * 262), int(y)))
        k = A.ease_out(A.clamp((t - 0.6) / (dur * 0.5)))
        A.pegar_centro(im, _neon_txt(f"{int(firmas * k):,}".replace(",", ".") + " FIRMAS", 84, AMARILLO), W / 2, 1150)
        k2 = A.clamp((t - dur * 0.35) / 0.3)
        if k2 > 0:
            tag = A._tarjeta_ia(520, 96, relleno=(224, 32, 32, 255), radio=20)
            A.pegar_centro(tag, A._texto_img_base(monto, 50, (255, 255, 255)), 260, 48)
            A.pegar_centro(im, A.con_alfa(tag, k2), W / 2, 590)

    return _escena(dur, dib, "golpe")


def _bandera_filipinas(w=300):
    h = w // 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, h // 2), fill=(0, 56, 168, 255))
    d.rectangle((0, h // 2, w, h), fill=(206, 17, 38, 255))
    d.polygon([(0, 0), (int(h * 0.866), h // 2), (0, h)], fill=(255, 255, 255, 255))
    cx, cy, r = h * 0.3, h / 2, h * 0.1
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(252, 209, 22, 255))
    for k in range(8):
        a = k * math.pi / 4
        d.line((cx + math.cos(a) * r, cy + math.sin(a) * r, cx + math.cos(a) * r * 2, cy + math.sin(a) * r * 2), fill=(252, 209, 22, 255), width=4)
    return im


def g_ley(dur, titulo="LEY EN FILIPINAS", puntos=("Avisar 6 meses antes", "Capacitar primero", "Indemnización x2")):
    """Bandera + documento de ley; los 3 puntos se marcan uno a uno."""
    band = _bandera_filipinas(260)
    items = [_ajustar(A._texto_img_base(p, 54, (255, 255, 255)), 640) for p in puntos]

    def dib(im, t):
        _titulo(im, titulo)
        A.pegar_centro(im, band, W / 2, 640)
        doc = A._tarjeta_ia(900, 470)
        for i, it in enumerate(items):
            k = A.clamp((t - (0.15, dur * 0.3, dur * 0.6)[i]) / 0.25)
            y = 90 + i * 140
            d = ImageDraw.Draw(doc)
            d.rounded_rectangle((50, y - 40, 130, y + 40), 14, outline=CIAN + (255,), width=5)
            if k > 0:
                d.line((65, y, 85 + 0 * k, y + 25), fill=AMARILLO + (255,), width=10)
                d.line((85, y + 25, 85 + 40 * k, y + 25 - 60 * k), fill=AMARILLO + (255,), width=10)
                doc.alpha_composite(A.con_alfa(it, k), (165, int(y - it.height / 2)))
        A.pegar_centro(im, doc, W / 2, 1030)

    return _escena(dur, dib, "pop")


def g_veneno(dur, ruta_logo=None, titulo="DEMANDAN A OPENAI", casos=10, sub="casos en menos de 2 años"):
    """Logo de OpenAI con alerta roja que late; martillo de juez; contador de casos."""
    lg = _logo(ruta_logo, 150, 420)
    martillo = A.emoji("⚖️", 150)
    alerta = A.emoji("⚠️", 120)

    def dib(im, t):
        _titulo(im, titulo, color=ROJO_N)
        late = 0.5 + 0.5 * math.sin(t * 9)
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(capa).ellipse((290, 560, 790, 1000), fill=ROJO_N + (int(60 + 80 * late),))
        im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(60)))
        if lg:
            A.pegar_centro(im, lg, W / 2, 780)
        A.pegar_centro(im, alerta, 250, 650)
        A.pegar_centro(im, martillo.rotate(25 * math.sin(min(t, 1.2) * 10) * max(0, 1 - t), expand=True), 830, 700)
        k = A.clamp((t - 0.5) / (dur * 0.4))
        n = max(1, int(round(casos * A.ease_out(k)))) if k > 0 else 0
        if n:
            A.pegar_centro(im, _neon_txt(f"{n} CASOS", 110, ROJO_N), W / 2, 1080)
            A.pegar_centro(im, A._texto_img_base(sub, 44, (230, 230, 240), False), W / 2, 1200)

    return _escena(dur, dib, "alerta")


def g_puerta(dur, ruta_logo=None, titulo="EL CONGRESO LO CITÓ", sello="A PUERTA CERRADA"):
    """Dos puertas de metal se cierran sobre el logo de Nvidia y cae el sello rojo."""
    lg = _logo(ruta_logo, 140, 420)
    st = _neon_txt(sello, 76, (255, 255, 255))
    sl = A._tarjeta_ia(st.width + 70, st.height + 50, relleno=(224, 32, 32, 255), radio=18)
    A.pegar_centro(sl, st, sl.width / 2, sl.height / 2)
    sl = sl.rotate(-6, resample=Image.BICUBIC, expand=True)

    def dib(im, t):
        _titulo(im, titulo)
        if lg:
            A.pegar_centro(im, lg, W / 2, 850)
        k = A.ease_in_out(A.clamp((t - 0.3) / 0.6))
        d = ImageDraw.Draw(im)
        hw = 360 * k
        for x0, x1 in ((180, 180 + hw), (900 - hw, 900)):
            if x1 - x0 > 2:
                d.rectangle((x0, 580, x1, 1130), fill=(26, 30, 52, 250), outline=CIAN + (200,), width=5)
                for yy in range(620, 1110, 70):
                    d.line((x0 + 15, yy, x1 - 15, yy), fill=(60, 70, 110, 255), width=3)
        ks = A.clamp((t - 1.0) / 0.18)
        if ks > 0:
            A.pegar_centro(im, A.con_alfa(A.escalar(sl, 2.0 - A.ease_out(ks)), ks), W / 2, 1220)
        q = A.clamp((t - dur * 0.7) / 0.3)
        if q > 0:
            A.pegar_centro(im, A.con_alfa(_neon_txt("¿QUÉ OCULTAN?", 60, MAGENTA), q), W / 2, 1330)

    return _escena(dur, dib, "golpe")


def g_hud(dur, texto="ALERTA · IA", color=CIAN):
    """Visor tipo HUD sobre la cámara (no tapa la cara): esquinas, escaneo y una etiqueta que parpadea arriba."""
    tx = _neon_txt(texto, 44, color)

    def cuadro(t):
        a, _ = A._entrada_salida(t, dur, 0.12)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        L = 120
        for (x, y, sx, sy) in ((50, 200, 1, 1), (W - 50, 200, -1, 1), (50, 1700, 1, -1), (W - 50, 1700, -1, -1)):
            d.line((x, y, x + sx * L, y), fill=color + (230,), width=7)
            d.line((x, y, x, y + sy * L), fill=color + (230,), width=7)
        if int(t * 4) % 2 == 0:
            d.ellipse((70, 1620, 100, 1650), fill=ROJO_N + (255,))
            im.alpha_composite(A._texto_img_base("REC", 34, (255, 255, 255)), (112, 1618))
        A.pegar_centro(im, tx, W / 2, 160)
        im = _glitch(im, t, _parpadeo(t, 0, 0.3), 3)
        return A.con_alfa(im, a)

    return A.Grafico(dur, (0, 0, W, H), cuadro, None)


def g_transicion_cyber(dur=0.32):
    """Glitch entre noticias: franjas magenta/cian/amarillo, separación RGB y destello."""
    rnd = random.Random(9)

    def cuadro(t):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = A.clamp(t / dur)
        pico = math.sin(math.pi * k)
        r2 = random.Random(int(t * 30))
        for _ in range(int(6 + 14 * pico)):
            y0 = r2.randint(0, H); hh = r2.randint(8, 90)
            x0 = r2.randint(-200, W); ww = r2.randint(200, 900)
            d.rectangle((x0, y0, x0 + ww, y0 + hh), fill=r2.choice((CIAN, MAGENTA, AMARILLO)) + (int(200 * pico),))
        if 0.35 < k < 0.6:
            d.rectangle((0, 0, W, H), fill=(255, 255, 255, int(120 * pico)))
        return im

    return A.Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def aplicar():
    A.aplicar_estilo("ia")
    A.CYBER = True
    A.g_transicion = g_transicion_cyber


def construir(g, dur, assets):
    t = g["tipo"]
    lg = lambda: f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None
    if t == "espia":
        return g_espia(dur, lg(), g.get("titulo", "¿UNA ESPÍA DE CHINA?"), g.get("objetivo", "OBJETIVO: JEFE DE NVIDIA"))
    if t == "valor":
        return g_valor(dur, lg(), g.get("cifra", "1,25 BILLONES"), g.get("sub", "de dólares"))
    if t == "marcha":
        return g_marcha(dur, g.get("titulo", "MARCHAS EN CANADÁ"), g.get("firmas", 24000), g.get("monto", "10.000 MILLONES"))
    if t == "ley":
        return g_ley(dur, g.get("titulo", "LEY EN FILIPINAS"), tuple(g.get("puntos", ("Avisar 6 meses antes", "Capacitar primero", "Indemnización x2"))))
    if t == "veneno":
        return g_veneno(dur, lg(), g.get("titulo", "DEMANDAN A OPENAI"), g.get("casos", 10), g.get("sub", "casos en menos de 2 años"))
    if t == "puerta":
        return g_puerta(dur, lg(), g.get("titulo", "EL CONGRESO LO CITÓ"), g.get("sello", "A PUERTA CERRADA"))
    if t == "hud":
        return g_hud(dur, g.get("texto", "ALERTA · IA"))
    return None
