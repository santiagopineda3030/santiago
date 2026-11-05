/**
 * Subidas.gs · Buzón para que Claude suba los videos editados a Drive.
 *
 * Va en el MISMO proyecto de Apps Script de la hoja "Plan contenido orgánico - ContentIA"
 * (Extensiones › Apps Script › + › Script › "Subidas"), y se publica como aplicación web.
 *
 * Qué hace: cuando Claude termina de editar, le pide a este buzón un permiso de subida
 * para UN video. El buzón revisa la clave, el nombre ("v7 1.0 tema.mp4") y el tamaño
 * (máx. 30 MB), y abre la subida SOLO dentro de "4. Contenido editado/<MES AAAA>".
 * El video lo sube Claude directo a Google Drive; nadie recibe tu sesión ni tu contraseña.
 *
 * Instalar (una vez):
 *  1. Pegar este archivo en el proyecto de la hoja.
 *  2. ⚙️ Configuración del proyecto › Propiedades del script › Agregar:
 *       CLAVE_SUBIDA = una clave larga que inventes (ej. 30 letras y números).
 *  3. Implementar › Nueva implementación › ⚙️ Aplicación web
 *       Ejecutar como: Yo · Quién tiene acceso: Cualquier persona › Implementar › Autorizar.
 *  4. Copiar la URL de la aplicación web (termina en /exec).
 */
const SUBIDAS = {
  CARPETA_EDITADOS: '1A1zlwXyvR-l2CZcJ6dnHUp-SZXnEcUGT', // Edición de videos › 2. Videos terminados (antes Instagram › 4. Contenido editado)
  MAX_MB: 30,
};

function doPost(e) {
  const responder = obj => ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
  try {
    const p = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const clave = PropertiesService.getScriptProperties().getProperty('CLAVE_SUBIDA');
    if (!clave || clave.length < 16 || p.clave !== clave) return responder({ ok: false, error: 'Clave incorrecta' });
    const nombre = String(p.nombre || '');
    if (!/^v\d+ \d+\.\d+ [^\/\\]+\.mp4$/i.test(nombre)) {
      return responder({ ok: false, error: 'Nombre inválido: debe ser "v7 1.0 tema.mp4"' });
    }
    const bytes = Number(p.tamano);
    if (!(bytes > 0) || bytes > SUBIDAS.MAX_MB * 1048576) {
      return responder({ ok: false, error: 'Tamaño inválido (máximo ' + SUBIDAS.MAX_MB + ' MB)' });
    }
    const carpeta = carpetaDelMes_(p.mes);
    const r = UrlFetchApp.fetch(
      'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,name,webViewLink', {
        method: 'post',
        contentType: 'application/json; charset=UTF-8',
        muteHttpExceptions: true,
        headers: {
          Authorization: 'Bearer ' + ScriptApp.getOAuthToken(),
          'X-Upload-Content-Type': 'video/mp4',
          'X-Upload-Content-Length': String(bytes),
        },
        payload: JSON.stringify({ name: nombre, parents: [carpeta.getId()], mimeType: 'video/mp4' }),
      });
    if (r.getResponseCode() !== 200) {
      return responder({ ok: false, error: 'Drive ' + r.getResponseCode() + ': ' + r.getContentText().slice(0, 200) });
    }
    const h = r.getHeaders();
    return responder({ ok: true, subida: h.Location || h.location, carpeta: carpeta.getName() });
  } catch (err) {
    return responder({ ok: false, error: String(err && err.message || err) });
  }
}

/** Subcarpeta del mes ("NOVIEMBRE 2026") dentro de editados; la crea si no existe. */
function carpetaDelMes_(mes) {
  const MESES = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE',
    'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'];
  const hoy = new Date();
  const nombre = /^[A-ZÁÉÍÓÚ]+ \d{4}$/.test(String(mes || '')) ? mes : MESES[hoy.getMonth()] + ' ' + hoy.getFullYear();
  const base = DriveApp.getFolderById(SUBIDAS.CARPETA_EDITADOS);
  const it = base.getFoldersByName(nombre);
  return it.hasNext() ? it.next() : base.createFolder(nombre);
}
