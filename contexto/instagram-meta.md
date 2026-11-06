# Instagram ↔ Meta: publicación automática (conectado 5 nov 2026)

## Datos (no son secretos)
| Qué | Valor |
|---|---|
| Cuenta | @soysanti__content_ia (dos guiones bajos) |
| IG_ID | `17841438740412085` |
| Página de Facebook | "Santi • content IA", id `1468491546343867` (la vieja "syntrix" no se usa) |
| App de Meta | "Publicador Santi", App ID `1462889889116914`, modo desarrollo, tipo Business |
| Producto | Instagram › "API setup with Facebook login" (graph.facebook.com) |
| Permisos del token | instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management |
| Cupo | 100 publicaciones por día por API |

## Dónde vive cada cosa
- Código de la hoja del plan: `google-apps-script/plan-contenido/Code.gs` (copia exacta de lo que está en Apps Script).
- `appsscript.json` del proyecto: scopes spreadsheets, drive, script.external_request, script.scriptapp,
  script.container.ui y **calendar** + bloque webapp (para el buzón `Subidas.gs`).
- Propiedades del script: `CLAVE_SUBIDA` (buzón), `DESDE`, **`META_TOKEN`** (token de página, no vence).
  El nombre tiene que ser exactamente `META_TOKEN`, en mayúsculas.
- Tareas automáticas (las crea `instalar`, corrido el 5 nov 12:44): `publicarPendientes` cada 15 min,
  `traerVideosNuevos` cada hora, `alEditar` al editar la hoja.

## Cómo se sacó el token (por si hay que repetirlo)
1. Graph API Explorer › app "Publicador Santi" › "Obtener token de acceso de usuario" › los 5 permisos ›
   Generate Access Token (elegir la página nueva y la cuenta de IG).
2. `me/accounts?fields=name,instagram_business_account{id,username}` → IG_ID.
3. Depurador de tokens › "Extender token de acceso" (usuario de 60 días).
4. Con ese token en el Explorer: `me/accounts?fields=name,access_token` → token de página que no vence.
5. Guardarlo en Propiedades del script como `META_TOKEN`. Probar con `probarConexion`.
Si Meta responde error 190, el token venció o es inválido: repetir 3–5.

## Lecciones de la conexión
- Santiago trabaja en iPad: al copiar código, que use el botón de copiar del bloque (una vez se pegó el texto del
  chat dentro de Code.gs y dio "SyntaxError: Unexpected identifier 'está'").
- Pedir capturas tapando tokens y claves. Nunca pedir el token por el chat.
- Cuando pide "el código completo", darlo entero en un solo bloque, listo para reemplazar todo.


## 6 nov 2026 · Falla: v2 salió en YouTube pero no en Instagram
- Hoja: Publicación quedó en `Programado` sin error y YouTube = `Publicado`. Santi lo subió a mano a IG y TikTok.
- Causa más probable: a las 11:00 una sola vuelta de `publicarPendientes` subía a YouTube (28 MB), luego a Instagram y
  esperaba hasta 2 min. Apps Script corta a los 6 min **sin pasar por el catch**, así que la fila quedó en `Programado`.
  (Confirmar en Apps Script › Ejecuciones: "Se excedió el tiempo máximo de ejecución".)
- Arreglo (Code.gs + YouTube.gs): cada vuelta hace **un solo paso pesado** y ninguno empieza pasados 90 s.
  1) A la hora: sube a Instagram, YouTube queda `Pendiente`, espera 30 s y revisa una vez (si ya procesó, publica).
  2) Vuelta siguiente (15 min): sube a YouTube; si IG seguía procesando, lo publica.
  Sin esperas largas en `revisar_`. TikTok: solo si `TikTok.gs` está instalado (`typeof tiktokFila_`), y por ahora a mano.
- Probado con simulación en node (4 vueltas): IG publicado en la 1ª o 2ª vuelta, YouTube en la 2ª.
- **Instalar:** Santi pega `Code.gs` y `YouTube.gs` del repo en Apps Script (reemplazar todo) y guarda. No hay que volver a autorizar.
