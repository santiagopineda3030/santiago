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
        pegar_centro(c, texto_img(formato.format(v=v).replace(".", ","), 150, ROJO), cw / 2, 120)
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


# --------------------------------------------------------------------------- escenas a pantalla completa (v2)
# Todo el contenido dentro de la zona segura de Instagram: x 120–960, y 250–1500.
def _titulo_escena(im, texto, y=330, color=BLANCO):
    if not texto:
        return
    y = max(y, 450)  # debajo del título de la noticia (y ≈ 250–380)
    pegar_centro(im, texto_ajustado(texto, 60, 820, color), W / 2, y)


def g_hacker(dur, total=81, etiqueta="fallas graves encontradas", titulo="IA HACKER DE OPENAI", ruta_logo=None):
    """Terminal que escribe código solo y va marcando fallas en rojo; contador que sube."""
    import random
    rnd = random.Random(4)
    fondo = _fondo_oscuro()
    trozos = ["scan(target)", "for f in files:", "  check(f)", "exploit?", "buffer_overflow", "auth.bypass()",
              "0x7ffe3a91", "if leak:", "  report()", "sandbox.escape", "parse(input)", "heap.alloc(4096)"]
    lineas = [(rnd.choice(trozos), rnd.random() < 0.3) for _ in range(14)]
    term = tarjeta(820, 540, relleno=(8, 12, 10, 255), radio=28, borde=(255, 255, 255, 70))
    lg = logo_blanco(ruta_logo, 90, 300) if ruta_logo else None
    f = fuente(34, negra=False)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 330, ROJO)
        tm = term.copy()
        d = ImageDraw.Draw(tm)
        visibles = int(clamp(t / (dur * 0.75)) * len(lineas)) + 1
        y0 = 40
        for i, (txt, falla) in enumerate(lineas[:visibles][-10:]):
            col = (90, 255, 140, 255)
            if falla:
                d.rounded_rectangle((24, y0 + i * 48 - 6, 796, y0 + i * 48 + 40), 8, fill=(150, 14, 14, 255))
                col = BLANCO + (255,)
                txt = "⚠ FALLA · " + txt
            d.text((40, y0 + i * 48), "> " + txt, font=f, fill=col)
        im.alpha_composite(tm, (130, 540))
        k = ease_out(clamp(t / (dur * 0.8)))
        n = texto_img(f"{round(total * k)}", 150, ROJO)
        pegar_centro(im, n, W / 2, 1180)
        pegar_centro(im, texto_ajustado(etiqueta, 44, 820, BLANCO, negra=False), W / 2, 1295)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "teclas")


def g_fuga(dur, logo_a, logo_b, n=3, texto="3 salidas en dos semanas", titulo="EL EQUIPO DE CLAUDE CODE"):
    """Personas que se pasan de una empresa a otra, una por una."""
    fondo = _fondo_oscuro()
    ca = tarjeta(300, 220, relleno=(255, 255, 255, 250), borde=(0, 0, 0, 0))
    pegar_centro(ca, logo(logo_a, 110, 240), 150, 110)
    cb = tarjeta(300, 220, relleno=(255, 255, 255, 250), borde=(0, 0, 0, 0))
    pegar_centro(cb, logo(logo_b, 110, 240), 150, 110)
    per = emoji("🧑‍💻", 120)
    xa, xb, y = 280, 800, 820

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 360)
        pegar_centro(im, ca, xa, y)
        pegar_centro(im, cb, xb, y)
        llegadas = 0
        for i in range(n):
            k = ease_in_out(clamp((t - 0.25 - i * (dur - 0.9) / n) / 0.55))
            if k >= 1:
                llegadas += 1
            x = xa + (xb - xa) * k
            yy = y + 230 - math.sin(math.pi * k) * 200
            pegar_centro(im, per, x + (i - (n - 1) / 2) * 95 * k, yy)
        cont = texto_img(f"{llegadas}", 130, ROJO)
        pegar_centro(im, cont, W / 2, 1200)
        pegar_centro(im, texto_ajustado(texto, 46, 820, BLANCO, negra=False), W / 2, 1320)
        d = ImageDraw.Draw(im)
        d.line((xa + 170, y, xb - 170, y), fill=(255, 255, 255, 90), width=6)
        d.polygon([(xb - 170, y), (xb - 195, y - 16), (xb - 195, y + 16)], fill=(255, 255, 255, 140))
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def g_versus(dur, izq, der, sello, titulo="DEMANDA"):
    """Dos partes enfrentadas y un sello que cae al final. izq/der = (texto, ruta_logo o None, emoji o None)."""
    fondo = _fondo_oscuro()

    def panel(txt, lg, ch, rojo):
        c = tarjeta(360, 420, relleno=(150, 14, 14, 255) if rojo else (28, 28, 34, 255), borde=(255, 255, 255, 70))
        if lg:
            pegar_centro(c, logo_blanco(lg, 110, 280), 180, 160)
        elif ch:
            pegar_centro(c, emoji(ch, 150), 180, 160)
        pegar_centro(c, texto_ajustado(txt, 46, 320, BLANCO), 180, 330)
        return c

    p1, p2 = panel(*izq, True), panel(*der, False)
    vs = texto_img("VS", 100, BLANCO)
    st = texto_img(sello, 74, BLANCO)
    sl = tarjeta(st.width + 70, st.height + 50, relleno=ROJO + (255,), radio=18, borde=(255, 255, 255, 230))
    pegar_centro(sl, st, sl.width / 2, sl.height / 2)
    sl = sl.rotate(-6, resample=Image.BICUBIC, expand=True)
    mazo = emoji("⚖️", 150)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 340)
        k1, k2 = ease_out(clamp(t / 0.35)), ease_out(clamp((t - 0.15) / 0.35))
        im.alpha_composite(p1, (int(-360 + (130 + 360) * k1), 560))
        im.alpha_composite(p2, (int(W + (W - 130 - 360 - W) * k2), 560))
        kv = ease_out_back(clamp((t - 0.4) / 0.25))
        if kv > 0:
            pegar_centro(im, escalar(vs, kv), W / 2, 770)
        ks = clamp((t - dur * 0.45) / 0.18)
        if ks > 0:
            s = 2.2 - 1.2 * ease_out(ks)
            pegar_centro(im, con_alfa(escalar(sl, s), ks), W / 2, 1100)
            pegar_centro(im, mazo, W / 2, 1280)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "golpe")


