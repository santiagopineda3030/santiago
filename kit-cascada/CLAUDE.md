# Cascada de contenidos

Este proyecto convierte cada clase o sesión grabada en Google Meet en pocos clips muy buenos para reels: el
documento con los cortes y las indicaciones de edición y, si se quiere, el reel ya editado (vertical, subtítulos,
gancho fijo, tarjetas, cierre con llamado a la acción y alumnos difuminados).

- Todo el criterio vive en `reglas.json` (marca, clips, privacidad, diseño, cierre, descripción). Si no existe, la
  persona todavía no ha instalado: usar la skill `cascada`, modo **A**, antes que cualquier otra cosa.
- `reglas.ejemplo.json` son las reglas con que nació el sistema (Work in Tech). Sirven de referencia, no se usan.
- `ingesta/Code.gs`: Apps Script que pasa las grabaciones de Meet a Drive y la transcripción a la hoja.
- `editor/`: `preparar_tramo.py` (encuadre + transcripción con tiempos), `armar_reel.py` (compone el reel) y
  `render/` (animaciones HTML que se dibujan con Chrome).
- `plantillas/`: la estructura del documento de cascada y una spec de reel de ejemplo.
- Carpetas de trabajo que se crean solas: `trabajo/`, `specs/`, `salidas/`.

Reglas:
- Python siempre con `.venv/bin/python` (Windows: `.venv\Scripts\python`).
- Nunca pedir contraseñas ni llaves por chat.
- Nada inventado: los clips salen solo de lo que está en la transcripción.
- Cuando la persona pida un cambio que debe valer para siempre, guardarlo en `reglas.json`.
