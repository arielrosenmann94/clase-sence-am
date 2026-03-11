# 🗄️ Django — Módulo 7 · Clase 1

## Acceso a Datos con Django

### AE7.1 — Características fundamentales de la integración del framework Django con bases de datos

---

> _"El ORM de Django no reemplaza a la base de datos — la hace invisible en el lugar correcto."_

---

## ¿Qué vas a aprender hoy?

- 🔌 Cómo Django se conecta a motores de bases de datos
- 🗂️ Qué es el ORM y por qué es uno de los pilares del framework
- 📐 Cómo se definen modelos y por qué se convierten en tablas
- 🔄 Qué son las migraciones y qué problema resuelven
- 🔍 Cómo construir consultas con el ORM — simples y avanzadas
- ⚡ Qué es la evaluación diferida y por qué mejora el rendimiento
- 🧩 Qué son los Q Objects y cuándo se usan
- 🔗 Cómo optimizar consultas con relaciones entre modelos
- 🛢️ Cuándo y cómo ejecutar SQL directo en Django

---

---

# PARTE I — DJANGO Y LAS BASES DE DATOS

---

## 1. La capa de datos de Django

Django separa el proyecto en responsabilidades claras. Cada parte del sistema sabe solo lo que necesita saber para hacer su trabajo. La capa de datos es la que se ocupa exclusivamente de **persistir y recuperar información**.

El flujo de una solicitud completa muestra dónde vive cada responsabilidad:

```
Navegador → urls.py → views.py → models.py → Base de datos
```

Toda la lógica de datos vive en `models.py`. Las vistas no conocen SQL. Los templates no conocen la base de datos. Esa separación es intencional y tiene un nombre técnico: **desacoplamiento**. Un sistema desacoplado es un sistema donde cada parte puede cambiar sin romper las otras.

---

## 2. En qué archivos del proyecto está el ORM

Esta es una pregunta fundamental que muchos nuevos developers confunden.

El ORM de Django no vive en un solo lugar — se usa desde distintos archivos según la tarea:

| Archivo          | Qué parte del ORM se escribe ahí                                            |
| ---------------- | --------------------------------------------------------------------------- |
| `models.py`      | La **definición** del modelo — campos, relaciones, Meta, métodos            |
| `views.py`       | Las **consultas** — `filter()`, `get()`, `all()`, `create()`                |
| `admin.py`       | Consultas para el panel de administración — implícitas y a veces explícitas |
| `forms.py`       | El `ModelForm` usa el modelo para generar el formulario                     |
| `serializers.py` | En APIs REST, lee modelos para convertirlos a JSON                          |
| `signals.py`     | Accede al modelo para reaccionar a eventos de guardado o eliminación        |
| `shell`          | Consultas interactivas de prueba o carga de datos                           |
| `tests.py`       | Creación de datos de prueba y verificación de comportamientos               |

La forma más simple de recordarlo: **definis en `models.py`, consultás en `views.py`**.

---

## 3. Motores de bases de datos soportados

Django no está atado a una base de datos específica. Soporta múltiples motores relacionales de forma nativa a través de **drivers**. Un driver es el adaptador que traduce las instrucciones del ORM al dialecto SQL específico de cada motor.

| Motor          | Uso recomendado                      | Paquete necesario          |
| -------------- | ------------------------------------ | -------------------------- |
| **SQLite**     | Desarrollo local — sin configuración | Ninguno — viene con Python |
| **PostgreSQL** | Producción — el más recomendado      | `psycopg` (versión 3)      |
| **MySQL**      | Producción — ampliamente usado       | `mysqlclient`              |
| **Oracle**     | Entornos corporativos                | `cx_Oracle`                |

La gran ventaja de esta arquitectura es que **cambiar de SQLite a PostgreSQL no requiere modificar una sola línea de lógica de negocio**. Solo cambia la configuración de `DATABASES` en `settings.py`. Todo el código Python del proyecto sigue igual.

**Recomendación para Django 6:** Para proyectos nuevos, PostgreSQL con el driver `psycopg` versión 3. Es más rápido que la versión anterior, soporta consultas asíncronas y es completamente compatible con las capacidades async del framework.

---

## 4. La configuración de la conexión en `settings.py`

Toda configuración de base de datos vive en una sola variable llamada `DATABASES`. Los dos casos más comunes son:

**Para desarrollo local con SQLite:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite guarda toda la base de datos en un archivo local (`db.sqlite3`). No necesita servidor, usuario ni contraseña. Por eso es ideal para desarrollo.

**Para producción con PostgreSQL:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Los campos `USER`, `PASSWORD` y `HOST` apuntan al servidor PostgreSQL. En producción, la contraseña nunca se escribe directamente en el código — se lee desde una variable de entorno. El archivo `settings.py` sube al repositorio; las contraseñas, nunca.

---

---

# PARTE II — EL ORM DE DJANGO

---

## 5. ¿Qué es un ORM y por qué existe?

**ORM** significa _Object-Relational Mapping_ (Mapeo Objeto-Relacional). Es el sistema que convierte automáticamente entre Python y SQL.

El problema que resuelve es la **impedancia de paradigmas**: Python trabaja con objetos, y la base de datos trabaja con tablas y filas. Son dos formas distintas de pensar sobre los datos. Escribir SQL dentro de código Python rompe la separación de responsabilidades, mezcla dos lenguajes en el mismo archivo, y requiere escribir manualmente código repetitivo para cada operación.

El ORM elimina ese problema. Define los datos una sola vez en Python, y el framework genera el SQL correspondiente automáticamente.

Comparación directa entre SQL manual y ORM:

| Operación     | SQL manual                                       | Django ORM                                                 |
| ------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Obtener todos | `SELECT * FROM tienda_producto`                  | `Producto.objects.all()`                                   |
| Filtrar       | `SELECT * FROM ... WHERE precio > 100`           | `Producto.objects.filter(precio__gt=100)`                  |
| Obtener uno   | `SELECT * FROM ... WHERE id = 1`                 | `Producto.objects.get(id=1)`                               |
| Crear         | `INSERT INTO tienda_producto (...) VALUES (...)` | `Producto.objects.create(nombre='...', precio=99)`         |
| Actualizar    | `UPDATE tienda_producto SET ... WHERE id = 1`    | `p = Producto.objects.get(id=1); p.nombre='...'; p.save()` |
| Eliminar      | `DELETE FROM tienda_producto WHERE id = 1`       | `Producto.objects.get(id=1).delete()`                      |

Además de simplificar la sintaxis, el ORM protege automáticamente contra **inyección SQL** — uno de los ataques más comunes en aplicaciones web. El SQL generado por el ORM siempre escapa los valores de forma correcta.

---

## 6. Definición de modelos

Un **modelo** es una clase Python que describe la estructura de los datos. Cada atributo de la clase se convierte en una columna de la tabla. Django se encarga de generar el SQL para crear esa tabla.

**Ejemplo de un modelo completo:**

```python
from django.db import models

class Producto(models.Model):
    nombre    = models.CharField(max_length=100)
    precio    = models.DecimalField(max_digits=8, decimal_places=2)
    stock     = models.IntegerField(default=0)
    activo    = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
```

**¿Qué genera Django en la base de datos?**

Cuando se aplica la migración de este modelo, Django ejecuta automáticamente un `CREATE TABLE` equivalente a:

```sql
CREATE TABLE "tienda_producto" (
    "id"         bigint       NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "nombre"     varchar(100) NOT NULL,
    "precio"     decimal(8,2) NOT NULL,
    "stock"      integer      NOT NULL DEFAULT 0,
    "activo"     boolean      NOT NULL DEFAULT TRUE,
    "creado_en"  timestamptz  NOT NULL
);
```

El nombre de la tabla sigue el patrón `nombre_de_app_nombre_del_modelo`, todo en minúsculas. El campo `id` se crea automáticamente en todos los modelos sin necesidad de declararlo. En Django 3.2 en adelante, es un `BigAutoField` — entero de 64 bits que soporta hasta 9 quintillones de registros.

El método `__str__` no crea ninguna columna. Solo define cómo se representa el objeto como texto cuando Django necesita imprimirlo — en el admin, en el shell, en los logs.

---

## 7. Tipos de campo

Cada tipo de campo en Django corresponde a un tipo de dato en la base de datos. La elección del tipo correcto no es solo técnica: define qué datos son válidos, qué se puede buscar, y cómo se almacena la información.

| Campo                     | Tipo SQL         | Para qué se usa                           |
| ------------------------- | ---------------- | ----------------------------------------- |
| `CharField(max_length=n)` | VARCHAR(n)       | Texto corto con límite: nombres, títulos  |
| `TextField()`             | TEXT             | Texto largo sin límite: descripciones     |
| `IntegerField()`          | INTEGER          | Números enteros: cantidades, edades       |
| `DecimalField(md, dp)`    | DECIMAL(md, dp)  | Dinero — precisión exacta, sin errores    |
| `FloatField()`            | FLOAT            | Cálculos científicos — no para dinero     |
| `BooleanField()`          | BOOLEAN          | Estados: activo, publicado, verificado    |
| `DateField()`             | DATE             | Solo fecha: nacimiento, vencimiento       |
| `DateTimeField()`         | TIMESTAMP        | Fecha y hora: creación, última edición    |
| `EmailField()`            | VARCHAR          | Como CharField pero valida formato email  |
| `URLField()`              | VARCHAR          | Como CharField pero valida formato URL    |
| `SlugField()`             | VARCHAR          | URLs amigables: `mi-primer-producto`      |
| `JSONField()`             | JSONB / JSON     | Datos sin esquema fijo (Django 3.1+)      |
| `ForeignKey()`            | INTEGER (FK)     | Relación muchos-a-uno                     |
| `OneToOneField()`         | INTEGER (FK)     | Relación uno-a-uno: perfil de usuario     |
| `ManyToManyField()`       | Tabla intermedia | Relación muchos-a-muchos: tags, etiquetas |

**Nota importante sobre `DecimalField` vs `FloatField`**: Los números de punto flotante (`float`) tienen un error de representación binaria. `0.1 + 0.2` en Python no da exactamente `0.3`. Para precios y cualquier valor monetario siempre se usa `DecimalField`, que usa aritmética decimal de precisión exacta.

**Nota sobre `JSONField`**: Disponible desde Django 3.1, guarda datos JSON directamente en la base de datos. En PostgreSQL usa el tipo `JSONB` que permite búsquedas dentro del JSON. En otras bases usa `TEXT` con JSON serializado.

---

## 8. Opciones comunes en los campos

Todos los campos aceptan parámetros que refinan su comportamiento. Estas son las más usadas:

