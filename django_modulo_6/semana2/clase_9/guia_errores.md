# 🚨 Django — Guía de Errores HTTP

## Páginas de Error Personalizadas

---

> _"Un 500 con el stack trace de Django en producción no es un error — es un currículum para hackers."_

---

## ¿De qué trata esta guía?

Cuando algo sale mal, el servidor responde con un **código de estado HTTP**.
Cada código tiene un significado preciso. Algunos los dispara Django automáticamente,
otros los dispara el código propio, y algunos requieren que el developer cree una página personalizada.

Esta guía cubre:

1. Todos los códigos de error relevantes y qué significan
2. Cuáles vale la pena personalizar y por qué
3. Cómo configurar cada uno en Django

---

## El interruptor: `DEBUG`

Hay un parámetro en `settings.py` que cambia todo el comportamiento de los errores:

| Comportamiento                       | `DEBUG = True` (desarrollo)    | `DEBUG = False` (producción) |
| ------------------------------------ | ------------------------------ | ---------------------------- |
| 404                                  | Página amarilla con las URLs   | Tu `404.html`                |
| 403                                  | Texto plano "403 Forbidden"    | Tu `403.html`                |
| 500                                  | Stack trace completo del error | Tu `500.html`                |
| ¿Las páginas personalizadas se usan? | ❌ No                          | ✅ Sí                        |

**Mientras `DEBUG = True`, Django ignora los templates personalizados.**
Se activan únicamente con `DEBUG = False`.

---

## Carpeta de templates a nivel proyecto

Todos los templates de error van en la raíz de `templates/`:

```
mi_proyecto/
├── templates/
│   ├── base.html
│   ├── 400.html
│   ├── 403.html
│   ├── 404.html
│   └── 500.html
├── mi_app/
└── settings.py
```

Y `settings.py` debe apuntar a esa carpeta:

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # ← sin esto Django no los encuentra
        'APP_DIRS': True,
        ...
    },
]
```

---

---

# Glosario — Términos técnicos que aparecen en esta guía

---

> Si es la primera vez que ves estas palabras, este glosario es el primer lugar para leer.

---

| Término           | Qué es en palabras simples                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Servidor**      | Una computadora (o programa) que recibe requests de los navegadores y responde con páginas, datos o errores                    |
| **Cliente**       | El navegador (Chrome, Firefox, etc.) — el que pide información al servidor                                                     |
| **Request**       | El mensaje que el navegador manda al servidor pidiendo algo ("dame la página /perfil/")                                        |
| **Response**      | La respuesta del servidor al request — puede ser HTML, un error, una redirección                                               |
| **HTTP**          | El protocolo que define cómo se comunican cliente y servidor — el idioma de la web                                             |
| **Nginx**         | Un servidor web muy usado — recibe los requests del navegador y los pasa a Django (o devuelve archivos estáticos directamente) |
| **Gunicorn**      | El programa que corre Django en producción — traduce los requests HTTP de Nginx en requests que Django puede procesar          |
| **Proxy**         | Un intermediario entre el cliente y el servidor — recibe el request, lo pasa a otro lado y devuelve la respuesta               |
| **Proxy inverso** | Como un proxy, pero del lado del servidor — Nginx actúa como proxy inverso frente a Django                                     |
| **Load balancer** | Un proxy especial que distribuye los requests entre varios servidores para no sobrecargar uno solo                             |
| **Stack trace**   | El "rastro de error" que Python muestra cuando el código crashea — lista las líneas de código que llevaron al error            |
| **Debug mode**    | Modo de desarrollo — Django muestra información interna (errores, URLs, etc.) que nunca debe salir a producción                |
| **Producción**    | El entorno real donde corre la app para los usuarios finales — opuesto a desarrollo local                                      |
| **Middleware**    | Una capa de código que Django ejecuta en cada request antes de llegar a la vista (sesiones, CSRF, autenticación, etc.)         |
| **CSRF**          | Cross-Site Request Forgery — un tipo de ataque. Django lo previene con tokens automáticos en los formularios                   |
| **Caché**         | Almacenamiento temporal de respuestas para no recalcularlas cada vez — el navegador guarda páginas para cargarlas más rápido   |
| **Header**        | Metadatos del request o response — información que acompaña al contenido (tipo de contenido, cookies, idioma, etc.)            |
| **Rate limiting** | Límite de requests por período de tiempo — "máximo 5 intentos de login por minuto" para prevenir ataques de fuerza bruta       |
| **Deploy**        | El proceso de subir el código a producción para que los usuarios puedan usarlo                                                 |
| **Handler**       | En Django, una función que "maneja" (procesa) un tipo específico de error — reemplaza el comportamiento por defecto            |

---

---

# Panorama completo — todos los errores HTTP

---

> Antes de saber cuáles personalizar, hay que entender qué existe.
> Los códigos HTTP se agrupan en familias. El número de centenas indica la familia.

---

## Familia 1xx — Informativos

Respuestas provisorias. El servidor dice "recibí el request, sigue enviando".

| Código | Nombre              | Qué significa                                              |
| ------ | ------------------- | ---------------------------------------------------------- |
| `100`  | Continue            | El servidor aceptó los headers, el cliente puede continuar |
| `101`  | Switching Protocols | El servidor acepta cambiar de protocolo (ej: WebSockets)   |

**¿Se personalizan en Django?** ❌ No. Son automáticos y el usuario nunca los ve.
Los gestiona el protocolo HTTP en segundo plano.

---

## Familia 2xx — Éxito

El request fue recibido, entendido y procesado correctamente.

| Código | Nombre     | Qué significa                                                     |
| ------ | ---------- | ----------------------------------------------------------------- |
| `200`  | OK         | Todo bien — la vista devolvió contenido                           |
| `201`  | Created    | El recurso fue creado (común en APIs al hacer POST)               |
| `204`  | No Content | Todo bien, pero no hay contenido que devolver (ej: DELETE en API) |

**¿Se personalizan en Django?** ❌ No como "página de error".
Son respuestas exitosas — el developer las controla desde la propia vista:

```python
from django.http import HttpResponse

