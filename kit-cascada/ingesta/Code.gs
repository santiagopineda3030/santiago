/**
 * Cascada de contenidos — ingesta de grabaciones de Google Meet (Apps Script independiente).
 *
 * Flujo:
 *  1. Las sesiones se graban en Google Meet con transcripción activada. Meet deja el video, la
 *     transcripción y (si se activó) las notas de Gemini en "Meet Recordings" del organizador, o
 *     compartidos con los coanfitriones.
 *  2. buscarGrabaciones (cada 30 min): encuentra esos archivos por el título del evento (PATRON),
 *     los copia a "<CARPETA>/<fecha · título>", y deja el texto de la transcripción en la pestaña
 *     TRANSCRIPCIONES. La sesión queda "Por analizar".
 *  3. Claude (skill "cascada") lee la transcripción, escoge los clips según reglas.json, escribe el
 *     documento de la cascada y las filas de CASCADA, y marca la sesión "Cascada lista".
 *
 * Instalar: crear un proyecto en script.google.com con la cuenta que recibe las grabaciones, pegar
 * todo, cambiar las 4 constantes de abajo, guardar y ejecutar `instalar` una vez (pide permisos).
 */

const PATRON = 'Clase en vivo';           // palabras que siempre trae el título del evento de Calendar
const CARPETA = 'Grabaciones sesiones';   // carpeta de Drive donde quedan las sesiones (se crea en Mi unidad)
const HOJA_NOMBRE = 'Cascada de contenidos';
const TZ = 'America/Bogota';

const TROZO = 40000; // una celda de Sheets aguanta 50.000 caracteres
const COLS = {
  'SESIONES': ['id', 'fecha', 'titulo', 'estado', 'carpeta', 'video', 'transcripcion', 'notas_gemini', 'doc_cascada',
    'archivos_origen'],
  'TRANSCRIPCIONES': ['id_sesion', 'parte', 'texto'],
  'CASCADA': ['sesion', 'pieza', 'categoria', 'titulo', 'minutos', 'doc', 'estado', 'entregado', 'video_sesion',
    'descripcion', 'link_publicado']
};
const ESTADOS_SESION = ['Esperando transcripción', 'Por analizar', 'Cascada lista', 'Sin contenido'];
const ESTADOS_PIEZA = ['Por editar', 'Borrador IA', 'En edición', 'Entregado', 'Programado', 'Publicado', 'Descartado'];

/* ---------- Instalación ---------- */

function instalar() {
  const props = PropertiesService.getScriptProperties();
  let carpeta = props.getProperty('CARPETA_ID') && DriveApp.getFolderById(props.getProperty('CARPETA_ID'));
  if (!carpeta) {
    const ya = DriveApp.getRootFolder().getFoldersByName(CARPETA);
    carpeta = ya.hasNext() ? ya.next() : DriveApp.getRootFolder().createFolder(CARPETA);
    props.setProperty('CARPETA_ID', carpeta.getId());
  }
  let ss = props.getProperty('HOJA_ID') && SpreadsheetApp.openById(props.getProperty('HOJA_ID'));
  if (!ss) {
    ss = SpreadsheetApp.create(HOJA_NOMBRE);
    DriveApp.getFileById(ss.getId()).moveTo(carpeta);
    props.setProperty('HOJA_ID', ss.getId());
  }
  Object.keys(COLS).forEach(n => {
    const sh = ss.getSheetByName(n) || ss.insertSheet(n);
    sh.getRange(1, 1, 1, COLS[n].length).setValues([COLS[n]]).setFontWeight('bold').setBackground('#1f2937').setFontColor('#ffffff');
    sh.setFrozenRows(1);
    sh.getRange('A:Z').setNumberFormat('@').setVerticalAlignment('top');
  });
  ss.getSheets().filter(s => !COLS[s.getName()]).forEach(s => ss.deleteSheet(s));
  const lista = v => SpreadsheetApp.newDataValidation().requireValueInList(v, true).build();
  ss.getSheetByName('SESIONES').getRange('D2:D').setDataValidation(lista(ESTADOS_SESION));
  const cas = ss.getSheetByName('CASCADA');
  cas.getRange('G2:G').setDataValidation(lista(ESTADOS_PIEZA));
  cas.getRange('D:D').setWrap(true);
  cas.getRange('J:J').setWrap(true);

  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('buscarGrabaciones').timeBased().everyMinutes(30).create();

  Logger.log('Carpeta: ' + carpeta.getUrl());
  Logger.log('Hoja: ' + ss.getUrl());
  buscarGrabaciones();
}

/* ---------- Grabaciones nuevas → carpeta de la sesión + transcripción en la hoja ---------- */

