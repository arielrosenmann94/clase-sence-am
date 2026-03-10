# Proyecto: Alke Web Base

PDF original: https://docs.google.com/document/d/1h4g7qqD2UYHK7EqNa8OTz958-evzd7fe/edit

## Módulo 6 — Desarrollo Web con Django: Fundamentos

---

## ¿De qué se trata este proyecto?

Vas a construir una aplicación web real usando Django — paso a paso, lección por lección.

No necesitás tenerlo todo claro desde el principio. Cada lección agrega una pieza nueva,
y al final del módulo vas a tener una aplicación funcionando que puedes mostrar en tu portafolio.

**La empresa ficticia:** Alke Solutions necesita que su equipo aprenda a construir aplicaciones web con Django.
Tú sos parte de ese equipo. El proyecto que desarrollés es la demostración de que puedes hacerlo.

---

## Herramientas necesarias

| Herramienta        | Para qué se usa                                  | Cómo conseguirla                                       |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------ |
| Python 3.x         | El lenguaje base — Django está escrito en Python | [python.org](https://python.org)                       |
| Django             | El framework web que usamos en todo el módulo    | `pip install django`                                   |
| Visual Studio Code | El editor de código — donde vas a escribir todo  | [code.visualstudio.com](https://code.visualstudio.com) |

---

## Objetivo

Al terminar este proyecto vas a poder:

- Crear un proyecto Django desde cero
- Organizar el código en aplicaciones separadas
- Hacer que URLs, vistas y templates trabajen juntos
- Agregar estilos CSS a través del sistema de archivos estáticos de Django
- Explicar cómo funciona el flujo de una petición en Django

---

## Requerimientos

> Estos son los puntos que se van a evaluar. Usá esta lista para revisar tu proyecto antes de entregar.

---

### 1. Configuración del proyecto

- [ ] El proyecto Django está creado y corre sin errores con `python manage.py runserver`
- [ ] Se puede acceder a `http://127.0.0.1:8000/` en el navegador
- [ ] El proyecto fue creado usando `django-admin startproject`
- [ ] El entorno virtual está configurado y Django instalado dentro de él

**Pista:** Si el servidor arranca y ves la pantalla de bienvenida de Django con el cohete, esta parte está lista ✅

---

### 2. Estructura y aplicaciones

- [ ] El proyecto tiene al menos una aplicación creada con `python manage.py startapp`
- [ ] La aplicación está registrada en `INSTALLED_APPS` dentro de `settings.py`
- [ ] Se entiende para qué sirve cada archivo generado (`views.py`, `models.py`, `apps.py`, etc.)

**Pista:** Si haces `python manage.py runserver` después de agregar la app y no hay errores, está bien registrada ✅

---

### 3. Vistas y rutas

- [ ] Hay al menos una vista definida en `views.py` que devuelve una respuesta
- [ ] Las URLs están configuradas tanto en el `urls.py` del proyecto como en el de la app
- [ ] Cada vista tiene su URL y al visitarla se muestra el contenido correspondiente

**Pista:** Si navegás a la URL de tu vista en el browser y ves tu contenido (no el cohete de Django), las rutas están bien ✅

---

### 4. Templates y archivos estáticos

- [ ] Hay al menos un template HTML en una carpeta `templates/`
- [ ] La vista renderiza ese template con `render(request, 'nombre.html')`
- [ ] Hay al menos un archivo CSS en una carpeta `static/`
- [ ] El CSS se carga correctamente usando `{% load static %}` y `{% static 'archivo.css' %}`
- [ ] Los estilos se aplican visualmente en el navegador

**Pista:** Si abres las DevTools del navegador (F12 → Network) y el archivo CSS carga con status 200, está bien configurado ✅

---

## Criterios de evaluación

| Criterio                                     | Puntaje     |
| -------------------------------------------- | ----------- |
| El proyecto corre sin errores                | 20 pts      |
| Estructura correcta de proyecto y aplicación | 20 pts      |
| URLs y vistas funcionando                    | 20 pts      |
| Templates integrados con vistas              | 20 pts      |
| Archivos estáticos (CSS) aplicados           | 10 pts      |
| El participante puede explicar cómo funciona | 10 pts      |
| **Total**                                    | **100 pts** |

---

## Desarrollo por lecciones

El proyecto se construye de forma incremental. Al final de cada lección, el proyecto debe funcionar.

---

### Lección 1 — Configuración inicial

**Objetivo:** Tener Django instalado y el proyecto corriendo.

**Tareas:**

- [ ] Crear la carpeta del proyecto
- [ ] Crear el entorno virtual: `python -m venv venv`
- [ ] Activar el entorno: `source venv/bin/activate` (Mac/Linux) o `venv\Scripts\activate` (Windows)
- [ ] Instalar Django: `pip install django`
- [ ] Crear el proyecto: `django-admin startproject mi_proyecto .`
- [ ] Correr el servidor: `python manage.py runserver`
- [ ] Verificar en el navegador: `http://127.0.0.1:8000/`

**Al terminar esta lección el proyecto debe mostrar la pantalla de bienvenida de Django.**

```
mi_proyecto/
├── manage.py         ← el comando central del proyecto
├── mi_proyecto/
│   ├── settings.py   ← configuración general
│   ├── urls.py       ← rutas del proyecto
│   └── wsgi.py       ← punto de entrada del servidor
```

---

### Lección 2 — Creación de la aplicación

**Objetivo:** Crear una app y registrarla en el proyecto.

**Tareas:**

- [ ] Crear la app: `python manage.py startapp mi_app`
- [ ] Abrir `settings.py` y agregar `'mi_app'` a `INSTALLED_APPS`
- [ ] Revisar qué archivo es cada cosa dentro de `mi_app/`

**Al terminar esta lección el proyecto debe seguir corriendo sin errores con la app registrada.**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'mi_app',   # ← la app que creamos
]
```

**¿Para qué sirve cada archivo de la app?**

| Archivo     | Para qué sirve                                                   |
| ----------- | ---------------------------------------------------------------- |
| `views.py`  | Las funciones que responden a los requests                       |
| `models.py` | Los modelos de la base de datos (usaremos en módulos siguientes) |
| `apps.py`   | Configuración de la app                                          |
| `admin.py`  | Registro de modelos en el panel de administración                |
| `tests.py`  | Tests automáticos (usaremos en módulos siguientes)               |

---

### Lección 3 — Vistas y URLs

**Objetivo:** Que el navegador muestre algo cuando visitás una URL.

**Tareas:**

- [ ] Crear una vista en `mi_app/views.py`
- [ ] Crear `mi_app/urls.py` y definir la ruta de la vista
- [ ] Conectar las URLs de la app al `urls.py` del proyecto con `include()`

**Al terminar esta lección, visitar `http://127.0.0.1:8000/inicio/` debe mostrar contenido propio.**

```python
# mi_app/views.py
from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')
```

```python
# mi_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
]
```

```python
# mi_proyecto/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('mi_app.urls')),   # ← conectar la app
]
```

---

### Lección 4 — Templates y archivos estáticos

**Objetivo:** Tener una página HTML con estilos propios.

**Tareas:**

- [ ] Crear la carpeta `templates/` y el archivo `inicio.html`
- [ ] Configurar `DIRS` en `TEMPLATES` en `settings.py`
- [ ] Crear la carpeta `static/` y un archivo `style.css`
- [ ] Configurar `STATICFILES_DIRS` en `settings.py`
- [ ] Cargar el CSS en el template con `{% load static %}`

**Al terminar esta lección, la página debe mostrarse con estilos aplicados.**

```html
<!-- templates/inicio.html -->
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="{% static 'style.css' %}" />
  </head>
  <body>
    <h1>Bienvenido a Alke Web Base</h1>
  </body>
</html>
```

```python
# settings.py — agregar al final
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## Entregables

### 1. Proyecto comprimido `.zip`

El zip debe incluir **todo el proyecto** con esta estructura mínima:

```
mi_proyecto_base.zip
└── mi_proyecto/
    ├── manage.py
    ├── requirements.txt        ← generado con: pip freeze > requirements.txt
    ├── mi_proyecto/
    │   ├── settings.py
    │   └── urls.py
    ├── mi_app/
    │   ├── views.py
    │   └── urls.py
    ├── templates/
    │   └── inicio.html         ← al menos un template
    └── static/
        └── style.css           ← al menos un archivo CSS
```

> ⚠️ **No incluir** la carpeta `venv/` en el zip — pesa mucho y no es parte del código.
> ✅ **Sí incluir** el archivo `requirements.txt` para que el evaluador pueda reinstalar las dependencias.

---

### 2. Documento explicativo (PDF o DOCX)

El documento debe tener **estas cinco secciones** y no necesita ser largo — una página es suficiente:

| Sección                      | Qué escribir                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------- |
| **Descripción del proyecto** | En 2-3 líneas: qué hace la app y qué páginas tiene                           |
| **¿Cómo instalar y correr?** | Los comandos para que alguien pueda correr el proyecto desde cero            |
| **Estructura del proyecto**  | Un árbol de carpetas comentado (igual al de esta guía)                       |
| **Flujo de una petición**    | Explicar con tus palabras qué pasa cuando alguien visita una URL             |
| **Dificultades encontradas** | Qué costó más, qué error fue el más difícil de resolver y cómo lo resolviste |

---

### 3. Capturas de pantalla

Incluir al menos **3 capturas**:

| Captura                               | Qué mostrar                                           |
| ------------------------------------- | ----------------------------------------------------- |
| El proyecto corriendo en el navegador | La URL `127.0.0.1:8000` con el contenido propio       |
| El panel de administración Django     | La URL `127.0.0.1:8000/admin/` con el login de Django |
| El código de una vista o template     | Una captura del editor mostrando el código            |

---

## Preguntas frecuentes

**¿Puedo usar Bootstrap en el CSS?**
Sí, puedes incluir Bootstrap desde un CDN. El requisito es que haya al menos un archivo CSS propio en `static/`.

**¿Cuántas páginas tiene que tener la app?**
Al menos una página que muestre contenido propio (no la pantalla de bienvenida de Django).

**¿Tengo que usar base de datos?**
No en este módulo. Los templates pueden mostrar contenido estático o variables pasadas desde la vista.

**¿Qué pasa si el proyecto no corre?**
Incluí igualmente el zip con el código, el documento explicativo y las capturas de lo que sí funcionó.
En el documento explicativo describe qué error encontraste y qué intentaste para resolverlo.

---

## Referencias

- [Django Project — Documentación oficial](https://docs.djangoproject.com/)
- [Django Girls — Tutorial paso a paso](https://tutorial.djangogirls.org/)
- [Simple is Better than Complex — Guías prácticas](https://simpleisbetterthancomplex.com/)

---

## Portafolio

Este proyecto es la base de tu portafolio como developer Django.
Una app bien documentada, con código limpio y un `README` claro comunica más que cualquier certificado.
Tratalo como si fuera un proyecto real que le vas a mostrar a un cliente o a un empleador.

---
