# Referencia Completa: Tipos de Campo en Django

> Actualizado para Django 5.x (Django 6 no ha sido lanzado al momento de esta guía — se actualiza esta documentación apenas esté disponible). La API de campos es retrocompatible desde Django 4.x.

---

## Opciones universales (aplican a TODOS los campos)

Antes de ver los tipos de campo, estas opciones están disponibles para cualquier campo sin excepción:

| Opción           | Tipo       | Default  | Descripción |
|------------------|------------|----------|-------------|
| `null`           | `bool`     | `False`  | Permite `NULL` en la base de datos |
| `blank`          | `bool`     | `False`  | Permite el campo vacío en formularios de Django |
| `default`        | cualquiera | —        | Valor por defecto si no se provee uno |
| `choices`        | `list/enum`| —        | Restringe los valores posibles a una lista |
| `unique`         | `bool`     | `False`  | Impone que no haya dos filas con el mismo valor |
| `db_index`       | `bool`     | `False`  | Crea un índice en la base de datos para ese campo |
| `primary_key`    | `bool`     | `False`  | Convierte el campo en la clave primaria de la tabla |
| `editable`       | `bool`     | `True`   | Si `False`, el campo no aparece en formularios ni en el Admin |
| `verbose_name`   | `str`      | —        | Nombre legible del campo para el Admin y formularios |
| `help_text`      | `str`      | `""`     | Texto de ayuda que se muestra en formularios |
| `validators`     | `list`     | `[]`     | Lista de funciones de validación a ejecutar sobre el valor |
| `db_column`      | `str`      | —        | Nombre explícito de la columna en la base de datos |
| `db_tablespace`  | `str`      | —        | Tablespace de BD para el índice (solo algunos motores) |
| `error_messages` | `dict`     | —        | Diccionario para sobreescribir mensajes de error por defecto |

---

## 1. Campos de texto

### `CharField`
Campo de texto corto. Requiere `max_length` obligatoriamente.

```python
nombre = models.CharField(max_length=200)
```

| Opción        | Tipo  | Descripción                               |
|---------------|-------|-------------------------------------------|
| `max_length`  | `int` | **Obligatorio.** Longitud máxima del campo |

---

### `TextField`
Campo de texto largo sin límite de caracteres. Equivale a `TEXT` en SQL.

```python
descripcion = models.TextField(blank=True)
```

| Opción | Descripción |
|--------|-------------|
| No tiene opciones propias — usa solo las universales |

---

### `EmailField`
Equivale a un `CharField(max_length=254)` con validación de formato de email.

```python
email = models.EmailField(unique=True)
```

| Opción       | Default | Descripción         |
|--------------|---------|---------------------|
| `max_length` | `254`   | Sobreescribible      |

---

### `URLField`
`CharField` con validación de formato de URL.

```python
sitio_web = models.URLField(blank=True)
```

| Opción       | Default | Descripción |
|--------------|---------|-------------|
| `max_length` | `200`   | Sobreescribible |

---

### `SlugField`
Campo de texto que solo acepta letras, números, guiones y guiones bajos. Usado en URLs amigables.

```python
slug = models.SlugField(unique=True)
```

| Opción           | Default | Descripción |
|------------------|---------|-------------|
| `max_length`     | `50`    | Sobreescribible |
| `allow_unicode`  | `False` | Si `True`, permite caracteres unicode además del ASCII estándar |

---

### `UUIDField`
Campo para almacenar UUIDs. Se almacena como `uuid` en PostgreSQL (nativo) y como `char(32)` en otros motores.

