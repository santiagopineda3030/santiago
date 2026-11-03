import { Component, Suspense, lazy, useEffect, useRef, useState } from 'react'
import { marca, hero, ctaPrincipal } from '../content.js'
import VideoIntro from './VideoIntro.jsx'
import { IconArrowDown } from './Icons.jsx'

// El 3D se descarga aparte y solo cuando el navegador está libre
const Background3D = lazy(() => import('./Background3D.jsx'))

/* Si el dispositivo no soporta WebGL, simplemente no mostramos el fondo */
class SinFondoSiFalla extends Component {
  state = { error: false }
  static getDerivedStateFromError() {
    return { error: true }
  }
  render() {
    return this.state.error ? null : this.props.children
  }
}

function useFondo3D() {
  const [modo, setModo] = useState(null) // null | 'full' | 'lite'

  useEffect(() => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const ahorroDatos = navigator.connection?.saveData === true
    if (reduce || ahorroDatos) return

    const movil = window.matchMedia('(max-width: 767px), (pointer: coarse)').matches
    const activar = () => setModo(movil ? 'lite' : 'full')

    // Esperamos a que la página cargue y el navegador esté libre
    let idle
    const programar = () => {
      idle =
        'requestIdleCallback' in window
          ? window.requestIdleCallback(activar, { timeout: 2500 })
          : window.setTimeout(activar, 1200)
    }
    if (document.readyState === 'complete') programar()
    else window.addEventListener('load', programar, { once: true })

    return () => {
      window.removeEventListener('load', programar)
      if ('cancelIdleCallback' in window) window.cancelIdleCallback(idle)
      window.clearTimeout(idle)
    }
  }, [])

  return modo
}

export default function Hero() {
  const modo = useFondo3D()
  const zonaRef = useRef(null)
  const [enPantalla, setEnPantalla] = useState(true)

  // Pausamos el 3D cuando el titular sale de la pantalla
  useEffect(() => {
    if (!zonaRef.current) return
    const io = new IntersectionObserver(([e]) => setEnPantalla(e.isIntersecting))
    io.observe(zonaRef.current)
    return () => io.disconnect()
  }, [])

  return (
    <header className="relative isolate">
      {/* Fondo 3D detrás del titular */}
      <div ref={zonaRef} className="absolute inset-x-0 top-0 -z-10 h-[440px] overflow-hidden sm:h-[500px] md:h-[540px]">
        {modo && (
          <SinFondoSiFalla>
            <Suspense fallback={null}>
              <Background3D lite={modo === 'lite'} visible={enPantalla} />
            </Suspense>
          </SinFondoSiFalla>
        )}
      </div>

      <div className="mx-auto max-w-5xl px-5 pb-16 pt-10 text-center md:px-8 md:pb-24 md:pt-16">
        <p data-hero className="text-sm font-medium tracking-[0.08em] text-fg-2">
          {marca}
        </p>

        <h1
          data-hero
          className="mx-auto mt-14 max-w-3xl text-balance text-[2.5rem] font-medium leading-[1.08] tracking-[-0.03em] sm:text-6xl md:mt-24 md:text-7xl"
        >
          {hero.titular}
        </h1>

        <p data-hero className="mx-auto mt-5 max-w-md text-pretty text-lg text-fg-2 md:mt-7 md:text-xl">
          {hero.subtitulo}
        </p>

        <div data-hero className="mt-12 md:mt-20">
          {/* VIDEO_INTRO: pegar aquí el embed de YouTube o Vimeo
              → el link va en src/content.js → video.url */}
          <VideoIntro />
        </div>

        <div data-hero className="mt-10 md:mt-12">
          <a href="#agenda" data-cta-principal className="btn-primary w-full max-w-sm sm:w-auto sm:px-10">
            {ctaPrincipal}
            <IconArrowDown className="h-5 w-5" />
          </a>
        </div>
      </div>
    </header>
  )
}
