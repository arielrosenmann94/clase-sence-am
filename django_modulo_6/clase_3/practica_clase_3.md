# 🛠️ Django — Módulo 6 · Guía Práctica (Clase 3)

### Consolidación del flujo MVT con una funcionalidad nueva

> En esta clase no vamos a agregar un tema avanzado. Vamos a **consolidar** lo aprendido en Clase 1 y 2 completando una funcionalidad nueva en el proyecto didáctico: la **ficha (detalle) de producto**.

---

## Qué vas a construir

Al terminar esta práctica, vas a poder:

- crear una URL dinámica en Django,
- escribir una vista que reciba parámetros,
- consultar un objeto específico con `get_object_or_404`,
- crear un template nuevo que herede de `base.html`,
- conectar navegación entre catálogo, búsqueda y carrito.

---

## Resultado esperado (flujo final)

Debe quedar funcionando este flujo:

1. Entrar al catálogo (`/productos/`)
2. Hacer clic en **Ver detalle** de un producto
3. Ver la ficha del producto en `/productos/<id>/`
4. Agregar al carrito desde la ficha
5. Volver al catálogo
6. Desde búsqueda, entrar también al detalle
7. Desde carrito, volver a seguir comprando

---

## Antes de empezar

Asegúrate de que tu proyecto heredado de Clase 1 y 2 esté funcionando:

- `python manage.py runserver`
- abre el catálogo
- prueba la búsqueda desde la navbar
- prueba entrar al carrito

> Si algo de eso no funciona, corrígelo antes de empezar. Esta práctica se apoya en lo ya construido.

---

## Paso 1 — Crear la vista de detalle en `productos/views.py`

Abre `productos/views.py`.

### 1.1 Asegura el import

Si no lo tienes, ajusta el import de `django.shortcuts` para incluir `get_object_or_404`:

```python
from django.shortcuts import render, redirect, get_object_or_404
```

### Lectura línea por línea (import)

- `from django.shortcuts ...`: importa funciones de ayuda que Django trae listas para usar en vistas.
- `render`: crea una respuesta HTML usando un template.
- `redirect`: redirige a otra URL (ya la venías usando en el carrito).
- `get_object_or_404`: busca un objeto y, si no existe, responde con error 404 en vez de romper la app.

### 1.2 Agrega la vista

```python
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    return render(request, 'detalle_producto.html', {
        'producto': producto,
    })
```

### Lectura línea por línea (vista)

- `def detalle_producto(request, producto_id):`
  - defines una nueva vista.
  - `request` es la solicitud HTTP.
  - `producto_id` llega desde la URL (lo capturaremos en `urls.py`).
- `producto = get_object_or_404(Producto, id=producto_id)`
  - busca un registro del modelo `Producto`.
  - `id=producto_id` significa: “tráeme el producto cuyo id sea el que vino en la ruta”.
  - si no existe, Django devuelve 404 automáticamente.
- `return render(request, 'detalle_producto.html', {...})`
  - le dice a Django que renderice un template HTML.
  - `'detalle_producto.html'` es el archivo que vamos a crear en el siguiente paso.
  - el diccionario es el **contexto** (los datos que el template puede usar).
- `'producto': producto`
  - en el template, la variable se llamará `producto`.
  - su valor es el objeto que acabamos de buscar.

### Qué estás practicando aquí

- Parámetros desde la URL (`producto_id`)
- Consulta de un solo objeto
- Uso de `render()` con contexto
- Manejo de 404 cuando el ID no existe

---

## Paso 2 — Registrar la URL dinámica en `productos/urls.py`

Abre `productos/urls.py` y agrega la nueva ruta.

### 2.1 Importa la vista de detalle

Si importas funciones una por una, agrega `detalle_producto`.

Ejemplo:

```python
from .views import lista_productos, buscar_producto, agregar_al_carrito, ver_carrito, detalle_producto
```

### Lectura línea por línea (import de vista)

- `from .views import ...`
  - importa funciones desde `views.py` de la misma app (`.` significa “esta app”).
- `detalle_producto`
  - agregamos esta nueva vista para poder usarla en `urlpatterns`.
- si olvidas importarla:
  - Django no podrá usarla en la ruta y dará error de nombre/import.

### 2.2 Agrega la ruta

```python
path('<int:producto_id>/', detalle_producto, name='detalle_producto'),
```

### Lectura línea por línea (ruta dinámica)

- `path(...)`: registra una ruta en Django.
- `'<int:producto_id>/'`
  - es una ruta dinámica.
  - `<int:...>` obliga a que el valor sea un número entero.
  - `producto_id` es el nombre del parámetro que Django enviará a la vista.
- `detalle_producto`
  - es la función vista que se ejecuta cuando la URL coincide.
- `name='detalle_producto'`
  - nombre interno de la ruta.
  - se usa en templates con `{% url 'detalle_producto' ... %}`.

