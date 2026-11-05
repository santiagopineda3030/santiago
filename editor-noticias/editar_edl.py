#!/usr/bin/env python3
"""
Renderiza el video a partir de una lista de cortes elegida a mano (edl-*.json).

Cada corte indica clip, segundos desde/hasta y el subtítulo corregido. Los tiempos
de cada palabra salen de la transcripción por trozos (carpeta --trozos); si el
subtítulo corregido no coincide palabra por palabra, se reparte en el tiempo.

Uso:
    python3 editar_edl.py --videos crudos --edl edl-dia-1.json --trozos salida/trozos
"""
import argparse
import json
import re
import shutil
from pathlib import Path

import editar
from editar import ffmpeg, normalizar, probar

PRE, POST = 0.10, 0.14      # aire antes y después de cada frase (s)
PIEZA_MAX = 4.5             # cada pieza más larga se parte en dos (zoom distinto)
COLA_CTA = 2.0              # segundos extra al final con la pregunta del CTA


def palabras_de(trozos, ini, fin):
    return [w for t in trozos for w in t["palabras"] if w["s"] >= ini - 0.25 and w["e"] <= fin + 0.25]


def alinear(texto, ws, ini, fin):
    """Asigna tiempos a las palabras del subtítulo corregido."""
    tokens = texto.split()
    if len(ws) == len(tokens):
        return [{"w": t, "s": w["s"], "e": w["e"]} for t, w in zip(tokens, ws)]
    a = ws[0]["s"] if ws else ini
    b = ws[-1]["e"] if ws else fin
    total = sum(len(t) + 1 for t in tokens)
    out, t = [], a
    for tok in tokens:
        d = (b - a) * (len(tok) + 1) / total
        out.append({"w": tok, "s": round(t, 3), "e": round(t + d * 0.92, 3)})
        t += d
    return out


def partir(corte, palabras):
    """Parte un corte largo en piezas de ≤ PIEZA_MAX s, en el hueco más grande cerca del medio."""
    ini, fin = corte["ini"], corte["fin"]
    if fin - ini <= PIEZA_MAX or len(palabras) < 4:
        return [(ini, fin, palabras)]
    mitad = (ini + fin) / 2
    i = min(range(1, len(palabras)),
            key=lambda k: abs(palabras[k]["s"] - mitad) - 3 * (palabras[k]["s"] - palabras[k - 1]["e"]))
    corte_t = (palabras[i - 1]["e"] + palabras[i]["s"]) / 2
    return (partir({"ini": ini, "fin": corte_t}, palabras[:i]) +
            partir({"ini": corte_t, "fin": fin}, palabras[i:]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--videos", required=True)
    ap.add_argument("--edl", required=True)
    ap.add_argument("--trozos", required=True, help="carpeta con la transcripción por trozos")
    ap.add_argument("--salida", default="salida")
    ap.add_argument("--nombre", default="v1 1.0 noticias-dia-1.mp4")
    ap.add_argument("--centro-x", type=float, default=0.53)
    a = ap.parse_args()
    editar.CENTRO_X = a.centro_x

    edl = json.loads(Path(a.edl).read_text(encoding="utf-8"))
    clips = sorted(p for p in Path(a.videos).iterdir() if p.suffix.lower() == ".mp4")
    por_codigo = {re.search(r"_(\d{4})_", c.name).group(1): i for i, c in enumerate(clips)}
    infos = [probar(c) for c in clips]
    trozos = {i: json.loads((Path(a.trozos) / f"{c.stem}.json").read_text()) for i, c in enumerate(clips)}
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    zooms = [1.0, 1.12, 1.05, 1.16]
    plan, secciones = [], []
    for s in edl["secciones"]:
        sec = {"titulo": s["titulo"], "tipo": s["tipo"], "etiqueta": s.get("etiqueta", ""), "texto": ""}
        secciones.append(sec)
        for k, c in enumerate(s["cortes"]):
            ci = por_codigo[c["clip"]]
            ini = max(0.0, c["desde"] - PRE)
            fin = min(infos[ci]["dur"], c["hasta"] + POST)
            ws = alinear(c["texto"], palabras_de(trozos[ci], c["desde"], c["hasta"]), c["desde"], c["hasta"])
            for j, (pi, pf, pw) in enumerate(partir({"ini": ini, "fin": fin}, ws)):
                plan.append({"seccion": s["titulo"], "clip": ci, "ini": round(pi, 3), "fin": round(pf, 3),
                             "zoom": 1.0 if (k == 0 and j == 0) else zooms[len(plan) % len(zooms)],
                             "palabras": pw})

    print(f"· {len(plan)} piezas · {sum(p['fin'] - p['ini'] for p in plan):.1f} s estimados", flush=True)
    tmp = salida / "_tmp"
    base = editar.render(plan, clips, infos, tmp)

    # Cola final: congelar el último cuadro unos segundos para leer la pregunta del CTA
    con_cola = tmp / "base_cola.mov"
    ffmpeg("-i", str(base), "-vf", f"tpad=stop_mode=clone:stop_duration={COLA_CTA}",
           "-af", f"apad=pad_dur={COLA_CTA}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-c:a", "pcm_s16le", str(con_cola))

    t = 0.0
    for pz in plan:
        pz["palabras_salida"] = [dict(w, s=t + max(0, w["s"] - pz["ini"]), e=t + min(pz["fin"], w["e"]) - pz["ini"])
                                 for w in pz["palabras"]]
        pz["salida_ini"], t = t, t + pz["dur_real"]
        pz["salida_fin"] = t
    for sec in secciones:
        pzs = [p for p in plan if p["seccion"] == sec["titulo"]]
        sec["salida_ini"], sec["salida_fin"] = pzs[0]["salida_ini"], pzs[-1]["salida_fin"]
    # El CTA no se grabó: va como texto en pantalla los últimos segundos
    secciones.append({"titulo": "CTA", "tipo": "cta", "etiqueta": "", "texto": edl["cta"],
                      "salida_ini": max(0, t - 3.0), "salida_fin": t + COLA_CTA - 0.6})

    ass = salida / "subtitulos.ass"
    editar.generar_ass(plan, secciones, edl.get("gancho_texto", ""), ass)
    print("· Exportando…", flush=True)
    dur, mb = editar.exportar(con_cola, ass, salida / a.nombre)
    shutil.rmtree(tmp, ignore_errors=True)

    lin = [f"# {a.nombre}", "", f"- Duración: **{dur:.1f} s** · Tamaño: **{mb:.1f} MB** · {len(plan)} cortes", "",
           "| Parte | Inicio en el video | Clips y segundos usados |", "|---|---|---|"]
    for sec, s in zip(secciones, edl["secciones"]):
        usados = ", ".join(f"{c['clip']} ({c['desde']:.1f}–{c['hasta']:.1f}s)" for c in s["cortes"])
        lin.append(f"| {sec['titulo']} | {sec['salida_ini']:.1f}s | {usados} |")
    lin.append(f"| CTA (texto en pantalla, no estaba grabado) | {secciones[-1]['salida_ini']:.1f}s | — |")
    (salida / "resumen.md").write_text("\n".join(lin) + "\n", encoding="utf-8")
    print("\n".join(lin))


if __name__ == "__main__":
    main()