def eliminar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return HttpResponse(status=204)   # ← devuelve 204 manualmente
```

El `200` es lo que Django devuelve por defecto con `render()`. No requiere configuración adicional.

---

## Familia 3xx — Redirecciones

El recurso existe, pero está en otro lugar. El servidor le dice al navegador adónde ir.

| Código | Nombre             | Qué significa                                                |
| ------ | ------------------ | ------------------------------------------------------------ |
| `301`  | Moved Permanently  | El recurso se movió para siempre — los buscadores actualizan |
| `302`  | Found              | Redirección temporal — el recurso está en otra URL por ahora |
| `304`  | Not Modified       | El recurso no cambió desde la última vez — usar la caché     |
| `307`  | Temporary Redirect | Redirección temporal que preserva el método HTTP (GET/POST)  |
| `308`  | Permanent Redirect | Redirección permanente que preserva el método HTTP           |

**¿Se personalizan en Django?** ❌ No como páginas de error — son respuestas exitosas.
Pero Django las genera frecuentemente para redirigir usuarios:

```python
from django.shortcuts import redirect

def login_exitoso(request):
    return redirect('/dashboard/')    # ← Django devuelve 302 automáticamente

# 301 — redirección permanente (SEO: cambio de URL definitivo)
from django.views.generic import RedirectView
path('perfil/', RedirectView.as_view(url='/cuenta/', permanent=True)),
#                                                    ↑ permanent=True → 301
#                                                    permanent=False  → 302 (defecto)
```

**El 302 es el más usado en Django:** login, logout, después de un form exitoso.
Siempre que llamás a `redirect()`, Django devuelve un 302 por defecto.

**El 304** lo gestiona el navegador y el servidor automáticamente con los headers de caché.
No requiere código del developer.

---

## Familia 4xx — Errores del cliente

El problema está del lado del que hizo el request.
La URL estaba mal, faltaba autenticación, o el recurso no existe.

| Código | Nombre               | Qué significa                                                       |
| ------ | -------------------- | ------------------------------------------------------------------- |
| `400`  | Bad Request          | El request está malformado o tiene datos inválidos                  |
| `401`  | Unauthorized         | Falta autenticación — el servidor no sabe quién sos                 |
| `403`  | Forbidden            | Autenticado pero sin permiso — el servidor sabe quién sos y dice no |
| `404`  | Not Found            | La URL o el recurso buscado no existe                               |
| `405`  | Method Not Allowed   | La URL existe pero no acepta ese método HTTP (GET vs POST)          |
| `408`  | Request Timeout      | El cliente tardó demasiado en enviar el request completo            |
| `410`  | Gone                 | El recurso existía pero fue eliminado permanentemente               |
| `413`  | Payload Too Large    | El archivo o cuerpo del request supera el límite del servidor       |
| `422`  | Unprocessable Entity | El request está bien formado pero tiene errores semánticos          |
| `429`  | Too Many Requests    | El cliente hizo demasiados requests en poco tiempo (rate limiting)  |

## Familia 5xx — Errores del servidor

El problema está del lado del servidor. El request estaba bien, pero el servidor falló.

| Código | Nombre                | Qué significa                                           |
| ------ | --------------------- | ------------------------------------------------------- |
| `500`  | Internal Server Error | El servidor lanzó una excepción no controlada           |
| `502`  | Bad Gateway           | El proxy o load balancer recibió una respuesta inválida |
| `503`  | Service Unavailable   | El servidor está sobrecargado o en mantenimiento        |
| `504`  | Gateway Timeout       | El proxy no recibió respuesta a tiempo del servidor     |

---

## Cuáles vale la pena personalizar en Django

| Familia | Código | ¿Personalizar?               | Razón                                                          |
| ------- | ------ | ---------------------------- | -------------------------------------------------------------- |
| 1xx     | todos  | ❌ No                        | El usuario nunca los ve — son automáticos del protocolo        |
| 2xx     | todos  | ❌ No como error             | Son éxitos — se controlan desde la vista normalmente           |
| 3xx     | `301`  | ⚠️ Redirigir desde la vista  | Cambio permanente de URL — usar `RedirectView(permanent=True)` |
| 3xx     | `302`  | ✅ Siempre, desde la vista   | Es lo que `redirect()` devuelve — el más usado en Django       |
| 4xx     | `400`  | ✅ Sí, en algunos casos      | Django lo dispara con `SuspiciousOperation`                    |
| 4xx     | `403`  | ✅ Sí, siempre               | El usuario necesita saber qué hacer (login, contactar admin)   |
| 4xx     | `404`  | ✅ Sí, siempre               | El más frecuente — URLs mal escritas o contenido eliminado     |
| 4xx     | `405`  | ⚠️ Opcional                  | Útil en APIs; raro que lo vea un usuario final                 |
| 4xx     | `429`  | ✅ Sí, si usas rate limiting | El usuario necesita saber que debe esperar                     |
| 5xx     | `500`  | ✅ Sí, siempre               | El más crítico — nunca mostrar el stack trace en producción    |
| 5xx     | `502`  | ❌ No en Django              | Lo maneja Nginx/proxy — Django no llega a ejecutarse           |
| 5xx     | `503`  | ❌ No en Django (mayormente) | Lo maneja Nginx/proxy o el sistema operativo                   |
| 5xx     | `504`  | ❌ No en Django              | Lo maneja el load balancer o proxy inverso                     |

---

**¿Por qué el 401 no se personaliza en Django?**

Django no usa el código `401` por convención.
Cuando un usuario no tiene sesión activa, la respuesta es siempre un **redirect 302** hacia el login — nunca un `401`.
El `401` es estándar en APIs REST puras (con tokens JWT), no en aplicaciones web tradicionales con sesiones.

---

---

# Parte I — Error 404

---

> _"La URL que buscás no existe. Pero el sitio sí."_
> **El más frecuente. Siempre vale la pena personalizarlo.**

---

## ¿Cuándo dispara Django un 404?

| Situación                                         | Cómo se dispara                   |
| ------------------------------------------------- | --------------------------------- |
| La URL no coincide con ningún patrón en `urls.py` | Automático, Django lo hace solo   |
| El objeto buscado no existe en la base de datos   | `get_object_or_404()` o `Http404` |
| El código lo lanza explícitamente                 | `raise Http404`                   |

---

## Cómo disparar un 404 desde el código

### La forma correcta: `get_object_or_404`

```python
from django.shortcuts import get_object_or_404, render
from .models import Producto

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    #          ↑ si pk=999 y no existe → dispara 404 automáticamente
    #            si existe              → devuelve el objeto normalmente
    return render(request, 'detalle.html', {'producto': producto})
