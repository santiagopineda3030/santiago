import { useState } from 'react'
import { video } from '../content.js'
import { IconPlay } from './Icons.jsx'

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
    <div className="relative mx-auto aspect-video w-full overflow-hidden rounded-2xl border border-line-strong bg-surface">
      {!hayVideo ? (
        /* Sin video todavía: espacio reservado (no es un botón porque no hace nada) */
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4">
          <span
            aria-hidden="true"
            className="flex h-16 w-16 items-center justify-center rounded-full border border-line-strong bg-bg/70 text-fg md:h-20 md:w-20"
          >
            <IconPlay className="ml-1 h-6 w-6 md:h-7 md:w-7" />
          </span>
          <p className="text-sm text-fg-2">{video.textoSinVideo}</p>
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
          <span className="relative flex h-16 w-16 items-center justify-center rounded-full border border-line-strong bg-bg/70 text-fg transition-transform duration-200 group-hover:scale-105 md:h-20 md:w-20">
            <IconPlay className="ml-1 h-6 w-6 md:h-7 md:w-7" />
          </span>
        </button>
      )}
    </div>
  )
}
