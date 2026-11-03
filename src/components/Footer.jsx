import { INSTAGRAM_URL, INSTAGRAM_USUARIO, MARCA, MARCA_LEMA, whatsappLink } from '../config.js'
import { IconInstagram, IconWhatsapp } from './Icons.jsx'

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="border-t border-line pb-28 md:pb-0">
      <div className="mx-auto max-w-6xl px-5 py-16 md:px-8 md:py-20">
        <div className="flex flex-col gap-10 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-2xl font-medium tracking-tight">{MARCA}</p>
            <p className="mt-2 text-fg-2">{MARCA_LEMA}</p>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row">
            <a href={whatsappLink()} target="_blank" rel="noreferrer" className="btn-ghost">
              <IconWhatsapp className="h-5 w-5" />
              Escríbeme por WhatsApp
            </a>
            <a href={INSTAGRAM_URL} target="_blank" rel="noreferrer" className="btn-ghost">
              <IconInstagram className="h-5 w-5" />
              {INSTAGRAM_USUARIO}
            </a>
          </div>
        </div>

        {/* TEXTO: aviso legal — revísalo y ajústalo a tu país */}
        <details id="aviso-legal" className="group mt-14 scroll-mt-6 border-t border-line pt-8">
          <summary className="flex cursor-pointer list-none items-center gap-2 text-sm text-fg-2 hover:text-fg [&::-webkit-details-marker]:hidden">
            Aviso legal y privacidad
            <span className="transition-transform duration-200 group-open:rotate-180" aria-hidden="true">
              ↓
            </span>
          </summary>
          <div className="mt-5 max-w-3xl space-y-3 text-sm leading-relaxed text-fg-3">
            <p>
              El contenido de esta página y de la clase es educativo. No prometemos ingresos, seguidores ni resultados
              específicos: lo que logre cada persona depende de su negocio, su contenido y su constancia. Los testimonios
              son experiencias individuales y no garantizan resultados similares.
            </p>
            <p>
              Los datos que envías en el formulario (nombre, WhatsApp, correo y respuestas) se usan solo para contactarte
              sobre el programa {`"Redes Automatizadas 1 a 1"`} y no se venden ni se comparten con terceros. Puedes pedir
              que los eliminemos escribiendo por WhatsApp o a [tu correo de contacto].
            </p>
            <p>
              Claude es una marca de Anthropic. Instagram y Facebook son marcas de Meta; TikTok, YouTube y otras redes
              pertenecen a sus respectivos dueños. Esta página no está afiliada ni patrocinada por ninguna de ellas.
            </p>
          </div>
        </details>

        <p className="mt-10 text-xs text-fg-3">
          © {year} {MARCA}. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  )
}