def g_lluvia(dur, total=164, etiqueta="demandas por derechos de autor", titulo="DEMANDAS CONTRA LA IA"):
    """Cuadrícula de documentos que se van llenando de rojo hasta el total."""
    fondo = _fondo_oscuro()
    cols, filas = 14, 12
    ox, oy, paso = 150, 530, 54

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 360)
        d = ImageDraw.Draw(im)
        k = ease_out(clamp(t / (dur * 0.75)))
        n = round(total * k)
        for i in range(cols * filas):
            x, y = ox + (i % cols) * paso, oy + (i // cols) * paso
            if i < n:
                d.rounded_rectangle((x, y, x + 40, y + 48), 6, fill=ROJO + (255,))
                d.line((x + 8, y + 16, x + 32, y + 16), fill=BLANCO + (220,), width=3)
                d.line((x + 8, y + 28, x + 28, y + 28), fill=BLANCO + (220,), width=3)
            elif i < total:
                d.rounded_rectangle((x, y, x + 40, y + 48), 6, outline=(255, 255, 255, 60), width=2)
        pegar_centro(im, texto_img(f"{n}", 150, BLANCO), W / 2, 1220)
        pegar_centro(im, texto_ajustado(etiqueta, 44, 820, BLANCO, negra=False), W / 2, 1320)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "teclas")


