# Editor automático · Noticias IA

Edita los videos crudos **siguiendo el guión** y la *Guía de edición · Noticias IA*, todo local con
ffmpeg + Whisper (sin Descript ni otras plataformas).

## Qué hace
1. **Transcribe** cada clip con Whisper (palabra por palabra, con tiempos).
2. **Encuentra cada parte del guión** (Gancho, Viral 1, Viral 2, Polémica 1, Polémica 2, Útil, CTA) en los clips,
   sin importar en qué orden se grabaron. Si hay varias tomas buenas usa **la última** (la del final suele ser la buena).
3. **Ordena** las partes tal como están en el guión y **quita silencios y respiraciones** (pausas > 0,30 s).
4. Arma el video **vertical 1080×1920** con un **zoom distinto en cada corte** (cambio visual cada 3–5 s).
5. Agrega **subtítulos de 2–4 palabras** (blancos con borde negro, empresas y cifras en rojo), corrige nombres
   (Anthropic, SETI, Gemini, Revolut…), **título por noticia** (VIRAL · ANTHROPIC…), **texto del gancho** en los
   primeros 3 s y la **pregunta del CTA** al final.
6. Normaliza la voz a **−14 LUFS** y exporta **H.264 ≤ 30 MB**: `v1 1.0 noticias-dia-1.mp4`.
7. Deja `resumen.md` con qué clip y qué segundos usó para cada parte, para revisarlo.

## Flujo actual (v2–v3, nov 2026) — el que hay que usar
```bash
pip install faster-whisper rapidfuzz opencv-python-headless cairosvg scipy   # una vez
# 1. Bajar el crudo (Drive: compartir con enlace un rato; luego Santi lo vuelve a Restringido)
curl -fL -o crudos-vN/DJI_2026MMDD000000_0001_D.MP4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"
# 2. Transcribir por trozos (ajustar initial_prompt de trozos.py con los nombres del guion)
python3 trozos.py crudos-vN salida-vN/trozos
# 3. Elegir tomas a mano → edl-vN.json (última toma buena; subtítulo con el mismo nº de palabras que Whisper)
# 4. Mirada solo en las tomas elegidas (rangos JSON [[desde,hasta],...]; respeta video vertical)
python3 mirada.py crudos-vN/<clip>.MP4 salida-vN/mirada.json "$(cat salida-vN/rangos.json)"
# 5. Render
python3 editar_v2.py --videos crudos-vN --edl edl-vN.json --trozos salida-vN/trozos --assets assets-v2 \
  --salida salida-vN --mirada salida-vN/mirada.json --musica musica/lofi-energico.wav --musica-db -14 \
  --musica-intro musica/suspenso.wav --luz limpia --estilo ia --nombre "vN 1.0 tema.mp4" \
  --centro-x 0.55 --centro-y 0.6 --zoom-base 2.0   # encuadre: probar con un cuadro antes (cambia cada día)
```
- `--mirada`: recorta los bordes donde no mira a cámara y sostiene la imagen (el audio sigue). Lo que queda en medio
  de una frase se tapa con una escena a pantalla completa (`"cubrir": {"clip","desde","hasta"}` en el EDL).
- `--adelanto 0.3` (por defecto): cada animación sale 0,3 s antes de su palabra (pedido de Santi, 7 nov).
- `--luz cine`: contraste, color cálido, viñeta y nitidez (pedido de Santi, 7 nov). `--zoom-base`/`--centro-y` para
  crudos verticales con mucho espacio arriba (el del 6 nov: 1.4 / 0.53). Tarjetas de texto en `"y": 455` para no tapar la cara.
- Música: `musica.py salida.wav <seg> <bpm> <energía>` compone una pista ORIGINAL (sin derechos). Santi la quiere
  audible: `lofi-energico` (100 BPM, energía 1.6) a `--musica-db -14`.
- Escenas (animaciones.py): hacker, fuga, versus, lluvia, carrera, precio, billetes, anuncio, igual, hack_banco, swat,
  paises, itinerario, resumen_ia, app. Emojis dentro de texto: usar `texto_emoji` (Inter no dibuja emojis).
- Crudos 4K 120 fps (7,6 GB): no hacer hojas de cuadros del crudo completo (decodificar tarda muchísimo); medir solo rangos.
- Subir a Drive: `subir-drive/subir_drive.sh "salida-vN/vN 1.x tema.mp4" "NOVIEMBRE 2026"` (funciona desde el 7 nov).
- Reglas de Santi (7 nov): estilo `ia` (nada de tanto rojo), luz `limpia` (sin amarillo), nunca cortar audio por la mirada
  (solo sostener imagen), suspenso en el gancho, noticias más fuertes primero.

## Uso (versión vieja, v1)
```bash
pip install faster-whisper rapidfuzz      # una vez
./descargar.sh crudos                      # baja los 6 videos de Drive (carpeta "nov 4")
python3 editar.py --videos crudos --guion guion-dia-1.md
```
Opciones útiles: `--solo-plan` (solo transcribe y muestra el plan), `--modelo medium` (transcripción más precisa,
más lenta), `--pausa 0.4` (deja pausas más largas), `--gancho-texto "..."`, `--nombre "v1 1.1 noticias-dia-1.mp4"`.

## Pendiente (no incluido todavía)
- B-roll (logos, capturas, clips de stock), música de fondo y efectos de sonido: necesitan los archivos.
  Si los dejas en Drive (carpeta *3. Recursos*), se pueden agregar.
