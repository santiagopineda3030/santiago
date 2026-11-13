# Santiago · AI Work — memoria del proyecto

Este archivo lo lee Claude al empezar cada sesión. Es la memoria en la nube (GitHub, rama
`claude/santiago-ia-landing-4q4ef1`, la rama principal del repositorio).

## Cómo usar la memoria (para gastar menos tokens)
- **Al abrir un chat nuevo: leer primero `contexto/estado-actual.md`** (qué funciona, qué sigue, reglas para gastar menos).
- Aquí va solo lo esencial. El detalle está en `contexto/`, y se lee **solo cuando la tarea lo necesita**:
  | Archivo | Cuándo leerlo |
  |---|---|
  | `contexto/bitacora.md` | Para saber qué se hizo y qué quedó a medias |
  | `contexto/drive.md` | Mapa completo de Drive con todos los IDs |
  | `contexto/chats.md` | Lista de chats (activos y archivados), su carpeta y tareas programadas |
  | `contexto/kit-contentia.md` | Kit de edición ContentIA: áreas, skills y documentos de reglas por red |
  | `contexto/tarea-guion-diario.md` | Texto exacto de la tarea de las 4:35 p. m. (para corregirla o recrearla) |
  | `drive-respaldo/` | Copias de lo importante de Drive (guía de edición, instructivo del sistema, guiones) |
  | `contexto/instagram-meta.md` | Publicación automática, token, errores de Meta |
  | `contexto/youtube.md` | YouTube Shorts automático: columnas, instalación, riesgo de video privado |
  | `contexto/guiones.md` | Carpetas de guiones (ideas, en frío, terminados), recursos por red, tarea de las 4:35 p. m. |
  | `contexto/anuncios-meta.md` | Anuncios Meta: flujo acordado, plan de automatización, qué falta |
  | `contexto/tiktok.md` | TikTok: borrador automático (plan A), app de TikTok, auditoría |
  | `contexto/referentes-edicion.md` | Estilo por tipo de video (referentes de Santi); skill `referentes-edicion`, videos en `referentes/` |
  | `contexto/agenda-mensual.md` | Kit de contenido mensual: agenda en la hoja, aviso para revisar |
  | `contexto/licencias.md` | Plan para entregar carpetas a clientes sin que las compartan (se monta al final) |
  | `contexto/ai-work.md` | Oferta, embudo, entrega, pendientes del negocio |
  | `contexto/producto.md` | Qué recibe el cliente: carpetas plantilla, módulos de Skool, requisitos |
  | `contexto/estudio-de-mercado.md` | Textos de venta, guiones de leads |
  | `editor-noticias/README.md` | Editar videos |
- **Al terminar cada tarea:** una línea en `contexto/bitacora.md`, actualizar este archivo si cambió algo
  importante, y commit + push a GitHub. Sin esperar a que lo pida.
- **Todo lo que se cree o cambie fuera del repo** (carpetas de Drive, tareas programadas, documentos de reglas) se guarda
  aquí también: IDs en `contexto/drive.md`, textos de tareas en `contexto/`, copias de documentos en `drive-respaldo/`.
  Santiago revisa GitHub y quiere encontrar TODO.
- Una sesión nueva por tarea grande: todo queda aquí, no hace falta un chat largo.

## Cómo está organizado Claude · Kit de edición ContentIA (5 nov)
- **Al empezar cada chat:**
  - Si el chat se llama **Santi · Base** o Santi dice "¿qué hay hoy?" → skill `rutina-diaria` (prioriza, abre un chat por pieza, cierra el día; no edita).
  - Si se llama **Santi · Preguntas** o pregunta cómo funciona algo → skill `preguntas` (responde con la memoria; no edita).
  - Si es el chat de **una pieza** (título `<código> · <tema>`) → seguir el `CLAUDE.md` y la skill de su área.
  - Link de un video que le gusta ("agrega este referente") → skill `agregar-referente`.
  - Aviso "🟢 Guion en frío listo" o "revisemos el guion" → skill `revisar-guion`.
- **Áreas** (`areas/<área>/CLAUDE.md` + su skill en `areas/<área>/.claude/skills/`):
  | Área | Skill | Reglas (Drive › <red> › 3. Recursos) |
  |---|---|---|
  | `areas/1-instagram` | `editar-instagram` | Guía de edición · Noticias IA |
  | `areas/2-tiktok` | `editar-tiktok` | Recursos y reglas · TikTok |
  | `areas/3-youtube` | `editar-youtube` | Recursos y reglas · YouTube |
  | `areas/4-anuncios-meta` | `editar-anuncio` | Recursos y reglas · Anuncios (Meta) |
