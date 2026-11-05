"""
Animaciones y gráficos para los videos de Noticias IA.

Cada gráfico se dibuja cuadro a cuadro con Pillow y se guarda como un clip
con transparencia (.mov), listo para ponerse encima del video con ffmpeg.
Todo es original (dibujado aquí); las únicas imágenes externas son los logos
de las empresas y fotos de dominio público (NASA).
"""
import math
import subprocess
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
ROJO = (224, 32, 32)
BLANCO = (255, 255, 255)
TINTA = (14, 14, 18)
FONDO_TARJETA = (14, 14, 18, 238)


def _fuente(estilo):
    ruta = subprocess.run(["fc-match", "-f", "%{file}", f"Inter:style={estilo}"], capture_output=True, text=True).stdout
    return ruta.strip()


INTER_BLACK = _fuente("Black")
INTER_BOLD = _fuente("Bold")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


@lru_cache(None)
def fuente(tam, negra=True):
    return ImageFont.truetype(INTER_BLACK if negra else INTER_BOLD, tam)


# --------------------------------------------------------------------------- curvas
def ease_out_back(x, s=1.7):
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 3 * x ** 2 - 2 * x ** 3


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def envolvente(t, dur, entrada=0.28, salida=0.2):
    """Escala y opacidad de un 'pop': entra con rebote y sale encogiéndose."""
    if t < entrada:
        k = clamp(t / entrada)
        return 0.2 + 0.8 * ease_out_back(k), clamp(k * 2.5)
    if t > dur - salida:
        k = clamp((dur - t) / salida)
        return 0.85 + 0.15 * k, k
    return 1.0, 1.0


# --------------------------------------------------------------------------- piezas
def emoji(ch, tam):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((tam, int(tam * im.height / im.width)), Image.LANCZOS)


def texto_img(texto, tam, color=BLANCO, negra=True):
    f = fuente(tam, negra)
    x0, y0, x1, y1 = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), texto, font=f)
    im = Image.new("RGBA", (x1 - x0 + 4, y1 - y0 + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-x0 + 2, -y0 + 2), texto, font=f, fill=color)
    return im


def texto_ajustado(texto, tam, max_ancho, color=BLANCO, negra=True):
    """Como texto_img, pero reduce el tamaño hasta que quepa en max_ancho."""
    im = texto_img(texto, tam, color, negra)
    while im.width > max_ancho and tam > 24:
        tam -= 3
        im = texto_img(texto, tam, color, negra)
    return im


def logo_blanco(ruta, alto_max, ancho_max):
    im = logo(ruta, alto_max, ancho_max)
    blanco = Image.new("RGBA", im.size, (255, 255, 255, 255))
    blanco.putalpha(im.getchannel("A"))
    return blanco


def tarjeta(ancho, alto, relleno=FONDO_TARJETA, radio=34, borde=(255, 255, 255, 46)):
    im = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, ancho - 1, alto - 1), radio, fill=relleno, outline=borde, width=3)
    return im


def pegar_centro(base, img, cx, cy):
    base.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


def logo(ruta, alto_max, ancho_max):
    im = Image.open(ruta).convert("RGBA")
    im = im.crop(im.getbbox())
    k = min(alto_max / im.height, ancho_max / im.width)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)


def con_alfa(img, a):
    if a >= 0.999:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    return img


def escalar(img, s):
    s = max(0.02, s)
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BILINEAR)


# --------------------------------------------------------------------------- render a clip
class Grafico:
    """Un gráfico animado: caja (x, y, ancho, alto) y una función cuadro(t) → imagen RGBA."""

    def __init__(self, dur, caja, cuadro, sonido=None):
        self.dur, self.caja, self.cuadro, self.sonido = dur, caja, cuadro, sonido

    def render(self, ruta):
        x, y, w, h = self.caja
        p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
                              "-pix_fmt", "rgba", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
                              "-c:v", "qtrle", "-pix_fmt", "argb", str(ruta)], stdin=subprocess.PIPE)
        n = max(1, round(self.dur * FPS))
        for i in range(n):
            im = self.cuadro(i / FPS)
            if im.size != (w, h):
                im = im.resize((w, h))
            p.stdin.write(im.tobytes())
        p.stdin.close()
        p.wait()
        return ruta


