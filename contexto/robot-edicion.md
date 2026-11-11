# Robot de edición (11 nov 2026) — punto 3 del plan

## Cómo funciona
1. **Santi** sube el crudo a Edición de videos › 1. Videos en frío, con el código adelante (`v8.mov`, `E1.mov`) o con la
   fecha (`10 nov` = noticias que salen el 11 nov).
2. **Robot.gs** (Apps Script, cada 15 min, gratis): ve el crudo nuevo → fila de la pieza en Estado `Grabado` → fila nueva en
   **COLA POR EDITAR** con Estado `Por editar` y el link del crudo. Instalar una vez: `instalarRobot()`.
3. **Tarea programada de Claude** "🎬 Robot de edición" (4 veces al día, Bogotá: 8:47, 14:47, 20:47, 23:47; sesión nueva
   cada vez, aviso al celular). Lee la COLA: si no hay nada `Por editar`, termina sin gastar más. Si hay: edita la pieza
   más cercana a publicarse, la sube a 2. Videos terminados, deja la fila en `Listo` (nunca `Publicar`), COLA → `Revisión`,
   y termina con el aviso **"🎬 <código> listo, míralo"** + link.
4. **Santi** revisa → correcciones juntas → "dale" en el chat 📁 Edición de videos → Claude pone `Publicar`.

## Texto exacto de la tarea programada (para corregirla o recrearla)
Ver `PROMPT` abajo; trigger id en la bitácora.

PROMPT:
Eres el robot de edición de videos de Santiago (ContentIA). Repo santiagopineda3030/santiago, rama claude/santiago-ia-landing-4q4ef1 (ya clonado; haz git pull).
1. Lee contexto/estado-actual.md, areas/5-edicion-videos/CLAUDE.md, areas/5-edicion-videos/.claude/skills/editar-video/SKILL.md y editor-noticias/README.md (sobre todo "Reglas de Santi", "Estilo cyberpunk" y "Trabas").
2. Lee la hoja 1lvs82vX8Pj3rHmVZyUj9cUh6dOm5srjbVDwzvWUyku4, pestaña "COLA POR EDITAR" (encabezados en la fila 3, datos desde la 4). Si ninguna fila tiene Estado "Por editar", termina YA con una sola línea "Nada por editar" (no leas nada más).
3. Toma UNA pieza "Por editar": la que se publica primero (busca su código en la columna # de la pestaña Noviembre). Pon su Estado en la COLA en "Editando".
4. Edítala con el flujo de editor-noticias (proxy SDR si es iPhone HDR, trozos_vad.py, EDL con la última toma buena de cada frase del guion de la fila, revisión LITERAL de trabas con initial_prompt de muletillas —ninguna frase repetida ni re-arranque—, voz seguida --aire 0.05 --unir 0.3, encuadre a la cara, estilo cyber, animaciones según el guion, partes en blanco y negro, música). Para bajar el crudo: compártelo con enlace (Drive share_file) y bájalo con curl. Verifica el video final con la transcripción literal y una hoja de cuadros antes de subirlo.
5. Súbelo con editor-noticias/subir-drive/subir_drive.sh a "NOVIEMBRE 2026". En la fila: Link Video Editado, Archivo, Descripción (del guion), Título YouTube, Estado "Editado", Publicación "Listo". NUNCA pongas "Publicar". En la COLA: Estado "Revisión" y el link en "Editado (link)".
6. Línea en contexto/bitacora.md, commit y push.
7. Tu último mensaje debe empezar con "🎬 <código> listo, míralo" + link del video en Drive + 3 líneas de qué hiciste + "Recuerda volver el crudo a Restringido". Santi lo revisa en el chat 📁 Edición de videos.
Español, frases cortas. Si algo falla (no hay guion, el crudo no baja), pon la COLA en "Corrección" con la nota y avísalo en el último mensaje.

## Estado (11 nov)
- Robot.gs en el repo (`google-apps-script/plan-contenido/Robot.gs`). ✅ Instalado por Santi 11 nov 12:09 (instalarRobot OK, 0 crudos en la carpeta).
- Tarea programada `trig_01Hf9JW6Q1ToNban24k5F9nw` "🎬 Robot de edición" creada **en pausa**: se creó sin conectores ni repo
  (la herramienta no deja pasarlos). **Falta: Santi la abre en claude.ai › Rutinas/Tareas programadas, le agrega el repo
  santiagopineda3030/santiago y los conectores Google Drive y Google Sheets, y la activa.**