```python
import uuid
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

| Opción | Descripción |
|--------|-------------|
| No tiene opciones propias — usa solo las universales |

---

### `GenericIPAddressField`
Almacena una dirección IP (v4 o v6).

```python
ip_cliente = models.GenericIPAddressField(blank=True, null=True)
```

| Opción         | Default  | Descripción |
|----------------|----------|-------------|
| `protocol`     | `'both'` | Opciones: `'both'`, `'IPv4'`, `'IPv6'` |
| `unpack_ipv4`  | `False`  | Si `True`, desempaqueta IPs IPv4 mapeadas en IPv6 como `::ffff:192.0.2.1` |

---

### `JSONField`
Almacena datos JSON arbitrarios. Nativo en PostgreSQL, SQLite ≥ 3.9.0 y MariaDB 10.2.7+.

```python
metadata = models.JSONField(default=dict)
```

| Opción    | Descripción |
|-----------|-------------|
| `encoder` | Clase JSON encoder personalizada |
| `decoder` | Clase JSON decoder personalizada |

> **Nota:** Los `JSONField` soportan búsquedas especiales en PostgreSQL como `metadata__clave`, `metadata__clave__contains`, etc.

---

## 2. Campos numéricos

### `IntegerField`
Número entero. Rango típico: -2.147.483.648 a 2.147.483.647.

```python
cantidad = models.IntegerField(default=0)
```

---

### `PositiveIntegerField`
Entero que solo acepta valores positivos (≥ 0).

```python
stock = models.PositiveIntegerField(default=0)
```

---

### `PositiveSmallIntegerField`
Entero positivo pequeño (0 a 32.767).

```python
calificacion = models.PositiveSmallIntegerField()
```

---

### `SmallIntegerField`
Entero pequeño con signo (-32.768 a 32.767).

```python
temperatura = models.SmallIntegerField()
```

---

### `BigIntegerField`
Entero grande. Rango: -9.223.372.036.854.775.808 a 9.223.372.036.854.775.807.

```python
visitas = models.BigIntegerField(default=0)
```

---

### `PositiveBigIntegerField`
Entero grande positivo (0 a 9.223.372.036.854.775.807).

```python
id_externo = models.PositiveBigIntegerField()
```

---

### `SmallAutoField`
Clave primaria autoincremental pequeña (1 a 32.767). Se usa en tablas con pocos registros.

```python
# Se configura en settings.py, no directamente en el modelo
DEFAULT_AUTO_FIELD = 'django.db.models.SmallAutoField'
```

---

### `AutoField`
Clave primaria autoincremental estándar (entero de 32 bits). Es el campo que Django agrega por defecto si no se define `primary_key`.

---

### `BigAutoField`
Clave primaria autoincremental grande (entero de 64 bits). Recomendado para aplicaciones con muchos registros.

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

### `FloatField`
Número de punto flotante de 64 bits. **No usar para dinero** — tiene imprecisión decimal.

```python
latitud = models.FloatField()
```

---

### `DecimalField`
Número decimal de precisión exacta. **Usar siempre para precios, montos y porcentajes**.

```python
precio = models.DecimalField(max_digits=10, decimal_places=2)
```

| Opción          | Tipo  | Descripción |
|-----------------|-------|-------------|
| `max_digits`    | `int` | **Obligatorio.** Total de dígitos significativos |
| `decimal_places`| `int` | **Obligatorio.** Dígitos después del punto decimal |

---

## 3. Campos booleanos

### `BooleanField`
Verdadero o falso. En PostgreSQL se almacena como `boolean`; en SQLite como `integer`.

```python
activo = models.BooleanField(default=True)
```

> **Nota histórica:** En versiones anteriores a Django 2.1, existía `NullBooleanField` para permitir `None` además de `True/False`. Hoy se usa `BooleanField(null=True)`.

---

## 4. Campos de fecha y hora

### `DateField`
Solo fecha (año, mes, día). Sin información de hora.

```python
fecha_nacimiento = models.DateField(null=True, blank=True)
```

| Opción         | Default | Descripción |
|----------------|---------|-------------|
| `auto_now`     | `False` | Si `True`, actualiza la fecha cada vez que se guarda el objeto |
| `auto_now_add` | `False` | Si `True`, registra la fecha de creación una sola vez |

> `auto_now` y `auto_now_add` hacen el campo de solo lectura implícitamente.

---

### `TimeField`
Solo hora (sin fecha).

```python
hora_apertura = models.TimeField()
```

| Opción         | Default | Descripción |
|----------------|---------|-------------|
| `auto_now`     | `False` | Actualiza la hora en cada guardado |
| `auto_now_add` | `False` | Registra la hora de creación |

---

### `DateTimeField`
Fecha y hora combinadas. El más usado para auditoría.

```python
creado_en    = models.DateTimeField(auto_now_add=True)
actualizado_en = models.DateTimeField(auto_now=True)
```

| Opción         | Default | Descripción |
|----------------|---------|-------------|
| `auto_now`     | `False` | Actualiza en cada guardado |
| `auto_now_add` | `False` | Registra solo al crear |

---

### `DurationField`
Almacena un período de tiempo (diferencia entre dos fechas). Equivale a `interval` en PostgreSQL.

```python
duracion_estimada = models.DurationField()
```

---

## 5. Campos de archivos

### `FileField`
Campo para subida de archivos.

```python
documento = models.FileField(upload_to='documentos/')
```

| Opción      | Default | Descripción |
|-------------|---------|-------------|
| `upload_to` | `""`    | Subcarpeta dentro de `MEDIA_ROOT` donde se guardan los archivos |
| `storage`   | —       | Motor de almacenamiento personalizado (ej. Amazon S3) |
| `max_length`| `100`   | Longitud máxima del path almacenado en la BD |

---

### `ImageField`
Extiende `FileField` con validación de que el archivo sea una imagen válida. Requiere `Pillow`.

```python
foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
```

| Opción           | Descripción |
|------------------|-------------|
| `height_field`   | Nombre del campo donde se guarda la altura de la imagen automáticamente |
| `width_field`    | Nombre del campo donde se guarda el ancho de la imagen automáticamente |
| + todos los de FileField | |

---

### `FilePathField`
Campo que solo acepta paths de archivos que existen en el sistema de archivos del servidor.

```python
template = models.FilePathField(path='/srv/templates', match='.*\.html$')
```

| Opción       | Default | Descripción |
|--------------|---------|-------------|
| `path`       | —       | **Obligatorio.** Ruta del directorio base |
| `match`      | —       | Regex para filtrar los archivos mostrados |
| `recursive`  | `False` | Si `True`, incluye subdirectorios |
| `allow_files`| `True`  | Si `False`, excluye archivos (solo directorios) |
| `allow_folders`| `False`| Si `True`, incluye directorios |
| `max_length` | `100`   | Longitud máxima del path |

---

## 6. Campos de relación

### `ForeignKey`
Relación muchos-a-uno. Crea una columna `campo_id` en la tabla.

```python
categoria = models.ForeignKey(
    'Categoria',
    on_delete=models.PROTECT,
    related_name='productos',
    null=True,
    blank=True
)
```

| Opción           | Descripción |
|------------------|-------------|
| `on_delete`      | **Obligatorio.** Comportamiento al eliminar el objeto relacionado |
| `related_name`   | Nombre del acceso inverso desde el modelo relacionado |
| `related_query_name` | Nombre del acceso en filtros de QuerySet |
| `limit_choices_to`| Limita las opciones en formularios con un dict o Q object |
| `to_field`       | Campo del modelo remoto al que apunta (por defecto: `pk`) |
| `db_constraint`  | `True` — si `False`, no crea la FK en la BD (útil para BDs heredadas) |
| `swappable`      | Activa el soporte de swapping para ese modelo |

**Valores de `on_delete`:**

| Valor              | Comportamiento |
|--------------------|----------------|
| `CASCADE`          | Elimina el objeto hijo al eliminar el padre |
| `PROTECT`          | Impide eliminar el padre si tiene hijos |
| `RESTRICT`         | Igual que PROTECT pero con mensaje de error más específico |
| `SET_NULL`         | Pone `NULL` en el hijo (requiere `null=True`) |
| `SET_DEFAULT`      | Pone el valor `default` del campo |
| `SET(valor)`       | Pone un valor específico o resultado de una función |
| `DO_NOTHING`       | No hace nada — puede romper la integridad referencial |

---

### `OneToOneField`
Relación uno-a-uno. Igual que `ForeignKey` pero con `unique=True` implícito.

```python
perfil = models.OneToOneField(
    'auth.User',
    on_delete=models.CASCADE,
    related_name='perfil'
)
```

Acepta las mismas opciones que `ForeignKey`.

---

### `ManyToManyField`
Relación muchos-a-muchos. Django crea automáticamente la tabla intermedia.

```python
ingredientes = models.ManyToManyField(
    'Ingrediente',
    blank=True,
    related_name='platos'
)
```

| Opción             | Descripción |
|--------------------|-------------|
| `through`          | Clase de modelo para la tabla intermedia personalizada |
| `through_fields`   | Tupla de campos de la tabla `through` que definen la relación |
| `related_name`     | Nombre del acceso inverso |
| `related_query_name`| Nombre en filtros |
| `limit_choices_to` | Filtra las opciones disponibles |
| `symmetrical`      | Solo para relaciones auto-referenciales — si `False`, la relación no es simétrica |
| `db_table`         | Nombre de la tabla intermedia generada automáticamente |
| `db_constraint`    | Si `False`, no crea restricciones de FK en la tabla intermedia |

---

## 7. Campos especiales y avanzados

### `AutoField` / `BigAutoField` / `SmallAutoField`
Claves primarias autoincrementales. Normalmente no se declaran — Django las agrega automáticamente.

```python
# Configuración global en settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