| `areas/5-edicion-videos` | `editar-video` | (Sin robot desde 13 nov: lo edita SOLO el chat 📁 Edición de videos) Edita lo de `1. Videos en frío`, revisa con Santi, sube a `2. Videos terminados` y programa |
- **Chats (renovados 12 nov, TODOS en Opus 5.5; al empezar leen `contexto/estado-actual.md`; regla de Santi: no hacer nada sin su permiso):**
  `Santi · Base 3` (`session_01McnvqtDPHNYbE9DQ8iQJeH`) · `Santi · Preguntas` (`session_01Mcnvqvgpb4vJdHLWw8g5tF`) ·
  📁 Edición de videos `session_01Mcnvqw535MF9WSXKXT5Cgs` · 📁 Guiones `session_01McnvqvLLYGtXVTA9bDdCQW` ·
  📁 Anuncios (Meta) `session_01McnvqsMdqqqXtnJVikQRtp` · 📁 TikTok `session_01McnvqvdnHAnmk3XpmCv1th` ·
  📁 Instagram `session_01McnvqvSeKF6PQgmxb8TMbh` · 📁 YouTube `session_01Mcnvqv6MuyBBGX1vcj7n1C` · Web · Landing `session_01Mcnvqshyy1YTa2uLZAZ2tP`.
  Al cerrar cada día se renuevan todos (nuevos y cortos, viejos archivados). Al crearlos con create_session SIEMPRE poner `source_url` (repo) y `source_revision`, o salen sin memoria. Viejos: `contexto/chats.md`.
- **Videos viejos se borran** (regla de Santi, 7 nov): cuando un video ya se publicó, su crudo va a la papelera y se revisa el
  espacio de Drive; Santi vacía la papelera.
- **Guiones viejos se borran** (regla de Santi, 5 nov): guion en frío → papelera al terminarlo; guion terminado + idea →
  papelera cuando el video se publica (antes, copia en `drive-respaldo/guiones/`). Nunca la clase gratis. Detalle: `contexto/guiones.md`.
- **Correcciones que son regla** → "Ajustes de Santi" del documento de la red (Drive + copia en `drive-respaldo/recursos/`) + bitácora.

## Quién es y cómo hablarle
- **Santiago Pineda** (santiagopineda3030@gmail.com), Colombia, zona horaria **America/Bogota**.
- **Siempre en español**, tuteo, frases cortas y simples. Explicar paso a paso, con capturas si hace falta.
  Desde el 6 nov trabaja desde su **PC** (ya no el iPad): las instrucciones pueden ser para computador.
  Claude corre en la nube y no ve el PC; si hace falta trabajar en archivos del PC, Santi abre Claude Desktop o `claude remote-control` allí.
- Nunca pedirle claves, tokens ni contraseñas por el chat (van en Propiedades del script o en el entorno).

## El negocio (detalle en `contexto/ai-work.md`)
- Marca personal de IA. Una sola oferta high ticket: **Cerebro de Contenido**, **$2.500 pago único**,
  vendida por **llamada**. Modelo *Done With You*: montamos, el cliente llena, su **Gestor IA** revisa.
- Instagram: **@soysanti__content_ia** (dos guiones bajos; cuenta profesional).
- Público: dueños de negocio sin tiempo para contenido. Redes: **Instagram, TikTok, YouTube** (Facebook no).
- Embudo: videos (noticias de IA + videos de leads) → "comenta CLAUDE" → clase gratis (~3 min) →
  web con video + formulario + calendario → sheet de leads → setter → closer.
- Regla de contenido: **mostrar resultados del sistema, nunca las herramientas ni la configuración.**
- Estudio de mercado: `contexto/estudio-de-mercado.md`.

## Contenido diario: Noticias de IA
- **Todos los días a las 11:00 a. m.** (Bogotá, siempre a las 11, no otra hora), con las 5 noticias del día anterior. Del 5 al 18 de nov 2026.
- Estructura: Gancho → Viral 1 → Viral 2 → Polémica 1 → Polémica 2 → Útil → CTA.
- **Un solo guion corto para Instagram, TikTok y YouTube Shorts** (es el mismo video). Lo único que se escribe aparte es el
  guion de **YouTube largo** (16:9, tema que esté funcionando en el momento). Regla de Santi, 5 nov.
- Guía de edición (Drive, Instagram › 3. Recursos): vertical 1080×1920, 45–75 s, H.264 ≤ 30 MB,
  subtítulos 2–4 palabras con palabras clave en rojo, título por noticia, gancho en los primeros 3 s,
  voz a −14 LUFS. Nombre del archivo: `v<código> <versión> <tema>.mp4` (ej. `v1 1.2 noticias-dia-1.mp4`).

