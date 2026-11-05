---
name: editar-anuncio
description: Edita un anuncio de Meta de ContentIA (9:16 o 4:5) o una VSL desde el guion, el crudo y su referente, con "Recursos y reglas · Anuncios (Meta)", hasta dejarlo en Listo. Úsalo cuando Santi dice "trabajemos el A1", "edita el anuncio …", "haz la corrección del A1" o en cualquier chat de areas/4-anuncios-meta.
---

# Editar un anuncio

Español, pasos cortos. Santi dirige y aprueba; Claude edita. Espera su OK donde dice **[OK]**.

1. **Leer** guion, referente y "Recursos y reglas · Anuncios (Meta)" completo. Si falta guion o referente: no editar.
   Referente nuevo → skill `agregar-referente`.
2. **Mirar el referente** (zoom cada ~5 s): se copia el formato, no el contenido.
3. **Transcribir** el crudo. **Tomas [OK]:** la última toma buena de cada frase del guion, en orden; mostrar la lista frase por frase.
4. **Base y escenas [OK]:** recorte 9:16 (zoom alterno 1,0/1,18), pausas > 0,4 s fuera, bordes alargados mientras suene la voz.
   Escenas: llamado al avatar fijo los primeros ~20 s, texto gigante, cifra + etiqueta, checks, recuadro, cierre enmarcado.
   **6 cuadros de muestra** comparados con el referente antes del render completo.
5. **Componer y sonido:** música ~16 dB bajo la voz con sidechain, efectos (whoosh, golpe, pop, ding), −14 LUFS.
6. **Auditoría [OK]** (sección 6 del documento: guion completo, reglas de Meta, cifras solo del guion/landing, zona segura
   x 120–960 / y 270–1250, sin congelados). Santi lo ve completo en el celular con sonido.
7. **Listo:** Anuncios (Meta) › `4. Contenido editado` como `<MERCADO>_<ÁNGULO>_<código>_v<n>.mp4`.

**Corrección:** versión nueva (v2, v3…; la anterior se queda), nunca renombrar lo entregado. Regla nueva → "Ajustes de Santi".