def g_carrera(dur, a_txt="Claude", b_txt="ChatGPT", pregunta="¿Claude se queda atrás?"):
    """Dos barras que compiten; la de b se adelanta y aparece la pregunta."""
    fondo = _fondo_oscuro()
    la, lb = texto_img(a_txt, 54, BLANCO), texto_img(b_txt, 54, BLANCO)
    q = texto_ajustado(pregunta, 66, 840, BLANCO)
    ch = emoji("🤔", 160)

    def cuadro(t):
        al, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, "LA CARRERA DE LA IA", 360, ROJO)
        d = ImageDraw.Draw(im)
        k = ease_out(clamp(t / (dur * 0.7)))
        for i, (lab, final, col) in enumerate(((la, 0.55, (90, 90, 104, 255)), (lb, 0.92, ROJO + (255,)))):
            y = 620 + i * 230
            im.alpha_composite(lab, (140, y - 70))
            d.rounded_rectangle((140, y, 940, y + 90), 45, fill=(40, 40, 48, 255))
            d.rounded_rectangle((140, y, 140 + max(90, int(800 * final * k)), y + 90), 45, fill=col)
        kq = ease_out_back(clamp((t - dur * 0.55) / 0.3))
        if kq > 0:
            pegar_centro(im, escalar(q, kq), W / 2, 1150)
            pegar_centro(im, escalar(ch, kq), W / 2, 1290)
        return con_alfa(im, al)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def g_precio(dur, precio="≈ US$1", sub="por video de 15 s", ruta_logo=None):
    """Un celular con un video vertical que se reproduce, y el precio comparado con un café."""
    fondo = _fondo_oscuro()
    tel = tarjeta(330, 600, relleno=(20, 20, 26, 255), radio=46, borde=(255, 255, 255, 160))
    lg = logo_blanco(ruta_logo, 70, 260) if ruta_logo else None
    cafe = emoji("☕", 130)
    pr = texto_img(precio, 96, ROJO)
    sb = texto_ajustado(sub, 42, 460, BLANCO, negra=False)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, "VIDEOS CON IA", 340)
        if lg:
            pegar_centro(im, lg, W / 2, 540)
        tm = tel.copy()
        d = ImageDraw.Draw(tm)
        d.rounded_rectangle((22, 60, 308, 540), 22, fill=(60, 30, 120, 255))
        d.polygon([(135, 250), (135, 350), (215, 300)], fill=BLANCO + (230,))
        d.rounded_rectangle((40, 515, 40 + int(250 * clamp(t / dur)), 525), 5, fill=ROJO + (255,))
        k = ease_out_back(clamp(t / 0.35))
        pegar_centro(im, escalar(tm, 0.6 + 0.4 * k), 330, 860)
        kp = ease_out_back(clamp((t - 0.35) / 0.3))
        if kp > 0:
            pegar_centro(im, escalar(pr, kp), 740, 760)
            pegar_centro(im, escalar(sb, kp), 740, 850)
        kc = ease_out_back(clamp((t - 0.7) / 0.3))
        if kc > 0:
            pegar_centro(im, escalar(texto_img("=", 90, BLANCO), kc), 640, 1010)
            pegar_centro(im, escalar(cafe, kc), 780, 1010)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "ding")


def g_billetes(dur, hasta=3000, titulo="LO QUE PIDEN LAS DISQUERAS"):
    """Billetes que caen y un contador que sube hasta US$X millones."""
    import random
    rnd = random.Random(9)
    fondo = _fondo_oscuro()
    bill = emoji("💵", 110)
    caidas = [(rnd.uniform(150, 930), rnd.uniform(0, 0.8), rnd.uniform(-25, 25)) for _ in range(18)]

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450)
        for x, t0, giro in caidas:
            k = clamp((t - t0) / 0.9)
            if 0 < k < 1:
                pegar_centro(im, bill.rotate(giro * k * 3, expand=True), x, 520 + 820 * ease_in_out(k))
        v = round(hasta * ease_out(clamp(t / (dur * 0.7))))
        pegar_centro(im, texto_img(f"US${v:,}".replace(",", "."), 130, ROJO), W / 2, 900)
        pegar_centro(im, texto_img("MILLONES DE DÓLARES", 58, BLANCO), W / 2, 1030)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "ding")


def g_anuncio(dur, ruta_logo=None, titulo="YA ESTÁ EN GOOGLE ADS"):
    """Panel de campaña de anuncios: el video hecho con IA se sube y se activa."""
    fondo = _fondo_oscuro()
    panel = tarjeta(820, 700, relleno=(245, 245, 248, 255), radio=30, borde=(0, 0, 0, 0))
    if ruta_logo:
        pegar_centro(panel, logo(ruta_logo, 80, 300), 120, 80)
    pegar_centro(panel, texto_img("Nueva campaña", 46, TINTA), 470, 80)
    ok = texto_img("✓ ACTIVA", 50, (20, 150, 70))

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        p = panel.copy()
        d = ImageDraw.Draw(p)
        k = ease_out(clamp(t / (dur * 0.55)))
        d.rounded_rectangle((60, 170, 300, 600), 22, fill=(60, 30, 120, 255))
        d.polygon([(150, 340), (150, 430), (220, 385)], fill=BLANCO + (230,))
        pegar_centro(p, texto_img("Video con IA · 15 s", 40, TINTA), 560, 230)
        d.rounded_rectangle((340, 300, 780, 340), 20, fill=(220, 220, 228, 255))
        d.rounded_rectangle((340, 300, 340 + int(440 * k), 340), 20, fill=ROJO + (255,))
        pegar_centro(p, texto_img(f"Subiendo {round(100 * k)}%", 36, TINTA, negra=False), 560, 390)
        kk = ease_out_back(clamp((t - dur * 0.6) / 0.25))
        if kk > 0:
            pegar_centro(p, escalar(ok, kk), 560, 520)
        im.alpha_composite(p, (130, 560))
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "pop")


