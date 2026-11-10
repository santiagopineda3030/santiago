# Kit de contenido mensual (acordado con Santi, 10 nov 2026) — se monta desde el jueves 12

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
