# Guion diario de Noticias IA (lo hace una tarea programada cada mañana)

Tarea programada "Guion diario Noticias IA" (`trig_01BFVwdMKp5sUs5icvey15m3`): corre **todos los días a las
5:43 a. m. (Bogotá)** dentro de la sesión de Claude Code "YouTube Shorts automático" (la que tiene Drive y Sheets
conectados; una sesión nueva creada por tarea no traía los conectores). Su instrucción es: hacer pull y seguir este
archivo. Para cambiar cómo se hace el guion, se cambia este archivo (no la tarea).

## Carpetas (Drive)
| Qué | ID |
|---|---|
| ContentIA › 0. Ideas | `1tEKOG_fwqdaGdlqYbLcyRZr9GwHabP12` |
| 0. Ideas › Instagram | `1qTmb3teZekzoscmXTP0xzm3622V0FCzE` |
| Instagram › NOVIEMBRE 2026 | `1CLvEZIP_nfIHvXL2m59-LAjXcv0gYvYR` |
| Hoja del plan | `1lvs82vX8Pj3rHmVZyUj9cUh6dOm5srjbVDwzvWUyku4` (pestaña del mes: Noviembre…) |

Estructura: `0. Ideas › Instagram › <MES AAAA> › <AAAA-MM-DD> · Noticias IA` y dentro el Google Doc del guion.
Si la carpeta del mes no existe, crearla (ej. `DICIEMBRE 2026`) y anotar su ID en esta tabla.

## Pasos
1. **Fechas** (zona America/Bogota): PUBLICA = hoy, a las 11:00. NOTICIAS = ayer. Si te dan otra fecha, usa esa.
   La campaña va del 5 al 18 de nov 2026: fuera de esas fechas, no hacer nada y avisar.
2. **Investigar** con WebSearch (modo extended) las noticias de IA de NOTICIAS. Elegir 5:
   Viral 1, Viral 2, Polémica 1, Polémica 2, Útil (la útil: algo que un dueño de negocio pueda aplicar o entender en plata).
   - Cada noticia con al menos una fuente fechada ese día. Nada inventado: si un dato no está en la fuente, no va.
   - No repetir noticias de los guiones de los 3 días anteriores (leer los docs en las carpetas de esos días).
3. **Escribir el guion** (español, tuteo, frases cortas, como le hablarías a un dueño de negocio, sin tecnicismos):
   - Gancho (primeros 3 s): la noticia más fuerte en una frase + "Estas son las 5 noticias más importantes de ayer, <d> de <mes>."
   - Viral 1 → Viral 2 → Polémica 1 → Polémica 2 → Útil: 2–4 frases cada una, con una comparación sencilla si ayuda.
   - CTA: "¿Y tú qué opinas de estas noticias del día de ayer?" (hasta que Santiago diga otro CTA).
   - Largo total 130–170 palabras (45–75 s hablado).
   - Al final: sección **Fuentes** con los links.
   Mismo formato del doc de v1 (`1ScuWZ3VeW2XJI4GK4EK5vzZUZEK_5A-Yq88E4Lf0NZo`): título, línea en cursiva con fechas,
   un subtítulo por bloque.
4. **Descripción de Instagram**: 3–5 líneas, la primera es el gancho, sin datos inventados, emoji solo en el cierre,
   5 hashtags al final.
5. **Drive**: crear la carpeta del día y dentro el Google Doc (subirlo como `text/html` para que quede con títulos).
   Título del doc: `v<N> · Noticias IA · Día <D> (publica <d> <mes>)`. Si ya existe la carpeta del día con un guion,
   **reemplazarlo** (mandar el viejo a la papelera) y actualizar el link en la hoja.
6. **Hoja** (pestaña del mes). Buscar la fila con esa Fecha y Tipo `Noticias IA`; si no hay, agregar una fila al final:
   | Columna | Valor |
   |---|---|
   | Fecha | dd/mm/aaaa de PUBLICA |
   | Estado | `Guion` |
   | Ángulo | "Top 5 noticias de IA del <d> <mes>: <5 temas cortos>" |
   | Explicación | "Las 5 noticias de IA más importantes del día anterior, explicadas simple para dueños de negocio." |
   | Guion | `v<N> · Noticias IA · Día <D>` |
   | Elementos adicionales | "Guion: <link del doc> · Seguir la Guía de edición · Noticias IA (Instagram/3. Recursos)" |
   | Descripción de Instagram | la del paso 4 |
   | # | `v<N>` |
   | Hora | `11:00` |
   | Tipo | `Noticias IA` |
   - N = el número `v` más alto de la hoja + 1 (si la fila ya existía, conservar su código). D = días desde el 4 nov (5 nov = Día 1).
   - **No tocar** Publicación, Link Video Editado, ni las columnas de YouTube/TikTok. **Nunca** poner `Publicar`.
   - No tocar otras filas.
7. **Cerrar**: una línea en `contexto/bitacora.md` ("Guion v<N> listo: <link>"), commit y push a la rama
   `claude/santiago-ia-landing-4q4ef1`. Respuesta final corta en español: link del doc + los 5 temas.

## Si algo falla
No inventar el guion para "cumplir". Dejar en la bitácora qué falló y terminar con el error claro.
