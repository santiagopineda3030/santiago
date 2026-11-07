/**
 * Plan de contenido orgánico — ContentIA
 * Apps Script dentro de la hoja "Plan contenido orgánico - ContentIA".
 *
 * Pestañas: <Mes> (Noviembre, Diciembre…) · COLA POR EDITAR · CAL IG (la crea el script).
 * Flujo:
 *  1. El video editado se sube a CARPETA_EDITADOS con el código al inicio: "v7 1.0 tema.mp4".
 *  2. traerVideosNuevos (cada hora): pega el link en la fila de esa idea → Publicación = "Escribiendo descripción".
 *  3. Se escribe la descripción y se pasa a "Listo". Lo "Listo" sin fecha recibe el siguiente día libre a la HORA.
 *  4. Quien aprueba cambia Publicación → "Publicar". A la fecha y hora de la fila se publica solo en Instagram
 *     y queda marcado en Google Calendar ("✅ Publicado · …", verde, sin notificaciones).
 *  5. Primero sale en Instagram; en las vueltas siguientes (cada 15 min) sale en YouTube Shorts (YouTube.gs) y llega a
 *     TikTok como borrador (TikTok.gs, columnas "TikTok" y "Link TikTok"). Un solo paso pesado por vuelta (límite de 6 min).
 *
 * El token de Meta (token de página que no vence) va en Configuración del proyecto › Propiedades del script
 * › META_TOKEN. Nunca en este código.
 */

const CONFIG = {
  CUENTA: '@soysanti__content_ia',                       // solo para el título del calendario
  IG_ID: '17841438740412085',                            // id de la cuenta profesional de Instagram. Vacío = sin publicar
  CARPETA_EDITADOS: '1A1zlwXyvR-l2CZcJ6dnHUp-SZXnEcUGT', // ContentIA › Edición de videos › 2. Videos terminados (antes Instagram › 4. Contenido editado)
  HORA: '11:00',                                         // hora por defecto (Bogotá)
  PRIMER_CODIGO: 1,
  MAX_MB: 30,
  TIPOS: { 'Noticias IA': '📰' },
  // Todos los días: Noticias IA (0 = domingo … 6 = sábado)
  PLANTILLA: { 0: ['Noticias IA'], 1: ['Noticias IA'], 2: ['Noticias IA'], 3: ['Noticias IA'], 4: ['Noticias IA'], 5: ['Noticias IA'], 6: ['Noticias IA'] },
  COLOR: '#dc2626',
  MARCAR_CALENDARIO: true                                // al publicar, crea "✅ Publicado · …" en tu Google Calendar
};

const GRAPH = 'https://graph.facebook.com/v23.0';
const COLA = 'COLA POR EDITAR';
const CAL = 'CAL IG';
const MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

const COLS_MES = ['Fecha', 'Estado', 'Ángulo', 'Referente', 'Explicación', 'Guion', 'Elementos adicionales',
  'Link Video Editado', 'Descripción de Instagram', '#', 'Archivo', 'Hora', 'Publicación', 'Link publicado', 'Tipo', 'contenedor'];
const ESTADOS_PROD = ['Idea', 'Guion', 'Grabado', 'Editado', 'Publicado'];
const PUB = ['Escribiendo descripción', 'Listo', 'Publicar', 'Programado', 'Publicando', 'Publicado', 'Error'];
const COLS_COLA = ['Subido', 'Código', 'Categoría', 'Título', 'Crudo', 'Carpeta', 'Instrucciones', 'Estado', 'Corrección',
  'Editado (link)', 'Entregado', 'Notas'];
const ESTADOS_COLA = ['Por editar', 'Editando', 'Revisión', 'Corrección', 'Entregado', 'Archivado', 'Descartado'];

/* ---------- Instalación y menú ---------- */

function instalar() {
  if (!CONFIG.CARPETA_EDITADOS) throw new Error('Llena CARPETA_EDITADOS en CONFIG');
  const hoy = new Date();
  crearMes_(hoy);
  crearMes_(new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1));
  crearCola_();
  prepararYouTube_();
  prepararTikTok_();
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('publicarPendientes').timeBased().everyMinutes(15).create();
  ScriptApp.newTrigger('traerVideosNuevos').timeBased().everyHours(1).create();
  ScriptApp.newTrigger('alEditar').forSpreadsheet(SpreadsheetApp.getActive()).onEdit().create();
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('DESDE')) props.setProperty('DESDE', new Date().toISOString());
  if (CONFIG.IG_ID && props.getProperty('META_TOKEN')) probarConexion();
  else avisar_('Instalado sin publicación automática (falta IG_ID o META_TOKEN). Todo lo demás funciona.');
  traerVideosNuevos();
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Plan IG')
    .addItem('Publicar ya lo que toca', 'publicarPendientes')
    .addItem('Traer videos nuevos del editor', 'traerVideosNuevos')
    .addItem('Unir video a esta fila por link…', 'unirPorLink')
    .addItem('Crear pestaña del mes siguiente', 'crearMesSiguiente')
    .addItem('Repintar calendario', 'pintarCalendario')
    .addItem('Probar conexión con Instagram', 'probarConexion')
    .addItem('Probar subida a Instagram (sin publicar)', 'probarSubidaInstagram')
    .addItem('Probar conexión con YouTube', 'probarYouTube')
    .addItem('Conectar TikTok', 'conectarTikTok')
    .addItem('Probar conexión con TikTok', 'probarTikTok')
    .addToUi();
}

