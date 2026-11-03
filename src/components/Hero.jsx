import { MARCA, MARCA_LEMA, VIDEO_CLASE_URL } from '../config.js'
import VideoEmbed from './VideoEmbed.jsx'
import { IconArrowDown } from './Icons.jsx'

export default function Hero() {
  return (
    <header className="relative">
      {/* Barra superior: nombre de la marca */}
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5 md:px-8 md:py-7">
        <a href="#" className="flex items-baseline gap-2 text-fg" aria-label={`${MARCA} — inicio`}>
          {/* FOTO/LOGO: si tienes logo, reemplaza este texto por <img src="/logo.svg" alt="Santiago" className="h-7" /> */}
          <span className="text-lg font-medium tracking-tight">{MARCA}</span>
          <span className="hidden text-sm text-fg-3 sm:inline">| {MARCA_LEMA}</span>
        </a>
        <a href="#agenda" className="btn-ghost hidden min-h-10 px-5 text-sm md:inline-flex">
          Agendar llamada
        </a>
      </div>

      <div className="mx-auto max-w-6xl px-5 pb-20 pt-4 text-center md:px-8 md:pb-32 md:pt-16">
        {/* TEXTO: etiqueta pequeña */}
        <p data-reveal className="eyebrow inline-flex items-center rounded-full border border-line-strong px-4 py-1.5">
          Clase gratuita
        </p>

        {/* TEXTO: titular principal */}
        <h1
          data-reveal
          className="mx-auto mt-6 max-w-4xl text-balance text-[2.15rem] font-medium leading-[1.1] tracking-[-0.025em] sm:text-5xl md:mt-9 md:text-6xl lg:text-[4.25rem]"
        >
          Cómo automatizar tus redes sociales con IA:{' '}
          <span className="text-fg-2">Claude edita y publica por ti</span>
        </h1>

        {/* TEXTO: subtítulo */}
        <p data-reveal className="mx-auto mt-5 max-w-xl text-pretty text-lg text-fg-2 md:mt-8 md:text-xl">
          Mira el video completo antes de agendar tu llamada
        </p>

        {/* ============================================================
            <!-- VIDEO_CLASE -->
            Video principal de la clase. Pega el link de embed de YouTube
            o Vimeo en src/config.js → VIDEO_CLASE_URL
            ============================================================ */}
        <div data-reveal className="mx-auto mt-8 max-w-5xl md:mt-14">
          <VideoEmbed
            src={VIDEO_CLASE_URL}
            title="Clase gratuita: cómo automatizar tus redes sociales con IA"
            label="Video de la clase"
            hint="Pega el link de YouTube o Vimeo en VIDEO_CLASE_URL"
          />
        </div>

        <div data-reveal className="mt-10 flex flex-col items-center gap-4 md:mt-12">
          <a href="#agenda" data-cta-hero className="btn-primary w-full max-w-sm sm:w-auto sm:px-10">
            Quiero agendar mi llamada
            <IconArrowDown className="h-5 w-5" />
          </a>
          {/* TEXTO: nota debajo del botón */}
          <p className="text-sm text-fg-3">La llamada no tiene costo. Primero vemos si el programa es para ti.</p>
        </div>
      </div>
    </header>
  )
}
