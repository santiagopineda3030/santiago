/**
 * TikTok.gs · Manda a TikTok la misma fila que se aprueba para Instagram (plan A: borrador).
 *
 * Va en el MISMO proyecto de Apps Script de la hoja (junto a Code.gs, YouTube.gs y Subidas.gs).
 *
 * Plan A: mientras TikTok no apruebe la app, el video llega a tu TikTok como BORRADOR (notificación en la app)
 * y te llega un correo con la descripción para copiar. Tú solo tocas Publicar. Los borradores vencen en ~24 h.
 * Cuando TikTok apruebe la app, se cambia a publicación directa.
 *
 * Instalar (una vez):
 *  1. Correr probarTikTok › en el Execution log sale la "URL de regreso": pegarla en la app de TikTok
 *     (Login Kit › Redirect URI).
 *  2. ⚙️ Propiedades del script: TIKTOK_CLIENT_KEY y TIKTOK_CLIENT_SECRET (los de la app). Nunca en el chat.
 *  3. En la hoja: menú Plan IG › Conectar TikTok › abrir el link › Autorizar.
 *  4. Plan IG › Probar conexión con TikTok.
 *
 * Columna "TikTok": vacía = va con Instagram · "No" = no subir · "Publicar" = mandarla ya ·
 * el script pone "Subiendo", "En borradores", "Publicado" o "Error". Nunca se reintenta solo.
 */

const TT = {
  ACTIVO: true,                                   // false = apaga TikTok sin tocar Instagram ni YouTube
  CORREO: 'santiagopineda3030@gmail.com',         // a dónde llega el aviso con la descripción para copiar
  API: 'https://open.tiktokapis.com/v2',
  AUTH: 'https://www.tiktok.com/v2/auth/authorize/',
  SCOPES: 'user.info.basic,video.upload',
  ESTADOS: ['Publicar', 'No', 'Subiendo', 'En borradores', 'Publicado', 'Error'],
  COLUMNAS: ['TikTok', 'Link TikTok']
};

/* ---------- Columnas ---------- */

function prepararTikTok_() {
  planes_().forEach(f => {
    const h = encabezados_(f.sh), n = f.sh.getMaxRows() - 1;
    TT.COLUMNAS.forEach(nombre => {
      if (h[norm_(nombre)]) return;
      const c = f.sh.getLastColumn() + 1;
      if (c > f.sh.getMaxColumns()) f.sh.insertColumnAfter(f.sh.getMaxColumns());
      f.sh.getRange(1, c).setValue(nombre).setFontWeight('bold').setBackground('#1f2937').setFontColor('#ffffff');
      f.sh.setColumnWidth(c, nombre === 'TikTok' ? 120 : 240);
      if (nombre === 'TikTok') {
        f.sh.getRange(2, c, n).setDataValidation(SpreadsheetApp.newDataValidation()
          .requireValueInList(TT.ESTADOS, true).setAllowInvalid(true).build());
        f.sh.getRange(1, c).setNote('Vacía = va a TikTok junto con Instagram (llega como borrador). "No" = no subir. ' +
          '"Publicar" = mandarla ya. Cuando la publiques en la app, el script la pasa a "Publicado".');
      }
      h[norm_(nombre)] = c;
    });
  });
}

/* ---------- Conexión (OAuth) ---------- */

const ttProp_ = k => String(PropertiesService.getScriptProperties().getProperty(k) || '').trim();
const ttRegreso_ = () => 'https://script.google.com/macros/d/' + ScriptApp.getScriptId() + '/usercallback';

