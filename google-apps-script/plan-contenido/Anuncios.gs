/**
 * Anuncios (Meta) · ContentIA
 * Token: Propiedades del script › META_ADS_TOKEN (usuario del sistema "ig contentia"). Nunca en este código.
 * Regla: este código NUNCA activa anuncios ni toca presupuesto. Solo lee, crea en pausa y pausa a pedido de Santi.
 */
const ADS = {
  CUENTA: 'act_1449021934086792', // ContentIA Ads (USD, America/Bogota)
};

function adsToken_() {
  const t = String(PropertiesService.getScriptProperties().getProperty('META_ADS_TOKEN') || '').trim().replace(/^"|"$/g, '');
  if (!t) throw new Error('Falta META_ADS_TOKEN en Configuración del proyecto › Propiedades del script');
  return t;
}

/** Prueba de solo lectura: no crea ni cambia nada. */
function probarAnuncios() {
  const url = 'https://graph.facebook.com/v23.0/' + ADS.CUENTA +
    '?fields=name,account_status,currency,timezone_name&access_token=' + encodeURIComponent(adsToken_());
  const r = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  const b = JSON.parse(r.getContentText());
  if (b.error) {
    console.log('❌ Meta: ' + b.error.message + ' (código ' + b.error.code + ')');
    return;
  }
  const estados = { 1: 'activa', 2: 'deshabilitada', 3: 'sin método de pago / pendiente', 7: 'en revisión', 9: 'en periodo de gracia', 101: 'cerrada' };
  console.log('✅ Conectado a la cuenta publicitaria "' + b.name + '" · ' + b.currency + ' · ' + b.timezone_name +
    ' · estado: ' + (estados[b.account_status] || b.account_status));
}
