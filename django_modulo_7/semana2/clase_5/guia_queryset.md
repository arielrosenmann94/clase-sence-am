# 📘 Guía Completa: QuerySet en Django
## Todo lo que necesitas saber para trabajar con datos como un profesional

> **AE 7.3** — Implementar la capa de modelo de acceso a datos utilizando entidades con relaciones.
>
> 📖 Esta guía es un material de referencia. Léanla, vuelvan a ella, úsenla como consulta cuando estén escribiendo código.

---

## 🗺️ Índice

| # | Tema |
|---|------|
| **1** | ¿Qué es un QuerySet? (y qué NO es) |
| **2** | El concepto clave: evaluación perezosa |
| **3** | Los métodos que vas a usar el 90% del tiempo |
| **4** | Filtros: el lenguaje secreto del doble guión bajo |
| **5** | Encadenar consultas: el superpoder del ORM |
| **6** | Métodos que devuelven UN objeto (no un QuerySet) |
| **7** | Contar, verificar y agregar sin cargar datos |
| **8** | Ordenar, limitar y paginar resultados |
| **9** | Anotaciones: agregarle columnas calculadas a tus resultados |
| **10** | Consultas complejas con Q Objects |
| **11** | Patrones reales: consultas que vas a escribir en tu primer trabajo |
| **12** | Los 7 errores más comunes con QuerySets |

---

---

# 🔍 1. ¿Qué es un QuerySet? (y qué NO es)

---

Un QuerySet es la forma en que Django te permite **pedirle datos a la base de datos**. Cada vez que escribes algo como:

```python
Producto.objects.all()
```

Eso devuelve un QuerySet. Pero — y esto es importante — **no es una lista de Python**. Es un objeto especial que tiene dos propiedades fundamentales:

### 1. Describe una intención, no un resultado

Cuando escribes `Producto.objects.filter(activo=True)`, Django **no va a la base de datos todavía**. Solo anota internamente: *"cuando alguien necesite los datos, busca productos donde activo sea True"*.

Es como hacer una lista de compras: escribir "leche" en el papel no hace que la leche aparezca en tu refrigerador. Solo describe lo que necesitas. Django funciona igual.

### 2. Es encadenable

Puedes agregar filtros, ordenamientos y transformaciones uno tras otro, y Django los acumula todos antes de ejecutar una sola consulta:

```python
# Cada línea agrega una instrucción, pero NINGUNA va a la BD todavía
qs = Producto.objects.filter(activo=True)
qs = qs.filter(precio__gte=100)
qs = qs.order_by('nombre')
qs = qs[:10]

# Django ejecuta UNA sola consulta SQL cuando realmente necesitas los datos
for p in qs:    # ← AQUÍ va a la BD
    print(p.nombre)
```

### ¿Qué NO es un QuerySet?

| Un QuerySet NO es... | ¿Por qué importa? |
|:---|:---|
| Una lista de Python (`list`) | No puedes usar `append()`, `sort()` ni `len()` directamente en él |
| Una consulta SQL | Django genera el SQL por ti — tú piensas en objetos Python |
| Un resultado inmediato | Los datos no se cargan hasta que los necesitas |
| Un objeto que se ejecuta una sola vez | Puedes reusar el mismo QuerySet en varias partes del código |

