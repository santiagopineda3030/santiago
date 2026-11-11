# TikTok · Auditoría para publicar directo (preparado 11 nov 2026)

## Lo importante primero (reglas de TikTok, revisadas hoy en developers.tiktok.com/doc/content-sharing-guidelines)
1. **Apps de uso personal/interno se rechazan.** "Una herramienta para subir a las cuentas que maneja tu equipo" está en la lista de NO aceptadas.
   → La app debe presentarse como **producto de ContentIA para sus clientes** (creadores/dueños de negocio que programan
   SUS propios videos). Es verdad: el Cerebro de Contenido se entrega a clientes.
2. **La pantalla de publicar tiene que cumplir esto (hoy la hoja NO lo cumple):**
   - Mostrar el **nombre de la cuenta** (creator_info, pedido al abrir la pantalla) y bloquear si TikTok dice que no puede publicar ahora; revisar duración máxima.
   - **Privacidad en lista desplegable, sin valor por defecto** (opciones de creator_info).
   - Casillas **Comentarios / Dúo / Stitch**, ninguna marcada por defecto (grises si la cuenta las tiene apagadas).
   - Interruptor **contenido comercial** (apagado): "Tu marca" / "Contenido de marca"; con él prendido y nada marcado, botón desactivado; contenido de marca no puede ser privado.
   - **Vista previa** del video, título y hashtags editables, sin marcas de agua.
   - Frase de **consentimiento** con link a la *Music Usage Confirmation* (y *Branded Content Policy* si aplica) antes del botón.
   - Después: "puede tardar unos minutos" + estado de la publicación.
3. Programar está bien si el dueño aprueba cada video con esa pantalla (así funcionan Buffer o Later).

## Qué falta construir (Claude, ~1 chat de código)
**Panel "Aprobar para TikTok"**: página web de Apps Script (se abre desde el menú Plan IG) con todo lo del punto 2.
Santi aprueba ahí cada video (privacidad, interacciones, consentimiento) y el script lo publica a la hora de la fila
(`TT.DIRECTO: true`, `video.publish`). Cambio para Santi: un clic más por video. **Necesita su OK.**

## Datos para el formulario (Production, inglés)
- **App name:** ContentIA Publicador · **Category:** Business / Productivity · **Platform:** Web
- **Description:** "ContentIA Publicador lets creators and small-business owners plan their own original short videos in a
  content calendar and publish them to their own TikTok account. For each video, the creator reviews a preview, edits the
  caption, chooses privacy and interaction settings and confirms before it is posted at the time they chose."
- **Login Kit:** "Each creator logs in with Login with TikTok to connect their own account. We only read basic profile
  info (display name, avatar) to show which account is connected on the publishing screen."
- **video.upload:** "Optional: the creator can send a video to their TikTok inbox as a draft to finish it in the TikTok app."
- **video.publish:** "On the publishing screen the creator sees their nickname, a preview, an editable caption, a privacy
  dropdown with no default (options from creator_info), comment/duet/stitch toggles off by default, the commercial content
  disclosure and the Music Usage Confirmation. Only after they click Publish is the video posted to their own account at
  their scheduled time. We never post to other users' accounts or without the creator's explicit approval."
- **Scopes:** `user.info.basic`, `video.upload`, `video.publish` · **Redirect URI:** la misma del Sandbox (`tiktok.md`).
- **Ícono:** `tiktok-app/icono-contentia-1024.png`.
- **Términos y Privacidad:** los Google Docs públicos (IDs en `drive.md`); cuando la web esté publicada, cambiarlos por
  `<dominio>/terminos` y `<dominio>/privacidad`. **Web URL:** la web propia apenas exista (Instagram es débil para la revisión).
  Revisar que Términos/Privacidad digan "creadores/clientes", no solo la cuenta de Santi.

## Video demo (mp4 < 50 MB, grabado en el PC con pantalla completa)
1. Abrir la web/landing → muestra qué es ContentIA Publicador (5 s).
2. "Login with TikTok" → pantalla de autorización de TikTok con los scopes → vuelve conectado (nombre visible).
3. Hoja del plan → fila del video → menú Plan IG › Aprobar para TikTok.
4. En el panel: vista previa, editar título, elegir privacidad (mostrar que no hay valor por defecto), marcar comentarios,
   mostrar el interruptor comercial, leer la frase de consentimiento → Publicar.
5. Mostrar el estado "Procesando… / Publicado" y abrir TikTok con el video publicado (en sandbox sale privado: está bien).
Sin cortes raros; con la URL del navegador visible. Se graba cuando el panel esté hecho.

## Pasos de Santi en el portal (developers.tiktok.com › ContentIA › ContentIA Publicador)
1. Sandbox Pruebas: prender **Direct Post** (agrega `video.publish`) › Apply changes. (Para probar el panel.)
2. Pestaña **Production**: llenar con los datos de arriba (ícono, categoría, descripción, Términos, Privacidad, web,
   plataforma Web, Redirect URI), productos Login Kit + Content Posting API con Direct Post, los 3 scopes.
3. Pegar los textos de cada producto/scope de arriba.
4. Subir el **video demo** y **Submit for review**. TikTok responde por correo (días a ~2 semanas).
5. Aprobada: copiar Client key/secret de **Production** a Propiedades del script › Plan IG › Conectar TikTok › probar.
