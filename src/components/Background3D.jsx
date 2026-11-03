import { useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { Icosahedron, PerformanceMonitor } from '@react-three/drei'
import { IcosahedronGeometry } from 'three'

/**
 * Fondo 3D del hero (estilo tecnológico):
 * - Un icosaedro en líneas cian que gira muy lento.
 * - Una nube de "píxeles" cuadrados alrededor, girando en sentido contrario.
 * Este archivo se carga de forma diferida (ver Hero.jsx).
 *
 * lite = true → versión liviana para móvil: menos detalle,
 * resolución 1x y ~30 cuadros por segundo.
 */
const CIAN = '#22d3ee'

function Forma({ lite }) {
  const malla = useRef()
  const nube = useRef()
  const { viewport } = useThree()
  // Tamaño relativo a la pantalla para que en móvil no tape todo
  const escala = Math.min(0.92, viewport.width / 5.2)

  // Posiciones de los píxeles: vértices de una esfera geodésica más grande
  const posiciones = useMemo(() => {
    const g = new IcosahedronGeometry(2.55, lite ? 2 : 3)
    const arr = g.getAttribute('position').array
    const vistos = new Set()
    const unicos = []
    for (let i = 0; i < arr.length; i += 3) {
      const k = `${arr[i].toFixed(3)},${arr[i + 1].toFixed(3)},${arr[i + 2].toFixed(3)}`
      if (vistos.has(k)) continue
      vistos.add(k)
      unicos.push(arr[i], arr[i + 1], arr[i + 2])
    }
    g.dispose()
    return new Float32Array(unicos)
  }, [lite])

  useFrame((_, delta) => {
    const d = Math.min(delta, 0.1)
    if (malla.current) {
      malla.current.rotation.y += d * 0.06
      malla.current.rotation.x += d * 0.025
    }
    if (nube.current) nube.current.rotation.y -= d * 0.035
  })

  return (
    <group scale={escala}>
      <Icosahedron ref={malla} args={[1.9, lite ? 1 : 2]} rotation={[0.4, 0.2, 0]}>
        <meshBasicMaterial wireframe color={CIAN} transparent opacity={lite ? 0.12 : 0.13} />
      </Icosahedron>

      {/* Píxeles: los puntos sin textura se dibujan cuadrados */}
      <points ref={nube} rotation={[0.2, 0, 0.1]}>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[posiciones, 3]} />
        </bufferGeometry>
        <pointsMaterial color={CIAN} size={lite ? 0.05 : 0.04} sizeAttenuation transparent opacity={0.55} depthWrite={false} />
      </points>
    </group>
  )
}

/* En móvil pedimos un cuadro cada ~33 ms en lugar de 60 por segundo */
function Ticker30fps({ activo }) {
  const invalidate = useThree((s) => s.invalidate)
  useEffect(() => {
    if (!activo) return
    const id = setInterval(() => invalidate(), 33)
    return () => clearInterval(id)
  }, [activo, invalidate])
  return null
}

export default function Background3D({ lite = false, visible = true }) {
  const [dpr, setDpr] = useState(lite ? 1 : 1.5)
  const [listo, setListo] = useState(false)

  return (
    <div
      aria-hidden="true"
      className={`pointer-events-none absolute inset-0 transition-opacity duration-[1600ms] ease-out ${
        listo ? 'opacity-100' : 'opacity-0'
      }`}
    >
      <Canvas
        dpr={dpr}
        frameloop={!visible ? 'never' : lite ? 'demand' : 'always'}
        camera={{ position: [0, 0, 5], fov: 45 }}
        gl={{ antialias: !lite, alpha: true, powerPreference: 'low-power' }}
        onCreated={() => setListo(true)}
      >
        <PerformanceMonitor onDecline={() => setDpr(1)} />
        {lite && <Ticker30fps activo={visible} />}
        <Forma lite={lite} />
      </Canvas>
    </div>
  )
}