| Opción         | Qué hace                                        | Cuándo usarla                            |
| -------------- | ----------------------------------------------- | ---------------------------------------- |
| `default`      | Valor inicial si no se provee uno               | Campos con valor por defecto del negocio |
| `blank=True`   | Permite que el campo quede vacío en formularios | Campos opcionales para el usuario        |
| `null=True`    | Permite NULL en la base de datos                | Campos que pueden no tener valor         |
| `unique=True`  | No permite valores repetidos en la columna      | Emails, documentos de identidad, slugs   |
| `choices`      | Lista de valores válidos — una enumeración      | Cuando el campo tiene opciones fijas     |
| `verbose_name` | Nombre legible en el admin y formularios        | Para texto en español o más descriptivo  |
| `auto_now_add` | Asigna la fecha actual solo al crear el objeto  | Timestamps de creación                   |
| `auto_now`     | Actualiza la fecha cada vez que se guarda       | Timestamps de última modificación        |

La diferencia entre `blank` y `null` es sutil pero importante. `null=True` afecta la base de datos — permite que la columna no tenga valor. `blank=True` afecta la validación de formularios — permite que el campo del formulario quede vacío. Para campos de texto, la convención es usar solo `blank=True` y guardar strings vacíos. Para otros tipos de datos (`DateField`, `ForeignKey`), se usa `null=True` cuando el valor es opcional.

---

---

# PARTE III — MIGRACIONES

---

## 9. Qué son las migraciones y por qué existen

Las migraciones son el sistema de control de versiones de la base de datos.

Sin migraciones, cada vez que modificaras un modelo tendrías que:

1. Conectarte manualmente a la base de datos
2. Escribir el SQL de `ALTER TABLE`, `CREATE TABLE`, `DROP COLUMN`
3. Hacerlo en todos los entornos: desarrollo de cada developer, staging, producción
4. Coordinar el orden con el equipo para que nadie aplique cambios fuera de secuencia

Las migraciones resuelven todo esto automáticamente. Django detecta qué cambió en los modelos, genera un archivo Python que describe ese cambio como operaciones, y registra en la base de datos cuáles migraciones ya fueron aplicadas.

---

## 10. El flujo de migraciones

Cada cambio en el modelo sigue siempre el mismo proceso de dos pasos:

**Paso 1 — Generar la migración:**

```bash
python manage.py makemigrations
```

Django compara el estado actual de los modelos con la última migración conocida, detecta las diferencias, y genera un archivo Python en la carpeta `migrations/` de la app. El archivo tiene un número secuencial y un nombre descriptivo: `0002_producto_activo_creado_en.py`.

**Paso 2 — Aplicar la migración:**

```bash
python manage.py migrate
```

Django lee todos los archivos de migración pendientes, los aplica a la base de datos en orden, y registra en la tabla `django_migrations` que esas migraciones ya fueron ejecutadas. Si se corre `migrate` de nuevo, Django sabe que no hay nada nuevo y no hace nada.

---

## 11. Anatomía de un archivo de migración

Los archivos de migración son Python legible. No son SQL. Eso es lo que permite que funcionen con distintos motores de base de datos.

```python
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
```

El atributo `dependencies` declara que esta migración depende de la `0001_initial`. Django aplica las migraciones en el orden que la cadena de dependencias define — nunca en orden arbitrario.

El atributo `operations` es la lista de cambios a aplicar. Cada operación tiene un equivalente SQL exacto que Django genera para el motor configurado.

> Importante: los archivos de migración se generan automáticamente y **no se editan a mano**, salvo en casos avanzados de migración de datos donde se agrega código Python dentro de la operación.

---

## 12. Comandos de migraciones

| Comando                                   | Qué hace                                                      |
| ----------------------------------------- | ------------------------------------------------------------- |
| `python manage.py makemigrations`         | Detecta cambios en modelos y genera archivos de migración     |
| `python manage.py migrate`                | Aplica todas las migraciones pendientes a la base de datos    |
| `python manage.py showmigrations`         | Lista todas las migraciones y cuáles tienen `[X]` (aplicadas) |
| `python manage.py sqlmigrate tienda 0002` | Muestra el SQL exacto que ejecutaría esa migración            |
| `python manage.py migrate tienda 0001`    | Revierte al estado de esa migración (deshace las posteriores) |

---

---

# PARTE IV — CONSULTAS CON EL ORM

---

## 13. El Manager y los QuerySets

Cada modelo tiene un objeto especial llamado **Manager**. Por convención, Django lo llama `objects`. Es el intermediario que construye y ejecuta las consultas.

```
Producto.objects.filter(precio__gt=100)
│         │        └── el método de la consulta
│         └── el Manager
└── el modelo
```

El Manager devuelve **QuerySets**. Un QuerySet no es una lista — es una descripción de lo que quieres obtener. Representa una consulta SQL que todavía no se ejecutó.

---

## 14. Consultas básicas

Las operaciones más comunes del ORM:

**Obtener todos los registros:**

```python
Producto.objects.all()
```

Equivale a `SELECT * FROM tienda_producto`. Devuelve un QuerySet con todos los objetos.

**Filtrar con condiciones:**

```python
Producto.objects.filter(activo=True)
Producto.objects.filter(precio__gt=100)
Producto.objects.filter(nombre__icontains='teclado')
```

El `__gt` se llama **lookup** — es un sufijo que define el operador de comparación. `__gt` es "greater than" (mayor que). Ver la tabla completa de lookups en la sección siguiente.

**Excluir registros:**

```python
Producto.objects.exclude(activo=False)
```

`exclude()` es el inverso de `filter()`. Devuelve todos los registros que NO cumplen la condición.

**Obtener exactamente un objeto:**

```python
Producto.objects.get(id=1)
```

`get()` es diferente a `filter()`. Si no encuentra ningún objeto, lanza `Producto.DoesNotExist`. Si encuentra más de uno, lanza `Producto.MultipleObjectsReturned`. Se usa cuando se espera exactamente un resultado — por ejemplo, buscar por ID o por un campo `unique`.

