# 🌐 Django — Módulo 7 · Clase 13

## Construcción de APIs con Django Rest Framework (DRF)

---

> _"En el ecosistema digital moderno, una aplicación que no se comunica con el resto está destinada al aislamiento. Las APIs son el lenguaje universal del intercambio de información."_

---

## ¿Qué vas a aprender hoy?

- 🏗️ Qué es una API y por qué el estándar REST es el preferido en la industria
- 📦 Qué es Django Rest Framework y cómo simplifica la creación de servicios web
- 🔄 Qué son los Serializadores y por qué son el "corazón" de una API
- 🚦 Cómo funcionan las Vistas (APIViews y ViewSets) para procesar peticiones HTTP
- 🗺️ Cómo usar Routers para generar URLs automáticas y limpias
- 🔐 Cómo proteger tus datos mediante Autenticación y Permisos
- 🧪 Cómo probar y documentar una API de forma profesional

---

---

# ¿POR QUÉ HABLAR DE APIs?

---

## El lenguaje de la conectividad

Una **API** (Application Programming Interface) es un conjunto de definiciones y protocolos que permiten que dos aplicaciones se comuniquen entre sí. En el contexto web, una API permite que un servidor entregue datos a un cliente (una app móvil, un sitio en React, un reloj inteligente) sin necesidad de entregarle una página HTML completa.

> 📊 **Dato real**: De acuerdo con el reporte "The State of the API" de Postman (2025), el 93% de los desarrolladores a nivel mundial utiliza APIs RESTful en su trabajo diario, consolidando este estándar como el pilar de la arquitectura de servicios web moderna.
>
> _Fuente: Postman, "The State of the API 2025 Report"_

---

## El Estándar REST

**REST** (Representational State Transfer) es un estilo de arquitectura que utiliza los verbos del protocolo HTTP para realizar operaciones sobre **recursos**.

```
Recurso: "Producto" (URL base: /api/productos/)

Verbo HTTP | Acción                   | Ejemplo de uso
-----------|--------------------------|-----------------------------------------
GET        | Leer / Listar            | Obtener el catálogo de productos
POST       | Crear                    | Agregar un nuevo producto al almacén
PUT/PATCH  | Actualizar               | Modificar el precio de un producto
DELETE     | Eliminar                 | Quitar un producto descatalogado
```

> 📊 **Dato real**: Se estima que para finales de 2026, la economía de las APIs generará un flujo de datos superior a los 10 zettabytes anuales, impulsado principalmente por la integración de servicios de Inteligencia Artificial y Microservicios.
>
> _Fuente: IDC (International Data Corporation), "Global DataSphere Forecast 2024-2028"_

---

---

# PARTE I — INTRODUCCIÓN A DJANGO REST FRAMEWORK (DRF)

---

## ¿Qué es DRF?

Django por defecto está diseñado para devolver HTML. **Django Rest Framework (DRF)** es un toolkit potente y flexible que se instala sobre Django para permitirle devolver **JSON** (JavaScript Object Notation), el formato estándar de intercambio de datos hoy en día.

**Por qué usar DRF y no "Django puro":**

- 🛡️ Autenticación avanzada (Token, JWT, OAuth).
- 📋 Serialización automática de modelos complejos.
- 🎨 Navegador de API interactivo (Web Browsable API).
- ⚙️ Modularidad extrema para personalizar cada parte del flujo.

---

## Instalación y Configuración

Para integrar DRF en un proyecto (como el de nuestra empresa ficticia **"Distribuidora Cóndor Andino"**), se deben seguir estos pasos:

1. Instalar el paquete: `pip install djangorestframework`
2. Registrarlo en `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # ← Agregamos el módulo de API
    'tienda_condor',   # ← Nuestra aplicación de negocio
]
```

---

---

# PARTE II — LOS SERIALIZADORES (SERIALIZERS)

---

## El "Traductor" de la API

El problema principal es que los objetos de Python (modelos de Django) no pueden enviarse directamente por la red. La base de datos guarda filas, Django tiene objetos, pero el cliente necesita **JSON**.

El **Serializador** es el componente encargado de esta traducción bidireccional:

```
        OBJETO DJANGO (Python)                      FORMATO JSON (Texto)
        ----------------------                      --------------------
        producto_1 = {                              {
            "id": 45,                                 "id": 45,
            "nombre": "Café Araucano",      ⇄         "nombre": "Café Araucano",
            "precio": 8990                            "precio": 8990
        }                                           }
```

