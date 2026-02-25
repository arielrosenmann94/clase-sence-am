# 📘 Informe Completo: ORM vs SQL (Django)

## 1. Introducción

En el contexto de Django, cuando hablamos de **ORM** nos referimos a:

**ORM = Object-Relational Mapping** (Mapeo Objeto-Relacional)

A veces, por error tipográfico, se escribe “ROM”, pero en desarrollo web con Django el término correcto es **ORM**.

### ¿Qué hace el ORM?

El ORM permite trabajar con la base de datos usando **Python** en lugar de escribir SQL manualmente para cada operación.

En vez de pensar únicamente en tablas, filas y columnas, el desarrollador trabaja con:

- **clases** (modelos),
- **objetos** (registros),
- **atributos** (campos),
- **métodos** (operaciones sobre esos datos).

---

## Mini glosario rápido (Django ORM)

- **ORM**: Object-Relational Mapping. Escribes Python y Django lo traduce a SQL.
- **Modelo**: clase Python que representa una tabla (ej: `Producto` → `productos_producto`).
- **QuerySet**: objeto que representa una consulta. Es “perezoso” (lazy) y se evalúa cuando lo usas.
- **Lookup**: sufijo después de `__` que define cómo comparar (`icontains`, `lt`, `in`, `range`, etc.).
- **`objects`**: administrador que expone métodos de consulta (`all`, `filter`, `get`, `create`, `update`, `delete`).
- **`get_object_or_404`**: helper que busca y devuelve 404 si no encuentra.
- **`select_related` / `prefetch_related`**: optimizan consultas con relaciones (evitan N+1).
- **`qs.query`**: muestra el SQL aproximado que Django generaría para un QuerySet.

---

## 2. ¿Qué es SQL?

**SQL** (Structured Query Language) es el lenguaje estándar para trabajar con bases de datos relacionales.

Con SQL puedes:

- consultar datos (`SELECT`)
- insertar datos (`INSERT`)
- actualizar datos (`UPDATE`)
- eliminar datos (`DELETE`)
- unir tablas (`JOIN`)
- agrupar y calcular (`GROUP BY`, `COUNT`, `SUM`, etc.)

Ejemplo SQL:

```sql
SELECT nombre, precio
FROM productos_producto
WHERE disponible = true
ORDER BY precio DESC;
```

---

## 3. Diferencia conceptual: ORM vs SQL

### SQL (nivel base de datos)

Con SQL escribes **instrucciones** directas para el motor de base de datos.

- Piensas en tablas
- Piensas en columnas
- Piensas en joins y sintaxis SQL

### ORM (nivel aplicación)

Con ORM escribes **código Python** que Django traduce a SQL.

- Piensas en modelos (`Producto`)
- Piensas en objetos (`producto`)
- Piensas en métodos y QuerySets

### Idea importante

El ORM **no reemplaza** SQL: lo **genera** por ti.

Por eso, para usar bien el ORM, conviene entender SQL.

---

## 4. Cómo se escribe ORM en Django (forma básica)

Supongamos este modelo:

```python
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
```

Con este modelo, Django crea una tabla (por ejemplo):

- `productos_producto`

Y cada campo del modelo se convierte en una columna de esa tabla.

---

## 5. Mapeo: Modelo Django -> Tabla SQL

| Django (Python) | SQL (BD relacional) |
| --- | --- |
| `class Producto(models.Model)` | Tabla `productos_producto` |
| `nombre = models.CharField(...)` | Columna tipo texto/varchar |
| `precio = models.DecimalField(...)` | Columna decimal/numeric |
| `disponible = models.BooleanField(...)` | Columna boolean |
| `id` (automático) | Clave primaria (`PRIMARY KEY`) |
| instancia `Producto(...)` | Fila (registro) |

---

## 6. Comparación práctica: ORM vs SQL (operaciones comunes)

## 6.1 Obtener todos los registros

### Django ORM

```python
productos = Producto.objects.all()
```

### SQL equivalente (conceptual)

```sql
SELECT * FROM productos_producto;
```

