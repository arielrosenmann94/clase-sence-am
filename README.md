# clasesam — Material de clases (HTML, CSS, Bootstrap, JavaScript, jQuery + Git)

## Introducción ejecutiva
Este repositorio reúne material práctico para clases orientadas a **desarrollo web front-end** y fundamentos de flujo de trabajo con **Git**. El enfoque es 100% “aprender haciendo”: cada archivo HTML es una **demo ejecutable** (sin build, sin instalaciones) para explicar conceptos clave y luego modificarlos en clase.

Incluye además notas de arquitectura (nivel senior) para un **carrito de compra** en Django SSR, útil como puente hacia desarrollo web backend y e-commerce.

---

## Bajada técnica (cómo está construido)
- **Ejecución directa en navegador**: la mayoría de los ejemplos son **HTML estático** con CSS/JS embebido o referenciado.
- **Dependencias por CDN** (cuando aplica):
  - **Bootstrap 4** para estilos rápidos de UI.
  - **jQuery 3.5.1** para eventos y animaciones.
- **Assets compartidos** en `assets/`:
  - CSS base (estilos generales y responsive).
  - JS base para páginas tipo “public_site”.
  - Imagen de ejemplo para prácticas.
- **Módulo jQuery** con demos separadas por tema (show/hide, fade, eventos, etc.) + README dedicado.
- **Notas** (`notas.md`) con una guía de arquitectura y checklist para terminar un carrito/checkout (enfoque Django SSR).

---

## Contenido principal

### 1) Demos base (archivos en raíz)
- `clase_html.html`  
  Base para explicar estructura HTML (head/body, secciones, listas, etc.).
- `clase_css.html`  
  Base para explicar estilos y clases CSS.
- `clase_boostrap.html` / `pagina_web _boostrap.html` / `panel_boostrap.html`  
  Ejemplos usando Bootstrap para construir UI rápidamente (componentes, layout).
- `js_1.html`  
  Ejercicio aplicado en JavaScript (por ejemplo calculadora de IMC).
- `clasejs_2.html`  
  Base para continuar JS (eventos, DOM, lógica).
- `ejemplos.html`  
  Demo aplicada tipo “Registro — Evento en línea de Programadores 2026” (ideal para formularios y UX).
- `git.html`  
  Apoyo visual/guía para temas Git (según contenido del archivo).
- `pdp.html` / `otroarchiv.html`  
  Archivos auxiliares para práctica/plantillas.

### 2) Módulo jQuery (carpeta `jquery/`)
Demos enfocadas en:
- visibilidad (`show/hide`)
- opacidad (`fadeIn/fadeOut`)
- eventos (varias variantes)
- una página índice con navegación y ejemplos

Incluye documentación en:
- `jquery/README.md` (explicación ejecutiva + bajada técnica de las animaciones)

### 3) Sitio “public_site” (carpeta `public_site/`)
Mini sitio multipágina (útil para explicar navegación, assets, estructura de páginas):
- `public_site/home.html`
- `public_site/services.html`
- `public_site/contact.html`

### 4) Assets compartidos (carpeta `assets/`)
- `assets/css/main.css`  
- `assets/css/media.css`  
- `assets/css/public_site.css`  
- `assets/js/main.js`  
- `assets/js/public_site.js`  
- `assets/img/perrito.jpeg`  

### 5) Notas de arquitectura (archivo `notas.md`)
Documento de nivel técnico (arquitectura + checklist) para implementar o cerrar un **carrito de compra** (enfoque SSR, recomendado para Django).

---

## Estructura del repositorio (referencial)
