# 🐍 Django — Módulo 6 · Clase 6

## El toolkit completo de Django Templates

---

> _"Conocer las herramientas es el primer paso. Saber cuándo y por qué usarlas es el segundo."_

---

## De dónde venimos

Ya configuramos el proyecto, los archivos estáticos, Bootstrap y la herencia básica. Hoy cerramos el panorama completo del **Django Template Language** — cómo se organiza, qué hace cada pieza, y cuáles son las reglas que no se rompen.

---

---

# Parte I — El flujo MTV: quién hace qué

---

En Django, cada solicitud pasa por tres capas. La responsabilidad de cada una es estricta:

| Capa         | Qué hace                                                  | Qué NO hace                   |
| ------------ | --------------------------------------------------------- | ----------------------------- |
| **Model**    | Gestiona datos y lógica de negocio                        | No genera HTML                |
| **View**     | Coordina: pide datos, arma el contexto, llama al template | No muestra nada               |
| **Template** | Presenta los datos al usuario                             | No hace consultas ni cálculos |

---

## El contexto: el paquete que viaja de la vista al template

La vista arma un diccionario y se lo pasa al template:

```python
# views.py
def lista_productos(request):
    contexto = {
        'titulo':    'Nuestros Productos',
        'productos': ['Mouse', 'Teclado', 'Monitor'],
        'total':     3,
    }
    return render(request, 'productos.html', contexto)
```

Cada clave del diccionario se convierte en una variable disponible en el template:

```html
<h1>{{ titulo }}</h1>
<p>Hay {{ total }} productos disponibles.</p>
```

Regla fundamental: **la vista calcula, el template muestra**. Si necesitás filtrar una lista, lo haces en la vista antes de pasarla. El template solo itera sobre lo que ya está listo.

---

## Acceso a datos anidados

El punto `.` navega cualquier estructura:

```html
{{ usuario.nombre }} → clave de diccionario o atributo de objeto {{
carrito.0.precio }} → primer elemento de la lista, luego su clave {{
empresa.get_nombre }} → método sin argumentos (sin paréntesis)
```

Django prueba en orden: clave de diccionario → atributo → método → índice de lista.

---

---

# Parte II — Las tres construcciones del DTL

---

Todo código en un template es una de estas tres cosas:

| Construcción | Sintaxis          | Propósito                                                         |
| ------------ | ----------------- | ----------------------------------------------------------------- |
| **Variable** | `{{ x }}`         | Mostrar el valor de una variable                                  |
| **Etiqueta** | `{% etiqueta %}`  | Control: `if`, `for`, `url`, `block`, `extends`, `load`, `static` |
| **Filtro**   | `{{ x\|filtro }}` | Transformar el valor antes de mostrarlo                           |

No se mezclan en el mismo par de llaves.

---

## Filtros — referencia rápida

| Filtro            | Qué hace                        | Ejemplo                            |
| ----------------- | ------------------------------- | ---------------------------------- |
| `length`          | Cuenta elementos                | `{{ lista\|length }}` → `3`        |
| `default`         | Valor de respaldo si está vacío | `{{ campo\|default:"Sin datos" }}` |
| `upper` / `lower` | Cambia capitalización           | `{{ nombre\|upper }}` → `ANA`      |
| `capfirst`        | Primera letra en mayúscula      | `{{ texto\|capfirst }}`            |
| `truncatewords:N` | Corta a N palabras con `...`    | `{{ desc\|truncatewords:10 }}`     |
| `date:"formato"`  | Formatea una fecha              | `{{ fecha\|date:"d/m/Y" }}`        |
| `floatformat:N`   | Fija N decimales                | `{{ precio\|floatformat:2 }}`      |
| `linebreaks`      | Saltos de línea → `<br>`        | `{{ comentario\|linebreaks }}`     |

Se pueden encadenar: `{{ texto|truncatewords:15|upper }}`

---

---

# Parte III — Etiquetas de control

---

## `{% if %}` — condicional

```html
{% if stock > 0 %}
<span class="badge bg-success">Disponible</span>
{% elif stock == 0 %}
<span class="badge bg-warning">Sin stock</span>
{% else %}
<span class="badge bg-secondary">Sin información</span>
{% endif %}
```

### Operadores disponibles

| Operador               | Ejemplo                                                    |
| ---------------------- | ---------------------------------------------------------- |
| Igualdad / desigualdad | `{% if rol == "admin" %}` · `{% if estado != "activo" %}`  |
| Comparación            | `{% if stock > 0 %}` · `{% if precio <= 5000 %}`           |
| Pertenencia            | `{% if "Editor" in roles %}`                               |
| Lógica                 | `{% if user and user.is_active %}`                         |
| Verdad / vacío         | `{% if productos %}` — lista no vacía evaluada como `True` |

> 💡 Lista vacía `[]`, `None`, `0` y `""` evalúan como `False`. Misma lógica que Python.

