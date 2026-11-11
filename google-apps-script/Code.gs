/**
 * Google Apps Script — recibe el formulario de la landing y lo guarda en Google Sheets.
 * Instrucciones paso a paso en README.md → "Conectar el formulario con Google Sheets".
 */

// Nombre de la pestaña donde se guardan los datos (se crea sola si no existe)
const NOMBRE_HOJA = 'Leads';

// Opcional: escribe tu correo para recibir un aviso por cada registro nuevo.
// Déjalo vacío ('') si no quieres avisos.
const CORREO_AVISO = '';

const COLUMNAS = [
  ['fecha', 'Fecha'],
  ['nombre', 'Nombre'],
  ['whatsapp', 'WhatsApp'],
  ['correo', 'Correo'],
  ['negocio', 'Negocio o marca'],
  ['redes', 'Redes donde publica'],
  ['inversion', '¿Puede invertir?'],
  ['origen', 'Origen (UTM)'],
  ['anuncio', 'Anuncio (código)'],   // = utm_content (A1, A2…). Lo usa el Tracker de anuncios
  ['utm_source', 'utm_source'],
  ['utm_medium', 'utm_medium'],
  ['utm_campaign', 'utm_campaign'],
  ['utm_content', 'utm_content'],
  ['fbclid', 'fbclid'],
  // Después vienen columnas que se llenan a mano o las llena el tracker:
  // Agendó · Fecha de la llamada · Asistió · Cerró · Notas
];
// Hoja de leads: "Leads - ContentIA" (Drive › ContentIA › Leads) 1a_GEgOia5tNyVp9rBDv9hyV0K_BSmOMK-vu-s7lGBFE

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const hoja = obtenerHoja_();
    const datos = Object.assign({}, (e && e.parameter) || {});
    datos.fecha = new Date();
    const m = String(datos.utm_content || '').toUpperCase().match(/(?:^|[_\s-])(A\d+)(?=$|[_\s-])/);
    datos.anuncio = m ? m[1] : '';

    const fila = COLUMNAS.map(([clave]) => limpiar_(datos[clave]));
    hoja.appendRow(fila);

    if (CORREO_AVISO) {
      MailApp.sendEmail({
        to: CORREO_AVISO,
        subject: `Nuevo registro: ${datos.nombre || 'sin nombre'} (${datos.inversion || '-'})`,
        body: COLUMNAS.map(([clave, titulo]) => `${titulo}: ${datos[clave] || ''}`).join('\n'),
      });
    }

    return respuesta_({ ok: true });
  } catch (err) {
    return respuesta_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Si abres la URL del script en el navegador verás este mensaje (sirve para probar)
function doGet() {
  return respuesta_({ ok: true, mensaje: 'El script está funcionando.' });
}

function obtenerHoja_() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  let hoja = libro.getSheetByName(NOMBRE_HOJA);
  if (!hoja && String(libro.getSheets()[0].getRange('A1').getValue()) === 'Fecha') hoja = libro.getSheets()[0].setName(NOMBRE_HOJA);
  if (!hoja) hoja = libro.insertSheet(NOMBRE_HOJA);
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(COLUMNAS.map(([, titulo]) => titulo));
    hoja.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold');
    hoja.setFrozenRows(1);
  }
  return hoja;
}

// Evita que un texto como "+57 300..." o "=..." se interprete como fórmula
function limpiar_(valor) {
  if (valor instanceof Date) return valor;
  const texto = String(valor == null ? '' : valor).slice(0, 2000);
  return /^[=+\-@]/.test(texto) ? "'" + texto : texto;
}

function respuesta_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