> *Fuente: Django Software Foundation. (2024). QuerySet API reference.* [https://docs.djangoproject.com/en/stable/ref/models/querysets/](https://docs.djangoproject.com/en/stable/ref/models/querysets/)

---

---

# ⏳ 2. Evaluación Perezosa (Lazy Evaluation)

---

Este concepto es la clave para entender por qué Django es tan eficiente. **Un QuerySet no ejecuta la consulta SQL hasta que algo lo obliga a entregar datos.**

### ¿Cuándo se evalúa un QuerySet?

| Acción | ¿Ejecuta el SQL? | ¿Por qué? |
|:---|:---|:---|
| `qs = Producto.objects.filter(activo=True)` | ❌ No | Solo estás describiendo la consulta |
| `qs = qs.order_by('nombre')` | ❌ No | Solo estás agregando instrucciones |
| `for p in qs:` | ✅ Sí | El `for` necesita los datos reales |
| `list(qs)` | ✅ Sí | `list()` convierte el QS a lista — necesita los datos |
| `print(qs)` | ✅ Sí | Para imprimir, Django necesita los objetos |
| `len(qs)` | ✅ Sí | Para contar, necesita ejecutar la consulta |
| `qs[0]` | ✅ Sí | Para acceder a un índice, necesita los datos |
| `if qs:` | ✅ Sí | Para evaluar como booleano, necesita verificar si hay resultados |
| `qs.count()` | ✅ Sí | Ejecuta `SELECT COUNT(*)` — pero sin traer los objetos |
| `qs.exists()` | ✅ Sí | Ejecuta `SELECT 1 LIMIT 1` — la forma más eficiente de verificar |

### ¿Por qué es útil?

Porque puedes construir consultas complejas paso a paso, acumulando condiciones, y Django las ejecuta todas juntas en **una sola consulta SQL optimizada**. En vez de hacer 5 viajes a la BD, haces 1.

```python
# Esto NO genera 4 consultas SQL — genera 1 sola
qs = Producto.objects.all()                      # Instrucción 1
qs = qs.filter(activo=True)                      # Instrucción 2
qs = qs.filter(precio__lte=500)                  # Instrucción 3
qs = qs.order_by('-precio')                      # Instrucción 4

# SQL generado (1 sola consulta):
# SELECT * FROM tienda_producto
# WHERE activo = TRUE AND precio <= 500
# ORDER BY precio DESC
```

> 💡 **Regla de oro:** Un QuerySet solo va a la base de datos cuando algo lo fuerza a entregar datos reales. Mientras solo describes, acumulas y encadenas, no hay costo.
>
> *Fuente: Django Software Foundation. (2024). When QuerySets are evaluated.* [https://docs.djangoproject.com/en/stable/ref/models/querysets/#when-querysets-are-evaluated](https://docs.djangoproject.com/en/stable/ref/models/querysets/#when-querysets-are-evaluated)

---

---

# 🛠️ 3. Los Métodos que Vas a Usar el 90% del Tiempo

---

Estos son los métodos más frecuentes. Cada uno devuelve un **nuevo QuerySet** (excepto los que devuelven un solo objeto — esos los vemos en la sección 6).

Usaremos como ejemplo los modelos de NebulaShop que definimos en clases anteriores:

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Producto(models.Model):
    nombre    = models.CharField(max_length=200)
    precio    = models.DecimalField(max_digits=10, decimal_places=2)
    stock     = models.IntegerField(default=0)
    activo    = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
```

---

### `.all()` — Todos los registros

```python
todos = Producto.objects.all()
# SQL: SELECT * FROM tienda_producto
```

Usarlo solo es necesario cuando quieres **explícitamente** todos los registros. En la práctica, casi siempre filtras.

---

### `.filter(**kwargs)` — Los que cumplen una condición

```python
# Productos activos
Producto.objects.filter(activo=True)
# SQL: SELECT * FROM tienda_producto WHERE activo = TRUE

# Productos con precio mayor o igual a 100
Producto.objects.filter(precio__gte=100)
# SQL: SELECT * FROM tienda_producto WHERE precio >= 100

# Múltiples condiciones (se combinan con AND)
Producto.objects.filter(activo=True, precio__gte=100)
# SQL: SELECT * FROM tienda_producto WHERE activo = TRUE AND precio >= 100
```

---

### `.exclude(**kwargs)` — Los que NO cumplen una condición

`.exclude()` es lo opuesto a `.filter()`:

```python
# Todos los productos EXCEPTO los inactivos
Producto.objects.exclude(activo=False)
# SQL: SELECT * FROM tienda_producto WHERE NOT (activo = FALSE)

# Productos que NO sean de la categoría "Accesorios"
Producto.objects.exclude(categoria__nombre='Accesorios')
```

---

### `.order_by(*fields)` — Ordenar los resultados

```python
# Orden ascendente (A → Z, menor → mayor)
Producto.objects.order_by('nombre')
# SQL: SELECT * FROM tienda_producto ORDER BY nombre ASC

# Orden descendente (Z → A, mayor → menor) → se agrega un guión
Producto.objects.order_by('-precio')
# SQL: SELECT * FROM tienda_producto ORDER BY precio DESC

# Orden múltiple: primero por categoría, después por precio descendente
Producto.objects.order_by('categoria__nombre', '-precio')
```

---

### `.values(*fields)` — Solo ciertas columnas (devuelve diccionarios)

En vez de traer objetos completos, `.values()` trae solo las columnas que necesitas:

```python
Producto.objects.values('nombre', 'precio')
# Devuelve: [{'nombre': 'Telescopio X', 'precio': Decimal('599.99')}, ...]
# SQL: SELECT nombre, precio FROM tienda_producto
```

Esto es más eficiente cuando solo necesitas mostrar una tabla o enviar datos a un template.

---

### `.values_list(*fields)` — Solo ciertas columnas (devuelve tuplas)

Igual que `.values()`, pero en vez de diccionarios devuelve tuplas:

```python
Producto.objects.values_list('nombre', 'precio')
# Devuelve: [('Telescopio X', Decimal('599.99')), ...]

# Si solo necesitas UNA columna, usa flat=True para obtener una lista plana
Producto.objects.values_list('nombre', flat=True)
# Devuelve: ['Telescopio X', 'Teclado Mecánico', 'Audífonos Bluetooth', ...]
```

---

### `.distinct()` — Eliminar duplicados

```python
# Categorías que tienen al menos un producto activo (sin repetir la categoría)
Categoria.objects.filter(productos__activo=True).distinct()
```

**¿Cuándo es obligatorio?** Cada vez que filtras a través de una relación inversa o ManyToMany. Sin `.distinct()`, obtienes una fila duplicada por cada coincidencia.

---

---

# 🔑 4. Filtros: El Lenguaje Secreto del Doble Guión Bajo

---

El doble guión bajo `__` es el operador más versátil del ORM de Django. Se usa para **dos cosas completamente distintas**, y entender la diferencia es fundamental.

## Uso 1: Comparaciones (lookups)

Después del nombre del campo, `__` indica **qué tipo de comparación** hacer:

| Lookup | Significado | Ejemplo | SQL generado |
|:---|:---|:---|:---|
| `__exact` | Igual a (es el default) | `filter(nombre__exact='Telescopio')` | `WHERE nombre = 'Telescopio'` |
| `__iexact` | Igual, ignorando mayúsculas | `filter(nombre__iexact='telescopio')` | `WHERE UPPER(nombre) = 'TELESCOPIO'` |
| `__contains` | Contiene el texto | `filter(nombre__contains='tele')` | `WHERE nombre LIKE '%tele%'` |
| `__icontains` | Contiene, ignorando mayúsculas | `filter(nombre__icontains='tele')` | `WHERE UPPER(nombre) LIKE '%TELE%'` |
| `__startswith` | Empieza con | `filter(nombre__startswith='Tel')` | `WHERE nombre LIKE 'Tel%'` |
| `__endswith` | Termina con | `filter(nombre__endswith='pro')` | `WHERE nombre LIKE '%pro'` |
| `__gt` | Mayor que | `filter(precio__gt=100)` | `WHERE precio > 100` |
| `__gte` | Mayor o igual que | `filter(precio__gte=100)` | `WHERE precio >= 100` |
| `__lt` | Menor que | `filter(precio__lt=500)` | `WHERE precio < 500` |
| `__lte` | Menor o igual que | `filter(precio__lte=500)` | `WHERE precio <= 500` |
| `__in` | Está en una lista | `filter(id__in=[1, 5, 9])` | `WHERE id IN (1, 5, 9)` |
| `__range` | Está en un rango | `filter(precio__range=(100, 500))` | `WHERE precio BETWEEN 100 AND 500` |
| `__isnull` | Es NULL (o no) | `filter(categoria__isnull=True)` | `WHERE categoria_id IS NULL` |
| `__date` | La parte de fecha de un DateTime | `filter(fecha__date='2025-03-16')` | `WHERE DATE(fecha) = '2025-03-16'` |
| `__year` | El año de una fecha | `filter(fecha__year=2025)` | `WHERE EXTRACT(YEAR FROM fecha) = 2025` |

### Ejemplos prácticos

```python
# Productos entre $50 y $300
Producto.objects.filter(precio__range=(50, 300))

# Productos cuyo nombre contiene "bluetooth" (sin importar mayúsculas)
Producto.objects.filter(nombre__icontains='bluetooth')

# Productos creados en 2025
Producto.objects.filter(fecha_creacion__year=2025)

# Productos con stock entre 1 y 50 unidades
Producto.objects.filter(stock__range=(1, 50))

# Productos cuyo ID está en una lista específica
ids_promocion = [3, 7, 15, 22]
Producto.objects.filter(id__in=ids_promocion)
```

---

## Uso 2: Cruzar relaciones

El `__` también permite **navegar de un modelo a otro** en la consulta:

```python
# Desde Producto → cruzar a Categoria → filtrar por nombre de categoría
Producto.objects.filter(categoria__nombre='Telescopios')
# SQL: SELECT * FROM tienda_producto
#      INNER JOIN tienda_categoria ON ...
#      WHERE tienda_categoria.nombre = 'Telescopios'

# Se pueden combinar: cruzar relación + lookup
Producto.objects.filter(categoria__nombre__icontains='tele')
# → Productos cuya categoría contenga "tele" en el nombre (sin importar mayúsculas)

# Desde Categoria → cruzar a Producto → filtrar por precio del producto
Categoria.objects.filter(productos__precio__gte=1000).distinct()
# → Categorías que tienen al menos un producto de $1000 o más
```

> 💡 **Clave:** Puedes encadenar tantos `__` como niveles de relación necesites. Si tu modelo tiene `Pedido → ItemPedido → Producto → Categoria`, puedes escribir:
> ```python
> Pedido.objects.filter(items__producto__categoria__nombre='Telescopios')
> ```
> Django resuelve todos los JOINs automáticamente.
>
> *Fuente: Django Software Foundation. (2024). Field lookups.* [https://docs.djangoproject.com/en/stable/ref/models/querysets/#field-lookups](https://docs.djangoproject.com/en/stable/ref/models/querysets/#field-lookups)

---

---

# ⛓️ 5. Encadenar Consultas: El Superpoder del ORM

---

Esta es la técnica que más van a usar en la vida real. Un QuerySet se puede encadenar con otros métodos, y Django acumula todo en una sola consulta SQL.

### Ejemplo paso a paso

```python
# Empezamos con TODOS los productos
qs = Producto.objects.all()

# Filtramos: solo los activos
qs = qs.filter(activo=True)

# Filtramos más: que tengan stock disponible
qs = qs.filter(stock__gt=0)

# Excluimos: que NO sean de la categoría "Liquidación"
qs = qs.exclude(categoria__nombre='Liquidación')

# Ordenamos: los más caros primero
qs = qs.order_by('-precio')

# Limitamos: solo los primeros 10
qs = qs[:10]
```

**¿Cuántas consultas SQL se hicieron?** **Cero.** Todavía ninguna. Todas esas líneas solo describieron lo que queremos. La consulta se ejecuta cuando iteramos:

```python
for p in qs:   # ← AQUÍ Django ejecuta 1 sola consulta
    print(f"{p.nombre}: ${p.precio}")
```

El SQL generado es:

```sql
SELECT * FROM tienda_producto
WHERE activo = TRUE
  AND stock > 0
  AND NOT (categoria_id IN (
      SELECT id FROM tienda_categoria WHERE nombre = 'Liquidación'
  ))
ORDER BY precio DESC
LIMIT 10
```

### La forma compacta (una sola línea)

Todo lo anterior se puede escribir en una sola cadena:

```python
top_10 = (Producto.objects
    .filter(activo=True, stock__gt=0)
    .exclude(categoria__nombre='Liquidación')
    .order_by('-precio')
    [:10]
)
```

Ambas formas hacen exactamente lo mismo. La forma paso a paso es más legible cuando la consulta es compleja. La forma compacta es más concisa.

---

---

# 🎯 6. Métodos que Devuelven UN Solo Objeto

---

Estos métodos **no devuelven un QuerySet** — devuelven un solo objeto o un solo valor. Es importante distinguirlos porque se comportan diferente.

### `.get(**kwargs)` — Obtener exactamente UN registro

```python
# Buscar un producto por su ID
producto = Producto.objects.get(id=5)
# SQL: SELECT * FROM tienda_producto WHERE id = 5 LIMIT 1

# Buscar una categoría por nombre
cat = Categoria.objects.get(nombre='Telescopios')
```

**⚠️ Cuidado:** `.get()` lanza excepciones en dos casos:

```python
# Si NO encuentra nada → DoesNotExist
try:
    p = Producto.objects.get(id=9999)
except Producto.DoesNotExist:
    print("Ese producto no existe")

# Si encuentra MÁS DE UNO → MultipleObjectsReturned
try:
    p = Producto.objects.get(activo=True)   # Muchos productos son activos
except Producto.MultipleObjectsReturned:
    print("Hay más de un producto activo — usa filter() en vez de get()")
```

**Regla:** Usa `.get()` solo cuando buscas por un campo **único** (como `id`, `email`, `username`). Para todo lo demás, usa `.filter()`.

---

### `.first()` y `.last()` — El primero o el último

```python
# El producto más caro
mas_caro = Producto.objects.order_by('-precio').first()
# SQL: SELECT * FROM tienda_producto ORDER BY precio DESC LIMIT 1

# El producto más reciente
ultimo = Producto.objects.order_by('-id').first()

# El producto más antiguo
primero = Producto.objects.order_by('id').first()
```

A diferencia de `.get()`, estos métodos devuelven `None` si no hay resultados — no lanzan excepción.

---

### `.create(**kwargs)` — Crear un registro y guardarlo de una sola vez

```python
# Forma larga (dos pasos):
p = Producto(nombre='Lente Gran Angular', precio=299.99, stock=15, categoria=cat)
p.save()

# Forma corta (un paso):
p = Producto.objects.create(
    nombre='Lente Gran Angular',
    precio=299.99,
    stock=15,
    categoria=cat,
)
# → Crea el objeto Y lo guarda en la BD inmediatamente
```

---

### `.get_or_create(**kwargs)` — Buscar o crear si no existe

```python
cat, creada = Categoria.objects.get_or_create(nombre='Accesorios')
# Si la categoría "Accesorios" ya existe → la devuelve, creada = False
# Si NO existe → la crea, creada = True
```

Muy útil en scripts de carga de datos y migraciones.

---

### `.update_or_create(**kwargs)` — Actualizar o crear

```python
perfil, creado = PerfilCliente.objects.update_or_create(
    usuario=user,                          # Busca por este campo
    defaults={                             # Si existe, actualiza estos campos
        'ciudad': 'Santiago',
        'puntos_lealtad': 100,
    }
)
```

---

---

# 📊 7. Contar, Verificar y Agregar Sin Cargar Datos

---

Estos métodos son fundamentales para la eficiencia. La regla general: **si no necesitas los objetos, no los cargues.**

### `.count()` — Cuántos hay

```python
total = Producto.objects.filter(activo=True).count()
# SQL: SELECT COUNT(*) FROM tienda_producto WHERE activo = TRUE
# Devuelve: 47  (un número, no objetos)
```

**¿Por qué no usar `len()`?** Porque `len()` primero carga TODOS los objetos en memoria y después los cuenta. `.count()` le pide a la BD que cuente — sin traer ningún objeto.

```python
# ❌ Carga 10,000 objetos en memoria solo para contarlos
total = len(Producto.objects.all())

# ✅ La BD cuenta y devuelve solo un número
total = Producto.objects.count()
```

---

### `.exists()` — ¿Hay al menos uno?

```python
hay_stock = Producto.objects.filter(stock__gt=0).exists()
# SQL: SELECT 1 FROM tienda_producto WHERE stock > 0 LIMIT 1
# Devuelve: True o False
```

Es la forma más eficiente de verificar si algo existe. Más rápido que `.count() > 0` porque se detiene en el primer resultado.

---

### `.aggregate()` — Cálculos sobre toda la tabla

```python
from django.db.models import Avg, Max, Min, Sum, Count

# Precio promedio de todos los productos
Producto.objects.aggregate(promedio=Avg('precio'))
# Devuelve: {'promedio': Decimal('245.50')}

# Múltiples cálculos a la vez
Producto.objects.aggregate(
    precio_promedio=Avg('precio'),
    precio_maximo=Max('precio'),
    precio_minimo=Min('precio'),
    total_stock=Sum('stock'),
    cantidad_productos=Count('id'),
)
# Devuelve: {'precio_promedio': ..., 'precio_maximo': ..., ...}
```

> `.aggregate()` devuelve un **diccionario**, no un QuerySet. Es un resultado final — no se puede encadenar más.

---

---

# 📑 8. Ordenar, Limitar y Paginar

---

### Ordenar

```python
# Ascendente (por defecto)
Producto.objects.order_by('precio')

# Descendente
Producto.objects.order_by('-precio')

# Múltiple: primero por categoría, después por precio descendente
Producto.objects.order_by('categoria__nombre', '-precio')

# Aleatorio (útil para mostrar productos "destacados" al azar)
Producto.objects.order_by('?')[:5]
# ⚠️ Cuidado: order_by('?') es lento en tablas grandes
```

### Limitar (slicing)

```python
# Los primeros 5 productos
Producto.objects.all()[:5]
# SQL: SELECT * FROM tienda_producto LIMIT 5

# Del producto 10 al 20 (para paginación manual)
Producto.objects.all()[10:20]
# SQL: SELECT * FROM tienda_producto LIMIT 10 OFFSET 10

# El tercer producto (índice 2)
Producto.objects.all()[2]
# SQL: SELECT * FROM tienda_producto LIMIT 1 OFFSET 2
```

> 💡 El slicing en QuerySets **NO carga todos los objetos primero**. Django traduce los índices directamente a `LIMIT` y `OFFSET` en SQL.

---

---

# 🧮 9. Anotaciones: Columnas Calculadas

---

`.annotate()` le agrega columnas extra a cada registro del resultado. Estas columnas no existen en la tabla — se calculan en el momento de la consulta.

### Ejemplo: contar productos por categoría

```python
from django.db.models import Count

categorias = Categoria.objects.annotate(
    total_productos=Count('productos')
)

for cat in categorias:
    print(f"{cat.nombre}: {cat.total_productos} productos")
    # Telescopios: 12 productos
    # Accesorios: 8 productos
    # Mapas Estelares: 3 productos
```

Django genera:

```sql
SELECT tienda_categoria.*, COUNT(tienda_producto.id) AS total_productos
FROM tienda_categoria
LEFT JOIN tienda_producto ON ...
GROUP BY tienda_categoria.id
```

### Ejemplo: calcular el valor total del stock por producto

```python
from django.db.models import F

productos = Producto.objects.annotate(
    valor_stock=F('precio') * F('stock')
)

for p in productos:
    print(f"{p.nombre}: ${p.valor_stock} en inventario")
    # Telescopio X: $11,999.80 en inventario
    # Teclado Mecánico: $4,500.00 en inventario
```

`F()` hace referencia al valor de un campo **dentro de la misma fila**. Permite hacer cálculos entre columnas sin traer los datos a Python.

### Ejemplo: filtrar por la anotación

Lo poderoso de `.annotate()` es que la columna calculada se puede usar en `.filter()` y `.order_by()`:

```python
# Categorías con más de 5 productos, ordenadas de más a menos
Categoria.objects.annotate(
    total=Count('productos')
).filter(
    total__gt=5
).order_by('-total')
```

> *Fuente: Django Software Foundation. (2024). Aggregation — annotate().* [https://docs.djangoproject.com/en/stable/topics/db/aggregation/](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)

---

---

# 🧩 10. Consultas Complejas con Q Objects

---

Cuando necesitas condiciones con **OR** o **negaciones complejas**, los kwargs de `.filter()` no alcanzan — porque siempre combinan con AND. Para eso existen los `Q Objects`.

### El problema

```python
# Esto busca productos activos Y con stock > 0 (AND)
Producto.objects.filter(activo=True, stock__gt=0)

# Pero ¿cómo busco productos activos O con stock > 0? (OR)
# No hay forma de hacerlo solo con kwargs
```

### La solución: Q()

```python
from django.db.models import Q

# OR: productos activos O con stock > 0
Producto.objects.filter(Q(activo=True) | Q(stock__gt=0))
# SQL: WHERE activo = TRUE OR stock > 0

# AND (también se puede hacer con Q, aunque kwargs ya lo permite)
Producto.objects.filter(Q(activo=True) & Q(stock__gt=0))
# SQL: WHERE activo = TRUE AND stock > 0

# NOT: productos que NO están activos
Producto.objects.filter(~Q(activo=True))
# SQL: WHERE NOT (activo = TRUE)
```

### Combinaciones complejas

```python
# Productos que: (estén activos Y tengan stock) O (sean de la categoría "Ofertas")
Producto.objects.filter(
    (Q(activo=True) & Q(stock__gt=0)) | Q(categoria__nombre='Ofertas')
)
# SQL: WHERE (activo = TRUE AND stock > 0) OR categoria_id IN (
#          SELECT id FROM tienda_categoria WHERE nombre = 'Ofertas'
#      )
```

### Búsqueda dinámica (caso real)

En una vista con un buscador, el usuario puede escribir cualquier cosa. Necesitas buscar en múltiples campos a la vez:

```python
def buscar_productos(request):
    query = request.GET.get('q', '')

    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |            # Busca en el nombre
            Q(categoria__nombre__icontains=query) |  # Busca en la categoría
            Q(descripcion__icontains=query)          # Busca en la descripción
        ).distinct()
    else:
        productos = Producto.objects.all()

    return render(request, 'productos/buscar.html', {'productos': productos})
```

> *Fuente: Django Software Foundation. (2024). Complex lookups with Q objects.* [https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects](https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects)

---

---

# 🏢 11. Patrones Reales: Consultas de Tu Primer Trabajo

---

Estas son consultas que vas a escribir en proyectos reales. Cada una resuelve un problema de negocio concreto.

### 📋 Dashboard: métricas del negocio

```python
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

# Métricas del día de hoy
hoy = timezone.now().date()

metricas = {
    'total_productos': Producto.objects.count(),
    'productos_activos': Producto.objects.filter(activo=True).count(),
    'sin_stock': Producto.objects.filter(stock=0, activo=True).count(),
    'valor_inventario': Producto.objects.aggregate(
        total=Sum(F('precio') * F('stock'))
    )['total'],
    'precio_promedio': Producto.objects.aggregate(
        promedio=Avg('precio')
    )['promedio'],
}
```

### 🔍 Buscador con múltiples criterios

```python
def listado_productos(request):
    qs = Producto.objects.select_related('categoria').filter(activo=True)

    # Filtro por búsqueda de texto
    q = request.GET.get('q')
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) | Q(categoria__nombre__icontains=q)
        )

    # Filtro por rango de precio
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        qs = qs.filter(precio__gte=precio_min)
    if precio_max:
        qs = qs.filter(precio__lte=precio_max)

    # Filtro por categoría
    cat_id = request.GET.get('categoria')
    if cat_id:
        qs = qs.filter(categoria_id=cat_id)

    # Ordenamiento
    orden = request.GET.get('orden', '-precio')
    qs = qs.order_by(orden)

    return render(request, 'productos/listado.html', {
        'productos': qs,
        'categorias': Categoria.objects.all(),
    })
