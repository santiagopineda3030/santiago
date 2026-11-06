# Código bueno Instagram · cómo instalarlo

Publica solo los Reels en Instagram desde una hoja de Google Sheets, a la fecha y hora de cada fila, y marca cada publicación en Google Calendar.

## Lo que necesitas antes
1. Una cuenta de Instagram **profesional** (creador o empresa) conectada a una **página de Facebook**.
2. Una app en developers.facebook.com (tipo Business) con el producto Instagram, y un **token de página** con estos permisos:
   instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement y business_management.
3. El **IG_ID** de tu cuenta, un número que empieza por 17841. Lo sacas en Graph API Explorer con:
   `me/accounts?fields=name,instagram_business_account{id,username}`
4. Una carpeta en Google Drive para los videos terminados. Su id es lo que va después de `/folders/` en el link.

## Instalar (unos 10 minutos)
1. Crea una hoja nueva de Google Sheets › **Extensiones** › **Apps Script**.
2. En **Code.gs** borra todo y pega el archivo `Code.gs` de esta carpeta.
3. Arriba, en `CONFIG`, llena **CUENTA**, **IG_ID** y **CARPETA_EDITADOS**. Si no estás en Colombia, cambia también la HORA.
4. ⚙️ **Configuración del proyecto**:
   - Marca "Mostrar el archivo de manifiesto appsscript.json" y pega el `appsscript.json` de esta carpeta. Si no estás en Colombia, cambia la zona horaria.
   - En **Propiedades del script**, agrega `META_TOKEN` con tu token de página. **El token nunca va en el código.**
5. Guarda. Elige la función **instalar** › **▶ Ejecutar** › acepta los permisos.
   Esto crea las pestañas del mes, la COLA POR EDITAR, el calendario y 3 tareas automáticas.
6. Elige **probarConexion** › **▶ Ejecutar**. Debe salir "Conectado a @tu_cuenta".

## Cómo se usa
1. Sube el video terminado a tu carpeta con el código al inicio del nombre (`v1 1.0 tema.mp4`).
2. Cada hora el script pone el link del video en la fila con ese código.
3. Escribe la descripción y pon **Publicación = Listo**. Si la fila no tiene fecha, el script le pone el siguiente día libre.
4. Cuando lo apruebes, pon **Publicar**. A la fecha y hora de la fila se publica solo (revisa cada 15 minutos).
5. Si sale **Error**, el motivo queda en "Link publicado".

Límites: videos de máximo 30 MB, en vertical, y hasta 100 publicaciones al día.
