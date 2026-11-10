---
name: cascada
description: Cascada de contenidos desde clases o sesiones grabadas en Google Meet. Úsalo para instalar el sistema por primera vez (entrevista de reglas, dependencias, ingesta de Meet a Drive y hoja), para sacar los clips de una sesión nueva (documento de cascada + filas en la hoja) o para editar esos clips como reels verticales con subtítulos y animaciones. Triggers: "instalar la cascada", "configurar mis reglas", "procesa la sesión", "saca los clips", "edita el reel", "cascada de contenido".
---

# Cascada de contenidos

De cada sesión grabada salen **pocos clips muy buenos** (no muchos), cada uno con indicaciones de edición, y
—si la persona quiere— el reel ya editado. Todo se gobierna con `reglas.json` en la raíz del kit: nada de la
marca está escrito en el código.

Hay tres modos. Identifica cuál pide la persona; si `reglas.json` no existe, empieza siempre por **A**.

Reglas de conversación (valen en los tres modos):
- Habla en el idioma de la persona, con frases cortas. Explica el **por qué** de cada paso en una línea.
- Pasos cortos y numerados. No pidas pantallazos: pregunta "¿listo?" o "¿qué te salió?".
- Lo que la persona deba pegar (código, textos) déjalo en el portapapeles (`pbcopy` en Mac con `LANG=en_US.UTF-8`,
  `clip` en Windows) y dile solo dónde pegarlo.
- Nunca pidas contraseñas ni llaves por chat. Si algo necesita credenciales, la persona las pone ella misma.
- Nunca inventes: si no está en la transcripción, no va.

---

## A. Instalar (primera vez)

### A1. Entrevista de reglas
Pregunta en **bloques de 3–4 preguntas** (no todo de una). Muestra entre paréntesis el ejemplo de
`reglas.ejemplo.json` para que la persona tenga una referencia, y acepta "usa el ejemplo".

1. **Marca:** nombre, etiqueta que va arriba del gancho ("CLASE EN VIVO · TU MARCA"), colores (fondo, acento,
   texto; en hex o "como mi logo" → pide el logo o la web y propón la paleta), fuente si tiene.
2. **Grabaciones:** ¿se graban en Google Meet? ¿Qué palabras trae siempre el título del evento? ¿Quién es el
   organizador o coanfitrión (esa cuenta recibe los archivos)? ¿Activan la transcripción? Idioma y zona horaria.
   Si no usan Meet, el kit sirve igual: los videos se dejan a mano en la carpeta y Claude transcribe con whisper
   (salta A3 y en B usa `editor/preparar_tramo.py` sobre el video completo para tener la transcripción).
3. **Quién presenta** (la voz que sale en los clips) y si usa **fondo virtual fijo** (eso permite detectar solo
   cuándo sale un alumno para difuminarlo).
4. **Clips:** cuántos por sesión (sugerir 3) y de qué tipos. Propón los del ejemplo (Explicación / Respuesta /
   Criterio) y pide que los adapte a su tema. Duración (sugerir 35–45 s). Qué priorizar y qué evitar.
5. **Alumnos y privacidad:** ¿puede salir la voz de un alumno (distorsionada) o solo como texto? ¿Difuminar caras?
   Nunca nombres.
6. **Diseño:** gancho fijo arriba todo el video (sí/no), presentación arriba y cámara abajo cuando comparte
   pantalla, tarjetas de idea, palabras por subtítulo. Explica la **zona segura de Instagram** (x 120–960,
   y 250–1500): todo el texto vive ahí.
7. **Cierre y llamado a la acción:** qué dice el final (ej. "cómo se ve esto en tu trabajo") y el CTA exacto
   (ej. "Comenta X y te cuento cómo empezar"). Palabras prohibidas y su reemplazo.
8. **Descripción de Instagram:** plantilla y 5 hashtags.
9. **Ideas largas** (YouTube u otro): ¿quiere 4–6 ideas por sesión además de los clips? ¿Con qué tipos?
10. **Edición:** `automatica` (Claude arma el reel con el editor del kit), `editor` (solo el documento para un
    editor humano) o `ambas`.

