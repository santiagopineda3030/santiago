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
3. **Auditar** antes de mostrar: igual que la skill `editar-instagram` paso 5.
4. **Revisar juntos [OK]:** mandarle el video (SendUserFile) y una lista corta de qué hiciste. Corregir lo que diga
   (versión nueva 1.1, 1.2…). Si una corrección es regla → "Ajustes de Santi" de la Guía (Drive + `drive-respaldo/recursos/`).
5. **Subir:** con el buzón (`editor-noticias/subir-drive/`, `SUBIDA_URL` y `SUBIDA_CLAVE`) a `2. Videos terminados`,
   nombre `v<N> <versión> <tema>.mp4`. Link en la fila de la hoja (Link Video Editado, Archivo) y en la COLA → **Entregado** + fecha.
6. **Programar:** la fecha y la hora salen de la hoja (columna Fecha; Noticias IA siempre a las **11:00**). Escribir la
   descripción (3–5 líneas, primera = gancho, emoji solo al cierre, 5 hashtags) y el Título YouTube. Redes:
   - Santi dice en qué redes. Las que NO van: poner `No` en la columna de esa red (`YouTube`, `TikTok`). Instagram siempre va.
   - Poner Publicación = `Publicar` **solo cuando Santi lo dijo en este chat** ("prográmalo en IG y TikTok"). Si no lo dijo,
     dejar `Listo` y preguntarle. Nunca `Publicar` si el video no está en `2. Videos terminados`.
   - El script publica solo a la hora y marca Calendar (`✅ Publicado · …`).
7. **Cerrar:** decirle en 3 líneas qué quedó programado, en qué redes y a qué hora. Línea en `contexto/bitacora.md` + commit + push.
