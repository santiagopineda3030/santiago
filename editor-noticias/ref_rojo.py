"""Escenas estilo REFERENTE DE NOTICIAS (referentes/noticias-ref1, 12 nov · v8, pedido de Santi):
fondo negro con resplandor rojo en el centro, títulos de 2 líneas (palabra corta en sans negrita + frase grande en
serif itálica con subrayado rojo, palabra por palabra), onda roja de neón con nodos numerados, contadores que suben,
cuadrícula que se llena, íconos en círculos con borde fino. Ritmo suave: fundidos y zooms.

Se engancha en cyber.construir (editar_v2 lo llama primero). Tipos: ref_cifra, ref_vs, ref_onda, ref_perdida,
ref_despidos, ref_candado, ref_seguro, ref_titulo.
"""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import animaciones as A

W, H = A.W, A.H
ROJO = (255, 46, 60)
ROJO_OSC = (150, 10, 20)
VERDE = (60, 230, 120)
BLANCO = (255, 255, 255)
GRIS = (175, 175, 185)
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


@lru_cache(None)
def _serif(tam, negra=False):
    try:
        return ImageFont.truetype(SERIF_BI if negra else SERIF_IT, tam)
    except OSError:
        return ImageFont.truetype(SERIF_IT, tam)


def _txt_serif(texto, tam, color=BLANCO, negra=False):
    f = _serif(tam, negra)
    x0, y0, x1, y1 = f.getbbox(texto)
    im = Image.new("RGBA", (x1 - x0 + 20, y1 - y0 + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - x0, 10 - y0), texto, font=f, fill=color + (255,))
    return im


def _sans(texto, tam, color=BLANCO, negra=True):
    return A._texto_img_base(texto, tam, color, negra)


def _glow(im, radio=12, fuerza=1.7):
    return A._brillo(im, radio, fuerza)


def _ajustar(img, ancho):
    return img if img.width <= ancho else A.escalar(img, ancho / img.width)


_cache = {}


def _fondo():
    if "f" not in _cache:
        y, x = np.mgrid[0:H, 0:W]
        d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.5) / (H * 0.42)) ** 2)
        g = np.clip(1 - d, 0, 1) ** 1.6
        arr = np.zeros((H, W, 3), np.float32)
        arr[..., 0] = 6 + 120 * g
        arr[..., 1] = 3 + 8 * g
        arr[..., 2] = 5 + 14 * g
        im = Image.fromarray(arr.clip(0, 255).astype("uint8"), "RGB").convert("RGBA")
        _cache["f"] = im
    return _cache["f"].copy()


def _fade(t, dur, ent=0.3, sal=0.25):
    return A.clamp(t / ent) * A.clamp((dur - t) / sal)


def _titulo(im, t, arriba, grande, y=430, ini=0.0):
    """Palabra corta sans blanca + frase serif itálica grande con subrayado rojo; aparecen con fundido."""
    if arriba:
        a = A.clamp((t - ini) / 0.3)
        if a > 0:
            A.pegar_centro(im, A.con_alfa(_ajustar(_sans(arriba, 56), 940), a), W / 2, y)
    if grande:
        pal = grande.split()
        imgs = [_txt_serif(p, 104) for p in pal]
        esp = 2
        total = sum(i.width for i in imgs) + esp * (len(imgs) - 1)
        esc = min(1.0, 960 / total)
        x = W / 2 - total * esc / 2
        yy = y + 110
        for k, ii in enumerate(imgs):
            a = A.clamp((t - ini - 0.15 - k * 0.12) / 0.25)
            ii2 = A.escalar(ii, esc) if esc < 1 else ii
            if a > 0:
                im.alpha_composite(A.con_alfa(ii2, a), (int(x), int(yy - ii2.height / 2)))
            x += ii2.width + esp * esc
        u = A.ease_out(A.clamp((t - ini - 0.35) / 0.5))
        if u > 0:
            capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            x0 = W / 2 - total * esc / 2
            ImageDraw.Draw(capa).line((x0, yy + 62, x0 + total * esc * u, yy + 62), fill=ROJO + (255,), width=6)
            im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(1)))
            im.alpha_composite(capa)


def _circulo(d, cx, cy, r, color=(255, 255, 255, 150), w=3):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=w)


