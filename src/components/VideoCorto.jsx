import { VIDEO_CORTO_URL, VIDEO_CORTO_FORMATO } from '../config.js'
import SectionHeading from './SectionHeading.jsx'
import VideoEmbed from './VideoEmbed.jsx'

export default function VideoCorto() {
  const vertical = VIDEO_CORTO_FORMATO === '9:16'

  return (
    <section id="antes-y-despues" className="border-y border-line bg-surface/40">
      <div className="mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-32">
        {/* TEXTO: título del segundo video */}
        <SectionHeading
          align="center"
          eyebrow="Antes y después"
          title="Así se ve el sistema funcionando"
          intro="De grabar un video a tenerlo publicado en tus redes, en un solo flujo."
        />

        {/* ============================================================
            <!-- VIDEO_CORTO -->
            Segundo video corto (ej: "antes y después" del sistema).
            Pega el link de embed en src/config.js → VIDEO_CORTO_URL
            y elige el formato en VIDEO_CORTO_FORMATO ('16:9' o '9:16').
            ============================================================ */}
        <div data-reveal className={`mx-auto mt-12 md:mt-16 ${vertical ? 'max-w-sm' : 'max-w-4xl'}`}>
          <VideoEmbed
            src={VIDEO_CORTO_URL}
            ratio={VIDEO_CORTO_FORMATO}
            title="Antes y después del sistema"
            label="Video corto"
            hint="Pega el link en VIDEO_CORTO_URL"
          />
        </div>
      </div>
    </section>
  )
}