### Ejemplo de estructura (referencia)

```python
from django.urls import path
from .views import (
    lista_productos,
    buscar_producto,
    agregar_al_carrito,
    ver_carrito,
    detalle_producto,
)

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('buscar/', buscar_producto, name='buscar_producto'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('<int:producto_id>/', detalle_producto, name='detalle_producto'),
]
```

### Cómo leer este bloque completo (sin memorizarlo)

- `from django.urls import path`: habilita la función `path()` para declarar rutas.
- `from .views import (...)`: trae las vistas que el enrutador va a usar.
- `urlpatterns = [...]`: lista de rutas de la app.
- cada `path(...)` tiene siempre la misma idea:
  - **ruta**
  - **vista**
  - **nombre**

> Si te pierdes, recuerda esta fórmula: `path('ruta/', vista, name='nombre')`.

> Nota: Django evalúa rutas en orden. Mantén las rutas específicas claras y revisa que no haya conflictos.

---

## Paso 3 — Crear el template `productos/templates/detalle_producto.html`

Crea este archivo nuevo:

- `productos/templates/detalle_producto.html`

Pega este contenido:

```html
{% extends "base.html" %}

{% block title %}{{ producto.nombre }}{% endblock %}

{% block content %}
<h1>{{ producto.nombre }}</h1>

<p><strong>Descripción:</strong></p>
<p>
  {% if producto.descripcion %}
    {{ producto.descripcion }}
  {% else %}
    Este producto no tiene descripción cargada.
  {% endif %}
</p>

<p><strong>Precio normal:</strong> ${{ producto.precio }}</p>

{% if producto.descuento > 0 %}
  <p><strong>Descuento:</strong> {{ producto.descuento }}%</p>
  <p><strong>Precio final:</strong> ${{ producto.precio_final }}</p>
  <p style="color: green;"><strong>Ahorro:</strong> ${{ producto.ahorro_monto }}</p>
{% else %}
  <p><strong>Precio final:</strong> ${{ producto.precio }}</p>
{% endif %}

<p>
  {% if producto.disponible %}
    <span style="color: green;">Disponible</span>
  {% else %}
    <span style="color: red;">No disponible</span>
  {% endif %}
</p>

<div style="margin-top: 20px; display: flex; gap: 12px; flex-wrap: wrap;">
  <a href="{% url 'lista_productos' %}">← Volver al catálogo</a>
  <a href="{% url 'agregar_al_carrito' producto.id %}">🛒 Agregar al carrito</a>
  <a href="{% url 'ver_carrito' %}">Ver carrito</a>
</div>
{% endblock %}
```

### Lectura línea por línea (template de detalle)

- `{% extends "base.html" %}`
  - este template hereda la estructura general (navbar, layout, etc.).
  - evita repetir HTML completo.
- `{% block title %}{{ producto.nombre }}{% endblock %}`
  - define el título de la pestaña/página.
  - usa el nombre del producto que envió la vista.
- `{% block content %}`
  - empieza el contenido específico de esta página.
- `<h1>{{ producto.nombre }}</h1>`
  - muestra el nombre del producto.
- `{{ ... }}`
  - imprime valores que vienen del contexto.
- `{% if producto.descripcion %} ... {% else %} ... {% endif %}`
  - si hay descripción, la muestra.
  - si no hay descripción, muestra un texto alternativo.
- `{{ producto.precio }}`
  - muestra el precio original.
- `{% if producto.descuento > 0 %}`
  - si el producto tiene descuento, muestra bloque de oferta.
- `{{ producto.precio_final }}`
  - llama al método del modelo `precio_final()` (en templates se usa sin paréntesis).
- `{{ producto.ahorro_monto }}`
  - muestra cuánto ahorro calcula el modelo.
- `{% if producto.disponible %}`
  - muestra estado visual de disponibilidad.
- `<a href="{% url 'lista_productos' %}">...`
  - crea un link usando el nombre de la ruta, no una URL escrita a mano.
- `<a href="{% url 'agregar_al_carrito' producto.id %}">...`
  - crea un link a una ruta que necesita parámetro (`producto.id`).
- `{% endblock %}`
  - cierra el bloque `content`.

> Importante: en templates Django, los métodos simples del modelo se usan como `{{ producto.precio_final }}` (sin `()`).

### Qué estás practicando aquí

- Herencia de templates (`base.html`)
- Variables de contexto (`producto`)
- Condicionales en DTL (`{% if %}`)
- Reutilización de lógica de negocio del modelo (`precio_final`, `ahorro_monto`)

---

## Paso 4 — Agregar enlace “Ver detalle” en el catálogo

Abre `productos/templates/lista_productos.html`.

Dentro del loop `{% for p in productos %}`, agrega un enlace al detalle del producto.

### Opción mínima

