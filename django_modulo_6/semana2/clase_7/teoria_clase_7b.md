# 🌐 Django — Módulo 6 · Clase 7B

## Por qué un sitio web carga rápido (o lento)

---

> _"La velocidad no es una característica. Es la ausencia de lo que molesta."_

---

## Intro: ¿Por qué importa la velocidad?

Antes de hablar de técnicas, hay que entender por qué la velocidad de un sitio es una decisión de negocio — no solo un detalle técnico.

**Amazon** calculó que cada 100ms de latencia adicional les costaba un **1% de ventas**.

**Google** descubrió que pasar de 0.4 a 0.9 segundos de carga en búsquedas redujo el tráfico un **20%**.

**Deloitte & Google (2019)** midieron que una mejora de **0.1 segundos** en el tiempo de carga produce un **aumento del 8% en conversiones** en retail.

El cerebro percibe las esperas como fricción. La fricción genera desconfianza. La desconfianza genera abandono.

> El sitio lento no pierde usuarios porque es lento. Los pierde porque la lentitud comunica descuido, y el descuido destruye la percepción de calidad de todo lo demás.

### El umbral del cerebro: ¿qué es "instantáneo"?

La neurociencia tiene respuestas bastante precisas:

| Tiempo de respuesta | Cómo lo percibe el cerebro                                           |
| ------------------- | -------------------------------------------------------------------- |
| **< 100ms**         | Instantáneo. Causa y efecto se sienten como la misma cosa            |
| **100ms – 300ms**   | Muy rápido. El usuario percibe que el sistema responde               |
| **300ms – 1000ms**  | Tolerable. Se nota la espera pero no interrumpe el flujo             |
| **1s – 3s**         | Frustrante. El usuario empieza a preguntarse si algo falló           |
| **> 3s**            | Abandono. El 53% de usuarios móviles cierra la página (Google, 2018) |

El umbral de lo instantáneo son **100ms** — eso es lo que el cerebro necesita para que causa y efecto se sientan conectados.

Diez años de redes sociales entrenaron ese cerebro para esperar respuestas casi instantáneas: TikTok muestra el primer video en menos de 1 segundo, Instagram carga fotos antes de terminar de hacer scroll, WhatsApp envía el mensaje antes de levantar el dedo. Ese condicionamiento no se apaga cuando el usuario entra a un sitio web cualquiera.

> La competencia real de cualquier sitio no es el sitio de su industria — es la velocidad de Instagram. El cerebro compara todo contra lo más rápido que conoce.

---

---

# Parte I — Qué pasa entre el clic y la pantalla

---

Cuando alguien hace clic en un link o escribe una URL, se dispara una cadena de eventos que la mayoría de los developers no visualiza completamente. Entender esa cadena es el primer paso para optimizar.

## El viaje de una página web

```
1. RESOLUCIÓN DNS
   El browser pregunta: "¿cuál es la dirección IP de midominio.com?"
   Un servidor DNS responde con la IP.
   → Tiempo típico: 20-120ms

2. CONEXIÓN TCP
   El browser establece una conexión con el servidor.
   Requiere un "handshake" de 3 pasos.
   → Tiempo típico: 20-100ms

   📦 Qué es un handshake: es un saludo formal entre dos partes antes de hablar.
   SYN y ACK son señales de control del protocolo TCP — no son datos, no son claves.
   SYN (Synchronize) = "quiero iniciar una conexión contigo".
   ACK (Acknowledge) = "recibí tu mensaje y lo confirmo".
   SYN-ACK = ambas a la vez: el servidor confirma el SYN recibido y manda el suyo propio.

   El browser dice "quiero conectarme" (SYN).
   El servidor responde "recibí tu mensaje, yo también quiero" (SYN-ACK).
   El browser confirma "perfecto, empecemos" (ACK).
   Esos 3 mensajes = 3 "pasos" del handshake. Sin esa confirmación mutua, ningún dato viaja.


3. NEGOCIACIÓN TLS (si el sitio usa HTTPS)
   El browser y el servidor intercambian certificados para cifrar la comunicación.
   → Tiempo adicional: 30-100ms

4. REQUEST HTTP
   El browser envía la URL — no pide "el HTML" explícitamente.
   Manda: método (GET), ruta (/home/), y headers (tipo de browser, idioma, etc.).
   El servidor lee eso y decide qué responder: HTML, JSON, un redirect o un error.
   Django corre aquí del lado del servidor.
   → Tiempo de viaje: 10-50ms (mismo país) | 80-300ms (otro continente)

5. RESPUESTA DEL SERVIDOR ← aquí es donde vive todo el código Django
   Cuando el request llega al servidor, Django lo recibe y ejecuta el siguiente flujo:
     a) El Router (urls.py) lee la URL y decide qué vista ejecutar
     b) La Vista (views.py) corre la lógica: consulta la DB, procesa datos, prepara el contexto
     c) El Template Engine renderiza el HTML final con los datos del contexto
     d) Django arma la respuesta HTTP y la envía de vuelta al browser
   Todo eso ocurre antes de que el browser reciba una sola línea de HTML.
   → Vista simple sin DB: 5-50ms | Con queries a DB: 50-500ms | Reportes complejos: 500ms- > 5s


6. DESCARGA DEL HTML
   El browser empieza a recibir el HTML.

7. PARSING DEL HTML
   El browser lee el HTML y construye el DOM.
   Cada vez que encuentra un <link>, <script> o <img>, hace un nuevo request.

8. DESCARGA DE RECURSOS (CSS, JS, imágenes, fuentes)
   Múltiples requests en paralelo o en serie.

9. RENDER
   El browser combina DOM + CSS y pinta la pantalla.
```