### `BinaryField`
Almacena datos binarios crudos (bytes).

```python
firma_digital = models.BinaryField()
```

| Opción     | Default | Descripción |
|------------|---------|-------------|
| `max_length`| —      | Longitud máxima en bytes |
| `editable` | `False` | Por defecto no aparece en formularios |

---

### `ArrayField` *(solo PostgreSQL)*
Campo para almacenar arrays de valores del mismo tipo.

```python
from django.contrib.postgres.fields import ArrayField

etiquetas = models.ArrayField(
    base_field=models.CharField(max_length=50),
    size=10,
    blank=True,
    default=list
)
```

| Opción       | Descripción |
|--------------|-------------|
| `base_field` | **Obligatorio.** Tipo de campo de cada elemento del array |
| `size`       | Tamaño máximo del array (opcional) |

---

### `HStoreField` *(solo PostgreSQL)*
Almacena pares clave-valor en formato `hstore` de PostgreSQL.

```python
from django.contrib.postgres.fields import HStoreField

atributos = models.HStoreField(blank=True, default=dict)
```

---

### `RangeField` *(solo PostgreSQL)*
Familia de campos para almacenar rangos numéricos o de fechas.

```python
from django.contrib.postgres.fields import IntegerRangeField, DateRangeField

edad_permitida = IntegerRangeField()
periodo_validez = DateRangeField()
```