Con las respuestas, escribe `reglas.json` con **la misma estructura** de `reglas.ejemplo.json`. Muéstrale un
resumen de 8–10 líneas y pide confirmación. Las reglas se pueden cambiar después: basta con pedirlo.

### A2. Dependencias (solo si `edicion` es `automatica` o `ambas`)
Revisa qué hay antes de instalar (`ffmpeg -version`, `python3 --version`, `node --version`, Google Chrome).
Instala solo lo que falte, explicando cada cosa en una línea:
- **ffmpeg** (corta y compone el video): Mac `brew install ffmpeg`; Windows `winget install Gyan.FFmpeg`.
- **Python 3.9+** y un entorno propio: `python3 -m venv .venv` y `.venv/bin/pip install -r requirements.txt`
  (Windows: `.venv\Scripts\pip`). Trae faster-whisper (transcribe con tiempos por palabra) y OpenCV (encuentra caras).
- **Node 18+** y `npm install` dentro de `editor/render` (dibuja las animaciones con Chrome).
- **Google Chrome** instalado. Si está en una ruta rara, `CHROME_PATH`.
- **Google Drive para escritorio** con la cuenta que recibe las grabaciones, para que los videos se lean como
  archivos locales. Anota en `reglas.json › grabaciones.carpeta_local` la ruta de la carpeta de grabaciones.

El código y el `.venv` viven en una carpeta normal del computador, **no dentro de Drive** (Drive daña los entornos
de Python y de Node al sincronizar miles de archivos pequeños).

### A3. Ingesta de Meet → Drive → hoja
Explica: Meet guarda el video y la transcripción en "Meet Recordings" del organizador; un Apps Script los copia
cada 30 min a una carpeta por sesión y pasa el texto a una hoja. Así Claude nunca tiene que buscar archivos.
1. Copia `ingesta/Code.gs` al portapapeles, con las 4 constantes de arriba ya cambiadas según `reglas.json`
   (`PATRON`, `CARPETA`, `HOJA_NOMBRE`, `TZ`).
2. Pasos para la persona: abrir script.google.com con la cuenta que recibe las grabaciones → Nuevo proyecto →
   pegar → guardar → elegir `instalar` → Ejecutar → aceptar permisos (explica que son para leer sus grabaciones
   y escribir en su hoja).
3. Pídele el link de la hoja que aparece en el registro de ejecución y guárdalo en `reglas.json › grabaciones.hoja_id`.
4. Recuérdale: la grabación necesita un plan de Google Workspace que permita grabar, y la transcripción se activa
   en cada reunión (o por defecto en la configuración de Meet).

### A4. Prueba
Con la primera sesión que quede `Por analizar` (o un video de prueba), corre el modo **B** y, si aplica, **C** con
un solo clip. Revisa el resultado con la persona y ajusta `reglas.json` con lo que pida. Ofrece programarlo para que
corra solo (una tarea programada que haga B y C después de cada sesión).

---

## B. Procesar una sesión (clips + documento)

1. Lee `reglas.json`. Con el conector de Google Sheets lee `SESIONES` de la hoja (`grabaciones.hoja_id`) y toma las
   filas `Por analizar`. Para cada una lee sus filas de `TRANSCRIPCIONES` (en orden de `parte`).
2. Si hay menos de ~2 minutos de conversación real, márcala `Sin contenido` y sigue.
3. Escoge exactamente `clips.por_sesion` clips, uno por cada tipo de `clips.tipos`, de 40–70 s de material
   (el reel final queda en `clips.duracion_seg`). Prioriza `clips.priorizar`, descarta `clips.evitar`.
   Reglas de cada clip:
   - Habla quien presenta (`grabaciones.presenta`). La pregunta de un alumno sigue `voces.pregunta_alumno`.
     Nunca el nombre de un alumno: si quien presenta lo dice, se corta antes.
   - Minutos exactos de la transcripción, con inicio y fin. Si hay una cifra dudosa o una frase que la persona
     misma corrige después, márcalo como **No usar** con su minuto.
4. Escribe el documento con la estructura de `plantillas/cascada-sesion.md` (mira `plantillas/cascada-ejemplo-wit.md`
   para el nivel de detalle): por clip **Corte, No usar, Gancho 0–3 s, Edición, Copy ≤ 125 caracteres**; las
   indicaciones generales para el editor; y, si `ideas_largas.activo`, las ideas largas.
   Respeta `prohibido` en todo texto público.