**Ordenar:**

```python
Producto.objects.order_by('nombre')
Producto.objects.order_by('-precio')
```

Sin prefijo: orden ascendente (A→Z, 0→∞). Con el prefijo `-`: orden descendente (Z→A, ∞→0).

**Limitar resultados:**

```python
Producto.objects.all()[:5]
Producto.objects.all()[10:20]
```

El slicing de Python se traduce a `LIMIT` y `OFFSET` en SQL. `[:5]` devuelve los primeros cinco. `[10:20]` devuelve del undécimo al vigésimo.

**Contar registros:**

```python
Producto.objects.filter(activo=True).count()
```

`count()` ejecuta `SELECT COUNT(*)` en la base de datos — mucho más eficiente que traer todos los objetos y usar `len()` en Python.

---

## 15. La tabla completa de lookups

Los lookups son los operadores del ORM. Siempre van después del nombre del campo separados por doble guión bajo:

| Lookup         | Operación             | Equivalente SQL             |
| -------------- | --------------------- | --------------------------- |
| `__exact`      | Igual (es el default) | `= valor`                   |
| `__iexact`     | Igual sin mayúsculas  | `ILIKE 'valor'`             |
| `__contains`   | Contiene el texto     | `LIKE '%valor%'`            |
| `__icontains`  | Contiene sin mayúsculas | `ILIKE '%valor%'`           |
| `__startswith` | Empieza con           | `LIKE 'valor%'`             |
| `__endswith`   | Termina con           | `LIKE '%valor'`             |
| `__gt`         | Mayor que             | `> valor`                   |
| `__gte`        | Mayor o igual         | `>= valor`                  |
| `__lt`         | Menor que             | `< valor`                   |
| `__lte`        | Menor o igual         | `<= valor`                  |
| `__in`         | Está en la lista      | `IN (val1, val2, ...)`      |
| `__range`      | Dentro del rango      | `BETWEEN val1 AND val2`     |
| `__isnull`     | Es nulo o no          | `IS NULL` / `IS NOT NULL`   |
| `__year`       | Año de una fecha      | `EXTRACT(YEAR FROM campo)`  |
| `__month`      | Mes de una fecha      | `EXTRACT(MONTH FROM campo)` |

Se pueden encadenar a través de relaciones. Ejemplo: `categoria__nombre__icontains='electro'` busca por el nombre de la categoría relacionada con `icontains`.

---

## 16. Evaluación diferida — Lazy Evaluation

Este es uno de los conceptos más importantes del ORM, y uno de los que más confunde al principio.

**Un QuerySet no ejecuta ningún SQL hasta que se necesitan los datos.**

Construir y encadenar filtros no genera ninguna consulta. La consulta se ejecuta en el momento en que algo requiere los datos reales.

```python
queryset = Producto.objects.filter(precio__gt=100)
queryset = queryset.filter(activo=True)
queryset = queryset.order_by('nombre')
```

Hasta este punto no se ejecutó ningún SQL. El `queryset` es una descripción de lo que queremos, no los datos en sí.

La consulta se ejecuta cuando se hace alguna de estas operaciones:

```python
for producto in queryset:        # iteración
lista = list(queryset)           # conversión explícita a lista
primero = queryset[0]            # acceso por índice
existe = queryset.exists()       # verificar si hay resultados
cantidad = queryset.count()      # contar
primero = queryset.first()       # el primero
```

**¿Por qué es útil esto?**

Permite construir consultas condicionalmente en distintas partes del código — por ejemplo, en una vista que tiene múltiples filtros opcionales — sin ejecutar consultas parciales innecesarias. Al final se ejecuta una sola consulta SQL eficiente con todas las condiciones.

---

## 17. Q Objects — consultas con OR y NOT

Los filtros encadenados de Django siempre combinan condiciones con AND. No hay forma nativa de hacer OR con `.filter()`.

Los **Q Objects** resuelven eso. Un Q Object encapsula una condición completa y permite combinarla con operadores lógicos.

Antes de usarlos, hay que importarlos:

```python
from django.db.models import Q
```

**AND explícito con Q Objects:**

```python
Producto.objects.filter(Q(precio__gt=50) & Q(stock__gte=10))
```

Esto es equivalente a `filter(precio__gt=50, stock__gte=10)` — las mismas condiciones con AND.

**OR — lo que `filter()` sola no puede hacer:**

```python
Producto.objects.filter(
    Q(nombre__icontains='teclado') | Q(nombre__icontains='mouse')
)
```

Esto devuelve productos cuyo nombre contiene "teclado" O "mouse". Con `.filter()` encadenado no es posible expresar OR.

**NOT — negar una condición:**

```python
Producto.objects.filter(~Q(activo=False))
```

El operador `~` niega el Q Object. Esto devuelve todos los productos donde `activo` no es `False`.

**Combinaciones complejas:**

```python
Producto.objects.filter(
    (Q(precio__gt=100) | Q(stock__gte=50)) & ~Q(activo=False)
)
```

Los paréntesis controlan el agrupamiento, exactamente como en álgebra booleana.

---

---

# PARTE V — RELACIONES ENTRE MODELOS

---

## 18. Por qué existen las relaciones en los modelos

En el mundo real, los datos están relacionados. Los productos pertenecen a categorías. Los pedidos tienen múltiples productos. Los usuarios tienen perfiles. Representar esas relaciones correctamente define la calidad del modelo de datos.

Django soporta tres tipos de relaciones, que corresponden exactamente a los tres tipos de relaciones del modelo relacional:

---

## 19. ForeignKey — muchos a uno