/** Revisa token, cuenta y cupo. No publica nada. */
function probarConexion() {
  if (!CONFIG.IG_ID) throw new Error('Falta IG_ID en CONFIG');
  const c = graph_('get', CONFIG.IG_ID, { fields: 'username' });
  const cupo = graph_('get', CONFIG.IG_ID + '/content_publishing_limit', { fields: 'quota_usage,config' }).data[0];
  avisar_('Conectado a @' + c.username + ' · publicaciones hoy por API: ' + cupo.quota_usage + ' de ' + cupo.config.quota_total);
  if (CONFIG.MARCAR_CALENDARIO) {
    try { avisar_('Google Calendar listo: ' + CalendarApp.getDefaultCalendar().getName()); }
    catch (e) { avisar_('Google Calendar sin permiso: ' + (e.message || e)); }
  }
}

function crearMesSiguiente() {
  const hoy = new Date();
  crearMes_(new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1));
}

/** Pestaña del mes con encabezados, validaciones y formatos (no toca una que ya exista). */
function crearMes_(fecha) {
  const ss = SpreadsheetApp.getActive(), nombre = MESES[fecha.getMonth()];
  if (ss.getSheetByName(nombre)) return;
  const sh = ss.insertSheet(nombre);
  const n = sh.getMaxRows() - 1, col = k => COLS_MES.indexOf(k) + 1;
  sh.getRange(1, 1, 1, COLS_MES.length).setValues([COLS_MES]).setFontWeight('bold')
    .setBackground('#1f2937').setFontColor('#ffffff');
  sh.setFrozenRows(1);
  const lista = (l, estricto) => SpreadsheetApp.newDataValidation().requireValueInList(l, true).setAllowInvalid(!estricto).build();
  sh.getRange(2, col('Fecha'), n).setNumberFormat('dd/mm/yyyy')
    .setDataValidation(SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(false).build());
  sh.getRange(2, col('Estado'), n).setDataValidation(lista(ESTADOS_PROD, true));
  sh.getRange(2, col('Publicación'), n).setDataValidation(lista(PUB, true));
  sh.getRange(2, col('Tipo'), n).setDataValidation(lista(Object.keys(CONFIG.TIPOS), true));
  sh.getRange(2, col('Hora'), n).setNumberFormat('@');
  ['Explicación', 'Guion', 'Descripción de Instagram'].forEach(k => sh.getRange(2, col(k), n).setWrap(true));
  [95, 90, 130, 160, 220, 220, 160, 200, 320, 50, 160, 60, 150, 200, 110].forEach((w, i) => sh.setColumnWidth(i + 1, w));
  sh.hideColumns(col('contenedor'));
  const r = sh.getRange(2, col('Publicación'), n);
  sh.setConditionalFormatRules([['Publicado', '#d1fae5'], ['Programado', '#ede9fe'], ['Publicar', '#ede9fe'],
    ['Listo', '#dbeafe'], ['Escribiendo descripción', '#fef3c7'], ['Error', '#fee2e2']]
    .map(([t, c]) => SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(t).setBackground(c).setRanges([r]).build()));
  sh.getRange(1, col('#')).setNote('Lo pone el script. El editor empieza el nombre del archivo con este código: "v7 1.0 tema.mp4"');
  sh.getRange(1, col('Publicación')).setNote('Solo cambia a "Publicar" cuando apruebes. Lo demás lo pone el script.');
  sh.getRange(1, col('Hora')).setNote('Hora local, ej. 11:00. Vacía = ' + CONFIG.HORA + ' al asignar fecha.');
  prepararYouTube_(); // columnas Título YouTube · YouTube · Link YouTube
  prepararTikTok_();  // columnas TikTok · Link TikTok
}

/** COLA POR EDITAR: filas 1–2 contadores, fila 3 encabezados, datos desde la 4. */
function crearCola_() {
  const ss = SpreadsheetApp.getActive();
  if (ss.getSheetByName(COLA)) return;
  const sh = ss.insertSheet(COLA);
  sh.getRange('A1').setValue('COLA POR EDITAR · una fila por pieza').setFontWeight('bold').setFontSize(13);
  sh.getRange('C1:G1').setValues([['Por editar', 'Editando', 'Revisión', 'Corrección', 'Entregados 7 días']]).setFontWeight('bold');
  sh.getRange('C2:G2').setFormulas([['=COUNTIF(H4:H,C1)', '=COUNTIF(H4:H,D1)', '=COUNTIF(H4:H,E1)', '=COUNTIF(H4:H,F1)',
    '=COUNTIFS(H4:H,"Entregado",K4:K,">="&(TODAY()-7))']]).setFontSize(14).setHorizontalAlignment('center');
  sh.getRange('H1').setValue('Flujo: Por editar → Editando → Revisión → Corrección → Entregado. ' +
    'El video final va a la carpeta de editados con el código al inicio del nombre.').setWrap(true).setFontColor('#6b7280');
  sh.getRange(3, 1, 1, COLS_COLA.length).setValues([COLS_COLA]).setFontWeight('bold').setBackground('#1f2937').setFontColor('#ffffff');
  sh.setFrozenRows(3);
  const n = sh.getMaxRows() - 3;
  const cat = Object.keys(CONFIG.TIPOS).concat(['B-roll', 'Recurso', 'Sin clasificar']);
  sh.getRange(4, 3, n).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(cat, true).build());
  sh.getRange(4, 8, n).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(ESTADOS_COLA, true).setAllowInvalid(false).build());
  [1, 11].forEach(c => sh.getRange(4, c, n).setNumberFormat('dd/mm/yyyy'));
  [85, 60, 110, 260, 160, 160, 320, 100, 260, 160, 85, 140].forEach((w, i) => sh.setColumnWidth(i + 1, w));
  [7, 9].forEach(c => sh.getRange(4, c, n).setWrap(true));
}

