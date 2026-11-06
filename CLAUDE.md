# Santiago · AI Work — memoria del proyecto

Este archivo lo lee Claude al empezar cada sesión. Es la memoria en la nube (GitHub, rama
`claude/santiago-ia-landing-4q4ef1`, la rama principal del repositorio).

## Cómo usar la memoria (para gastar menos tokens)
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
  | `contexto/tiktok.md` | TikTok: borrador automático (plan A), app de TikTok, auditoría |
  | `contexto/licencias.md` | Plan para entregar carpetas a clientes sin que las compartan (se monta al final) |
  | `contexto/ai-work.md` | Oferta, embudo, entrega, pendientes del negocio |
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
| `areas/5-edicion-videos` | `editar-video` | Edita lo de `1. Videos en frío`, revisa con Santi, sube a `2. Videos terminados` y programa |
- **Chats:** `Santi · Base` (`session_01McnvqwgYFW5FkckcrCQLTM`) y `Santi · Preguntas` (`session_01McnvqsAY6qsuVP5J8RGKgS`), fijados arriba a mano; un chat por pieza con etiqueta `area:<red>`.
  - Carpetas (chats al mismo nivel que Base, cada uno se presenta en su primer mensaje): 📁 Instagram
    `session_01Mcnvqs7Mruj2n8hLGHzTTS` · 📁 TikTok `session_01Mcnvqun84DQpBZzc9mkVNF` · 📁 YouTube `session_01McnvqtEmdYchkSMiZkWiyW` ·
    📁 Anuncios (Meta) `session_01McnvqspjmNbL6TY5zg81DQ` · 📁 Guiones `session_01McnvqsoboeaDTB6ormVrbC` · 📁 Edición de videos `session_01McnvqvgdvcfNzme6m5dsJP`.
    (Las creadas desde Base quedaban escondidas dentro de él: archivadas.) Los chats de cada pieza los abre Base.
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
  `Programado` → `Publicado`. Claude nunca pone `Publicar` sin que Santiago lo diga.
- Nunca poner `Publicar` si el video no está en Drive: el script lo marca Error y deja de enlazarlo.
- Descripción: 3–5 líneas, la primera es el gancho, sin datos inventados, emoji solo en el cierre, 5 hashtags.
- COLA POR EDITAR: fila por pieza; al entregar → `Entregado` + link + fecha.
- **Cada video publicado se marca también en Google Calendar** (calendario principal de Santiago):
  título `✅ Publicado · <título original>`, color verde (colorId 10), hora real de publicación,
  y en la descripción las redes, la hora y el link del video en Drive. Sin notificaciones.
- Publicación automática en Instagram: **conectada** (5 nov 2026). **6 nov:** el v2 salió en YouTube pero NO en Instagram
  (la vuelta se pasó de 6 min). Código arreglado: un paso pesado por vuelta (IG primero, YouTube en la siguiente). Falta que
  Santi pegue `Code.gs` y `YouTube.gs` nuevos en Apps Script. IG_ID `17841438740412085`, token en
  Propiedades del script (`META_TOKEN`). Código: `google-apps-script/plan-contenido/Code.gs`. Detalle: `contexto/instagram-meta.md`.

## Herramientas que ya están montadas en este repositorio
- `editor-noticias/`: editor de video propio (ffmpeg + Whisper + animaciones). Flujo que funcionó en v1:
  1. `trozos.py` transcribe cada trozo de voz (detecta tomas repetidas).
  2. Elegir tomas a mano en `edl-*.json` (última toma buena, subtítulos corregidos, gráficos por palabra).
  3. `editar_v2.py` renderiza: cortes por detector de voz, audio sincronizado, animaciones, efectos.
  4. Revisar: transcribir el resultado, buscar silencios (VAD), hojas de cuadros, axe/consola si es web.
- `editor-noticias/subir-drive/`: el **buzón de Apps Script** para que Claude suba videos a Drive solo.
  Necesita en el entorno `SUBIDA_URL` y `SUBIDA_CLAVE`.
- Landing de la llamada: `src/` (React + Vite + Tailwind, estilo tecnológico cian, logo SPR en píxeles).

## Lo próximo (6 nov) · detalle en `contexto/bitacora.md` › Plan del día
1. v2 1.3 a Instagram + YouTube Shorts a las 11:00 (MP4 en 2. Videos terminados; descripción más corta). TikTok no automático.
2. Corrección de TikTok. 3. Estudio de mercado: avatar, oferta y cómo se vende.

## Pendientes grandes (en orden)
1. Confirmar la primera publicación automática real (Instagram ya conectado e instalado).
2. YouTube Shorts: **funcionando** (canal @santimediayt, probado 5 nov). Sale con la misma aprobación de IG.
   TikTok plan A (borrador + correo): código listo, falta crear la app e instalar (`contexto/tiktok.md`).
3. Guiones (`contexto/guiones.md`): carpeta **Guiones** montada (5 nov). La tarea de las 4:35 p. m. deja la idea y el
   guion en frío y avisa; luego se revisa juntos y se mueve a terminados. Recursos y reglas de TikTok, YouTube y Meta:
   creados (5 nov, Kit ContentIA: `contexto/kit-contentia.md`), falta revisarlos juntos. Falta organizar TikTok.
3b. Repartir el Cerebro a clientes sin que lo compartan: plan aprobado (`contexto/licencias.md`), se monta AL FINAL.
4. Del plan AI Work: nombre de las redes y bio, clase gratis, módulos, plantilla del cerebro, CRM.
