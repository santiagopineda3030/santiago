import { useEffect, useRef, useState } from 'react'
import { APPS_SCRIPT_URL, CALENDARIO_URL, PROGRAMA, whatsappLink } from '../config.js'
import { IconCalendar, IconCheck, IconArrowRight } from './Icons.jsx'

/* TEXTO: opciones de las preguntas de filtro */
const REDES = ['Instagram', 'TikTok', 'YouTube', 'Facebook', 'LinkedIn', 'X / Twitter', 'Aún no publico']
const INVERSION = ['Sí', 'No', 'Necesito más información']

const INICIAL = { nombre: '', whatsapp: '', correo: '', negocio: '', redes: [], inversion: '', web: '' }
const STORAGE_KEY = 'agenda-enviada'

function validar(d) {
  const e = {}
  if (d.nombre.trim().length < 2) e.nombre = 'Escribe tu nombre.'
  if (d.whatsapp.replace(/\D/g, '').length < 7) e.whatsapp = 'Escribe tu número con código de país.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.correo.trim())) e.correo = 'Revisa tu correo.'
  if (d.negocio.trim().length < 2) e.negocio = 'Cuéntanos qué negocio o marca tienes.'
  if (d.redes.length === 0) e.redes = 'Elige al menos una opción.'
  if (!d.inversion) e.inversion = 'Elige una opción.'
  return e
}

/* Lee los parámetros UTM del link (útil para saber si vienen de Instagram) */
function origen() {
  const p = new URLSearchParams(window.location.search)
  return ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content']
    .map((k) => p.get(k))
    .filter(Boolean)
    .join(' / ')
}

/* Si usas Calendly, rellenamos nombre y correo automáticamente */
function urlCalendario(base, { nombre, correo }) {
  if (!base) return ''
  if (!base.includes('calendly.com')) return base
  const url = new URL(base)
  url.searchParams.set('name', nombre)
  url.searchParams.set('email', correo)
  return url.toString()
}

