import { useEffect, useRef } from 'react'

/**
 * Fondo de píxeles: una cuadrícula de puntos muy tenues donde algunos
 * píxeles se encienden en cian y se apagan poco a poco.
 * - Canvas 2D liviano (~24 cuadros por segundo), se pausa con la pestaña oculta.
 * - Con "reducir movimiento" se dibuja una sola vez, sin animación.
 */
const PASO = 22 // distancia entre píxeles (px)
const COLOR = '34, 211, 238' // --tech en RGB

export default function PixelField() {
  const ref = useRef(null)

  useEffect(() => {
    const canvas = ref.current
    const ctx = canvas.getContext('2d')
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let cols = 0
    let rows = 0
    let brillo = new Float32Array(0)
    let dpr = 1
    let raf = 0
    let ultimo = 0

    const medir = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2)
      const w = window.innerWidth
      const h = window.innerHeight
      canvas.width = Math.round(w * dpr)
      canvas.height = Math.round(h * dpr)
      canvas.style.width = `${w}px`
      canvas.style.height = `${h}px`
      cols = Math.ceil(w / PASO) + 1
      rows = Math.ceil(h / PASO) + 1
      brillo = new Float32Array(cols * rows)
      // Algunos píxeles encendidos desde el inicio
      for (let i = 0; i < brillo.length * 0.02; i++) brillo[(Math.random() * brillo.length) | 0] = Math.random()
    }

    const dibujar = () => {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      const off = PASO / 2
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
          const b = brillo[y * cols + x]
          const px = x * PASO + off
          const py = y * PASO + off
          if (b > 0.04) {
            ctx.fillStyle = `rgba(${COLOR}, ${(b * 0.55).toFixed(3)})`
            ctx.fillRect(px - 1.5, py - 1.5, 3, 3)
          } else {
            ctx.fillStyle = 'rgba(148, 190, 230, 0.07)'
            ctx.fillRect(px - 0.5, py - 0.5, 1, 1)
          }
        }
      }
    }

    const paso = (t) => {
      raf = requestAnimationFrame(paso)
      if (t - ultimo < 42) return // ~24 fps
      ultimo = t
      for (let i = 0; i < brillo.length; i++) if (brillo[i] > 0) brillo[i] *= 0.955
      const nuevos = Math.max(1, (brillo.length * 0.0025) | 0)
      for (let i = 0; i < nuevos; i++) brillo[(Math.random() * brillo.length) | 0] = 0.6 + Math.random() * 0.4
      dibujar()
    }

    const onResize = () => {
      medir()
      dibujar()
    }
    const onVisible = () => {
      cancelAnimationFrame(raf)
      if (!document.hidden && !reduce) raf = requestAnimationFrame(paso)
    }

    medir()
    dibujar()
    if (!reduce) raf = requestAnimationFrame(paso)
    window.addEventListener('resize', onResize)
    document.addEventListener('visibilitychange', onVisible)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', onResize)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [])

  return <canvas ref={ref} aria-hidden="true" className="pointer-events-none fixed inset-0 -z-20" />
}