### Cómo interpretarlo

- `Producto.objects` = punto de entrada al ORM para ese modelo
- `.all()` = “trae todos los registros”
- Resultado: un **QuerySet** (no una lista simple inmediata)

---

## 6.2 Filtrar por una condición (`WHERE`)

### Django ORM

```python
disponibles = Producto.objects.filter(disponible=True)
```

### SQL equivalente

```sql
SELECT *
FROM productos_producto
WHERE disponible = true;
```

### Interpretación

- `.filter(...)` agrega condiciones
- `disponible=True` se traduce a `WHERE disponible = true`
- Devuelve múltiples resultados (posiblemente 0)

---

## 6.3 Obtener un registro específico

### Django ORM

```python
producto = Producto.objects.get(id=5)
```

### SQL equivalente

```sql
SELECT *
FROM productos_producto
WHERE id = 5;
```

### Interpretación

- `.get(...)` espera **un solo resultado**
- Si no existe, Django lanza excepción (`DoesNotExist`)
- Si hay más de uno (en campos no únicos), lanza `MultipleObjectsReturned`

> En vistas, suele ser más cómodo usar `get_object_or_404(...)`.

---

## 6.4 Búsqueda parcial (`LIKE` / `ILIKE`)

### Django ORM

```python
resultados = Producto.objects.filter(nombre__icontains='cafe')
```

#### Desglose de `nombre__icontains`

- `nombre` = nombre del campo en el modelo.
- `__` (doble guion bajo) = separador entre el campo y el **lookup**.
- `icontains` = “contiene” sin distinguir mayúsculas/minúsculas (i = insensitive).
  - Equivale a `ILIKE` en bases de datos que lo soportan.
  - Variante sensible a mayúsculas: `contains`.
  - Variante exacta: `iexact` (case-insensitive) o `exact` (case-sensitive).

### SQL equivalente (aproximado)

```sql
SELECT *
FROM productos_producto
WHERE nombre ILIKE '%cafe%';
```

### Interpretación

- `nombre__icontains` significa:
  - campo `nombre`
  - búsqueda “contiene”
  - sin distinguir mayúsculas/minúsculas (`i` = case-insensitive)
- El doble guion bajo `__` separa:
  - **campo** + **lookup** (tipo de comparación)

#### Variantes útiles del mismo patrón

- `nombre__startswith='ca'` → `LIKE 'ca%'` (sensitivo a mayúsculas).
- `nombre__istartswith='ca'` → `ILIKE 'ca%'` (insensitivo a mayúsculas).
- `nombre__endswith='fe'` / `nombre__iendswith='fe'`.
- `descripcion__regex='^Promo'` → expresión regular (según motor).

---

## 6.5 Ordenar resultados (`ORDER BY`)

### Django ORM

```python
productos = Producto.objects.order_by('precio')
```

### SQL equivalente

```sql
SELECT *
FROM productos_producto
ORDER BY precio ASC;
```

### Descendente

```python
productos = Producto.objects.order_by('-precio')
```

```sql
SELECT *
FROM productos_producto
ORDER BY precio DESC;
```

### Interpretación

- `'precio'` = ascendente
- `'-precio'` = descendente

---

## 6.6 Limitar resultados (`LIMIT`)

### Django ORM

```python
top_5 = Producto.objects.order_by('-creado_en')[:5]
```

### SQL equivalente

```sql
SELECT *
FROM productos_producto
ORDER BY creado_en DESC
LIMIT 5;
```

### Interpretación

- El slicing `[:5]` en QuerySets se traduce a `LIMIT`
- No es una lista de Python común; Django lo traduce a SQL

---

## 6.7 Insertar (`INSERT`)

### Opción A — Crear y guardar

```python
p = Producto(
    nombre='Taza térmica',
    precio=12990,
    descuento=10,
    disponible=True,
)
p.save()
```

### SQL equivalente (conceptual)

```sql
INSERT INTO productos_producto (nombre, precio, descuento, disponible, descripcion, creado_en)
VALUES ('Taza térmica', 12990, 10, true, '', NOW());
```