def _logo(ruta, alto, ancho):
    return A.logo_blanco(ruta, alto, ancho) if ruta else None


def _escena(dur, dib, sonido="pop", zoom=0.04):
    def cuadro(t):
        im = _fondo()
        dib(im, t)
        z = 1 + zoom * A.clamp(t / dur)
        if z > 1.001:
            im2 = im.resize((int(W * z), int(H * z)), Image.BILINEAR)
            ox, oy = (im2.width - W) // 2, (im2.height - H) // 2
            im = im2.crop((ox, oy, ox + W, oy + H))
        return A.con_alfa(im, _fade(t, dur))

    return A.Grafico(dur, (0, 0, W, H), cuadro, sonido)


def _cifra(texto, tam=150, color=BLANCO):
    return _glow(_sans(texto, tam, color), 14, 1.6)


def _contar(desde, hasta, k):
    return desde + (hasta - desde) * A.ease_out(A.clamp(k))


def _fmt(v, formato):
    s = formato.format(v=v)
    # 1,234.5 -> 1.234,5 (estilo español)
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def _onda(im, t, y, n, activo, etiquetas=(), amp=34, color=ROJO):
    """Onda roja de neón que cruza la pantalla con n nodos; los nodos hasta 'activo' se iluminan."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    pts = [(x, y + amp * math.sin(x / 70 + t * 2.4)) for x in range(-20, W + 20, 6)]
    d.line(pts, fill=color + (255,), width=7)
    im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(3)))
    im.alpha_composite(capa)
    d = ImageDraw.Draw(im)
    margen = 110
    for i in range(n):
        x = margen + (W - 2 * margen) * (i / max(1, n - 1))
        yy = y + amp * math.sin(x / 70 + t * 2.4)
        on = i < activo
        r = 30
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(20, 8, 10, 255), outline=(ROJO if on else (90, 90, 100)) + (255,), width=5)
        if on:
            halo = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
            ImageDraw.Draw(halo).ellipse((60, 60, 140, 140), fill=ROJO + (150,))
            im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(16)), (int(x - 100), int(yy - 100)))
            A.pegar_centro(im, _sans(str(i + 1), 34), x, yy)
        if i < len(etiquetas) and etiquetas[i]:
            A.pegar_centro(im, A.con_alfa(_sans(etiquetas[i], 30, BLANCO if on else GRIS, False), 1 if on else 0.5), x, yy - 70)


def _tarjeta(w, h, borde=ROJO, alfa=235):
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 30, 30 + w, 30 + h), 30, outline=borde + (200,), width=5)
    g = im.filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    ImageDraw.Draw(out).rounded_rectangle((30, 30, 30 + w, 30 + h), 30, fill=(16, 10, 14, alfa), outline=borde + (230,), width=3)
    return out


# --------------------------------------------------------------------------- escenas
def g_ref_cifra(dur, ruta_logo=None, arriba="", grande="", desde=0, hasta=1000, formato="+{v:,.0f}", sufijo="MILLONES",
                sub="", color=BLANCO):
    """Título + logo en círculo + cifra grande que sube con contador."""
    lg = _logo(ruta_logo, 120, 300)

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        d = ImageDraw.Draw(im)
        if lg:
            k = A.ease_out_back(A.clamp((t - 0.1) / 0.4))
            _circulo(d, W / 2, 850, 150)
            A.pegar_centro(im, A.escalar(_glow(lg, 10, 1.2), max(0.05, k)), W / 2, 850)
        kc = A.clamp((t - 0.35) / max(0.6, dur * 0.55))
        if t > 0.35:
            num = _fmt(_contar(desde, hasta, kc), formato)
            A.pegar_centro(im, _ajustar(_cifra(num, 170, color), 980), W / 2, 1130)
            if sufijo:
                A.pegar_centro(im, _ajustar(_sans(sufijo, 56, ROJO), 900), W / 2, 1260)
        if sub:
            a = A.clamp((t - 0.8) / 0.3)
            if a > 0:
                A.pegar_centro(im, A.con_alfa(_ajustar(_sans(sub, 42, GRIS, False), 900), a), W / 2, 1590)

    return _escena(dur, dib, "pop")


def g_ref_vs(dur, ruta_a=None, ruta_b=None, a_txt="ANTHROPIC", b_txt="OPENAI", a_val=1.4, b_val=1.25, unidad="billones",
             arriba="Ahora vale", grande="más que OpenAI"):
    """Dos barras que crecen con su cifra: la ganadora en rojo neón."""
    la, lb = _logo(ruta_a, 90, 220), _logo(ruta_b, 90, 220)

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        d = ImageDraw.Draw(im)
        base = 1220
        mx = max(a_val, b_val)
        for i, (lg, nom, val, col) in enumerate(((la, a_txt, a_val, ROJO), (lb, b_txt, b_val, (120, 120, 135)))):
            cx = 330 + i * 420
            k = A.ease_out(A.clamp((t - 0.4 - i * 0.2) / 0.9))
            h = 480 * (val / mx) * k
            capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(capa).rounded_rectangle((cx - 110, base - h, cx + 110, base), 22, fill=col + (255,))
            if i == 0:
                im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(18)))
            im.alpha_composite(capa)
            if k > 0.05:
                A.pegar_centro(im, _cifra(_fmt(val * k, "{v:.2f}").rstrip("0").rstrip(","), 84), cx, base - h - 70)
            if lg:
                A.pegar_centro(im, A.escalar(lg, 0.6), cx, base + 50)
            A.pegar_centro(im, _sans(nom, 30, BLANCO if i == 0 else GRIS), cx, base + 115)
        a = A.clamp((t - 1.2) / 0.3)
        if a > 0:
            A.pegar_centro(im, A.con_alfa(_sans(unidad.upper() + " DE DÓLARES", 40, GRIS, False), a), W / 2, 1580)

    return _escena(dur, dib, "pop", zoom=0.02)


def g_ref_onda(dur, n=7, arriba="Sus", grande="7 fundadores", cifra="250 M", sub="cada uno", etiquetas=()):
    """Onda neón con n nodos que se encienden uno a uno; abajo la cifra."""

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        act = int(A.clamp((t - 0.3) / max(0.5, dur * 0.55)) * n + 0.999) if t > 0.3 else 0
        _onda(im, t, 900, n, act, etiquetas)
        a = A.ease_out_back(A.clamp((t - dur * 0.55) / 0.4))
        if a > 0:
            A.pegar_centro(im, A.escalar(_ajustar(_cifra(cifra, 170), 980), a), W / 2, 1170)
            A.pegar_centro(im, A.con_alfa(_sans(sub, 50, ROJO), A.clamp(a)), W / 2, 1310)

    return _escena(dur, dib, "pop", zoom=0.02)


def g_ref_perdida(dur, ruta_logo=None, arriba="Facturó", grande="en solo 3 meses", antes="+10.000 M", despues="-11.000 M",
                  sub="perdió casi el doble"):
    """Cifra verde que gira y se vuelve roja (pérdida)."""
    lg = _logo(ruta_logo, 100, 260)

    def dib(im, t):
        cambio = dur * 0.48
        if t < cambio:
            _titulo(im, t, arriba, grande)
        else:
            _titulo(im, t - cambio, "Y aun así", "perdió casi", ini=0)
        d = ImageDraw.Draw(im)
        if lg:
            _circulo(d, W / 2, 790, 120)
            A.pegar_centro(im, lg, W / 2, 790)
        k = (t - cambio) / 0.3
        if k < 0:
            img = _cifra(antes, 170, VERDE)
            sy = 1
        else:
            img = _cifra(despues, 170, ROJO)
            sy = A.clamp(k)
        if t < cambio - 0.3 + 0.3 and k > -1 and k < 0:
            sy = A.clamp(-k)
        e = A.ease_out_back(A.clamp((t - 0.2) / 0.4))
        img = _ajustar(img, 980)
        img = img.resize((max(1, int(img.width * e)), max(1, int(img.height * max(0.05, sy) * e))), Image.BILINEAR)
        A.pegar_centro(im, img, W / 2, 1090)
        flecha = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        dd = ImageDraw.Draw(flecha)
        if k >= 0:
            dd.polygon([(60, 115), (10, 45), (40, 45), (40, 5), (80, 5), (80, 45), (110, 45)], fill=ROJO + (255,))
        else:
            dd.polygon([(60, 5), (10, 75), (40, 75), (40, 115), (80, 115), (80, 75), (110, 75)], fill=VERDE + (255,))
        A.pegar_centro(im, _glow(flecha, 8, 1.4), W / 2, 1265)
        if k > 1 and sub:
            A.pegar_centro(im, A.con_alfa(_sans(sub, 46, GRIS, False), A.clamp(k - 1)), W / 2, 1590)

    return _escena(dur, dib, "alerta", zoom=0.03)


def _avion(w=300):
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = w / 300
    p = lambda pts: [(x * s, y * s) for x, y in pts]
    d.polygon(p([(150, 20), (165, 40), (165, 120), (285, 190), (285, 215), (165, 175), (165, 245), (200, 270), (200, 285),
                 (150, 272), (100, 285), (100, 270), (135, 245), (135, 175), (15, 215), (15, 190), (135, 120), (135, 40)]),
              fill=BLANCO + (255,))
    return im.rotate(-90, resample=Image.BICUBIC)


def g_ref_despidos(dur, arriba="Qantas despide a", grande="850 empleados", total=850, de="AUSTRALIA", a="INDIA",
                   sub="de oficina"):
    """Cuadrícula de 850 que se va apagando (empleos) + avión que va de Australia a India."""
    av = _glow(_avion(170), 8, 1.3)
    cols = 50  # 50 x 17 = 850 cuadritos

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        d = ImageDraw.Draw(im)
        k = A.clamp((t - 0.3) / max(0.6, dur * 0.5))
        lado, gap = 15, 5
        x0 = (W - (cols * (lado + gap) - gap)) / 2
        y0 = 870
        enc = int(total * k)
        for i in range(total):
            c, f = i % cols, i // cols
            x, y = x0 + c * (lado + gap), y0 + f * (lado + gap)
            col = ROJO + (255,) if i < enc else (70, 70, 80, 255)
            d.rectangle((x, y, x + lado, y + lado), fill=col)
        num = _fmt(int(total * k), "{v:,.0f}")
        A.pegar_centro(im, _cifra(num, 120, ROJO), W / 2, 700)
        A.pegar_centro(im, _sans("EMPLEOS " + sub.upper(), 36, GRIS, False), W / 2, 800)
        kr = A.clamp((t - dur * 0.45) / (dur * 0.45))
        if kr > 0:
            ya = 1270
            d.line((180, ya, 900, ya), fill=(255, 255, 255, 90), width=3)
            A.pegar_centro(im, _sans(de, 32), 180, ya + 45)
            A.pegar_centro(im, _sans(a, 32, ROJO), 900, ya + 45)
            _circulo(d, 180, ya, 12, BLANCO + (255,), 5)
            _circulo(d, 900, ya, 12, ROJO + (255,), 5)
            A.pegar_centro(im, A.escalar(av, 0.5), 180 + 720 * A.ease_in_out(kr), ya - 10)

    return _escena(dur, dib, "alerta", zoom=0.02)


def _candado(w=260, abierto=1.0):
    oy = w * 0.35
    im = Image.new("RGBA", (w, int(w * 1.3 + oy)), (0, 0, 0, 0))
    gr = int(w * 0.09)
    arco = Image.new("RGBA", im.size, (0, 0, 0, 0))
    da = ImageDraw.Draw(arco)
    x0, x1 = w * 0.24, w * 0.76
    top = oy + w * 0.12
    da.arc((x0, top, x1, top + (x1 - x0)), 180, 360, fill=BLANCO + (255,), width=gr)
    ym = top + (x1 - x0) / 2
    da.line((x0 + gr / 2, ym - 2, x0 + gr / 2, oy + w * 0.72), fill=BLANCO + (255,), width=gr)
    da.line((x1 - gr / 2, ym - 2, x1 - gr / 2, oy + w * 0.72), fill=BLANCO + (255,), width=gr)
    arco = arco.rotate(18 * abierto, resample=Image.BICUBIC, center=(x0 + gr / 2, oy + w * 0.7),
                       translate=(0, -w * 0.2 * abierto))
    im.alpha_composite(arco)
    d = ImageDraw.Draw(im)
    bw = w * 0.86
    bx, by = (w - bw) / 2, oy + w * 0.62
    d.rounded_rectangle((bx, by, bx + bw, by + w * 0.62), int(w * 0.08), fill=ROJO + (255,))
    d.ellipse((w / 2 - w * 0.07, by + w * 0.18, w / 2 + w * 0.07, by + w * 0.32), fill=(20, 0, 0, 255))
    d.rectangle((w / 2 - w * 0.03, by + w * 0.28, w / 2 + w * 0.03, by + w * 0.46), fill=(20, 0, 0, 255))
    return im


def g_ref_candado(dur, arriba="Grok dejó", grande="35.000 apps abiertas", hasta=35000, sello="DATOS PRIVADOS",
                  sub="sin contraseña"):
    """Candado que se abre, contador de apps y tarjetas de apps que se iluminan en rojo; sello al final."""

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        ab = A.ease_out_back(A.clamp((t - 0.3) / 0.5))
        A.pegar_centro(im, _glow(_candado(210, ab), 14, 1.4), W / 2, 760)
        k = A.clamp((t - 0.4) / max(0.6, dur * 0.5))
        A.pegar_centro(im, _cifra(_fmt(hasta * A.ease_out(k), "{v:,.0f}"), 150), W / 2, 1050)
        A.pegar_centro(im, _sans("APPS · " + sub.upper(), 40, GRIS, False), W / 2, 1150)
        d = ImageDraw.Draw(im)
        n = 6
        for i in range(n):
            c, f = i % 6, i // 6
            x, y = 150 + c * 140, 1215 + f * 130
            on = i < int(n * k)
            d.rounded_rectangle((x, y, x + 100, y + 100), 22, fill=(30, 14, 18, 255), outline=(ROJO if on else (80, 80, 90)) + (255,), width=4)
            if on:
                d.line((x + 25, y + 40, x + 75, y + 40), fill=ROJO + (255,), width=6)
                d.line((x + 25, y + 62, x + 60, y + 62), fill=(200, 200, 210, 255), width=6)
        ks = A.clamp((t - dur * 0.62) / 0.2)
        if ks > 0:
            st = _sans(sello, 70)
            sl = Image.new("RGBA", (st.width + 80, st.height + 50), (0, 0, 0, 0))
            ImageDraw.Draw(sl).rounded_rectangle((0, 0, sl.width - 1, sl.height - 1), 16, fill=ROJO + (255,))
            A.pegar_centro(sl, st, sl.width / 2, sl.height / 2)
            sl = sl.rotate(-6, resample=Image.BICUBIC, expand=True)
            A.pegar_centro(im, A.con_alfa(A.escalar(sl, 2 - A.ease_out(ks)), ks), W / 2, 1600)

    return _escena(dur, dib, "alerta", zoom=0.02)


def _robot(w=300):
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line((w / 2, w * 0.08, w / 2, w * 0.22), fill=BLANCO + (255,), width=8)
    d.ellipse((w / 2 - 16, w * 0.02, w / 2 + 16, w * 0.02 + 32), fill=ROJO + (255,))
    d.rounded_rectangle((w * 0.15, w * 0.22, w * 0.85, w * 0.78), int(w * 0.12), outline=BLANCO + (255,), width=9)
    for cx in (w * 0.37, w * 0.63):
        d.ellipse((cx - 24, w * 0.42 - 24, cx + 24, w * 0.42 + 24), fill=ROJO + (255,))
    d.line((w * 0.35, w * 0.62, w * 0.65, w * 0.62), fill=BLANCO + (255,), width=9)
    return im


def _escudo(w=520):
    h = int(w * 1.15)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(w / 2, 10), (w - 20, h * 0.16), (w - 40, h * 0.55), (w / 2, h - 12), (40, h * 0.55), (20, h * 0.16)]
    d.polygon(pts, fill=(40, 10, 16, 230), outline=ROJO + (255,))
    d.line(pts + [pts[0]], fill=ROJO + (255,), width=10)
    return im


def g_ref_seguro(dur, arriba="Ya existe un", grande="seguro para tu IA", sello="SI LA IA SE EQUIVOCA", sub="Cowbell · Estados Unidos"):
    """Escudo rojo que cubre a un robot; check al final."""
    esc = _glow(_escudo(480), 18, 1.5)
    rob = _robot(260)

    def dib(im, t):
        _titulo(im, t, arriba, grande)
        k = A.ease_out_back(A.clamp((t - 0.25) / 0.5))
        A.pegar_centro(im, A.escalar(esc, max(0.05, k)), W / 2, 960)
        A.pegar_centro(im, rob, W / 2, 940 + 8 * math.sin(t * 3))
        kc = A.clamp((t - dur * 0.5) / 0.35)
        if kc > 0:
            c = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
            dd = ImageDraw.Draw(c)
            dd.ellipse((0, 0, 159, 159), fill=VERDE + (255,))
            dd.line([(40, 85), (70, 115), (122, 50)], fill=BLANCO + (255,), width=16, joint="curve")
            A.pegar_centro(im, A.escalar(c, A.ease_out_back(kc)), W / 2 + 190, 1180)
            A.pegar_centro(im, A.con_alfa(_ajustar(_sans(sello, 54, BLANCO), 960), kc), W / 2, 1590)
            A.pegar_centro(im, A.con_alfa(_sans(sub, 40, GRIS, False), kc), W / 2, 1665)

    return _escena(dur, dib, "pop", zoom=0.03)


def g_ref_titulo(dur, arriba="", grande="", sub="", ch=None):
    """Solo título del referente, grande y centrado (para el gancho y el cierre)."""

    def dib(im, t):
        _titulo(im, t, arriba, grande, y=700)
        _onda(im, t, 1400, 5, int(A.clamp(t / max(0.4, dur * 0.7)) * 5 + 0.999), ())
        if sub:
            a = A.clamp((t - 0.6) / 0.3)
            if a > 0:
                A.pegar_centro(im, A.con_alfa(_ajustar(_sans(sub, 48, GRIS, False), 940), a), W / 2, 1590)

    return _escena(dur, dib, "golpe", zoom=0.03)


def construir(g, dur, assets):
    t = g["tipo"]
    lg = lambda k="logo": f"{assets}/logo_{g[k]}.png" if g.get(k) else None
    if t == "ref_cifra":
        return g_ref_cifra(dur, lg(), g.get("arriba", ""), g.get("grande", ""), g.get("desde", 0), g.get("hasta", 1000),
                           g.get("formato", "+{v:,.0f}"), g.get("sufijo", "MILLONES"), g.get("sub", ""),
                           tuple(g.get("color", BLANCO)))
    if t == "ref_vs":
        return g_ref_vs(dur, lg("logo"), lg("logo_b"), g.get("a_txt", "ANTHROPIC"), g.get("b_txt", "OPENAI"),
                        g.get("a_val", 1.4), g.get("b_val", 1.25), g.get("unidad", "billones"),
                        g.get("arriba", "Ahora vale"), g.get("grande", "más que OpenAI"))
    if t == "ref_onda":
        return g_ref_onda(dur, g.get("n", 7), g.get("arriba", "Sus"), g.get("grande", "7 fundadores"),
                          g.get("cifra", "250 M"), g.get("sub", "cada uno"), tuple(g.get("etiquetas", ())))
    if t == "ref_perdida":
        return g_ref_perdida(dur, lg(), g.get("arriba", "Facturó"), g.get("grande", "en solo 3 meses"),
                             g.get("antes", "+10.000 M"), g.get("despues", "-11.000 M"), g.get("sub", ""))
    if t == "ref_despidos":
        return g_ref_despidos(dur, g.get("arriba", "Qantas despide a"), g.get("grande", "850 empleados"))
    if t == "ref_candado":
        return g_ref_candado(dur, g.get("arriba", "Grok dejó"), g.get("grande", "35.000 apps abiertas"),
                             g.get("hasta", 35000), g.get("sello", "DATOS PRIVADOS"), g.get("sub", "sin contraseña"))
    if t == "ref_seguro":
        return g_ref_seguro(dur, g.get("arriba", "Ya existe un"), g.get("grande", "seguro para tu IA"),
                            g.get("sello", "SI LA IA SE EQUIVOCA"), g.get("sub", "Cowbell · Estados Unidos"))
    if t == "ref_titulo":
        return g_ref_titulo(dur, g.get("arriba", ""), g.get("grande", ""), g.get("sub", ""))
    return None
