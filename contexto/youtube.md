# YouTube Shorts: publicación automática (instalado y probado 5 nov 2026)

- Canal: **Soy Santi media YT** (@santimediayt), en santiagopineda3030@gmail.com.
- `probarYouTube` corrió bien el 5 nov 13:12 y creó las columnas en la hoja.
- Prueba real 5 nov: subió v1 sola (shorts/6-jhDrkqmfM), sin aviso de privado. Funciona por el disparador de 15 min.

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
6. v1 ya lo subió Santiago a mano (marcado `Publicado`). La primera prueba real es el próximo video aprobado.

## Riesgo conocido
YouTube deja **privados (bloqueados)** los videos subidos por proyectos de API sin verificar. Si pasa, la columna
Link YouTube dice "⚠ YouTube lo dejó private". Solución: pasar el script a un proyecto de Google Cloud propio y pedir
la auditoría de la API de YouTube (formulario de Google, tarda días). Mientras tanto se publica a mano desde Studio.
Cupo: 10.000 unidades/día; cada subida ~1.600 → hasta 6 por día.

## YouTube largo (11 nov)
- Tipo "YouTube largo" en la hoja → va SOLO a YouTube (TikTok = "No", Instagram no), sin #Shorts, link youtu.be/<id>.
- Sube por partes de 16 MB con la subida reanudable (UrlFetch máx. 50 MB): ~4 min por vuelta, guarda el avance en Propiedades del script `YTL_<id del archivo>`. Mientras sube: YouTube = "Subiendo", Link YouTube = "Subiendo video largo: N%".
- La fila principal queda "Publicado" con link "Solo YouTube (video largo)". Si falla: "Error" → poner "Publicar" en la columna YouTube para reintentar.
- Código: YouTube.gs (youtubeLargo_, esLargo_) + Code.gs (publicarPendientes). Primera prueba real: Y1, sáb 14 nov 18:00.
