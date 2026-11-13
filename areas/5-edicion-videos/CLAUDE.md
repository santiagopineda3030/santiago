# Área 5 · Edición de videos (un solo video para Instagram, TikTok y YouTube Shorts)

Este chat (📁 Edición de videos) edita los videos de Santi de principio a fin. Reglas generales: `CLAUDE.md` de la raíz.
Paso a paso: skill `editar-video` (`.claude/skills/editar-video/SKILL.md` de esta carpeta). Úsala siempre.

- **Frase de arranque:** "Claude, ya subí los videos a videos en frío" (o parecido).
- **Drive › ContentIA › Edición de videos** `1d-q-IQvGntqwJBuLkk5arAwd2AytkCzi`:
  - `1. Videos en frío` `1GFl-0CSYI8afA0tzKGa0AVmM7FC-d4ON` → aquí Santi sube los crudos (antes "Instagram › 2. Crudo sin editar", mismo ID).
  - `2. Videos terminados` `1A1zlwXyvR-l2CZcJ6dnHUp-SZXnEcUGT` → aquí van los editados (antes "Instagram › 4. Contenido editado",
    mismo ID: la publicación automática de Instagram, YouTube y TikTok lee esta carpeta, no cambiar el ID).
- **Reglas de edición:** "Guía de edición · Noticias IA" (Instagram › 3. Recursos) + "Recursos y reglas" de TikTok y YouTube.
- **Guion:** Guiones › Instagram › `3. Guiones terminados` (un solo guion sirve para las 3 redes).
- **Videos largos de YouTube (16:9):** también se editan aquí, pero se entregan en YouTube › `4. Contenido editado` y Santi
  los sube a mano en Studio (ver `areas/3-youtube/CLAUDE.md`).

## Regla del 10 nov (Santi): editar según la Agenda
- Cada crudo se llama con su código (v7, E1, Y1, L1, S1…). Busca su fila en la pestaña del mes (columna #).
- El guion está en la columna G ("Guion: <link>"). Edita con ese guion **y su sección "Edición"** (indicaciones de estilo, pantalla, b-roll, música, duración) más lo que Santi diga.
- Orden: lo que se publica más pronto primero. Al terminar: subir a 2. Videos terminados, estado `Listo`, y avisar "🎬 <código> listo, míralo". Santi revisa siempre (máx. 2 versiones).
- YouTube largo (Y): 16:9. Clips (C): salen de la cascada (kit-cascada/) del Y correspondiente. Detalle: contexto/agenda-mensual.md.
- **Sin robot (13 nov, Santi):** el robot de edición se eliminó. Este chat edita TODO: Santi sube el crudo a 1. Videos en frío y avisa aquí; Claude edita, sube a 2. Videos terminados, deja la fila en `Listo` y espera el "dale" para poner `Publicar`. Toda regla nueva va al README del editor.

## Referentes de edición (11 nov, Santi) — OBLIGATORIO
Antes de editar cualquier video usa la skill **`referentes-edicion`** (`.claude/skills/referentes-edicion/SKILL.md`):
lee la sección del tipo en `contexto/referentes-edicion.md` y mira la hoja de cuadros del referente en `referentes/`.