---

## `{% for %}` — iteración

```html
<ul>
  {% for producto in productos %}
  <li>{{ producto.nombre }} — ${{ producto.precio|floatformat:0 }}</li>
  {% empty %}
  <li>No hay productos disponibles.</li>
  {% endfor %}
</ul>
```

`{% empty %}` se ejecuta cuando la lista está vacía. Siempre incluirla.

### Variable `forloop`

Disponible automáticamente dentro de cada `{% for %}`:

| Variable             | Valor                              |
| -------------------- | ---------------------------------- |
| `forloop.counter`    | Iteración actual, empieza en **1** |
| `forloop.counter0`   | Iteración actual, empieza en **0** |
| `forloop.first`      | `True` solo en la primera vuelta   |
| `forloop.last`       | `True` solo en la última vuelta    |
| `forloop.revcounter` | Cuenta regresiva, termina en 1     |

```html
<table class="table">
  {% for item in lista %}
  <tr class="{% if forloop.first %}table-primary{% endif %}">
    <td>{{ forloop.counter }}</td>
    <td>{{ item.nombre }}</td>
    <td>{% if forloop.last %}← último{% endif %}</td>
  </tr>
  {% endfor %}
</table>
```

---

---

# Parte IV — Archivos estáticos y Bootstrap

---

## Configuración en `settings.py`

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']   # archivos en desarrollo
STATIC_ROOT = BASE_DIR / 'staticfiles'     # destino de collectstatic
```

Estructura de carpetas recomendada:

```
static/
├── css/
│   └── estilos.css
├── js/
│   └── app.js
└── images/
    └── logo.png
```

## Uso en el template

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/estilos.css' %}" />
<img src="{% static 'images/logo.png' %}" alt="Logo" />
<script src="{% static 'js/app.js' %}"></script>
```

> ⚠️ `{% load static %}` va al inicio del template, o justo después de `{% extends %}` si lo hay. Sin esta línea, la etiqueta `{% static %}` no existe y el template falla con error.

---

## Bootstrap — CDN

```html
<!-- En el <head> -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
/>

<!-- Antes del </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

|                                 | CDN       | Archivo local     |
| ------------------------------- | --------- | ----------------- |
| Setup                           | Inmediato | Requiere descarga |
| Sin internet                    | ❌        | ✅                |
| Compartido en caché del browser | ✅        | No                |
| Uso en clase / prototipo        | ✅ Ideal  | No necesario      |

---

---

# Parte V — Herencia de templates

---

## La idea central

`base.html` tiene lo que **todas las páginas comparten**: navbar, footer, Bootstrap, CSS propio. Usa `{% block %}` para marcar los lugares que cada página puede personalizar. Los templates hijos extienden la base y solo definen esos bloques.

---

## `base.html` — estructura mínima funcional

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Mi Sitio{% endblock %}</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    />
    <link rel="stylesheet" href="{% static 'css/estilos.css' %}" />
    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <nav class="navbar navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="{% url 'inicio' %}">Mi Sitio</a>
        <div class="navbar-nav ms-auto">
          <a class="nav-link" href="{% url 'inicio' %}">Inicio</a>
          <a class="nav-link" href="{% url 'productos' %}">Productos</a>
        </div>
      </div>
    </nav>

    <main class="container mt-4">{% block content %}{% endblock %}</main>

    <footer class="bg-dark text-white text-center py-3 mt-5">
      <p>&copy; 2025 Mi Sitio</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
  </body>
</html>
```

## Template hijo — solo lo que cambia

```html
{% extends "base.html" %} {% block title %}Listado de Productos{% endblock %} {%
block content %}
<h1>Productos</h1>
{% for p in productos %}
<p>{{ p }}</p>
{% empty %}
<p class="text-muted">No hay productos disponibles.</p>
{% endfor %} {% endblock %}
```

## Bloques más usados

| Bloque                  | Propósito                          |
| ----------------------- | ---------------------------------- |
| `{% block title %}`     | Título de la pestaña del navegador |
| `{% block content %}`   | Contenido principal de la página   |
| `{% block extra_css %}` | CSS adicional solo para esa página |
| `{% block extra_js %}`  | JS adicional solo para esa página  |

Un bloque con valor en la base actúa como **default**: si el hijo no lo sobreescribe, se usa el de la base.

## `{{ block.super }}` — agregar sin reemplazar

```html
{% block extra_css %} {{ block.super }}
<link rel="stylesheet" href="{% static 'css/detalle.css' %}" />
{% endblock %}
```

Incluye lo que el padre tenía, y agrega el contenido propio después.

---

---

# Parte VI — `{% url %}` y navegación

---

## El problema del link hardcodeado

```html
<!-- ❌ Si la URL cambia en urls.py, esto se rompe en silencio -->
<a href="/productos/">Catálogo</a>

<!-- ✅ Django genera la URL correcta según urls.py -->
<a href="{% url 'productos' %}">Catálogo</a>
```

