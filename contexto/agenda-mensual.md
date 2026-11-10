# Kit de contenido mensual (acordado con Santi, 10 nov 2026) — arranca el 11 nov (Santi)

## Idea
Todo el contenido del mes en la hoja, con fecha, hora, tipo y guion. Santi solo graba y sube el crudo. El sistema edita,
avisa para revisar y, con el OK de Santi, publica solo a la hora de la fila. Se regenera cada mes.

## Flujo
1. **Inicio de mes:** Claude llena la pestaña **Agenda <Mes>** con todas las piezas (noticias diarias, videos de leads,
   explicativos, YouTube largo, anuncios, clips de cascada) y escribe sus guiones (link en la fila).
   Ej.: 12 nov → YouTube largo, ya queda programado para YouTube.
2. **Santi** graba y sube el crudo a Edición de videos › 1. Videos en frío, con el código adelante (`v7.mov`, `L2.mov`, `Y1.mov`).
3. **Robot de edición** (tarea programada cada pocas horas): ve el crudo nuevo, busca su fila por código, edita según
   guion y tipo (vertical 9:16 o YouTube largo 16:9), sube a 2. Videos terminados, pone estado `Listo para revisar`.
4. **Aviso a Santi:** "🎬 Video 7 listo, míralo" (notificación al celular + link). SIEMPRE con revisión (regla de Santi).
5. Santi revisa → correcciones juntas (máx. 2 versiones) → "dale" → Claude pone `Publicar`.
6. **Publicación** (Code.gs, leyendo la Agenda): sale a la fecha y hora de la fila en sus redes.

## Columnas de la Agenda
Código · Tipo · Redes · Fecha · Hora · Guion (link) · Estado · Crudo (link) · Video editado (link) · Descripción ·
Título YouTube · Links publicados (IG / YouTube / TikTok).
Estados: Por guion → Por grabar → Grabado → Editando → Listo para revisar → Publicar → Programado → Publicado.

## Pendiente
- Code.gs: leer la Agenda (hoy lee la pestaña Noviembre) y subir YouTube largo (no probado; ojo peso).
- Robot de edición: tarea programada + reglas por tipo de video.
- Encajar la cascada (kit-cascada/): sus clips caen como filas de la Agenda.

## Grabación por lotes (Santi, 10 nov)
- Santi graba todo el mes de una vez (ej. 40 crudos) y los sube a Videos en frío con el código adelante.
- Claude edita en orden de fecha de publicación (lo más cercano primero), ~2 días antes, y avisa "Video X listo".
- Noticias NO se pueden grabar por lote (son del día anterior): se graban a diario.
- OJO espacio: crudos del iPhone en 4K HDR pesan ~3 GB; 40 = ~120 GB. Grabar en 1080p 30 fps (~200–400 MB c/u) o ampliar Drive.
- Horas aprobadas: 11:00 noticias, 6:00 p. m. lo demás. Agenda 11–18 nov aprobada (v7–v14, E1, Y1 12 nov, C1–C3, L1–L2, E2, S1 17 nov).

## Montado (10 nov)
- La Agenda es la misma pestaña **Noviembre** (el script ya publica a la Fecha + Hora de cada fila; las noticias las crea la tarea de las 4:35).
- Filas 8–16: E1 (11), Y1 (12), C1 (13), L1 (14), E2 (15), C2 (16), S1 (17), L2 (18), C3 (18, 20:00). Hora 18:00. Estado `Por guion` / `Sale de Y1`. Columna Tipo: Explicativo, YouTube largo, Clip cascada, Lead, VSL (Code.gs CONFIG.TIPOS solo tiene 'Noticias IA': agregar los nuevos en el bloque 2).
- Fechas: escribir como texto dd/mm/aaaa (la hoja está en español: =DATE con comas da #ERROR).
- Calendar: 9 eventos "🎬 <código> · …" (ids o36dtsqi…, 1468l40c…, pel9p7bl…, svcupnlb…, qp16kgd1…, 8se56at0…, 7vncno2c…, 1c5r0fkk…, ob84brn8…).
- Falta del bloque 1: guiones de E1, Y1, L1, E2, S1, L2 (link en la columna Guion) y la Agenda del 19 al 30.
- Pestaña **VIDEOS MES** (sheetId 4, 2.ª pestaña): lista del mes que se llena sola con `=QUERY(Noviembre!A2:U; "select J, O, A, L, F, B, M, G, H, N, R, S, T where A is not null order by A, L"; 0)` en A4. Columnas: Código, Tipo, Fecha, Hora, Pieza, Producción, Publicación, Guion, Video editado, Instagram, YouTube, Link YouTube, TikTok. No escribir ahí. Para diciembre: cambiar `Noviembre` por `Diciembre`.
- CAL IG (calendario visual) ya muestra las piezas nuevas solo.
- Ojo: fórmulas en esta hoja van con `;` (hoja en español).
