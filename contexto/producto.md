# Producto: lo que se entrega al cliente (borrador 6 nov 2026)

El cliente recibe **el mismo sistema que usa Santi** (sus redes son la prueba). Hasta el 18 nov: hacer muchas pruebas
con los videos de Santi para dejarlo estable y venderlo. Clase 1 a 1: la da Santi por ahora.

## Requisitos del cliente
- Cuenta de Google (Drive, Sheets, Apps Script: gratis).
- **Claude con Claude Code** (plan Max ~$100/mes si edita video seguido; Pro $20 si no).
- Instagram profesional + página de Facebook (para publicar), canal de YouTube, cuenta de TikTok.

## Carpetas de Drive plantilla (lo que se copia por cliente)
| Carpeta | Qué lleva | Viene de |
|---|---|---|
| 0. Sistema | Code.gs, YouTube.gs, TikTok.gs, appsscript.json + LÉEME de instalación | `google-apps-script/plan-contenido/` |
| Plan de contenido (hoja) | Pestañas del mes, COLA POR EDITAR, CAL IG, columnas de YouTube/TikTok | hoja de Santi, vacía |
| Guiones | Ideas / Guiones en frío / Guiones terminados + plantilla de guion | `contexto/guiones.md` |
| Edición de videos | 1. Videos en frío / 2. Videos terminados + LÉEME | `areas/5-edicion-videos` |
| Recursos | Guía de edición y reglas por red (con "Ajustes del cliente") | `drive-respaldo/recursos/` |
| Repositorio de Claude | Memoria (CLAUDE.md), skills, editor de video | este repo, versión plantilla |

## Módulos del curso en Skool (borrador)
1. **Bienvenida**: qué es el Cerebro y cómo se ve funcionando (sin mostrar herramientas en redes, aquí sí se explican).
2. **Instalación (semana 1)**: copiar carpetas, conectar Instagram/Meta, YouTube, TikTok, pegar el Apps Script, probar.
3. **Carga**: llenar la marca, referentes, B-roll, guía de edición propia.
4. **Rutina diaria**: guion → grabar → subir a "Videos en frío" → Claude edita → revisar → programar.
5. **Gestor IA**: cómo revisar y aprobar (checklist), qué corregir, cuándo poner "Publicar".
6. **Problemas comunes**: token vencido, video privado en YouTube, errores en la hoja.
7. **Bono**: análisis de la cuenta y opciones de mejora.

## Tracker de alumnos (pedido de Santi, 6 nov)
- Cada módulo de Skool trae **tareas**. El tracker registra quién hizo qué y cuándo (ej. "Pepito hizo las tareas del módulo 1 el sábado").
- Con esos datos se hace un **análisis por alumno** que se le entrega en la llamada semanal.
- Por definir: si sale de Skool (exportar o API) o de un Google Form por tarea → hoja "Tracker de alumnos".

## Después del 18 nov (no ahora)
- Método de pago de los $2.500 (aún no hay: Wompi, Mercado Pago, Stripe, PayPal, Hotmart…).
- Setter y closer: por ahora Santi hace todo.

## Por hacer antes del 18 nov
- [ ] Pruebas diarias: v3, v4… publicando solos en IG + YouTube (+ TikTok cuando esté).
- [ ] Crear la comunidad de Skool (Santi aún no la tiene).
- [ ] Versión "plantilla" de cada carpeta, sin datos de Santi (como la de Juanita).
- [ ] Grabar los módulos.
- [ ] Protección contra duplicar/compartir (`licencias.md`).
- [ ] **Tracker de alumnos** (tareas por módulo + análisis para la llamada semanal).
- [ ] **Landing:** mejoras y subirla (la web existe en `src/`); grabar el **video gratis** que va en la página → agendar llamada.

## Módulo de conexiones (decidido 9 nov, Santi)
El curso enseña al cliente a conectar SU Cerebro: crear su app de Meta (Instagram), conectar YouTube, TikTok a borradores (publica a mano hasta que la app pase la auditoría), y qué plan de Claude necesita. Pendiente: probarlo antes del primer cliente en una cuenta ajena (socia) con plan de $20, para saber cuánto gasta editar.