/* ---------- Lectura de las pestañas del mes ---------- */

const norm_ = s => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();

function encabezados_(sh) {
  const m = {};
  sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0].forEach((h, i) => { if (h !== '') m[norm_(h)] = i + 1; });
  return m;
}

/** Pestañas del plan: las que tienen "#", "Link Video Editado" y "Publicación" en la fila 1. */
function planes_() {
  return SpreadsheetApp.getActive().getSheets().map(sh => {
    if (sh.getLastColumn() < 2) return null;
    const h = encabezados_(sh);
    if (!h['#'] || !h['link video editado'] || !h['publicacion']) return null;
    return { sh, col: {
      fecha: h['fecha'], prod: h['estado'], angulo: h['angulo'], explicacion: h['explicacion'], guion: h['guion'],
      video: h['link video editado'], desc: h['descripcion de instagram'], codigo: h['#'], archivo: h['archivo'],
      hora: h['hora'], estado: h['publicacion'], link: h['link publicado'], tipo: h['tipo'], contenedor: h['contenedor'],
      yttitulo: h['titulo youtube'], yt: h['youtube'], ytlink: h['link youtube'], tt: h['tiktok'], ttlink: h['link tiktok'] } };
  }).filter(Boolean);
}

function leer_(f) {
  const n = f.sh.getLastRow() - 1, w = f.sh.getLastColumn();
  f.vals = n > 0 ? f.sh.getRange(2, 1, n, w).getValues() : [];
  f.disp = n > 0 ? f.sh.getRange(2, 1, n, w).getDisplayValues() : [];
  f.v = (i, k) => f.col[k] ? f.vals[i][f.col[k] - 1] : '';
  f.d = (i, k) => f.col[k] ? f.disp[i][f.col[k] - 1] : '';
  f.set = (i, k, val) => {
    if (!f.col[k]) return;
    f.vals[i][f.col[k] - 1] = val;
    const r = f.sh.getRange(i + 2, f.col[k]);
    if (k === 'hora') r.setNumberFormat('@');
    r.setValue(val);
    if (k === 'hora') f.disp[i][f.col[k] - 1] = String(val);
  };
  if (f.col.video) chips_(f, n);
  return f;
}

/** Si pegaron un chip de Drive en "Link Video Editado", saca el link del chip (solo en memoria). */
function chips_(f, n) {
  let ricos = null;
  for (let i = 0; i < n; i++) {
    const val = String(f.vals[i][f.col.video - 1] || '').trim();
    if (!val || idDe_(val)) continue;
    ricos = ricos || f.sh.getRange(2, f.col.video, n, 1).getRichTextValues();
    const rt = ricos[i][0];
    const url = rt && (rt.getLinkUrl() || rt.getRuns().map(x => x.getLinkUrl()).filter(Boolean)[0] || '');
    if (idDe_(url)) f.vals[i][f.col.video - 1] = url;
  }
}

const titulo_ = (f, i) => String(f.v(i, 'guion') || f.v(i, 'explicacion') || f.v(i, 'angulo')).replace(/[“”"]/g, '').trim();

/* ---------- 1. Videos del editor → fila de su idea ---------- */

function traerVideosNuevos() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    const props = PropertiesService.getScriptProperties();
    const desde = new Date(props.getProperty('DESDE') || 0);
    const planes = planes_().map(leer_);
    numerarIdeas_(planes);
    const usados = new Set();
    planes.forEach(f => f.vals.forEach((r, i) => { const id = idDe_(f.v(i, 'video')); if (id) usados.add(id); }));
    let unidos = 0;
    const sueltos = [];
    listarVideos_(DriveApp.getFolderById(CONFIG.CARPETA_EDITADOS)).sort((a, b) => a.creado - b.creado).forEach(v => {
      if (usados.has(v.id)) return;
      const cod = codigoDe_(v.nombre);
      const destino = cod && buscarCodigo_(planes, cod);
      if (!destino) { if (v.creado >= desde) sueltos.push(v.nombre); return; }
      const { f, i } = destino;
      if (['Publicar', 'Programado', 'Publicando', 'Publicado'].includes(f.v(i, 'estado'))) return; // ya va en camino
      const actual = idDe_(f.v(i, 'video'));
      if (actual) {
        try { if (DriveApp.getFileById(actual).getDateCreated() > v.creado) return; } catch (e) { /* borrado */ }
      }
      f.set(i, 'video', v.url);
      f.set(i, 'archivo', v.nombre);
      if (!/publicad/i.test(f.v(i, 'prod'))) f.set(i, 'prod', 'Editado');
      f.set(i, 'estado', String(f.v(i, 'desc')).trim() ? 'Listo' : 'Escribiendo descripción');
      usados.add(v.id);
      unidos++;
    });
    props.setProperty('SUELTOS', sueltos.slice(-10).join(' · '));
    asignarFechas_(planes);
    pintarCalendario();
    if (unidos) avisar_(unidos + ' video(s) unidos a su idea');
  } finally {
    lock.releaseLock();
  }
}