/** Desde el menú de la hoja: abre el link para autorizar la cuenta de TikTok. */
function conectarTikTok() {
  const key = ttProp_('TIKTOK_CLIENT_KEY');
  if (!key || !ttProp_('TIKTOK_CLIENT_SECRET')) throw new Error('Faltan TIKTOK_CLIENT_KEY y TIKTOK_CLIENT_SECRET en Propiedades del script');
  const state = ScriptApp.newStateToken().withMethod('tiktokVolver').withTimeout(600).createToken();
  const url = TT.AUTH + '?client_key=' + encodeURIComponent(key) + '&scope=' + encodeURIComponent(TT.SCOPES) +
    '&response_type=code&redirect_uri=' + encodeURIComponent(ttRegreso_()) + '&state=' + encodeURIComponent(state);
  console.log('Abre este link para conectar TikTok: ' + url);
  try {
    SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(
      '<p style="font-family:sans-serif">1. Toca el botón y autoriza tu cuenta de TikTok.<br>2. Vuelve aquí y cierra esta ventana.</p>' +
      '<p><a href="' + url + '" target="_blank" style="font-family:sans-serif;font-size:18px;background:#000;color:#fff;' +
      'padding:12px 20px;border-radius:8px;text-decoration:none">Conectar TikTok</a></p>').setWidth(380).setHeight(180), 'TikTok');
  } catch (e) { /* corrido desde el editor: el link queda en el Execution log */ }
}

/** TikTok vuelve aquí con el código: lo cambia por los tokens y los guarda en Propiedades del script. */
function tiktokVolver(req) {
  const p = req.parameter || {};
  if (p.error || !p.code) return HtmlService.createHtmlOutput('❌ TikTok no autorizó: ' + (p.error_description || p.error || 'sin código'));
  try {
    ttGuardar_(ttToken_({ grant_type: 'authorization_code', code: p.code, redirect_uri: ttRegreso_() }));
    return HtmlService.createHtmlOutput('<h2 style="font-family:sans-serif">✅ TikTok conectado. Ya puedes cerrar esta pestaña.</h2>');
  } catch (e) {
    return HtmlService.createHtmlOutput('❌ ' + (e.message || e));
  }
}

function ttToken_(params) {
  const r = UrlFetchApp.fetch(TT.API + '/oauth/token/', { method: 'post', muteHttpExceptions: true,
    contentType: 'application/x-www-form-urlencoded',
    payload: Object.assign({ client_key: ttProp_('TIKTOK_CLIENT_KEY'), client_secret: ttProp_('TIKTOK_CLIENT_SECRET') }, params) });
  const b = JSON.parse(r.getContentText());
  if (!b.access_token) throw new Error('TikTok token: ' + (b.error_description || b.error || r.getContentText().slice(0, 200)));
  return b;
}

function ttGuardar_(b) {
  PropertiesService.getScriptProperties().setProperties({
    TIKTOK_REFRESH: b.refresh_token, TIKTOK_ACCESS: b.access_token,
    TIKTOK_VENCE: String(Date.now() + (Number(b.expires_in || 86400) - 300) * 1000) });
}

/** Token vigente: si venció (dura 24 h), lo renueva con el refresh token (dura 1 año). */
function ttAcceso_() {
  if (!ttProp_('TIKTOK_REFRESH')) throw new Error('TikTok no está conectado: menú Plan IG › Conectar TikTok');
  if (Number(ttProp_('TIKTOK_VENCE')) > Date.now() && ttProp_('TIKTOK_ACCESS')) return ttProp_('TIKTOK_ACCESS');
  const b = ttToken_({ grant_type: 'refresh_token', refresh_token: ttProp_('TIKTOK_REFRESH') });
  ttGuardar_(b);
  return b.access_token;
}

function tt_(ruta, cuerpo, metodo) {
  const r = UrlFetchApp.fetch(TT.API + ruta, { method: metodo || 'post', muteHttpExceptions: true,
    contentType: 'application/json; charset=UTF-8', headers: { Authorization: 'Bearer ' + ttAcceso_() },
    payload: cuerpo ? JSON.stringify(cuerpo) : undefined });
  const b = JSON.parse(r.getContentText() || '{}');
  if (b.error && b.error.code && b.error.code !== 'ok') throw new Error('TikTok: ' + b.error.code + ' · ' + (b.error.message || ''));
  return b.data || {};
}

