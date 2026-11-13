# Referentes de edición (los lee el robot de edición antes de editar)
Videos en `referentes/` (repo). Por tipo de video de la Agenda. Copiar el ESTILO, no el contenido.

## Explicativo (E)
### ref1 · `referentes/explicativo-ref1.mp4` (19 s, vertical) · hoja de cuadros `explicativo-ref1-cuadros.jpg`
- **Plano:** cara al frente, cuarto oscuro con luces cálidas desenfocadas atrás (bokeh). Ropa oscura lisa.
- **Ritmo:** corte o cambio de zoom cada ~1 s. Alterna plano medio ↔ primer plano (punch-in) en la misma toma.
- **Subtítulos:** 1–3 palabras, blancos, letra limpia sin caja, centrados a la altura del pecho (~60 % de alto). La palabra clave va de color (ej. "Claude" en naranja).
- **Efectos:** un tramo corto en blanco y negro para marcar un giro (ya lo tenemos: `"bn": true`). Al inicio, captura de una pantalla flotando arriba.
- **Gráficos:** fotos tipo tarjeta (esquinas redondeadas, algo inclinadas) que aparecen flotando alrededor de la cara cuando nombra ejemplos ("como estos"); fila de logos/íconos bajo el subtítulo cuando dice una categoría ("Inteligencia Artificial"), con el fondo oscurecido; logo animado (asterisco de Claude) bajo el subtítulo al nombrar la marca.
- **Regla ContentIA:** en nuestros videos no mostrar la configuración ni las herramientas por dentro; los logos solo como ilustración.


> **12 nov · E1 (Santi):** los explicativos con escenas (varias personas) van **muy fluidos, sin animaciones**: subtítulos de un color por persona (Santi blanco, la otra persona amarillo), efectos de sonido en cada transición (`--fluido --sfx-cortes whoosh`). Detalle: `editor-noticias/README.md` › "Videos con escenas y varias personas".

## Noticias (v)
### ref1 · `referentes/noticias-ref1.mp4` (15,6 s, solo animación, sin cara) · `noticias-ref1-cuadros.jpg`
Sirve para las **escenas animadas** que tapan o acompañan cada noticia (no para el plano de Santi).
- **Fondo:** negro con resplandor rojo suave en el centro (viñeta). Todo con brillo/glow.
- **Títulos arriba:** 2 líneas: palabra corta en sans negrita blanca ("Encuentra") + frase grande en serif itálica con subrayado rojo ("cada momento"). Aparecen palabra por palabra con fundido.
- **Tarjetas de pantalla:** capturas en tarjetas redondeadas con sombra/glow, que entran y se agrandan (zoom suave).
- **Línea neón:** onda roja tipo neón que cruza la pantalla con nodos numerados 1, 2, 3 (para listas o pasos); el número activo se ilumina.
- **Cifras:** contador animado que sube (765 → 3.055) con ícono al lado.
- **Íconos:** dentro de círculos con borde fino; logos con glow (asterisco naranja).
- **Diagrama:** un nodo que se abre en varias líneas hacia una lista (1 → muchos).
- **Cuadrícula:** cuadritos que se llenan uno a uno para mostrar cantidad.
- **Ritmo:** cada idea 2–3 s, transiciones suaves (fundidos y zooms), nada de cortes bruscos en las animaciones.

### ref2 · `referentes/noticias-ref2.mp4` (27,7 s, vertical, con cara) · `noticias-ref2-cuadros.jpg` · aprobado por Santi 13 nov (v9 en adelante)
Formato completo del video de noticias (plano de Santi + animaciones). **En ROJO, no en verde** (Santi, 13 nov).
- **Título grande arriba** en mayúsculas con brillo neón, entra palabra por palabra (gancho).
- **Subtítulos 2 pisos:** primera parte chica en blanco + palabra clave abajo, grande, negrita y con glow (rojo).
- **Tarjetas animadas** (esquinas redondas, fondo oscuro) que se llenan paso a paso: barra de progreso con íconos, velocímetro que cae a rojo, lista que se marca con ✓/✗.
- **Blanco y negro** en las frases de reflexión o dolor (solo esa frase).
- **Destello de luz cálida** como transición entre partes.
- **Pantallas completas sin la cara:** fondo oscuro con objeto 3D (globo, billetes, servidores) o fondo claro con logos que entran uno a uno en tarjetas blancas.
- **Palabra negativa en rojo fuerte** en los contrastes.
- Foto de perfil fija en una esquina.
- **Qué NO copiar:** el verde, el voseo, el contenido. Traducir a la marca: acento rojo, CTA de la marca, mostrar resultados y no herramientas.