def g_igual(dur, izq="☕", der="🎬", texto="El video de tu anuncio", sub="por lo que cuesta un café"):
    """Dos cosas que valen lo mismo: emoji = emoji, con texto."""
    fondo = _fondo_oscuro()
    e1, e2 = emoji(izq, 230), emoji(der, 230)
    ig = texto_img("=", 150, BLANCO)
    t1, t2 = texto_ajustado(texto, 64, 840, BLANCO), texto_ajustado(sub, 50, 840, ROJO)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        k1, k2, k3 = (ease_out_back(clamp((t - d) / 0.3)) for d in (0.0, 0.2, 0.4))
        if k1 > 0:
            pegar_centro(im, escalar(e1, k1), 270, 780)
        if k2 > 0:
            pegar_centro(im, escalar(ig, k2), W / 2, 780)
        if k3 > 0:
            pegar_centro(im, escalar(e2, k3), 810, 780)
        kt = ease_out(clamp((t - 0.35) / 0.3))
        if kt > 0:
            pegar_centro(im, con_alfa(t1, kt), W / 2, 1050)
            pegar_centro(im, con_alfa(t2, kt), W / 2, 1140)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "pop")


# --------------------------------------------------------------------------- escenas v3 (6 nov)
def texto_emoji(ch, texto, tam, color=BLANCO, negra=True):
    """Emoji a color + texto en la misma línea (la fuente Inter no dibuja emojis)."""
    e = emoji(ch, int(tam * 1.15))
    tx = texto_img(texto, tam, color, negra)
    im = Image.new("RGBA", (e.width + 14 + tx.width, max(e.height, tx.height)), (0, 0, 0, 0))
    im.alpha_composite(e, (0, (im.height - e.height) // 2))
    im.alpha_composite(tx, (e.width + 14, (im.height - tx.height) // 2))
    return im


def _banco(tam=360, color=BLANCO):
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = tam
    d.polygon([(w * 0.08, w * 0.34), (w * 0.5, w * 0.08), (w * 0.92, w * 0.34)], fill=color + (255,))
    d.rectangle((w * 0.1, w * 0.36, w * 0.9, w * 0.42), fill=color + (255,))
    for i in range(5):
        x = w * (0.16 + i * 0.16)
        d.rectangle((x, w * 0.46, x + w * 0.07, w * 0.8), fill=color + (255,))
    d.rectangle((w * 0.06, w * 0.82, w * 0.94, w * 0.9), fill=color + (255,))
    return im


def g_hack_banco(dur, hasta=1_000_000, titulo="IAs ATACANDO BANCOS"):
    """Gancho: banco bajo ataque, lluvia de código rojo, alerta parpadeando y dinero que se va."""
    import random
    rnd = random.Random(11)
    f = fuente(34, negra=False)
    cols = [(x, rnd.uniform(0, 1), rnd.uniform(500, 1100)) for x in range(130, 960, 46)]
    chars = "01$#@!ABCDEF0x7F"
    banco = _banco(380)
    banco_r = _banco(380, ROJO)
    alerta = tarjeta(520, 110, relleno=ROJO + (255,), radio=24, borde=(255, 255, 255, 230))
    pegar_centro(alerta, texto_img("⚠ ATAQUE CON IA", 54, BLANCO), 260, 55)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur, 0.1)
        im = Image.new("RGBA", (W, H), (18, 4, 6, 255))
        d = ImageDraw.Draw(im)
        for x, fase, vel in cols:
            y0 = ((fase * 1400 + t * vel) % 1400) + 250
            for k in range(9):
                yy = y0 - k * 40
                if 250 <= yy <= 1500:
                    d.text((x, yy), rnd.choice(chars), font=f, fill=(255, 60, 60, max(20, 230 - k * 26)))
        _titulo_escena(im, titulo, 450)
        sacudida = 10 * math.sin(t * 60) * clamp(1 - t / 0.5)
        roja = int(t * 6) % 2 == 0
        pegar_centro(im, banco_r if roja else banco, W / 2 + sacudida, 760)
        ka = ease_out_back(clamp((t - 0.15) / 0.25))
        if ka > 0:
            pegar_centro(im, escalar(alerta, ka), W / 2, 1010)
        v = round(hasta * ease_out(clamp((t - 0.2) / (dur * 0.7))))
        pegar_centro(im, texto_img(f"-US${v:,}".replace(",", "."), 104, ROJO), W / 2, 1180)
        pegar_centro(im, texto_img("robados con IA", 44, BLANCO, negra=False), W / 2, 1270)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "alerta")


def g_swat(dur, titulo="EL SWAT DE LA IA", sub="Estados Unidos"):
    """Gancho: radar que barre y marca a los hackers con una X; placa de SWAT que cae."""
    fondo = _fondo_oscuro()
    cx, cy, r = W / 2, 860, 330
    hk = emoji("🦹", 96)
    objetivos = [(-160, -120), (170, -60), (-60, 170), (120, 190), (-220, 60)]
    tt = texto_ajustado(titulo, 60, 760, BLANCO)
    placa = tarjeta(tt.width + 80, 130, relleno=ROJO + (255,), radio=20, borde=(255, 255, 255, 230))
    pegar_centro(placa, tt, placa.width / 2, 65)
    sb = texto_emoji("🇺🇸", sub, 46)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur, 0.1)
        im = fondo.copy()
        d = ImageDraw.Draw(im)
        for k in (1, 0.66, 0.33):
            d.ellipse((cx - r * k, cy - r * k, cx + r * k, cy + r * k), outline=(90, 255, 140, 120), width=4)
        d.line((cx - r, cy, cx + r, cy), fill=(90, 255, 140, 60), width=2)
        d.line((cx, cy - r, cx, cy + r), fill=(90, 255, 140, 60), width=2)
        ang = t * 4.2
        for j in range(18):
            aa = ang - j * 0.04
            d.line((cx, cy, cx + r * math.cos(aa), cy + r * math.sin(aa)), fill=(90, 255, 140, 200 - j * 11), width=6)
        for ox, oy in objetivos:
            pegar_centro(im, hk, cx + ox, cy + oy)
            a_obj = math.atan2(oy, ox) % (2 * math.pi)
            if ang % (2 * math.pi) > a_obj or ang > 2 * math.pi:
                d.line((cx + ox - 50, cy + oy - 50, cx + ox + 50, cy + oy + 50), fill=ROJO + (255,), width=14)
                d.line((cx + ox + 50, cy + oy - 50, cx + ox - 50, cy + oy + 50), fill=ROJO + (255,), width=14)
        kp = clamp((t - 0.1) / 0.2)
        if kp > 0:
            pegar_centro(im, con_alfa(escalar(placa, 2.0 - ease_out(kp)), kp), W / 2, 450)
            pegar_centro(im, con_alfa(sb, kp), W / 2, 560)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "golpe")