Muchos productos pueden pertenecer a una categoría. Una categoría puede tener muchos productos. Esta es la relación más común.

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre    = models.CharField(max_length=100)
    precio    = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
    )
```

El parámetro `on_delete` define qué hace Django cuando se elimina el objeto referenciado (la categoría en este caso):

| Opción        | Comportamiento                                                       |
| ------------- | -------------------------------------------------------------------- |
| `CASCADE`     | Elimina también todos los productos de esa categoría                 |
| `PROTECT`     | Lanza un error — no permite eliminar la categoría si tiene productos |
| `SET_NULL`    | Pone NULL en `categoria_id` (requiere `null=True` en el campo)       |
| `SET_DEFAULT` | Pone el valor default definido en el campo                           |
| `DO_NOTHING`  | No hace nada — delega la responsabilidad a la base de datos          |

El parámetro `related_name` define el nombre para acceder a la relación inversa. Con `related_name='productos'` se puede hacer `categoria.productos.all()`. Sin `related_name`, Django genera automáticamente `categoria.producto_set.all()` — funciona igual pero es menos expresivo.

**Cómo se ve en la base de datos:**

```
tabla Producto:
id  nombre          categoria_id
1   Teclado         1
2   Mouse           1
3   Monitor 4K      2

tabla Categoria:
id  nombre
1   Periféricos
2   Monitores
```

La columna `categoria_id` en la tabla `Producto` es la clave foránea. Django la genera automáticamente a partir del campo `ForeignKey`.

---

## 20. OneToOneField — uno a uno

Un perfil de producto existe exactamente para un producto. Un producto tiene exactamente un perfil. Esta es una extensión del modelo principal.

```python
class PerfilProducto(models.Model):
    producto      = models.OneToOneField(Producto, on_delete=models.CASCADE)
    descripcion   = models.TextField()
    ficha_tecnica = models.JSONField(default=dict)
```

En la base de datos, `OneToOneField` se implementa igual que `ForeignKey` — con una columna de clave foránea — pero con una restricción `UNIQUE` adicional que impide que dos filas apunten al mismo `Producto`.

El acceso desde el modelo principal es directo: `producto.perfilproducto`. No devuelve un QuerySet sino un objeto único.

---

## 21. ManyToManyField — muchos a muchos

Un producto puede tener varios tags. Un tag puede estar en varios productos. Esta relación requiere una tabla intermedia en la base de datos.

### La pregunta técnica importante

**¿Por qué Django usa `ManyToManyField` si en diseño de bases de datos se evita y se crea una tabla intermedia explícitamente?**

La respuesta es que Django también crea la tabla intermedia. La diferencia es que lo hace automáticamente, de forma transparente.

Cuando defines:

```python
class Tag(models.Model):
    nombre = models.CharField(max_length=50)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tags   = models.ManyToManyField(Tag, blank=True, related_name='productos')
```

Django genera internamente una tercera tabla:

```
tabla tienda_producto_tags (generada automáticamente):
id  producto_id  tag_id
1   1            3
2   1            5
3   2            3
```

Esta tabla intermedia tiene exactamente la misma estructura que crearías manualmente en SQL. La diferencia es que Django la gestiona por tú.

**¿Cuándo crear la tabla intermedia manualmente?** Cuando la relación muchos-a-muchos tiene **datos propios**. Por ejemplo, si quieres registrar la fecha en que se agregó un tag a un producto, o quién lo agregó, necesitás una tabla intermedia con campos adicionales. Para eso Django tiene el atributo `through`:

```python
class ProductoTag(models.Model):
    producto    = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tag         = models.ForeignKey(Tag, on_delete=models.CASCADE)
    agregado_en = models.DateTimeField(auto_now_add=True)
    agregado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tags   = models.ManyToManyField(Tag, through=ProductoTag)
```

Regla: usa `ManyToManyField` sin `through` cuando la relación solo necesita saber "A está relacionado con B". Usa `through` cuando la relación en sí tiene datos adicionales.

---

## 22. Consultar a través de relaciones

El ORM permite filtrar usando campos de modelos relacionados con el mismo operador `__` (doble guión bajo):

```python
Producto.objects.filter(categoria__nombre='Periféricos')
```

Django genera automáticamente el JOIN necesario. Puedes atravesar tantas relaciones como necesites:

```python
Producto.objects.filter(categoria__nombre__icontains='electro')
Producto.objects.filter(tags__nombre__icontains='gaming')
```

Para acceder a objetos relacionados desde una instancia:

```python
producto = Producto.objects.get(id=1)
producto.categoria
producto.categoria.nombre
producto.tags.all()

categoria = Categoria.objects.get(id=1)
categoria.productos.all()
```

---

## 23. Optimización — `select_related` y `prefetch_related`

Sin optimización, acceder a datos relacionados en un bucle genera el **problema N+1**: una consulta para traer N objetos y luego N consultas adicionales para traer los datos relacionados de cada uno.

**El problema N+1:**

```python
productos = Producto.objects.all()
for p in productos:
    print(p.categoria.nombre)
```

Este código ejecuta 1 consulta para traer los productos, y luego 1 consulta por cada producto para traer su categoría. Si hay 100 productos, son 101 consultas.

---

### `select_related` — para ForeignKey y OneToOne

Hace un `JOIN` SQL y trae todos los datos en **una sola consulta**:

```python
productos = Producto.objects.select_related('categoria').all()
for p in productos:
    print(p.categoria.nombre)