function buscarGrabaciones() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;
  try {
    const ss = hoja();
    const sh = ss.getSheetByName('SESIONES');
    const sesiones = leer(sh);
    const vistos = new Set();
    sesiones.forEach(s => String(s.archivos_origen).split(',').filter(String).forEach(id => vistos.add(id)));

    const desde = Utilities.formatDate(new Date(Date.now() - 14 * 864e5), 'UTC', "yyyy-MM-dd'T'HH:mm:ss");
    const it = DriveApp.searchFiles("title contains '" + PATRON.replace(/'/g, "\\'") + "' and modifiedDate > '" + desde +
      "' and trashed = false");
    const nuevos = [];
    while (it.hasNext()) {
      const f = it.next();
      if (vistos.has(f.getId())) continue;   // las copias se llaman "Video · fecha": no traen PATRON
      const tipo = clase(f);
      if (tipo) nuevos.push({ f: f, clase: tipo });
    }
    nuevos.sort((a, b) => a.f.getDateCreated() - b.f.getDateCreated());

    nuevos.forEach(n => {
      const fecha = fechaDe(n.f);
      let s = sesiones.find(x => x.id === fecha);
      if (!s) {
        s = { id: fecha, fecha: fecha, titulo: tituloDe(n.f), estado: 'Esperando transcripción', archivos_origen: '' };
        const nombreSub = fecha + ' · ' + s.titulo;
        const ya = carpetaRaiz().getFoldersByName(nombreSub);
        s.carpeta = (ya.hasNext() ? ya.next() : carpetaRaiz().createFolder(nombreSub)).getUrl();
        s._fila = sh.getLastRow() + 1;
        sesiones.push(s);
      }
      const sub = DriveApp.getFolderById(idDe(s.carpeta));
      const nombre = { video: 'Video', transcripcion: 'Transcripción', notas: 'Notas de Gemini' }[n.clase] + ' · ' + fecha;
      let url;
      try {
        url = n.f.makeCopy(nombre, sub).getUrl();
      } catch (e) { // si el video es muy pesado para copiar, queda un acceso directo
        url = DriveApp.getFileById(sub.createShortcut(n.f.getId()).getId()).getUrl();
      }
      const col = { video: 'video', transcripcion: 'transcripcion', notas: 'notas_gemini' }[n.clase];
      s[col] = s[col] ? s[col] + '\n' + url : url;

      if (n.clase !== 'video') {
        // Meet a veces deja la transcripción como una pestaña dentro del Doc de notas de Gemini.
        textoDoc(n.f.getId()).forEach(t => {
          const etiqueta = /transcrip/i.test(t.titulo) || n.clase === 'transcripcion' ? 'transcripción' : 'notas gemini';
          guardarTexto(ss, fecha, etiqueta, t.texto);
          if (etiqueta === 'transcripción' && t.texto.trim() && /^(Esperando transcripción|)$/.test(s.estado)) s.estado = 'Por analizar';
        });
      }
      s.archivos_origen = [s.archivos_origen, n.f.getId()].filter(String).join(',');
      escribir(sh, s);
    });

    // Respaldo: 4 horas después sin transcripción pero con notas de Gemini → se analiza con las notas.
    sesiones.filter(s => s.estado === 'Esperando transcripción' && s.notas_gemini &&
      Date.now() - new Date(s.fecha + 'T23:59:00').getTime() > 0).forEach(s => {
      s.estado = 'Por analizar';
      escribir(sh, s);
    });
  } finally {
    lock.releaseLock();
  }
}

// Meet deja hasta tres archivos por grabación: video, transcripción (Doc) y notas de Gemini (Doc).
function clase(f) {
  const m = f.getMimeType();
  if (/^video\//.test(m)) return 'video';
  if (m === MimeType.GOOGLE_DOCS) return /gemini|notas|notes/i.test(f.getName()) ? 'notas' : 'transcripcion';
  return null;
}

function fechaDe(f) {
  const m = f.getName().match(/(\d{4})[-\/](\d{2})[-\/](\d{2})/);
  return m ? m[1] + '-' + m[2] + '-' + m[3] : Utilities.formatDate(f.getDateCreated(), TZ, 'yyyy-MM-dd');
}

// "Clase en vivo - 2026/10/27 17:02 GMT-05:00 - Recording" → "Clase en vivo"
function tituloDe(f) {
  return f.getName().split(/\s+-\s+\d{4}[\/-]/)[0].trim().slice(0, 60) || PATRON;
}

// Texto de cada pestaña del Doc (incluidas subpestañas): [{titulo, texto}].
function textoDoc(id) {
  const doc = DocumentApp.openById(id);
  if (!doc.getTabs) return [{ titulo: '', texto: doc.getBody().getText() }];
  const out = [];
  const recorrer = tabs => tabs.forEach(t => {
    if (t.getType() === DocumentApp.TabType.DOCUMENT_TAB) out.push({ titulo: t.getTitle(), texto: t.asDocumentTab().getBody().getText() });
    recorrer(t.getChildTabs());
  });
  recorrer(doc.getTabs());
  return out;
}

function guardarTexto(ss, id, etiqueta, texto) {
  const sh = ss.getSheetByName('TRANSCRIPCIONES');
  const trozos = [];
  for (let i = 0; i < texto.length; i += TROZO) trozos.push(texto.slice(i, i + TROZO));
  if (!trozos.length) trozos.push('(vacío)');
  const filas = trozos.map((t, i) => [id, etiqueta + ' ' + (i + 1) + '/' + trozos.length, t]);
  sh.getRange(sh.getLastRow() + 1, 1, filas.length, 3).setNumberFormat('@').setValues(filas);
}

/* ---------- utilidades ---------- */

function hoja() {
  return SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('HOJA_ID'));
}

function carpetaRaiz() {
  return DriveApp.getFolderById(PropertiesService.getScriptProperties().getProperty('CARPETA_ID'));
}

// Filas de una pestaña como objetos { columna: valor, _fila: n }.
function leer(sh) {
  const v = sh.getDataRange().getDisplayValues();
  const h = v[0];
  return v.slice(1).map((r, i) => {
    const o = { _fila: i + 2 };
    h.forEach((c, j) => o[c] = r[j]);
    return o;
  }).filter(o => o[h[0]]);
}

function escribir(sh, o) {
  const h = COLS[sh.getName()];
  sh.getRange(o._fila, 1, 1, h.length).setNumberFormat('@').setValues([h.map(c => o[c] == null ? '' : String(o[c]))]);
}

function idDe(url) {
  return (String(url).match(/[-\w]{25,}/) || [])[0];
}
