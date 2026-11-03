import { IconPlay } from './Icons.jsx'

/**
 * Muestra un video de YouTube/Vimeo si le pasas `src` (link de "embed").
 * Si `src` está vacío, muestra un espacio reservado con la etiqueta indicada.
 *
 * ratio: '16:9' | '9:16' | '4:5' | '1:1'
 */
const RATIOS = {
  '16:9': 'aspect-video',
  '9:16': 'aspect-[9/16]',
  '4:5': 'aspect-[4/5]',
  '1:1': 'aspect-square',
}

export default function VideoEmbed({ src, title, label, ratio = '16:9', hint, className = '' }) {
  const aspect = RATIOS[ratio] ?? RATIOS['16:9']

  return (
    <div
      className={`relative w-full overflow-hidden rounded-2xl border border-line bg-surface ${aspect} ${className}`}
    >
      {src ? (
        <iframe
          src={src}
          title={title}
          className="absolute inset-0 h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen"
          allowFullScreen
          loading="lazy"
          referrerPolicy="strict-origin-when-cross-origin"
        />
      ) : (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 p-6 text-center">
          <span className="flex h-16 w-16 items-center justify-center rounded-full border border-line-strong text-fg md:h-20 md:w-20">
            <IconPlay className="ml-1 h-6 w-6 md:h-7 md:w-7" />
          </span>
          {label && <span className="eyebrow">{label}</span>}
          {hint && <span className="max-w-xs text-sm text-fg-3">{hint}</span>}
        </div>
      )}
    </div>
  )
}
