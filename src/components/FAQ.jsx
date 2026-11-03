import { useId, useState } from 'react'
import SectionHeading from './SectionHeading.jsx'
import { IconPlus } from './Icons.jsx'

/* ==========================================================================
   TEXTO: PREGUNTAS FRECUENTES (placeholders)
   Cambia preguntas y respuestas. Lo que está entre [corchetes] es para completar.
   ========================================================================== */
const PREGUNTAS = [
  {
    p: '¿Necesito saber programar o tener experiencia con IA?',
    r: 'No. El programa está pensado para empezar desde cero. Te acompaño paso a paso y montamos el sistema juntos, con herramientas que puedas usar tú mismo.',
  },
  {
    p: '¿Cómo funciona el acompañamiento 1 a 1?',
    r: '[Describe aquí el formato: número de sesiones, duración, por dónde se dan (Zoom, Meet) y qué soporte tienen entre sesiones.]',
  },
  {
    p: '¿Qué necesito para empezar?',
    r: '[Ej: un computador, tus cuentas de redes sociales y ganas de grabar contenido. Ajusta según lo que realmente pidas.]',
  },
  {
    p: '¿En qué redes funciona el sistema?',
    r: '[Ej: Instagram, TikTok, YouTube y Facebook. Indica si se puede adaptar a otras redes como LinkedIn.]',
  },
  {
    p: '¿Cuánto cuesta el programa?',
    r: 'La inversión depende de tu caso y de lo que necesites montar. Lo revisamos juntos en la llamada, sin compromiso. [Ajusta este texto si prefieres mostrar un precio.]',
  },
]

export default function FAQ() {
  const [abierta, setAbierta] = useState(0)
  const base = useId()

  return (
    <section id="preguntas" className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
      <div className="grid gap-12 lg:grid-cols-[1fr_1.35fr] lg:gap-20">
        <SectionHeading eyebrow="Preguntas frecuentes" title="Lo que más me preguntan" />

        <div data-reveal className="border-t border-line">
          {PREGUNTAS.map(({ p, r }, i) => {
            const open = abierta === i
            const btnId = `${base}-q${i}`
            const panelId = `${base}-a${i}`
            return (
              <div key={p} className="border-b border-line">
                <h3>
                  <button
                    id={btnId}
                    type="button"
                    aria-expanded={open}
                    aria-controls={panelId}
                    onClick={() => setAbierta(open ? -1 : i)}
                    className="group flex w-full items-center justify-between gap-6 py-6 text-left text-lg font-medium tracking-tight md:text-xl"
                  >
                    <span>{p}</span>
                    <span
                      className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-line-strong transition-transform duration-300 group-hover:border-fg-2 ${
                        open ? 'rotate-45' : ''
                      }`}
                    >
                      <IconPlus className="h-4 w-4" />
                    </span>
                  </button>
                </h3>
                <div
                  id={panelId}
                  role="region"
                  aria-labelledby={btnId}
                  className={`grid transition-[grid-template-rows] duration-300 ease-out ${
                    open ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'
                  }`}
                >
                  <div className="overflow-hidden" inert={!open}>
                    <p className="max-w-xl pb-7 pr-12 text-fg-2">{r}</p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
