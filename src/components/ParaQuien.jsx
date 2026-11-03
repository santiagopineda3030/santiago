import SectionHeading from './SectionHeading.jsx'
import { IconBriefcase, IconCamera, IconUsers } from './Icons.jsx'

/* TEXTO: las 3 tarjetas de "Para quién es" */
const PERFILES = [
  {
    icon: IconBriefcase,
    titulo: 'Dueños de negocios',
    texto:
      'Sabes que necesitas estar en redes, pero no tienes tiempo para editar y publicar todos los días. Quieres un sistema que lo haga contigo.',
  },
  {
    icon: IconCamera,
    titulo: 'Creadores de contenido',
    texto:
      'Grabas mucho y publicas poco porque la edición se come tu semana. Quieres que la IA haga el trabajo repetitivo y tú enfocarte en crear.',
  },
  {
    icon: IconUsers,
    titulo: 'Community managers',
    texto:
      'Manejas varias cuentas y clientes. Quieres un flujo con IA que te ahorre horas y te deje atender más marcas sin perder calidad.',
  },
]

export default function ParaQuien() {
  return (
    <section id="para-quien" className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
      <SectionHeading eyebrow="Para quién es" title="Esto es para ti si publicas en redes y quieres recuperar tu tiempo" />

      <div className="mt-12 grid gap-4 md:mt-16 md:grid-cols-3 md:gap-5">
        {PERFILES.map(({ icon: Icon, titulo, texto }) => (
          <article
            key={titulo}
            data-reveal
            className="rounded-xl border border-line bg-surface p-7 transition-colors duration-200 hover:border-line-strong md:p-8"
          >
            <span className="flex h-12 w-12 items-center justify-center rounded-full border border-line-strong">
              <Icon className="h-5 w-5" />
            </span>
            <h3 className="mt-6 text-xl font-medium tracking-tight">{titulo}</h3>
            <p className="mt-3 text-fg-2">{texto}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