Cada uno de esos pasos tiene un costo de tiempo. La velocidad total es la suma de todos.

---

## La metáfora del restaurante

Un sitio web lento funciona como un restaurante mal organizado:

| Problema                 | Restaurante              | Web                                    |
| ------------------------ | ------------------------ | -------------------------------------- |
| El mozo no llega         | DNS lento                | El servidor tarda en responder         |
| La cocina demora         | Servidor lento           | Vista Django con queries lentas        |
| Traen todo de a uno      | Recursos sin paralelizar | CSS, JS e imágenes que bloquean        |
| El plato llega frío      | Sin compresión ni caché  | Archivos grandes sin optimizar         |
| No hay lugar para sentar | Sin CDN                  | Servidor físicamente lejos del usuario |

La experiencia total del comensal depende de todos los pasos juntos.

---

---

# Parte II — Los tres cuellos de botella

---

La velocidad de un sitio tiene tres grandes áreas de responsabilidad. Cada una tiene sus propias palancas:

## 1. El servidor (backend)

Lo que hace Django antes de enviar la respuesta.

**Problemas típicos:**

- Queries a la base de datos sin índices
- Demasiadas queries para generar una sola página (el problema N+1)
- Lógica de negocio compleja que corre en cada request
- Imágenes o archivos generados en tiempo real sin caché

**El principio**: el servidor debería hacer el mínimo trabajo posible por request. Lo que se puede precalcular, se pre-calcula. Lo que se puede guardar en caché, se guarda.

---

## 2. La red (transferencia)

Lo que viaja entre el servidor y el browser del usuario.

**Problemas típicos:**

- Archivos HTML, CSS y JS sin comprimir (texto plano viaja más pesado)
- Imágenes en resolución original sin redimensionar
- Muchos archivos pequeños en lugar de pocos archivos grandes
- Servidor en otro continente que el usuario

**El principio**: enviar menos datos, desde más cerca, una sola vez.

---

## 3. El browser (frontend)

Lo que hace el browser del usuario una vez que recibe los archivos.

**Problemas típicos:**

- JavaScript que bloquea el renderizado del HTML
- CSS que no llega antes de que se muestre contenido
- Fuentes de Google que se cargan tarde (el texto aparece invisible)
- Imágenes que no tienen dimensiones declaradas (el layout "salta")

**El principio**: el browser debería poder mostrar algo útil tan pronto como sea posible, aunque no todo esté listo.

---

---

# Parte III — Conceptos clave (sin código)

---

## Caché: la memoria del sitio

El caché es guardar una respuesta ya calculada para reutilizarla la próxima vez, en lugar de calcularla de nuevo.

Hay tres niveles de caché:

**Browser cache**: el browser guarda copias de CSS, JS e imágenes. La segunda vez que el usuario visita el sitio, no los descarga de nuevo.

**Servidor cache**: Django puede guardar el resultado de una vista compleja en memoria. El próximo request no toca la base de datos — devuelve la copia guardada.

**CDN (Content Delivery Network)**: servidores distribuidos alrededor del mundo que guardan copias estáticas del sitio. El usuario se conecta al servidor más cercano geográficamente, no al original.