### Opción B — `create()`

```python
p = Producto.objects.create(
    nombre='Taza térmica',
    precio=12990,
    descuento=10,
    disponible=True,
)
```

### Interpretación

- `.create(...)` construye el objeto y lo guarda en una sola operación
- `save()` permite más control si quieres modificar algo antes de guardar

---

## 6.8 Actualizar (`UPDATE`)

### Django ORM (objeto individual)

```python
p = Producto.objects.get(id=5)
p.descuento = 25
p.save()
```

### SQL equivalente

```sql
UPDATE productos_producto
SET descuento = 25
WHERE id = 5;
```

### Django ORM (update directo en QuerySet)

```python
Producto.objects.filter(disponible=False).update(descuento=0)
```

### SQL equivalente

```sql
UPDATE productos_producto
SET descuento = 0
WHERE disponible = false;
```

### Interpretación

- `.save()` trabaja sobre una instancia
- `.update(...)` trabaja a nivel de consulta (más eficiente para lotes)

---

## 6.9 Eliminar (`DELETE`)

### Django ORM (instancia)

```python
p = Producto.objects.get(id=5)
p.delete()
```

### SQL equivalente

```sql
DELETE FROM productos_producto
WHERE id = 5;
```

### Django ORM (QuerySet)

```python
Producto.objects.filter(disponible=False).delete()
```

### SQL equivalente

```sql
DELETE FROM productos_producto
WHERE disponible = false;
```

---

## 6.10 Contar registros (`COUNT`)

### Django ORM

```python
total = Producto.objects.count()
```

### SQL equivalente

```sql
SELECT COUNT(*)
FROM productos_producto;
```

### Interpretación

- `.count()` hace el cálculo en la base de datos
- Mejor que traer todos los registros y usar `len(...)`

---

## 7. Lookups en Django ORM (cómo leerlos)

Los **lookups** son sufijos que Django usa para traducir comparaciones a SQL.

Se escriben con doble guion bajo `__`.

### Sintaxis general

```python
Modelo.objects.filter(campo__lookup=valor)
```

### Ejemplos comunes

| ORM | Significado | SQL aproximado |
| --- | --- | --- |
| `precio__lt=100` | menor que | `precio < 100` |
| `precio__lte=100` | menor o igual | `precio <= 100` |
| `precio__gt=100` | mayor que | `precio > 100` |
| `precio__gte=100` | mayor o igual | `precio >= 100` |
| `nombre__contains='a'` | contiene | `LIKE '%a%'` |
| `nombre__icontains='a'` | contiene (sin distinguir mayús/minús) | `ILIKE '%a%'` |
| `id__in=[1,2,3]` | está dentro de lista | `IN (1,2,3)` |
| `descuento__isnull=True` | es nulo | `IS NULL` |

#### Notas rápidas sobre lookups

- `contains` vs `icontains`: `icontains` no diferencia mayúsculas/minúsculas.
- `exact` vs `iexact`: igualdad estricta vs igualdad sin distinguir mayúsculas.
- Rangos: `precio__range=(1000, 5000)` → `BETWEEN 1000 AND 5000`.
- Fechas: `creado_en__date=fecha` filtra por solo la fecha (omite hora).
- Booleanos: usa `True`/`False` en ORM; en SQL será `1/0` o `true/false` según motor.

### Ejemplo combinado

```python
Producto.objects.filter(disponible=True, precio__lt=20000)
```

SQL aproximado:

```sql
SELECT *
FROM productos_producto
WHERE disponible = true AND precio < 20000;
```

---

## 8. Relaciones: cómo el ORM reemplaza JOINs explícitos

Uno de los mayores beneficios del ORM aparece cuando hay relaciones entre tablas.