function listarVideos_(carpeta) {
  const out = [];
  (function recorrer(c) {
    const files = c.getFiles();
    while (files.hasNext()) {
      const f = files.next();
      if (/^video\//.test(f.getMimeType())) out.push({ id: f.getId(), url: f.getUrl(), nombre: f.getName(), creado: f.getDateCreated() });
    }
    const subs = c.getFolders();
    while (subs.hasNext()) recorrer(subs.next());
  })(carpeta);
  return out;
}

/** "v7 1.0 tema.mp4" → "v7". */
function codigoDe_(nombre) {
  const m = String(nombre).match(/^\s*v\s*0*(\d+)(?=[\s._-]|$)/i);
  return m ? 'v' + m[1] : '';
}

function buscarCodigo_(planes, cod) {
  for (const f of planes) for (let i = 0; i < f.vals.length; i++) {
    if (String(f.v(i, 'codigo')).toLowerCase().replace(/\s/g, '') === cod) return { f, i };
  }
  return null;
}

/** Ideas con contenido y sin código → siguiente código libre. */
function numerarIdeas_(planes) {
  let max = CONFIG.PRIMER_CODIGO - 1;
  planes.forEach(f => f.vals.forEach((r, i) => {
    const m = String(f.v(i, 'codigo')).match(/^v(\d+)$/i);
    if (m) max = Math.max(max, Number(m[1]));
  }));
  planes.forEach(f => f.vals.forEach((r, i) => {
    if (f.v(i, 'codigo') || !titulo_(f, i)) return;
    f.set(i, 'codigo', 'v' + (++max));
  }));
}

/** Unir un video a la fila donde está parado el cursor (por si el editor no puso el código). */
function unirPorLink() {
  const ui = SpreadsheetApp.getUi();
  const sh = SpreadsheetApp.getActiveSheet(), fila = sh.getActiveRange().getRow();
  const f = planes_().find(p => p.sh.getName() === sh.getName());
  if (!f || fila < 2) { ui.alert('Párate en la fila de la idea, en la pestaña del mes.'); return; }
  const r = ui.prompt('Link del video en Drive', ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  const file = DriveApp.getFileById(idDe_(r.getResponseText()));
  sh.getRange(fila, f.col.video).setValue(file.getUrl());
  if (f.col.archivo) sh.getRange(fila, f.col.archivo).setValue(file.getName());
  const desc = String(sh.getRange(fila, f.col.desc).getValue()).trim();
  sh.getRange(fila, f.col.estado).setValue(desc ? 'Listo' : 'Escribiendo descripción');
  pintarCalendario();
}

/* ---------- 2. Fechas ---------- */

const tz_ = () => SpreadsheetApp.getActive().getSpreadsheetTimeZone();
const dia_ = d => Utilities.formatDate(d, tz_(), 'yyyy-MM-dd');
const fechaDe_ = clave => Utilities.parseDate(clave + ' 12:00', tz_(), 'yyyy-MM-dd HH:mm');
const masDias_ = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n, 12);

/** A lo "Listo" sin fecha: siguiente día libre que le toque según la plantilla. */
function asignarFechas_(planes) {
  const ocupados = {};
  planes.forEach(f => f.vals.forEach((r, i) => {
    const fe = f.v(i, 'fecha');
    if (fe instanceof Date && f.v(i, 'estado') !== 'Error') ocupados[dia_(fe)] = String(f.v(i, 'tipo')).trim();
  }));
  const manana = masDias_(new Date(), 1);
  planes.forEach(f => f.vals.forEach((r, i) => {
    if (f.v(i, 'estado') !== 'Listo' || f.v(i, 'fecha') instanceof Date) return;
    const tipo = String(f.v(i, 'tipo')).trim();
    const d = diaLibre_(manana, tipo, ocupados, true) || diaLibre_(manana, tipo, ocupados, false) || manana;
    ocupados[dia_(d)] = tipo;
    f.set(i, 'fecha', fechaDe_(dia_(d)));
    if (!String(f.d(i, 'hora')).trim()) f.set(i, 'hora', CONFIG.HORA);
  }));
}

function diaLibre_(desde, tipo, ocupados, estricto) {
  const dias = Object.keys(CONFIG.PLANTILLA).filter(k => (CONFIG.PLANTILLA[k] || []).length).map(Number);
  const variosTipos = Object.keys(CONFIG.TIPOS).length > 1; // con un solo tipo se puede repetir todos los días
  for (let k = 0; k < 90; k++) {
    const d = masDias_(desde, k);
    if (dia_(d) in ocupados || !dias.includes(d.getDay())) continue;
    if (estricto && !CONFIG.PLANTILLA[d.getDay()].includes(tipo)) continue;
    if (variosTipos && tipo && (ocupados[dia_(masDias_(d, -1))] === tipo || ocupados[dia_(masDias_(d, 1))] === tipo)) continue;
    return d;
  }
  return null;
}

/** Fecha de la celda + hora "11:00" / "6:30 pm" (zona de la hoja) → Date. Sin fecha = ya. */
function cuando_(fecha, hora) {
  if (!(fecha instanceof Date)) return new Date(0);
  let h = 12, m = 0;
  const t = String(hora).toLowerCase().match(/(\d{1,2})(?::(\d{2}))?\s*([ap])?/);
  if (t) {
    h = Number(t[1]) % 24; m = Number(t[2] || 0);
    if (t[3] === 'p' && h < 12) h += 12;
    if (t[3] === 'a' && h === 12) h = 0;
  }
  return Utilities.parseDate(dia_(fecha) + ' ' + h + ':' + ('0' + m).slice(-2), tz_(), 'yyyy-MM-dd H:mm');
}

/* ---------- 3. Publicar ---------- */

function publicarPendientes() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return; // otra vuelta sigue corriendo
  const inicio = Date.now();
  // Apps Script corta a los 6 min SIN avisar (no pasa por el catch y la fila queda "Programado").
  // Por eso cada vuelta hace como máximo UN paso pesado (subir a Instagram, subir a YouTube o subir a TikTok)
  // y ninguno empieza si ya van más de 90 s. Lo que falte sigue en la próxima vuelta (cada 15 min).
  let pesado = false;
  const puedo = () => !pesado && Date.now() - inicio < 90 * 1000;
  try {
    planes_().map(leer_).forEach(f => f.vals.forEach((r, i) => {
      const est = f.v(i, 'estado');
      const yt = String(f.v(i, 'yt')).trim();
      // YouTube: pedido a mano ("Publicar") o pendiente porque Instagram ya arrancó ("Pendiente").
      if ((yt === 'Publicar' || yt === 'Pendiente') && puedo()) { youtubeFila_(f, i, true); pesado = true; }
      // TikTok: pedido a mano, "Pendiente" porque Instagram ya arrancó, o revisar si ya publicaste el borrador.
      if (typeof tiktokFila_ === 'function' && puedo() && tiktokFila_(f, i)) pesado = true;
      if (!['Publicar', 'Programado', 'Publicando'].includes(est)) return;
      try {
        if (est === 'Publicando') { revisar_(f, i); return; } // liviano: solo pregunta a Instagram
        const file = archivo_(f.v(i, 'video'));
        if (!String(f.v(i, 'desc')).trim()) throw new Error('Falta la descripción');
        if (cuando_(f.v(i, 'fecha'), f.d(i, 'hora')) > new Date()) {
          if (est !== 'Programado') { f.set(i, 'estado', 'Programado'); f.set(i, 'link', ''); }
          return;
        }
        if (!puedo()) return; // ya hubo un paso pesado en esta vuelta: sigue en la próxima
        // Llegó la hora: primero Instagram (lo más importante). YouTube y TikTok quedan "Pendiente" para las próximas vueltas.
        if (f.col.yt && yt === '') f.set(i, 'yt', 'Pendiente');
        if (f.col.tt && String(f.v(i, 'tt')).trim() === '') f.set(i, 'tt', 'Pendiente');
        SpreadsheetApp.flush();
        pesado = true;
        subir_(f, i, file); // deja la fila en "Publicando"
        SpreadsheetApp.flush();
        Utilities.sleep(30000); // Instagram suele procesar en menos de 1 min: una sola revisión rápida
        revisar_(f, i);        // si aún no está, la próxima vuelta lo publica
      } catch (e) {
        const msg = String(e.message || e);
        console.log('Instagram, fila ' + (i + 2) + ': ' + msg);
        const props = PropertiesService.getScriptProperties(), clave = 'reintentos_' + idDe_(f.v(i, 'video'));
        const n = Number(props.getProperty(clave) || 0) + 1;
        props.setProperty(clave, String(n));
        if (/ProcessingFailed|ERROR/.test(msg) && n <= 3) {
          f.set(i, 'estado', 'Publicar'); f.set(i, 'link', ('Instagram falló al procesar (reintento ' + n + ' de 3): ' + msg).slice(0, 300));
        } else {
          f.set(i, 'estado', 'Error'); f.set(i, 'link', msg.slice(0, 300));
        }
        f.set(i, 'contenedor', '');
      }
    }));
    pintarCalendario();
  } finally {
    lock.releaseLock();
  }
}

