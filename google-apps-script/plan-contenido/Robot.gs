/**
 * Robot de edición · parte 1 (Apps Script, gratis, sin tokens) — 11 nov 2026
 *
 * Cada 15 min mira "Edición de videos › 1. Videos en frío". Por cada crudo NUEVO:
 *   - saca su código del nombre ("v8.mov", "E1 toma.mov" → v8 / e1). Si no trae código pero trae fecha
 *     ("10 nov", "Vid 9 nov") se toma como Noticias IA del día siguiente (las noticias son del día anterior).
 *   - busca la fila de esa pieza en la pestaña del mes (columna #) → Estado = "Grabado".
 *   - agrega una fila en COLA POR EDITAR: Estado "Por editar", link del crudo, código, tipo y título.
 * La parte 2 es una tarea programada de Claude (contexto/robot-edicion.md): lee la COLA, edita lo "Por editar",
 * sube a "2. Videos terminados", deja la fila en "Listo" (NUNCA "Publicar") y avisa "🎬 <código> listo, míralo".
 *
 * Instalar: pegar este archivo en el proyecto de la hoja y ejecutar UNA vez instalarRobot().
 */

const ROBOT = {
  CARPETA_FRIO: '1GFl-0CSYI8afA0tzKGa0AVmM7FC-d4ON', // ContentIA › Edición de videos › 1. Videos en frío
  PROP: 'ROBOT_VISTOS'                              // ids de crudos ya registrados (para no repetir)
};

function instalarRobot() {
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'vigilarVideosEnFrio').forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('vigilarVideosEnFrio').timeBased().everyMinutes(15).create();
  // Los crudos que ya están hoy en la carpeta cuentan como vistos (ya se editaron a mano).
  const ids = listarVideos_(DriveApp.getFolderById(ROBOT.CARPETA_FRIO)).map(v => v.id);
  PropertiesService.getScriptProperties().setProperty(ROBOT.PROP, JSON.stringify(ids));
  avisar_('Robot instalado: vigila Videos en frío cada 15 min (' + ids.length + ' crudos marcados como vistos)');
}

function vigilarVideosEnFrio() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    const props = PropertiesService.getScriptProperties();
    const vistos = new Set(JSON.parse(props.getProperty(ROBOT.PROP) || '[]'));
    const nuevos = listarVideos_(DriveApp.getFolderById(ROBOT.CARPETA_FRIO))
      .filter(v => !vistos.has(v.id)).sort((a, b) => a.creado - b.creado);
    if (!nuevos.length) return;
    const planes = planes_().map(leer_);
    const cola = SpreadsheetApp.getActive().getSheetByName(COLA);
    nuevos.forEach(v => {
      const destino = filaDelCrudo_(planes, v.nombre, v.creado);
      let cod = '', tipo = 'Sin clasificar', titulo = v.nombre;
      if (destino) {
        const { f, i } = destino;
        cod = String(f.v(i, 'codigo')).trim();
        tipo = String(f.v(i, 'tipo') || 'Noticias IA');
        titulo = titulo_(f, i);
        if (!/editad|publicad/i.test(f.v(i, 'prod'))) f.set(i, 'prod', 'Grabado');
      }
      if (cola) {
        const fila = Math.max(cola.getLastRow() + 1, 4);
        cola.getRange(fila, 1, 1, 8).setValues([[new Date(), cod || '?', tipo, titulo, v.url, 'Videos en frío', '', 'Por editar']]);
      }
      vistos.add(v.id);
      avisar_('📥 Crudo recibido: ' + v.nombre + (cod ? ' → ' + cod : ' (sin código: revisar)'));
    });
    props.setProperty(ROBOT.PROP, JSON.stringify(Array.from(vistos).slice(-300)));
  } finally {
    lock.releaseLock();
  }
}

/** Fila de la pieza: primero por código ("v8 …"); si no, por fecha en el nombre ("10 nov" → noticias del 11 nov). */
function filaDelCrudo_(planes, nombre, creado) {
  const cod = codigoDe_(nombre);
  if (cod) return buscarCodigo_(planes, cod);
  const meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  const m = norm_(nombre).match(/(\d{1,2})\s*(?:de\s*)?(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)/);
  if (!m) return null;
  const dia = new Date(creado.getFullYear(), meses.indexOf(m[2]), Number(m[1]) + 1);
  const clave = Utilities.formatDate(dia, 'America/Bogota', 'dd/MM/yyyy');
  for (const f of planes) for (let i = 0; i < f.vals.length; i++) {
    const fecha = f.v(i, 'fecha');
    const txt = fecha instanceof Date ? Utilities.formatDate(fecha, 'America/Bogota', 'dd/MM/yyyy') : String(fecha).trim();
    if (txt === clave && /noticias/i.test(String(f.v(i, 'tipo') || 'Noticias IA'))) return { f, i };
  }
  return null;
}
