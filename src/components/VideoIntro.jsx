import { useState } from 'react'
import { video } from '../content.js'
import { IconPlay } from './Icons.jsx'
import { HudCorners } from './Pixel.jsx'

/* Saca la miniatura de YouTube si el link es de YouTube */
function miniaturaYouTube(url) {
  const m = url.match(/(?:youtube\.com\/(?:embed\/|shorts\/|watch\?v=)|youtu\.be\/)([\w-]{6,})/)
  return m ? `https://i.ytimg.com/vi/${m[1]}/hqdefault.jpg` : ''
}

function conAutoplay(url) {
  try {
    const u = new URL(url)
    u.searchParams.set('autoplay', '1')
    if (u.hostname.includes('youtube')) {
      u.searchParams.set('rel', '0')
      u.searchParams.set('playsinline', '1')
    }
    return u.toString()
  } catch {
    return url
  }
}

/**
 * Video principal. Para que la página abra rápido, el reproductor de
 * YouTube/Vimeo solo se carga cuando la persona toca "play".
 */
export default function VideoIntro() {
  const [reproduciendo, setReproduciendo] = useState(false)
  const hayVideo = Boolean(video.url)
  const portada = video.portada || miniaturaYouTube(video.url)

  return (
    <div className="mx-auto w-full">
      <div className="relative">
        {/* Esquinas tipo visor */}
        <HudCorners />
        <div className="relative aspect-video w-full overflow-hidden rounded-lg border border-line-strong bg-surface">
          {!hayVideo ? (
            /* Sin video todavía: espacio reservado (no es un botón porque no hace nada) */
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-4">
              <span
                aria-hidden="true"
                className="flex h-16 w-16 items-center justify-center rounded-md border border-tech/60 bg-bg/70 text-tech md:h-20 md:w-20"
              >
                <IconPlay className="ml-1 h-6 w-6 md:h-7 md:w-7" />
              </span>
              <p className="font-mono text-xs uppercase tracking-[0.14em] text-fg-2">{video.textoSinVideo}</p>
            </div>
          ) : reproduciendo ? (
            <iframe
              src={conAutoplay(video.url)}
              title={video.titulo}
              className="absolute inset-0 h-full w-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen"
              allowFullScreen
              referrerPolicy="strict-origin-when-cross-origin"
            />
          ) : (
            <button
              type="button"
              onClick={() => setReproduciendo(true)}
              aria-label={`Reproducir: ${video.titulo}`}
              className="group absolute inset-0 flex h-full w-full cursor-pointer items-center justify-center focus-visible:outline-offset-[-4px]"
            >
              {portada && (
                <img
                  src={portada}
                  alt=""
                  className="absolute inset-0 h-full w-full object-cover opacity-70 transition-opacity duration-300 group-hover:opacity-80"
                />
              )}
              <span className="relative flex h-16 w-16 items-center justify-center rounded-md border border-tech/60 bg-bg/70 text-tech transition-[transform,border-color] duration-200 group-hover:scale-105 group-hover:border-tech md:h-20 md:w-20">
                <IconPlay className="ml-1 h-6 w-6 md:h-7 md:w-7" />
              </span>
            </button>
          )}
        </div>
      </div>

      {/* Barra técnica debajo del video */}
      <div aria-hidden="true" className="mt-4 flex items-center justify-between font-mono text-[0.7rem] uppercase tracking-[0.14em] text-fg-2 md:mt-5 md:text-xs">
        <span className="flex items-center gap-2">
          <span className="h-1.5 w-1.5 bg-tech" />
          {video.archivo}
        </span>
        <span>{video.detalle}</span>
      </div>
    </div>
  )
}