function archivo_(link) {
  const id = idDe_(link);
  let file = null;
  try { file = id && DriveApp.getFileById(id); } catch (e) { file = null; }
  if (!file || !/^video\//.test(file.getMimeType())) throw new Error('Falta el link de un video de Drive');
  return file;
}

/** Crea el contenedor de Reel y le sube el video de Drive en un solo envío. */
function subir_(f, i, file) {
  const id = subirContenedor_(file, String(f.v(i, 'desc')));
  f.set(i, 'contenedor', id);
  f.set(i, 'estado', 'Publicando');
  f.set(i, 'link', 'Instagram procesando el video');
}

/** Crea el contenedor y sube el video. Devuelve el id del contenedor. No publica nada. */
function subirContenedor_(file, caption) {
  if (!CONFIG.IG_ID) throw new Error('Falta IG_ID en CONFIG (publicación automática no configurada)');
  const mb = file.getSize() / 1048576;
  if (mb > CONFIG.MAX_MB) throw new Error('El video pesa ' + Math.round(mb) + ' MB (máx. ' + CONFIG.MAX_MB + '): exportarlo más liviano');
  const c = graph_('post', CONFIG.IG_ID + '/media', {
    media_type: 'REELS', upload_type: 'resumable', caption: caption, share_to_feed: 'true' });
  const r = UrlFetchApp.fetch(c.uri, {
    method: 'post', contentType: 'application/octet-stream',
    payload: file.getBlob(), // el blob directo: getBytes() con videos de ~28 MB se queda sin memoria
    headers: { Authorization: 'OAuth ' + token_(), offset: '0', file_size: String(file.getSize()) },
    muteHttpExceptions: true });
  const txt = r.getContentText();
  if (r.getResponseCode() !== 200 || /"success"\s*:\s*false|"error"/.test(txt)) {
    throw new Error('Subida ' + r.getResponseCode() + ': ' + txt.slice(0, 200));
  }
  return c.id;
}

/** Explica en español los errores de Instagram más comunes al procesar un Reel. */
function pistaIG_(status) {
  const s = String(status || '');
  if (/2207026/.test(s)) return ' → Formato no soportado: exportar MP4 H.264, audio AAC 48 kHz, 30 fps, 1080×1920, con faststart.';
  if (/2207008|2207027/.test(s)) return ' → El contenedor venció o no está listo: se vuelve a subir.';
  if (/2207003|2207020/.test(s)) return ' → Instagram no pudo descargar el video (subida incompleta).';
  if (/2207004|2207005|2207006/.test(s)) return ' → Video muy pesado o muy largo para Reels.';
  return '';
}

/**
 * PRUEBA SEGURA: sube a Instagram el video de la fila con el código de PRUEBA_IG, SIN PUBLICAR,
 * y escribe en el registro lo que responde Instagram. Sirve para saber por qué rechaza un video.
 * Correr desde el editor (▶) o desde el menú Plan IG. El contenedor sin publicar se borra solo en 24 h.
 */
const PRUEBA_IG = 'v3';
function probarSubidaInstagram() {
  const d = buscarCodigo_(planes_().map(leer_), PRUEBA_IG);
  if (!d) throw new Error('No encontré la fila ' + PRUEBA_IG);
  const file = archivo_(d.f.v(d.i, 'video'));
  console.log('Video: ' + file.getName() + ' · ' + (file.getSize() / 1048576).toFixed(1) + ' MB');
  const id = subirContenedor_(file, 'Prueba (no se publica)');
  console.log('Subido. Contenedor ' + id + '. Esperando a Instagram…');
  for (let k = 0; k < 12; k++) {
    Utilities.sleep(15000);
    const st = graph_('get', id, { fields: 'status_code,status' });
    console.log('Instagram dice: ' + st.status_code + ' · ' + (st.status || ''));
    if (st.status_code !== 'IN_PROGRESS') {
      avisar_(st.status_code === 'FINISHED' ? '✅ Instagram aceptó el video (no se publicó).' :
        '❌ Instagram: ' + st.status_code + ' · ' + (st.status || '') + pistaIG_(st.status));
      return;
    }
  }
  avisar_('Instagram sigue procesando después de 3 min. Vuelve a probar más tarde.');
}

/** Pregunta a Instagram si ya procesó el video; si sí, lo publica. Si no, sigue en la próxima vuelta. */
function revisar_(f, i) {
  const id = String(f.v(i, 'contenedor'));
  if (!id) throw new Error('Se perdió el contenedor: vuelve a poner Publicar');
  const st = graph_('get', id, { fields: 'status_code,status' }); // una sola pregunta: nada de esperas largas
  if (st.status_code === 'IN_PROGRESS') { f.set(i, 'link', 'Instagram procesando el video (sigue en 15 min)'); return; }
  if (st.status_code === 'PUBLISHED') { f.set(i, 'estado', 'Publicado'); f.set(i, 'contenedor', ''); return; } // ya salió en otra vuelta
  if (st.status_code !== 'FINISHED') throw new Error('Instagram: ' + st.status_code + ' · ' + (st.status || '') + pistaIG_(st.status));
  const pub = graph_('post', CONFIG.IG_ID + '/media_publish', { creation_id: id });
  const ahora = new Date();
  // Ya está publicado: se marca de una vez, para que un error de aquí en adelante nunca lo vuelva a publicar.
  f.set(i, 'estado', 'Publicado');
  f.set(i, 'contenedor', '');
  f.set(i, 'prod', 'Publicado');
  if (!(f.v(i, 'fecha') instanceof Date)) f.set(i, 'fecha', fechaDe_(dia_(ahora)));
  let link = 'Publicado (id ' + pub.id + ')';
  try { link = graph_('get', pub.id, { fields: 'permalink' }).permalink || link; } catch (e) { /* el link no es crítico */ }
  f.set(i, 'link', link);
  marcarEnCalendario_(f, i, ahora, link);
}

/** Evento "✅ Publicado · <título>" en el calendario principal: verde, sin notificaciones. Nunca rompe la publicación. */
function marcarEnCalendario_(f, i, cuando, link) {
  if (!CONFIG.MARCAR_CALENDARIO) return;
  try {
    const fin = new Date(cuando.getTime() + 15 * 60 * 1000);
    const yt = String(f.v(i, 'yt')) === 'Publicado' ? String(f.v(i, 'ytlink')) : '';
    const tt = ['En borradores', 'Publicado'].includes(String(f.v(i, 'tt'))) ? String(f.v(i, 'tt')) : '';
    const desc = 'Redes: Instagram (' + CONFIG.CUENTA + ')' + (yt ? ' · YouTube Shorts' : '') +
      (tt ? ' · TikTok (' + tt.toLowerCase() + ')' : '') + '\n' +
      'Hora: ' + Utilities.formatDate(cuando, tz_(), 'dd/MM/yyyy HH:mm') + '\n' +
      'Video en Drive: ' + (f.v(i, 'video') || '—') + '\n' +
      'Instagram: ' + link + (yt ? '\nYouTube: ' + yt : '');
    const ev = CalendarApp.getDefaultCalendar().createEvent('✅ Publicado · ' + titulo_(f, i), cuando, fin, { description: desc });
    ev.setColor(CalendarApp.EventColor.GREEN);
    ev.removeAllReminders();
  } catch (e) {
    console.log('No se pudo marcar en Calendar: ' + (e.message || e));
  }
}

/** Al poner "Publicar" arranca de una vez; si cambia el plan o el mes del calendario, repinta. */
function alEditar(e) {
  const r = e && e.range;
  if (!r) return;
  if (String(e.value) === 'Publicar') { publicarPendientes(); return; }
  const nombre = r.getSheet().getName();
  if (nombre === CAL || planes_().some(p => p.sh.getName() === nombre)) pintarCalendario();
}

/* ---------- 4. Calendario ---------- */

const ESTILO = {
  'Idea': ['⚪', '#6b7280'], 'Grabado': ['🟠', '#c2410c'], 'Editado': ['🟡', '#a16207'],
  'Listo para aprobar': ['🔵', '#1d4ed8'], 'Programado': ['🟣', '#6d28d9'], 'Publicado': ['🟢', '#047857'],
  'Error': ['🔴', '#b91c1c']
};

function etapa_(pub, prod, video) {
  if (pub === 'Publicado') return 'Publicado';
  if (['Publicar', 'Programado', 'Publicando'].includes(pub)) return 'Programado';
  if (pub === 'Listo') return 'Listo para aprobar';
  if (pub === 'Error') return 'Error';
  if (pub === 'Escribiendo descripción' || video || /editad/i.test(prod)) return 'Editado';
  if (/grabad/i.test(prod)) return 'Grabado';
  return 'Idea';
}

function pintarCalendario() {
  const ss = SpreadsheetApp.getActive(), tz = tz_(), hoy = new Date();
  const icono = t => CONFIG.TIPOS[t] ? CONFIG.TIPOS[t] + ' ' : '';
  const ev = [], sinFecha = [];
  planes_().map(leer_).forEach(f => f.vals.forEach((r, i) => {
    const titulo = titulo_(f, i);
    if (!titulo) return;
    const est = f.v(i, 'estado'), fe = f.v(i, 'fecha'), tipo = String(f.v(i, 'tipo')).trim();
    const e = { hora: f.d(i, 'hora'), etapa: etapa_(est, f.v(i, 'prod'), f.v(i, 'video')),
      url: ss.getUrl() + '#gid=' + f.sh.getSheetId() + '&range=A' + (i + 2) };
    if (fe instanceof Date) ev.push(Object.assign(e, { dia: dia_(fe), titulo: icono(tipo) + titulo }));
    else if (est !== 'Publicado') sinFecha.push(Object.assign(e, { titulo: (f.v(i, 'codigo') ? f.v(i, 'codigo') + ' · ' : '') + icono(tipo) + titulo }));
  }));

  const etiqueta = d => MESES[d.getMonth()] + ' ' + d.getFullYear();
  let sh = ss.getSheetByName(CAL);
  if (!sh) {
    sh = ss.insertSheet(CAL, 0);
    sh.setHiddenGridlines(true);
    for (let c = 1; c <= 7; c++) sh.setColumnWidth(c, 190);
    sh.getRange('A1').setFontSize(15).setFontWeight('bold').setFontColor(CONFIG.COLOR);
    sh.getRange('F1').setValue('Mes →').setHorizontalAlignment('right').setFontColor('#6b7280');
    sh.getRange('G1').setFontWeight('bold').setBackground('#f3f4f6');
    sh.setFrozenRows(3);
  }
  const opciones = [];
  for (let k = -2; k <= 6; k++) opciones.push(etiqueta(new Date(hoy.getFullYear(), hoy.getMonth() + k, 1)));
  sh.getRange('G1').setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(opciones, true).build());
  sh.getRange('A1').setValue('CALENDARIO INSTAGRAM · ' + CONFIG.CUENTA);
  const g1 = sh.getRange('G1');
  let ref = g1.getValue();
  if (!(ref instanceof Date)) {
    const sel = String(ref).trim().split(/\s+/);
    const m = MESES.map(norm_).indexOf(norm_(sel[0]));
    ref = m >= 0 ? new Date(Number(sel[1]) || hoy.getFullYear(), m, 1) : hoy;
  }
  const mes = ref.getMonth(), anio = ref.getFullYear();
  g1.setNumberFormat('@').setValue(etiqueta(new Date(anio, mes, 1)));

  sh.getRange(2, 1, 1, 7).setValues([Object.keys(ESTILO).map(k => ESTILO[k][0] + ' ' + k)]).setFontSize(9).setFontColor('#374151');
  sh.getRange(3, 1, 1, 7).setValues([['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']])
    .setFontWeight('bold').setBackground(CONFIG.COLOR).setFontColor('#ffffff').setHorizontalAlignment('center');

  const porDia = {};
  ev.forEach(e => (porDia[e.dia] = porDia[e.dia] || []).push(e));
  Object.values(porDia).forEach(l => l.sort((a, b) => String(a.hora).localeCompare(String(b.hora))));

  const enlaces = (lista, largo) => {
    let texto = '';
    const tramos = [];
    lista.forEach(e => {
      const [punto, col] = ESTILO[e.etapa] || ESTILO['Idea'];
      const ini = texto.length + (texto ? 1 : 0);
      texto += (texto ? '\n' : '') + punto + ' ' + (e.hora && e.dia ? e.hora + ' · ' : '') + String(e.titulo).slice(0, largo);
      tramos.push({ ini, fin: texto.length, col, url: e.url });
    });
    const rt = SpreadsheetApp.newRichTextValue().setText(texto);
    tramos.forEach(t => rt.setLinkUrl(t.ini, t.fin, t.url)
      .setTextStyle(t.ini, t.fin, SpreadsheetApp.newTextStyle().setForegroundColor(t.col).setUnderline(false).build()));
    return rt.build();
  };

  const primero = new Date(anio, mes, 1);
  const inicio = new Date(anio, mes, 1 - ((primero.getDay() + 6) % 7)); // lunes de la primera semana
  const SEMANAS = 6, hoyClave = dia_(hoy);
  sh.getRange(4, 1, Math.max(sh.getMaxRows() - 3, 1), 9).breakApart().clear();
  for (let w = 0; w < SEMANAS; w++) {
    const nums = [], conts = [], bn = [], bc = [];
    for (let d = 0; d < 7; d++) {
      const fecha = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate() + w * 7 + d);
      const clave = Utilities.formatDate(fecha, tz, 'yyyy-MM-dd'), delMes = fecha.getMonth() === mes;
      nums.push(String(fecha.getDate()) + (clave === hoyClave ? '  · HOY' : ''));
      bn.push(!delMes ? '#f9fafb' : clave === hoyClave ? '#fde68a' : '#f3f4f6');
      conts.push(enlaces(delMes ? (porDia[clave] || []) : [], 70));
      bc.push(delMes ? '#ffffff' : '#f9fafb');
    }
    const fila = 4 + w * 2;
    sh.getRange(fila, 1, 1, 7).setValues([nums]).setBackgrounds([bn]).setFontWeight('bold').setFontSize(9)
      .setFontColor('#374151').setHorizontalAlignment('left');
    sh.getRange(fila + 1, 1, 1, 7).setRichTextValues([conts]).setBackgrounds([bc]).setWrap(true)
      .setVerticalAlignment('top').setFontSize(10);
    sh.setRowHeight(fila, 20);
    sh.setRowHeight(fila + 1, 90);
  }
  sh.getRange(4, 1, SEMANAS * 2, 7).setBorder(true, true, true, true, true, false, '#e5e7eb', SpreadsheetApp.BorderStyle.SOLID);

  sh.getRange(3, 9).clear();
  if (sinFecha.length) {
    sh.setColumnWidth(8, 24);
    sh.setColumnWidth(9, 330);
    sh.getRange(3, 9).setValue('SIN FECHA (' + sinFecha.length + ')').setFontWeight('bold').setBackground(CONFIG.COLOR)
      .setFontColor('#ffffff').setHorizontalAlignment('center');
    sh.getRange(4, 9, SEMANAS * 2, 1).merge();
    sh.getRange(4, 9).setRichTextValue(enlaces(sinFecha, 60)).setFontSize(9).setWrap(true).setVerticalAlignment('top');
  }
  const pie = 4 + SEMANAS * 2 + 1;
  const sueltos = PropertiesService.getScriptProperties().getProperty('SUELTOS');
  sh.getRange(pie, 1).setValue(sueltos ? 'Videos en la carpeta sin código (renómbralos con su v…): ' + sueltos : '')
    .setFontColor('#b91c1c').setFontSize(9);
  sh.getRange(pie + 1, 1).setValue('Actualizado ' + Utilities.formatDate(new Date(), tz, 'dd/MM HH:mm') +
    ' · clic en un título para ir a su fila').setFontColor('#9ca3af').setFontSize(8);
}

