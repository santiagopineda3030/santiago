import { useEffect, useState } from 'react'

/* ==========================================================================
   Piezas de estilo "pixel"
   ========================================================================== */

/* Logo "SPR" en pixel art: 3 letras de 5x7 con un espacio entre ellas.
   Cada # es un píxel encendido. Para cambiar el logo, edita este dibujo. */
const LOGO = [
  '.###. ####. ####.',
  '#...# #...# #...#',
  '#.... #...# #...#',
  '.###. ####. ####.',
  '....# #.... #.#..',
  '#...# #.... #..#.',
  '.###. #.... #...#',
]

export function PixelLogo({ size = 3, className = '', label }) {
  const ancho = LOGO[0].length
  const celdas = []
  LOGO.forEach((fila, y) =>
    [...fila].forEach((c, x) => {
      if (c === '#') celdas.push({ x, y, d: x * 28 + y * 18 })
    }),
  )
  return (
    <svg
      width={ancho * size}
      height={LOGO.length * size}
      viewBox={`0 0 ${ancho} ${LOGO.length}`}
      shapeRendering="crispEdges"
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      className={`pixel-logo ${className}`}
    >
      {celdas.map(({ x, y, d }) => (
        <rect key={`${x}-${y}`} x={x} y={y} width="1" height="1" fill="currentColor" style={{ animationDelay: `${d}ms` }} />
      ))}
    </svg>
  )
}

/* Fila de píxeles que separa secciones */
export function PixelDivider({ className = '' }) {
  const patron = [1, 0.15, 0.6, 0.15, 0.3, 0.15, 1, 0.6, 0.15, 0.3]
  return (
    <div aria-hidden="true" className={`flex items-center justify-center gap-1.5 ${className}`}>
      {patron.map((o, i) => (
        <span key={i} className="h-1.5 w-1.5 bg-tech" style={{ opacity: o }} />
      ))}
    </div>
  )
}

/* Esquinas tipo visor (HUD) alrededor de un elemento */
export function HudCorners({ className = '' }) {
  const base = 'absolute h-4 w-4 border-tech md:h-5 md:w-5'
  return (
    <div aria-hidden="true" className={`pointer-events-none absolute -inset-2 md:-inset-3 ${className}`}>
      <span className={`${base} left-0 top-0 border-l-2 border-t-2`} />
      <span className={`${base} right-0 top-0 border-r-2 border-t-2`} />
      <span className={`${base} bottom-0 left-0 border-b-2 border-l-2`} />
      <span className={`${base} bottom-0 right-0 border-b-2 border-r-2`} />
    </div>
  )
}

/* Texto que se "decodifica": las letras pasan por símbolos aleatorios
   hasta quedar fijas. Pensado para texto monoespaciado (no salta).
   Con "reducir movimiento" se muestra directo. */
const SIMBOLOS = '01#$%&*+<>/\\|=_[]{}'
const mezclar = (t) => [...t].map((c) => (c === ' ' ? c : SIMBOLOS[(Math.random() * SIMBOLOS.length) | 0])).join('')
const sinMovimiento = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

export function DecodeText({ text, className = '', delay = 250, as: Tag = 'span' }) {
  const [salida, setSalida] = useState(() => (sinMovimiento() ? text : mezclar(text)))

  useEffect(() => {
    if (sinMovimiento()) return
    let frame = 0
    let id
    const total = 22
    const inicio = setTimeout(() => {
      id = setInterval(() => {
        frame++
        const fijas = Math.floor((frame / total) * text.length)
        setSalida(
          [...text]
            .map((c, i) => (c === ' ' || i < fijas ? c : SIMBOLOS[(Math.random() * SIMBOLOS.length) | 0]))
            .join(''),
        )
        if (frame >= total) {
          clearInterval(id)
          setSalida(text)
        }
      }, 40)
    }, delay)
    return () => {
      clearTimeout(inicio)
      clearInterval(id)
    }
  }, [text, delay])

  return (
    <Tag className={className}>
      <span className="sr-only">{text}</span>
      <span aria-hidden="true">{salida}</span>
    </Tag>
  )
}
