---
name: referentes-edicion
description: Estilo de edición de ContentIA por tipo de video, sacado de los referentes de Santi. Úsalo SIEMPRE antes de editar cualquier video (noticias v, explicativo E, YouTube largo Y, lead L, VSL S, clip de cascada C), sea el robot de edición o un chat de edición. También cuando Santi manda un video nuevo de referente para guardarlo.
---

# Referentes de edición · ContentIA

Los referentes son videos que a Santi le gustan. Se copia el **estilo** (ritmo, subtítulos, animaciones, color), nunca el contenido.

## Antes de editar
1. Saca el tipo por la letra del código: `v` Noticias · `E` Explicativo · `Y` YouTube largo · `L` Lead · `S` VSL · `C` Clip cascada
   (o por la columna Tipo de la fila).
2. Lee la sección de ese tipo en `contexto/referentes-edicion.md`.
3. **Mira la hoja de cuadros** del referente (`referentes/<tipo>-refN-cuadros.jpg`) con la herramienta de leer imágenes. Si hace falta más detalle, saca cuadros del mp4 (`referentes/<tipo>-refN.mp4`) con ffmpeg.
4. Edita siguiendo, en este orden: (a) la sección **Edición** del guion de la fila, (b) lo que Santi diga, (c) el referente del tipo, (d) `editor-noticias/README.md`. Si chocan, gana el guion o Santi.
5. Al revisar el video final, compara tu hoja de cuadros con la del referente: subtítulos, ritmo y gráficos deben parecerse.

Siempre: colores de ContentIA (cian; en noticias, rojo), sin mostrar herramientas ni configuración por dentro, sin fotos de famosos.
VSL (S): no hay referente propio todavía → usar el de YouTube largo para el formato 16:9 y el de Lead para la versión vertical corta.

## Cuando Santi manda un referente nuevo
1. `ffprobe` (duración, tamaño) + hoja de cuadros 20 cuadros (`fps=20/DUR,scale=216:-1,tile=5x4`) y mírala.
2. Copia el video a `referentes/<tipo>-refN.mp4` y la hoja a `referentes/<tipo>-refN-cuadros.jpg`.
3. Escribe sus rasgos en `contexto/referentes-edicion.md` (plano, ritmo, subtítulos, gráficos, transiciones, cómo aplicarlo a ContentIA).
4. Actualiza el doc de Drive "Referentes de edición · ContentIA" (id en `contexto/drive.md`), bitácora, commit y push.
