# Santiago · AI Work — memoria del proyecto

Este archivo lo lee Claude al empezar cada sesión. Es la memoria en la nube (GitHub, rama
`claude/santiago-ia-landing-4q4ef1`, la rama principal del repositorio).

## Cómo usar la memoria (para gastar menos tokens)
- Aquí va solo lo esencial. El detalle está en `contexto/`, y se lee **solo cuando la tarea lo necesita**:
  | Archivo | Cuándo leerlo |
  |---|---|
  | `contexto/bitacora.md` | Para saber qué se hizo y qué quedó a medias |
  | `contexto/instagram-meta.md` | Publicación automática, token, errores de Meta |
  | `contexto/youtube.md` | YouTube Shorts automático: columnas, instalación, riesgo de video privado |
  | `contexto/guion-diario.md` | Tarea de las 5:43 a. m.: guion diario de Noticias IA (pasos, carpetas, hoja) |
  | `contexto/tiktok.md` | TikTok: borrador automático (plan A), app de TikTok, auditoría |
  | `contexto/ai-work.md` | Oferta, embudo, entrega, pendientes del negocio |
  | `contexto/estudio-de-mercado.md` | Textos de venta, guiones de leads |
  | `editor-noticias/README.md` | Editar videos |
- **Al terminar cada tarea:** una línea en `contexto/bitacora.md`, actualizar este archivo si cambió algo
  importante, y commit + push a GitHub. Sin esperar a que lo pida.
- Una sesión nueva por tarea grande: todo queda aquí, no hace falta un chat largo.

## Quién es y cómo hablarle
- **Santiago Pineda** (santiagopineda3030@gmail.com), Colombia, zona horaria **America/Bogota**.
- **Siempre en español**, tuteo, frases cortas y simples. Explicar paso a paso, con capturas si hace falta.
  Muchas veces trabaja desde el **iPad**: dar instrucciones que se puedan seguir ahí.
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
- Guía de edición (Drive, Instagram › 3. Recursos): vertical 1080×1920, 45–75 s, H.264 ≤ 30 MB,
  subtítulos 2–4 palabras con palabras clave en rojo, título por noticia, gancho en los primeros 3 s,
  voz a −14 LUFS. Nombre del archivo: `v<código> <versión> <tema>.mp4` (ej. `v1 1.2 noticias-dia-1.mp4`).

## Dónde está todo (Google Drive › ContentIA)
| Qué | Dónde | ID |
|---|---|---|
| Carpeta raíz | ContentIA | `1LvKFGptavlfPDXzj48OVJZR7Yos2VIFC` |
| Plan de contenido IG (hoja) | Plan contenido orgánico - ContentIA | `1lvs82vX8Pj3rHmVZyUj9cUh6dOm5srjbVDwzvWUyku4` |
| Sistema (Code.gs, Subidas.gs, prompt) | 0. Sistema | `1SlcWLrDd6LfoA_PRwedJ4MeVFIL_0HxL` |
| Guiones IG | Instagram › 1. Guiones | `1uXn5Scfl7lNsCLGJioJxwoFFkGGxv7hX` |
| Crudos IG | Instagram › 2. Crudo sin editar | `1GFl-0CSYI8afA0tzKGa0AVmM7FC-d4ON` |
| Recursos IG (guía de edición) | Instagram › 3. Recursos | `1Hd3rJljSfAr6ehoBet0xeFJIk1Fz84Rn` |
| Editados IG | Instagram › 4. Contenido editado | `1A1zlwXyvR-l2CZcJ6dnHUp-SZXnEcUGT` |
| TikTok / YouTube / Anuncios (Meta) | misma estructura 1–4, vacías | — |

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
- Publicación automática en Instagram: **conectada** (5 nov 2026). IG_ID `17841438740412085`, token en
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

## Pendientes grandes (en orden)
1. Confirmar la primera publicación automática real (Instagram ya conectado e instalado).
2. YouTube Shorts: **funcionando** (canal @santimediayt, probado 5 nov). Sale con la misma aprobación de IG.
   TikTok plan A (borrador + correo): código listo, falta crear la app e instalar (`contexto/tiktok.md`).
3. Guion diario: carpeta `ContentIA › 0. Ideas › Instagram › <MES AAAA> › <AAAA-MM-DD> · Noticias IA` y tarea
   programada 5:43 a. m. que deja guion + fila en la hoja (`contexto/guion-diario.md`). Montado el 5 nov.
3b. Repartir las carpetas a clientes sin que las compartan (token/acceso): por definir con Santiago.
4. Del plan AI Work: nombre de las redes y bio, clase gratis, módulos, plantilla del cerebro, CRM.
