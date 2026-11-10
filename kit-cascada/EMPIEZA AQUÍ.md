# Cascada de contenidos · Empieza aquí

**Qué hace:** cada vez que grabas una clase o sesión en Google Meet, el sistema saca de ahí 3 clips muy buenos
para reels (con minutos exactos, gancho, indicaciones de edición y descripción para Instagram) y, si quieres, te
entrega los reels ya editados: verticales, con subtítulos, gancho fijo, tarjetas, cierre con tu llamado a la acción
y las caras de los alumnos difuminadas. Las reglas las pones tú.

```
Google Meet (grabación + transcripción)
      │  Apps Script, cada 30 min
      ▼
Drive: carpeta por sesión  +  hoja "Cascada de contenidos" (SESIONES · TRANSCRIPCIONES · CASCADA)
      │  Claude lee la transcripción con TUS reglas
      ▼
Documento de la cascada (clips + indicaciones)  →  filas en CASCADA  →  reels editados en la carpeta Reels
```

## Lo que necesitas
- **Claude** con Claude Code: la app de escritorio de Claude (pestaña Code) o Claude Code en la terminal.
- En Claude, los conectores de **Google Drive** y **Google Sheets** activos con tu cuenta.
- **Google Workspace** que permita grabar en Meet, con la transcripción activada.
- **Google Drive para escritorio** con la cuenta que recibe las grabaciones (solo si quieres los reels editados).
- 20–30 minutos para la instalación guiada.

## Cómo arrancar
1. Descarga esta carpeta completa a tu computador, en una carpeta normal (por ejemplo `Documentos/cascada`).
   **No la dejes dentro de Google Drive:** ahí se dañan los programas que instala.
2. Abre Claude → Code → abre esa carpeta como proyecto.
3. Escríbele:

   > Instala la cascada de contenidos

Claude te va a entrevistar para armar tus reglas: tu marca y colores, qué clips quieres de cada sesión, cómo
cuidar a los alumnos, cómo cierra cada reel y tu llamado a la acción. Después instala lo que haga falta, te guía
para conectar Meet con Drive y hace una prueba con tu primera grabación.

## Después, el día a día
- "Procesa la sesión de hoy" → documento de la cascada y filas en la hoja.
- "Edita los reels de la sesión del martes" → reels listos en la carpeta `Reels` de la sesión.
- "De ahora en adelante el gancho más corto" / "nunca digas X" → Claude cambia tus reglas y vale para siempre.
- Si quieres que corra solo después de cada sesión, pídele a Claude que lo programe.

En `reglas.ejemplo.json` están las reglas con que nació este sistema (Work in Tech), por si te sirven de ejemplo.
