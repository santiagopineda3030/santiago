import { useLayoutEffect } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

import Hero from './components/Hero.jsx'
import Agenda from './components/Agenda.jsx'
import Footer from './components/Footer.jsx'
import StickyCTA from './components/StickyCTA.jsx'
import PixelField from './components/PixelField.jsx'

gsap.registerPlugin(ScrollTrigger)

export default function App() {
  /* Animaciones de entrada suaves (fade + subida corta).
     Se omiten si la persona tiene activado "reducir movimiento". */
  useLayoutEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    document.documentElement.classList.add('js-anim')
    const ctx = gsap.context(() => {
      gsap.from('[data-hero]', {
        opacity: 0,
        y: 24,
        duration: 1,
        ease: 'power3.out',
        stagger: 0.1,
        delay: 0.05,
      })

      gsap.set('[data-reveal]', { y: 28 })
      ScrollTrigger.batch('[data-reveal]', {
        start: 'top 90%',
        once: true,
        onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out', stagger: 0.1 }),
      })
    })

    return () => {
      ctx.revert()
      document.documentElement.classList.remove('js-anim')
    }
  }, [])

  return (
    <>
      {/* Fondo de píxeles animado (detrás de toda la página) */}
      <PixelField />
      <Hero />
      <main>
        <Agenda />
      </main>
      <Footer />
      <StickyCTA />
    </>
  )
}