```

Resultado: 1 sola consulta SQL con `INNER JOIN`. Sin importar cuántos productos haya, siempre es 1 consulta.

---

### `prefetch_related` — para ManyToMany y relaciones inversas

Las relaciones ManyToMany no se pueden optimizar con JOIN (generarían filas duplicadas). `prefetch_related` hace **2 consultas** y luego une los resultados en Python:

```python
productos = Producto.objects.prefetch_related('tags').all()
for p in productos:
    for tag in p.tags.all():
        print(tag.nombre)
```

Resultado: 2 consultas en lugar de N+1. La segunda consulta trae todos los tags de todos los productos de una vez, y Python los agrupa.

---

---

# PARTE VI — SQL DIRECTO EN DJANGO

---

## 24. ¿Cuándo usar SQL directo?

El ORM cubre el 95% de los casos. Las situaciones donde el SQL directo tiene sentido son específicas:

- Consultas con funciones propias del motor (funciones de ventana, `ROLLUP`, `CUBE` en PostgreSQL)
- Reportería compleja con múltiples niveles de `GROUP BY`
- Procedimientos almacenados existentes en un sistema heredado
- Optimizaciones de rendimiento medidas y comprobadas donde el SQL del ORM no es eficiente

Fuera de esos casos, el ORM siempre es preferible.

---

## 25. `raw()` — SQL que devuelve objetos del modelo

`raw()` ejecuta una consulta SQL y devuelve instancias del modelo. No devuelve tuplas — devuelve objetos Python con los mismos atributos que si los hubieras obtenido con el ORM normal.

```python
productos = Producto.objects.raw(
    'SELECT * FROM tienda_producto WHERE precio > %s',
    [100]
)

for p in productos:
    print(p.nombre, p.precio)
```

El segundo argumento es siempre una lista de parámetros. Django los inserta en la consulta de forma segura — nunca concatenando strings. Esta es la forma correcta de prevenir inyección SQL en consultas directas.

Limitaciones: la consulta debe incluir el campo `id` del modelo. No soporta `.filter()`, `.order_by()` ni ningún método de QuerySet después.

---

## 26. `connection.cursor()` — control total

Cuando se necesitan resultados que no corresponden a ningún modelo — por ejemplo, datos de reportes, conteos agrupados, o consultas a múltiples tablas — se usa el cursor de base de datos directamente:

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT categoria_id, COUNT(*), AVG(precio) FROM tienda_producto GROUP BY categoria_id"
    )
    resultados = cursor.fetchall()

for categoria_id, cantidad, precio_promedio in resultados:
    print(f"Categoría {categoria_id}: {cantidad} productos, promedio ${precio_promedio:.2f}")
```

El bloque `with` garantiza que la conexión se cierra correctamente después de ejecutar la consulta, incluso si ocurre un error en el medio. `fetchall()` trae todos los resultados como una lista de tuplas. `fetchone()` trae solo la primera fila.

---

## 27. Comparación final: ORM vs SQL directo

| Criterio      | ORM                                        | SQL directo (`raw` / `cursor`)            |
| ------------- | ------------------------------------------ | ----------------------------------------- |
| Portabilidad  | Funciona con cualquier motor sin cambios   | Depende del dialecto SQL del motor        |
| Seguridad     | Protección automática contra SQL injection | Responsabilidad del developer             |
| Legibilidad   | Alta — es Python puro                      | Media — requiere conocer SQL del motor    |
| Mantenimiento | El ORM evoluciona con Django               | Requiere actualización manual             |
| Rendimiento   | Muy bueno para el 95% de los casos         | Máximo control en consultas complejas     |
| Depuración    | Stack traces en Python                     | Errores de SQL más difíciles de trazar    |
| Cuándo usarlo | Siempre que sea posible                    | Consultas complejas no expresables en ORM |

---

---

# MAPA COMPLETO DEL MÓDULO

---

```
DJANGO Y SUS DATOS
│
├── ARCHIVOS DONDE OPERA EL ORM
│   ├── models.py      → definición de modelos y relaciones
│   ├── views.py       → consultas y manipulación de datos
│   ├── admin.py       → configuración del panel de gestión
│   ├── forms.py       → ModelForm genera forms desde modelos
│   └── tests.py       → creación de datos de prueba
│
├── CONFIGURACIÓN
│   ├── settings.py → DATABASES → motor + credenciales
│   ├── SQLite      → sin servidor, ideal para desarrollo
│   └── PostgreSQL  → recomendado para producción
│
├── MODELOS
│   ├── Campos        → tipos de dato → columnas en SQL
│   ├── Opciones      → default, blank, null, unique, choices
│   └── __str__       → cómo se muestra el objeto como texto
│
├── MIGRACIONES
│   ├── makemigrations → detecta cambios → genera archivo
│   └── migrate        → aplica el archivo → actualiza la BD
│
├── ORM — CONSULTAS
│   ├── .all()                         → todos los registros
│   ├── .filter(campo__lookup=valor)   → con condición
│   ├── .exclude(...)                  → lo inverso de filter
│   ├── .get(...)                       → exactamente uno
│   ├── .order_by('campo')             → ordenar
│   ├── .first() / .last()             → el primero o último
│   ├── .count()                       → contar sin traer datos
│   └── Lazy evaluation                → SQL al final, no antes
│
├── Q OBJECTS
│   ├── &  → AND explícito
│   ├── |  → OR (imposible con filter() solo)
│   └── ~  → NOT
│
├── RELACIONES
│   ├── ForeignKey       → muchos-a-uno → tabla principal + FK
│   ├── OneToOneField    → uno-a-uno    → FK con restricción UNIQUE
│   └── ManyToManyField  → muchos-a-muchos → Django crea tabla intermedia
│
├── OPTIMIZACIÓN
│   ├── select_related   → JOIN para ForeignKey / OneToOne
│   └── prefetch_related → 2 consultas para ManyToMany
│
└── SQL DIRECTO
    ├── .raw('SQL', [params])   → devuelve instancias del modelo
    └── connection.cursor()     → control total, devuelve tuplas
```

