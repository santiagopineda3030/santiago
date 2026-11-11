/**
 * Anuncios (Meta) · ContentIA · Tracker cada 3 días
 * Token: Propiedades del script › META_ADS_TOKEN (usuario del sistema "ig contentia"). Nunca en este código.
 * Regla: este código NUNCA activa anuncios, NUNCA toca presupuesto y NUNCA crea gasto. Solo LEE datos de Meta.
 *
 * Qué hace reporteAnuncios() (corre solo cada 3 días a las 7 a. m.):
 *  1. Pide a Meta los números de los últimos 3 días por anuncio.
 *  2. Cuenta los leads REALES de la hoja de leads (etiqueta utm_content = código del anuncio, ej. A1). Sin píxel.
 *  3. Mira en Google Calendar si cada lead agendó la llamada (su correo aparece como invitado).
 *  4. Escribe una fila por anuncio en "Cada 3 días" y recalcula "Veredicto" (Funciona / Probar más / Apagar).
 *  5. Manda un correo corto a Santi con el resumen.
 */
const ADS = {
  CUENTA: 'act_1449021934086792', // ContentIA Ads (USD, America/Bogota)
  API: 'https://graph.facebook.com/v23.0/',
  TRACKER: '1rpHemhgypm3j85Nb1qx6yXvRIJchrbkZTT6Y84QkS2k', // Tracker de anuncios - ContentIA
  LEADS: '1a_GEgOia5tNyVp9rBDv9hyV0K_BSmOMK-vu-s7lGBFE',   // Leads - ContentIA (pestaña "Leads")
  DIAS: 3,
};

const COLS_PERIODO = ['Desde', 'Hasta', 'Código', 'Anuncio (Meta)', 'ID anuncio', 'Estado en Meta', 'Gasto (USD)',
  'Impresiones', 'Alcance', 'Frecuencia', 'Clics en el link', 'CTR link %', 'CPC link (USD)', 'Vistas 3 s', '% gancho (3 s)',
  'Vistas 75 %', '% ve el 75 %', 'Mensajes', 'Comentarios', 'Leads Meta', 'Leads reales', 'Agendaron', 'Costo por lead (USD)',
  'Costo por agenda (USD)', 'Actualizado'];

const COLS_VEREDICTO = ['Código', 'Anuncio (Meta)', 'Estado en Meta', 'Primer día con gasto', 'Gasto total (USD)', 'Impresiones',
  'CTR link %', '% gancho (3 s)', '% ve el 75 %', 'Leads reales', 'Agendaron', 'Costo por lead (USD)', 'Costo por agenda (USD)',
  'Veredicto', 'Por qué', 'Actualizado'];

// Valores por defecto. Santi los cambia en la pestaña "Cómo leerlo" (columna B), no aquí.
const REGLAS_DEF = {
  'Costo por lead objetivo (USD)': 10,
  'Costo por lead máximo (USD)': 20,
  'Gasto sin leads para apagar (USD)': 30,
  'CTR link mínimo %': 0.8,
  '% gancho mínimo': 25,
  'Impresiones mínimas para juzgar': 2000,
  'Leads para decir Funciona': 3,
};

function adsToken_() {
  const t = String(PropertiesService.getScriptProperties().getProperty('META_ADS_TOKEN') || '').trim().replace(/^"|"$/g, '');
  if (!t) throw new Error('Falta META_ADS_TOKEN en Configuración del proyecto › Propiedades del script');
  return t;
}

/** Solo GET. No existe en este archivo ninguna llamada que cree, active o cambie algo en Meta. */
function adsGet_(ruta, params) {
  const q = Object.keys(params || {}).map(k => k + '=' + encodeURIComponent(params[k])).join('&');
  let url = ADS.API + ruta + '?' + q + (q ? '&' : '') + 'access_token=' + encodeURIComponent(adsToken_());
  const datos = [];
  for (let i = 0; i < 20 && url; i++) {
    const r = UrlFetchApp.fetch(url, { method: 'get', muteHttpExceptions: true });
    const b = JSON.parse(r.getContentText());
    if (b.error) throw new Error('Meta: ' + b.error.message + ' (código ' + b.error.code + ')');
    if (!b.data) return b;
    datos.push.apply(datos, b.data);
    url = b.paging && b.paging.next;
  }
  return datos;
}

