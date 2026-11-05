# Repartir el Cerebro a clientes sin que lo compartan (PLAN APROBADO, se monta al final)

Santiago lo aprobó el 5 nov 2026, pero **se construye cuando todo lo demás esté hecho**. No empezar antes.
Idea: no es quitarle el acceso a nadie, es que no lo compartan ni lo dupliquen.

## Regla de oro
Las carpetas siguen siendo de Santiago (dueño). Al cliente se le da acceso con su correo, no una copia suya.
En Drive nada se bloquea al 100 % (capturas, grabar pantalla): la idea es que compartir no sirva y que se sepa quién filtró.

## 3 carpetas por cliente (ContentIA › Clientes › <Nombre>)
1. **Material** (guías, clases, plantillas): solo lector, sin descargar/imprimir/copiar
   (`copyRequiresWriterPermission`), link restringido, **marca de agua** con nombre y correo en cada doc.
2. **Su sistema** (hoja del plan + script): editor sin poder compartir (`writersCanShare=false`).
   Protegido con **licencia**: el script del cliente es una cáscara; el trabajo lo hace el **motor** en la cuenta de
   Santiago, que valida licencia + ID de la hoja + correo + estado Activa. Una copia de la hoja no funciona.
   Los prompts nunca se entregan como texto.
3. **Su contenido** (crudos, guiones, editados): 100 % del cliente.

## Panel: hoja "Licencias"
Cliente · Correo · Licencia · Hoja · Estado (Activa/Suspendida) · Fecha.
Alta = un script crea las 3 carpetas desde una plantilla, pone candados, marca de agua y licencia.
Suspendida = quita accesos y el motor deja de trabajar para esa licencia.
Más una cláusula en el contrato: si comparte, pierde el acceso sin reembolso.

## Orden cuando se monte
1. Hoja de Licencias + "Alta de cliente" (Apps Script con Drive API v3 avanzado).
2. Motor con licencia (reescribir cómo se instala el script en cada cliente).
## Pendiente de definir
- Qué va exactamente en "Material". Si el cliente usa su Gmail o una cuenta nueva. Dónde van las clases grabadas.
