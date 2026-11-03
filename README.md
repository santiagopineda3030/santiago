# Santiago | Aprende IA y automatiza tus redes

Landing de una sola página con **un solo objetivo**: que la persona vea el video de introducción y agende una llamada de 30 minutos.

React + Vite + Tailwind CSS · GSAP (animaciones de entrada) · React Three Fiber + drei (fondo 3D). Pensada primero para celular.

---

## 1. Correr la página

Necesitas [Node.js](https://nodejs.org) 20 o superior.

```bash
npm install
cp .env.example .env   # luego completa los valores (paso 3)
npm run dev            # abre http://localhost:5173
npm run build          # versión final en /dist
```

---

## 2. Qué cambiar y dónde

| Qué | Dónde |
|---|---|
| Todos los textos (titular, formulario, errores, footer) | `src/content.js` |
| Video de introducción | `src/content.js` → `video.url` (marcador `VIDEO_INTRO` en `src/components/Hero.jsx`) |
| Instagram y WhatsApp | `src/content.js` → `footer` (reemplaza `[NÚMERO]`) |
| URL de Google Sheets | `.env` → `VITE_APPS_SCRIPT_URL` |
| Calendario | `.env` → `VITE_CALENDAR_URL` (marcador `CALENDARIO` en `src/components/Agenda.jsx`) |
| Colores | variables al inicio de `src/index.css` |
| Título para Google y al compartir | `index.html` |

**Link del video (embed):**
- YouTube: *Compartir → Insertar* → copia lo que está dentro de `src="..."` → `https://www.youtube.com/embed/ABC123`. Súbelo como **No listado** si solo quieres que lo vean desde la página.
- Vimeo: *Compartir → Insertar* → `https://player.vimeo.com/video/123456789`.

El reproductor solo se carga cuando la persona toca *play*, así la página abre rápido desde Instagram. Con YouTube se usa la miniatura del video como portada automáticamente.

**Link del calendario:**
- Calendly: `https://calendly.com/tu-usuario/llamada-30-min?hide_gdpr_banner=1&background_color=141414&text_color=f5f5f5&primary_color=e02020` (la página rellena sola el nombre y el correo).
- Google Calendar (agenda de citas): *Página de reservas → Compartir → Insertar* → copia el `src`.
- Cal.com: `https://cal.com/tu-usuario/30min?embed=true&theme=dark`.

---

## 3. Conectar el formulario con Google Sheets (paso a paso)

Cada persona que llena el formulario queda guardada como una fila en tu hoja.

1. **Crea la hoja.** Entra a [sheets.new](https://sheets.new) y ponle un nombre, por ejemplo *Leads – Llamadas*.
2. **Abre Apps Script.** Menú **Extensiones → Apps Script**. Se abre un editor con el archivo `Código.gs`.
3. **Pega el código.** Borra todo lo que hay y pega el contenido de [`google-apps-script/Code.gs`](google-apps-script/Code.gs).
   - Opcional: en `CORREO_AVISO` escribe tu correo para recibir un email por cada registro nuevo.
4. **Guarda** (`Ctrl/Cmd + S`) y ponle nombre al proyecto, por ejemplo *Formulario landing*.
5. **Publícalo como aplicación web.** Botón azul **Implementar → Nueva implementación**.
   - En el engranaje ⚙️ junto a "Seleccionar tipo", elige **Aplicación web**.
   - *Ejecutar como*: **Yo**.
   - *Quién tiene acceso*: **Cualquier persona** (necesario para que la página pueda enviar datos; con esa URL nadie puede leer tu hoja, solo agregar filas).
   - Clic en **Implementar**.
6. **Autoriza.** *Autorizar acceso* → elige tu cuenta. Si aparece "Google no verificó esta app": **Configuración avanzada → Ir a Formulario landing (no seguro) → Permitir**. Es normal: el script es tuyo.
7. **Copia la URL** de la aplicación web (termina en `/exec`).
8. **Pégala en `.env`:**
   ```
   VITE_APPS_SCRIPT_URL=https://script.google.com/macros/s/XXXXXXXX/exec
   ```
   Reinicia `npm run dev`. Si publicas en Vercel o Netlify, agrega la misma variable en *Settings → Environment Variables* y vuelve a publicar.
9. **Prueba.** Abre la URL `/exec` en el navegador: debe decir `"El script está funcionando."`. Luego llena el formulario y revisa la pestaña **Leads** (se crea sola con los títulos).

> Si después cambias el código del script: **Implementar → Administrar implementaciones → ✏️ → Versión: Nueva versión → Implementar**. Así la URL no cambia.

Columnas: Fecha, Nombre, WhatsApp, Correo, Negocio o marca, Redes donde publica, ¿Puede invertir?, Origen (UTM).

**Tip:** en el link de tu bio de Instagram agrega `?utm_source=instagram&utm_medium=bio`. Quedará guardado en la columna *Origen*.

---

## 4. Estilo tecnológico

- **Colores** (`src/index.css`): fondo casi negro azulado, **cian eléctrico** (`--tech`) para los detalles técnicos y **rojo solo en el botón principal**.
- **Píxeles** (`src/components/Pixel.jsx` y `PixelField.jsx`): logo "S" en pixel art, campo de píxeles animado de fondo, separador de píxeles, esquinas tipo visor (HUD) en el video y el calendario, y la línea técnica que se "decodifica" al cargar.
- **Tipografía**: Inter para textos y JetBrains Mono para etiquetas técnicas.
- **Fondo 3D** (`src/components/Background3D.jsx`): un icosaedro en líneas cian con una nube de píxeles que gira en sentido contrario.
  - Se descarga aparte y **después** de que la página ya se ve.
  - **Celular:** versión liviana (menos detalle, resolución 1x, ~30 cuadros por segundo).
  - **Desactivado** con *reducir movimiento* o *ahorro de datos*, y en pausa cuando sale de la pantalla.
- Con *reducir movimiento* activado no hay animaciones: el campo de píxeles queda quieto, el texto no se decodifica y el cursor no parpadea.

## 5. Accesibilidad

Contraste verificado: texto principal 17.7:1, texto secundario 7.7:1, placeholders 5.5:1, cian 11.2:1, texto del botón rojo 4.8:1. Foco visible en todos los controles, botones y opciones de 44px o más, labels en todos los campos y errores anunciados al lector de pantalla.

## 6. Publicar

[Vercel](https://vercel.com) o [Netlify](https://netlify.com): *New project* → elige el repositorio → *Build command* `npm run build`, *Output* `dist` → agrega las variables de `.env` → *Deploy*.