5. Súbelo como Google Doc en la carpeta de la sesión (conector de Drive, `text/markdown`) con el título
   `Cascada · Sesión AAAA-MM-DD`, y pon su link en `SESIONES › doc_cascada`.
6. Agrega una fila por clip en `CASCADA`: `sesion | pieza (Reel 1..n) | categoria (tipo) | titulo | minutos | doc |
   estado = Por editar | entregado (vacío) | video_sesion (link del video) | descripcion (de la plantilla de
   reglas.json) | link_publicado (vacío)`. Textos que empiecen por `=`, `+` o `-` llevan apóstrofo delante.
7. Marca la sesión `Cascada lista` y dile a la persona: link del documento y los títulos de los clips.

---

## C. Editar los reels (si `edicion` es `automatica` o `ambas`)

Para cada fila `Por editar` de `CASCADA`:
1. **Video:** busca el archivo de video de la sesión en `grabaciones.carpeta_local` (en Drive para escritorio
   puede no tener extensión; si hay varios, el más pesado). ffmpeg lo lee directo. Si no está, dilo y para.
2. **Preparar el tramo** (15 s de margen antes y después de los minutos):
   `.venv/bin/python editor/preparar_tramo.py "<video>" <inicio> <fin> trabajo/AAAA-MM-DD_C<n>`.
   Deja `base.json` (encuadre de cámara, presentación y colores del fondo), `camara.png`, `presentacion.png` y la
   transcripción con tiempos. **Mira las dos imágenes**: la cara debe verse y la diapositiva sin la barra del
   navegador. Si el diseño de Meet es otro, ajusta `camara` / `presentacion` a mano.
3. **Spec** `specs/AAAA-MM-DD_C<n>_<tema>.json`: parte de `base.json` y sigue `plantillas/spec-ejemplo.json`:
   - `tramos`: solo frases de quien presenta, cortando en silencios (fin de una palabra → inicio de la siguiente),
     nunca a mitad de palabra; quita rodeos y frases corregidas. Cada tramo se entiende solo.
   - `alumno`: índices de los tramos donde habla un alumno (voz distorsionada, cara difuminada, nota de privacidad).
   - `escenas`: `hook` con `"fixed": true` y `"end": 999` si `diseno.gancho_fijo` (≤ `gancho_max_palabras`, con
     `<em>` en la parte clave); una `card` por idea sincronizada con cuando se dice (`ok` verde, `alt` coral);
     `end` sobre el último tramo con `cierre.texto` y `cta` = `cierre.cta`.
   - `correcciones`: lo que whisper oyó mal (clave = `start` exacto de la palabra; `""` la quita).
   - `clave`: 6–12 palabras que se resaltan con el color de acento.
   - `salida`: `salidas/AAAA-MM-DD_C<n>_<tema>.mp4`.
4. **Armar:** `.venv/bin/python editor/armar_reel.py specs/<spec>.json` (≈ 1–2 min). Si imprime "alumno en
   cámara", quedó difuminado.
5. **Revisar** con una hoja de contacto (`ffmpeg -i <reel> -vf "select='not(mod(n,96))',scale=270:-1,tile=7x1"
   -frames:v 1 hoja.png`) y mírala: que las tarjetas no tapen la cara, que nada se salga de la zona segura, que los
   subtítulos no partan palabras raras y que el cierre se lea completo. Corrige y vuelve a armar si hace falta.
6. **Entregar:** copia el mp4 a `<carpeta de la sesión>/Reels/` dentro de `grabaciones.carpeta_local` (Drive lo
   sube solo). En `CASCADA`: `estado = Borrador IA` y `entregado` = link del archivo en Drive (búscalo por nombre
   con el conector cuando haya sincronizado). La persona revisa, ajusta la descripción y publica.

Cuando la persona pida un cambio de diseño o de criterio ("el gancho más corto", "nunca uses X"), cámbialo en
`reglas.json` (o en `editor/render/overlay.html` si es visual) para que valga en todos los reels siguientes, y díselo.
