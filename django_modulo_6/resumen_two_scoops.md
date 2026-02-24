# 🍦 Resumen Pedagógico: "Two Scoops of Django"

> **"Two Scoops of Django"** (por Daniel Feldroy y Audrey Roy Greenfeld) no es un libro para aprender Django desde cero. Es un libro sobre **cómo hacer las cosas bien** cuando ya sabés lo básico. Es la recopilación de años de errores y aciertos de dos de los desarrolladores más experimentados de la comunidad.

A continuación, un resumen de las enseñanzas más valiosas del libro, explicadas de forma sencilla y listas para aplicar en proyectos reales.

---

## 1. Regla de Oro: Mantenelo simple y estándar

Django tiene su forma de hacer las cosas (el "Django Way"). El libro insiste en que no intentes reinventar la rueda ni luchar contra el framework.

- **No crees tu propio sistema de usuarios** desde cero si podés extender el de Django.
- **No uses microframeworks dentro de Django** para cosas que Django ya resuelve y resuelve bien (como usar SQLAlchemy en lugar del ORM de Django sin una razón de mucho peso).
- **Abrazá las convenciones**: Si Django espera que las plantillas estén en una carpeta `templates`, ponelas ahí. Las convenciones ahorran tiempo de discusión y facilitan que nuevos desarrolladores entiendan tu código en 5 minutos en lugar de 5 días.

---

## 2. La estructura del proyecto: El patrón "Core" o "Config"

El comando por defecto `django-admin startproject miproyecto` crea una carpeta `miproyecto/miproyecto`, lo cual es confuso porque mezcla el nombre del proyecto general con la carpeta de configuraciones.

**La recomendación de Two Scoops:**
Renombrar la carpeta interna de configuración a `config` o `core`.

```text
miproyecto/              ← Repositorio Git
├── manage.py
├── requirements.txt
├── config/              ← ⚙️ ¡ACÁ va settings y urls globales!
│   ├── settings.py
│   └── urls.py
├── usuarios/            ← 📦 App
├── productos/           ← 📦 App
└── ventas/              ← 📦 App
```

¿Por qué? Porque elimina la redundancia y deja claro de un vistazo dónde están las configuraciones globales.

---

## 3. Settings en múltiples archivos

A medida que un proyecto crece, no podés tener un único `settings.py` con las configuraciones de tu máquina local, las del servidor de pruebas y las de producción mezcladas con `if / else`. Es una receta para el desastre (ej: borrar la base de datos de producción por error).

**La recomendación:**
Crear una carpeta `settings/` y dividir las configuraciones:

```text
config/
└── settings/
    ├── __init__.py
    ├── base.py       ← Lo que es igual para todos (INSTALLED_APPS, etc.)
    ├── local.py      ← Base de datos SQLite, DEBUG=True
    ├── test.py       ← Para correr pruebas automatizadas
    └── production.py ← PostgreSQL, DEBUG=False, contraseñas seguras
```

---

## 4. El mantra: "Fat Models, Thin Views" (Modelos gordos, Vistas flacas)

Esta es probablemente **la regla arquitectónica más importante** del libro.

**El problema:**
Los principiantes suelen poner toda la lógica (cálculos matemáticos, validaciones complejas, envío de emails) dentro de `views.py`. Esto hace que las vistas sean kilométricas y muy difíciles de testear.

**La solución de Two Scoops:**
Mové la "lógica de negocio" a metoditos dentro de tus clases en `models.py`.

**❌ Mal (Lógica en la Vista):**

```python
def procesar_compra(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if producto.stock > 0 and producto.activo:
        # 20 líneas de código calculando impuestos,
        # descontando stock, enviando un email...
```

**✅ Bien (Lógica en el Modelo):**

```python
# models.py
class Producto(models.Model):
    # campos...
    def hay_stock_y_esta_activo(self):
        return self.stock > 0 and self.activo

    def procesar_compra_y_notificar(self, usuario):
        # La lógica pesada va acá

# views.py
def procesar_compra(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if producto.hay_stock_y_esta_activo():
        producto.procesar_compra_y_notificar(request.user)
```

**Resultado:** Vistas que son fáciles de leer (le dicen _qué_ hacer al modelo) y modelos independientes que saben _cómo_ hacerlo.

---

## 5. Diseño de Apps: Pequeñas y con un propósito único

Una "App" en Django no es el proyecto entero. Es un componente que hace **una sola cosa bien**.

**La regla general:**
Si el nombre de tu app es genérico como `core`, `main`, o `general` (y le metés de todo adentro), la estás pensando mal. Si tu app se llama `usuarios_y_pagos_y_notificaciones`, la estás pensando mal.

**Ejemplo de buenas apps:**

- `usuarios` (maneja registro y perfiles)
- `productos` (maneja el catálogo)
- `pagos` (maneja facturación)

Si una app tiene más de 10-15 modelos, probablemente necesita ser dividida en dos o tres apps más pequeñas.

---

## 6. Secretos fuera de Git

**¡Nunca subas contraseñas, claves de API o la `SECRET_KEY` de Django a GitHub!**

**La recomendación de Two Scoops:**
Usá variables de entorno. Herramientas como `django-environ` o `python-decouple` permiten leer configuraciones sensibles desde un archivo `.env` que queda **fuera** del control de versiones (agregado al `.gitignore`).

```python
# settings.py
import environ

env = environ.Env()
# Lee de un archivo .env si existe
environ.Env.read_env()

# Si no está en el .env, falla (esto es seguro)
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
```

---

## 7. Modelos: TimeStampedModel y orden

**El problema:** En el 99% de los proyectos, casi todas las tablas necesitan saber _cuándo_ se creó un registro y _cuándo_ fue la última vez que se modificó. Estar escribiendo esos dos campos una y otra vez es aburrido y propenso a olvidos.

**La solución:** Crear una clase abstracta base y heredar de ella.

```python
# core/models.py
from django.db import models

class TimeStampedModel(models.Model):
    """
    Una clase base abstracta que provee campos
    'creado_en' y 'modificado_en' a quienes la hereden.
    """
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Esto le dice a Django: No crees una tabla real para esto

# productos/models.py
class Producto(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    # ¡Listo! Automáticamente Producto tiene creado_en y modificado_en
```

---

## 8. Evitá los "Import estrella" (`import *`)

Hacer `from .models import *` es una pésima práctica en Python y el libro lo prohíbe terminantemente en Django.

**¿Por qué?**

- Contamina el "espacio de nombres" (namespace).
- Si alguien más lee tu código, no tiene idea de qué modelos estás usando realmente en esa vista.
- Los IDEs (Visual Studio Code, PyCharm) no pueden ayudarte a autocompletar o detectar errores bien.

**Usá siempre importaciones explícitas:**
`from .models import Producto, Categoria`

---

## 9. Seguridad: Nunca confíes en el usuario final

- Nunca uses diccionarios de datos directos de `request.POST` o `request.GET` para hacer consultas a la base de datos sin antes validarlos con **Formularios de Django** o **Serializadores (de DRF)**.
- Los formularios no solo están para generar cajitas de texto en HTML; su función principal y más poderosa es **limpiar y validar datos**.

---

## Resumen Final

_Two Scoops of Django_ se trata de **cordura y mantenimiento**. El código que escribís hoy lo va a leer otra persona (o vos mismo) en 6 meses. Si seguís el "Django Way", dividís tus configuraciones, mantenés las vistas flacas, las apps pequeñas y sacás los secretos del código, tu proyecto podrá crecer años sin convertirse en un monstruo de código espagueti.