---

## Cómo funciona

```python
# urls.py

urlpatterns = [
    path('productos/',           views.lista,   name='productos'),
    path('productos/<int:pk>/', views.detalle,  name='producto-detalle'),
]
```

```html
<a href="{% url 'productos' %}">Ver todos</a>

{% for p in productos %}
<a href="{% url 'producto-detalle' pk=p.id %}">{{ p.nombre }}</a>
{% endfor %}
```

## Namespaces — cuando hay varias apps

```python
# tienda/urls.py
app_name = 'tienda'

urlpatterns = [
    path('',          views.lista,   name='lista'),
    path('<int:pk>/', views.detalle, name='detalle'),
]
```

```html
<a href="{% url 'tienda:lista' %}">Ver tienda</a>
<a href="{% url 'tienda:detalle' pk=p.id %}">Ver producto</a>
```

Sin namespaces, si dos apps tienen una URL llamada `lista`, Django no sabe a cuál apuntar.

---

---

# Parte VII — Manejo de errores

---

## `try/except` en la vista

```python
def calcular(request):
    try:
        resultado = 10 / 0
    except ZeroDivisionError:
        resultado = "No es posible dividir por cero."
    return render(request, 'resultado.html', {'resultado': resultado})
```

## `get_object_or_404` — el shortcut que siempre se usa

```python
from django.shortcuts import get_object_or_404

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})
```

`objects.get()` lanza excepción si no existe → la app explota.
`get_object_or_404()` devuelve una respuesta 404 limpia → siempre preferirlo.

---

## Páginas de error personalizadas

```python
# urls.py principal
handler404 = 'mi_app.views.error_404'
handler500 = 'mi_app.views.error_500'
```

```python
# views.py
def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
```

```html
<!-- templates/404.html -->
{% extends "base.html" %} {% block title %}Página no encontrada{% endblock %} {%
block content %}
<div class="text-center py-5">
  <h1 class="display-1 text-muted">404</h1>
  <p class="lead">La página que buscás no existe.</p>
  <a href="{% url 'inicio' %}" class="btn btn-primary">Volver al inicio</a>
</div>
{% endblock %}
```

> ⚠️ Las páginas personalizadas solo funcionan con `DEBUG = False`. En desarrollo siempre aparece el traceback completo.

### Códigos HTTP más comunes

| Código | Nombre                | Causa                 |
| ------ | --------------------- | --------------------- |
| 400    | Bad Request           | Solicitud mal formada |
| 403    | Forbidden             | Sin permisos          |
| 404    | Not Found             | El recurso no existe  |
| 500    | Internal Server Error | Error del servidor    |

---

---

# Referencia rápida — Todo el DTL

---

| Herramienta         | Sintaxis                                            | Notas                                          |
| ------------------- | --------------------------------------------------- | ---------------------------------------------- |
| Variable            | `{{ x }}`                                           |                                                |
| Variable anidada    | `{{ x.y.z }}`                                       | Punto navega dict, atributos, métodos, índices |
| Filtro              | `{{ x\|filtro }}`                                   |                                                |
| Filtros encadenados | `{{ x\|f1\|f2 }}`                                   |                                                |
| Condicional         | `{% if %} … {% elif %} … {% else %} … {% endif %}`  |                                                |
| Iteración           | `{% for x in lista %} … {% empty %} … {% endfor %}` |                                                |
| Extensión           | `{% extends "base.html" %}`                         | Primera línea del template hijo                |
| Bloque              | `{% block nombre %} … {% endblock %}`               |                                                |
| Cargar librería     | `{% load static %}`                                 | Antes del primer `{% static %}`                |
| Archivo estático    | `{% static 'ruta/archivo' %}`                       | Requiere `{% load static %}`                   |
| URL dinámica        | `{% url 'nombre' %}`                                |                                                |
| URL con parámetros  | `{% url 'nombre' param=valor %}`                    |                                                |
| URL con namespace   | `{% url 'ns:nombre' %}`                             |                                                |
| Contenido padre     | `{{ block.super }}`                                 | Dentro de un bloque hijo                       |
| Comentario          | `{# texto #}`                                       | No aparece en el HTML generado                 |

---

## El flujo en un vistazo

```
Solicitud HTTP
    → urls.py encuentra la ruta
    → views.py ejecuta la función, arma el contexto
    → render(request, 'template.html', contexto)
        → Django carga el template
        → Si hay {% extends %}, carga la base y fusiona bloques
        → Reemplaza {{ variables }} con valores del contexto
        → Evalúa {% if %}, {% for %}, {% url %}, {% static %}
    → HTML final al navegador
```

---

> _"El DTL no es Python. Es un lenguaje de presentación que hace exactamente lo que necesita y nada más. Su austeridad es su diseño: te obliga a separar lo que se calcula de lo que se muestra."_

---