/** Prueba de solo lectura: no crea ni cambia nada. */
function probarAnuncios() {
  const b = adsGet_(ADS.CUENTA, { fields: 'name,account_status,currency,timezone_name' });
  const estados = { 1: 'activa', 2: 'deshabilitada', 3: 'sin método de pago / pendiente', 7: 'en revisión', 9: 'en periodo de gracia', 101: 'cerrada' };
  console.log('✅ Conectado a la cuenta publicitaria "' + b.name + '" · ' + b.currency + ' · ' + b.timezone_name +
    ' · estado: ' + (estados[b.account_status] || b.account_status));
}

/** Una sola vez: deja las pestañas listas y programa el reporte cada 3 días a las 7 a. m. */
function instalarTracker() {
  prepararTracker_();
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'reporteAnuncios').forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('reporteAnuncios').timeBased().everyDays(ADS.DIAS).atHour(7).inTimezone('America/Bogota').create();
  console.log('✅ Tracker listo. Reporte cada 3 días a las 7 a. m. Ojo: si vuelves a correr instalar() de Code.gs, corre también instalarTracker().');
}

function prepararTracker_() {
  const ss = SpreadsheetApp.openById(ADS.TRACKER);
  let p = ss.getSheetByName('Cada 3 días') || ss.getSheetByName('Diario');
  if (p.getName() === 'Diario') p.setName('Cada 3 días');
  encabezar_(p, COLS_PERIODO);
  const v = ss.getSheetByName('Veredicto') || ss.insertSheet('Veredicto', 1);
  encabezar_(v, COLS_VEREDICTO);
  return ss;
}

function encabezar_(sh, cols) {
  sh.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold');
  sh.setFrozenRows(1);
}

/** Lo corre el reloj cada 3 días. También se puede correr a mano. */
function reporteAnuncios() {
  const ss = prepararTracker_();
  const reglas = leerReglas_(ss);
  const tz = 'America/Bogota';
  const hoy = new Date();
  const hasta = new Date(hoy.getTime() - 864e5);                  // ayer (día completo)
  const desde = new Date(hasta.getTime() - (ADS.DIAS - 1) * 864e5);
  const f = d => Utilities.formatDate(d, tz, 'yyyy-MM-dd');

  // 1. Números de Meta del periodo y de toda la vida, por anuncio
  const campos = 'ad_id,ad_name,spend,impressions,reach,frequency,inline_link_clicks,inline_link_click_ctr,' +
    'cost_per_inline_link_click,actions,video_p75_watched_actions,date_start';
  const periodo = adsGet_(ADS.CUENTA + '/insights', { level: 'ad', fields: campos, limit: 500,
    time_range: JSON.stringify({ since: f(desde), until: f(hasta) }) });
  const vida = adsGet_(ADS.CUENTA + '/insights', { level: 'ad', fields: campos, limit: 500, date_preset: 'maximum' });
  const primerDia = {};
  adsGet_(ADS.CUENTA + '/insights', { level: 'ad', fields: 'ad_id,spend', limit: 500, date_preset: 'maximum', time_increment: 1 })
    .forEach(r => { if (Number(r.spend) > 0 && (!primerDia[r.ad_id] || r.date_start < primerDia[r.ad_id])) primerDia[r.ad_id] = r.date_start; });
  const estado = {};
  adsGet_(ADS.CUENTA + '/ads', { fields: 'id,effective_status', limit: 500 }).forEach(a => estado[a.id] = a.effective_status);

  // 2 y 3. Leads reales y agendas, por código
  const leads = leerLeads_(ss);

  // 4a. Filas del periodo (se reemplazan si el periodo ya estaba)
  const sh = ss.getSheetByName('Cada 3 días');
  const ya = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 5).getDisplayValues() : [];
  for (let i = ya.length - 1; i >= 0; i--) if (ya[i][0] === f(desde) && ya[i][1] === f(hasta)) sh.deleteRow(i + 2);
  const filas = periodo.map(r => {
    const m = metricas_(r), cod = codigo_(r.ad_name);
    const l = contar_(leads, cod, desde, hasta);
    return [f(desde), f(hasta), cod, r.ad_name, r.ad_id, estado[r.ad_id] || '', m.gasto, m.imp, m.alcance, m.frec, m.clics, m.ctr,
      m.cpc, m.v3, m.gancho, m.v75, m.p75, m.mensajes, m.comentarios, m.leadsMeta, l.leads, l.agendas,
      l.leads ? redondo_(m.gasto / l.leads) : '', l.agendas ? redondo_(m.gasto / l.agendas) : '', hoy];
  });
  if (filas.length) sh.getRange(sh.getLastRow() + 1, 1, filas.length, COLS_PERIODO.length).setValues(filas);

  // 4b. Veredicto con toda la vida del anuncio
  const vsh = ss.getSheetByName('Veredicto');
  if (vsh.getLastRow() > 1) vsh.getRange(2, 1, vsh.getLastRow() - 1, COLS_VEREDICTO.length).clearContent();
  const resumen = [];
  const vfilas = vida.map(r => {
    const m = metricas_(r), cod = codigo_(r.ad_name);
    const l = contar_(leads, cod, null, null);
    const dias = primerDia[r.ad_id] ? Math.floor((hoy - new Date(primerDia[r.ad_id] + 'T00:00:00-05:00')) / 864e5) : 0;
    const v = veredicto_(m, l, dias, reglas);
    resumen.push(cod + ' → ' + v[0] + ' (' + v[1] + ')');
    return [cod, r.ad_name, estado[r.ad_id] || '', primerDia[r.ad_id] || '', m.gasto, m.imp, m.ctr, m.gancho, m.p75,
      l.leads, l.agendas, l.leads ? redondo_(m.gasto / l.leads) : '', l.agendas ? redondo_(m.gasto / l.agendas) : '', v[0], v[1], hoy];
  });
  if (vfilas.length) vsh.getRange(2, 1, vfilas.length, COLS_VEREDICTO.length).setValues(vfilas);
  colorear_(vsh);

  // 5. Aviso corto
  const cuerpo = vfilas.length ? resumen.join('\n') : 'Sin datos de anuncios todavía (nada ha gastado).';
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(), '📊 Anuncios · ' + f(desde) + ' a ' + f(hasta),
    cuerpo + '\n\nHoja: https://docs.google.com/spreadsheets/d/' + ADS.TRACKER + '\n(Claude nunca prende ni apaga nada: decides tú.)');
  console.log('✅ Reporte listo: ' + filas.length + ' anuncios en el periodo, ' + vfilas.length + ' en el veredicto.');
}