```

### 📊 Top 5 categorías con más productos

```python
top_categorias = (Categoria.objects
    .annotate(total=Count('productos'))
    .filter(total__gt=0)
    .order_by('-total')
    [:5]
)
```

### 🛒 Calcular total de un pedido (con modelo intermedio)

```python
from django.db.models import F, Sum

total_pedido = pedido.items.aggregate(
    total=Sum(F('cantidad') * F('precio_unidad'))
)['total']
```

### 📈 Productos más vendidos del mes

```python
from django.utils import timezone

inicio_mes = timezone.now().replace(day=1)

mas_vendidos = (Producto.objects
    .filter(en_pedidos__pedido__fecha__gte=inicio_mes)
    .annotate(total_vendido=Sum('en_pedidos__cantidad'))
    .order_by('-total_vendido')
    [:10]
)
```

---

---

# ⚠️ 12. Los 7 Errores Más Comunes con QuerySets

---

| # | Error | Código incorrecto | Código correcto |
|:---|:---|:---|:---|
| **1** | Usar `len()` en vez de `.count()` | `len(Producto.objects.all())` | `Producto.objects.count()` |
| **2** | Usar `if qs` en vez de `.exists()` | `if Producto.objects.filter(activo=True):` | `if Producto.objects.filter(activo=True).exists():` |
| **3** | Usar `.get()` sin manejar excepciones | `p = Producto.objects.get(id=9999)` | `try/except Producto.DoesNotExist` |
| **4** | Hacer queries en un loop (N+1) | `for p in productos: print(p.categoria.nombre)` | Usar `select_related('categoria')` antes del loop |
| **5** | Olvidar `.distinct()` en filtros inversos | `Categoria.objects.filter(productos__activo=True)` | Agregar `.distinct()` al final |
| **6** | Evaluar el QS múltiples veces | Usar el mismo QS sin cachear en variable | Guardar en variable: `resultado = list(qs)` |
| **7** | Filtrar en Python en vez de en la BD | `[p for p in Producto.objects.all() if p.precio > 100]` | `Producto.objects.filter(precio__gt=100)` |

### Sobre el error 7 — vale la pena profundizar

Este es el error más frecuente en desarrolladores que vienen de Python puro:

```python
# ❌ NUNCA hagas esto: trae TODOS los productos a Python y filtra uno por uno
productos_caros = []
for p in Producto.objects.all():       # ← Carga 10,000 objetos en memoria
    if p.precio > 1000:
        productos_caros.append(p)