Supongamos:

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
```

### 8.1 Acceder a la relación (join implícito en Python)

```python
p = Producto.objects.get(id=1)
print(p.categoria.nombre)
```

### Qué pasa conceptualmente

Django resuelve la relación entre `Producto` y `Categoria` usando la clave foránea.

### SQL aproximado (conceptual)

```sql
SELECT p.*, c.nombre
FROM productos_producto p
JOIN productos_categoria c ON p.categoria_id = c.id
WHERE p.id = 1;
```

> En la práctica, Django puede hacer más de una consulta si no optimizas (ver `select_related`).

---

## 9. QuerySet: qué es y cómo se interpreta

Un **QuerySet** es un objeto de Django que representa una consulta a la base de datos.

### Importante para entender el ORM

Un QuerySet generalmente es:

- **perezoso** (lazy)
- **encadenable**
- **traducible a SQL**

### Ejemplo encadenado

```python
qs = Producto.objects.filter(disponible=True).order_by('-precio')[:10]
```

Esto Django lo interpreta como una sola consulta SQL equivalente a:

```sql
SELECT *
FROM productos_producto
WHERE disponible = true
ORDER BY precio DESC
LIMIT 10;
```

### ¿Qué significa “lazy”?

Django no siempre ejecuta la consulta inmediatamente cuando escribes el QuerySet.
La ejecuta cuando realmente necesita los datos, por ejemplo cuando:

- iteras (`for p in qs`)
- conviertes a lista (`list(qs)`)
- renderizas en un template
- llamas `count()`, `exists()`, etc.

> Truco práctico: si dudas, imprime `qs.query` para ver el SQL que generaría y así confirmar que tu cadena de lookups quedó bien.

---

## 10. Cómo ver el SQL que genera el ORM (muy útil para aprender)

Aprender ORM es mucho más fácil si miras el SQL que Django genera.

### Opción 1 — Imprimir la consulta de un QuerySet

```python
qs = Producto.objects.filter(nombre__icontains='cafe').order_by('-precio')
print(qs.query)
```

Esto muestra una representación SQL (aproximada) de la consulta.

### Opción 2 — Django Debug Toolbar (en proyectos de desarrollo)

En desarrollo, herramientas como **Django Debug Toolbar** permiten ver:

- cuántas consultas se ejecutaron
- qué SQL exacto se ejecutó
- cuánto tardó cada una

> Para un curso inicial, `print(qs.query)` ya es excelente para aprender.

---

## 11. ORM y SQL: ventajas y desventajas (comparación realista)

## 11.1 Ventajas del ORM

### 1. Más productivo para CRUD

Para operaciones comunes (crear, listar, filtrar, editar, eliminar), el ORM es más rápido de escribir y mantener.

### 2. Código más legible para el equipo Python

El código queda en el mismo lenguaje de la aplicación (Python), sin saltar de contexto constantemente.

### 3. Menos repetición

Los modelos centralizan estructura y lógica de datos.

### 4. Seguridad (si se usa bien)

El ORM ayuda a evitar errores comunes al construir SQL manual, especialmente en consultas con parámetros.

### 5. Portabilidad entre motores

El mismo código ORM puede funcionar con SQLite, PostgreSQL, MySQL, etc. (con matices).

---

## 11.2 Desventajas / límites del ORM

### 1. No reemplaza entender SQL

Si no entiendes SQL, te costará optimizar consultas y depurar problemas de rendimiento.

### 2. Consultas complejas pueden ser difíciles de leer

Para ciertos reportes o joins avanzados, SQL manual puede ser más claro.

### 3. Riesgo de escribir consultas ineficientes sin darte cuenta

Ejemplo típico: problema **N+1 queries**.

### 4. A veces necesitas SQL crudo

Para:

- consultas muy específicas
- funciones nativas del motor
- optimizaciones avanzadas
- migraciones o scripts especiales

---

## 12. Cómo “traducir mentalmente” ORM -> SQL (método para estudiantes)

Cuando veas una consulta ORM, interprétala en este orden:

1. **¿Qué modelo?** -> tabla principal
2. **¿Qué método?** (`all`, `filter`, `get`, `order_by`, `count`, `update`, etc.)
3. **¿Qué condiciones?** -> `WHERE`
4. **¿Hay orden?** -> `ORDER BY`
5. **¿Hay límite?** -> `LIMIT`
6. **¿Devuelve uno o muchos?** -> `get()` vs `filter()`

### Ejemplo guiado

ORM:

```python
Producto.objects.filter(disponible=True, nombre__icontains='taza').order_by('-precio')[:3]
```

Lectura mental:

- tabla `productos_producto`
- `WHERE disponible = true`
- `AND nombre ILIKE '%taza%'`
- `ORDER BY precio DESC`
- `LIMIT 3`

SQL equivalente:

```sql
SELECT *
FROM productos_producto
WHERE disponible = true
  AND nombre ILIKE '%taza%'
