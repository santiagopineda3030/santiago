import { useEffect, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { Icosahedron, PerformanceMonitor } from '@react-three/drei'

/**
 * Fondo 3D del hero: un icosaedro en wireframe que gira muy lento,
 * con una luz roja suave que llega desde abajo.
 * Este archivo se carga de forma diferida (ver Hero.jsx).
 *
 * lite = true → versión liviana para móvil: menos detalle,
 * resolución 1x y ~30 cuadros por segundo.
 */
function Forma({ lite }) {
  const ref = useRef()
  const { viewport } = useThree()
  // Tamaño relativo a la pantalla para que en móvil no tape todo
  const escala = Math.min(0.92, viewport.width / 5.2)

  useFrame((_, delta) => {
    if (!ref.current) return
    const d = Math.min(delta, 0.1)
    ref.current.rotation.y += d * 0.06
    ref.current.rotation.x += d * 0.025
  })

  return (
    <Icosahedron ref={ref} args={[1.9, lite ? 1 : 2]} scale={escala} rotation={[0.4, 0.2, 0]}>
      <meshStandardMaterial
        wireframe
        color="#8a8a8a"
        roughness={1}
        metalness={0}
        transparent
        opacity={lite ? 0.32 : 0.28}
      />
    </Icosahedron>
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
        <ambientLight intensity={0.55} />
        {/* Luz roja suave y baja: el único toque de color del fondo */}
        <directionalLight position={[-1.5, -3, 1.5]} intensity={2.4} color="#e02020" />
        <Forma lite={lite} />
      </Canvas>
    </div>
  )
}