Variantes disponibles: `IntegerRangeField`, `BigIntegerRangeField`, `DecimalRangeField`, `DateRangeField`, `DateTimeRangeField`.

---

### `SearchVectorField` *(solo PostgreSQL)*
Campo para búsqueda de texto completo (full-text search). Almacena el vector de búsqueda directamente en la tabla para consultas más rápidas.

```python
from django.contrib.postgres.search import SearchVectorField

vector_busqueda = models.SearchVectorField(null=True, editable=False)
```

> Requiere configuración adicional con signals o triggers para mantenerse actualizado.

---

## 8. Tabla comparativa rápida

| Campo                   | SQL equivalente | Requiere parámetros obligatorios |
|-------------------------|-----------------|----------------------------------|
| `CharField`             | `VARCHAR(n)`    | `max_length`                     |
| `TextField`             | `TEXT`          | Ninguno                          |
| `EmailField`            | `VARCHAR(254)`  | Ninguno                          |
| `URLField`              | `VARCHAR(200)`  | Ninguno                          |
| `SlugField`             | `VARCHAR(50)`   | Ninguno                          |
| `UUIDField`             | `UUID`          | Ninguno                          |
| `JSONField`             | `JSON` / `JSONB`| Ninguno                          |
| `IntegerField`          | `INTEGER`       | Ninguno                          |
| `PositiveIntegerField`  | `INTEGER`+CHECK | Ninguno                          |
| `BigIntegerField`       | `BIGINT`        | Ninguno                          |
| `FloatField`            | `DOUBLE`        | Ninguno                          |
| `DecimalField`          | `NUMERIC(p,s)`  | `max_digits`, `decimal_places`   |
| `BooleanField`          | `BOOLEAN`       | Ninguno                          |
| `DateField`             | `DATE`          | Ninguno                          |
| `TimeField`             | `TIME`          | Ninguno                          |
| `DateTimeField`         | `TIMESTAMP`     | Ninguno                          |
| `DurationField`         | `INTERVAL`      | Ninguno                          |
| `FileField`             | `VARCHAR(100)`  | Ninguno                          |
| `ImageField`            | `VARCHAR(100)`  | Ninguno                          |
| `ForeignKey`            | `INTEGER`+FK    | `on_delete`                      |
| `OneToOneField`         | `INTEGER`+FK+UQ | `on_delete`                      |
| `ManyToManyField`       | Tabla intermedia| Ninguno                          |
| `BinaryField`           | `BYTEA`         | Ninguno                          |
| `ArrayField` (PG)       | `tipo[]`        | `base_field`                     |

---

## 9. Constraints de la clase Meta

Las `Meta.constraints` agregan restricciones directamente en la base de datos, independientemente de la validación a nivel de Python.

### `CheckConstraint`

```python
from django.db.models import Q

class Meta:
    constraints = [
        models.CheckConstraint(
            check=Q(precio__gte=0),
            name='precio_no_negativo',
            violation_error_message='El precio no puede ser negativo.'  # Django 4.1+
        )
    ]
```

---