---

---

# 30 PREGUNTAS FRECUENTES

---

> Esta sección anticipa las preguntas que aparecen en clase, en entrevistas técnicas y en discusiones de equipo.

---

**1. ¿El ORM de Django es más lento que escribir SQL directamente?**

En la mayoría de los casos, la diferencia es insignificante. El ORM genera SQL eficiente y las consultas están optimizadas por el motor de base de datos. La diferencia de rendimiento solo se nota en consultas extremadamente complejas, y en esos casos se puede usar `raw()` o `cursor()` puntualmente.

**2. ¿En qué archivo van las consultas del ORM?**

La definición del modelo (qué campos tiene) va en `models.py`. Las consultas (qué datos traer) van en `views.py`. Es la división de responsabilidades que Django establece por convención.

**3. ¿Por qué Django crea `ManyToManyField` si en diseño de BD se crea la tabla intermedia?**

Django también crea la tabla intermedia. La diferencia es que lo hace automáticamente. Cuando usas `ManyToManyField`, Django genera una tercera tabla con las claves foráneas de ambos lados. Si la relación necesita campos propios (como una fecha o un estado), se usa `through` para definir la tabla intermedia manualmente con campos adicionales.

**4. ¿Qué diferencia hay entre `filter()` y `get()`?**

`filter()` siempre devuelve un QuerySet — puede tener cero, uno o muchos resultados. `get()` espera exactamente un resultado: si no encuentra ninguno lanza `DoesNotExist`, si encuentra más de uno lanza `MultipleObjectsReturned`. Se usa `get()` cuando el campo es único (como `id`) y `filter()` cuando pueden existir múltiples resultados.

**5. ¿Qué pasa si no corro `migrate` después de crear un modelo?**

El modelo existe en Python pero la tabla no existe en la base de datos. Cualquier consulta al modelo lanzará un error del tipo `django.db.OperationalError: no such table`.

**6. ¿Para qué sirve `related_name`?**

Define el nombre del atributo que se usa para acceder a la relación inversa. Un `ForeignKey` de `Producto` a `Categoria` con `related_name='productos'` permite hacer `categoria.productos.all()`. Sin `related_name`, Django genera automáticamente el nombre `producto_set`.

**7. ¿Cuándo uso `null=True` y cuándo `blank=True`?**

`null=True` afecta la base de datos — permite que la columna tenga valor NULL. `blank=True` afecta la validación de formularios — permite que el campo quede vacío al enviar un formulario. Para campos de texto, la convención es solo `blank=True` y guardar strings vacíos. Para otros tipos (`DateField`, `ForeignKey`), si el valor es opcional se usa `null=True`.

**8. ¿Qué es la evaluación diferida (lazy evaluation)?**

Es el comportamiento del ORM donde construir y encadenar filtros no ejecuta ningún SQL. La consulta SQL recién se ejecuta cuando los datos son necesarios — al iterar, convertir a lista, o usar `.count()`, `.first()`, etc. Esto permite construir consultas complejas condicionalmente sin ejecutar consultas intermedias innecesarias.

**9. ¿Cuál es la diferencia entre `select_related` y `prefetch_related`?**

`select_related` hace un JOIN SQL y trae datos relacionados de `ForeignKey` y `OneToOneField` en una sola consulta. `prefetch_related` hace dos consultas separadas para relaciones `ManyToManyField` o relaciones inversas de `ForeignKey`, y luego une los resultados en Python. Ambos resuelven el problema N+1 de distintas formas según el tipo de relación.

**10. ¿Qué es el problema N+1?**

Es el patrón ineficiente donde una consulta trae N objetos y luego se ejecutan N consultas adicionales para traer datos relacionados de cada uno. Si hay 100 productos y cada uno accede a su categoría en un bucle, son 101 consultas. `select_related` y `prefetch_related` lo resuelven.

**11. ¿Cuándo no se puede usar el ORM y hay que usar SQL directo?**

Cuando la consulta requiere funciones específicas del motor de base de datos que el ORM no soporta (como `ROLLUP`, funciones de ventana avanzadas, o procedimientos almacenados), o cuando la consulta es tan compleja que el SQL generado por el ORM es ineficiente. Son casos de la minoría.

**12. ¿Por qué hay que usar parámetros en `raw()` y no concatenar strings?**

La concatenación de strings para construir SQL permite **inyección SQL** — el atacante puede insertar SQL malicioso que modifica la consulta. Al usar parámetros (`%s`), Django escapa los valores automáticamente, haciendo imposible que un valor externo modifique la estructura del SQL.

**13. ¿Qué significa que la tabla de un modelo se llama `tienda_producto`?**

El nombre de tabla sigue el patrón `nombre_de_app_nombre_del_modelo`. Si la app se llama `tienda` y el modelo `Producto`, la tabla es `tienda_producto`. Esto evita colisiones de nombres entre modelos de distintas apps con el mismo nombre.

**14. ¿Puedo cambiar el nombre de la tabla que Django genera?**

Sí. En la clase `Meta` del modelo: `db_table = 'mi_tabla_personalizada'`. Esto es útil al integrar Django con una base de datos existente cuyas tablas tienen nombres predefinidos.

**15. ¿Qué es `on_delete=models.CASCADE`?**

