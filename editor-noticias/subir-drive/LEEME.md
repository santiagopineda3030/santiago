# Subir videos editados a Drive

El buzón **Subidas.gs** está instalado en el proyecto de Apps Script de la hoja
"Plan contenido orgánico - ContentIA" y publicado como aplicación web.

- Sube solo a `Edición de videos › 2. Videos terminados › <MES AAAA>` (antes Instagram › 4. Contenido editado; mismo ID) (la crea si no existe).
- Solo acepta nombres `v<código> <versión> <tema>.mp4` y máximo 30 MB.
- Necesita la clave guardada en Propiedades del script › `CLAVE_SUBIDA`.
- El manifiesto (`appsscript.json`) debe incluir el permiso `https://www.googleapis.com/auth/drive`.
  Si cambias el código o los permisos: Implementar › Administrar implementaciones › ✏️ › Nueva versión.

Para que Claude lo use en cada sesión, en el entorno de Claude Code deben estar:
`SUBIDA_URL` (la URL /exec del buzón) y `SUBIDA_CLAVE` (la clave).

```bash
./subir_drive.sh "salida/v1 1.2 noticias-dia-1.mp4" "NOVIEMBRE 2026"
```

## Estado (7 nov 2026)
- URL del buzón (no es secreta): `https://script.google.com/macros/s/AKfycbxuLACr8EWZxcRuCknOUrErnTo5-aFbxgumqYNoL_t_te-JXa8V0iNKu_OCwxa9Wwfn/exec`
- Clave cambiada por Santi el 7 nov (la vieja se filtró). Probado 13:58: el buzón responde ok y abre la subida en `NOVIEMBRE 2026`.
- La clave NO va en GitHub: solo en Propiedades del script (`CLAVE_SUBIDA`) y en el entorno (`SUBIDA_CLAVE`).
