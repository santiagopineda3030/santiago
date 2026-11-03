import { useEffect, useState } from 'react'

/**
 * Botón fijo "Agendar llamada" — solo en móvil.
 * Se oculta mientras está a la vista el botón del hero o el formulario,
 * para no repetir el mismo botón dos veces en pantalla.
 */
export default function StickyCTA() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const targets = document.querySelectorAll('[data-cta-hero], [data-cta-hide]')
    const enVista = new Set()
    let pasoHero = false

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) enVista.add(e.target)
          else enVista.delete(e.target)
          if (e.target.hasAttribute('data-cta-hero') && !e.isIntersecting && e.boundingClientRect.top < 0) {
            pasoHero = true
          }
        })
        setVisible(pasoHero && enVista.size === 0)
      },
      { threshold: 0 },
    )
    targets.forEach((t) => io.observe(t))
    return () => io.disconnect()
  }, [])

  return (
    <div
      className={`fixed inset-x-0 bottom-0 z-50 border-t border-line bg-bg/85 px-4 pt-3 backdrop-blur-md transition-all duration-300 md:hidden ${
        visible ? 'translate-y-0 opacity-100' : 'pointer-events-none translate-y-full opacity-0'
      }`}
      style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}
      aria-hidden={!visible}
    >
      <a href="#agenda" className="btn-primary w-full" tabIndex={visible ? 0 : -1}>
        Agendar llamada
      </a>
    </div>
  )
}
