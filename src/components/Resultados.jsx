import SectionHeading from './SectionHeading.jsx'
import VideoEmbed from './VideoEmbed.jsx'
import { IconImage } from './Icons.jsx'

/* ==========================================================================
   TESTIMONIOS EN VIDEO
   Pega en `src` el link de embed (YouTube Shorts / Vimeo) de cada testimonio.
   Para YouTube Shorts usa: https://www.youtube.com/embed/ID_DEL_SHORT
   ========================================================================== */
const TESTIMONIOS = [
  /* <!-- TESTIMONIO_1 --> */
  { id: 'TESTIMONIO_1', src: '', nombre: 'Nombre del cliente', rol: 'Negocio o marca' },
  /* <!-- TESTIMONIO_2 --> */
  { id: 'TESTIMONIO_2', src: '', nombre: 'Nombre del cliente', rol: 'Negocio o marca' },
  /* <!-- TESTIMONIO_3 --> */
  { id: 'TESTIMONIO_3', src: '', nombre: 'Nombre del cliente', rol: 'Negocio o marca' },
]

/* ==========================================================================
   CAPTURAS (mensajes, comentarios, métricas)
   FOTO: sube las imágenes a la carpeta /public (ej: /public/captura-1.jpg)
   y escribe la ruta en `src`: '/captura-1.jpg'
   ========================================================================== */
const CAPTURAS = [
  /* <!-- CAPTURA_1 --> */
  { id: 'CAPTURA_1', src: '', alt: 'Captura de un mensaje de un cliente' },
  /* <!-- CAPTURA_2 --> */
  { id: 'CAPTURA_2', src: '', alt: 'Captura de un mensaje de un cliente' },
  /* <!-- CAPTURA_3 --> */
  { id: 'CAPTURA_3', src: '', alt: 'Captura de un mensaje de un cliente' },
]

/* Carrusel horizontal en móvil, cuadrícula en escritorio */
const rail =
  '-mx-5 flex snap-x snap-mandatory scroll-px-5 gap-4 overflow-x-auto px-5 pb-2 [scrollbar-width:none] md:mx-0 md:grid md:grid-cols-3 md:gap-5 md:overflow-visible md:px-0 [&::-webkit-scrollbar]:hidden'

export default function Resultados() {
  return (
    <section id="resultados" className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
      <SectionHeading
        eyebrow="Resultados"
        title="Lo que dicen quienes ya lo implementaron"
        intro="Experiencias reales de personas que pasaron por el programa. Cada caso es distinto y depende del trabajo de cada uno."
      />

      <div className={`mt-12 md:mt-16 ${rail}`}>
        {TESTIMONIOS.map((t) => (
          <figure key={t.id} data-reveal className="w-[72%] shrink-0 snap-start sm:w-[45%] md:w-auto">
            <VideoEmbed src={t.src} ratio="9:16" title={`Testimonio de ${t.nombre}`} label="Testimonio en video" />
            <figcaption className="mt-4">
              <span className="block font-medium">{t.nombre}</span>
              <span className="text-sm text-fg-3">{t.rol}</span>
            </figcaption>
          </figure>
        ))}
      </div>

      <div className={`mt-14 md:mt-20 ${rail}`}>
        {CAPTURAS.map((c) => (
          <div
            key={c.id}
            data-reveal
            className="relative aspect-[4/5] w-[72%] shrink-0 snap-start overflow-hidden rounded-2xl border border-line bg-surface sm:w-[45%] md:w-auto"
          >
            {c.src ? (
              <img src={c.src} alt={c.alt} loading="lazy" className="absolute inset-0 h-full w-full object-cover" />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-fg-3">
                <IconImage className="h-7 w-7" />
                <span className="eyebrow text-fg-3">Captura</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