> La mejor request es la que no existe. Si el browser ya tiene el archivo, no hay request.

---

## Compresión: menos datos, misma información

Todo texto (HTML, CSS, JavaScript) se puede comprimir antes de enviarlo. El servidor lo comprime, el browser lo descomprime en microsegundos.

La compresión más común reduce el tamaño de los archivos de texto entre un **60% y un 80%**.

Es el cambio de mayor impacto con menor esfuerzo: se activa con una línea de configuración en el servidor y no requiere cambiar nada del código.

---

## Critical Path: qué debe llegar primero

El **Critical Path** (ruta crítica) es el conjunto mínimo de recursos que el browser necesita para mostrar el contenido visible sin hacer scroll — lo que se llama "above the fold".

La idea es simple: el CSS que controla el diseño inicial debe llegar antes que cualquier otra cosa. El JavaScript que no afecta el primer render puede esperar.

Un sitio bien construido muestra contenido útil en menos de 1 segundo, aunque no todo haya cargado todavía.

---

## Lazy Loading: cargar cuando se necesita

Las imágenes debajo de la página visible no necesitan cargarse inmediatamente. **Lazy loading** significa postergar la descarga de recursos hasta que el usuario los necesite (cuando está por llegar a esa parte de la página con el scroll).

El resultado: la parte visible carga mucho más rápido, aunque el peso total de la página sea el mismo.

---

## Performance percibida vs performance real

Este es el concepto más filosófico de todos — y el más importante.

**La performance real** es cuántos milisegundos tarda la página en cargar completamente.

**La performance percibida** es cuán rápido _siente_ el usuario que carga.

Los dos números son distintos y el segundo importa más.

Un sitio que muestra un skeleton (la estructura gris de la página) en 200ms y carga el contenido real en 800ms se siente más rápido que uno que muestra una pantalla en blanco durante 600ms y carga todo de golpe.

Netflix, YouTube y LinkedIn usan esta técnica. No porque el servidor sea más rápido — porque el usuario siente que sí.

> El usuario no mide milisegundos. Mide sensaciones. Diseñar para la percepción es tan válido como optimizar el servidor.

---

---

# Parte III-B — Cómo aplica todo esto en un proyecto Django

---

Los conceptos de la parte anterior no son abstractos. Cada uno tiene una forma concreta de aparecer en un proyecto Django. A continuación, una explicación simple de cada uno:

---

### Cache de servidor

Django puede "recordar" el resultado de una vista y devolverlo directamente la próxima vez, sin volver a consultar la base de datos.

Se hace con un decorador sobre la vista:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)   # guarda el resultado durante 15 minutos
def mi_vista(request):
    ...
```

Es útil para páginas que no cambian con frecuencia: portadas, listas de productos, páginas de inicio.

---

### Cache de browser

Cuando Django sirve archivos estáticos (CSS, JS, imágenes), el servidor puede decirle al browser "guarda este archivo durante X días". La próxima visita, el browser no los descarga de nuevo.

En producción esto lo maneja automáticamente **WhiteNoise** (librería de Django) o el servidor web (Nginx). No requiere código propio.

---

### Compresion de texto

Django incluye un middleware que comprime automáticamente el HTML, CSS y JS antes de enviarlo. Se activa agregando una sola línea en `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',   # agregar al principio
    ...
]
```

Con eso, los archivos de texto que Django envía pueden reducir su tamaño entre un 60% y un 80%.

---

### Critical Path — el orden del HTML importa

En el `base.html`, el CSS debe ir en el `<head>` para que el browser lo tenga antes de pintar la pantalla. El JavaScript, si no es necesario para el primer render, va al final del `<body>` con el atributo `defer`:

```html
<head>
  <link rel="stylesheet" href="{% static 'css/main.css' %}" />
  <!-- va aquí -->
</head>
<body>
  ...
  <script src="{% static 'js/main.js' %}" defer></script>
  <!-- al final -->
</body>
```

`defer` le dice al browser: "descargá este script pero no lo ejecutes hasta que el HTML esté listo". Así la página aparece más rápido.

---

### Lazy loading en imagenes

Las imágenes que están más abajo en la página no necesitan cargarse desde el inicio. Un solo atributo en el template lo resuelve:

```html
<img
  src="{% static 'img/foto.jpg' %}"
  loading="lazy"
  width="800"
  height="600"
  alt="..."
