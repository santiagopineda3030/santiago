---
name: editar-video
description: Edita los videos que Santi subió a "Edición de videos › 1. Videos en frío", los revisa con él, los sube a "2. Videos terminados" y los programa en la hoja según el calendario, en las redes que Santi diga. Úsalo cuando Santi dice "ya subí los videos a videos en frío", "edítalo", "prográmalo" o en el chat 📁 Edición de videos.
---

# Editar y programar un video (en frío → terminado → programado)

Español, frases cortas (Santi trabaja desde el PC). Espera su OK donde dice **[OK]**.
Un solo video sirve para **Instagram, TikTok y YouTube Shorts**. IDs en `areas/5-edicion-videos/CLAUDE.md`.

1. **Buscar:** listar `1. Videos en frío` (archivos nuevos). Con el código (v<N>) o la fecha, encontrar la fila en la hoja
   del plan (pestaña del mes) y el guion en Guiones › Instagram › `3. Guiones terminados`. Si no está claro qué video es
   cuál, preguntarle. COLA POR EDITAR: crear/actualizar la fila, Estado **Editando**.
2. **Editar:** con `editor-noticias/` (README y flujo del `CLAUDE.md` de la raíz): `trozos.py` → `edl-<código>.json`
   (última toma buena, subtítulos del guion) → `editar_v2.py`. Seguir la Guía de edición (1080×1920, 45–75 s,
   subtítulos 2–4 palabras con clave en rojo, título por noticia, gancho en 3 s, −14 LUFS, H.264 ≤ 30 MB).
   Comando completo y opciones en `editor-noticias/README.md` › "Flujo actual". Lo que Santi pidió (5–7 nov) y es regla:
   cortes cuando mira a cámara (`--mirada`), muchas animaciones (gancho muy animado), zona segura, animación ANTES de la
   palabra (`--adelanto`), música original que SÍ se escuche (`lofi-energico`, −14 dB). Desde el 7 nov: tomas fieles al guion,
   luz original, estilo `ia`, y donde lee el guion o no sale en cuadro → animación a pantalla completa (README › Reglas de Santi).
3. **Auditar** antes de mostrar: igual que la skill `editar-instagram` paso 5.
4. **Revisar juntos [OK]:** mandarle el video (SendUserFile) y una lista corta de qué hiciste. Corregir lo que diga
   (versión nueva 1.1, 1.2…). Si una corrección es regla → "Ajustes de Santi" de la Guía (Drive + `drive-respaldo/recursos/`).
5. **Subir:** (si no hay `SUBIDA_URL`/`SUBIDA_CLAVE`, Santi lo sube a mano y avisa; tú buscas el archivo y comparas el tamaño) con el buzón (`editor-noticias/subir-drive/`, `SUBIDA_URL` y `SUBIDA_CLAVE`) a `2. Videos terminados`,
   nombre `v<N> <versión> <tema>.mp4`. Link en la fila de la hoja (Link Video Editado, Archivo) y en la COLA → **Entregado** + fecha.
6. **Programar:** la fecha y la hora salen de la hoja (columna Fecha; Noticias IA siempre a las **11:00**). Escribir la
   descripción (3–5 líneas, primera = gancho, emoji solo al cierre, 5 hashtags) y el Título YouTube. Redes:
   - Santi dice en qué redes. Las que NO van: poner `No` en la columna de esa red (`YouTube`, `TikTok`). Instagram siempre va.
   - Poner Publicación = `Publicar` **solo cuando Santi lo dijo en este chat** ("prográmalo en IG y TikTok"). Si no lo dijo,
     dejar `Listo` y preguntarle. Nunca `Publicar` si el video no está en `2. Videos terminados`.
   - El script publica solo a la hora y marca Calendar (`✅ Publicado · …`).
7. **Cerrar:** decirle en 3 líneas qué quedó programado, en qué redes y a qué hora. Línea en `contexto/bitacora.md` + commit + push.

## Referentes (11 nov)
Antes de editar: skill `referentes-edicion` (estilo por tipo, hojas de cuadros en `referentes/`).

## Cascada (clips C1, C2…) — 11 nov, reglas de Santi en `kit-cascada/reglas.json`
- **Cuándo:** al terminar de editar un video de origen (Y, E, v o L), mira en la pestaña del mes si hay filas Tipo
  "Clip cascada" que digan "Sale de <código>" (columna Estado o Elementos adicionales). Si las hay y están vacías, agrega una
  fila por clip en COLA POR EDITAR: Código C<n>, Categoría "Clip cascada", Crudo = link del video de origen YA EDITADO,
  Estado "Por editar". Si el origen no tiene filas C, no crees ninguna.
- **Editar un C:** baja el video de origen editado, transcríbelo completo (literal, con muletillas) y escoge los
  **3 momentos más fuertes** (explicación, resultado, consejo, opinión o historia), **15–20 s cada uno**, que se entiendan
  solos. Un C = un momento (C1 el más fuerte, C2, C3). Corta en frase completa, sin trabas ni silencios.
- **Diseño:** vertical 1080×1920, etiqueta **CONTENTIA** arriba, gancho fijo (≤ 9 palabras) arriba todo el clip,
  subtítulos de 3 palabras. Color de acento según el origen: **cian** YouTube largo, explicativo o clase; **rojo** noticias;
  **amarillo** lead. Estilo cyber del editor (`editar_v2.py --estilo cyber` con un EDL de un solo corte) o el editor del
  kit (`kit-cascada/editor/armar_reel.py`).
- **Sin CTA:** termina con la última idea; nada de "comenta" ni cierre. Nunca mostrar herramientas ni configuración.
- **Descripción:** el texto del clip + 5 hashtags de `reglas.json`, sin llamado a la acción.
- Nombre: `C<n> 1.0 <tema>.mp4`. Mismo final que siempre: sube, fila en `Listo` (nunca `Publicar`), COLA `Revisión`, aviso
  "🎬 C<n> listo, míralo".
