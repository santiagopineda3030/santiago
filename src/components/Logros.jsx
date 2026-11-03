import SectionHeading from './SectionHeading.jsx'
import { IconSparkles, IconGrid, IconLoop, IconClock } from './Icons.jsx'

/* TEXTO: los 4 resultados de "Qué vas a lograr".
   Si publicas en otras redes, cambia la lista del segundo punto. */
const LOGROS = [
  {
    icon: IconSparkles,
    titulo: 'Tus videos editados por IA',
    texto: 'Subes tu grabación y Claude se encarga de cortes, subtítulos y textos. Tú revisas y apruebas.',
  },
  {
    icon: IconGrid,
    titulo: 'Publicados en 4 redes',
    texto: 'Un mismo contenido adaptado y programado para Instagram, TikTok, YouTube y Facebook.',
  },
  {
    icon: IconLoop,
    titulo: 'Un sistema que trabaja por ti',
    texto: 'Lo dejamos montado a tu medida, paso a paso, para que funcione cada semana sin empezar de cero.',
  },
  {
    icon: IconClock,
    titulo: 'Más tiempo para tu negocio',
    texto: 'Las horas que hoy se van en editar y publicar las usas para vender, atender o crear.',
  },
]

export default function Logros() {
  return (
    <section id="logros" className="border-y border-line bg-surface/40">
      <div className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
        <SectionHeading eyebrow="Qué vas a lograr" title="Un sistema de contenido con IA, montado contigo" />

        <div className="mt-12 grid gap-x-10 gap-y-12 sm:grid-cols-2 md:mt-16 lg:grid-cols-4">
          {LOGROS.map(({ icon: Icon, titulo, texto }, i) => (
            <div key={titulo} data-reveal className="border-t border-line-strong pt-6">
              <div className="flex items-center justify-between">
                <Icon className="h-7 w-7" />
                <span className="text-sm tabular-nums text-fg-3">0{i + 1}</span>
              </div>
              <h3 className="mt-6 text-xl font-medium tracking-tight">{titulo}</h3>
              <p className="mt-3 text-fg-2">{texto}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
