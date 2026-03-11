# Respuestas al Desafío para Avanzados — Clase 1

Este documento es para uso del profesor. Aquí están las explicaciones técnicas a los 10 desafíos planteados en la práctica.

---

### 1. El Misterio de la Tabla ManyToMany

**Respuesta:** Django tiene una convención de nombres por defecto. Si el modelo se llama `Plato` y el campo se llama `ingredientes` dentro de una app llamada `menu`, Django busca automáticamente la tabla `menu_plato_ingredientes`. Como nuestro script SQL sigue exactamente esa convención, la conexión es automática.

### 2. Filtros en el Admin

**Respuesta:** Para buscar por campos de modelos relacionados, se usa la sintaxis de doble guion bajo (`__`):

```python
search_fields = ['ingredientes__nombre']
```

### 3. El superpoder de `ReadOnlyField`

**Respuesta:** Una técnica limpia es sobrescribir el método `get_readonly_fields` en el `ModelAdmin`:

```python
def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self.model._meta.fields] + [f.name for f in self.model._meta.many_to_many]
```

### 4. Custom QuerySets

**Respuesta:** Se sobrescribe el método `get_queryset` en el `ModelAdmin`:

```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(disponible=True)
```

### 5. Formato de Moneda

**Respuesta:** Se crea un método en el modelo (o en el Admin) y se agrega a `list_display`:

```python
def precio_formateado(self, obj):
    return f"${obj.precio:,.0f}".replace(",", ".")
precio_formateado.short_description = 'Precio'
```

### 6. Contador de Relaciones

**Respuesta:** Se usa `annotate` en el QuerySet del Admin:

```python
from django.db.models import Count
def get_queryset(self, request):
    return super().get_queryset(request).annotate(total_platos=Count('plato'))
```

### 7. La importancia de `__str__`

**Respuesta:** Sin `__str__`, Django muestra algo como `<Ingrediente object (1)>`. Esto hace que sea imposible para un humano saber qué ingrediente está seleccionando en un formulario, rompiendo totalmente la usabilidad del sistema.

### 8. Seguridad en la Base de Datos

**Respuesta:** El botón "Añadir" lo controla el **Sistema de Permisos de Django** (Auth), no PostgreSQL. Django asume que si eres "Superusuario", puedes hacer todo. El error solo aparecerá cuando Django intente ejecutar el `INSERT` y PostgreSQL lo rechace por falta de permisos.

### 9. Rendimiento (Select Related)

**Respuesta:** Se usa el atributo `list_select_related` en el `ModelAdmin`:

```python
list_select_related = ['categoria']
```

Esto hace un `JOIN` en la base de datos y trae todo en una sola consulta.

### 10. Exploración de Metadatos

**Respuesta:** Sí, el comando es:

```bash
python manage.py inspectdb > models_generados.py
```

Este comando analiza las tablas existentes y genera el código Python necesario. Es la forma más rápida de empezar un proyecto con una base de datos legacy.

---
