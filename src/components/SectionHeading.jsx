export default function SectionHeading({ eyebrow, title, intro, align = 'left' }) {
  const center = align === 'center'
  return (
    <div className={center ? 'mx-auto max-w-2xl text-center' : 'max-w-2xl'}>
      {eyebrow && (
        <p data-reveal className="eyebrow">
          {eyebrow}
        </p>
      )}
      <h2
        data-reveal
        className="mt-4 text-balance text-3xl font-medium leading-[1.15] tracking-[-0.02em] md:text-5xl"
      >
        {title}
      </h2>
      {intro && (
        <p data-reveal className="mt-5 text-pretty text-lg text-fg-2">
          {intro}
        </p>
      )}
    </div>
  )
}