def pop(elemento, dur, cx, cy, sonido="pop", flotar=6, giro=0):
    """Pone un elemento (imagen) con animación de 'pop' y un leve flote."""
    margen = 1.25
    w, h = int(elemento.width * margen) + 40, int(elemento.height * margen) + 40

    def cuadro(t):
        s, a = envolvente(t, dur)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        e = escalar(elemento, s)
        if giro:
            e = e.rotate(giro * math.sin(t * 5) * (1 - clamp(t / dur)), resample=Image.BICUBIC, expand=True)
        pegar_centro(im, con_alfa(e, a), w / 2, h / 2 + flotar * math.sin(t * 3.2))
        return im

    return Grafico(dur, (int(cx - w / 2), int(cy - h / 2), w, h), cuadro, sonido)


# --------------------------------------------------------------------------- gráficos concretos
def g_logo(ruta_logo, dur, cy=560, texto=None, ancho=600):
    lg = logo(ruta_logo, 130, ancho - 120)
    alto = lg.height + (150 if texto else 90)
    c = tarjeta(max(ancho, lg.width + 120), alto, relleno=(255, 255, 255, 250), borde=(0, 0, 0, 0))
    pegar_centro(c, lg, c.width / 2, 45 + lg.height / 2)
    if texto:
        tx = texto_img(texto, 40, TINTA, negra=False)
        pegar_centro(c, tx, c.width / 2, alto - 52)
    return pop(c, dur, W / 2, cy)


def g_emoji(ch, dur, cx, cy, tam=190):
    return pop(emoji(ch, tam), dur, cx, cy, giro=10)


def g_texto(lineas, dur, cy=560, ancho=860, ch=None, acento=0):
    """Tarjeta oscura con 1–2 líneas; la línea `acento` va en rojo. Emoji opcional a la izquierda."""
    em = emoji(ch, 110) if ch else None
    libre = 960 - 90 - (140 if em else 0)
    imgs = [texto_ajustado(l, 66 if i == 0 else 44, libre, ROJO if i == acento else BLANCO, negra=i == 0)
            for i, l in enumerate(lineas)]
    cont_w = max(i.width for i in imgs) + (em.width + 30 if em else 0)
    alto = sum(i.height for i in imgs) + 22 * (len(imgs) - 1) + 80
    c = tarjeta(max(ancho, cont_w + 90), alto)
    x = (c.width - cont_w) / 2
    if em:
        pegar_centro(c, em, x + em.width / 2, alto / 2)
        x += em.width + 30
    y = 40
    for i in imgs:
        c.alpha_composite(i, (int(x), int(y)))
        y += i.height + 22
    return pop(c, dur, W / 2, cy)


def g_contador(desde, hasta, formato, etiqueta, dur, cy=560):
    """Número grande que cuenta (ej. −90%) con etiqueta y barra que se encoge."""
    cw, chh = 760, 330

    def cuadro(t):
        s, a = envolvente(t, dur)
        k = ease_out(clamp((t - 0.15) / 1.1))
        v = desde + (hasta - desde) * k
        c = tarjeta(cw, chh)
        pegar_centro(c, texto_img(formato.format(v=v), 150, ROJO), cw / 2, 120)
        pegar_centro(c, texto_img(etiqueta, 40, BLANCO, negra=False), cw / 2, 228)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((70, 268, cw - 70, 290), 11, fill=(255, 255, 255, 40))
        largo = (cw - 140) * (1 - 0.9 * k)
        d.rounded_rectangle((70, 268, 70 + max(22, largo), 290), 11, fill=ROJO)
        im = Image.new("RGBA", (cw + 120, chh + 120), (0, 0, 0, 0))
        pegar_centro(im, con_alfa(escalar(c, s), a), im.width / 2, im.height / 2)
        return im

    return Grafico(dur, (int(W / 2 - (cw + 120) / 2), int(cy - (chh + 120) / 2), cw + 120, chh + 120), cuadro, "ding")