def g_paises(dur, titulo="ALERTA EN LOS BANCOS"):
    """Dos países en alerta con anillos rojos que laten."""
    fondo = _fondo_oscuro()

    def panel(flag, nombre, txt):
        c = tarjeta(360, 470, relleno=(28, 28, 34, 255), borde=(255, 255, 255, 70))
        pegar_centro(c, emoji(flag, 150), 180, 140)
        pegar_centro(c, texto_img(nombre, 50, BLANCO), 180, 270)
        pegar_centro(c, texto_ajustado(txt, 36, 320, BLANCO, negra=False), 180, 370)
        return c

    p1 = panel("🇮🇳", "India", "alerta a todos sus bancos")
    p2 = panel("🇰🇷", "Corea del Sur", "una IA ya hackeó bancos")

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        d = ImageDraw.Draw(im)
        for i, (p, x) in enumerate(((p1, 130), (p2, 590))):
            k = ease_out_back(clamp((t - i * 0.2) / 0.3))
            if k <= 0:
                continue
            pul = (t * 1.6 + i * 0.5) % 1
            rr = 200 + 140 * pul
            ccx, ccy = x + 180, 780
            d.ellipse((ccx - rr, ccy - rr, ccx + rr, ccy + rr), outline=ROJO + (int(200 * (1 - pul)),), width=8)
            pegar_centro(im, escalar(p, k), ccx, ccy)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "alerta")


