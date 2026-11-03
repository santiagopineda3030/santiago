import { useEffect, useLayoutEffect } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

import Hero from './components/Hero.jsx'
import ParaQuien from './components/ParaQuien.jsx'
import Logros from './components/Logros.jsx'
import Resultados from './components/Resultados.jsx'
import VideoCorto from './components/VideoCorto.jsx'
import Agenda from './components/Agenda.jsx'
import FAQ from './components/FAQ.jsx'
import Footer from './components/Footer.jsx'
import StickyCTA from './components/StickyCTA.jsx'

gsap.registerPlugin(ScrollTrigger)

export default function App() {
  /* Animaciones de entrada suaves: los elementos con data-reveal
     aparecen con un fade + subida al entrar en pantalla. */
  useLayoutEffect(() => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduce) return

    document.documentElement.classList.add('js-anim')
    const ctx = gsap.context(() => {
      gsap.set('[data-reveal]', { y: 28 })
      ScrollTrigger.batch('[data-reveal]', {
        start: 'top 90%',
        once: true,
        onEnter: (els) =>
          gsap.to(els, {
            opacity: 1,
            y: 0,
            duration: 0.9,
            ease: 'power3.out',
            stagger: 0.08,
            overwrite: true,
          }),
      })
    })

    return () => {
      ctx.revert()
      document.documentElement.classList.remove('js-anim')
    }
  }, [])

  /* Abre el "Aviso legal" cuando alguien hace clic en un link hacia él */
  useEffect(() => {
    const abrir = (e) => {
      const a = e.target.closest('a[href="#aviso-legal"]')
      if (a) document.getElementById('aviso-legal')?.setAttribute('open', '')
    }
    document.addEventListener('click', abrir)
    return () => document.removeEventListener('click', abrir)
  }, [])

  return (
    <>
      <Hero />
      <main>
        <ParaQuien />
        <Logros />
        <Resultados />
        <VideoCorto />
        <Agenda />
        <FAQ />
      </main>
      <Footer />
      <StickyCTA />
    </>
  )
}
