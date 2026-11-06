# TikTok: plan A (borrador automático) · código listo 5 nov 2026, falta instalar

## Cómo funciona
- Misma fila y misma aprobación que IG/YouTube. A la hora, `publicarPendientes` manda el video a TikTok como
  **borrador** (API Content Posting, modo inbox `video.upload`) y le llega a Santiago un **correo** con la descripción
  para copiar. Él abre TikTok › notificación › pega › Publicar. El borrador vence en ~24 h.
- Por qué borrador: TikTok solo deja publicar en público a apps auditadas. Cuando aprueben la app, se cambia a
  publicación directa (`video.publish`, endpoint `/post/publish/video/init/` con `post_info`).
- Código: `google-apps-script/plan-contenido/TikTok.gs` + ganchos en `Code.gs`; `appsscript.json` suma `script.send_mail`.
- 6 nov: arreglado para que salga solo: a la hora, IG primero; la columna TikTok queda `Pendiente` y sube en la
  vuelta siguiente (después de YouTube), un paso pesado por vuelta.
- Columnas: **TikTok** (vacía = va con IG · `No` · `Publicar` = ya · el script pone `Subiendo`, `En borradores`,
  `Publicado`, `Error`) y **Link TikTok**. Cada 15 min revisa si el borrador ya se publicó.
- Tokens en Propiedades del script: `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` (los pone Santiago),
  `TIKTOK_REFRESH`/`TIKTOK_ACCESS`/`TIKTOK_VENCE` (los pone el script). Access dura 24 h, refresh 1 año.
- Redirect URI = `https://script.google.com/macros/d/<SCRIPT_ID>/usercallback` (sale en el log de `probarTikTok`).

## Instalar (Santiago)
1. developers.tiktok.com › entrar con la cuenta de TikTok de la marca › Manage apps › crear app.
2. Productos: **Login Kit** + **Content Posting API** (solo "Upload"). Scopes: `user.info.basic`, `video.upload`.
3. Pegar en Apps Script `TikTok.gs`, el `Code.gs` nuevo y el `appsscript.json` nuevo.
4. Correr `probarTikTok` › copiar la Redirect URI del log › Login Kit › Redirect URI (Web).
5. Pestaña **Sandbox** › agregar su cuenta como usuario de prueba. Copiar Client key y Client secret a Propiedades.
6. Hoja › Plan IG › Conectar TikTok › Autorizar. Luego Plan IG › Probar conexión con TikTok.
7. Pedir la auditoría (necesita páginas de Términos y Privacidad públicas y un video demo) para pasar a directo.

## Pendiente / dudas
- 6 nov: **app creada** en developers.tiktok.com. El error de ayer era que ahora TikTok exige una *organización*.
  - Organización **ContentIA** (Org ID `7705137509315019796`) › app **ContentIA Publicador** (tipo Other).
  - Sandbox **Pruebas**: plataforma Web, Login Kit + Content Posting API (Direct Post apagado), scopes
    `user.info.basic` + `video.upload`, target user **soysanti_media**.
  - Script ID (hoja del plan): `1N_00QeBrzzAoUwcmInJBEkHs2rPnvQNeF0jd15DQc5lZgVdbmQ9ZYNpr` → Redirect URI
    `https://script.google.com/macros/d/1N_00QeBrzzAoUwcmInJBEkHs2rPnvQNeF0jd15DQc5lZgVdbmQ9ZYNpr/usercallback` (ya pegada).
  - Ícono: `tiktok-app/icono-contentia-1024.png`. Faltaba para "Apply changes": ícono, categoría, descripción y links
    (Términos, Privacidad, sitio web). Siguiente: links, Apply changes, claves del Sandbox a Propiedades, pegar código.
- Confirmar que el sandbox deja mandar borradores reales a su cuenta (si no, hay que pedir revisión de la app).
- La landing aún no está publicada: Términos y Privacidad hay que alojarlos en algún lado para la auditoría.