ORDER BY precio DESC
LIMIT 3;
```

---

## 13. Errores comunes al aprender ORM (y cómo evitarlos)

### Error 1 — Confundir `get()` con `filter()`

- `get()` -> un resultado
- `filter()` -> varios resultados (QuerySet)

### Error 2 — Pensar que `QuerySet` es una lista normal

Se parece, pero Django lo traduce a SQL y lo evalúa cuando hace falta.

### Error 3 — Poner lógica de negocio en el template

Si repites cálculos en HTML, esa lógica debería estar en el modelo.

### Error 4 — No revisar el SQL generado

Para aprender y depurar, `print(qs.query)` ayuda muchísimo.

### Error 5 — No optimizar relaciones

Cuando uses relaciones (`ForeignKey`, `ManyToMany`), aprende más adelante:

- `select_related()`
- `prefetch_related()`

Esto evita consultas innecesarias.

---

## 14. ¿Cuándo usar ORM y cuándo SQL en un proyecto real?

### Usa ORM (la mayoría del tiempo)

- CRUD habitual
- formularios
- vistas de listados y detalle
- filtros y búsquedas comunes
- trabajo diario en Django

### Usa SQL (o SQL crudo) cuando realmente lo necesites

- reportes muy complejos
- optimización avanzada
- consultas específicas del motor de BD
- análisis o scripts de datos

> En Django profesional, lo normal es usar **ORM como primera opción** y SQL cuando hay una razón técnica clara.

---

## 15. Resumen final (para estudiantes)

- **ORM** se escribe **ORM**, no “ROM” en este contexto.
- El ORM de Django te permite escribir consultas usando Python.
- Django traduce esas consultas a SQL.
- Aprender ORM es más fácil si entiendes cómo se ve su equivalente en SQL.
- Entender SQL te ayuda a usar mejor el ORM.
- Entender ambos te convierte en mejor programador/a Django.

---

## 16. Mini tabla de referencia rápida (ORM -> SQL)

| Django ORM | SQL (aproximado) |
| --- | --- |
| `Producto.objects.all()` | `SELECT * FROM productos_producto;` |
| `Producto.objects.get(id=1)` | `SELECT * FROM productos_producto WHERE id = 1;` |
| `Producto.objects.filter(disponible=True)` | `SELECT * FROM productos_producto WHERE disponible = true;` |
| `Producto.objects.order_by('-precio')` | `SELECT * FROM productos_producto ORDER BY precio DESC;` |
| `Producto.objects.count()` | `SELECT COUNT(*) FROM productos_producto;` |
| `Producto.objects.create(...)` | `INSERT INTO ...` |
| `p.save()` (objeto existente) | `UPDATE ... WHERE id = ...` |
| `p.delete()` | `DELETE FROM ... WHERE id = ...` |

---

## 17. Ejercicio sugerido para practicar (opcional)

Toma estas consultas ORM y escribe su equivalente SQL aproximado:

1. `Producto.objects.filter(precio__lt=10000)`
2. `Producto.objects.filter(nombre__icontains='mate').order_by('nombre')`
3. `Producto.objects.filter(disponible=True).count()`
4. `Producto.objects.filter(id__in=[1, 3, 8])`

Luego verifica tus ideas con:

```python
print(Producto.objects.filter(precio__lt=10000).query)
```

> Este ejercicio entrena exactamente la habilidad que necesitas para dominar Django con criterio.