def g_itinerario(dur, ruta_logo=None, titulo="TU AGENTE DE VIAJES CON IA"):
    """Celular con un mapa: la ruta se dibuja entre pines y aparecen las partes del viaje."""
    fondo = _fondo_oscuro()
    lg = logo_blanco(ruta_logo, 80, 300) if ruta_logo else None
    pines = [(70, 420), (170, 300), (250, 360), (210, 170)]
    items = [("✈️", "Vuelo"), ("🏠", "Dónde dormir"), ("🗺️", "Mapa"), ("📸", "Fotos")]

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450)
        if lg:
            pegar_centro(im, lg, W / 2, 545)
        tel = tarjeta(330, 600, relleno=(232, 240, 236, 255), radio=46, borde=(255, 255, 255, 200))
        d = ImageDraw.Draw(tel)
        for gx in range(0, 330, 40):
            d.line((gx, 0, gx, 600), fill=(200, 214, 206, 255), width=2)
        for gy in range(0, 600, 40):
            d.line((0, gy, 330, gy), fill=(200, 214, 206, 255), width=2)
        k = clamp(t / (dur * 0.6)) * (len(pines) - 1)
        for i in range(len(pines) - 1):
            f = clamp(k - i)
            if f > 0:
                (x0, y0), (x1, y1) = pines[i], pines[i + 1]
                d.line((x0, y0, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f), fill=ROJO + (255,), width=8)
        for i, (x, y) in enumerate(pines):
            if k >= i - 0.05:
                d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=ROJO + (255,), outline=BLANCO + (255,), width=4)
        im.alpha_composite(tel, (140, 640))
        for i, txt in enumerate(items):
            ki = ease_out_back(clamp((t - 0.3 - i * 0.22) / 0.25))
            if ki > 0:
                c = tarjeta(380, 100, relleno=(28, 28, 34, 255), radio=22, borde=(255, 255, 255, 80))
                pegar_centro(c, texto_emoji(txt[0], txt[1], 40), 190, 50)
                pegar_centro(im, escalar(c, ki), 720, 720 + i * 125)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "pop")


def g_resumen_ia(dur, porcentaje=-7.4, titulo="LA IA DE GOOGLE VS. USA TODAY"):
    """Búsqueda: aparece el resumen con IA arriba, el link al periódico se hunde y caen los ingresos."""
    fondo = _fondo_oscuro()
    caja = tarjeta(820, 100, relleno=(255, 255, 255, 255), radio=50, borde=(0, 0, 0, 0))
    resumen = tarjeta(820, 250, relleno=(232, 236, 255, 255), radio=26, borde=(0, 0, 0, 0))
    pegar_centro(resumen, texto_emoji("✨", "Resumen con IA", 44, (60, 60, 140)), 240, 50)
    dr = ImageDraw.Draw(resumen)
    for i, w in enumerate((720, 680, 560)):
        dr.rounded_rectangle((40, 100 + i * 45, 40 + w, 122 + i * 45), 10, fill=(190, 196, 230, 255))
    link = tarjeta(820, 120, relleno=(255, 255, 255, 255), radio=22, borde=(0, 0, 0, 0))
    pegar_centro(link, texto_img("USA TODAY · la noticia completa", 38, (30, 30, 160)), 410, 60)
    q = "noticias de hoy"

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450)
        c = caja.copy()
        n = int(clamp(t / 0.5) * len(q))
        pegar_centro(c, texto_emoji("🔍", q[:n] or " ", 40, TINTA, negra=False), 410, 50)
        im.alpha_composite(c, (130, 540))
        kr = ease_out(clamp((t - 0.5) / 0.3))
        y_link = 680 + int(280 * kr)
        if kr > 0:
            im.alpha_composite(con_alfa(resumen, kr), (130, 670))
        im.alpha_composite(con_alfa(link, 1 - 0.6 * kr), (130, y_link))
        kc = clamp((t - 0.8) / 0.4)
        if kc > 0 and porcentaje is not None:
            v = porcentaje * ease_out(kc)
            pegar_centro(im, texto_img(f"{v:.1f} %".replace(".", ","), 120, ROJO), W / 2, 1230)
            pegar_centro(im, texto_img("en sus ingresos", 44, BLANCO, negra=False), W / 2, 1330)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "whoosh")


def g_app(dur, titulo="CURSOR CREA LA APP COMPLETA", pedido="Hazme una app de reservas"):
    """Escribes lo que quieres y se va armando la app: base de datos, inicio de sesión, link y seguridad."""
    fondo = _fondo_oscuro()
    pasos = ["Base de datos", "Inicio de sesión", "Link para compartir", "Revisión de seguridad"]
    f = fuente(38, negra=False)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        ed = tarjeta(820, 120, relleno=(8, 12, 10, 255), radio=22, borde=(255, 255, 255, 70))
        n = int(clamp(t / 0.6) * len(pedido))
        ImageDraw.Draw(ed).text((36, 38), "> " + pedido[:n] + ("_" if int(t * 4) % 2 else ""), font=f,
                                fill=(90, 255, 140, 255))
        im.alpha_composite(ed, (130, 540))
        for i, p in enumerate(pasos):
            k = ease_out_back(clamp((t - 0.6 - i * 0.25) / 0.25))
            if k <= 0:
                continue
            c = tarjeta(820, 110, relleno=(28, 28, 34, 255), radio=22, borde=(255, 255, 255, 70))
            pegar_centro(c, texto_img(p, 46, BLANCO), 360, 55)
            pegar_centro(c, texto_img("✓", 60, (90, 255, 140)), 760, 55)
            pegar_centro(im, escalar(c, k), W / 2, 760 + i * 135)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "ding")