# ✅ Deja que la BD haga el trabajo (es para lo que existe)
productos_caros = Producto.objects.filter(precio__gt=1000)
# ← La BD filtra y devuelve solo los que cumplen. Puede ser 50 en vez de 10,000.
```

La base de datos está **optimizada** para filtrar — tiene índices, planes de ejecución, y décadas de algoritmos perfeccionados. Python no. Siempre que puedas, empuja la lógica de filtrado **hacia la BD**.

---

---

## 📚 Tabla Resumen: QuerySet de un Vistazo

| Necesito... | Método | Devuelve |
|:---|:---|:---|
| Todos los registros | `.all()` | QuerySet |
| Filtrar por condición | `.filter(**kwargs)` | QuerySet |
| Excluir por condición | `.exclude(**kwargs)` | QuerySet |
| Ordenar | `.order_by(*fields)` | QuerySet |
| Solo ciertas columnas | `.values()` / `.values_list()` | QuerySet de dicts/tuplas |
| Sin duplicados | `.distinct()` | QuerySet |
| Un solo objeto por ID | `.get(**kwargs)` | Objeto (o excepción) |
| El primero del QuerySet | `.first()` | Objeto o None |
| Crear y guardar | `.create(**kwargs)` | Objeto creado |
| Buscar o crear | `.get_or_create(**kwargs)` | (Objeto, bool) |
| Contar | `.count()` | int |
| ¿Existe alguno? | `.exists()` | bool |
| Cálculo global | `.aggregate()` | dict |
| Columna calculada | `.annotate()` | QuerySet con campo extra |
| Condiciones OR/NOT | `Q()` | Se usa dentro de filter() |
| Optimizar FK | `.select_related()` | QuerySet (1 consulta con JOIN) |
| Optimizar M2M | `.prefetch_related()` | QuerySet (2 consultas) |

---

## 📚 Bibliografía y Fuentes

- *Django Software Foundation. (2024). QuerySet API reference.* [https://docs.djangoproject.com/en/stable/ref/models/querysets/](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- *Django Software Foundation. (2024). Making queries.* [https://docs.djangoproject.com/en/stable/topics/db/queries/](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- *Django Software Foundation. (2024). Aggregation.* [https://docs.djangoproject.com/en/stable/topics/db/aggregation/](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)
- *Django Software Foundation. (2024). Database access optimization.* [https://docs.djangoproject.com/en/stable/topics/db/optimization/](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

---