/* ---------- utilidades ---------- */

function graph_(metodo, ruta, params) {
  params = Object.assign({ access_token: token_() }, params);
  const opts = { method: metodo, muteHttpExceptions: true };
  let url = GRAPH + '/' + ruta;
  if (metodo === 'get') url += '?' + Object.keys(params).map(k => k + '=' + encodeURIComponent(params[k])).join('&');
  else opts.payload = params;
  const body = JSON.parse(UrlFetchApp.fetch(url, opts).getContentText());
  if (body.error) {
    const vencido = body.error.code === 190 ? ' (el token venció o es inválido: genera uno nuevo y cámbialo en META_TOKEN)' : '';
    throw new Error('Meta: ' + (body.error.error_user_msg || body.error.message) + vencido);
  }
  return body;
}

function token_() {
  const t = String(PropertiesService.getScriptProperties().getProperty('META_TOKEN') || '').trim().replace(/^"|"$/g, '');
  if (!t) throw new Error('Falta META_TOKEN en Configuración del proyecto › Propiedades del script');
  return t;
}

function idDe_(link) {
  const m = String(link || '').match(/[-\w]{25,}/);
  return m ? m[0] : '';
}

function avisar_(msg) {
  console.log(msg);
  try { SpreadsheetApp.getActive().toast(msg, 'Plan IG', 8); } catch (e) { /* sin hoja abierta */ }
}