```

**Por qué no usar `.get()` directamente:**

```python
# ❌ Forma incorrecta
producto = Producto.objects.get(pk=pk)
# Si no existe → DoesNotExist → crash → error 500
# Un "objeto no encontrado" termina siendo un "error del servidor". Incorrecto.

# ✅ Forma correcta
producto = get_object_or_404(Producto, pk=pk)
# Si no existe → 404. Semánticamente correcto — el recurso no existe.
```

### `get_object_or_404` acepta cualquier campo

```python
articulo = get_object_or_404(Articulo, slug=slug)

# con condición adicional: si existe pero no está publicado → también 404
articulo = get_object_or_404(Articulo, slug=slug, publicado=True)
```

### Lanzar `Http404` manualmente

```python
from django.http import Http404

def busqueda(request):
    query = request.GET.get('q', '')
    if len(query) < 3:
        raise Http404("La búsqueda necesita al menos 3 caracteres")
```

---

## El template `404.html`

```html
<!-- templates/404.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1 text-warning">404</h1>
  <h2>Página no encontrada</h2>
  <p class="text-muted">La página que buscás no existe o fue movida.</p>
  {% if exception %}
  <p class="text-secondary"><small>Detalle: {{ exception }}</small></p>
  {% endif %}
  <a href="{% url 'home' %}" class="btn btn-primary">Volver al inicio</a>
</div>

{% endblock %}
```

**Variable especial `{{ exception }}`:** Django la pasa automáticamente.
Contiene el mensaje dentro de `raise Http404("...")`.

---

## Manejador personalizado para el 404

```python
# mi_app/views.py
from django.shortcuts import render

def handler_404(request, exception):
    context = {
        'url_intentada': request.path,
    }
    return render(request, '404.html', context, status=404)
    #                                            ↑ status=404 es obligatorio
    #                                              sin él Django responde 200 aunque muestre el error
```

```python
# urls.py raíz del proyecto
handler404 = 'mi_app.views.handler_404'
```

---

## Probar el 404 en desarrollo

```python
# mi_app/views.py — solo para testing, sacar en producción
from django.shortcuts import render

def test_404(request):
    return render(request, '404.html', status=404)
```

```python
path('test-404/', test_404),
```

---

---

# Parte II — Error 403

---

> _"Sé quién sos. Pero no puedes entrar."_
> **Siempre vale la pena personalizarlo — y decidir si redirigir al login.**

---

## ¿Cuándo dispara Django un 403?

| Situación                                  | Cómo se dispara                                        |
| ------------------------------------------ | ------------------------------------------------------ |
| Permiso requerido y el usuario no lo tiene | `@permission_required(..., raise_exception=True)`      |
| Permiso requerido en vista de clase        | `PermissionRequiredMixin` con `raise_exception = True` |
| Lógica manual en la vista                  | `raise PermissionDenied`                               |
| Token CSRF inválido o ausente              | Middleware CSRF — automático                           |

---

## Cómo disparar un 403

### Con decorador

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('tienda.change_producto', raise_exception=True)
#                                              ↑ sin esto → redirige al login aunque tenga sesión
#                                                con esto  → muestra 403
def editar_producto(request, pk):
    ...
```

### Con Mixin en vista de clase

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView

class EditarProductoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Producto
    fields              = ['nombre', 'precio']
    template_name       = 'producto_form.html'
    permission_required = 'tienda.change_producto'
    raise_exception     = True
```

### Lanzar `PermissionDenied` manualmente

```python
from django.core.exceptions import PermissionDenied

def editar_perfil(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if perfil.usuario != request.user:
        raise PermissionDenied   # → 403
    ...
```

---

## El template `403.html`

```html
<!-- templates/403.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1 text-danger">403</h1>
  <h2>Acceso denegado</h2>
  <p class="text-muted">
    No tienes permiso para ver esta página. Contactá a un administrador si crees
    que esto es un error.
  </p>
  <a href="{% url 'home' %}" class="btn btn-secondary">Volver al inicio</a>
</div>

{% endblock %}
```

---

## Comportamiento del 403 según el estado de sesión

```
Usuario sin sesión → intenta acceder a /panel-admin/
      ↓
¿Cómo está configurado el decorador?

  @login_required solo                    → redirige a /login/?next=/panel-admin/
  @permission_required(raise_exception)   → muestra 403 (confuso si no tenía sesión)
  @login_required + @permission_required  → primero verifica sesión → redirige al login ✅
```

**Regla:** `@login_required` siempre antes de `@permission_required`.
Los decoradores se aplican de abajo hacia arriba — el orden importa.

---

## Redirección al login en lugar de mostrar el 403

### Opción A — Dejar que `@login_required` lo maneje (automático)

```python
# settings.py
LOGIN_URL = '/login/'

# views.py
@login_required   # → si no hay sesión: /login/?next=/mi-vista/
def mi_vista(request):
    ...
```

### Opción B — Redirigir manualmente desde la vista

```python
from django.shortcuts import redirect

@login_required
def panel(request):
    if not request.user.has_perm('app.view_reporte'):
        return redirect(f'/login/?next={request.path}')
    ...
```

### Opción C — Handler global (la más profesional)

```python
# mi_app/views.py
from django.shortcuts import redirect, render

def handler_403(request, exception):
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    return render(request, '403.html', status=403)
```

```python
# urls.py raíz
handler403 = 'mi_app.views.handler_403'
```

---

---

# Parte III — Error 500

---

> _"El servidor encontró un error que no supo manejar. Siempre es un bug del código."_
> **El más crítico. Siempre personalizar. Nunca mostrar el stack trace.**

---

## ¿Cuándo dispara Django un 500?

| Situación                              | Ejemplo                             |
| -------------------------------------- | ----------------------------------- |
| Excepción no capturada en la vista     | `AttributeError`, `TypeError`, etc. |
| Error en el template                   | Variable o método que no existe     |
| La base de datos no responde           | `OperationalError` de psycopg2      |
| Cualquier `Exception` que Django no ve | Cualquier bug no manejado           |

El 500 no se puede disparar intencionalmente — aparece cuando hay un bug.

---

## Por qué el `500.html` no puede heredar de `base.html`

> Si el servidor crasheó por un problema con la BD, intentar renderizar `base.html`
> (que puede tener `{{ user.username }}` u otras consultas) puede causar otro error encima del primero.

El `500.html` debe ser **HTML puro y estático**:

```html
<!-- templates/500.html — sin Django templates, sin extends, sin {% url %} -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Error del servidor</title>
    <style>
      body {
        font-family: sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        background: #f8f9fa;
        text-align: center;
        padding: 1rem;
      }
      h1 {
        font-size: 5rem;
        color: #dc3545;
        margin: 0;
      }
      h2 {
        color: #343a40;
      }
      p {
        color: #6c757d;
      }
      a {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.5rem 1.5rem;
        background: #0d6efd;
        color: #fff;
        border-radius: 0.375rem;
        text-decoration: none;
      }
    </style>
  </head>
  <body>
    <h1>500</h1>
    <h2>Error interno del servidor</h2>
    <p>Algo salió mal de nuestro lado. El equipo ya fue notificado.</p>
    <a href="/">Volver al inicio</a>
    <!-- ↑ "/" directo — no {% url 'home' %}, el motor de templates puede estar roto -->
  </body>
</html>
```

**Lo que NO puede tener:**

```
❌ {% extends 'base.html' %}
❌ {% url 'home' %}
❌ {{ user.username }}
❌ {% load static %}
```

---

## Manejador personalizado para el 500

```python
# mi_app/views.py
from django.shortcuts import render

def handler_500(request):
    # el 500 NO recibe 'exception' — el servidor está en estado inestable
    return render(request, '500.html', status=500)
```

```python
# urls.py raíz
handler500 = 'mi_app.views.handler_500'
```

---

## Notificar errores 500 al equipo

```python
# settings.py
ADMINS = [
    ('Nombre Developer', 'dev@empresa.com'),
]
```

Con `DEBUG = False` y `ADMINS` configurado, Django envía un email con el stack trace
completo cada vez que ocurre un 500. El usuario ve la página genérica; el equipo ve el detalle.

---

---

# Parte IV — Error 400 (Bad Request)

---

> _"El request llegó malformado. El servidor no lo puede procesar."_
> **Vale la pena personalizar si el proyecto tiene formularios complejos o APIs.**

---

## ¿Cuándo dispara Django un 400?

| Situación                                      | Cómo se dispara                          |
| ---------------------------------------------- | ---------------------------------------- |
| Datos del request inconsistentes o malformados | `raise SuspiciousOperation` en una vista |
| Headers de sesión inválidos                    | Automático por el middleware de sesión   |
| Datos de formulario con tamaño excesivo        | Automático por el parser del request     |

Más raro de ver en proyectos web simples. Más común en APIs.

---

## Cómo dispararlo manualmente

```python
from django.core.exceptions import SuspiciousOperation

def procesar_pago(request):
    monto = request.POST.get('monto')
    if not monto or int(monto) <= 0:
        raise SuspiciousOperation("El monto debe ser positivo")
        # ↑ dispara un 400 — el request tiene datos inválidos a nivel de protocolo
```

---

## El template `400.html`

```html
<!-- templates/400.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1 text-secondary">400</h1>
  <h2>Solicitud incorrecta</h2>
  <p class="text-muted">
    El servidor no pudo procesar la solicitud porque contiene datos inválidos.
  </p>
  <a href="{% url 'home' %}" class="btn btn-primary">Volver al inicio</a>
</div>

{% endblock %}
```

---

## Manejador personalizado para el 400

```python
# mi_app/views.py
from django.shortcuts import render

def handler_400(request, exception):
    return render(request, '400.html', status=400)
```

```python
# urls.py raíz
handler400 = 'mi_app.views.handler_400'
```

---

---

# Parte V — Error 429 (Too Many Requests)

---

> _"Estás haciendo demasiados requests en poco tiempo. Esperá."_
> **Vale la pena personalizar si el proyecto usa rate limiting.**

---

## ¿Qué es el rate limiting?

Es un mecanismo que limita cuántos requests puede hacer un usuario en un período de tiempo.
Protege el servidor contra ataques de fuerza bruta, bots y abusos.

```
Usuario hace 100 requests en 1 minuto
         ↓
El sistema detecta el abuso
         ↓
Los siguientes requests reciben 429
         ↓
Después de X segundos, vuelve a funcionar
```

---

## Django y el 429

Django no tiene rate limiting incorporado.
Se añade con la librería `django-ratelimit`:

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
# ↑ máximo 5 requests por minuto desde la misma IP
# block=True → si supera el límite → 429
def login_view(request):
    ...
```

---

## El template `429.html`

```html
<!-- templates/429.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1 text-warning">429</h1>
  <h2>Demasiados intentos</h2>
  <p class="text-muted">
    Realizaste demasiadas solicitudes en poco tiempo. Esperá unos minutos antes
    de intentarlo de nuevo.
  </p>
  <a href="{% url 'home' %}" class="btn btn-secondary">Volver al inicio</a>
</div>

{% endblock %}
```

---

---

# Parte VI — Errores que maneja la infraestructura, no Django

---

> No todo error llega a Django. El 502, 503 y 504 los maneja el servidor web (Nginx, Apache)
> antes de que Django se ejecute o cuando Django no puede responder.

---

## 502 — Bad Gateway

```
Navegador → Nginx → Django (Gunicorn)
                        ↑
                    Gunicorn está caído
                        ↓
                    Nginx devuelve 502
```

**Django no llega a ejecutarse.** La página de error es de Nginx, no de Django.
Se puede personalizar en la configuración de Nginx con una directiva `error_page`.

---

## 503 — Service Unavailable

Aparece cuando el servidor está en mantenimiento o sobrecargado.
En deploy con Nginx + Gunicorn, se puede configurar una página de mantenimiento estática:

```nginx
# nginx.conf
error_page 503 /mantenimiento.html;
location = /mantenimiento.html {
    root /var/www/html;
    internal;
}
```

El archivo `mantenimiento.html` es HTML puro — no pasa por Django.

---

## 504 — Gateway Timeout

El proxy o load balancer esperó demasiado al servidor. Generalmente indica que Django
tardó más de lo permitido en responder (query lenta, proceso pesado sin timeout).

**Solución:** no es una página de error — es un problema de performance o configuración.

---

---

# Resumen final

---

## Tabla de decisión: ¿personalizo o no?

| Error | ¿Personalizar en Django? | ¿Con qué template?    | ¿Puede heredar `base.html`? |
| ----- | ------------------------ | --------------------- | --------------------------- |
| `400` | ✅ Sí, si hay APIs/forms | `400.html`            | ✅ Sí                       |
| `403` | ✅ Sí, siempre           | `403.html` + redirect | ✅ Sí                       |
| `404` | ✅ Sí, siempre           | `404.html`            | ✅ Sí                       |
| `429` | ✅ Sí, si hay rate limit | `429.html`            | ✅ Sí                       |
| `500` | ✅ Sí, siempre           | `500.html`            | ❌ No — HTML puro           |
| `502` | ❌ No en Django          | Nginx/proxy           | —                           |
| `503` | ❌ No en Django          | Nginx/proxy           | —                           |
| `504` | ❌ No en Django          | Nginx/proxy           | —                           |

---

## Handlers en `urls.py` raíz

```python
# proyecto/urls.py

handler400 = 'mi_app.views.handler_400'
handler403 = 'mi_app.views.handler_403'
handler404 = 'mi_app.views.handler_404'
handler500 = 'mi_app.views.handler_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mi_app.urls')),
]
```

---

## Diferencias clave entre handlers

| Handler       | Recibe `exception` | Puede redirigir | Notas                                    |
| ------------- | ------------------ | --------------- | ---------------------------------------- |
| `handler_400` | ✅ Sí              | ✅ Sí           | —                                        |
| `handler_403` | ✅ Sí              | ✅ Sí           | Ideal para redirigir al login sin sesión |
| `handler_404` | ✅ Sí              | ✅ Sí           | El más usado                             |
| `handler_500` | ❌ No              | ⚠️ Con cuidado  | Servidor en estado inestable             |

---

## Checklist de producción

```
[ ] 1. Crear templates/404.html — puede usar {% extends 'base.html' %}
[ ] 2. Crear templates/403.html — puede usar {% extends 'base.html' %}
[ ] 3. Crear templates/500.html — HTML puro, sin Django templates
[ ] 4. Crear templates/400.html — si el proyecto tiene formularios o API
[ ] 5. DIRS configurado en TEMPLATES en settings.py
[ ] 6. DEBUG = False en producción
[ ] 7. ALLOWED_HOSTS con el dominio real
[ ] 8. handler403 con lógica de redirección al login si no hay sesión
[ ] 9. ADMINS configurado para recibir emails en caso de 500
[ ] 10. Página de mantenimiento estática (503) configurada en Nginx
```

---

## Flujo completo de errores

```
Request entra al servidor
        ↓
¿Nginx puede conectar con Django?
        │
        ├── NO → 502 (Nginx) o 503 (mantenimiento) o 504 (timeout)
        │          └── Manejado por Nginx, no por Django
        │
        └── SÍ → Django procesa el request
                        │
                        ├── URL no coincide ──────────────→ 404
                        │
                        └── Vista se ejecuta
                                │
                                ├── raise Http404 ─────────→ 404
                                ├── raise PermissionDenied ─→ 403
                                │     └── ¿tiene sesión?
                                │           NO → redirect /login/?next=
                                │           SÍ → mostrar 403.html
                                ├── SuspiciousOperation ───→ 400
                                ├── excepción no capturada ─→ 500 (HTML puro)
                                └── OK ──────────────────→ 200 ✅

DEBUG=True:  Django ignora tus templates y muestra páginas propias con info interna.
DEBUG=False: tus templates toman el control — nunca se expone info interna.
```

---

> _"En producción, el usuario nunca debería ver el stack trace de Python.
> Esa información es para el developer — y vía logs, no vía el navegador."_

---