/>
```

`loading="lazy"` — el browser solo descarga la imagen cuando el usuario está cerca de verla.

`width` y `height` — le dicen al browser cuánto espacio reservar antes de que llegue la imagen. Sin esos atributos el layout "salta" (eso es el CLS que vimos en la tabla de métricas).

---

### Menos consultas a la base de datos

Cada consulta extra al ORM es tiempo de respuesta adicional. Django tiene dos métodos para traer datos relacionados de una sola vez:

```python
# Sin optimizar: hace una query por cada producto para buscar su categoría (problema N+1)
productos = Producto.objects.all()

# Optimizado: trae productos y categorías en una sola consulta
productos = Producto.objects.select_related('categoria').all()
```

`select_related` y `prefetch_related` son las herramientas más directas para reducir el tiempo de respuesta del servidor en Django.

---

> Ninguno de estos cambios requiere reescribir la aplicación. La mayoría son una línea en `settings.py`, un atributo en el `<img>` o el orden del CSS en el `base.html`. Lo que los hace posibles es entender por qué importan.

---

---

# Parte IV — Las reglas de oro

---

Estas reglas no son framework-específicas. Aplican a cualquier sitio web, construido con cualquier tecnología:

---

**Regla 1: Lo que no se carga es gratis**

El recurso más rápido es el que no existe. Antes de optimizar cómo carga algo, preguntarse si realmente hace falta cargarlo.

---

**Regla 2: Medir antes de optimizar**

Sin medición, la optimización es intuición disfrazada de ingeniería. Herramientas como Google PageSpeed Insights y Lighthouse miden exactamente dónde se pierde el tiempo.

---

**Regla 3: El 80/20 de la performance**

El 80% del tiempo de carga generalmente lo causan el 20% de los problemas. Normalmente: imágenes sin optimizar, JavaScript bloqueante y queries lentas a la base de datos.

---

**Regla 4: La velocidad es una feature, no un extra**

Los sitios lentos no pierdne usuarios porque el equipo de desarrollo no se preocupa. Los pierden porque la velocidad nunca entró en la conversación desde el principio. Se diseñó todo, se implementó todo, y al final se "optimizó". Ese orden es el problema.

---

**Regla 5: El usuario más lento define la experiencia**

El sitio que carga en 0.5 segundos en la notebook del developer puede tardar 8 segundos en el celular de un usuario con una conexión móvil del campo. La experiencia que importa es la del usuario más limitado, no la del equipo que lo construyó.

---

---

# Cierre

---

La performance web no es un tema de devops ni de infraestructura. Es una decisión de diseño que atraviesa cada capa del sistema: cómo se estructuran las vistas, qué se devuelve en cada request, cómo se organizan los archivos estáticos, y qué se muestra primero.

Un developer que entiende por qué un sitio es lento — antes de saber cómo arreglarlo — tiene una ventaja enorme sobre uno que solo aplica recetas.

> _"La optimización prematura es la raíz de todos los males. Pero la ignorancia de la performance es la raíz del sitio que nadie usa."_
>
> — Parafraseando a Donald Knuth

---

---

# Apéndice — Tiempos de referencia

---

Estas son las métricas que Google mide y considera al rankear un sitio. Son el estándar de la industria:

| Métrica                            | Qué mide                                        | Excelente | Aceptable | Mal     |
| ---------------------------------- | ----------------------------------------------- | --------- | --------- | ------- |
| **TTFB** (Time to First Byte)      | Cuánto tarda el servidor en empezar a responder | < 200ms   | 200-500ms | > 500ms |
| **FCP** (First Contentful Paint)   | Cuándo aparece el primer contenido en pantalla  | < 1s      | 1-2.5s    | > 2.5s  |
| **LCP** (Largest Contentful Paint) | Cuándo carga el elemento principal de la página | < 2.5s    | 2.5-4s    | > 4s    |
| **TBT** (Total Blocking Time)      | Cuánto tiempo el JS bloquea la interacción      | < 200ms   | 200-600ms | > 600ms |
| **CLS** (Layout Shift)             | Cuánto "salta" el layout mientras carga         | < 0.1     | 0.1-0.25  | > 0.25  |
| **Peso total**                     | Todos los archivos combinados                   | < 500KB   | 500KB-2MB | > 2MB   |

> Estas métricas las mide Google PageSpeed Insights de forma gratuita, con cualquier URL. El objetivo no es llegar a "excelente" en todo — es entender cuál está causando la mala experiencia y atacarla primero.

---
