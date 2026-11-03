import { useEffect, useRef, useState } from 'react'
import { agenda } from '../content.js'
import { IconAlert, IconCalendar, IconCheck } from './Icons.jsx'

/* URLs privadas: se configuran en el archivo .env (ver README.md) */
const APPS_SCRIPT_URL = import.meta.env.VITE_APPS_SCRIPT_URL || ''
const CALENDAR_URL = import.meta.env.VITE_CALENDAR_URL || ''

const { campos, errores: msg } = agenda
const INICIAL = { nombre: '', whatsapp: '', correo: '', negocio: '', redes: [], inversion: '', web: '' }
const ORDEN = ['nombre', 'whatsapp', 'correo', 'negocio', 'redes', 'inversion']

function validar(d) {
  const e = {}
  if (d.nombre.trim().length < 2) e.nombre = msg.nombre
  const digitos = d.whatsapp.replace(/\D/g, '')
  if (digitos.length < 8 || digitos.length > 15) e.whatsapp = msg.whatsapp
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.correo.trim())) e.correo = msg.correo
  if (d.negocio.trim().length < 2) e.negocio = msg.negocio
  if (d.redes.length === 0) e.redes = msg.redes
  if (!d.inversion) e.inversion = msg.inversion
  return e
}

/* Guarda de dónde viene la visita (ej: ?utm_source=instagram) */
function origen() {
  const p = new URLSearchParams(window.location.search)
  return ['utm_source', 'utm_medium', 'utm_campaign']
    .map((k) => p.get(k))
    .filter(Boolean)
    .join(' / ')
}

/* Si el calendario es de Calendly, rellena nombre y correo */
function urlCalendario(base, { nombre, correo }) {
  if (!base.includes('calendly.com')) return base
  try {
    const u = new URL(base)
    u.searchParams.set('name', nombre)
    u.searchParams.set('email', correo)
    return u.toString()
  } catch {
    return base
  }
}