### `UniqueConstraint`

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['email', 'dominio'],
            name='email_unico_por_dominio',
            condition=Q(activo=True),        # Unicidad parcial (solo a activos)
            nulls_distinct=False,            # Django 5.0+ — NULL se considera igual a NULL
            deferrable=models.Deferrable.DEFERRED,  # PostgreSQL: valida al commitear
        )
    ]
```

| Opción               | Disponible desde | Descripción |
|----------------------|------------------|-------------|
| `fields`             | siempre          | **Obligatorio.** Campos que forman la clave única |
| `name`               | siempre          | **Obligatorio.** Nombre del constraint en la BD |
| `condition`          | Django 3.0       | Restringe la unicidad a filas que cumplen la condición |
| `include`            | Django 3.2       | Añade columnas al índice sin incluirlas en el constraint |
| `opclasses`          | Django 3.2       | PostgreSQL: clases de operador para el índice |
| `nulls_distinct`     | Django 5.0       | Si `False`, trata `NULL` como igual a `NULL` |
| `deferrable`         | Django 3.1       | Permite diferir la validación hasta el commit de la transacción |
| `violation_error_code`| Django 5.0     | Código de error lanzado al violar el constraint |
| `violation_error_message`| Django 4.1  | Mensaje de error personalizado |

---

### `ExclusionConstraint` *(solo PostgreSQL)*

```python
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators

class Meta:
    constraints = [
        ExclusionConstraint(
            name='sin_reservas_superpuestas',
            expressions=[
                ('sala', RangeOperators.EQUAL),
                ('periodo', RangeOperators.OVERLAPS),
            ]
        )
    ]
```

Garantiza que ningún par de filas satisfaga simultáneamente todos los operadores definidos. Útil para reservas de salas, turnos de médico, etc.

---

## 10. Índices de la clase Meta

```python
from django.db.models import Index

class Meta:
    indexes = [
        # Índice simple
        models.Index(fields=['nombre']),

        # Índice compuesto
        models.Index(fields=['categoria', 'precio'], name='idx_cat_precio'),

        # Índice parcial (solo PostgreSQL y SQLite)
        models.Index(
            fields=['precio'],
            name='idx_precio_activo',
            condition=Q(disponible=True)
        ),

        # Índice funcional — Django 5.0+
        models.Index(
            Upper('nombre'),
            name='idx_nombre_upper'
        ),
    ]
```

### `HashIndex` *(solo PostgreSQL)*

```python
from django.contrib.postgres.indexes import HashIndex, GinIndex, GistIndex, BrinIndex

class Meta:
    indexes = [
        HashIndex(fields=['token'], name='idx_token_hash'),
        GinIndex(fields=['metadata'], name='idx_metadata_gin'),  # para JSONField y ArrayField
        GistIndex(fields=['periodo'], name='idx_periodo_gist'),  # para RangeField
        BrinIndex(fields=['creado_en'], name='idx_created_brin'), # para tablas ordenadas cronológicamente
    ]
```

---

## 11. Validators (validadores de campo)

Los validators son funciones que se ejecutan sobre el valor antes de guardar. Se importan de `django.core.validators`.

```python
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
    MinLengthValidator, MaxLengthValidator,
    RegexValidator, EmailValidator,
    URLValidator, DecimalValidator,
    FileExtensionValidator, validate_image_file_extension
)

calificacion = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
)

codigo_postal = models.CharField(
    max_length=10,
    validators=[RegexValidator(r'^\d{4,8}$', 'Solo se permiten entre 4 y 8 dígitos.')]
)

documento = models.FileField(
    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
)
```

| Validator                        | Descripción |
|----------------------------------|-------------|
| `MinValueValidator(n)`           | Valor numérico mínimo |
| `MaxValueValidator(n)`           | Valor numérico máximo |
| `MinLengthValidator(n)`          | Longitud mínima de texto |
| `MaxLengthValidator(n)`          | Longitud máxima de texto |
| `RegexValidator(pattern)`        | El valor debe coincidir con la expresión regular |
| `EmailValidator()`               | Valida formato de email |
| `URLValidator()`                 | Valida formato de URL |
| `ProhibitNullCharactersValidator`| Bloquea caracteres nulos (`\x00`) en texto |
| `DecimalValidator(max_d, dec_p)` | Controla dígitos del decimal |
| `FileExtensionValidator([exts])` | Valida la extensión del archivo |
| `validate_image_file_extension`  | Valida que el archivo sea una imagen |
| `validate_ipv4_address`          | Valida IPv4 |
| `validate_ipv6_address`          | Valida IPv6 |
| `validate_comma_separated_integer_list` | Valida lista de enteros separados por coma |

---