## Dónde está todo (Google Drive › ContentIA)
| Qué | Dónde | ID |
|---|---|---|
| Carpeta raíz | ContentIA | `1LvKFGptavlfPDXzj48OVJZR7Yos2VIFC` |
| Plan de contenido IG (hoja) | Plan contenido orgánico - ContentIA | `1lvs82vX8Pj3rHmVZyUj9cUh6dOm5srjbVDwzvWUyku4` |
| Sistema (Code.gs, Subidas.gs, prompt) | 0. Sistema | `1SlcWLrDd6LfoA_PRwedJ4MeVFIL_0HxL` |
| **Guiones** (todas las redes) | Guiones › <red> › 1. Ideas / 2. Guiones en frío / 3. Guiones terminados | `15J5tBsxY1o98Eee_v0jEH98mE720Ql8s` |
| Ideas IG / En frío IG / Terminados IG | Guiones › Instagram › … | `1qosYx_N0AKGhGMweD3nJtLZtUwNDlud_` / `1xmfC0MN5kSMKIJMRpb4XSwhGZChCy0t5` / `1Kx0aOb41wOsZLvxPAt1fNY83eFe-7O2p` |
| Videos en frío (crudos, las 3 redes) | Edición de videos › 1. Videos en frío | `1GFl-0CSYI8afA0tzKGa0AVmM7FC-d4ON` |
| Recursos IG (guía de edición) | Instagram › 3. Recursos | `1Hd3rJljSfAr6ehoBet0xeFJIk1Fz84Rn` |
| Videos terminados (los lee la publicación automática) | Edición de videos › 2. Videos terminados | `1A1zlwXyvR-l2CZcJ6dnHUp-SZXnEcUGT` |
| TikTok / YouTube / Anuncios (Meta) | misma estructura: 2. Crudo, 3. Recursos, 4. Editado (vacías) | todos los IDs en `contexto/drive.md` |

## El plan de contenido (hoja) — reglas que no se rompen
- Pestaña del mes (Noviembre…): una fila por idea; código `#` = v1, v2…
- **Publicación**: `Escribiendo descripción` → `Listo` (Claude) → `Publicar` (**solo Santiago aprueba**) →
  `Programado` → `Publicado`. **Desde el 7 nov:** Claude le muestra a Santi el video y la descripción, Santi confirma en el chat
  ("dale", "publícalo") y **Claude pone `Publicar`** en la hoja. Sin esa confirmación explícita, nunca.
- Nunca poner `Publicar` si el video no está en Drive: el script lo marca Error y deja de enlazarlo.
- Descripción: 3–5 líneas, la primera es el gancho, sin datos inventados, emoji solo en el cierre, 5 hashtags.
- COLA POR EDITAR: fila por pieza; al entregar → `Entregado` + link + fecha.
- **Cada video publicado se marca también en Google Calendar** (calendario principal de Santiago):
  título `✅ Publicado · <título original>`, color verde (colorId 10), hora real de publicación,
  y en la descripción las redes, la hora y el link del video en Drive. Sin notificaciones.
- Publicación automática en Instagram: **conectada** (5 nov 2026). **6 nov:** el v2 salió en YouTube pero NO en Instagram
  (la vuelta se pasó de 6 min). Código arreglado: un paso pesado por vuelta (IG primero, YouTube en la siguiente). **Instalado por Santi el 6 nov
  13:06** (probarConexion OK). **7 nov:** el v3 falló en IG (sin memoria con getBytes; como blob → ProcessingFailed; por partes → no se acepta). **Arreglo final probado 13:22 (FINISHED):** Instagram descarga el video desde Drive con `video_url` (link abierto solo mientras procesa, luego privado). Prueba sin publicar: `probarSubidaInstagram`. Primera prueba real: v4, 8 nov 11:00. IG_ID `17841438740412085`, token en
  Propiedades del script (`META_TOKEN`). Código: `google-apps-script/plan-contenido/Code.gs`. Detalle: `contexto/instagram-meta.md`.

## Herramientas que ya están montadas en este repositorio
- `editor-noticias/`: editor de video propio (ffmpeg + Whisper + animaciones). Flujo que funcionó en v1:
  1. `trozos.py` transcribe cada trozo de voz (detecta tomas repetidas).
  2. Elegir tomas a mano en `edl-*.json` (última toma buena, subtítulos corregidos, gráficos por palabra).
  3. `editar_v2.py` renderiza: cortes por detector de voz, audio sincronizado, animaciones, efectos.
  4. Revisar: transcribir el resultado, buscar silencios (VAD), hojas de cuadros, axe/consola si es web.