/** Revisa la conexión. Si falta configurar, muestra en el Execution log la URL de regreso para la app de TikTok. */
function probarTikTok() {
  prepararTikTok_();
  console.log('URL de regreso (Redirect URI) para la app de TikTok: ' + ttRegreso_());
  if (!ttProp_('TIKTOK_REFRESH')) { avisar_('TikTok aún no está conectado. Columnas listas en la hoja.'); return; }
  const u = tt_('/user/info/?fields=display_name', null, 'get');
  avisar_('TikTok conectado: ' + ((u.user && u.user.display_name) || '¿?') + ' · columnas listas en la hoja');
}

/* ---------- Envío ---------- */

/** Lo llama publicarPendientes, después de YouTube. Nunca rompe Instagram. aprobada = llegó su hora. */
function tiktokFila_(f, i, aprobada) {
  if (!TT.ACTIVO || !f.col.tt) return;
  const est = String(f.v(i, 'tt')).trim();
  if (est === 'En borradores') { revisarTikTok_(f, i); return; }
  if (!(est === 'Publicar' || (est === '' && aprobada))) return;
  if (!ttProp_('TIKTOK_REFRESH')) return; // sin conectar: no marca nada
  f.set(i, 'tt', 'Subiendo');
  SpreadsheetApp.flush(); // si se corta a mitad queda "Subiendo" y no se manda dos veces
  try {
    const file = archivo_(f.v(i, 'video'));
    const size = file.getSize();
    const ini = tt_('/post/publish/inbox/video/init/', {
      source_info: { source: 'FILE_UPLOAD', video_size: size, chunk_size: size, total_chunk_count: 1 } });
    const r = UrlFetchApp.fetch(ini.upload_url, { method: 'put', contentType: 'video/mp4', muteHttpExceptions: true,
      payload: file.getBlob().getBytes(), headers: { 'Content-Range': 'bytes 0-' + (size - 1) + '/' + size } });
    if (r.getResponseCode() >= 300) throw new Error('Subida ' + r.getResponseCode() + ': ' + r.getContentText().slice(0, 200));
    PropertiesService.getScriptProperties().setProperty('tt_' + idDe_(f.v(i, 'video')), ini.publish_id);
    f.set(i, 'tt', 'En borradores');
    f.set(i, 'ttlink', 'Llegó a tus borradores de TikTok: publícalo antes de 24 h (' +
      Utilities.formatDate(new Date(), tz_(), 'dd/MM HH:mm') + ')');
    correoTikTok_(f, i);
  } catch (e) {
    f.set(i, 'tt', 'Error');
    f.set(i, 'ttlink', ('TikTok: ' + (e.message || e)).slice(0, 300));
  }
}

/** Pregunta a TikTok si ya publicaste el borrador. */
function revisarTikTok_(f, i) {
  const id = ttProp_('tt_' + idDe_(f.v(i, 'video')));
  if (!id || !ttProp_('TIKTOK_REFRESH')) return;
  try {
    const s = tt_('/post/publish/status/fetch/', { publish_id: id });
    if (s.status === 'PUBLISH_COMPLETE') {
      const post = (s.publicaly_available_post_id || [])[0];
      f.set(i, 'tt', 'Publicado');
      f.set(i, 'ttlink', post ? 'https://www.tiktok.com/video/' + post : 'Publicado en TikTok');
    } else if (s.status === 'FAILED') {
      f.set(i, 'tt', 'Error');
      f.set(i, 'ttlink', 'TikTok: ' + (s.fail_reason || 'falló'));
    }
  } catch (e) { console.log('Estado TikTok: ' + (e.message || e)); }
}

/** Correo con la descripción lista para copiar y pegar en TikTok. */
function correoTikTok_(f, i) {
  if (!TT.CORREO) return;
  try {
    const cod = f.v(i, 'codigo') ? f.v(i, 'codigo') + ' · ' : '';
    MailApp.sendEmail(TT.CORREO, '📲 TikTok: ' + cod + titulo_(f, i) + ' está en tus borradores',
      'Abre TikTok › Bandeja de entrada (notificaciones) › toca el aviso del video › pega la descripción › Publicar.\n' +
      'Tienes unas 24 horas antes de que el borrador se borre.\n\n' +
      '— Descripción para copiar —\n\n' + String(f.v(i, 'desc')).trim());
  } catch (e) { console.log('Correo TikTok: ' + (e.message || e)); }
}
