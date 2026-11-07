# Anuncios (Meta) · cómo funciona y plan de automatización (7 nov 2026)

## Flujo acordado con Santi
1. Un video ya editado (orgánico, en Instagram › 4. Contenido editado) o un anuncio hecho desde guion (A1, A2…).
2. Santi dice en la carpeta 📁 Anuncios (Meta): "quiero subir este video a anuncios".
3. **Análisis de rentabilidad (100% sincero):** antes de subir nada, Claude le hace a Santi un reporte corto
   y le dice **Sí / No / Sí con cambios**, con las razones. Mira: números orgánicos del video (vistas,
   retención, guardados, compartidos), gancho en los primeros 3 s, si se entiende la oferta y si lleva a la
   llamada, duración, y si Meta lo podría rechazar. Si no es rentable, se dice claro y no se sube.
   Si Santi dice que sí: copia en Anuncios (Meta) › 4. Contenido editado con nombre
   `<MERCADO>_<ÁNGULO>_<código>_v<n>.mp4` (el orgánico se queda igual). **No se cambia el CTA** (regla de Santi, 7 nov).
4. Un script sube el video a Meta y crea el anuncio **EN PAUSA** (cuando esté instalado).
5. **Santi pone presupuesto y le da Activar.** Sin su clic no se gasta nada.
6. **Apagar un anuncio:** si Santi dice "apaga el A1", Claude lo **pausa** por la API (no lo borra; se puede
   volver a prender). Antes confirma cuál es (nombre + gasto de hoy). Claude **nunca** activa, sube presupuesto
   ni crea gasto: eso solo lo hace Santi.
7. Reporte diario: gasto, leads, costo por lead, retención → hoja + aviso corto.

## Orden para montarlo
1. Primera campaña a mano (Santi aprende Ads Manager).
2. Reporte diario (sin riesgo).
3. Subida automática en pausa.
4. Reglas automáticas de Meta (ej. pausar si gasta $X sin leads) — se configuran en Ads Manager.

## Qué falta
- Cuenta publicitaria en Meta Business conectada a Instagram.
- Píxel de Meta en la web (`src/`) para medir quién agenda.
- Permiso `ads_management` / `ads_read` en el token de Meta (hoy `META_TOKEN` solo publica en IG).
- Hoja "Anuncios" (una fila por anuncio). IDs a `drive.md` cuando exista.

## Campaña sugerida
1 campaña (objetivo: agendar llamada) · 1 público amplio · 3–5 anuncios · solo ubicaciones de Instagram.