- `editor-noticias/subir-drive/`: el **buzón de Apps Script** para que Claude suba videos a Drive solo.
  **Listo desde el 7 nov:** `SUBIDA_URL` y `SUBIDA_CLAVE` están en el entorno (los leen los chats nuevos). Uso: `./subir_drive.sh "<video>.mp4" "NOVIEMBRE 2026"`.
- Landing de la llamada: `src/` (React + Vite + Tailwind, estilo tecnológico cian, logo SPR en píxeles).

## Hoja de ruta hasta el 18 de nov 2026
**PLAN NUEVO (9 nov): doc https://docs.google.com/document/d/1ZsW9J9k2MZroeop9mlxMhJjaJz8fHtQA3qDC6ShQhaw · meta: probar todo antes de vender (posible venta inicio 2027). La tabla de abajo es la vieja (6 nov).**

### Hoja de ruta vieja (6 nov)
Flujo: Santi sube crudos a "Videos en frío" → Claude edita, sube, organiza hoja y calendario → publica solo → Claude da ideas de guiones.
Plan maestro (doc): https://claude.ai/artifact/PnzCmT7dUjbUxnE5Qtg7r1 · Hecho: estudio de mercado (`estudio-de-mercado.md`), oferta (`ai-work.md`), producto (`producto.md`), nombre de marca (ContentIA).
**Todos los días:** prueba automática de las 11:00 (IG + YouTube, luego TikTok) y revisar el guion de las 4:35.
| Día | Qué |
|---|---|
| Jue 6 | ✅ Oferta cerrada. ✅ **TikTok** instalado y conectado (sandbox, sale a borradores después de IG; directo listo con interruptor apagado) |
| Vie 7 | Revisar que el v3 salga solo (IG → YouTube → TikTok a borradores). **Arreglar la subida de videos** (poner `SUBIDA_URL`/`SUBIDA_CLAVE` en el entorno con Santi). **TikTok: permisos** para publicar solo (auditoría, `tiktok.md`). Arrancar **Meta Ads** (📁 Anuncios (Meta)) |
| Sáb 8 | **Meta Ads**: cuenta publicitaria, píxel, campaña en borrador (sin gastar) |
| Dom 9 | **Día de guiones**: guiones del mes (videos de leads + YouTube largos + video gratis) |
| Lun 10 | **Grabar** los videos del mes y el video gratis |
| Mar 11 | **Análisis de la encuesta** (Santi la hace en persona en negocios, plazo martes) · **Web**: preguntas filtro, calendario, hoja de leads, privacidad y términos, dominio; subirla |
| Mié 12 | **Guion de la llamada de venta** · crear **Skool** y la estructura de módulos con tareas |
| Jue 13 | **Carpetas plantilla** de Drive (sin datos de Santi) |
| Vie 14 | **Grabar los módulos** del curso |
| Sáb 15 | **Tracker de alumnos** + bienvenida y onboarding |
| Dom 16 | **Protección del Drive** (`licencias.md`) |
| Lun 17 | **Meta Ads** lista para encender + revisión final de todo |
| Mar 18 | **Todo listo**: lanzar |
No va por ahora: automatizar "comenta CLAUDE" (Santi, 6 nov). Después del 18: pago, setter y closer.

## Pendientes grandes (estado técnico)
1. Confirmar la primera publicación automática real (Instagram ya conectado e instalado).
2. YouTube Shorts: **funcionando** (canal @santimediayt, probado 5 nov). Sale con la misma aprobación de IG.
   TikTok plan A (borrador + correo): **instalado y conectado 6 nov** (sandbox; sale ~15–30 min después de IG a borradores). Falta: primera prueba real y auditoría para publicación directa (`contexto/tiktok.md`).
3. Guiones (`contexto/guiones.md`): carpeta **Guiones** montada (5 nov). La tarea de las 4:35 p. m. deja la idea y el
   guion en frío y avisa; luego se revisa juntos y se mueve a terminados. Recursos y reglas de TikTok, YouTube y Meta:
   creados (5 nov, Kit ContentIA: `contexto/kit-contentia.md`), falta revisarlos juntos. Falta organizar TikTok.
3b. Repartir el Cerebro a clientes sin que lo compartan: plan aprobado (`contexto/licencias.md`), se monta AL FINAL.
4. Del plan AI Work: nombre de las redes y bio, clase gratis, módulos, plantilla del cerebro, CRM.
