# YouTube Shorts: publicación automática (código listo 5 nov 2026, falta instalar)

## Cómo funciona
- Misma hoja, misma fila, misma aprobación: cuando Santiago pone `Publicar` y llega la fecha y hora,
  `publicarPendientes` sube **primero a YouTube** y después publica en Instagram.
- Código: `google-apps-script/plan-contenido/YouTube.gs` (+ ganchos en `Code.gs`) y `appsscript.json`.
- Columnas nuevas al final de cada pestaña del mes (las crea `prepararYouTube_` / `probarYouTube`):
  - **Título YouTube** (opcional, máx. 100). Vacía = primera línea de la descripción sin hashtags.
  - **YouTube**: vacía = sale con Instagram · `No` = no subir · `Publicar` = subir ya (para videos que ya
    salieron en IG, ej. v1) · el script pone `Subiendo` / `Publicado` / `Error`.
  - **Link YouTube**: `https://youtube.com/shorts/<id>` o el error.
- Descripción = la de Instagram + `#Shorts`. Tags = los hashtags. Categoría 28 (Ciencia y tecnología), español,
  público, no es para niños. Un Short = vertical y ≤ 3 min: nuestros videos ya cumplen.
- Nunca reintenta solo (para no duplicar): `Error` o `Subiendo` → revisar en YouTube Studio y volver a poner `Publicar`.
- Las filas que ya estaban `Publicado` en IG **no** se suben solas.
- El evento de Calendar ahora dice "Instagram · YouTube Shorts" y trae los dos links.
- Apagar YouTube sin tocar IG: `YT.ACTIVO = false` en `YouTube.gs`.

## Instalar (Santiago, una vez, desde Apps Script de la hoja)
1. Tener canal de YouTube en santiagopineda3030@gmail.com (youtube.com › foto › Crear un canal).
2. Apps Script › **Servicios +** › YouTube Data API v3 › Agregar (identificador `YouTube`).
3. ⚙️ Configuración › marcar "Mostrar el archivo de manifiesto" › `appsscript.json` › reemplazar todo por el del repo.
4. Reemplazar `Code.gs` entero y crear el archivo `YouTube` (+ › Script) con `YouTube.gs`.
5. Elegir `probarYouTube` › Ejecutar › Autorizar (pide permiso de YouTube) → debe salir el nombre del canal.
6. Prueba real: en la fila de v1 poner `Publicar` en la columna **YouTube** → revisar el Short en YouTube Studio.

## Riesgo conocido
YouTube deja **privados (bloqueados)** los videos subidos por proyectos de API sin verificar. Si pasa, la columna
Link YouTube dice "⚠ YouTube lo dejó private". Solución: pasar el script a un proyecto de Google Cloud propio y pedir
la auditoría de la API de YouTube (formulario de Google, tarda días). Mientras tanto se publica a mano desde Studio.
Cupo: 10.000 unidades/día; cada subida ~1.600 → hasta 6 por día.
