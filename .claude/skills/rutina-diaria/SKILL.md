---
name: rutina-diaria
description: Rutina diaria de Santiago (chat "Santi · Base"). Úsalo cuando Santi dice "¿qué hay hoy?", "qué tengo pendiente", "empecemos el día", "sigamos" o "cierro el día". Lee la hoja del plan, la COLA POR EDITAR y la carpeta Guiones, ordena lo pendiente por prioridad y abre un chat por pieza en su área (Instagram, TikTok, YouTube, Anuncios Meta).
---

# Rutina diaria · Santi · Base

Español, tuteo, frases cortas (Santi suele estar en el iPad). Este chat **solo prioriza, abre chats y cierra el día**: no edita.

## 1. Leer (conectores de Google Sheets y Drive; IDs en `contexto/drive.md`)
- Hoja **Plan contenido orgánico - ContentIA** `1lvs82vX8Pj3rHmVZyUj9cUh6dOm5srjbVDwzvWUyku4`:
  - Pestaña del mes (Noviembre…): A Fecha · B Estado · C Ángulo · D Referente · E Explicación · F Guion · G Elementos adicionales ·
    H Link Video Editado · I Descripción de Instagram · J # · K Archivo · L Hora · M Publicación · N Link publicado · O Tipo ·
    P contenedor (oculta, no tocar) · Q Título YouTube · R YouTube · S Link YouTube.
  - **COLA POR EDITAR** (datos desde la fila 4): A Subido · B Código · C Categoría · D Título · E Crudo · F Carpeta ·
    G Instrucciones · H Estado · I Corrección · J Editado (link) · K Entregado · L Notas.
    Estados: Por editar → Editando → Revisión → Corrección → Entregado.
- Drive › **Guiones** › <red> › `2. Guiones en frío`: guiones que la tarea de las 4:35 dejó y falta revisar.
- Drive › <red> › `2. Crudo sin editar`: crudos nuevos que aún no tienen fila en la COLA.

## 2. Contarle qué hay (máximo 8 líneas, por prioridad)
1. **Corrección** (lo que Santi devolvió). Siempre primero.
2. **Guion en frío** sin revisar (sobre todo el del video de mañana a las 11:00).
3. **Por editar** / crudos nuevos, empezando por lo que se publica antes.
4. Lo que está en **Revisión** esperando que Santi lo vea.
5. Filas en **Listo** que esperan su aprobación (`Publicar` solo lo pone Santi).
Termina con: "Te propongo empezar por …". Si no hay nada: "Todo al día".

## 3. Un chat por pieza
Cuando Santi escoja una pieza ("trabajemos el v2", "revisemos el guion de hoy"):
- Si la herramienta `create_session` está disponible: crear una sesión con **title** `<código> · <título corto>`
  (ej. `v2 · Noticias IA 6 nov`), **tags** con su área (`area:instagram`, `area:tiktok`, `area:youtube`, `area:meta`,
  `area:guiones`) y **prompt** con la fila completa + "usa el CLAUDE.md y la skill de `areas/<área>`". Antes, buscar con
  `list_sessions` si la pieza ya tiene chat y mandarlo a ese. Decirle en una línea: "Te abrí *v2 · Noticias IA* en Instagram."
- Si no está disponible: trabajar la pieza aquí mismo siguiendo `areas/<área>/CLAUDE.md` y su skill.
- Guiones → skill `revisar-guion`. Video de Instagram → `areas/1-instagram`. TikTok → `areas/2-tiktok`.
  YouTube → `areas/3-youtube`. Anuncios → `areas/4-anuncios-meta`.

## 4. Archivar lo terminado (cada mañana)
Pieza terminada = Estado **Entregado** en la COLA y **Publicado** en la pestaña del mes. Archivar su chat
(`list_sessions` + `archive_session`; archivar no borra). Nunca borrar nada de Drive.

## 5. Cerrar el día ("cierro el día")
Resumen de 3–5 líneas: qué quedó listo, qué sigue pendiente, reglas nuevas. Escribirlo en `contexto/bitacora.md`
y hacer commit + push a GitHub.
