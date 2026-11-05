#!/usr/bin/env bash
# Descarga los videos crudos de la carpeta "nov 4" de Google Drive.
# Requiere: que los videos (o la carpeta) estén como "Cualquier persona con el enlace"
# y que la red de la sesión permita drive.google.com y drive.usercontent.google.com.
set -euo pipefail
DESTINO="${1:-crudos}"
mkdir -p "$DESTINO"
# nombre|id de Drive
VIDEOS=(
  "DJI_20261104222426_0094_D.MP4|1DWmzfzroWeZxvKMdbHbX5Wpsq0Y4v-aX"
  "DJI_20261104222823_0098_D.MP4|1TyVU9jA82cd--P2vUj58zDtfIiA6cdG_"
  "DJI_20261104224055_0102_D.MP4|1unF1Z4euosFGTusctK_WQ42W1hCq6ZoP"
  "DJI_20261104224337_0103_D.MP4|12KtGfIvkvfDFdHKUpj2HiNK85B_zhXuZ"
  "DJI_20261104224444_0104_D.MP4|1mGWdRUrCp-0JhUM5csHHtOBi4AMaSEcM"
  "DJI_20261104224537_0105_D.MP4|1WOVLv03EBEuusypzOLf4LS3TeR2HAuv6"
)
for v in "${VIDEOS[@]}"; do
  nombre="${v%%|*}"; id="${v##*|}"
  if [[ -s "$DESTINO/$nombre" ]]; then echo "✓ $nombre (ya estaba)"; continue; fi
  echo "↓ $nombre"
  curl -fL --retry 4 --retry-delay 2 -o "$DESTINO/$nombre.part" \
    "https://drive.usercontent.google.com/download?id=${id}&export=download&confirm=t"
  if head -c 512 "$DESTINO/$nombre.part" | grep -qi "<html"; then
    rm -f "$DESTINO/$nombre.part"
    echo "✗ $nombre: Drive devolvió una página web. ¿El video está como 'Cualquier persona con el enlace'?" >&2
    exit 1
  fi
  mv "$DESTINO/$nombre.part" "$DESTINO/$nombre"
done
echo "Listo: $(ls "$DESTINO" | wc -l) videos en $DESTINO"
