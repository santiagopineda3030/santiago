/* =========================================================================
   TEXTOS DE LA PÁGINA
   Cambia aquí cualquier texto: se actualiza en toda la página.
   Las URLs privadas (Google Sheet y calendario) van en el archivo .env
   ========================================================================= */

export const marca = 'Santiago'

export const hero = {
  /* Línea técnica encima del titular (se "decodifica" al cargar) */
  etiqueta: 'IA · Automatización · Redes',
  titular: 'Automatiza tus redes sociales con IA',
  resaltado: 'IA', // palabra del titular que va en cian (déjala vacía para no resaltar)
  subtitulo: 'Mira este video y agenda tu llamada',
}

export const video = {
  /* VIDEO_INTRO: link de "insertar" (embed) de tu video.
     YouTube: 'https://www.youtube.com/embed/TU_ID'
     Vimeo:   'https://player.vimeo.com/video/TU_ID'
     Si lo dejas vacío se muestra el espacio con el botón de play. */
  url: '',
  titulo: 'Video de introducción',
  /* Imagen de portada opcional (súbela a /public, ej: '/portada.jpg').
     Si usas YouTube y la dejas vacía, se usa la miniatura del video. */
  portada: '',
  textoSinVideo: 'Video de introducción',
  /* Textos de la barra técnica debajo del video */
  archivo: 'intro.mp4',
  detalle: 'HD · 16:9',
}

export const ctaPrincipal = 'Agendar mi llamada'
export const ctaFijoMovil = 'Agendar llamada'

export const agenda = {
  etiqueta: 'Paso final · Agenda',
  titulo: 'Agenda tu llamada de 10 minutos',
  intro: 'Completa tus datos y elige el horario que mejor te quede.',

  campos: {
    nombre: { label: 'Nombre', placeholder: 'Tu nombre' },
    whatsapp: { label: 'WhatsApp', placeholder: '+57 300 123 4567', ayuda: 'Con código de país.' },
    correo: { label: 'Correo', placeholder: 'tu@correo.com' },
    negocio: { label: '¿Qué negocio o marca tienes?', placeholder: 'Ej: tienda de ropa, consultorio, marca personal' },
    redes: { label: '¿En qué redes publicas hoy?', opciones: ['Instagram', 'TikTok', 'YouTube', 'Facebook'] },
    inversion: {
      label: '¿Estás en posición de invertir en un acompañamiento personalizado?',
      opciones: ['Sí', 'No', 'Necesito más información'],
    },
  },

  errores: {
    nombre: 'Escribe tu nombre.',
    whatsapp: 'Escribe un número de WhatsApp válido, con código de país.',
    correo: 'Escribe un correo válido, por ejemplo nombre@correo.com.',
    negocio: 'Cuéntanos qué negocio o marca tienes.',
    redes: 'Elige al menos una red.',
    inversion: 'Elige una opción.',
    resumen: 'Revisa los campos marcados.',
    envio: 'No pudimos enviar tus datos. Revisa tu conexión e inténtalo de nuevo.',
  },

  boton: 'Enviar y elegir horario',
  enviando: 'Enviando…',
  privacidad: 'Usamos tus datos solo para contactarte sobre la llamada.',

  exito: {
    titulo: (nombre) => (nombre ? `Listo, ${nombre}. Elige tu horario` : 'Listo. Elige tu horario'),
    texto: 'Reserva el espacio que mejor te quede. Te llegará la confirmación a tu correo.',
    sinCalendario: 'Aquí aparecerá tu calendario',
  },
}

export const footer = {
  instagram: { texto: 'Instagram', url: 'https://instagram.com/TU_USUARIO' },
  /* WhatsApp: número con código de país, sin + ni espacios (ej: 573001234567) */
  whatsapp: { texto: 'WhatsApp', numero: '[NÚMERO]', mensaje: 'Hola Santiago, vi tu video y tengo una pregunta.' },
  lema: 'Aprende IA y automatiza tus redes',
  estado: 'Sistema activo',
}
