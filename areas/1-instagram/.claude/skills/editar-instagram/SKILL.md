---
name: editar-instagram
description: Edita un reel de Instagram de ContentIA (Noticias IA o video de leads, 9:16) desde el crudo y el guion terminado, con la Guía de edición, hasta dejarlo en Revisión. Úsalo cuando Santi dice "trabajemos el v2", "edita el video de hoy", "haz la corrección del v2" o en cualquier chat de areas/1-instagram.
---

# Editar un reel de Instagram

Español, pasos cortos. Santi dirige y revisa; Claude edita. Espera su OK donde dice **[OK]**.

1. **Leer** la fila (pestaña del mes + COLA), el guion terminado y la Guía de edición completa. Estado COLA = **Editando**.
2. **Transcribir** cada trozo del crudo: `python3 editor-noticias/trozos.py …` (detecta tomas repetidas).
3. **Tomas [OK]:** en `editor-noticias/edl-<código>.json`, la **última toma buena** de cada frase del guion, en su orden.
   Subtítulos corregidos (del guion, no de Whisper). Mostrarle a Santi la lista frase por frase.
4. **Render:** `python3 editor-noticias/editar_v2.py …` (cortes por detector de voz, audio sincronizado, animaciones, títulos
   por noticia, palabras clave en rojo).
5. **Auditoría:** gancho en los primeros 3 s · ningún corte se come palabras (alargar el borde si la voz sigue) · sin silencios
   (VAD) · subtítulos 2–4 palabras sin errores · zona segura (x 120–960, y 250–1500) · voz −14 LUFS · 45–75 s · H.264 ≤ 30 MB ·
   nada de herramientas en pantalla · CTA del guion.
6. **Entregar [OK]:** subir con el buzón a Instagram › `4. Contenido editado`, link en la COLA, Estado **Revisión**.
   Escribir la descripción (3–5 líneas, primera = gancho, emoji solo al cierre, 5 hashtags) y poner Publicación = `Listo`.

**Corrección:** versión nueva (1.1, 1.2…; la anterior se queda), "Hecho: …" en la columna Corrección, vuelve a Revisión.
Si la corrección es una regla, va a "Ajustes de Santi" de la Guía de edición (Drive + copia del repo).
