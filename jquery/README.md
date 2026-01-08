# Animaciones jQuery para clases — Demo SSR (show/hide, fade, slide, animate + menú)

## Introducción ejecutiva
Este proyecto es una página HTML única, lista para usar en clases, que demuestra de forma práctica y didáctica las principales funciones de animación y visibilidad de jQuery. El objetivo es que estudiantes puedan **ver, ejecutar y modificar** ejemplos reales de:

- Mostrar/ocultar contenido
- Transiciones suaves con opacidad
- Acordeones con animación vertical
- Microinteracciones personalizadas con `animate()`
- Patrones típicos de UX para validaciones y feedback (shake, highlight)

La página incorpora un **menú sticky con scroll suave** para navegar rápidamente entre secciones durante la clase.

---

## Bajada técnica (arquitectura y funcionamiento)

### Enfoque
- **Single Page Demo (HTML único)**: todo está en un solo archivo para facilitar copiar/pegar y ejecutar sin configuración.
- **SSR estático**: no requiere servidor; se ejecuta directamente en el navegador.
- **Dependencias vía CDN**:
  - Bootstrap 4 (solo estilos, opcional)
  - jQuery 3.5.1 (core de comportamiento)

### Estructura del documento
- **Header sticky**: permanece fijo al hacer scroll para mantener el menú accesible.
- **Secciones por ID**: cada sección (`#sec-show-hide`, `#sec-fade`, etc.) contiene:
  - Explicación breve
  - Botones de acción
  - Un “target” (caja) que se anima
  - Un `<pre>` que imprime el código del ejemplo para enseñanza

### Componentes clave
1. **Menú con scroll suave**
   - Intercepta el click en links `.js-scroll`
   - Usa `$("html, body").animate({ scrollTop: ... }, 450)` con offset para el header sticky

2. **Targets (bloques a animar)**
   - `.target` parte con `display:none` para que el alumno vea claramente el efecto al iniciar
   - En algunos casos se fuerzan estilos antes de animar para controlar el “estado inicial”

3. **Uso correcto de `stop(true, true)`**
   - Antes de animar, se utiliza `stop(true,true)` para:
     - cortar animaciones previas
     - evitar acumulación de colas (bug típico en demos con muchos clics)

4. **`animate()` y limitaciones**
   - jQuery anima **propiedades CSS numéricas**: `opacity`, `marginLeft`, `width`, `height`, etc.
   - No anima transformaciones complejas como `transform: scale()` sin plugins; por eso el “pop” se **simula** con `width/padding + opacity`

---

## Requisitos
- Navegador moderno (Chrome/Firefox/Edge).
- Conexión a Internet para cargar los CDN (Bootstrap y jQuery).

---

## Cómo ejecutar (rápido)
1. Copia el código en un archivo, por ejemplo:
   - `animaciones-jquery.html`
2. Ábrelo en el navegador:
   - Doble click, o
   - Desde terminal:
     - Linux: `xdg-open animaciones-jquery.html`
     - macOS: `open animaciones-jquery.html`
     - Windows: `start animaciones-jquery.html`

---

## Qué incluye (secciones)

### 1) show() / hide() / toggle()
- Controlan la visibilidad con `display:none` sin transición.
- Útil para mostrar/ocultar bloques de forma instantánea.

### 2) fadeIn() / fadeOut() / fadeToggle()
- Transición basada en opacidad.
- Útil para mensajes, avisos, contenido “suave”.

### 3) slideDown() / slideUp() / slideToggle()
- Transición vertical ajustando altura.
- Útil para FAQ, acordeones, paneles.

### 4) animate(): animaciones personalizadas
- “Entrada/salida” combinando opacidad y desplazamiento horizontal.
- Demuestra:
  - seteo de estado inicial
  - callback al finalizar para ocultar

### 5) Extras (patrones para clase)
- **Pop In/Out (simulado)**: usa `width/padding + opacity` por limitación de `transform`.
- **Shake**: secuencia corta para feedback de error o validación.
- **Highlight**: “pulse” de opacidad + borde temporal para llamar atención.

---

## Puntos didácticos recomendados (para explicar en clase)
- Diferencia entre:
  - `toggle()` vs `fadeToggle()` vs `slideToggle()` (misma idea, distinta UX)
- Importancia de:
  - `stop(true,true)` para evitar colas
  - preparar estado inicial antes de animar (`css()` + `animate()`)
- Limitaciones reales:
  - jQuery no anima transform sin plugins; cómo resolver (simulación o CSS transitions)

---

## Personalización rápida
- Cambiar velocidades:
  - Ajusta `400`, `450`, `350` en los métodos para más rápido/lento.
- Ajustar offset del menú:
  - Variable `offset = 120` en el scroll suave.
- Mostrar targets por defecto:
  - Cambia `.target { display: none; }` a `display:block;` en casos específicos.

---

## Estructura sugerida del repo (opcional)
Si quieres publicarlo como repo didáctico:

