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