```html
<a href="{% url 'detalle_producto' p.id %}">🔎 Ver detalle</a>
```

### Lectura línea por línea (link desde catálogo)

- `<a href="...">`: crea un enlace HTML.
- `{% url 'detalle_producto' p.id %}`
  - Django construye la URL usando el nombre de ruta.
  - `p.id` es el parámetro que esa ruta necesita.
- `🔎 Ver detalle`
  - texto visible del link.

### Opción combinada (si quieres dejar ambos links juntos)

```html
<a href="{% url 'detalle_producto' p.id %}">🔎 Ver detalle</a>
<a href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar al carrito</a>
```

> Si ya tienes el botón de carrito, no lo borres: solo agrega el de detalle.

---

## Paso 5 — Mini mejora: enlazar al detalle desde la búsqueda

Abre `productos/templates/buscar.html`.

Dentro del loop de resultados, agrega el enlace al detalle.

### Ejemplo de cómo debería verse cada resultado

```html
<li>
  <strong>{{ p.nombre }}</strong> —
  <span class="precio">${{ p.precio_final }}</span>
  <a href="{% url 'detalle_producto' p.id %}">🔎 Ver detalle</a>
  <a class="btn" href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar</a>
</li>
```

### Lectura línea por línea (resultado de búsqueda)

- `<li> ... </li>`: un resultado de la lista.
- `{{ p.nombre }}`: nombre del producto encontrado.
- `{{ p.precio_final }}`
  - reutiliza la lógica del modelo.
  - muestra precio con descuento si corresponde.
- link `detalle_producto`
  - permite navegar a la ficha del producto.
- link `agregar_al_carrito`
  - mantiene la acción principal desde la búsqueda.

> Observa que repetimos un patrón: mostrar datos + link de detalle + link de acción.

### Qué estás practicando aquí

- Reuso de rutas con parámetros
- Consistencia de navegación entre páginas
- Lectura del mismo patrón en más de un template

---

## Paso 6 — Mini mejora: “Seguir comprando” en el carrito

Abre `productos/templates/carrito.html`.

Agrega un enlace al catálogo para facilitar el regreso.

### Si el carrito tiene productos (ejemplo)

Debajo del total o al final del contenido:

```html
<p><a href="{% url 'lista_productos' %}">← Seguir comprando</a></p>
```

### Lectura línea por línea (volver al catálogo)

- `<p> ... </p>`: envuelve el enlace en un párrafo para separarlo visualmente.
- `{% url 'lista_productos' %}`
  - construye la URL del catálogo por nombre.
  - si mañana cambias la ruta real, este link seguirá funcionando si mantienes el `name`.

### Si el carrito está vacío

Si ya tienes un botón “Ir al catálogo”, puedes dejarlo igual. Si no, agrega:

```html
<a class="btn" href="{% url 'lista_productos' %}">Ir al catálogo →</a>
```

### Lectura línea por línea (carrito vacío)

- `class="btn"`: reutiliza el estilo de botón que ya tengas en el proyecto.
- `href="{% url 'lista_productos' %}"`: lleva al catálogo.
- texto del botón: guía al usuario cuando el carrito está vacío.

---

## Paso 7 — Prueba y verificación (checklist)

Ejecuta el servidor y comprueba uno por uno:

```bash
python manage.py runserver
```

### Checklist funcional

- [ ] `/productos/` carga correctamente
- [ ] Cada producto muestra “Ver detalle”
- [ ] Al hacer clic, se abre `/productos/<id>/`
- [ ] El detalle muestra nombre, descripción y precios
- [ ] Si hay descuento, se ve `precio_final` y ahorro
- [ ] El detalle permite agregar al carrito
- [ ] Desde búsqueda también puedo entrar al detalle
- [ ] El carrito tiene opción de volver al catálogo

### Prueba importante (debugging)

Prueba manualmente un ID inexistente, por ejemplo:

- `/productos/999999/`

Debes ver una respuesta **404**. Eso confirma que `get_object_or_404(...)` está funcionando.

---

## Paso 8 — Preguntas de reflexión (después de programar)

Responde con tus palabras:

1. ¿Dónde se captura `producto_id`: en la vista o en la URL?
2. ¿Qué archivo decide que `/productos/5/` llama a `detalle_producto`?
3. ¿Qué archivo consulta la base de datos?
4. ¿Qué archivo decide cómo se ve la ficha en pantalla?
5. ¿Por qué esta funcionalidad refuerza el flujo MVT completo?

---

## Cierre de práctica (qué debe quedar funcionando)

Tu proyecto debe mostrar:

- catálogo con enlace a detalle,
- detalle de producto funcionando,
- navegación desde búsqueda hacia detalle,
- navegación desde carrito hacia catálogo,
- uso de `base.html` (herencia) en el nuevo template.

> Si completaste esta práctica, ya estás ampliando un proyecto Django básico con criterio de programador/a.