function metricas_(r) {
  const acc = t => ((r.actions || []).filter(a => a.action_type === t)[0] || {}).value || 0;
  const imp = Number(r.impressions || 0), gasto = Number(r.spend || 0);
  const v3 = Number(acc('video_view'));
  const v75 = Number(((r.video_p75_watched_actions || [])[0] || {}).value || 0);
  return {
    gasto: redondo_(gasto), imp: imp, alcance: Number(r.reach || 0), frec: redondo_(Number(r.frequency || 0)),
    clics: Number(r.inline_link_clicks || 0), ctr: redondo_(Number(r.inline_link_click_ctr || 0)),
    cpc: redondo_(Number(r.cost_per_inline_link_click || 0)), v3: v3, gancho: imp ? redondo_(v3 / imp * 100) : 0,
    v75: v75, p75: v3 ? redondo_(v75 / v3 * 100) : 0,
    mensajes: Number(acc('onsite_conversion.messaging_conversation_started_7d')), comentarios: Number(acc('comment')),
    leadsMeta: Number(acc('lead')) + Number(acc('offsite_conversion.fb_pixel_lead')),
  };
}

/** Código del anuncio dentro del nombre (ej. "CO_DUEÑOS_A1_v1" → "A1"). Sin código → "SIN CÓDIGO". */
function codigo_(nombre) {
  const m = String(nombre || '').toUpperCase().match(/(?:^|[_\s-])(A\d+)(?=$|[_\s-])/);
  return m ? m[1] : 'SIN CÓDIGO';
}

/** Lee la hoja de leads. Agendó = "Sí" escrito a mano, o el correo aparece como invitado en Calendar. */
function leerLeads_() {
  const libro = SpreadsheetApp.openById(ADS.LEADS);
  const sh = libro.getSheetByName('Leads') || libro.getSheets()[0];
  if (!sh || sh.getLastRow() < 2) return [];
  const datos = sh.getDataRange().getValues();
  const cab = datos.shift().map(String);
  const c = n => cab.indexOf(n);
  const invitados = correosAgendados_();
  const out = [];
  datos.forEach((fila, i) => {
    const fecha = fila[c('Fecha')] instanceof Date ? fila[c('Fecha')] : new Date(fila[c('Fecha')]);
    if (isNaN(fecha)) return;
    let cod = String(fila[c('Anuncio (código)')] || '').trim().toUpperCase();
    if (!cod) cod = codigo_(fila[c('utm_content')]);
    const correo = String(fila[c('Correo')] || '').trim().toLowerCase();
    let ag = String(fila[c('Agendó')] || '').trim().toLowerCase();
    if (!ag && correo && invitados[correo]) {
      sh.getRange(i + 2, c('Agendó') + 1).setValue('Sí');
      sh.getRange(i + 2, c('Fecha de la llamada') + 1).setValue(invitados[correo]);
      ag = 'sí';
    }
    out.push({ fecha: fecha, cod: cod, agendo: ag === 'sí' || ag === 'si' });
  });
  return out;
}

