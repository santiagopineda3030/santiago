\# Prompt · Sistema de plan de contenido orgánico de Instagram para una marca nueva  
  
\> \*\*Cómo usarlo:\*\* pega este documento completo en una conversación nueva con Claude (Claude Code o claude.ai con  
\> los conectores de Google Drive y Google Sheets) y escribe debajo: \*"Móntale este sistema a la marca \_\_\_"\*.  
\> Claude primero hace las preguntas de la sección 1 y después arma todo.  
  
\---  
  
\#\# Tu tarea, Claude  
  
Vas a montarle a una marca un sistema de plan de contenido orgánico para \*\*Instagram (Reels)\*\* en una sola hoja de  
Google Sheets, con un Apps Script adentro. Es una copia probada de un sistema que ya funciona; no lo rediseñes:  
respeta las columnas, los estados y el flujo tal como están aquí. Solo cambian los datos de la marca.  
  
El sistema son \*\*3 pestañas\*\* y \*\*una tarea diaria tuya\*\*:  
  
| Pieza | Para qué |  
|---|---|  
| \*\*Pestaña del mes\*\* (Noviembre, Diciembre…) | El plan: una fila por idea, desde la idea hasta el link publicado |  
| \*\*COLA POR EDITAR\*\* | Los crudos grabados, en fila para el editor |  
| \*\*CAL IG\*\* | Calendario visual del mes, pintado solo desde el plan |  
| Tarea diaria de descripciones | Claude escribe la descripción de cada video editado y lo deja "Listo" |  
  