def g_barra(etiqueta, dur, cy=560):
    cw, chh = 860, 270
    check = emoji("✅", 64)

    def cuadro(t):
        s, a = envolvente(t, dur)
        k = ease_in_out(clamp((t - 0.25) / 1.3))
        c = tarjeta(cw, chh)
        pegar_centro(c, texto_ajustado(etiqueta, 50, cw - 100, BLANCO), cw / 2, 62)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((60, 115, cw - 60, 155), 20, fill=(255, 255, 255, 40))
        d.rounded_rectangle((60, 115, 60 + max(40, (cw - 120) * k), 155), 20, fill=ROJO)
        pct = texto_img(f"{int(100 * k)}%", 58, BLANCO)
        pegar_centro(c, pct, cw / 2 - (40 if k >= 1 else 0), 212)
        if k >= 1:
            pegar_centro(c, escalar(check, ease_out_back(clamp((t - 1.55) / 0.25))), cw / 2 + pct.width / 2 + 10, 210)
        im = Image.new("RGBA", (cw + 100, chh + 100), (0, 0, 0, 0))
        pegar_centro(im, con_alfa(escalar(c, s), a), im.width / 2, im.height / 2)
        return im

    return Grafico(dur, (int(W / 2 - (cw + 100) / 2), int(cy - (chh + 100) / 2), cw + 100, chh + 100), cuadro, "ding")


def g_sello(texto, dur, cy=600, angulo=-7):
    tx = texto_ajustado(texto, 104, 860, BLANCO)
    c = Image.new("RGBA", (tx.width + 90, tx.height + 70), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 18, fill=ROJO + (255,),
                                         outline=BLANCO + (255,), width=8)
    pegar_centro(c, tx, c.width / 2, c.height / 2)
    c = c.rotate(angulo, resample=Image.BICUBIC, expand=True)
    w, h = int(c.width * 1.9), int(c.height * 1.9)

    def cuadro(t):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        if t < 0.18:
            k = ease_out(t / 0.18)
            s, a = 2.2 - 1.2 * k, k
        elif t > dur - 0.2:
            k = clamp((dur - t) / 0.2)
            s, a = 1.0, k
        else:
            s, a = 1.0, 1.0
        temblor = 10 * math.exp(-(t - 0.18) * 14) * math.sin(t * 90) if t > 0.18 else 0
        pegar_centro(im, con_alfa(escalar(c, s), a), w / 2 + temblor, h / 2)
        return im

    return Grafico(dur, (int(W / 2 - w / 2), int(cy - h / 2), w, h), cuadro, "golpe")


def g_buscador(texto, dur, cy=560):
    """Barra de búsqueda genérica: se escribe el texto y luego queda bloqueada."""
    cw, chh = 860, 150
    lupa = Image.new("RGBA", (70, 70), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lupa)
    dl.ellipse((6, 6, 46, 46), outline=(90, 90, 100), width=7)
    dl.line((40, 40, 64, 64), fill=(90, 90, 100), width=8)

    def cuadro(t):
        s, a = envolvente(t, dur)
        c = tarjeta(cw, chh, relleno=(255, 255, 255, 252), radio=75, borde=(0, 0, 0, 0))
        c.alpha_composite(lupa, (40, 40))
        n = int(clamp((t - 0.3) / 0.9) * len(texto))
        visible = texto[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(texto) else "")
        c.alpha_composite(texto_img(visible or " ", 54, TINTA, negra=False), (130, 44))
        bloqueo = clamp((t - 1.35) / 0.15)
        if bloqueo > 0:
            d = ImageDraw.Draw(c)
            d.rounded_rectangle((0, 0, cw - 1, chh - 1), 75, outline=ROJO + (int(255 * bloqueo),), width=10)
            d.line((60, chh / 2, 60 + (cw - 120) * bloqueo, chh / 2), fill=ROJO, width=12)
        im = Image.new("RGBA", (cw + 100, chh + 160), (0, 0, 0, 0))
        pegar_centro(im, con_alfa(escalar(c, s), a), im.width / 2, chh / 2 + 50)
        if bloqueo >= 1:
            et = texto_img("BLOQUEADO", 46, BLANCO)
            caja = Image.new("RGBA", (et.width + 40, et.height + 24), ROJO + (255,))
            pegar_centro(caja, et, caja.width / 2, caja.height / 2)
            pegar_centro(im, con_alfa(escalar(caja, ease_out_back(clamp((t - 1.5) / 0.25))), a),
                         im.width / 2, chh + 95)
        return im

    return Grafico(dur, (int(W / 2 - (cw + 100) / 2), int(cy - 125), cw + 100, chh + 160), cuadro, "teclas")


