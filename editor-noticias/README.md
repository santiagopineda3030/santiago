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

## Uso
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
