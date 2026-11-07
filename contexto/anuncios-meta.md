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

## Tracker + reporte diario (acordado 7 nov)
- **Hoja "Tracker de anuncios"** (en Anuncios (Meta); ID a `drive.md` cuando se cree):
  - Pestaña **Anuncios**: una fila por anuncio → código, nombre, video, fecha de inicio, presupuesto diario,
    estado (Activo / Pausado), veredicto de rentabilidad inicial.
  - Pestaña **Diario**: una fila por anuncio y por día → fecha, código, gasto, alcance, impresiones, frecuencia,
    % que ve 3 s (gancho), % que lo ve completo, clics, CTR, leads/agendas, costo por lead, semáforo (verde/amarillo/rojo).
  - El script llena la pestaña Diario solo cada mañana con los datos de Meta.
- **Documento diario** "Reporte de anuncios · <fecha>" (Drive › Anuncios (Meta) › 5. Reportes): resumen del día,
  cada anuncio comparado con los días anteriores, recomendación **Seguir / Vigilar / Pausar** con razones. 100% sincero.
- Los primeros 3–4 días Meta está "aprendiendo": no se juzga un anuncio por un solo día.
- **Santi (o su equipo) decide.** Si dice "pausa el A1", Claude lo pausa. Claude nunca pausa por su cuenta.
- Falta definir con Santi: costo por lead objetivo (para el semáforo) y hora del reporte (propuesta: 8:00 a. m.).

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

## Lista para montar la automatización (7 nov; Santi no pone anuncios todavía)
| # | Paso | Quién | Estado |
|---|---|---|---|
| 1 | Cuenta publicitaria **ContentIA Ads** creada 7 nov en el portfolio **soysanti__content_ia** (zona America/Bogota, divisa **USD**). Santi con acceso total. Sin método de pago | Santi | ✅ ID `act_1449021934086792` |
| 2 | App "Publicador Santi" (`1462889889116914`): agregar producto **Marketing API** | Santi | ⏳ |
| 3 | **Usuario del sistema** (admin) en el negocio + asignarle cuenta publicitaria, página, IG y la app | Santi | ⏳ |
| 4 | Token del usuario del sistema (no vence) con `ads_management`, `ads_read`, `business_management` → Propiedades del script `META_ADS_TOKEN` | Santi (guiado) | ⏳ |
| 5 | **Píxel** (Administrador de eventos › Conjunto de datos) → ID a este archivo | Santi | ⏳ |
| 6 | Hoja **Tracker de anuncios** (pestañas Anuncios y Diario) + carpeta `5. Reportes` | Claude | ⏳ |
| 7 | `Anuncios.gs`: reporte diario, subir en pausa, pausar a pedido | Claude | ⏳ |
| 8 | Píxel en la web (`src/`) | Claude | ⏳ |
| 9 | Prueba: campaña y anuncio **en pausa** (sin gastar) | Claude + Santi | ⏳ |
Portfolio comercial (negocio): **soysanti__content_ia** (2 páginas, 2 personas). Hay 2 negocios vacíos "Prueba 1" y "Prueba 1.1": no se usan.
Cuenta publicitaria: **ContentIA Ads**, ID `1449021934086792` (en la API: `act_1449021934086792`).
Datos (no secretos) cuando existan: ID de cuenta publicitaria (`act_…`), ID del píxel, ID del usuario del sistema.
