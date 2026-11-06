/**
 * YouTube.gs · Publica en YouTube Shorts la misma fila que se aprueba para Instagram.
 *
 * Va en el MISMO proyecto de Apps Script de la hoja (junto a Code.gs y Subidas.gs).
 * Necesita el servicio avanzado "YouTube Data API v3" (identificador: YouTube) y el permiso
 * https://www.googleapis.com/auth/youtube en appsscript.json.
 *
 * Cómo funciona (no hay que hacer nada distinto en la hoja):
 *  - Cuando una fila está aprobada ("Publicar" / "Programado") y llega su fecha y hora, publicarPendientes
 *    sube primero el video a YouTube y después lo publica en Instagram.
 *  - Columna "YouTube": vacía = va a YouTube con Instagram · "No" = no subir · "Publicar" = subirla ya
 *    (sirve para videos que ya salieron en Instagram) · el script pone "Subiendo", "Publicado" o "Error".
 *  - Columna "Título YouTube": opcional. Vacía = la primera línea de la descripción (el gancho).
 *  - Nunca se reintenta solo: si queda "Error" o "Subiendo", se revisa y se vuelve a poner "Publicar".
 */

const YT = {
  ACTIVO: true,                  // false = apaga YouTube sin tocar Instagram
  PRIVACIDAD: 'public',          // 'public' · 'unlisted' · 'private'
  CATEGORIA: '28',               // Ciencia y tecnología
  IDIOMA: 'es',
  ESTADOS: ['Publicar', 'Pendiente', 'No', 'Subiendo', 'Publicado', 'Error'],
  COLUMNAS: ['Título YouTube', 'YouTube', 'Link YouTube']
};

/** Agrega las columnas de YouTube a las pestañas del plan que no las tengan (al final, sin mover nada). */
function prepararYouTube_() {
  planes_().forEach(f => {
    const h = encabezados_(f.sh);
    const n = f.sh.getMaxRows() - 1;
    YT.COLUMNAS.forEach(nombre => {
      if (h[norm_(nombre)]) return;
      const c = f.sh.getLastColumn() + 1;
      if (c > f.sh.getMaxColumns()) f.sh.insertColumnAfter(f.sh.getMaxColumns());
      f.sh.getRange(1, c).setValue(nombre).setFontWeight('bold').setBackground('#1f2937').setFontColor('#ffffff');
      f.sh.setColumnWidth(c, nombre === 'YouTube' ? 110 : 220);
      if (nombre === 'YouTube') {
        f.sh.getRange(2, c, n).setDataValidation(SpreadsheetApp.newDataValidation()
          .requireValueInList(YT.ESTADOS, true).setAllowInvalid(true).build());
        f.sh.getRange(1, c).setNote('Vacía = sale en YouTube junto con Instagram. "No" = no subir. ' +
          '"Publicar" = subirla ya (para videos que ya salieron en Instagram). Lo demás lo pone el script.');
      }
      if (nombre === 'Título YouTube') f.sh.getRange(1, c).setNote('Opcional, máx. 100 letras. Vacía = primera línea de la descripción.');
      h[norm_(nombre)] = c;
    });
  });
}

/** Revisa que YouTube esté conectado y muestra el canal. No sube nada. */
function probarYouTube() {
  prepararYouTube_();
  const r = YouTube.Channels.list('snippet,status', { mine: true });
  if (!r.items || !r.items.length) throw new Error('Esta cuenta de Google no tiene canal de YouTube: créalo en youtube.com › Crear un canal');
  const c = r.items[0];
  avisar_('YouTube conectado: ' + c.snippet.title + (c.snippet.customUrl ? ' (' + c.snippet.customUrl + ')' : '') +
    ' · columnas listas en la hoja');
}

/**
 * Lo llama publicarPendientes para cada fila, antes de Instagram. Nunca rompe la publicación de Instagram.
 * aprobada = la fila ya llegó a su hora y está en Publicar / Programado.
 */
function youtubeFila_(f, i, aprobada) {
  if (!YT.ACTIVO || !f.col.yt) return;
  const est = String(f.v(i, 'yt')).trim();
  // "Pendiente" = Instagram ya arrancó con esta fila y YouTube va en la vuelta siguiente (lo pone publicarPendientes).
  if (!(est === 'Publicar' || est === 'Pendiente' || (est === '' && aprobada))) return;
  f.set(i, 'yt', 'Subiendo');
  SpreadsheetApp.flush(); // si el script se corta a mitad, la fila queda "Subiendo" y no se sube dos veces
  try {
    const file = archivo_(f.v(i, 'video'));
    const v = YouTube.Videos.insert({
      snippet: {
        title: tituloYouTube_(f, i), description: descripcionYouTube_(f, i), tags: hashtags_(f.v(i, 'desc')),
        categoryId: YT.CATEGORIA, defaultLanguage: YT.IDIOMA, defaultAudioLanguage: YT.IDIOMA },
      status: { privacyStatus: YT.PRIVACIDAD, selfDeclaredMadeForKids: false, embeddable: true }
    }, 'snippet,status', file.getBlob());
    const link = 'https://youtube.com/shorts/' + v.id;
    f.set(i, 'yt', 'Publicado');
    // YouTube deja privados los videos subidos desde proyectos de API sin verificar: se avisa en la fila.
    const priv = v.status && v.status.privacyStatus;
    f.set(i, 'ytlink', priv && priv !== YT.PRIVACIDAD ? link + ' · ⚠ YouTube lo dejó ' + priv : link);
  } catch (e) {
    f.set(i, 'yt', 'Error');
    f.set(i, 'ytlink', ('YouTube: ' + (e.message || e)).slice(0, 300));
  }
}

/** Título: columna "Título YouTube" o la primera línea de la descripción, sin hashtags, máx. 100 letras. */
function tituloYouTube_(f, i) {
  let t = String(f.v(i, 'yttitulo') || '').trim();
  if (!t) t = String(f.v(i, 'desc')).split('\n').map(s => s.replace(/#[\p{L}\d_]+/gu, '').trim()).filter(Boolean)[0] || titulo_(f, i);
  t = t.replace(/[<>]/g, '').replace(/\s+/g, ' ').trim();
  return t.length > 100 ? t.slice(0, 99).trim() + '…' : t;
}

/** Descripción de Instagram + #Shorts (YouTube la reconoce como Short por ser vertical y corta). */
function descripcionYouTube_(f, i) {
  const d = String(f.v(i, 'desc')).replace(/[<>]/g, '').trim();
  return (/#shorts\b/i.test(d) ? d : d + '\n\n#Shorts').slice(0, 4900);
}

function hashtags_(texto) {
  return (String(texto).match(/#[\p{L}\d_]+/gu) || []).map(h => h.slice(1))
    .filter((h, k, l) => !/^shorts$/i.test(h) && l.findIndex(x => x.toLowerCase() === h.toLowerCase()) === k).slice(0, 15);
}