export default function Agenda() {
  const [datos, setDatos] = useState(INICIAL)
  const [errores, setErrores] = useState({})
  const [estado, setEstado] = useState('idle') // idle | enviando | listo | error
  const formRef = useRef(null)
  const exitoRef = useRef(null)

  const limpiarError = (campo) => errores[campo] && setErrores((e) => ({ ...e, [campo]: undefined }))

  const onTexto = (campo) => (ev) => {
    setDatos((d) => ({ ...d, [campo]: ev.target.value }))
    limpiarError(campo)
  }

  const onRed = (red) => {
    setDatos((d) => ({
      ...d,
      redes: d.redes.includes(red) ? d.redes.filter((r) => r !== red) : [...d.redes, red],
    }))
    limpiarError('redes')
  }

  async function enviar(ev) {
    ev.preventDefault()
    const e = validar(datos)
    setErrores(e)
    const primero = ORDEN.find((k) => e[k])
    if (primero) {
      formRef.current?.querySelector(`[data-campo="${primero}"]`)?.focus()
      return
    }

    // Campo trampa anti-spam: si un bot lo llena, no enviamos nada
    if (datos.web) return setEstado('listo')

    setEstado('enviando')
    try {
      if (APPS_SCRIPT_URL) {
        await fetch(APPS_SCRIPT_URL, {
          method: 'POST',
          mode: 'no-cors', // Google Apps Script no devuelve CORS: enviamos sin leer la respuesta
          body: new URLSearchParams({
            nombre: datos.nombre.trim(),
            whatsapp: datos.whatsapp.trim(),
            correo: datos.correo.trim(),
            negocio: datos.negocio.trim(),
            redes: datos.redes.join(', '),
            inversion: datos.inversion,
            origen: origen(),
          }),
        })
      } else {
        console.warn('[Agenda] Falta VITE_APPS_SCRIPT_URL en .env: los datos NO se guardaron.')
      }
      setEstado('listo')
    } catch (err) {
      console.error(err)
      setEstado('error')
    }
  }

  useEffect(() => {
    if (estado !== 'listo' || !exitoRef.current) return
    exitoRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    exitoRef.current.focus({ preventScroll: true })
  }, [estado])

  const nombreCorto = datos.nombre.trim().split(/\s+/)[0]
  const hayErrores = ORDEN.some((k) => errores[k])

  return (
    <section id="agenda" className="scroll-mt-6 px-5 pb-24 pt-20 md:px-8 md:pb-32 md:pt-28">
      <div className="mx-auto max-w-xl">
        {estado !== 'listo' ? (
          <>
            <div data-reveal className="text-center">
              <h2 className="text-balance text-3xl font-medium leading-tight tracking-[-0.02em] md:text-[2.75rem]">
                {agenda.titulo}
              </h2>
              <p className="mx-auto mt-4 max-w-md text-pretty text-fg-2 md:text-lg">{agenda.intro}</p>
            </div>

            <form
              ref={formRef}
              data-reveal
              data-oculta-cta
              onSubmit={enviar}
              noValidate
              className="relative mt-12 grid gap-7 rounded-2xl border border-line bg-surface p-6 sm:p-9"
            >
              <Campo id="nombre" label={campos.nombre.label} error={errores.nombre}>
                <input
                  id="nombre"
                  data-campo="nombre"
                  type="text"
                  autoComplete="name"
                  className="field"
                  placeholder={campos.nombre.placeholder}
                  value={datos.nombre}
                  onChange={onTexto('nombre')}
                  aria-invalid={!!errores.nombre}
                  aria-describedby={errores.nombre ? 'nombre-error' : undefined}
                  required
                />
              </Campo>

              <Campo id="whatsapp" label={campos.whatsapp.label} ayuda={campos.whatsapp.ayuda} error={errores.whatsapp}>
                <input
                  id="whatsapp"
                  data-campo="whatsapp"
                  type="tel"
                  inputMode="tel"
                  autoComplete="tel"
                  className="field"
                  placeholder={campos.whatsapp.placeholder}
                  value={datos.whatsapp}
                  onChange={onTexto('whatsapp')}
                  aria-invalid={!!errores.whatsapp}
                  aria-describedby={errores.whatsapp ? 'whatsapp-ayuda whatsapp-error' : 'whatsapp-ayuda'}
                  required
                />
              </Campo>

              <Campo id="correo" label={campos.correo.label} error={errores.correo}>
                <input
                  id="correo"
                  data-campo="correo"
                  type="email"
                  inputMode="email"
                  autoComplete="email"
                  className="field"
                  placeholder={campos.correo.placeholder}
                  value={datos.correo}
                  onChange={onTexto('correo')}
                  aria-invalid={!!errores.correo}
                  aria-describedby={errores.correo ? 'correo-error' : undefined}
                  required
                />
              </Campo>

              <Campo id="negocio" label={campos.negocio.label} error={errores.negocio}>
                <textarea
                  id="negocio"
                  data-campo="negocio"
                  rows={3}
                  className="field min-h-24 resize-y"
                  placeholder={campos.negocio.placeholder}
                  value={datos.negocio}
                  onChange={onTexto('negocio')}
                  aria-invalid={!!errores.negocio}
                  aria-describedby={errores.negocio ? 'negocio-error' : undefined}
                  required
                />
              </Campo>

              <fieldset aria-describedby={errores.redes ? 'redes-error' : undefined}>
                <legend className="label">{campos.redes.label}</legend>
                <div className="grid grid-cols-2 gap-2.5">
                  {campos.redes.opciones.map((red, i) => {
                    const on = datos.redes.includes(red)
                    return (
                      <Opcion key={red} activa={on} invalida={!!errores.redes}>
                        <input
                          type="checkbox"
                          className="peer sr-only"
                          data-campo={i === 0 ? 'redes' : undefined}
                          checked={on}
                          onChange={() => onRed(red)}
                          aria-invalid={!!errores.redes}
                        />
                        <span
                          className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-[6px] border ${
                            on ? 'border-fg bg-fg text-bg' : 'border-line-strong'
                          }`}
                        >
                          {on && <IconCheck className="h-3.5 w-3.5" strokeWidth={2.4} />}
                        </span>
                        {red}
                      </Opcion>
                    )
                  })}
                </div>
                <Error id="redes-error" texto={errores.redes} />
              </fieldset>

              <fieldset aria-describedby={errores.inversion ? 'inversion-error' : undefined}>
                <legend className="label">{campos.inversion.label}</legend>
                <div className="grid gap-2.5">
                  {campos.inversion.opciones.map((op, i) => {
                    const on = datos.inversion === op
                    return (
                      <Opcion key={op} activa={on} invalida={!!errores.inversion}>
                        <input
                          type="radio"
                          name="inversion"
                          value={op}
                          className="peer sr-only"
                          data-campo={i === 0 ? 'inversion' : undefined}
                          checked={on}
                          onChange={onTexto('inversion')}
                          aria-invalid={!!errores.inversion}
                        />
                        <span
                          className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                            on ? 'border-fg' : 'border-line-strong'
                          }`}
                        >
                          {on && <span className="h-2.5 w-2.5 rounded-full bg-fg" />}
                        </span>
                        {op}
                      </Opcion>
                    )
                  })}
                </div>
                <Error id="inversion-error" texto={errores.inversion} />
              </fieldset>

              {/* Campo trampa anti-spam: invisible para personas */}
              <div className="absolute -left-[9999px] h-px w-px overflow-hidden" aria-hidden="true">
                <label>
                  Sitio web
                  <input type="text" tabIndex={-1} autoComplete="off" value={datos.web} onChange={onTexto('web')} />
                </label>
              </div>

              <div className="grid gap-4 pt-1">
                <div aria-live="polite" className="empty:hidden">
                  {hayErrores && <Error texto={msg.resumen} />}
                  {estado === 'error' && <Error texto={msg.envio} />}
                </div>
                <button type="submit" className="btn-primary w-full" disabled={estado === 'enviando'}>
                  {estado === 'enviando' ? agenda.enviando : agenda.boton}
                </button>
                <p className="text-center text-sm text-fg-2">{agenda.privacidad}</p>
              </div>
            </form>
          </>
        ) : (
          <div ref={exitoRef} tabIndex={-1} data-oculta-cta className="scroll-mt-6 outline-none">
            <div className="text-center">
              <h2 className="text-balance text-3xl font-medium leading-tight tracking-[-0.02em] md:text-[2.75rem]">
                {agenda.exito.titulo(nombreCorto)}
              </h2>
              <p className="mx-auto mt-4 max-w-md text-pretty text-fg-2 md:text-lg">{agenda.exito.texto}</p>
            </div>

            <div className="mt-10 overflow-hidden rounded-2xl border border-line bg-surface">
              {/* CALENDARIO: pegar aquí el embed
                  → el link va en el archivo .env → VITE_CALENDAR_URL
                    (Calendly, Google Calendar o Cal.com) */}
              {CALENDAR_URL ? (
                <iframe
                  src={urlCalendario(CALENDAR_URL, datos)}
                  title="Calendario para agendar tu llamada"
                  className="block h-[720px] w-full border-0"
                />
              ) : (
                <div className="flex aspect-[4/5] flex-col items-center justify-center gap-4 p-6 text-center sm:aspect-[4/3]">
                  <IconCalendar className="h-8 w-8 text-fg-2" />
                  <p className="text-fg-2">{agenda.exito.sinCalendario}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

function Campo({ id, label, ayuda, error, children }) {
  return (
    <div>
      <label htmlFor={id} className="label">
        {label}
      </label>
      {children}
      {ayuda && (
        <p id={`${id}-ayuda`} className="mt-2 text-sm text-fg-2">
          {ayuda}
        </p>
      )}
      <Error id={`${id}-error`} texto={error} />
    </div>
  )
}

function Opcion({ activa, invalida, children }) {
  return (
    <label
      className={`flex min-h-12 cursor-pointer select-none items-center gap-3 rounded-xl border px-4 py-3 text-[0.975rem] transition-colors duration-150 has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-fg has-[:focus-visible]:[outline-style:solid] ${
        activa
          ? 'border-fg text-fg'
          : invalida
            ? 'border-fg/70 text-fg'
            : 'border-line-strong text-fg hover:border-fg-2'
      }`}
    >
      {children}
    </label>
  )
}

function Error({ id, texto }) {
  if (!texto) return null
  return (
    <p id={id} role={id ? undefined : 'alert'} className="mt-2.5 flex items-start gap-2 text-sm font-medium text-fg">
      <IconAlert className="mt-px h-[18px] w-[18px] shrink-0" />
      {texto}
    </p>
  )
}
