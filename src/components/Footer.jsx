import { footer, marca } from '../content.js'
import { IconInstagram, IconWhatsapp } from './Icons.jsx'
import { PixelLogo } from './Pixel.jsx'

const linkWhatsapp = `https://wa.me/${footer.whatsapp.numero}?text=${encodeURIComponent(footer.whatsapp.mensaje)}`

const enlace =
  'inline-flex min-h-11 items-center gap-2.5 rounded-md px-3 text-fg-2 transition-colors duration-150 hover:text-tech'

export default function Footer() {
  return (
    <footer className="border-t border-line px-5 pb-28 pt-12 md:px-8 md:pb-12">
      <div className="mx-auto flex max-w-5xl flex-col items-center gap-6 text-center md:flex-row md:justify-between md:text-left">
        <div className="flex flex-col items-center gap-3 md:items-start">
          <p className="flex items-center gap-3 text-sm text-fg-2">
            <PixelLogo size={2} className="text-tech" />
            <span>
              <span className="font-medium text-fg">{marca}</span> · {footer.lema}
            </span>
          </p>
          <p className="flex items-center gap-2 font-mono text-[0.7rem] uppercase tracking-[0.14em] text-fg-2">
            <span className="h-1.5 w-1.5 animate-pulse bg-tech motion-reduce:animate-none" aria-hidden="true" />
            {footer.estado}
          </p>
        </div>
        <nav aria-label="Redes" className="flex items-center gap-2">
          <a href={footer.instagram.url} target="_blank" rel="noreferrer" className={enlace}>
            <IconInstagram className="h-5 w-5" />
            {footer.instagram.texto}
          </a>
          <a href={linkWhatsapp} target="_blank" rel="noreferrer" className={enlace}>
            <IconWhatsapp className="h-5 w-5" />
            {footer.whatsapp.texto}
          </a>
        </nav>
      </div>
    </footer>
  )
}
