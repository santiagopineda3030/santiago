#!/usr/bin/env bash
# Sube un video editado a Drive › Instagram › 4. Contenido editado › <MES AAAA>
# usando el buzón de Apps Script (Subidas.gs).
#
# Necesita dos variables del entorno (se configuran en el entorno de Claude Code, no en el chat):
#   SUBIDA_URL    URL de la aplicación web del buzón (termina en /exec)
#   SUBIDA_CLAVE  la misma clave guardada en Propiedades del script › CLAVE_SUBIDA
#
# Uso: ./subir_drive.sh "salida/v1 1.2 noticias-dia-1.mp4" ["NOVIEMBRE 2026"]
set -euo pipefail
: "${SUBIDA_URL:?Falta la variable SUBIDA_URL}"
: "${SUBIDA_CLAVE:?Falta la variable SUBIDA_CLAVE}"
archivo="$1"
mes="${2:-}"
nombre="$(basename "$archivo")"
tamano=$(stat -c%s "$archivo")

pedido=$(python3 -I -c 'import json,sys; print(json.dumps({"clave":sys.argv[1],"nombre":sys.argv[2],"tamano":int(sys.argv[3]),"mes":sys.argv[4]}))' \
  "$SUBIDA_CLAVE" "$nombre" "$tamano" "$mes")
# Apps Script responde con una redirección: -L la sigue (como GET) y trae la respuesta JSON
respuesta=$(curl -sSL --max-time 60 -H 'Content-Type: application/json' --data "$pedido" "$SUBIDA_URL")
url=$(python3 -I -c 'import json,sys
d = json.loads(sys.argv[1])
if not d.get("ok"): sys.exit("✗ El buzón respondió: " + str(d.get("error")))
print(d["subida"])' "$respuesta")

echo "↑ Subiendo $nombre ($((tamano / 1048576)) MB)…"
resultado=$(curl -sS --fail --retry 3 --max-time 900 -X PUT -H "Content-Type: video/mp4" --upload-file "$archivo" "$url")
python3 -I -c 'import json,sys; d=json.loads(sys.argv[1]); print("✓ En Drive:", d["name"], "·", d.get("webViewLink", d["id"]))' "$resultado"