## Lead (L)
### ref1 · `referentes/lead-ref1.mp4` (15 s, vertical) · `lead-ref1-cuadros.jpg`
- **Gancho:** pregunta en una píldora negra redondeada arriba ("¿Qué es GitHub?"), palabra clave en amarillo; debajo aparecen chips pequeños con el contexto ("para ser analista de datos", "2027" en amarillo).
- **Pantalla dividida:** mitad de arriba negra con la animación de la idea; mitad de abajo la cara hablando. Alterna con plano completo de la cara.
- **Animación de arriba:** palabra grande en sans muy negrita (amarilla o blanca) que aparece palabra por palabra; la palabra clave con **resaltador amarillo** detrás ("del código", "Limpias", "Nadie"); íconos de línea fina (carpeta, archivo, laptop, barras); mini maquetas que se escriben solas (tabla, código, nombre de archivo).
- **Transición:** destello naranja/amarillo a pantalla completa para cambiar de parte.
- **Subtítulos:** muy pequeños, con la palabra clave en amarillo.
- **Ritmo:** una idea cada 1–2 s; frases cortas que se arman en pantalla mientras las dice.
- Para ContentIA: misma estructura (pregunta arriba + idea animada + cara), con nuestros colores (cian) o amarillo si Santi lo pide.

## Clip cascada (C) · clips de YouTube largo o de sesiones de clase
### ref1 · `referentes/clip-ref1.mp4` (8,7 s, vertical) · `clip-ref1-cuadros.jpg`
Es exactamente el estilo que produce el kit de Juanita (`kit-cascada/editor/render/overlay.html`): usarlo tal cual, con colores de ContentIA.
- **Fondo:** la misma toma muy desenfocada llenando la pantalla vertical.
- **Arriba, fijo todo el video:** etiqueta en píldora pequeña ("CLASE EN VIVO · WORK IN TECH" → para nosotros "CEREBRO DE CONTENIDO · CONTENTIA") + gancho de 2 líneas en blanco con la parte clave en color ("no sale en rojo").
- **Centro:** la presentación/pantalla en una tarjeta redondeada (con el cursor visible); debajo, la cámara en otra tarjeta más pequeña.
- **Tarjeta de idea:** recuadro con borde verde y check ("✓ CONSULTA EJECUTADA · …pero eso no significa que responda bien") que aparece cuando lo dice.
- **Subtítulos:** 2–3 palabras abajo, blancos con la palabra clave en amarillo.
- Si no hay pantalla compartida (YouTube largo con solo cara): cámara en la tarjeta grande y tarjetas de idea encima.

## YouTube largo (Y)
### ref1 · `referentes/youtube-largo-ref1.mp4` (25 s, 16:9) · `youtube-largo-ref1-cuadros.jpg`
- **Plano principal:** sentado, plano abierto que muestra el lugar (se ve el espacio, no solo la cara). Corte a plano más cerrado para frases importantes. Color cálido y cinematográfico.
- **Título detrás de la persona:** texto gigante en negrita ("TODA MI HISTORIA", rojo + blanco) puesto DETRÁS del cuerpo (efecto profundidad: la persona tapa parte de las letras). Se usa para el título del video o de cada capítulo.
- **Subtítulos:** frases de 4–6 palabras en itálica blanca, centradas abajo, con la palabra clave en negrita ("real", "fin", "camino"); entran con fundido.
- **B-roll entre frases:** clips tipo vlog cámara en mano (a veces en blanco y negro), fotos de archivo reveladas con una **lupa** que pasa por encima, collage de fotos sobre fondo rojo oscuro, clips emotivos. Cada inserto 1–3 s.
- **Ritmo:** pausado comparado con los verticales: plano principal largo + insertos que ilustran lo que dice.
- Para ContentIA (Y1 "Cómo publico todos los días sin editar"): título detrás de Santi con cian + blanco; b-roll de grabando, del calendario lleno, de notificaciones de "publicado" (sin mostrar herramientas por dentro).