# --------------------------------------------------------------------------- escenas v4 (7 nov)
def g_llamada(dur, hasta=129_000_000, titulo="VOZ CLONADA CON IA", quien="El jefe"):
    """Gancho: celular sonando con una llamada del 'jefe', onda de voz y contador de dinero robado."""
    fondo = Image.new("RGBA", (W, H), (14, 6, 8, 255))
    tel = tarjeta(420, 640, relleno=(20, 20, 26, 255), radio=56, borde=(255, 255, 255, 170))
    avatar = emoji("👔", 150)
    nom = texto_img(quien, 52, BLANCO)
    sub = texto_img("llamada entrante...", 34, (200, 200, 210), negra=False)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur, 0.1)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        tm = tel.copy()
        d = ImageDraw.Draw(tm)
        for k in range(3):
            pul = (t * 1.5 + k / 3) % 1
            rr = 90 + 120 * pul
            d.ellipse((210 - rr, 190 - rr, 210 + rr, 190 + rr), outline=(90, 255, 140, int(170 * (1 - pul))), width=5)
        pegar_centro(tm, avatar, 210, 190)
        pegar_centro(tm, nom, 210, 340)
        pegar_centro(tm, sub, 210, 390)
        for i in range(24):
            h = 12 + 70 * abs(math.sin(t * 9 + i * 0.7)) * (0.4 + 0.6 * abs(math.sin(i * 1.3)))
            x = 50 + i * 13.5
            d.rounded_rectangle((x, 500 - h / 2, x + 8, 500 + h / 2), 4, fill=ROJO + (255,))
        sac = 8 * math.sin(t * 50) * (1 if int(t * 3) % 2 == 0 else 0)
        im.alpha_composite(tm, (int(W / 2 - 210 + sac), 520))
        v = round(hasta * ease_out(clamp((t - 0.2) / (dur * 0.7))))
        pegar_centro(im, texto_img(f"-US${v:,}".replace(",", "."), 92, ROJO), W / 2, 1250)
        pegar_centro(im, texto_img("robados con su voz falsa", 42, BLANCO, negra=False), W / 2, 1340)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "alerta")


def g_bolsa(dur, cifra="-2,3 BILLONES", sub="en un solo día", titulo="WALL STREET SE DESPLOMA"):
    """Gráfico de bolsa que se cae en rojo, flecha hacia abajo y la cifra que golpea."""
    import random
    rnd = random.Random(5)
    fondo = _fondo_oscuro()
    puntos = [0.25]
    for i in range(40):
        puntos.append(puntos[-1] + rnd.uniform(-0.03, 0.04) if i < 16 else puntos[-1] + rnd.uniform(0.01, 0.06))
    x0, x1, y0, y1 = 140, 940, 560, 1080

    def cuadro(t):
        a, _ = _entrada_salida(t, dur, 0.1)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        d = ImageDraw.Draw(im)
        d.rectangle((x0, y0, x1, y1), outline=(255, 255, 255, 50), width=2)
        n = max(2, int(clamp(t / (dur * 0.65)) * len(puntos)))
        pts = [(x0 + (x1 - x0) * i / (len(puntos) - 1), y0 + (y1 - y0) * min(1, p)) for i, p in enumerate(puntos[:n])]
        col = (90, 255, 140, 255) if n < 18 else ROJO + (255,)
        d.line(pts, fill=col, width=10, joint="curve")
        if n >= 18:
            ex, ey = pts[-1]
            d.polygon([(ex - 30, ey - 10), (ex + 30, ey - 10), (ex, ey + 40)], fill=ROJO + (255,))
        kc = ease_out_back(clamp((t - dur * 0.55) / 0.25))
        if kc > 0:
            pegar_centro(im, escalar(texto_img(cifra, 104, ROJO), kc), W / 2, 1220)
            pegar_centro(im, escalar(texto_img(sub, 44, BLANCO, negra=False), kc), W / 2, 1320)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "golpe")