Define qué hace Django cuando se elimina el objeto referenciado por una `ForeignKey`. `CASCADE` elimina en cascada todos los objetos que apuntan al eliminado. `PROTECT` impide la eliminación si existen objetos relacionados. `SET_NULL` pone NULL en el campo de clave foránea.

**16. ¿Para qué sirve `auto_now_add` y en qué se diferencia de `default`?**

`auto_now_add=True` asigna automáticamente la fecha y hora actuales solo cuando se crea el objeto — y después no se puede modificar. `default=timezone.now` también asigna la fecha actual, pero el campo puede modificarse luego. `auto_now=True` actualiza la fecha cada vez que se guarda el objeto.

**17. ¿Qué es un Manager y puedo tener más de uno?**

El Manager es el objeto `objects` de cada modelo — el intermediario que construye y ejecuta consultas. Sí, puedes tener múltiples Managers en un modelo. Es útil para crear consultas nombradas y reutilizables: por ejemplo, `Producto.activos.all()` que llama a un Manager personalizado que ya incluye `filter(activo=True)`.

**18. ¿Qué diferencia hay entre `FloatField` y `DecimalField`?**

`FloatField` usa aritmética de punto flotante binaria — tiene errores de representación. `0.1 + 0.2` puede dar `0.30000000000000004`. `DecimalField` usa aritmética decimal de precisión exacta. Para dinero siempre `DecimalField`.

**19. ¿Puedo conectar Django a una base de datos existente?**

Sí. Django tiene el comando `inspectdb` que analiza una base de datos existente y genera el código Python de los modelos automáticamente. Útil para integrar Django con sistemas heredados.

**20. ¿Qué es `JSONField` y cuándo se usa?**

Campo disponible desde Django 3.1 que guarda estructuras JSON directamente en la base de datos. En PostgreSQL usa el tipo `JSONB` que permite búsquedas dentro del JSON. Se usa cuando los datos tienen estructura variable que no se puede definir con campos fijos — preferencias de usuario, configuraciones, datos de APIs externas.

**21. ¿Qué pasa si dos developers modifican el mismo modelo al mismo tiempo?**

Ambos generan una migración desde el mismo estado base. Al hacer `migrate` en el orden incorrecto, pueden ocurrir conflictos. Django detecta los conflictos de migraciones y tiene el comando `squashmigrations` para reducirlas. En equipos, la convención es comunicar los cambios de modelos y mergear las migraciones antes de aplicarlas.

**22. ¿Los Q Objects reemplazan a los filtros normales?**

No. Los filtros normales son más legibles para condiciones simples. Los Q Objects solo son necesarios cuando se necesita OR o NOT. Mezclar ambos en la misma consulta es válido: un argumento normal y uno Q Object pueden coexistir en el mismo `filter()`.

**23. ¿El campo `id` siempre es un entero? ¿Se puede usar otro campo como clave primaria?**

Por defecto `id` es un `BigAutoField` — entero autoincremental de 64 bits. Pero se puede cambiar. Con `primary_key=True` en cualquier campo, ese campo se convierte en la clave primaria y Django no genera el `id` automático. Por ejemplo, un campo `uuid` o un `slug` como clave primaria.

**24. ¿Cuál es la diferencia entre `makemigrations` y `migrate`?**

`makemigrations` detecta cambios en los modelos y genera archivos Python que describen esos cambios. `migrate` lee esos archivos y aplica los cambios a la base de datos. Son dos pasos separados: primero se define qué cambiar, luego se aplica el cambio.

**25. ¿Se pueden hacer consultas asíncronas con el ORM en Django 6?**

Sí. Django 4.1 introdujo soporte async en las consultas del ORM. Se usa con `async for`, `aget()`, `afilter()`, `acreate()`, `adelete()`. En Django 6, se agregó `AsyncPaginator` para paginación asíncrona. Esto es útil en vistas asíncronas con `async def`.

**26. ¿Qué hace `Producto.objects.none()`?**

Devuelve un QuerySet vacío — nunca ejecuta ningún SQL. Es útil como valor inicial en páginas de búsqueda donde se quiere mostrar nada hasta que el usuario realice una búsqueda, o en formularios de filtrado con ningún criterio.

**27. ¿Cuál es la diferencia entre `DELETE` de ORM y `Producto.objects.filter().delete()`?**

La primera es la eliminación de un objeto individual: `producto.delete()`. La segunda es una eliminación masiva que ejecuta un solo `DELETE WHERE` sin traer los objetos a Python — mucho más eficiente para eliminar muchos registros. La diferencia importante: la eliminación masiva no dispara las signals `pre_delete` y `post_delete` para cada objeto individual.

**28. ¿Puedo ver el SQL que genera el ORM?**

Sí. Tres formas: `str(queryset.query)` imprime el SQL del QuerySet. `django.db.connection.queries` lista todas las consultas ejecutadas. `django-debug-toolbar` es un paquete que muestra las consultas en el navegador durante el desarrollo.

**29. ¿Qué diferencia hay entre `Producto.objects.filter()` y `Producto.objects.all().filter()`?**

Son equivalentes. `filter()` en el Manager devuelve el mismo resultado que `all().filter()`. La convención es usar `filter()` directamente sin `all()` cuando se especifica una condición.

**30. ¿Cuándo es mejor crear una migración de datos además de una migración de esquema?**

Cuando necesitás transformar datos existentes al aplicar un cambio de modelo. Por ejemplo, si partís un campo `nombre_completo` en `nombre` y `apellido`, necesitás migrar el esquema (agregar las columnas) y luego migrar los datos (copiar y dividir los valores existentes). Esto se hace con `migrations.RunPython()` dentro de la migración.

---
