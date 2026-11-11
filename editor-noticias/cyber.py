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


# --------------------------------------------------------------------------- escenas v6 (10 nov)
def g_infiel(dur, ruta_logo=None, titulo="UNA INFIDELIDAD CARÍSIMA", cifra="-200.000 MILLONES"):
    """Corazón neón que se parte en dos sobre el logo de Nvidia; la cifra cae en rojo."""
    lg = _logo(ruta_logo, 120, 380)
    cor = A.emoji("❤️", 300)
    L = cor.crop((0, 0, cor.width // 2, cor.height)); R = cor.crop((cor.width // 2, 0, cor.width, cor.height))

    def dib(im, t):
        _titulo(im, titulo, color=MAGENTA)
        k = A.ease_out(A.clamp((t - 0.45) / 0.35))
        cy = 730 + 6 * math.sin(t * 7)
        im.alpha_composite(L.rotate(14 * k, expand=True), (int(W / 2 - L.width - 60 * k), int(cy - L.height / 2 + 40 * k)))
        im.alpha_composite(R.rotate(-14 * k, expand=True), (int(W / 2 + 60 * k), int(cy - R.height / 2 + 40 * k)))
        if lg:
            A.pegar_centro(im, lg, W / 2, 1010)
        k2 = A.ease_out_back(A.clamp((t - dur * 0.45) / 0.3))
        if k2 > 0:
            A.pegar_centro(im, A.escalar(_ajustar(_neon_txt(cifra, 100, ROJO_N), 980), k2), W / 2, 1180)
            A.pegar_centro(im, A._texto_img_base("de dólares en valor", 42, (230, 230, 240), False), W / 2, 1290)

    return _escena(dur, dib, "golpe")


def g_generador(dur, ruta_logo=None, titulo="GENERADORES DE GAS", cifra="3.400 MILLONES", sello="SIN CONFIRMAR"):
    """Fila de generadores con rayos; contador de millones; sello amarillo."""
    lg = _logo(ruta_logo, 100, 320)
    rayo = A.emoji("⚡", 90)

    def dib(im, t):
        _titulo(im, titulo)
        if lg:
            A.pegar_centro(im, lg, W / 2, 600)
        d = ImageDraw.Draw(im)
        for i in range(3):
            x0 = 150 + i * 270
            d.rounded_rectangle((x0, 720, x0 + 230, 920), 18, fill=(30, 34, 60, 255), outline=CIAN + (220,), width=5)
            for k in range(4):
                d.line((x0 + 30, 760 + k * 35, x0 + 200, 760 + k * 35), fill=(70, 80, 120, 255), width=6)
            if int(t * 8 + i) % 3 != 0:
                A.pegar_centro(im, rayo, x0 + 115, 680 + 8 * math.sin(t * 12 + i))
        k = A.ease_out(A.clamp((t - 0.3) / (dur * 0.45)))
        A.pegar_centro(im, _ajustar(_neon_txt(f"{3400 * k:,.0f}".replace(",", ".") + " MILLONES", 96, AMARILLO), 980), W / 2, 1060)
        A.pegar_centro(im, A._texto_img_base("de dólares en energía", 42, (230, 230, 240), False), W / 2, 1160)
        ks = A.clamp((t - dur * 0.6) / 0.18)
        if ks > 0:
            st = A._texto_img_base(sello, 54, (20, 20, 20))
            sl = Image.new("RGBA", (st.width + 60, st.height + 40), AMARILLO + (255,))
            A.pegar_centro(sl, st, sl.width / 2, sl.height / 2)
            sl = sl.rotate(-8, resample=Image.BICUBIC, expand=True)
            A.pegar_centro(im, A.con_alfa(A.escalar(sl, 2 - A.ease_out(ks)), ks), W / 2, 1270)

    return _escena(dur, dib, "golpe")


def g_dibujo(dur, titulo="IA ENTRENADA CON DISNEY", izq="DISNEY", der="ADOBE"):
    """Un pincel neón dibuja un castillo línea a línea; arriba las dos marcas unidas con un +."""
    pincel = A.emoji("🖌️", 110)
    trazo = [(300, 1150), (300, 850), (360, 850), (360, 760), (420, 700), (480, 760), (480, 850), (540, 650), (600, 850),
             (600, 760), (660, 700), (720, 760), (720, 850), (780, 850), (780, 1150), (300, 1150)]

    def dib(im, t):
        _titulo(im, titulo)
        A.pegar_centro(im, _neon_txt(f"{izq}  +  {der}", 64, CIAN), W / 2, 570)
        k = A.clamp((t - 0.2) / (dur * 0.7))
        n = (len(trazo) - 1) * k
        d = ImageDraw.Draw(im)
        pts = trazo[: int(n) + 1]
        if int(n) < len(trazo) - 1:
            a, b = trazo[int(n)], trazo[int(n) + 1]
            f = n - int(n)
            pts = pts + [(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)]
        if len(pts) > 1:
            capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(capa).line(pts, fill=MAGENTA + (255,), width=16, joint="curve")
            im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(10)))
            d.line(pts, fill=(255, 255, 255, 255), width=7, joint="curve")
            A.pegar_centro(im, pincel, pts[-1][0] + 40, pts[-1][1] - 40)

    return _escena(dur, dib, "pop")