def g_ejercito(dur, total=300, titulo="UN HACKER Y SU EJÉRCITO DE IA"):
    """Un hacker en el centro; aparecen decenas de agentes de IA y van robando llaves."""
    import random
    rnd = random.Random(8)
    fondo = _fondo_oscuro()
    hk = emoji("🦹", 170)
    bot = emoji("🤖", 70)
    llave = emoji("🔑", 60)
    pos = [(rnd.uniform(160, 920), rnd.uniform(560, 1120)) for _ in range(28)]
    pos = [p for p in pos if abs(p[0] - W / 2) > 120 or abs(p[1] - 840) > 120]

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450)
        for i, (x, y) in enumerate(pos):
            k = ease_out_back(clamp((t - i * 0.035) / 0.2))
            if k > 0:
                pegar_centro(im, escalar(bot, k), x, y)
            kl = clamp((t - 0.6 - i * 0.03) / 0.3)
            if 0 < kl < 1:
                pegar_centro(im, llave, x + (W / 2 - x) * ease_in_out(kl), y + (840 - y) * ease_in_out(kl))
        pegar_centro(im, hk, W / 2, 840)
        v = round(total * ease_out(clamp((t - 0.5) / (dur * 0.6))))
        pegar_centro(im, texto_emoji("🔑", f"{v} llaves robadas", 64, ROJO), W / 2, 1270)
        pegar_centro(im, texto_img("de apps de iPhone", 42, BLANCO, negra=False), W / 2, 1360)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "teclas")


def g_nunca_duerme(dur, ruta_logo=None, precio="200 dólares al mes", titulo="EL EMPLEADO QUE NUNCA DUERME"):
    """Oficina de noche: un reloj que gira 24 h, un computador trabajando y avisos que llegan."""
    fondo = Image.new("RGBA", (W, H), (10, 12, 30, 255))
    d0 = ImageDraw.Draw(fondo)
    import random
    rnd = random.Random(3)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(250, 700)
        d0.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255, 120))
    lg = logo_blanco(ruta_logo, 80, 300) if ruta_logo else None
    luna = emoji("🌙", 110)
    avisos = [("🔔", "Un cliente dejó de comprar"), ("📋", "Plan para recuperarlo"), ("✅", "Te aviso para decidir")]

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450)
        if lg:
            pegar_centro(im, lg, W / 2, 545)
        pegar_centro(im, luna, 860, 640)
        d = ImageDraw.Draw(im)
        cx, cy, r = 300, 780, 130
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLANCO + (220,), width=8)
        ang = t * 7
        d.line((cx, cy, cx + r * 0.8 * math.sin(ang), cy - r * 0.8 * math.cos(ang)), fill=ROJO + (255,), width=8)
        d.line((cx, cy, cx + r * 0.5 * math.sin(ang / 12), cy - r * 0.5 * math.cos(ang / 12)), fill=BLANCO + (255,), width=10)
        pegar_centro(im, texto_img("24 h", 60, BLANCO), cx, cy + r + 60)
        for i, (ch, txt) in enumerate(avisos):
            k = ease_out_back(clamp((t - 0.3 - i * 0.35) / 0.25))
            if k > 0:
                c = tarjeta(470, 100, relleno=(28, 28, 40, 255), radio=22, borde=(255, 255, 255, 80))
                pegar_centro(c, texto_emoji(ch, txt, 30), 235, 50)
                pegar_centro(im, escalar(c, k), 700, 740 + i * 120)
        kp = ease_out(clamp((t - dur * 0.6) / 0.3))
        if kp > 0:
            pegar_centro(im, con_alfa(texto_img(precio, 70, ROJO), kp), W / 2, 1230)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "ding")


def g_rebelde(dur, titulo="¿LA IA SE ESTÁ REBELANDO?"):
    """Un robot que se niega: barra de rendimiento que cae −40 % y un signo de pregunta."""
    fondo = _fondo_oscuro()
    robot = emoji("🤖", 220)

    def cuadro(t):
        a, _ = _entrada_salida(t, dur)
        im = fondo.copy()
        _titulo_escena(im, titulo, 450, ROJO)
        giro = 12 * math.sin(t * 6)
        pegar_centro(im, robot.rotate(giro, resample=Image.BICUBIC, expand=True), W / 2, 760)
        d = ImageDraw.Draw(im)
        k = ease_out(clamp((t - 0.3) / (dur * 0.5)))
        d.rounded_rectangle((140, 1000, 940, 1070), 35, fill=(40, 40, 48, 255))
        d.rounded_rectangle((140, 1000, 140 + int(800 * (1 - 0.4 * k)), 1070), 35, fill=ROJO + (255,))
        pegar_centro(im, texto_img(f"-{round(40 * k)} %", 110, ROJO), W / 2, 1200)
        pegar_centro(im, texto_img("de rendimiento en seguridad", 40, BLANCO, negra=False), W / 2, 1300)
        return con_alfa(im, a)

    return Grafico(dur, (0, 0, W, H), cuadro, "alerta")


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