---

## ModelSerializer: La forma eficiente

DRF ofrece `ModelSerializer`, que lee la definición de tu modelo y genera automáticamente el serializador correspondiente, incluyendo validaciones automáticas.

```python
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'  # O especificar: ('id', 'nombre', 'precio')
```

> 💡 **Importante**: El serializador no solo convierte de objeto a JSON (lectura), sino que también valida que los datos que vienen del cliente (POST/PUT) cumplan con las reglas del modelo antes de guardarlos.

---

---

# PARTE III — VISTAS Y VIEWSETS

---

## Diferentes niveles de abstracción

DRF permite escribir la lógica de la API en diferentes niveles, desde el más manual hasta el más automático.

### 1. APIView (Control Total)

Es similar a una vista de Django basada en clase, pero adaptada para APIs. Tú defines el método `get()`, `post()`, etc.

### 2. Generic Views (Equilibrio)

Django ya trae lógica pre-escrita para "Listar y Crear" o "Detalle, Actualizar y Eliminar". Solo configuras el queryset y el serializador.

### 3. ViewSets (Máxima Productividad)

Un **ViewSet** permite definir la lógica para todas las operaciones CRUD en una sola clase. No defines "get" o "post", sino acciones como `list()`, `retrieve()`, `create()`, `update()` y `destroy()`.

```python
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

---

---

# PARTE IV — RUTEO AUTOMÁTICO (ROUTERS)

---

## Olvídate de escribir URLs una por una

Cuando usas ViewSets, no necesitas registrar manualmente la URL para listar, la URL para el detalle, la URL para editar, etc. Los **Routers** lo hacen por ti.

```python
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = router.urls
```

**Resultado automático:**

- `GET /api/productos/` → Lista todos los productos.
- `POST /api/productos/` → Crea un producto.
- `GET /api/productos/1/` → Detalle del producto 1.
- `PUT /api/productos/1/` → Edita el producto 1.
- `DELETE /api/productos/1/` → Elimina el producto 1.

---

---

# PARTE V — SEGURIDAD: AUTENTICACIÓN Y PERMISOS

---

## ¿Quién puede entrar?

Una API pública sin protección es un riesgo de seguridad crítico. DRF separa la protección en dos conceptos:

### 1. Autenticación (¿Quién eres?)

Identifica al usuario. Puede ser mediante sesión (cookies), autenticación básica o **Tokens** (el estándar para APIs).

### 2. Permisos (¿Qué puedes hacer?)

Decide si el usuario autenticado tiene el derecho de realizar la acción.

**Permisos comunes incluidos:**

- `AllowAny`: Acceso libre (público).
- `IsAuthenticated`: Solo usuarios logueados.
- `IsAdminUser`: Solo superusuarios.
- `IsAuthenticatedOrReadOnly`: Público para ver, privado para editar/borrar.

```python
class ProductoViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAuthenticatedOrReadOnly]
```

---

---

# RESUMEN — El flujo de una petición en DRF

---

```
Petición HTTP (GET/POST) ──▶ URL (Router) ──▶ Vista (ViewSet)
                                                 │
                                                 ▼
        Respuesta JSON ◀── Serializador ◀── Objeto Modelo
```

---

## Glosario de la clase

| Concepto       | Definición                                                               |
| -------------- | ------------------------------------------------------------------------ |
| **REST**       | Estilo de arquitectura para comunicación entre sistemas usando HTTP.     |
| **JSON**       | Formato de texto ligero para intercambio de datos (clave-valor).         |
| **Serializer** | Clase que transforma modelos en JSON y valida datos entrantes.           |
| **ViewSet**    | Clase que agrupa toda la lógica CRUD para un recurso en un solo lugar.   |
| **Router**     | Herramienta que genera automáticamente las rutas URL para un ViewSet.    |
| **Token**      | Cadena de caracteres que identifica de forma segura a un cliente de API. |
| **Endpoint**   | Una URL específica de la API donde se puede acceder a un recurso.        |

---

> _"Construir una API con Django Rest Framework es como ensamblar una maquinaria de precisión: cada pieza tiene un propósito claro, y cuando todas encajan, tu aplicación adquiere una escala global."_

---
