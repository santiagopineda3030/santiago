/**
 * Crea la encuesta "Tu negocio y las redes" en Google Forms (una sola vez).
 * Cómo usarlo: script.google.com › Nuevo proyecto › pega esto › Ejecutar › crearEncuesta › acepta permisos.
 * Al final, en "Registro de ejecución" salen el link para compartir y el link para editar.
 */
function crearEncuesta() {
  const f = FormApp.create('Tu negocio y las redes · 2 minutos');
  f.setDescription('Gracias por ayudarme. Son 9 preguntas cortas sobre cómo manejas hoy el contenido de tu negocio. ' +
    'No vendo nada en esta encuesta: es para entender mejor a los dueños de negocio. — Santi');
  f.setCollectEmail(false).setProgressBar(true);

  f.addListItem().setTitle('¿Qué tipo de negocio tienes?').setRequired(true).setChoiceValues([
    'Servicios profesionales (abogado, contador, consultor…)', 'Salud o estética', 'Restaurante o comida',
    'Tienda física u online', 'Inmobiliaria', 'Coach, formador o creador', 'Otro']);
  f.addMultipleChoiceItem().setTitle('¿En qué país está tu negocio?').setRequired(true)
    .setChoiceValues(['Colombia', 'México', 'España', 'Estados Unidos', 'Otro país de habla hispana']);
  f.addMultipleChoiceItem().setTitle('¿Cada cuánto publicas hoy en redes?').setRequired(true).setChoiceValues([
    'Casi todos los días', '1 a 3 veces por semana', 'Unas pocas veces al mes', 'Casi nunca o nunca']);
  f.addMultipleChoiceItem().setTitle('¿Quién hace hoy tu contenido (grabar, editar, publicar)?').setRequired(true)
    .setChoiceValues(['Yo mismo', 'Alguien de mi equipo', 'Un editor o community manager freelance', 'Una agencia', 'Nadie']);
  f.addCheckboxItem().setTitle('¿Qué es lo que más te frena con las redes? (puedes marcar varias)').setRequired(true)
    .setChoiceValues(['No sé qué publicar', 'No tengo tiempo', 'Publico pero no me compran', 'No llego a la gente correcta',
      'Me da pena salir en cámara', 'Editar es difícil o lento', 'Lo que pago no da resultados']).showOtherOption(true);
  f.addMultipleChoiceItem().setTitle('¿Cuánto inviertes al mes en contenido o redes (personas, agencia, herramientas)?')
    .setRequired(true).setChoiceValues(['Nada', 'Menos de 500.000 COP (unos 125 USD)', 'Entre 500.000 y 2 millones COP',
      'Entre 2 y 4 millones COP', 'Más de 4 millones COP']);
  f.addMultipleChoiceItem().setTitle('¿Usas inteligencia artificial (ChatGPT u otra) en tu negocio?').setRequired(true)
    .setChoiceValues(['Sí, todos los días', 'A veces', 'La probé pero no la uso', 'No, nunca']);
  f.addScaleItem().setTitle('Si alguien te dejara un sistema que crea, edita y publica tus videos con tu voz, ¿qué tan útil sería?')
    .setBounds(1, 5).setLabels('Nada útil', 'Lo necesito ya').setRequired(true);
  f.addParagraphTextItem().setTitle('En tus palabras: ¿qué es lo más frustrante de tener redes para tu negocio?').setRequired(false);
  f.addTextItem().setTitle('Si quieres que te cuente los resultados, deja tu WhatsApp (opcional)').setRequired(false);

  console.log('Link para compartir: ' + f.getPublishedUrl());
  console.log('Link para editar: ' + f.getEditUrl());
}
