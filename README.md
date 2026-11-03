# Landing "Clase gratuita + agenda tu llamada"

**Santiago | Aprende IA y automatiza tus redes** — página de una sola sección para que el visitante vea la clase y agende una llamada para **Redes Automatizadas 1 a 1**.

Hecha con React + Vite + Tailwind CSS. GSAP solo para animaciones suaves de entrada. Pensada primero para móvil.

---

## 1. Correr la página en tu computador

Necesitas [Node.js](https://nodejs.org) 20 o superior.

```bash
npm install
npm run dev       # abre http://localhost:5173
npm run build     # genera la versión final en /dist
```

---

## 2. Qué cambiar y dónde

Casi todo se cambia en **`src/config.js`**:

| Qué | Variable en `src/config.js` | Marcador en el código |
|---|---|---|
| Video principal de la clase | `VIDEO_CLASE_URL` | `<!-- VIDEO_CLASE -->` en `src/components/Hero.jsx` |
| Video corto (antes y después) | `VIDEO_CORTO_URL` y `VIDEO_CORTO_FORMATO` | `<!-- VIDEO_CORTO -->` en `src/components/VideoCorto.jsx` |
| Calendario | `CALENDARIO_URL` | `<!-- CALENDARIO -->` en `src/components/Agenda.jsx` |
| Google Sheets | `APPS_SCRIPT_URL` | — |
| WhatsApp e Instagram | `WHATSAPP_NUMERO`, `WHATSAPP_MENSAJE`, `INSTAGRAM_URL`, `INSTAGRAM_USUARIO` | — |

Otros puntos (busca los comentarios `TEXTO:`, `FOTO:` y los marcadores):

- **Testimonios en video y capturas**: `src/components/Resultados.jsx` → `<!-- TESTIMONIO_1 -->`, `<!-- TESTIMONIO_2 -->`, `<!-- TESTIMONIO_3 -->`, `<!-- CAPTURA_1 -->`… Las fotos van en la carpeta `public/` (ej. `public/captura-1.jpg` → `src: '/captura-1.jpg'`).
- **Preguntas frecuentes**: `src/components/FAQ.jsx` (lo que está entre `[corchetes]` es para completar).
- **Para quién es / Qué vas a lograr**: `src/components/ParaQuien.jsx` y `src/components/Logros.jsx`.
- **Aviso legal**: `src/components/Footer.jsx`.
- **Colores**: variables al inicio de `src/index.css` (`--bg-primary`, `--accent`, etc.).
- **Título para Google y al compartir**: `index.html`.

### Cómo obtener el link "embed" de los videos

- **YouTube**: abre el video → *Compartir* → *Insertar* → copia solo lo que está dentro de `src="..."`.
  Queda así: `https://www.youtube.com/embed/ABC123xyz`. Puedes agregar `?rel=0&modestbranding=1` al final.
  Tip: sube la clase como **"No listado"** para que solo la vean quienes llegan a la página.
- **Vimeo**: *Compartir* → *Insertar* → copia el `src`. Queda así: `https://player.vimeo.com/video/123456789`.

### Calendario

- **Calendly**: usa el link de tu evento, por ejemplo
  `https://calendly.com/tu-usuario/llamada?hide_gdpr_banner=1&background_color=141414&text_color=f5f5f5&primary_color=e02020`
  (la página rellena automáticamente el nombre y el correo que la persona escribió en el formulario).
- **Google Calendar (agenda de citas)**: *Página de reservas* → *Compartir* → *Insertar* → copia el `src`.
- **Cal.com**: `https://cal.com/tu-usuario/llamada?embed=true&theme=dark`.

---

## 3. Conectar el formulario con Google Sheets (paso a paso)

Cada persona que llena el formulario queda guardada como una fila en tu Google Sheet.

1. **Crea la hoja.** Entra a [sheets.new](https://sheets.new) y ponle un nombre, por ejemplo *Leads – Redes Automatizadas*.
2. **Abre Apps Script.** En la hoja, menú **Extensiones → Apps Script**. Se abre un editor con un archivo `Código.gs`.
3. **Pega el código.** Borra todo lo que hay en `Código.gs` y pega el contenido de [`google-apps-script/Code.gs`](google-apps-script/Code.gs) de este proyecto.
   - Opcional: en `CORREO_AVISO` escribe tu correo si quieres recibir un email por cada registro.
4. **Guarda** (ícono del disquete o `Ctrl/Cmd + S`). Ponle un nombre al proyecto, por ejemplo *Formulario landing*.
5. **Publica el script.** Botón azul **Implementar → Nueva implementación**.
   - En el engranaje ⚙️ de "Seleccionar tipo", elige **Aplicación web**.
   - *Descripción*: `Formulario landing`.
   - *Ejecutar como*: **Yo** (tu correo).
   - *Quién tiene acceso*: **Cualquier persona**. (Esto es necesario para que la página pueda enviar datos; nadie puede leer tu hoja con esa URL, solo enviar filas nuevas).
   - Clic en **Implementar**.
6. **Autoriza.** Google te pedirá permisos: *Autorizar acceso* → elige tu cuenta → si aparece "Google no verificó esta app", clic en **Configuración avanzada → Ir a Formulario landing (no seguro)** → **Permitir**. Es normal: el script es tuyo.
7. **Copia la URL.** Al terminar verás la **URL de la aplicación web**, que termina en `/exec`. Cópiala.
8. **Pégala en la página.** En `src/config.js`:
   ```js
   export const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/XXXXXXXX/exec'
   ```
9. **Prueba.** Abre esa URL en el navegador: debe decir `"El script está funcionando."`. Luego llena el formulario de la página y revisa que aparezca la fila en la pestaña **Leads** (se crea sola con los títulos de las columnas).

> **Importante:** si después cambias el código del script, debes ir a **Implementar → Administrar implementaciones → ✏️ Editar → Versión: Nueva versión → Implementar**. Así la URL sigue siendo la misma. Si creas una *nueva implementación*, la URL cambia y tendrás que actualizar `APPS_SCRIPT_URL`.

Columnas que se guardan: Fecha, Nombre, WhatsApp, Correo, Negocio o marca, Redes donde publica, ¿Puede invertir?, Origen (UTM) y Página.

**Tip para Instagram:** en el link de tu bio o historias agrega parámetros UTM, por ejemplo
`https://tu-pagina.com/?utm_source=instagram&utm_medium=bio`. Quedarán guardados en la columna *Origen*.

---

## 4. Publicar la página

La forma más simple: [Vercel](https://vercel.com) o [Netlify](https://netlify.com).

1. Sube este repositorio a GitHub (ya lo está).
2. En Vercel/Netlify: *New project* → elige el repositorio.
3. Configuración: *Build command* `npm run build`, *Output directory* `dist`.
4. Publica y conecta tu dominio si tienes uno.

---

## Estructura

```
src/
  config.js              ← links, URLs y datos de contacto
  index.css              ← colores (variables CSS) y estilos base
  App.jsx                ← orden de las secciones + animaciones GSAP
  components/
    Hero.jsx             ← 1. Clase gratuita + video principal
    ParaQuien.jsx        ← 2. Para quién es
    Logros.jsx           ← 3. Qué vas a lograr
    Resultados.jsx       ← 4. Testimonios y capturas
    VideoCorto.jsx       ← 5. Segundo video corto
    Agenda.jsx           ← 6. Formulario + calendario
    FAQ.jsx              ← 7. Preguntas frecuentes
    Footer.jsx           ← 8. WhatsApp, Instagram y aviso legal
    StickyCTA.jsx        ← Botón fijo "Agendar llamada" (solo móvil)
google-apps-script/
  Code.gs                ← código para pegar en Google Apps Script
```