def g_robo(dur, ruta_logo=None, titulo="HACKERS CON IA", datos=(("300+", "CERTIFICADOS DE APPLE"), ("190.000", "CREDENCIALES"), ("≈ $1.500", "LO QUE LES COSTÓ"))):
    """Candado que se rompe sobre el logo y tres cifras que aparecen una a una."""
    lg = _logo(ruta_logo, 110, 300)
    candado, roto = A.emoji("🔒", 150), A.emoji("🔓", 150)

    def dib(im, t):
        _titulo(im, titulo, color=ROJO_N)
        if lg:
            A.pegar_centro(im, lg, W / 2 - 110, 650)
        A.pegar_centro(im, roto if t > 0.6 else candado, W / 2 + 110 + (8 * math.sin(t * 40) if 0.4 < t < 0.6 else 0), 650)
        for i, (num, et) in enumerate(datos):
            k = A.ease_out_back(A.clamp((t - 0.6 - i * dur * 0.2) / 0.3))
            if k > 0:
                y = 850 + i * 160
                A.pegar_centro(im, A.escalar(_neon_txt(num, 78, ROJO_N if i < 2 else AMARILLO), k), W / 2, y)
                A.pegar_centro(im, A.con_alfa(A._texto_img_base(et, 36, (230, 230, 240), False), min(1, k)), W / 2, y + 62)

    return _escena(dur, dib, "alerta")


_construir_v5 = construir


def construir(g, dur, assets):
    t = g["tipo"]
    lg = f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None
    if t == "infiel":
        return g_infiel(dur, lg, g.get("titulo", "UNA INFIDELIDAD CARÍSIMA"), g.get("cifra", "-200.000 MILLONES"))
    if t == "generador":
        return g_generador(dur, lg, g.get("titulo", "GENERADORES DE GAS"), g.get("cifra", "3.400 MILLONES"), g.get("sello", "SIN CONFIRMAR"))
    if t == "dibujo":
        return g_dibujo(dur, g.get("titulo", "IA ENTRENADA CON DISNEY"))
    if t == "robo":
        return g_robo(dur, lg, g.get("titulo", "HACKERS CON IA"))
    return _construir_v5(g, dur, assets)


# --------------------------------------------------------------------------- escenas v7 (11 nov)
def g_agujero(dur, titulo="FABLE 5.2", sub="el nuevo modelo de Claude", ruta_logo=None):
    """Agujero negro con disco de acreción girando y el nombre del modelo enorme encima."""
    lg = _logo(ruta_logo, 90, 260)

    def dib(im, t):
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        cx, cy = W / 2, 900
        for k in range(26):
            a = t * 2.2 + k * 0.5
            r = 170 + k * 9
            col = (AMARILLO if k % 3 == 0 else MAGENTA if k % 3 == 1 else CIAN) + (150,)
            d.arc((cx - r * 1.6, cy - r * 0.55, cx + r * 1.6, cy + r * 0.55), math.degrees(a) % 360, (math.degrees(a) + 90) % 360, fill=col, width=5)
        im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(3)))
        ImageDraw.Draw(im).ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=(0, 0, 0, 255), outline=AMARILLO + (255,), width=4)
        if lg:
            A.pegar_centro(im, lg, cx, cy)
        k = A.ease_out_back(A.clamp((t - 0.1) / 0.35))
        if k > 0:
            A.pegar_centro(im, A.escalar(_ajustar(_neon_txt(titulo, 150, AMARILLO), 980), k), W / 2, 560)
        q = A.clamp((t - 0.5) / 0.3)
        if q > 0:
            A.pegar_centro(im, A.con_alfa(A._texto_img_base(sub, 46, (240, 240, 250), False), q), W / 2, 1200)

    return _escena(dur, dib, "golpe")