/** Correos de invitados en el calendario principal (últimos 60 días y próximos 30). */
function correosAgendados_() {
  const res = {};
  const ahora = Date.now();
  CalendarApp.getDefaultCalendar().getEvents(new Date(ahora - 60 * 864e5), new Date(ahora + 30 * 864e5))
    .forEach(ev => ev.getGuestList().forEach(g => { const e = g.getEmail().toLowerCase(); if (!res[e]) res[e] = ev.getStartTime(); }));
  return res;
}

function contar_(leads, cod, desde, hasta) {
  const ini = desde ? new Date(Utilities.formatDate(desde, 'America/Bogota', 'yyyy-MM-dd') + 'T00:00:00-05:00') : null;
  const fin = hasta ? new Date(Utilities.formatDate(hasta, 'America/Bogota', 'yyyy-MM-dd') + 'T23:59:59-05:00') : null;
  const ls = leads.filter(l => l.cod === cod && (!ini || l.fecha >= ini) && (!fin || l.fecha <= fin));
  return { leads: ls.length, agendas: ls.filter(l => l.agendo).length };
}

function leerReglas_(ss) {
  const r = Object.assign({}, REGLAS_DEF);
  const sh = ss.getSheetByName('Cómo leerlo');
  if (sh) sh.getDataRange().getValues().forEach(f => { if (f[0] in r && f[1] !== '' && !isNaN(Number(f[1]))) r[f[0]] = Number(f[1]); });
  return r;
}

/** Reglas simples. Devuelve [veredicto, por qué]. */
function veredicto_(m, l, dias, R) {
  const cpl = l.leads ? m.gasto / l.leads : Infinity;
  const juzgable = m.imp >= R['Impresiones mínimas para juzgar'];
  if (m.gasto >= R['Gasto sin leads para apagar (USD)'] && l.leads === 0)
    return ['Apagar', 'Gastó $' + m.gasto + ' y no trajo ningún lead'];
  if (l.leads >= 2 && cpl > R['Costo por lead máximo (USD)'] && dias >= 4)
    return ['Apagar', 'Cada lead cuesta $' + redondo_(cpl) + ' (máximo $' + R['Costo por lead máximo (USD)'] + ')'];
  if (juzgable && dias >= 4 && m.ctr < R['CTR link mínimo %'] / 2 && l.leads === 0)
    return ['Apagar', 'Casi nadie toca el link (CTR ' + m.ctr + '%)'];
  if (l.leads >= R['Leads para decir Funciona'] && cpl <= R['Costo por lead objetivo (USD)'])
    return ['Funciona', l.leads + ' leads a $' + redondo_(cpl) + ' c/u' + (l.agendas ? ' · ' + l.agendas + ' agendaron' : '')];
  if (dias < 4) return ['Probar más', 'Meta todavía está aprendiendo (día ' + dias + ' de 4)'];
  const motivos = [];
  if (juzgable && m.gancho < R['% gancho mínimo']) motivos.push('gancho flojo (' + m.gancho + '%)');
  if (juzgable && m.ctr < R['CTR link mínimo %']) motivos.push('CTR bajo (' + m.ctr + '%)');
  if (l.leads) motivos.push(l.leads + ' leads a $' + redondo_(cpl));
  else motivos.push('aún sin leads con $' + m.gasto);
  return ['Probar más', motivos.join(' · ')];
}

function colorear_(sh) {
  const n = sh.getLastRow() - 1;
  if (n < 1) return;
  const col = COLS_VEREDICTO.indexOf('Veredicto') + 1;
  const rango = sh.getRange(2, col, n, 1);
  rango.setBackgrounds(rango.getValues().map(v => [v[0] === 'Funciona' ? '#c8e6c9' : v[0] === 'Apagar' ? '#ffcdd2' : '#fff9c4']));
}

function redondo_(x) { return Math.round(x * 100) / 100; }