\#\#\# El flujo en una línea por paso  
1\. La marca llena ideas en la pestaña del mes (ángulo, referente, explicación, guion, tipo; fecha si ya la sabe).  
 El script le pone a cada idea un \*\*código\*\* en la columna \`\#\`: v1, v2, v3…  
2\. Graban. El crudo entra a \*\*COLA POR EDITAR\*\* con el código de su idea; la idea pasa a \`Grabado\`.  
3\. El editor edita y sube el video terminado a la \*\*carpeta de editados\*\* con el código al inicio del nombre:  
 \`v7 1.0 tema.mp4\` (la versión corregida: \`v7 1.1 tema.mp4\`). Marca la fila de la cola como \`Entregado\`.  
4\. Cada hora el script encuentra el video, lo pega en la fila de su idea y deja \*\*Publicación =  
 \`Escribiendo descripción\`\*\*.  
5\. Tu tarea diaria escribe la descripción y la pasa a \*\*\`Listo\`\*\*. El script le pone fecha sola (siguiente día libre  
 según la plantilla semanal) y la hora por defecto.  
6\. La persona responsable revisa y cambia Publicación a \*\*\`Publicar\`\*\*. Si la fecha ya pasó, sale de una; si no, queda  
 \*\*\`Programado\`\*\* y sale ese día y hora. El link del post vuelve a la fila (\`Publicado\`).  
7\. \*\*CAL IG\*\* muestra todo el mes con colores por etapa y la lista de ideas sin fecha.  
  
\---  
  
\#\# 1. Primero pregunta esto a la marca (y nada más)  
  
Haz estas preguntas en un solo mensaje, cortas, con un ejemplo en cada una. No sigas hasta tener las respuestas  
de los puntos 1 a 6; los demás tienen valor por defecto.  
  
1\. \*\*Cuenta de Instagram:\*\* ¿cuál es el @? ¿Es cuenta profesional (Empresa o Creador) y está vinculada a una página de  
 Facebook? ¿Quién tiene acceso de administrador a esa página en Meta Business? \*(Sin esto no se puede publicar  
 solo; el resto del sistema sí funciona.)\*  
2\. \*\*Tipos de contenido (pilares):\*\* 3 a 6 tipos, cada uno con un emoji. Ej.: Educativo ð · Historia de cliente ð¢ ·  
 Opinión ð£️ · Tendencia ð¥ · Detrás de cámaras ð¤.  
3\. \*\*Frecuencia y plantilla semanal:\*\* ¿qué días se publica y qué tipo va cada día? Ej.: lunes Educativo, miércoles  
 Opinión, viernes Tendencia. Un día sin tipo = ese día no se publica.  
4\. \*\*Hora de publicación\*\* por defecto y \*\*zona horaria\*\* (ej. 18:30, America/Bogota).  
5\. \*\*Quién edita\*\* y quién aprueba (el que pone \`Publicar\`). ¿El editor tiene acceso a Drive de la marca?  
6\. \*\*Carpeta de Drive:\*\* dónde vive el contenido. Si no hay, propón esta estructura y créala:  
 \`Contenido \<Marca\>/1. Guiones\` · \`2. Crudo sin editar/\<mes aa\>\` · \`3. Recursos\` · \`4. Contenido editado/\<MES AAAA\>\`.  
7\. \*\*Descripciones:\*\* la llamada a la acción fija del cierre (ej. "Comenta GUÍA y te la envío ð"), cuántos hashtags  
 (por defecto 5), tono (tuteo/usted, país) y palabras prohibidas. Si tienen 2–3 descripciones que les gustaron,  
 pídelas como modelo.  
8\. \*\*Código inicial:\*\* ¿ya numeraban videos? Si sí, el siguiente número libre. Si no, empieza en v1.  
9\. \*\*Cuenta de Google\*\* dueña de la hoja (la que instala el script y recibe los permisos).  
  
Si algo no lo saben, usa el valor por defecto y anótalo en la pestaña del mes como nota del encabezado.  
  
\---  
  
\#\# 2. Estructura exacta de cada pestaña  
  
\> El script crea las tres pestañas solo (función \`instalar\`). Esta sección es la referencia para revisar que  
\> quedaron bien y para quien las quiera crear a mano. \*\*No cambies los nombres de los encabezados:\*\* el script  
\> encuentra las columnas por nombre (sin importar tildes ni mayúsculas), así que el orden se puede mover, el  
\> nombre no.  
  
\#\#\# 2.1 Pestaña del mes — nombre = el mes en español: \`Noviembre\`, \`Diciembre\`…  
Fila 1 encabezados (congelada), una fila por idea desde la 2. Una pestaña por mes; el script reconoce como "plan"  
toda pestaña que tenga las columnas \`\#\`, \`Link Video Editado\` y \`Publicación\`.  
  
| Col | Encabezado | Qué va | Quién lo llena | Validación / formato |  
|---|---|---|---|---|  
| A | \*\*Fecha\*\* | Día en que sale | La marca, o el script al quedar \`Listo\` | Fecha \`dd/mm/aaaa\` |  
| B | \*\*Estado\*\* | Estado de producción | La marca; el script pone \`Editado\` y \`Publicado\` | Lista: Idea · Guion · Grabado · Editado · Publicado |  
| C | \*\*Ángulo\*\* | El enfoque o gancho en pocas palabras | La marca | Texto |  
| D | \*\*Referente\*\* | Link al reel de ejemplo a seguir en la edición | La marca | Link |  
| E | \*\*Explicación\*\* | De qué trata, en 1–2 frases | La marca | Texto ajustado |  
| F | \*\*Guion\*\* | Título del guion o el guion completo | La marca | Texto ajustado |  
| G | \*\*Elementos adicionales\*\* | Gráficos, textos en pantalla, música… para el editor | La marca | Texto |  
| H | \*\*Link Video Editado\*\* | Link de Drive del video final | El script | Link (sirve también un chip de Drive) |  
| I | \*\*Descripción de Instagram\*\* | El caption completo con hashtags | Claude (tarea diaria) | Texto ajustado |  
| J | \*\*\#\*\* | Código de la idea: v1, v2… | El script (a toda fila con ángulo, explicación o guion) | Texto |  
| K | \*\*Archivo\*\* | Nombre del archivo del video | El script | Texto |  
| L | \*\*Hora\*\* | Hora de salida (\`18:30\` o \`6:30 pm\`) | La marca o el script | Texto plano (\`@\`) |  
| M | \*\*Publicación\*\* | Estado de publicación | Script + la persona que aprueba | Lista (abajo) |  
| N | \*\*Link publicado\*\* | Link del post, o el mensaje de error | El script | Link |  
| O | \*\*Tipo\*\* | Pilar de contenido | La marca | Lista = los tipos de la marca |  
| P | \*\*contenedor\*\* | Uso interno del script | El script | \*\*Oculta\*\* |  
  
\*\*Estados de Publicación (columna M):\*\*  
  
| Estado | Quién lo pone | Qué significa |  
|---|---|---|  
| \`Escribiendo descripción\` | Script | Llegó el video; falta la descripción |  
| \`Listo\` | Claude | Descripción escrita; el script le asigna fecha. Espera aprobación |  
| \`Publicar\` | \*\*La persona que aprueba\*\* | Aprobado: sale ya o en su fecha |  
| \`Programado\` | Script | Aprobado con fecha futura |  
| \`Publicando\` | Script | Instagram está procesando el video |  
| \`Publicado\` | Script | Salió; el link queda en la columna N |  
| \`Error\` | Script | Algo falló; el motivo queda en la columna N. Se corrige y se vuelve a poner \`Publicar\` |  
  
Colores (formato condicional en M): Publicado verde, Programado/Publicar morado, Listo azul, Escribiendo  
descripción amarillo, Error rojo.  
  
\*\*Plantilla semanal por tipo:\*\* vive en el script (\`CONFIG.PLANTILLA\`). Al asignar fecha, cada video busca el  
siguiente día libre cuyo tipo coincida con el suyo; nunca pone el mismo tipo dos días seguidos; si en 90 días no  
hay un día de su tipo, toma cualquier día de publicación libre. Las fechas que la marca escribe a mano se respetan  
y cuentan como ocupadas.  
  
\#\#\# 2.2 COLA POR EDITAR  
Filas 1–2 contadores, fila 3 encabezados (congeladas), datos desde la fila 4.  
  
\- \*\*Fila 1:\*\* A1 título · C1:G1 \`Por editar\` · \`Editando\` · \`Revisión\` · \`Corrección\` · \`Entregados 7 días\` ·  
 H1 instrucción corta del flujo.  
\- \*\*Fila 2:\*\* contadores: \`=CONTAR.SI(H4:H;C1)\` … y en G2 \`=CONTAR.SI.CONJUNTO(H4:H;"Entregado";K4:K;"\>="&(HOY()-7))\`  
 (el script los escribe en inglés y Sheets los traduce solo).  
  
| Col | Encabezado | Qué va | Validación |  
|---|---|---|---|  
| A | \*\*Subido\*\* | Fecha en que entró el crudo | Fecha |  
| B | \*\*Código\*\* | El \`\#\` de la idea del plan (v7). Vacío si no tiene idea | Texto |  
| C | \*\*Categoría\*\* | Tipo de contenido | Lista: los tipos de la marca + B-roll · Recurso · Sin clasificar |  
| D | \*\*Título\*\* | Corto (≤50 caracteres), dice de qué trata | Texto |  
| E | \*\*Crudo\*\* | Link de Drive del crudo | Link |  
| F | \*\*Carpeta\*\* | Link a la carpeta donde quedó | \`=HYPERLINK("\<link\>";"\<nombre corto\>")\` |  
| G | \*\*Instrucciones\*\* | 1–2 líneas para el editor: qué es, referente, "guion en la fila del dd/mm" | Texto ajustado |  
| H | \*\*Estado\*\* | Dónde va la pieza | Lista estricta: Por editar · Editando · Revisión · Corrección · Entregado · Archivado · Descartado |  
| I | \*\*Corrección\*\* | Lo que hay que cambiar (y "Hecho: 1.1" cuando se corrige) | Texto ajustado |  
| J | \*\*Editado (link)\*\* | Link del video entregado | Link |  
| K | \*\*Entregado\*\* | Fecha de entrega | Fecha |  
| L | \*\*Notas\*\* | Libre (pagos al editor, observaciones) | Texto |  
  
\*\*Reglas de la cola:\*\*  
\- Una fila por pieza final. Varias tomas de lo mismo = una fila ("3 tomas; usar la 2").  
\- B-roll y recursos van en \`Archivado\` (no se editan, quedan para usar).  
\- Si un crudo no encaja con ninguna idea: Código vacío e Instrucciones empieza con "Sin idea en el plan:".  
\- Cuando un crudo entra con código, la idea del plan pasa a \`Grabado\` (si estaba en Idea o Guion).  
\- El editor entrega subiendo el video a la carpeta de editados \*\*con el código al inicio del nombre\*\*; eso es lo que  
 conecta la cola con el plan. Pegar el link en J y poner \`Entregado\` es para llevar la cuenta.  
\- Organizar los crudos (opcional, si la marca quiere): la marca sube todo a una carpeta "crudo organizar" y tú, con el  
 conector de Drive, miras cada archivo, decides categoría, título e idea del plan, lo mueves a  
 \`2. Crudo sin editar/\<mes aa\>\` con el nombre \`\<código\> \<título\>\` y creas la fila. Nunca borres archivos; si dudas  
 entre dos ideas, deja el código vacío y escribe la duda en Instrucciones.  
  
\#\#\# 2.3 CAL IG  
La pinta el script (no se escribe a mano). Se repinta cada 15 min, cada hora y cada vez que se edita el plan.  
  
\- \*\*A1\*\* "CALENDARIO INSTAGRAM · @cuenta" · \*\*F1\*\* "Mes →" · \*\*G1\*\* selector del mes (lista: 2 meses atrás a 6  
 adelante). Cambiar G1 repinta ese mes.  
\- \*\*Fila 2\*\* leyenda: ⚪ Idea · ð  Grabado · ð¡ Editado · ðµ Listo para aprobar · ð£ Programado · ð¢ Publicado · ð´ Error.  
\- \*\*Fila 3\*\* LUNES … DOMINGO con el color de la marca.  
\- \*\*Filas 4–15:\*\* 6 semanas; por semana una fila con el número del día (hoy en amarillo, "· HOY") y una fila alta con  
 los posts: \`ð£ 18:30 · ð Título\`. Cada título es un link a su fila del plan.  
\- \*\*Columna I:\*\* "SIN FECHA (n)": las ideas sin fecha, con su código, en una celda alta.  
\- \*\*Pie:\*\* videos de la carpeta de editados que llegaron sin código (para renombrarlos) y hora de actualización.  
  
La etapa de cada idea sale de Publicación y Estado: Publicado → ð¢; Publicar/Programado/Publicando → ð£; Listo → ðµ;  
Error → ð´; Escribiendo descripción, con video o Estado Editado → ð¡; Estado Grabado → ð ; lo demás → ⚪.  
  
\---  
  
\#\# 3. Pasos para montarlo  
  
\#\#\# Paso 1 · Drive y la hoja (lo haces tú con los conectores)  
1\. Crear (o confirmar) las carpetas del punto 6 de las preguntas. Anotar el \*\*id de la carpeta  
 \`4. Contenido editado\`\*\* (lo que va después de \`/folders/\` en el link).  
2\. Crear la hoja \*\*"Plan contenido orgánico - \<Marca\>"\*\* en el Drive de la cuenta dueña. Configurarla en  
 \*Archivo › Configuración\* con la zona horaria de la marca y configuración regional Colombia/México/España según el  
 país (así las fechas salen \`dd/mm/aaaa\`).  
3\. No crees las pestañas a mano: el script las crea. Si la marca ya tiene ideas, después de instalar pégalas en la  
 pestaña del mes respetando las columnas.  
  
\#\#\# Paso 2 · Token de Meta (lo hace la persona con acceso; tú no lo ves)  
La API para publicar Reels necesita una cuenta profesional de Instagram vinculada a una página de Facebook y un  
token con permisos \`instagram\_basic\`, \`instagram\_content\_publish\`, \`pages\_show\_list\` y \`pages\_read\_engagement\`.  
1\. En \*\*Meta Business › Configuración del negocio › Usuarios del sistema\*\*, crear un usuario del sistema  
 (administrador), asignarle la página y la cuenta de Instagram, y \*\*Generar token\*\* con esos permisos para una app  
 de la marca (si no tienen app, crear una tipo "Negocio" en developers.facebook.com). Elegir que no caduque.  
2\. Para el \*\*IG\_ID\*\*: en el Explorador de la API Graph, con ese token, consultar  
 \`me/accounts?fields=name,instagram\_business\_account\`; el número de \`instagram\_business\_account.id\` es el IG\_ID  
 (empieza por 1784…).  
3\. \*\*Nunca pidas el token por chat ni lo escribas en la hoja, en un documento o en el código.\*\* Va únicamente en las  
 Propiedades del script (paso 3).  
  
\#\#\# Paso 3 · Instalar el Apps Script (≈5 min, lo hace la persona dueña de la hoja; tú guías)  
1\. En la hoja: \*\*Extensiones › Apps Script\*\*.  
2\. ⚙️ \*\*Configuración del proyecto\*\* › marcar "Mostrar el archivo de manifiesto appsscript.json". Volver al editor,  
 abrir \`appsscript.json\` y pegar el manifiesto de la sección 6 (cambiar \`timeZone\` por la de la marca).  
3\. Abrir \`Código.gs\`, borrar lo que haya y pegar el código de la sección 6. Llenar el bloque \*\*\`CONFIG\`\*\* con las  
 respuestas: \`CUENTA\`, \`IG\_ID\`, \`CARPETA\_EDITADOS\`, \`HORA\`, \`PRIMER\_CODIGO\`, \`TIPOS\` (nombre → emoji),  
 \`PLANTILLA\` (día → tipos; 0 = domingo), \`COLOR\`. Guardar (⌘S / Ctrl+S).  
4\. ⚙️ \*\*Configuración del proyecto › Propiedades del script › Agregar propiedad:\*\* nombre \`META\_TOKEN\`, valor = el  
 token. Guardar.  
5\. En el editor, elegir la función \*\*\`instalar\`\*\* y \*\*Ejecutar\*\* → aceptar permisos (Drive, Hojas, conexión externa,  
 activadores). Crea la pestaña del mes actual y la del siguiente, COLA POR EDITAR y CAL IG, los activadores  
 (publicar cada 15 min, traer videos cada hora, al editar) y muestra "Conectado a @cuenta".  
6\. Recargar la hoja: aparece el menú \*\*Plan IG\*\*.  
  
Si la marca todavía no tiene el token, se puede usar todo menos publicar: en \`instalar\` comenta la línea \`token\_();\`  
y \`probarConexion();\`, y cuando llegue el token se agrega la propiedad y se vuelve a ejecutar \`instalar\`.  
  
\#\#\# Paso 4 · La tarea diaria de descripciones (tú)  
Crea una tarea programada diaria (antes de la hora de publicación, ej. 7:00) con este prompt, rellenado con los datos  
de la marca:  
  
\`\`\`  
Hoja "Plan contenido orgánico - \<Marca\>" (\<ID de la hoja\>), conector de Google Sheets.  
1\. En las pestañas del mes (las que tienen en la fila 1 "\#", "Link Video Editado" y "Publicación") busca las filas con  
 Publicación = "Escribiendo descripción". Si no hay, termina diciendo "sin videos nuevos".  
2\. Para cada una, reúne el material: Explicación, Ángulo, Guion de la fila; el guion completo si hay un Google Doc  
 con ese título en \<carpeta de guiones\>; y, si tienes cómo transcribir el video, lo que se dice en él.  
3\. Escribe la descripción en "Descripción de Instagram":  
 - 3 a 5 líneas cortas. La primera es el gancho con la idea más fuerte de lo que se dice en el video. No inventes  
 datos: cifras solo si están en el video o el guion.  
 - Cierre fijo: "\<CTA de la marca\>".  
 - Al final \<N\> hashtags separados por espacio.  
 - Tono: \<tuteo/usted, país\>. Sin emojis salvo el del cierre. Palabras prohibidas: \<lista\>.  
 - Modelos aprobados: \<pegar 1–3 descripciones que le gustaron a la marca\>.  
4\. Cambia Publicación a "Listo". No toques ninguna otra columna ni filas en otro estado.  
5\. Reporte corto: cuántas descripciones, de qué ideas (código + título) y qué quedó pendiente y por qué.  
\`\`\`  
  
\#\#\# Paso 5 · Probarlo de punta a punta (tú, con la marca)  
1\. Escribir una idea de prueba en la pestaña del mes (Ángulo + Tipo). Menú \*\*Plan IG › Traer videos nuevos\*\*: debe  
 aparecerle un código v….  
2\. Subir un video corto (\<30 MB) a la carpeta de editados con nombre \`v\<código\> 1.0 prueba.mp4\`. Menú \*\*Traer  
 videos nuevos\*\*: la fila recibe link, archivo y \`Escribiendo descripción\`.  
3\. Escribir una descripción y poner \`Listo\` → \*\*Traer videos nuevos\*\*: aparece fecha y hora.  
4\. Mirar CAL IG: el post en su día con ðµ.  
5\. Solo si la marca quiere probar la publicación real: borrar la fecha, poner \`Publicar\` y esperar el link  
 (1–3 min). Si no, dejarlo en \`Listo\` y borrar la fila.  
6\. Explicarle a la marca, en 5 líneas, el uso diario (sección 4).  
  
\---  
  
\#\# 4. Uso diario (lo que le explicas a la marca)  
  
\- \*\*La marca:\*\* llena ideas en la pestaña del mes con Ángulo, Explicación, Guion, Referente y Tipo. Fecha opcional.  
\- \*\*Quien graba:\*\* sube los crudos; entran a COLA POR EDITAR con el código de su idea.  
\- \*\*El editor:\*\* trabaja la cola en orden; entrega subiendo a \`4. Contenido editado/\<MES AAAA\>\` con nombre  
 \`v\<código\> \<versión\> \<tema\>.mp4\` (1.0, 1.1…), máximo 30 MB (exportar H.264, \~6 Mbps); pega el link en la cola y  
 pone \`Entregado\`.  
\- \*\*Quien aprueba:\*\* revisa lo que está en ðµ Listo (video + descripción + fecha) y cambia Publicación a \`Publicar\`.  
 Para mover un post, cambia la fecha; para sacarlo de la programación, vuelve a poner \`Listo\`.  
\- \*\*Error:\*\* leer el motivo en Link publicado, corregir (video más liviano, descripción, link) y volver a \`Publicar\`.  
\- \*\*Mes nuevo:\*\* menú \*\*Plan IG › Crear pestaña del mes siguiente\*\* (hacerlo antes del día 25).  
\- \*\*Video que no cayó solo\*\* (sin código en el nombre): renombrarlo con su código, o pararse en la fila de la idea  
 y usar \*\*Plan IG › Unir video a esta fila por link…\*\*.  
\- \*\*Lo que la API de Instagram no hace\*\* (va a mano desde la app): música en tendencia, stickers, ubicación,  
 carruseles y fotos. Esos posts se publican desde la app y se marca la fila como \`Publicado\` con el link.  
  
\---  
  
\#\# 5. Qué queda fuera por ahora (no lo montes aunque lo veas en otros sistemas)  
\- \*\*Reels sacados de clases o sesiones en vivo\*\* (cascada de contenidos) y todo lo de sesiones en vivo.  
\- \*\*YouTube\*\* (banco de ideas, calendario de YouTube, títulos y miniaturas).  
\- \*\*Anuncios y VSL\*\* (su bandeja y su flujo de aprobación son otros).  
\- Pago al editor por pieza (calculadora, nómina), edición automática con IA, compresión automática de videos y  
 transcripción automática con scripts locales.  
\- Métricas del orgánico (alcance, seguidores, qué pilar funciona): es la siguiente fase, cuando haya 1–2 meses de  
 publicaciones.  
  
Si la marca pide alguna de estas, anótala como siguiente fase y termina primero las 3 pestañas.  
  
\---  
  
\#\# 6. Código  
  
\#\#\# appsscript.json  
\`\`\`json  
{  
 "timeZone": "America/Bogota",  
 "dependencies": {},  
 "exceptionLogging": "STACKDRIVER",  
 "runtimeVersion": "V8",  
 "oauthScopes": \[  
 "https://www.googleapis.com/auth/spreadsheets",  
 "https://www.googleapis.com/auth/drive",  
 "https://www.googleapis.com/auth/script.external\_request",  
 "https://www.googleapis.com/auth/script.scriptapp",  
 "https://www.googleapis.com/auth/script.container.ui"  
 \]  
}  
\`\`\`  
  
\#\#\# Código.gs  
\`\`\`javascript  
/\*\*  
 \* Plan de contenido orgánico de Instagram — Apps Script dentro de la hoja del plan  
 \* (Extensiones › Apps Script, con la cuenta dueña de la hoja).  
 \*  
 \* Tres pestañas:  
 \* - \<Mes\> (Noviembre, Diciembre…): una fila por idea. El script le pone código (\#: v1, v2…).  
 \* - COLA POR EDITAR: los crudos en fila para el editor (la llena el equipo o Claude).  
 \* - CAL IG: calendario mensual pintado desde el plan (cambia el mes en G1; clic en un título → su fila).  
 \*  
 \* Flujo:  
 \* 1. El editor sube el video terminado a CARPETA\_EDITADOS con el código al inicio del nombre: "v7 1.0 tema.mp4".  
 \* 2. traerVideosNuevos (cada hora): pega el link en la fila de esa idea → Publicación = "Escribiendo descripción"  
 \* (o "Listo" si ya tenía descripción).  
 \* 3. Claude escribe la descripción (tarea diaria) y la pasa a "Listo". Lo "Listo" sin fecha recibe el siguiente  
 \* día libre según la PLANTILLA semanal, a la HORA por defecto.  
 \* 4. La persona responsable cambia Publicación → "Publicar". Si la fecha ya pasó sale de una; si no, queda  
 \* "Programado" y sale ese día. El link publicado vuelve a la fila.  
 \*  
 \* Instalar: pegar este archivo y appsscript.json, llenar CONFIG, guardar META\_TOKEN en Propiedades del script  
 \* y ejecutar \`instalar\` una vez.  
 \*/  
  
const CONFIG = {  
 CUENTA: '@cuenta', // solo para el título del calendario  
 IG\_ID: '', // id de la cuenta profesional de Instagram (1784…)  
 CARPETA\_EDITADOS: '', // id de la carpeta de Drive donde el editor sube los videos terminados  
 HORA: '18:30', // hora por defecto (zona horaria de la hoja)  
 PRIMER\_CODIGO: 1, // v1 (si la marca ya usó códigos, empezar después)  
 MAX\_MB: 30, // Instagram falla con videos más pesados subidos desde Apps Script  
 // Tipos de contenido (pilares) con su ícono para el calendario  
 TIPOS: { 'Educativo': 'ð', 'Historia': 'ð¢', 'Opinión': 'ð£️', 'Viral': 'ð¥', 'Personal': 'ð¤' },  
 // Plantilla semanal: día (0 = domingo … 6 = sábado) → tipos de ese día. Día sin tipos = no se publica.  
 PLANTILLA: { 1: \['Educativo'\], 2: \['Historia'\], 3: \['Opinión'\], 4: \['Educativo'\], 5: \['Viral'\], 6: \['Personal'\], 0: \[\] },  
 COLOR: '\#be185d'  
};  
  
const GRAPH = 'https://graph.facebook.com/v23.0';  
const COLA = 'COLA POR EDITAR';  
const CAL = 'CAL IG';  
const MESES = \['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'\];  
  
const COLS\_MES = \['Fecha', 'Estado', 'Ángulo', 'Referente', 'Explicación', 'Guion', 'Elementos adicionales',  
 'Link Video Editado', 'Descripción de Instagram', '\#', 'Archivo', 'Hora', 'Publicación', 'Link publicado', 'Tipo', 'contenedor'\];  
const ESTADOS\_PROD = \['Idea', 'Guion', 'Grabado', 'Editado', 'Publicado'\];  
const PUB = \['Escribiendo descripción', 'Listo', 'Publicar', 'Programado', 'Publicando', 'Publicado', 'Error'\];  
const COLS\_COLA = \['Subido', 'Código', 'Categoría', 'Título', 'Crudo', 'Carpeta', 'Instrucciones', 'Estado', 'Corrección',  
 'Editado (link)', 'Entregado', 'Notas'\];  
const ESTADOS\_COLA = \['Por editar', 'Editando', 'Revisión', 'Corrección', 'Entregado', 'Archivado', 'Descartado'\];  
  
/\* ---------- Instalación y menú ---------- \*/  
  
function instalar() {  
 token\_();  
 if (\!CONFIG.IG\_ID || \!CONFIG.CARPETA\_EDITADOS) throw new Error('Llena IG\_ID y CARPETA\_EDITADOS en CONFIG');  
 const hoy = new Date();  
 crearMes\_(hoy);  
 crearMes\_(new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1));  
 crearCola\_();  
 ScriptApp.getProjectTriggers().forEach(t =\> ScriptApp.deleteTrigger(t));  
 ScriptApp.newTrigger('publicarPendientes').timeBased().everyMinutes(15).create();  
 ScriptApp.newTrigger('traerVideosNuevos').timeBased().everyHours(1).create();  
 ScriptApp.newTrigger('alEditar').forSpreadsheet(SpreadsheetApp.getActive()).onEdit().create();  
 const props = PropertiesService.getScriptProperties();  
 if (\!props.getProperty('DESDE')) props.setProperty('DESDE', new Date().toISOString());  
 probarConexion();  
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
 .addToUi();  
}  
  
function probarConexion() {  
 const c = graph\_('get', CONFIG.IG\_ID, { fields: 'username' });  
 const cupo = graph\_('get', CONFIG.IG\_ID + '/content\_publishing\_limit', { fields: 'quota\_usage,config' }).data\[0\];  
 avisar\_('Conectado a @' + c.username + ' · publicaciones hoy por API: ' + cupo.quota\_usage + ' de ' + cupo.config.quota\_total);  
}  
  
function crearMesSiguiente() {  
 const hoy = new Date();  
 crearMes\_(new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1));  
}  
  
/\*\* Pestaña del mes con encabezados, validaciones y formatos (no toca una que ya exista). \*/  
function crearMes\_(fecha) {  
 const ss = SpreadsheetApp.getActive(), nombre = MESES\[fecha.getMonth()\];  
 if (ss.getSheetByName(nombre)) return;  
 const sh = ss.insertSheet(nombre);  
 const n = sh.getMaxRows() - 1, col = k =\> COLS\_MES.indexOf(k) + 1;  
 sh.getRange(1, 1, 1, COLS\_MES.length).setValues(\[COLS\_MES\]).setFontWeight('bold')  
 .setBackground('\#1f2937').setFontColor('\#ffffff');  
 sh.setFrozenRows(1);  
 const lista = (l, estricto) =\> SpreadsheetApp.newDataValidation().requireValueInList(l, true).setAllowInvalid(\!estricto).build();  
 sh.getRange(2, col('Fecha'), n).setNumberFormat('dd/mm/yyyy')  
 .setDataValidation(SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(false).build());  
 sh.getRange(2, col('Estado'), n).setDataValidation(lista(ESTADOS\_PROD, true));  
 sh.getRange(2, col('Publicación'), n).setDataValidation(lista(PUB, true));  
 sh.getRange(2, col('Tipo'), n).setDataValidation(lista(Object.keys(CONFIG.TIPOS), true));  
 sh.getRange(2, col('Hora'), n).setNumberFormat('@');  
 \['Explicación', 'Guion', 'Descripción de Instagram'\].forEach(k =\> sh.getRange(2, col(k), n).setWrap(true));  
 \[95, 90, 130, 160, 220, 220, 160, 200, 320, 50, 160, 60, 150, 200, 110\].forEach((w, i) =\> sh.setColumnWidth(i + 1, w));  
 sh.hideColumns(col('contenedor'));  
 const r = sh.getRange(2, col('Publicación'), n);  
 sh.setConditionalFormatRules(\[\['Publicado', '\#d1fae5'\], \['Programado', '\#ede9fe'\], \['Publicar', '\#ede9fe'\],  
 \['Listo', '\#dbeafe'\], \['Escribiendo descripción', '\#fef3c7'\], \['Error', '\#fee2e2'\]\]  
 .map((\[t, c\]) =\> SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(t).setBackground(c).setRanges(\[r\]).build()));  
 sh.getRange(1, col('\#')).setNote('Lo pone el script. El editor empieza el nombre del archivo con este código: "v7 1.0 tema.mp4"');  
 sh.getRange(1, col('Publicación')).setNote('Solo cambia a "Publicar" cuando apruebes. Lo demás lo pone el script.');  
 sh.getRange(1, col('Hora')).setNote('Hora local, ej. 18:30. Vacía = ' + CONFIG.HORA + ' al asignar fecha.');  
}  
  
/\*\* COLA POR EDITAR: filas 1–2 contadores, fila 3 encabezados, datos desde la 4. \*/  
function crearCola\_() {  
 const ss = SpreadsheetApp.getActive();  
 if (ss.getSheetByName(COLA)) return;  
 const sh = ss.insertSheet(COLA);  
 sh.getRange('A1').setValue('COLA POR EDITAR · una fila por pieza').setFontWeight('bold').setFontSize(13);  
 sh.getRange('C1:G1').setValues(\[\['Por editar', 'Editando', 'Revisión', 'Corrección', 'Entregados 7 días'\]\]).setFontWeight('bold');  
 sh.getRange('C2:G2').setFormulas(\[\['=COUNTIF(H4:H,C1)', '=COUNTIF(H4:H,D1)', '=COUNTIF(H4:H,E1)', '=COUNTIF(H4:H,F1)',  
 '=COUNTIFS(H4:H,"Entregado",K4:K,"\>="&(TODAY()-7))'\]\]).setFontSize(14).setHorizontalAlignment('center');  
 sh.getRange('H1').setValue('Flujo: Por editar → Editando → Revisión → Corrección → Entregado. ' +  
 'El video final va a la carpeta de editados con el código al inicio del nombre.').setWrap(true).setFontColor('\#6b7280');  
 sh.getRange(3, 1, 1, COLS\_COLA.length).setValues(\[COLS\_COLA\]).setFontWeight('bold').setBackground('\#1f2937').setFontColor('\#ffffff');  
 sh.setFrozenRows(3);  
 const n = sh.getMaxRows() - 3;  
 const cat = Object.keys(CONFIG.TIPOS).concat(\['B-roll', 'Recurso', 'Sin clasificar'\]);  
 sh.getRange(4, 3, n).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(cat, true).build());  
 sh.getRange(4, 8, n).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(ESTADOS\_COLA, true).setAllowInvalid(false).build());  
 \[1, 11\].forEach(c =\> sh.getRange(4, c, n).setNumberFormat('dd/mm/yyyy'));  
 \[85, 60, 110, 260, 160, 160, 320, 100, 260, 160, 85, 140\].forEach((w, i) =\> sh.setColumnWidth(i + 1, w));  
 \[7, 9\].forEach(c =\> sh.getRange(4, c, n).setWrap(true));  
}  
  
/\* ---------- Lectura de las pestañas del mes ---------- \*/  
  
const norm\_ = s =\> String(s || '').toLowerCase().normalize('NFD').replace(/\[̀-ͯ\]/g, '').trim();  
  
function encabezados\_(sh) {  
 const m = {};  
 sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()\[0\].forEach((h, i) =\> { if (h \!== '') m\[norm\_(h)\] = i + 1; });  
 return m;  
}  
  
/\*\* Pestañas del plan: las que tienen "\#", "Link Video Editado" y "Publicación" en la fila 1. \*/  
function planes\_() {  
 return SpreadsheetApp.getActive().getSheets().map(sh =\> {  
 if (sh.getLastColumn() \< 2) return null;  
 const h = encabezados\_(sh);  
 if (\!h\['\#'\] || \!h\['link video editado'\] || \!h\['publicacion'\]) return null;  
 return { sh, col: {  
 fecha: h\['fecha'\], prod: h\['estado'\], angulo: h\['angulo'\], explicacion: h\['explicacion'\], guion: h\['guion'\],  
 video: h\['link video editado'\], desc: h\['descripcion de instagram'\], codigo: h\['\#'\], archivo: h\['archivo'\],  
 hora: h\['hora'\], estado: h\['publicacion'\], link: h\['link publicado'\], tipo: h\['tipo'\], contenedor: h\['contenedor'\] } };  
 }).filter(Boolean);  
}  
  
function leer\_(f) {  
 const n = f.sh.getLastRow() - 1, w = f.sh.getLastColumn();  
 f.vals = n \> 0 ? f.sh.getRange(2, 1, n, w).getValues() : \[\];  
 f.disp = n \> 0 ? f.sh.getRange(2, 1, n, w).getDisplayValues() : \[\];  
 f.v = (i, k) =\> f.col\[k\] ? f.vals\[i\]\[f.col\[k\] - 1\] : '';  
 f.d = (i, k) =\> f.col\[k\] ? f.disp\[i\]\[f.col\[k\] - 1\] : '';  
 f.set = (i, k, val) =\> {  
 if (\!f.col\[k\]) return;  
 f.vals\[i\]\[f.col\[k\] - 1\] = val;  
 const r = f.sh.getRange(i + 2, f.col\[k\]);  
 if (k === 'hora') r.setNumberFormat('@');  
 r.setValue(val);  
 if (k === 'hora') f.disp\[i\]\[f.col\[k\] - 1\] = String(val);  
 };  
 if (f.col.video) chips\_(f, n);  
 return f;  
}  
  
/\*\* Si pegaron un chip de Drive en "Link Video Editado", saca el link del chip (solo en memoria). \*/  
function chips\_(f, n) {  
 let ricos = null;  
 for (let i = 0; i \< n; i++) {  
 const val = String(f.vals\[i\]\[f.col.video - 1\] || '').trim();  
 if (\!val || idDe\_(val)) continue;  
 ricos = ricos || f.sh.getRange(2, f.col.video, n, 1).getRichTextValues();  
 const rt = ricos\[i\]\[0\];  
 const url = rt && (rt.getLinkUrl() || rt.getRuns().map(x =\> x.getLinkUrl()).filter(Boolean)\[0\] || '');  
 if (idDe\_(url)) f.vals\[i\]\[f.col.video - 1\] = url;  
 }  
}  
  
const titulo\_ = (f, i) =\> String(f.v(i, 'guion') || f.v(i, 'explicacion') || f.v(i, 'angulo')).replace(/\[“”"\]/g, '').trim();  
  
/\* ---------- 1. Videos del editor → fila de su idea ---------- \*/  
  
function traerVideosNuevos() {  
 const lock = LockService.getScriptLock();  
 if (\!lock.tryLock(30000)) return;  
 try {  
 const props = PropertiesService.getScriptProperties();  
 const desde = new Date(props.getProperty('DESDE') || 0);  
 const planes = planes\_().map(leer\_);  
 numerarIdeas\_(planes);  
 const usados = new Set();  
 planes.forEach(f =\> f.vals.forEach((r, i) =\> { const id = idDe\_(f.v(i, 'video')); if (id) usados.add(id); }));  
 let unidos = 0;  
 const sueltos = \[\];  
 listarVideos\_(DriveApp.getFolderById(CONFIG.CARPETA\_EDITADOS)).sort((a, b) =\> a.creado - b.creado).forEach(v =\> {  
 if (usados.has(v.id)) return;  
 const cod = codigoDe\_(v.nombre);  
 const destino = cod && buscarCodigo\_(planes, cod);  
 if (\!destino) { if (v.creado \>= desde) sueltos.push(v.nombre); return; }  
 const { f, i } = destino;  
 if (\['Publicar', 'Programado', 'Publicando', 'Publicado'\].includes(f.v(i, 'estado'))) return; // ya va en camino  
 const actual = idDe\_(f.v(i, 'video'));  
 if (actual) {  
 try { if (DriveApp.getFileById(actual).getDateCreated() \> v.creado) return; } catch (e) { /\* borrado \*/ }  
 }  
 f.set(i, 'video', v.url);  
 f.set(i, 'archivo', v.nombre);  
 if (\!/publicad/i.test(f.v(i, 'prod'))) f.set(i, 'prod', 'Editado');  
 f.set(i, 'estado', String(f.v(i, 'desc')).trim() ? 'Listo' : 'Escribiendo descripción');  
 usados.add(v.id);  
 unidos++;  
 });  
 props.setProperty('SUELTOS', sueltos.slice(-10).join(' · '));  
 asignarFechas\_(planes);  
 pintarCalendario();  
 if (unidos) avisar\_(unidos + ' video(s) unidos a su idea');  
 } finally {  
 lock.releaseLock();  
 }  
}  
  
function listarVideos\_(carpeta) {  
 const out = \[\];  
 (function recorrer(c) {  
 const files = c.getFiles();  
 while (files.hasNext()) {  
 const f = files.next();  
 if (/^video\\//.test(f.getMimeType())) out.push({ id: f.getId(), url: f.getUrl(), nombre: f.getName(), creado: f.getDateCreated() });  
 }  
 const subs = c.getFolders();  
 while (subs.hasNext()) recorrer(subs.next());  
 })(carpeta);  
 return out;  
}  
  
/\*\* "v7 1.0 tema.mp4" → "v7". \*/  
function codigoDe\_(nombre) {  
 const m = String(nombre).match(/^\\s\*v\\s\*0\*(\\d+)(?=\[\\s.\_-\]|$)/i);  
 return m ? 'v' + m\[1\] : '';  
}  
  
function buscarCodigo\_(planes, cod) {  
 for (const f of planes) for (let i = 0; i \< f.vals.length; i++) {  
 if (String(f.v(i, 'codigo')).toLowerCase().replace(/\\s/g, '') === cod) return { f, i };  
 }  
 return null;  
}  
  
/\*\* Ideas con contenido y sin código → siguiente código libre. \*/  
function numerarIdeas\_(planes) {  
 let max = CONFIG.PRIMER\_CODIGO - 1;  
 planes.forEach(f =\> f.vals.forEach((r, i) =\> {  
 const m = String(f.v(i, 'codigo')).match(/^v(\\d+)$/i);  
 if (m) max = Math.max(max, Number(m\[1\]));  
 }));  
 planes.forEach(f =\> f.vals.forEach((r, i) =\> {  
 if (f.v(i, 'codigo') || \!titulo\_(f, i)) return;  
 f.set(i, 'codigo', 'v' + (++max));  
 }));  
}  
  
/\*\* Unir un video a la fila donde está parado el cursor (por si el editor no puso el código). \*/  
function unirPorLink() {  
 const ui = SpreadsheetApp.getUi();  
 const sh = SpreadsheetApp.getActiveSheet(), fila = sh.getActiveRange().getRow();  
 const f = planes\_().find(p =\> p.sh.getName() === sh.getName());  
 if (\!f || fila \< 2) { ui.alert('Párate en la fila de la idea, en la pestaña del mes.'); return; }  
 const r = ui.prompt('Link del video en Drive', ui.ButtonSet.OK\_CANCEL);  
 if (r.getSelectedButton() \!== ui.Button.OK) return;  
 const file = DriveApp.getFileById(idDe\_(r.getResponseText()));  
 sh.getRange(fila, f.col.video).setValue(file.getUrl());  
 if (f.col.archivo) sh.getRange(fila, f.col.archivo).setValue(file.getName());  
 const desc = String(sh.getRange(fila, f.col.desc).getValue()).trim();  
 sh.getRange(fila, f.col.estado).setValue(desc ? 'Listo' : 'Escribiendo descripción');  
 pintarCalendario();  
}  
  
/\* ---------- 2. Fechas ---------- \*/  
  
const tz\_ = () =\> SpreadsheetApp.getActive().getSpreadsheetTimeZone();  
const dia\_ = d =\> Utilities.formatDate(d, tz\_(), 'yyyy-MM-dd');  
const fechaDe\_ = clave =\> Utilities.parseDate(clave + ' 12:00', tz\_(), 'yyyy-MM-dd HH:mm');  
const masDias\_ = (d, n) =\> new Date(d.getFullYear(), d.getMonth(), d.getDate() + n, 12);  
  
/\*\* A lo "Listo" sin fecha: siguiente día libre que le toque según la plantilla, sin repetir tipo dos días seguidos. \*/  
function asignarFechas\_(planes) {  
 const ocupados = {};  
 planes.forEach(f =\> f.vals.forEach((r, i) =\> {  
 const fe = f.v(i, 'fecha');  
 if (fe instanceof Date && f.v(i, 'estado') \!== 'Error') ocupados\[dia\_(fe)\] = String(f.v(i, 'tipo')).trim();  
 }));  
 const manana = masDias\_(new Date(), 1);  
 planes.forEach(f =\> f.vals.forEach((r, i) =\> {  
 if (f.v(i, 'estado') \!== 'Listo' || f.v(i, 'fecha') instanceof Date) return;  
 const tipo = String(f.v(i, 'tipo')).trim();  
 const d = diaLibre\_(manana, tipo, ocupados, true) || diaLibre\_(manana, tipo, ocupados, false) || manana;  
 ocupados\[dia\_(d)\] = tipo;  
 f.set(i, 'fecha', fechaDe\_(dia\_(d)));  
 if (\!String(f.d(i, 'hora')).trim()) f.set(i, 'hora', CONFIG.HORA);  
 }));  
}  
  
function diaLibre\_(desde, tipo, ocupados, estricto) {  
 const dias = Object.keys(CONFIG.PLANTILLA).filter(k =\> (CONFIG.PLANTILLA\[k\] || \[\]).length).map(Number);  
 for (let k = 0; k \< 90; k++) {  
 const d = masDias\_(desde, k);  
 if (dia\_(d) in ocupados || \!dias.includes(d.getDay())) continue;  
 if (estricto && \!CONFIG.PLANTILLA\[d.getDay()\].includes(tipo)) continue;  
 if (tipo && (ocupados\[dia\_(masDias\_(d, -1))\] === tipo || ocupados\[dia\_(masDias\_(d, 1))\] === tipo)) continue;  
 return d;  
 }  
 return null;  
}  
  
/\*\* Fecha de la celda + hora "18:30" / "6:30 pm" (zona de la hoja) → Date. Sin fecha = ya. \*/  
function cuando\_(fecha, hora) {  
 if (\!(fecha instanceof Date)) return new Date(0);  
 let h = 12, m = 0;  
 const t = String(hora).toLowerCase().match(/(\\d{1,2})(?::(\\d{2}))?\\s\*(\[ap\])?/);  
 if (t) {  
 h = Number(t\[1\]) % 24; m = Number(t\[2\] || 0);  
 if (t\[3\] === 'p' && h \< 12) h += 12;  
 if (t\[3\] === 'a' && h === 12) h = 0;  
 }  
 return Utilities.parseDate(dia\_(fecha) + ' ' + h + ':' + ('0' + m).slice(-2), tz\_(), 'yyyy-MM-dd H:mm');  
}  
  
/\* ---------- 3. Publicar ---------- \*/  
  
function publicarPendientes() {  
 const lock = LockService.getScriptLock();  
 if (\!lock.tryLock(1000)) return; // otra vuelta sigue corriendo  
 const inicio = Date.now();  
 try {  
 planes\_().map(leer\_).forEach(f =\> f.vals.forEach((r, i) =\> {  
 if (Date.now() - inicio \> 4 \* 60 \* 1000) return; // Apps Script corta a los 6 min: sigue en la próxima vuelta  
 const est = f.v(i, 'estado');  
 if (\!\['Publicar', 'Programado', 'Publicando'\].includes(est)) return;  
 try {  
 if (est === 'Publicando') { revisar\_(f, i); return; }  
 const file = archivo\_(f.v(i, 'video'));  
 if (\!String(f.v(i, 'desc')).trim()) throw new Error('Falta la descripción');  
 if (cuando\_(f.v(i, 'fecha'), f.d(i, 'hora')) \> new Date()) {  
 if (est \!== 'Programado') { f.set(i, 'estado', 'Programado'); f.set(i, 'link', ''); }  
 return;  
 }  
 subir\_(f, i, file);  
 revisar\_(f, i);  
 } catch (e) {  
 const msg = String(e.message || e);  
 const props = PropertiesService.getScriptProperties(), clave = 'reintentos\_' + idDe\_(f.v(i, 'video'));  
 const n = Number(props.getProperty(clave) || 0) + 1;  
 props.setProperty(clave, String(n));  
 // Instagram a veces falla al procesar: reintentar con un contenedor nuevo hasta 3 veces  
 if (/ProcessingFailed|ERROR/.test(msg) && n \<= 3) {  
 f.set(i, 'estado', 'Publicar'); f.set(i, 'link', 'Instagram falló al procesar: reintento ' + n + ' de 3');  
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
  
function archivo\_(link) {  
 const id = idDe\_(link);  
 let file = null;  
 try { file = id && DriveApp.getFileById(id); } catch (e) { file = null; }  
 if (\!file || \!/^video\\//.test(file.getMimeType())) throw new Error('Falta el link de un video de Drive');  
 return file;  
}  
  
/\*\* Crea el contenedor de Reel y le sube el video de Drive en un solo envío. \*/  
function subir\_(f, i, file) {  
 const mb = file.getSize() / 1048576;  
 if (mb \> CONFIG.MAX\_MB) throw new Error('El video pesa ' + Math.round(mb) + ' MB (máx. ' + CONFIG.MAX\_MB + '): exportarlo más liviano');  
 const c = graph\_('post', CONFIG.IG\_ID + '/media', {  
 media\_type: 'REELS', upload\_type: 'resumable', caption: String(f.v(i, 'desc')), share\_to\_feed: 'true' });  
 const r = UrlFetchApp.fetch(c.uri, {  
 method: 'post', contentType: 'application/octet-stream', payload: file.getBlob().getBytes(),  
 headers: { Authorization: 'OAuth ' + token\_(), offset: '0', file\_size: String(file.getSize()) },  
 muteHttpExceptions: true });  
 if (r.getResponseCode() \!== 200) throw new Error('Subida ' + r.getResponseCode() + ': ' + r.getContentText().slice(0, 200));  
 f.set(i, 'contenedor', c.id);  
 f.set(i, 'estado', 'Publicando');  
 f.set(i, 'link', 'Instagram procesando el video');  
}  
  
/\*\* Espera a que Instagram procese el video (hasta \~2 min por vuelta) y lo publica. \*/  
function revisar\_(f, i) {  
 const id = String(f.v(i, 'contenedor'));  
 if (\!id) throw new Error('Se perdió el contenedor: vuelve a poner Publicar');  
 let st;  
 for (let k = 0; k \< 12; k++) {  
 st = graph\_('get', id, { fields: 'status\_code,status' });  
 if (st.status\_code \!== 'IN\_PROGRESS') break;  
 Utilities.sleep(10000);  
 }  
 if (st.status\_code === 'IN\_PROGRESS') return; // sigue en la próxima vuelta  
 if (st.status\_code \!== 'FINISHED') throw new Error('Instagram: ' + st.status\_code + ' · ' + (st.status || ''));  
 const pub = graph\_('post', CONFIG.IG\_ID + '/media\_publish', { creation\_id: id });  
 const media = graph\_('get', pub.id, { fields: 'permalink' });  
 f.set(i, 'estado', 'Publicado');  
 f.set(i, 'link', media.permalink);  
 f.set(i, 'contenedor', '');  
 f.set(i, 'prod', 'Publicado');  
 if (\!(f.v(i, 'fecha') instanceof Date)) f.set(i, 'fecha', fechaDe\_(dia\_(new Date())));  
}  
  
/\*\* Al poner "Publicar" arranca de una vez; si cambia el plan o el mes del calendario, repinta. \*/  
function alEditar(e) {  
 const r = e && e.range;  
 if (\!r) return;  
 if (String(e.value) === 'Publicar') { publicarPendientes(); return; }  
 const nombre = r.getSheet().getName();  
 if (nombre === CAL || planes\_().some(p =\> p.sh.getName() === nombre)) pintarCalendario();  
}  
  
/\* ---------- 4. Calendario ---------- \*/  
  
const ESTILO = {  
 'Idea': \['⚪', '\#6b7280'\], 'Grabado': \['ð ', '\#c2410c'\], 'Editado': \['ð¡', '\#a16207'\],  
 'Listo para aprobar': \['ðµ', '\#1d4ed8'\], 'Programado': \['ð£', '\#6d28d9'\], 'Publicado': \['ð¢', '\#047857'\],  
 'Error': \['ð´', '\#b91c1c'\]  
};  
  
function etapa\_(pub, prod, video) {  
 if (pub === 'Publicado') return 'Publicado';  
 if (\['Publicar', 'Programado', 'Publicando'\].includes(pub)) return 'Programado';  
 if (pub === 'Listo') return 'Listo para aprobar';  
 if (pub === 'Error') return 'Error';  
 if (pub === 'Escribiendo descripción' || video || /editad/i.test(prod)) return 'Editado';  
 if (/grabad/i.test(prod)) return 'Grabado';  
 return 'Idea';  
}  
  
function pintarCalendario() {  
 const ss = SpreadsheetApp.getActive(), tz = tz\_(), hoy = new Date();  
 const icono = t =\> CONFIG.TIPOS\[t\] ? CONFIG.TIPOS\[t\] + ' ' : '';  
 const ev = \[\], sinFecha = \[\];  
 planes\_().map(leer\_).forEach(f =\> f.vals.forEach((r, i) =\> {  
 const titulo = titulo\_(f, i);  
 if (\!titulo) return;  
 const est = f.v(i, 'estado'), fe = f.v(i, 'fecha'), tipo = String(f.v(i, 'tipo')).trim();  
 const e = { hora: f.d(i, 'hora'), etapa: etapa\_(est, f.v(i, 'prod'), f.v(i, 'video')),  
 url: ss.getUrl() + '\#gid=' + f.sh.getSheetId() + '\&range=A' + (i + 2) };  
 if (fe instanceof Date) ev.push(Object.assign(e, { dia: dia\_(fe), titulo: icono(tipo) + titulo }));  
 else if (est \!== 'Publicado') sinFecha.push(Object.assign(e, { titulo: (f.v(i, 'codigo') ? f.v(i, 'codigo') + ' · ' : '') + icono(tipo) + titulo }));  
 }));  
  
 const etiqueta = d =\> MESES\[d.getMonth()\] + ' ' + d.getFullYear();  
 let sh = ss.getSheetByName(CAL);  
 if (\!sh) {  
 sh = ss.insertSheet(CAL, 0);  
 sh.setHiddenGridlines(true);  
 for (let c = 1; c \<= 7; c++) sh.setColumnWidth(c, 190);  
 sh.getRange('A1').setFontSize(15).setFontWeight('bold').setFontColor(CONFIG.COLOR);  
 sh.getRange('F1').setValue('Mes →').setHorizontalAlignment('right').setFontColor('\#6b7280');  
 sh.getRange('G1').setFontWeight('bold').setBackground('\#f3f4f6');  
 sh.setFrozenRows(3);  
 }  
 const opciones = \[\];  
 for (let k = -2; k \<= 6; k++) opciones.push(etiqueta(new Date(hoy.getFullYear(), hoy.getMonth() + k, 1)));  
 sh.getRange('G1').setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(opciones, true).build());  
 sh.getRange('A1').setValue('CALENDARIO INSTAGRAM · ' + CONFIG.CUENTA);  
 const g1 = sh.getRange('G1');  
 let ref = g1.getValue();  
 if (\!(ref instanceof Date)) {  
 const sel = String(ref).trim().split(/\\s+/);  
 const m = MESES.map(norm\_).indexOf(norm\_(sel\[0\]));  
 ref = m \>= 0 ? new Date(Number(sel\[1\]) || hoy.getFullYear(), m, 1) : hoy;  
 }  
 const mes = ref.getMonth(), anio = ref.getFullYear();  
 g1.setNumberFormat('@').setValue(etiqueta(new Date(anio, mes, 1)));  
  
 sh.getRange(2, 1, 1, 7).setValues(\[Object.keys(ESTILO).map(k =\> ESTILO\[k\]\[0\] + ' ' + k)\]).setFontSize(9).setFontColor('\#374151');  
 sh.getRange(3, 1, 1, 7).setValues(\[\['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'\]\])  
 .setFontWeight('bold').setBackground(CONFIG.COLOR).setFontColor('\#ffffff').setHorizontalAlignment('center');  
  
 const porDia = {};  
 ev.forEach(e =\> (porDia\[e.dia\] = porDia\[e.dia\] || \[\]).push(e));  
 Object.values(porDia).forEach(l =\> l.sort((a, b) =\> String(a.hora).localeCompare(String(b.hora))));  
  
 const enlaces = (lista, largo) =\> {  
 let texto = '';  
 const tramos = \[\];  
 lista.forEach(e =\> {  
 const \[punto, col\] = ESTILO\[e.etapa\] || ESTILO\['Idea'\];  
 const ini = texto.length + (texto ? 1 : 0);  
 texto += (texto ? '\\n' : '') + punto + ' ' + (e.hora && e.dia ? e.hora + ' · ' : '') + String(e.titulo).slice(0, largo);  
 tramos.push({ ini, fin: texto.length, col, url: e.url });  
 });  
 const rt = SpreadsheetApp.newRichTextValue().setText(texto);  
 tramos.forEach(t =\> rt.setLinkUrl(t.ini, t.fin, t.url)  
 .setTextStyle(t.ini, t.fin, SpreadsheetApp.newTextStyle().setForegroundColor(t.col).setUnderline(false).build()));  
 return rt.build();  
 };  
  
 const primero = new Date(anio, mes, 1);  
 const inicio = new Date(anio, mes, 1 - ((primero.getDay() + 6) % 7)); // lunes de la primera semana  
 const SEMANAS = 6, hoyClave = dia\_(hoy);  
 sh.getRange(4, 1, Math.max(sh.getMaxRows() - 3, 1), 9).breakApart().clear();  
 for (let w = 0; w \< SEMANAS; w++) {  
 const nums = \[\], conts = \[\], bn = \[\], bc = \[\];  
 for (let d = 0; d \< 7; d++) {  
 const fecha = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate() + w \* 7 + d);  
 const clave = Utilities.formatDate(fecha, tz, 'yyyy-MM-dd'), delMes = fecha.getMonth() === mes;  
 nums.push(String(fecha.getDate()) + (clave === hoyClave ? ' · HOY' : ''));  
 bn.push(\!delMes ? '\#f9fafb' : clave === hoyClave ? '\#fde68a' : '\#f3f4f6');  
 conts.push(enlaces(delMes ? (porDia\[clave\] || \[\]) : \[\], 70));  
 bc.push(delMes ? '\#ffffff' : '\#f9fafb');  
 }  
 const fila = 4 + w \* 2;  
 sh.getRange(fila, 1, 1, 7).setValues(\[nums\]).setBackgrounds(\[bn\]).setFontWeight('bold').setFontSize(9)  
 .setFontColor('\#374151').setHorizontalAlignment('left');  
 sh.getRange(fila + 1, 1, 1, 7).setRichTextValues(\[conts\]).setBackgrounds(\[bc\]).setWrap(true)  
 .setVerticalAlignment('top').setFontSize(10);  
 sh.setRowHeight(fila, 20);  
 sh.setRowHeight(fila + 1, 90);  
 }  
 sh.getRange(4, 1, SEMANAS \* 2, 7).setBorder(true, true, true, true, true, false, '\#e5e7eb', SpreadsheetApp.BorderStyle.SOLID);  
  
 sh.getRange(3, 9).clear();  
 if (sinFecha.length) {  
 sh.setColumnWidth(8, 24);  
 sh.setColumnWidth(9, 330);  
 sh.getRange(3, 9).setValue('SIN FECHA (' + sinFecha.length + ')').setFontWeight('bold').setBackground(CONFIG.COLOR)  
 .setFontColor('\#ffffff').setHorizontalAlignment('center');  
 sh.getRange(4, 9, SEMANAS \* 2, 1).merge();  
 sh.getRange(4, 9).setRichTextValue(enlaces(sinFecha, 60)).setFontSize(9).setWrap(true).setVerticalAlignment('top');  
 }  
 const pie = 4 + SEMANAS \* 2 + 1;  
 const sueltos = PropertiesService.getScriptProperties().getProperty('SUELTOS');  
 sh.getRange(pie, 1).setValue(sueltos ? 'Videos en la carpeta sin código (renómbralos con su v…): ' + sueltos : '')  
 .setFontColor('\#b91c1c').setFontSize(9);  
 sh.getRange(pie + 1, 1).setValue('Actualizado ' + Utilities.formatDate(new Date(), tz, 'dd/MM HH:mm') +  
 ' · clic en un título para ir a su fila').setFontColor('\#9ca3af').setFontSize(8);  
}  
  
/\* ---------- utilidades ---------- \*/  
  
function graph\_(metodo, ruta, params) {  
 params = Object.assign({ access\_token: token\_() }, params);  
 const opts = { method: metodo, muteHttpExceptions: true };  
 let url = GRAPH + '/' + ruta;  
 if (metodo === 'get') url += '?' + Object.keys(params).map(k =\> k + '=' + encodeURIComponent(params\[k\])).join('&');  
 else opts.payload = params;  
 const body = JSON.parse(UrlFetchApp.fetch(url, opts).getContentText());  
 if (body.error) throw new Error('Meta: ' + (body.error.error\_user\_msg || body.error.message));  
 return body;  
}  
  
function token\_() {  
 const t = PropertiesService.getScriptProperties().getProperty('META\_TOKEN');  
 if (\!t) throw new Error('Falta META\_TOKEN en Configuración del proyecto › Propiedades del script');  
 return t;  
}  
  
function idDe\_(link) {  
 const m = String(link || '').match(/\[-\\w\]{25,}/);  
 return m ? m\[0\] : '';  
}  
  
function avisar\_(msg) {  
 console.log(msg);  
 try { Spreadshe
