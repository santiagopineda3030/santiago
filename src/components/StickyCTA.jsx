import { useEffect, useState } from 'react'
import { ctaFijoMovil } from '../content.js'

/**
 * Botón fijo "Agendar llamada" — solo en móvil.
 * Se muestra cuando no está a la vista ni el botón principal ni el
 * formulario/calendario, para que nunca haya dos botones rojos a la vez.
 */
export default function StickyCTA() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const enVista = new Set()
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) enVista.add(e.target)
        else enVista.delete(e.target)
      }
      setVisible(enVista.size === 0)
    })

    // Vigila el botón principal y el formulario (o el calendario, que lo reemplaza)
    const observar = () => {
      io.disconnect()
      enVista.clear()
      document.querySelectorAll('[data-cta-principal], [data-oculta-cta]').forEach((el) => io.observe(el))
    }
    observar()

    const agenda = document.getElementById('agenda')
    const mo = agenda ? new MutationObserver(observar) : null
    mo?.observe(agenda, { childList: true, subtree: true })

    return () => {
      io.disconnect()
      mo?.disconnect()
    }
  }, [])

  return (
    <div
      className={`fixed inset-x-0 bottom-0 z-50 border-t border-line bg-bg/90 px-4 pt-3 backdrop-blur-md transition-[transform,opacity] duration-300 md:hidden ${
        visible ? 'translate-y-0 opacity-100' : 'pointer-events-none translate-y-full opacity-0'
      }`}
      style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}
      aria-hidden={!visible}
      inert={!visible}
    >
      <a href="#agenda" className="btn-primary w-full">
        {ctaFijoMovil}
      </a>
    </div>
  )
}
