# 🐍 Django — Módulo 6 · Clase 3

### Teoría: Cómo piensa un programador Django (Resumen de Clase 1 y 2)

---

## Clase 3: qué vas a lograr hoy

Hoy no vamos a sumar una herramienta nueva de Django.

Hoy vas a hacer algo más importante para crecer como programador/a:

- ordenar lo aprendido en Clase 1 y Clase 2,
- entender cómo viaja la información en un proyecto Django,
- y preparar el terreno para ampliar el proyecto sin romper lo que ya funciona.

> Idea central: pasar de “seguir pasos” a “entender el sistema”.

---

## 1. Dónde estamos (qué ya construimos)

### En la Clase 1 construimos el flujo base de Django

Aprendimos a:

- crear proyecto y app,
- definir un modelo (`Producto`),
- hacer migraciones,
- usar el panel admin,
- crear vistas,
- conectar URLs,
- renderizar templates.

Eso nos dio el primer flujo completo **MVT** funcionando.

### En la Clase 2 profesionalizamos el proyecto

Aprendimos a:

- entender la anatomía del proyecto (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`),
- usar una estructura más clara (`config/`),
- mover lógica de negocio al modelo,
- trabajar con **sesiones** (carrito),
- usar **Forms** de Django,
- aplicar **herencia de templates** con `base.html`.

> Si la Clase 1 fue “hacer que funcione”, la Clase 2 fue “hacerlo mejor”.

---

## 2. Mapa del proyecto (pensar por capas)

Un proyecto Django básico se entiende mejor si lo lees por capas.

### A. Capa de configuración global (`config/`)

Aquí viven las reglas del proyecto completo.

- `settings.py`: configuración global (apps, base de datos, templates, idioma, seguridad, etc.)
- `urls.py`: enrutador principal del sitio
- `wsgi.py` / `asgi.py`: puntos de entrada del servidor

### B. Capa de aplicación (`productos/`)

Aquí vive la funcionalidad del negocio (nuestro catálogo).

- `models.py`: datos + lógica de negocio
- `views.py`: coordinación de solicitudes y respuestas
- `urls.py`: rutas específicas de la app
- `forms.py`: validación de formularios (si la app los usa)

### C. Capa de presentación (`templates/` y templates de app)

Aquí vive lo que ve el usuario.

- `templates/base.html`: estructura compartida (navbar, layout)
- templates hijos: catálogo, búsqueda, carrito, home, etc.

### Regla de oro de lectura

Cuando no entiendas un proyecto Django, pregúntate:

1. ¿Qué URL se pidió?
2. ¿Qué vista responde?
3. ¿Qué modelo consulta?
4. ¿Qué template renderiza?

---

## 3. El viaje de una petición (flujo MVT real)

El patrón MVT se entiende de verdad cuando sigues una petición real de principio a fin.

### Flujo general

```text
Navegador
   │
   ├── pide una URL (ej: /productos/)
   ▼
config/urls.py
   │
   ├── delega a productos/urls.py
   ▼
views.py
   │
   ├── consulta models.py (ORM)
   ├── prepara contexto
   └── llama a un template
   ▼
template.html
   │
   └── Django genera HTML
   ▼
Navegador (respuesta final)
```

### Ejemplo 1 — Catálogo (`/productos/`)

- El navegador pide `/productos/`
- Django revisa `config/urls.py`
- Se delega a `productos/urls.py`
- Se ejecuta `lista_productos`
- La vista consulta `Producto.objects...`
- Se renderiza `lista_productos.html`
- El usuario ve la lista

### Ejemplo 2 — Búsqueda (`/productos/buscar/?q=...`)

- El navegador envía un `GET` con un parámetro (`q`)
- La vista lee `request.GET`
- Filtra productos con el ORM
- Envía resultados al template `buscar.html`

### Ejemplo 3 — Carrito (sesión)

- El usuario hace clic en “Agregar al carrito”
- La vista modifica `request.session`
- Luego hace `redirect(...)`
- Otra vista (`ver_carrito`) lee esa sesión y muestra el contenido

> Observa que el carrito simple usa sesión: no necesitamos un modelo de carrito todavía.

---

## 4. Decisiones de Clase 2 que importan a nivel de programador

### 4.1 `config/` como organización profesional

Renombrar la carpeta de configuración a `config/` ayuda a separar:

- configuración global del proyecto,
- lógica de negocio de las apps.

No cambia “qué puede hacer Django”, pero sí mejora cómo se lee y mantiene el proyecto.

### 4.2 Fat Models, Thin Views

Idea clave:

- **Modelo**: sabe cosas del negocio (ej: `precio_final()`, `ahorro_monto()`)
- **Vista**: coordina la solicitud (recibe request, consulta, renderiza o redirige)

Esto reduce duplicación y mejora el mantenimiento.

### 4.3 Forms de Django

Un `Form` no es solo HTML.

También aporta:

- validación del lado del servidor,
- limpieza de datos,
- mensajes de error,
- estructura clara del formulario.

> Regla de seguridad: nunca confiar solo en validaciones del navegador.

### 4.4 Sesiones (`request.session`)

Las sesiones permiten guardar estado del usuario entre solicitudes.

En nuestro proyecto didáctico se usan para:

- guardar IDs de productos en carrito,
- mostrar el carrito después,
- mantener datos mientras el usuario navega.

### 4.5 Herencia de templates (`base.html`)

Con `base.html` evitamos repetir:

- `<head>`
- navbar
- estructura principal

Cada template hijo solo define lo específico.

Eso aplica el principio **DRY** (No te repitas).

### 4.6 `GET` vs `POST` (visión conceptual)

- `GET`: buscar, navegar, consultar
- `POST`: enviar datos o ejecutar acciones que modifican estado

En cursos iniciales a veces se simplifican acciones con links para enfocarse en el flujo. Lo importante por ahora es **entender la diferencia conceptual**.

---

## 5. Cómo leer código Django sin perderte

Cuando abras un archivo y no entiendas qué hace, usa este orden:

### Paso 1 — Buscar la ruta

Identifica el `name=` y la URL asociada en `urls.py`.

### Paso 2 — Leer la vista completa

En la vista, identifica:

- entradas (`request`, parámetros de URL)
- consultas al modelo
- si hace `render()` o `redirect()`
- qué template usa
- qué contexto envía

### Paso 3 — Revisar el template

Busca:

- variables (`{{ ... }}`)
- condicionales (`{% if %}`)
- loops (`{% for %}`)
- rutas (`{% url '...' %}`)

### Paso 4 — Volver al modelo (si hay lógica)

Si ves algo como `p.precio_final`, revisa `models.py` para entender la lógica real.

> Este hábito te ayuda a pensar como programador/a, no solo a copiar código.

---

## 6. Preguntas para pensar y discutir en clase

Este bloque **no es una prueba para atraparte**.

Es un entrenamiento para aprender a pensar como programador/a Django:

- mirar el código antes de responder,
- explicar con tus palabras,
- justificar usando el flujo MVT,
- y detectar en qué parte del proyecto está el problema.

### Cómo trabajar estas preguntas (método simple)

Antes de responder una pregunta, haz esto:

1. Identifica de qué capa habla (URL, vista, modelo, template, settings, sesión).
2. Piensa qué archivo tocarías si tuvieras que corregirlo.
3. Responde en una frase simple.
4. Si puedes, agrega un “porque...”.

> No importa usar palabras perfectas. Importa que entiendas el flujo.

### Recomendación de trabajo en clase

- Primero responde individualmente las preguntas más fáciles.
- Luego compáralas en pareja o grupo.
- Después revisen el código real del proyecto y ajusten respuestas.

### Nivel 1 — Ubicarte en el proyecto (más directas)

Estas preguntas te ayudan a reconocer responsabilidades y flujo básico.

#### A. Lectura de código (P1–P8)

**P1.** ¿Qué archivo recibe primero una petición HTTP en Django: `models.py`, `views.py` o `urls.py`?

**P2.** En una vista, ¿qué diferencia práctica hay entre `render()` y `redirect()`?

**P3.** Si una vista hace `return render(request, 'buscar.html', {'resultados': resultados})`, ¿qué significa ese diccionario?

**P4.** ¿Por qué conviene que `precio_final()` esté en `models.py` y no escrito directamente en el template?

**P5.** ¿Qué problema resuelve `{% extends "base.html" %}`?

**P6.** ¿Qué ventaja tiene usar `{% url 'lista_productos' %}` en vez de escribir `/productos/` manualmente?

**P7.** ¿Qué hace `request.GET.get('q', '')` en una vista de búsqueda?

**P8.** ¿Qué rol cumple `request.session` en el carrito de compras didáctico?

### Nivel 2 — Entender decisiones de diseño (intermedio)

Aquí ya no solo importa “qué archivo”, sino **por qué** esa decisión es mejor.

#### B. Arquitectura y responsabilidades (P9–P15)

**P9.** ¿Qué tipo de cosas deberían configurarse en `settings.py`?

**P10.** Si quieres crear una página “Acerca de”, ¿en qué app la pondrías y por qué?

**P11.** ¿Qué responsabilidad tiene `productos/urls.py` y qué cosa NO debería hacer?

**P12.** ¿Qué significa “Fat Models, Thin Views” en una frase?

**P13.** Si una vista empieza a tener muchos cálculos de negocio, ¿qué señal arquitectónica te está mostrando?

**P14.** ¿Por qué un `Form` de Django es mejor que confiar solo en `<input>` HTML para validar datos?

**P15.** ¿Qué ventaja aporta una carpeta global `templates/` para `base.html`?

### Nivel 3 — Diagnóstico (debugging básico)

Aquí la idea es pensar como alguien que depura:

- ¿qué error veo?
- ¿qué significa?
- ¿dónde reviso primero?

#### C. Debugging y diagnóstico (P16–P24)

**P16.** Si aparece `TemplateDoesNotExist`, menciona al menos 2 cosas que revisarías primero.

**P17.** Si aparece `NoReverseMatch`, ¿qué relación tiene ese error con `{% url %}` o `redirect()`?

**P18.** Si modificas un modelo y luego aparece un error de base de datos, ¿qué comandos de Django recordarías revisar/ejecutar?

**P19.** ¿Qué pasa si creas una app con `startapp` pero no la agregas a `INSTALLED_APPS`?

**P20.** Si en un template una variable no se muestra, ¿qué revisarías en la vista?

**P21.** ¿Por qué conviene probar una URL directamente en el navegador cuando estás depurando?

**P22.** ¿Qué ventaja tiene `get_object_or_404(...)` frente a un `.get(...)` simple en vistas básicas?

**P23.** ¿Qué diferencia hay entre un error de ruta (URL) y un error de template a nivel de “dónde buscar” el problema?

**P24.** Si el carrito no muestra lo esperado, ¿qué archivos revisarías primero: modelo, vista, template, urls o sesión? Justifica.

### Nivel 4 — Predicción y criterio (más desafiante)

Estas preguntas te ayudan a anticipar problemas antes de que ocurran.

#### D. Predicción y pensamiento de programador (P25–P30)

**P25.** Si cambias el nombre de una ruta en `urls.py` pero no actualizas el template, ¿qué error podrías esperar?

**P26.** Si cambias `base.html`, ¿qué páginas deberían verse afectadas y por qué?

**P27.** ¿Qué parte del sistema decide qué datos llegan al template?

**P28.** ¿Qué parte del sistema decide cómo se ven esos datos en pantalla?

**P29.** ¿Qué aprendizaje de Clase 2 te parece más importante para mantener un proyecto cuando crece?

**P30.** Explica en 4 pasos el flujo completo de una funcionalidad de Django usando un ejemplo del proyecto.

### Cómo saber si vas bien

Vas muy bien si puedes hacer estas tres cosas:

- explicar qué hace una vista sin leerla línea por línea,
- decir en qué archivo buscarías un error antes de tocar nada,
- y conectar URL -> vista -> modelo -> template con un ejemplo real.

---

## 7. Errores comunes (guía rápida)

| Error | Qué suele significar | Qué revisar primero |
| --- | --- | --- |
| `TemplateDoesNotExist` | Django no encuentra el template | nombre del archivo, ruta, carpeta `templates`, `TEMPLATES['DIRS']` |
| `NoReverseMatch` | Django no puede construir una URL por nombre | `name=` en `urls.py`, parámetros requeridos, `{% url %}` |
| `AttributeError` | Se intenta usar algo que no existe | nombre del atributo/campo/método en modelo o vista |
| `OperationalError` | Problema con la base de datos (a menudo migraciones) | cambios en `models.py`, `makemigrations`, `migrate` |
| `ImportError` | Import mal escrito o circular | rutas de import en `views.py`/`urls.py` |

---

## 8. Siguiente paso: práctica de consolidación

Vamos a completar el proyecto con una funcionalidad nueva, todavía dentro del nivel básico:

### Práctica final (consolidación)

- crear una **vista de detalle de producto**,
- usar una **URL dinámica** (`<int:producto_id>`),
- crear un **template nuevo** que herede de `base.html`,
- conectar navegación desde catálogo, búsqueda y carrito.

Con esto vas a recorrer otra vez el flujo completo de Django, pero ahora con más criterio.

> Meta de esta clase: que puedas leer, explicar y ampliar un proyecto Django básico sin perderte.