def g_telefono(dur, cx=W / 2, cy=520):
    """Teléfono con apps: un asistente (orbe) va tocando apps una por una."""
    pw, ph = 250, 440
    colores = [(66, 133, 244), (52, 168, 83), (251, 188, 5), (234, 67, 53), (155, 89, 182), (26, 188, 156),
               (241, 196, 15), (231, 76, 60), (52, 152, 219)]
    pos = [(55 + (i % 3) * 70, 95 + (i // 3) * 80) for i in range(9)]
    orden = [0, 4, 8, 2, 6]

    def cuadro(t):
        s, a = envolvente(t, dur)
        c = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((0, 0, pw - 1, ph - 1), 42, fill=(20, 20, 26, 245), outline=(255, 255, 255, 90), width=6)
        d.rounded_rectangle((pw / 2 - 40, 16, pw / 2 + 40, 30), 7, fill=(0, 0, 0, 255))
        paso = (t - 0.3) / 0.45
        activo = orden[int(paso) % len(orden)] if paso > 0 else -1
        for i, (x, y) in enumerate(pos):
            r = 26 if i != activo else 26 + 6 * math.sin(clamp(paso % 1) * math.pi)
            d.rounded_rectangle((x - r, y - r, x + r, y + r), 14, fill=colores[i] + (255,),
                                outline=BLANCO + (255,) if i == activo else None, width=5)
        # orbe del asistente
        o = 30 + 6 * math.sin(t * 8)
        oy = ph - 70
        for k, col in enumerate([(224, 32, 32, 90), (224, 32, 32, 170), (255, 120, 120, 255)]):
            rr = o - k * 9
            d.ellipse((pw / 2 - rr, oy - rr, pw / 2 + rr, oy + rr), fill=col)
        im = Image.new("RGBA", (pw + 80, ph + 80), (0, 0, 0, 0))
        pegar_centro(im, con_alfa(escalar(c, s), a), im.width / 2, im.height / 2)
        return im

    return Grafico(dur, (int(cx - (pw + 80) / 2), int(cy - (ph + 80) / 2), pw + 80, ph + 80), cuadro, "pop")


def g_advertencia(texto, dur, cy=560):
    em = emoji("⚠️", 110)
    tx = texto_ajustado(texto, 60, 980 - 110 - 130, BLANCO)
    c = tarjeta(tx.width + em.width + 130, max(tx.height, em.height) + 70, relleno=(150, 14, 14, 245),
                borde=(255, 255, 255, 120))
    pegar_centro(c, em, 45 + em.width / 2, c.height / 2)
    c.alpha_composite(tx, (int(em.width + 80), int(c.height / 2 - tx.height / 2)))
    w, h = c.width + 120, c.height + 120

    def cuadro(t):
        s, a = envolvente(t, dur)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dx = 9 * math.sin(t * 55) * (0.5 + 0.5 * math.sin(t * 4))
        pegar_centro(im, con_alfa(escalar(c, s), a), w / 2 + dx, h / 2)
        return im

    return Grafico(dur, (int(W / 2 - w / 2), int(cy - h / 2), w, h), cuadro, "alerta")


def g_cambio(antes, despues, dur, cy=560, ch="⏱️"):
    """'ANTES → DESPUÉS': lo de antes se tacha y aparece lo nuevo en rojo."""
    em = emoji(ch, 96)
    a_img, d_img = texto_img(antes, 62, BLANCO), texto_img(despues, 74, ROJO)
    flecha = texto_img("→", 64, BLANCO)
    cw, chh = 170 + a_img.width + 25 + flecha.width + 30 + d_img.width + 60, 210
    if cw > 980:
        k = 980 / cw
        a_img, d_img = escalar(a_img, k), escalar(d_img, k)
        cw = 980

    def cuadro(t):
        s, a = envolvente(t, dur)
        c = tarjeta(cw, chh)
        c.alpha_composite(em, (40, int(chh / 2 - em.height / 2)))
        k = ease_out(clamp((t - 0.35) / 0.35))
        ax = 170
        c.alpha_composite(a_img, (ax, int(chh / 2 - a_img.height / 2)))
        if k > 0:
            ImageDraw.Draw(c).line((ax - 6, chh / 2, ax - 6 + (a_img.width + 12) * k, chh / 2), fill=ROJO, width=10)
        k2 = ease_out_back(clamp((t - 0.7) / 0.35))
        if k2 > 0:
            c.alpha_composite(flecha, (ax + a_img.width + 25, int(chh / 2 - flecha.height / 2)))
            pegar_centro(c, escalar(d_img, max(0.05, k2)), ax + a_img.width + 25 + flecha.width + 30 + d_img.width / 2,
                         chh / 2)
        im = Image.new("RGBA", (cw + 100, chh + 100), (0, 0, 0, 0))
        pegar_centro(im, con_alfa(escalar(c, s), a), im.width / 2, im.height / 2)
        return im

    return Grafico(dur, (int(W / 2 - (cw + 100) / 2), int(cy - (chh + 100) / 2), cw + 100, chh + 100), cuadro, "whoosh")


# --------------------------------------------------------------------------- pantalla completa
def _entrada_salida(t, dur, d=0.18):
    a = min(clamp(t / d), clamp((dur - t) / d))
    s = 1.06 - 0.06 * ease_out(clamp(t / 0.35))
    return a, s


def _degradado_inferior(im):
    """Oscurece la parte de abajo para que los subtítulos se lean sobre la foto."""
    g = Image.new("L", (1, H))
    for y in range(H):
        g.putpixel((0, y), int(200 * clamp((y - H * 0.55) / (H * 0.35))))
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    sombra.putalpha(g.resize((W, H)))
    im.alpha_composite(sombra)
    return im


def g_foto(ruta, dur, etiqueta=None, zoom=(1.0, 1.14), foco=(0.5, 0.5)):
    """Foto a pantalla completa con movimiento lento (Ken Burns)."""
    foto = Image.open(ruta).convert("RGB")
    k = max(W * zoom[1] / foto.width, H * zoom[1] / foto.height)
    foto = foto.resize((int(foto.width * k) + 2, int(foto.height * k) + 2), Image.LANCZOS)
    pill = None
    if etiqueta:
        tx = texto_img(etiqueta, 40, BLANCO)
        pill = tarjeta(tx.width + 60, tx.height + 36, radio=30)
        pegar_centro(pill, tx, pill.width / 2, pill.height / 2)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        z = zoom[0] + (zoom[1] - zoom[0]) * (t / dur)
        cw, chh = W * zoom[1] / z, H * zoom[1] / z
        cx = foco[0] * (foto.width - cw) + cw / 2
        cy = foco[1] * (foto.height - chh) + chh / 2
        crop = foto.crop((int(cx - cw / 2), int(cy - chh / 2), int(cx + cw / 2), int(cy + chh / 2))).resize((W, H))
        im = _degradado_inferior(crop.convert("RGBA"))
        if pill:
            im.alpha_composite(pill, (int(W / 2 - pill.width / 2), 400))
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def _fondo_oscuro():
    im = Image.new("RGBA", (W, H), (10, 10, 14, 255))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line((x, 0, x, H), fill=(255, 255, 255, 10))
    for y in range(0, H, 60):
        d.line((0, y, W, y), fill=(255, 255, 255, 10))
    return im


def g_comparacion(izq, der, dur, logo_izq=None):
    """Pantalla completa: dos opciones enfrentadas (ej. pagar Uber vs. carro propio)."""
    fondo = _fondo_oscuro()

    def panel(ch, titulo, sub, destacado, lg=None):
        c = tarjeta(440, 560, relleno=(28, 28, 34, 255) if not destacado else (150, 14, 14, 255),
                    borde=(255, 255, 255, 60))
        pegar_centro(c, emoji(ch, 170), 220, 150)
        if lg:
            pegar_centro(c, logo_blanco(lg, 64, 300), 220, 300)
        pegar_centro(c, texto_ajustado(titulo, 56, 400, BLANCO), 220, 390 if lg else 330)
        pegar_centro(c, texto_ajustado(sub, 38, 400, BLANCO, negra=False), 220, 465 if lg else 410)
        return c

    p1 = panel(*izq, False, logo_izq)
    p2 = panel(*der, True)
    vs = texto_img("VS", 90, BLANCO)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        k1 = ease_out(clamp(t / 0.4))
        k2 = ease_out(clamp((t - 0.25) / 0.4))
        im.alpha_composite(p1, (int(-440 + (60 + 440) * k1), 560))
        im.alpha_composite(p2, (int(W + (W - 500 - W) * k2), 560))
        kv = ease_out_back(clamp((t - 0.55) / 0.3))
        if kv > 0:
            pegar_centro(im, escalar(vs, kv), W / 2, 840)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def g_ia_crea_ia(dur, titulo="IA creando mejores IA"):
    """Pantalla completa: una 'IA' genera otras, que generan otras (árbol que crece)."""
    fondo = _fondo_oscuro()
    tt = texto_img(titulo, 64, BLANCO)
    niveles = [[(W / 2, 640)], [(W / 2 - 220, 900), (W / 2 + 220, 900)],
               [(W / 2 - 330, 1160), (W / 2 - 110, 1160), (W / 2 + 110, 1160), (W / 2 + 330, 1160)]]

    def chip(tam, rojo):
        c = tarjeta(tam, int(tam * 0.62), relleno=(224, 32, 32, 255) if rojo else (34, 34, 42, 255), radio=24,
                    borde=(255, 255, 255, 120))
        pegar_centro(c, texto_img("IA", int(tam * 0.3), BLANCO), c.width / 2, c.height / 2)
        return c

    chips = [chip(230, True), chip(180, False), chip(150, False)]

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        pegar_centro(im, tt, W / 2, 420)
        d = ImageDraw.Draw(im)
        for n, nivel in enumerate(niveles):
            k = ease_out_back(clamp((t - 0.1 - n * 0.45) / 0.35))
            if k <= 0:
                continue
            for j, (x, y) in enumerate(nivel):
                if n > 0:
                    px, py = niveles[n - 1][j // 2]
                    kl = clamp((t - 0.1 - n * 0.45) / 0.25)
                    d.line((px, py + 60, px + (x - px) * kl, py + 60 + (y - 60 - py - 60) * kl),
                           fill=(255, 255, 255, 140), width=6)
                pegar_centro(im, escalar(chips[n], k), x, y)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def g_transicion(dur=0.32):
    """Barrido diagonal rojo entre noticias."""
    def cuadro(t):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        k = ease_in_out(clamp(t / dur))
        x = -W * 1.6 + (W * 3.2) * k
        d = ImageDraw.Draw(im)
        d.polygon([(x, 0), (x + 420, 0), (x + 420 - 700, H), (x - 700, H)], fill=ROJO + (255,))
        d.polygon([(x + 460, 0), (x + 520, 0), (x + 520 - 700, H), (x + 460 - 700, H)], fill=BLANCO + (255,))
        return im

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


# --------------------------------------------------------------------------- efectos de sonido (sintetizados)
def sonidos(sr=48000):
    import numpy as np

    rng = np.random.default_rng(7)

    def env(n, ataque, caida):
        e = np.ones(n)
        a = int(ataque * sr)
        e[:a] = np.linspace(0, 1, a)
        e[a:] = np.exp(-np.linspace(0, caida, n - a))
        return e

    def whoosh(d=0.45):
        n = int(d * sr)
        ruido = rng.standard_normal(n)
        # filtro paso banda que sube (barrido)
        out, y1, y2 = np.zeros(n), 0.0, 0.0
        for i in range(n):
            f = 300 + 3500 * (i / n) ** 1.5
            w = 2 * np.pi * f / sr
            r = 0.97
            y = ruido[i] + 2 * r * np.cos(w) * y1 - r * r * y2
            out[i], y2, y1 = y, y1, y
        out *= np.sin(np.linspace(0, np.pi, n)) ** 2
        return out / np.abs(out).max() * 0.5

    def tono(f0, f1, d, caida=8, armonico=0.0):
        n = int(d * sr)
        f = np.linspace(f0, f1, n)
        fase = 2 * np.pi * np.cumsum(f) / sr
        s = np.sin(fase) + armonico * np.sin(2 * fase)
        return s * env(n, 0.004, caida) * 0.6

    def golpe():
        n = int(0.35 * sr)
        s = tono(140, 50, 0.35, 9) + 0.25 * rng.standard_normal(n) * env(n, 0.002, 30)
        return s / np.abs(s).max() * 0.8

    def teclas():
        n = int(1.0 * sr)
        s = np.zeros(n)
        for k in range(8):
            i = int((0.06 + k * 0.11) * sr)
            m = int(0.02 * sr)
            s[i:i + m] += rng.standard_normal(m) * env(m, 0.001, 12) * 0.35
        return s

    return {
        "whoosh": whoosh(),
        "pop": tono(900, 380, 0.12, 14),
        "ding": tono(1320, 1320, 0.7, 6, armonico=0.4) * 0.6,
        "golpe": golpe(),
        "alerta": np.concatenate([tono(880, 880, 0.12, 4), tono(660, 660, 0.16, 4)]) * 0.5,
        "teclas": teclas(),
    }