def _bandera_australia(w=320):
    h = w // 2
    im = Image.new("RGBA", (w, h), (0, 0, 139, 255))
    d = ImageDraw.Draw(im)
    q = (0, 0, w // 2, h // 2)
    d.line((0, 0, q[2], q[3]), fill=(255, 255, 255, 255), width=10); d.line((0, q[3], q[2], 0), fill=(255, 255, 255, 255), width=10)
    d.line((0, 0, q[2], q[3]), fill=(200, 16, 46, 255), width=4); d.line((0, q[3], q[2], 0), fill=(200, 16, 46, 255), width=4)
    d.rectangle((q[2] / 2 - 9, 0, q[2] / 2 + 9, q[3]), fill=(255, 255, 255, 255)); d.rectangle((0, q[3] / 2 - 9, q[2], q[3] / 2 + 9), fill=(255, 255, 255, 255))
    d.rectangle((q[2] / 2 - 5, 0, q[2] / 2 + 5, q[3]), fill=(200, 16, 46, 255)); d.rectangle((0, q[3] / 2 - 5, q[2], q[3] / 2 + 5), fill=(200, 16, 46, 255))

    def estrella(x, y, r):
        pts = [(x + (r if i % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + i * math.pi / 7), y + (r if i % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + i * math.pi / 7)) for i in range(14)]
        d.polygon(pts, fill=(255, 255, 255, 255))
    estrella(w * 0.25, h * 0.75, h * 0.14)
    for x, y in ((0.75, 0.2), (0.62, 0.45), (0.86, 0.4), (0.75, 0.8)):
        estrella(w * x, h * y, h * 0.07)
    return im


def g_australia(dur, ruta_logo=None, titulo="ENTRÓ SIN PERMISO", sub="portal del gobierno de Australia"):
    """Bandera de Australia, portal bloqueado que se 'rompe' y sello rojo SIN PERMISO."""
    band = _bandera_australia(360)
    lg = _logo(ruta_logo, 90, 260)

    def dib(im, t):
        A.pegar_centro(im, band, W / 2, 600)
        p = A._tarjeta_ia(760, 300)
        A.pegar_centro(p, A._texto_img_base("ACCESO RESTRINGIDO", 44, (255, 255, 255)), 380, 80)
        bar = int(620 * A.clamp((t - 0.2) / (dur * 0.4)))
        ImageDraw.Draw(p).rectangle((70, 160, 70 + bar, 200), fill=ROJO_N + (255,))
        if lg:
            A.pegar_centro(p, lg, 380, 250)
        A.pegar_centro(im, _glitch(p, t, 0.7) if A.clamp((t - dur * 0.4) / 0.2) > 0 and int(t * 10) % 3 == 0 else p, W / 2, 900)
        ks = A.clamp((t - dur * 0.45) / 0.18)
        if ks > 0:
            st = _neon_txt(titulo, 76, (255, 255, 255))
            sl = A._tarjeta_ia(st.width + 70, st.height + 50, relleno=(224, 32, 32, 255), radio=18)
            A.pegar_centro(sl, st, sl.width / 2, sl.height / 2)
            A.pegar_centro(im, A.con_alfa(A.escalar(sl.rotate(-6, resample=Image.BICUBIC, expand=True), 2 - A.ease_out(ks)), ks), W / 2, 1150)
            A.pegar_centro(im, A.con_alfa(A._texto_img_base(sub, 40, (230, 230, 240), False), ks), W / 2, 1290)

    return _escena(dur, dib, "alerta")


def g_aviso(dur, ruta_logo=None, cifra="1.200 MILLONES", sub="de usuarios cada semana"):
    """Ventana de chat 'creando imagen…' con barra de progreso; aparece un anuncio dentro; luego la cifra."""
    lg = _logo(ruta_logo, 70, 220)

    def dib(im, t):
        v = A._tarjeta_ia(860, 520)
        d = ImageDraw.Draw(v)
        if lg:
            A.pegar_centro(v, lg, 120, 70)
        v.alpha_composite(A._texto_img_base("Creando tu imagen" + "." * (int(t * 4) % 4), 40, (255, 255, 255), False), (200, 50))
        pr = A.clamp(t / (dur * 0.8))
        d.rounded_rectangle((60, 140, 800, 175), 16, fill=(40, 44, 80, 255))
        d.rounded_rectangle((60, 140, 60 + 740 * pr, 175), 16, fill=CIAN + (255,))
        ka = A.ease_out_back(A.clamp((t - 0.5) / 0.35))
        if ka > 0:
            ad = Image.new("RGBA", (740, 260), (0, 0, 0, 0))
            ImageDraw.Draw(ad).rounded_rectangle((0, 0, 739, 259), 22, fill=(250, 250, 250, 255), outline=AMARILLO + (255,), width=6)
            ad.alpha_composite(A._texto_img_base("ANUNCIO", 30, (120, 120, 120)), (30, 24))
            A.pegar_centro(ad, A._texto_img_base("Here's an ad while", 52, (20, 20, 30)), 370, 120)
            A.pegar_centro(ad, A._texto_img_base("we create your image", 52, (20, 20, 30)), 370, 190)
            A.pegar_centro(v, A.escalar(ad, ka), 430, 360)
        A.pegar_centro(im, v, W / 2, 820)
        kc = A.ease_out_back(A.clamp((t - dur * 0.55) / 0.3))
        if kc > 0:
            A.pegar_centro(im, A.escalar(_ajustar(_neon_txt(cifra, 100, ROJO_N), 980), kc), W / 2, 1180)
            A.pegar_centro(im, A._texto_img_base(sub, 42, (230, 230, 240), False), W / 2, 1280)

    return _escena(dur, dib, "pop")


def g_cursor(dur, titulo="UN EMPLEADO DE IA EN TU PC", sello="HAY QUE SUPERVISARLO"):
    """Escritorio con ventanas; un cursor se mueve solo y hace clic; al final un sello."""
    flecha = Image.new("RGBA", (60, 80), (0, 0, 0, 0))
    ImageDraw.Draw(flecha).polygon([(0, 0), (0, 64), (16, 50), (28, 78), (38, 74), (26, 46), (46, 46)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    ruta = [(260, 700), (700, 640), (520, 900), (820, 1000), (360, 1040)]

    def dib(im, t):
        _titulo(im, titulo)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((120, 560, 960, 1180), 24, fill=(18, 22, 48, 255), outline=CIAN + (200,), width=5)
        for i, (x0, y0) in enumerate(((170, 620), (560, 610), (200, 900), (600, 900))):
            d.rounded_rectangle((x0, y0, x0 + 330, y0 + 220), 14, fill=(32, 38, 80, 255), outline=(MAGENTA if i % 2 else CIAN) + (180,), width=3)
            for k in range(3):
                d.line((x0 + 25, y0 + 60 + k * 45, x0 + 300 - k * 60, y0 + 60 + k * 45), fill=(90, 100, 150, 255), width=8)
        k = (t / dur) * (len(ruta) - 1)
        i = min(int(k), len(ruta) - 2); f = A.ease_in_out(k - i)
        x = ruta[i][0] + (ruta[i + 1][0] - ruta[i][0]) * f; y = ruta[i][1] + (ruta[i + 1][1] - ruta[i][1]) * f
        if f > 0.9:
            d.ellipse((x - 30, y - 30, x + 30, y + 30), outline=AMARILLO + (255,), width=4)
        im.alpha_composite(flecha, (int(x), int(y)))
        ks = A.clamp((t - dur * 0.6) / 0.18)
        if ks > 0:
            st = _neon_txt(sello, 56, (255, 255, 255))
            sl = A._tarjeta_ia(st.width + 60, st.height + 40, relleno=(224, 32, 32, 255), radio=18)
            A.pegar_centro(sl, st, sl.width / 2, sl.height / 2)
            A.pegar_centro(im, A.con_alfa(A.escalar(sl.rotate(-5, resample=Image.BICUBIC, expand=True), 2 - A.ease_out(ks)), ks), W / 2, 1270)

    return _escena(dur, dib, "teclas")


_construir_v6 = construir


def construir(g, dur, assets):
    t = g["tipo"]
    lg = f"{assets}/logo_{g['logo']}.png" if g.get("logo") else None
    if t == "agujero":
        return g_agujero(dur, g.get("titulo", "FABLE 5.2"), g.get("sub", "el nuevo modelo de Claude"), lg)
    if t == "australia":
        return g_australia(dur, lg, g.get("titulo", "ENTRÓ SIN PERMISO"), g.get("sub", "portal del gobierno de Australia"))
    if t == "aviso":
        return g_aviso(dur, lg, g.get("cifra", "1.200 MILLONES"), g.get("sub", "de usuarios cada semana"))
    if t == "cursor":
        return g_cursor(dur, g.get("titulo", "UN EMPLEADO DE IA EN TU PC"), g.get("sello", "HAY QUE SUPERVISARLO"))
    return _construir_v6(g, dur, assets)