export default function Agenda() {
  const [datos, setDatos] = useState(INICIAL)
  const [errores, setErrores] = useState({})
  const [estado, setEstado] = useState('idle') // idle | enviando | listo | error
  const pasoDosRef = useRef(null)

  // Si la persona ya envió el formulario (y recarga la página), mostramos el calendario
  useEffect(() => {
    try {
      const guardado = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || 'null')
      if (guardado) {
        setDatos((d) => ({ ...d, ...guardado }))
        setEstado('listo')
      }
    } catch {
      /* sin almacenamiento disponible: no pasa nada */
    }
  }, [])

  const set = (campo) => (ev) => {
    setDatos((d) => ({ ...d, [campo]: ev.target.value }))
    if (errores[campo]) setErrores((e) => ({ ...e, [campo]: undefined }))
  }

  const toggleRed = (red) => {
    setDatos((d) => ({
      ...d,
      redes: d.redes.includes(red) ? d.redes.filter((r) => r !== red) : [...d.redes, red],
    }))
    if (errores.redes) setErrores((e) => ({ ...e, redes: undefined }))
  }

  async function enviar(ev) {
    ev.preventDefault()
    const e = validar(datos)
    setErrores(e)
    if (Object.keys(e).length) {
      const primero = Object.keys(e)[0]
      document.querySelector(`[data-campo="${primero}"]`)?.focus()
      return
    }

    // Campo trampa para bots: si viene lleno, fingimos éxito y no enviamos nada
    if (datos.web) {
      setEstado('listo')
      return
    }

    setEstado('enviando')
    const payload = new URLSearchParams({
      nombre: datos.nombre.trim(),
      whatsapp: datos.whatsapp.trim(),
      correo: datos.correo.trim(),
      negocio: datos.negocio.trim(),
      redes: datos.redes.join(', '),
      inversion: datos.inversion,
      origen: origen(),
      pagina: window.location.href,
    })

    try {
      if (APPS_SCRIPT_URL) {
        // mode: 'no-cors' evita problemas de CORS con Google Apps Script.
        await fetch(APPS_SCRIPT_URL, { method: 'POST', mode: 'no-cors', body: payload })
      } else {
        console.warn('[Agenda] APPS_SCRIPT_URL está vacío: los datos NO se guardaron. Configúralo en src/config.js')
      }
      try {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ nombre: datos.nombre, correo: datos.correo }))
      } catch {
        /* ignorar */
      }
      setEstado('listo')
    } catch (err) {
      console.error(err)
      setEstado('error')
    }
  }

  // Al pasar al paso 2, llevamos a la persona al calendario
  useEffect(() => {
    if (estado === 'listo' && pasoDosRef.current) {
      pasoDosRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
      pasoDosRef.current.focus({ preventScroll: true })
    }
  }, [estado])

  const listo = estado === 'listo'
  const nombreCorto = datos.nombre.trim().split(' ')[0]

  return (
    <section id="agenda" data-cta-hide className="scroll-mt-4 border-t border-line">
      <div className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
        <div className="grid gap-12 lg:grid-cols-[1fr_1.35fr] lg:gap-20">
          {/* Columna de texto */}
          <div className="lg:sticky lg:top-12 lg:self-start">
            <p data-reveal className="eyebrow">
              Agenda tu llamada
            </p>
            {/* TEXTO: título de la sección del formulario */}
            <h2
              data-reveal
              className="mt-4 text-balance text-3xl font-medium leading-[1.15] tracking-[-0.02em] md:text-5xl"
            >
              Hablemos de tu caso
            </h2>
            <p data-reveal className="mt-5 text-pretty text-lg text-fg-2">
              En la llamada vemos cómo publicas hoy, qué te quita más tiempo y si {PROGRAMA} encaja contigo. Sin
              compromiso.
            </p>

            <ol data-reveal className="mt-10 space-y-4" aria-label="Pasos">
              {['Completa tus datos', 'Elige el día y la hora'].map((paso, i) => {
                const hecho = listo && i === 0
                const activo = listo ? i === 1 : i === 0
                return (
                  <li key={paso} className="flex items-center gap-4">
                    <span
                      className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border text-sm tabular-nums transition-colors ${
                        activo ? 'border-fg text-fg' : 'border-line-strong text-fg-3'
                      }`}
                    >
                      {hecho ? <IconCheck className="h-4 w-4" /> : i + 1}
                    </span>
                    <span className={activo ? 'text-fg' : 'text-fg-3'}>{paso}</span>
                  </li>
                )
              })}
            </ol>
          </div>

          {/* Columna del formulario / calendario */}
          <div data-reveal>
            {!listo ? (
              <form
                onSubmit={enviar}
                noValidate
                className="relative rounded-2xl border border-line bg-surface p-6 sm:p-8 md:p-10"
                aria-label="Formulario para agendar llamada"
              >
                <div className="grid gap-6">
                  <Campo id="nombre" label="Nombre" error={errores.nombre}>
                    <input
                      id="nombre"
                      data-campo="nombre"
                      className="field"
                      type="text"
                      autoComplete="name"
                      placeholder="Tu nombre"
                      value={datos.nombre}
                      onChange={set('nombre')}
                      aria-invalid={!!errores.nombre}
                      aria-describedby={errores.nombre ? 'nombre-error' : undefined}
                    />
                  </Campo>

                  <div className="grid gap-6 sm:grid-cols-2">
                    <Campo id="whatsapp" label="WhatsApp" error={errores.whatsapp}>
                      <input
                        id="whatsapp"
                        data-campo="whatsapp"
                        className="field"
                        type="tel"
                        inputMode="tel"
                        autoComplete="tel"
                        placeholder="+57 300 123 4567"
                        value={datos.whatsapp}
                        onChange={set('whatsapp')}
                        aria-invalid={!!errores.whatsapp}
                        aria-describedby={errores.whatsapp ? 'whatsapp-error' : undefined}
                      />
                    </Campo>
                    <Campo id="correo" label="Correo" error={errores.correo}>
                      <input
                        id="correo"
                        data-campo="correo"
                        className="field"
                        type="email"
                        inputMode="email"
                        autoComplete="email"
                        placeholder="tu@correo.com"
                        value={datos.correo}
                        onChange={set('correo')}
                        aria-invalid={!!errores.correo}
                        aria-describedby={errores.correo ? 'correo-error' : undefined}
                      />
                    </Campo>
                  </div>

                  <div className="my-1 h-px bg-line" />

                  <Campo id="negocio" label="¿Qué negocio o marca tienes?" error={errores.negocio}>
                    <textarea
                      id="negocio"
                      data-campo="negocio"
                      className="field min-h-24 resize-y"
                      rows={3}
                      placeholder="Ej: tienda de ropa, consultorio, marca personal…"
                      value={datos.negocio}
                      onChange={set('negocio')}
                      aria-invalid={!!errores.negocio}
                      aria-describedby={errores.negocio ? 'negocio-error' : undefined}
                    />
                  </Campo>

                  <fieldset aria-describedby={errores.redes ? 'redes-error' : undefined}>
                    <legend className="mb-3 text-[0.95rem] font-medium">¿En qué redes publicas hoy?</legend>
                    <div className="flex flex-wrap gap-2">
                      {REDES.map((red, i) => {
                        const on = datos.redes.includes(red)
                        return (
                          <label
                            key={red}
                            className={`inline-flex min-h-11 cursor-pointer select-none items-center gap-2 rounded-full border px-4 text-[0.95rem] transition-colors duration-150 has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-fg ${
                              on ? 'border-fg bg-fg text-bg' : 'border-line-strong text-fg-2 hover:border-fg-2'
                            }`}
                          >
                            <input
                              type="checkbox"
                              className="sr-only"
                              data-campo={i === 0 ? 'redes' : undefined}
                              checked={on}
                              onChange={() => toggleRed(red)}
                            />
                            {on && <IconCheck className="h-4 w-4" />}
                            {red}
                          </label>
                        )
                      })}
                    </div>
                    <Error id="redes-error" msg={errores.redes} />
                  </fieldset>

                  <fieldset aria-describedby={errores.inversion ? 'inversion-error' : undefined}>
                    <legend className="mb-3 text-[0.95rem] font-medium">
                      ¿Estás en posición de invertir en un acompañamiento personalizado?
                    </legend>
                    <div className="grid gap-2 sm:grid-cols-[1fr_1fr_2fr]">
                      {INVERSION.map((op, i) => {
                        const on = datos.inversion === op
                        return (
                          <label
                            key={op}
                            className={`flex min-h-12 cursor-pointer items-center gap-3 rounded-xl border px-4 py-3 text-[0.95rem] transition-colors duration-150 has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-fg ${
                              on ? 'border-fg text-fg' : 'border-line-strong text-fg-2 hover:border-fg-2'
                            }`}
                          >
                            <input
                              type="radio"
                              name="inversion"
                              value={op}
                              className="sr-only"
                              data-campo={i === 0 ? 'inversion' : undefined}
                              checked={on}
                              onChange={set('inversion')}
                            />
                            <span
                              className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                                on ? 'border-fg' : 'border-line-strong'
                              }`}
                            >
                              {on && <span className="h-2.5 w-2.5 rounded-full bg-fg" />}
                            </span>
                            {op}
                          </label>
                        )
                      })}
                    </div>
                    <Error id="inversion-error" msg={errores.inversion} />
                  </fieldset>

                  {/* Campo trampa anti-spam: invisible para personas */}
                  <div className="absolute -left-[9999px]" aria-hidden="true">
                    <label>
                      Sitio web
                      <input type="text" tabIndex={-1} autoComplete="off" value={datos.web} onChange={set('web')} />
                    </label>
                  </div>

                  {estado === 'error' && (
                    <p role="alert" className="rounded-xl border border-line-strong p-4 text-sm text-fg-2">
                      No pudimos enviar tus datos. Revisa tu conexión e inténtalo otra vez, o{' '}
                      <a className="text-fg underline underline-offset-4" href={whatsappLink()} target="_blank" rel="noreferrer">
                        escríbeme por WhatsApp
                      </a>
                      .
                    </p>
                  )}

                  <button type="submit" className="btn-primary mt-2 w-full" disabled={estado === 'enviando'}>
                    {estado === 'enviando' ? 'Enviando…' : 'Elegir mi horario'}
                    {estado !== 'enviando' && <IconArrowRight className="h-5 w-5" />}
                  </button>

                  {/* TEXTO: aviso de privacidad del formulario */}
                  <p className="text-center text-xs leading-relaxed text-fg-3">
                    Al enviar aceptas que te contacte por WhatsApp o correo sobre el programa. Tus datos no se comparten
                    con terceros. <a href="#aviso-legal" className="underline underline-offset-2 hover:text-fg-2">Aviso legal</a>
                  </p>
                </div>
              </form>
            ) : (
              <div
                ref={pasoDosRef}
                tabIndex={-1}
                className="scroll-mt-6 rounded-2xl border border-line bg-surface p-4 outline-none sm:p-6 md:p-8"
              >
                <div className="px-2 pb-6 pt-2 sm:px-0">
                  <p className="eyebrow">Paso 2 de 2</p>
                  <h3 className="mt-3 text-2xl font-medium tracking-tight md:text-3xl">
                    {nombreCorto ? `Gracias, ${nombreCorto}.` : 'Gracias.'} Ahora elige tu horario
                  </h3>
                  <p className="mt-3 text-fg-2">Reserva el espacio que mejor te quede. Te llegará la confirmación a tu correo.</p>
                </div>

                {/* ============================================================
                    <!-- CALENDARIO -->
                    Calendario para reservar la llamada. Pega el link de tu
                    agenda (Calendly, Google Calendar, Cal.com) en
                    src/config.js → CALENDARIO_URL
                    ============================================================ */}
                {CALENDARIO_URL ? (
                  <iframe
                    src={urlCalendario(CALENDARIO_URL, datos)}
                    title="Calendario para agendar tu llamada"
                    className="h-[720px] w-full rounded-xl border-0 bg-bg md:h-[760px]"
                    loading="lazy"
                  />
                ) : (
                  <div className="flex aspect-[4/5] w-full flex-col items-center justify-center gap-4 rounded-xl border border-dashed border-line-strong bg-bg p-6 text-center sm:aspect-video">
                    <IconCalendar className="h-8 w-8 text-fg-2" />
                    <span className="eyebrow">Calendario</span>
                    <span className="max-w-xs text-sm text-fg-3">Pega el link de tu agenda en CALENDARIO_URL</span>
                  </div>
                )}

                <p className="mt-5 px-2 text-center text-sm text-fg-3 sm:px-0">
                  ¿Ningún horario te sirve?{' '}
                  <a className="text-fg-2 underline underline-offset-4 hover:text-fg" href={whatsappLink('Hola Santiago, llené el formulario pero no encuentro un horario que me sirva.')} target="_blank" rel="noreferrer">
                    Escríbeme por WhatsApp
                  </a>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

function Campo({ id, label, error, children }) {
  return (
    <div>
      <label htmlFor={id} className="mb-2 block text-[0.95rem] font-medium">
        {label}
      </label>
      {children}
      <Error id={`${id}-error`} msg={error} />
    </div>
  )
}

function Error({ id, msg }) {
  if (!msg) return null
  return (
    <p id={id} className="mt-2 text-sm text-fg-2">
      <span className="mr-1.5 inline-block h-1.5 w-1.5 -translate-y-0.5 rounded-full bg-accent align-middle" aria-hidden="true" />
      {msg}
    </p>
  )
}
