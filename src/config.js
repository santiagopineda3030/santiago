/* =========================================================================
   CONFIGURACIÓN — todo lo que tienes que cambiar está en este archivo.
   ========================================================================= */

/* URL de tu Google Apps Script (termina en /exec).
   Paso a paso en README.md → "Conectar el formulario con Google Sheets". */
export const APPS_SCRIPT_URL = ''

/* <!-- VIDEO_CLASE -->
   Link de "insertar" (embed) del video principal. Ejemplos:
   YouTube: 'https://www.youtube.com/embed/TU_ID_DE_VIDEO?rel=0&modestbranding=1'
   Vimeo:   'https://player.vimeo.com/video/TU_ID_DE_VIDEO?dnt=1'
   Déjalo vacío ('') y se mostrará el espacio reservado. */
export const VIDEO_CLASE_URL = ''

/* <!-- VIDEO_CORTO -->
   Segundo video (por ejemplo, el "antes y después" del sistema). */
export const VIDEO_CORTO_URL = ''
/* Formato del video corto: '16:9' (horizontal) o '9:16' (vertical tipo Reel) */
export const VIDEO_CORTO_FORMATO = '16:9'

/* <!-- CALENDARIO -->
   Link de tu agenda. Funciona con Calendly, Google Calendar (citas), Cal.com, etc.
   Calendly:        'https://calendly.com/TU_USUARIO/llamada?hide_gdpr_banner=1&background_color=141414&text_color=f5f5f5&primary_color=e02020'
   Google Calendar: 'https://calendar.google.com/calendar/appointments/schedules/TU_ID?gv=true'
   Cal.com:         'https://cal.com/TU_USUARIO/llamada?embed=true&theme=dark' */
export const CALENDARIO_URL = ''

/* TEXTO: datos de contacto del footer */
export const WHATSAPP_NUMERO = '570000000000' // con código de país, sin + ni espacios (ej: 573001234567)
export const WHATSAPP_MENSAJE = 'Hola Santiago, vi la clase gratuita y tengo una pregunta.'
export const INSTAGRAM_URL = 'https://instagram.com/TU_USUARIO'
export const INSTAGRAM_USUARIO = '@tu_usuario'

/* TEXTO: nombres de la marca y del programa */
export const MARCA = 'Santiago'
export const MARCA_LEMA = 'Aprende IA y automatiza tus redes'
export const PROGRAMA = 'Redes Automatizadas 1 a 1'

export const whatsappLink = (mensaje = WHATSAPP_MENSAJE) =>
  `https://wa.me/${WHATSAPP_NUMERO}?text=${encodeURIComponent(mensaje)}`
