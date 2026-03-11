# Django — Módulo 7 · Clase 1

## Práctica: Menú Digital de Restaurante

---

> ⚠️ **PROHIBIDO ejecutar `migrate` sin la opción `--fake`. La base de datos ya existe y no puede ser modificada por Django bajo ninguna circunstancia.**

---

## El objetivo

Conectar un proyecto Django a una base de datos PostgreSQL existente, sin modificarla, y ver los datos del restaurante **"La Buena Mesa de Django"** en el panel de administración.

No se diseña la base de datos. No se corren consultas en el shell. La validación es simple: **abrir el admin en el navegador y ver los datos cargados**.

---

## Credenciales de la base de datos

El profesor te entrega los datos de conexión. Usa la opción según tu equipo:

### Opción A — Via Pooler (IPv4, recomendada)

Si tu equipo no soporta IPv6 o tienes problemas de conexión, usa esta:

```
Motor:      PostgreSQL
Host:       aws-0-us-west-2.pooler.supabase.com
Puerto:     6543
Nombre:     postgres
Usuario:    student_readonly.pepuqhrltqfdagvhoxxc
Contraseña: lectura123
```

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "supabase_ro": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "student_readonly.pepuqhrltqfdagvhoxxc",
        "PASSWORD": "lectura123",
        "HOST": "aws-0-us-west-2.pooler.supabase.com",
        "PORT": "6543",
    },
}
```

### Opción B — Conexión Directa (IPv6)

Solo si la Opción A no funciona:

```
Motor:      PostgreSQL
Host:       db.pepuqhrltqfdagvhoxxc.supabase.co
Puerto:     5432
Nombre:     postgres
Usuario:    student_readonly
Contraseña: lectura123
```

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "supabase_ro": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "student_readonly",
        "PASSWORD": "lectura123",
        "HOST": "db.pepuqhrltqfdagvhoxxc.supabase.co",
        "PORT": "5432",
    },
}
```

> ℹ️ **NOTA:** Estamos usando una **arquitectura híbrida**. El sistema de usuarios y administración de Django vivirá en tu archivo local `db.sqlite3` (base de datos `"default"`), pero los datos del restaurante vendrán de Supabase (base de datos `"supabase_ro"`).

---

---

# Paso a paso

---

## Paso 1 — Crear el proyecto Django

Crea un proyecto Django nuevo. Luego crea dentro una aplicación que llamarás `menu`.

---

## Paso 2 — Configurar la conexión a la base de datos

En el archivo de configuración del proyecto (`settings.py`) hay que registrar dos cosas:

**Primera:** Agregar la aplicación `menu` a la lista de aplicaciones instaladas (`INSTALLED_APPS`).

**Segunda:** Reemplazar el bloque `DATABASES` completo por el código que te entregó el profesor (el que tiene `default` y `supabase_ro`).

---

## Paso 3 — Escribir los modelos

Dentro de la app `menu`, en el archivo `models.py`, debes definir cuatro clases. A continuación se describe cada una en palabras — el código lo escribes tú.

---

### Modelo 1 — Categoria

Representa una categoría del menú (Entradas, Principales, Postres, Bebidas).

**Campos:**

| Campo       | Tipo de dato               | Restricciones                |
| ----------- | -------------------------- | ---------------------------- |
| nombre      | Texto corto (máx 100 car.) | Obligatorio                  |
| descripcion | Texto largo                | Opcional — puede estar vacío |

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor              | Para qué sirve                                |
| ----------- | ------------------ | --------------------------------------------- |
| managed     | False              | Django no toca la tabla — ya existe           |
| db_table    | `'menu_categoria'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 2 — Alergeno

Representa un alérgeno (gluten, lácteos, mariscos, etc.).

**Campos:**

| Campo  | Tipo de dato               | Restricciones |
| ------ | -------------------------- | ------------- |
| nombre | Texto corto (máx 100 car.) | Obligatorio   |

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor             | Para qué sirve                                |
| ----------- | ----------------- | --------------------------------------------- |
| managed     | False             | Django no toca la tabla — ya existe           |
| db_table    | `'menu_alergeno'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 3 — Ingrediente

Representa un ingrediente. Cada ingrediente puede tener varios alérgenos, y un alérgeno puede estar en muchos ingredientes.

**Campos:**

| Campo     | Tipo de dato               | Restricciones                                                  |
| --------- | -------------------------- | -------------------------------------------------------------- |
| nombre    | Texto corto (máx 100 car.) | Obligatorio                                                    |
| alergenos | Relación muchos a muchos   | Apunta al modelo `Alergeno` — puede estar vacío (`blank=True`) |

Para la relación muchos a muchos, define el campo `ManyToManyField` apuntando al modelo `Alergeno`. Con `managed = False` activo, Django no va a intentar crear ni modificar ninguna tabla, por lo que la conexión se resolverá correctamente.

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor                | Para qué sirve                                |
| ----------- | -------------------- | --------------------------------------------- |
| managed     | False                | Django no toca la tabla — ya existe           |
| db_table    | `'menu_ingrediente'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 4 — Plato

El corazón del sistema. Cada plato es un ítem del menú.

**Campos:**

| Campo              | Tipo de dato                       | Restricciones y comportamiento                     |
| ------------------ | ---------------------------------- | -------------------------------------------------- |
| nombre             | Texto corto (máx 200 car.)         | Obligatorio                                        |
| descripcion        | Texto largo                        | Obligatorio                                        |
| precio             | Decimal (10 dígitos, 2 decimales)  | Obligatorio — usar DecimalField, no FloatField     |
| tiempo_preparacion | Número entero                      | Obligatorio — minutos de preparación               |
| disponible         | Booleano                           | Obligatorio — valor por defecto: True              |
| creado_en          | Fecha y hora                       | Se completa automáticamente al crear el registro   |
| categoria          | Relación muchos-a-uno (ForeignKey) | Apunta al modelo `Categoria` — `on_delete=PROTECT` |
| ingredientes       | Relación muchos a muchos           | Apunta al modelo `Ingrediente` — puede estar vacío |

Para la relación muchos a muchos con ingredientes, define el campo `ManyToManyField` apuntando al modelo `Ingrediente`. Con `managed = False` activo, Django no intentará crear ninguna tabla adicional.

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor          | Para qué sirve                                |
| ----------- | -------------- | --------------------------------------------- |
| managed     | False          | Django no toca la tabla — ya existe           |
| db_table    | `'menu_plato'` | Nombre exacto de la tabla en la base de datos |

---

## Paso 4 — Registrar los modelos en el admin

En el archivo `admin.py` de la app `menu`, registra los cuatro modelos.

Como estamos usando dos bases de datos, debemos decirle a cada modelo del Admin que use la conexión de la base de datos externa. Para esto, agrega este método dentro de **cada clase** de tu `admin.py`:

```python
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

    def get_queryset(self, request):
        return super().get_queryset(request).using('supabase_ro')

admin.site.register(Categoria, CategoriaAdmin)
```

(Repite lo mismo para `AlergenoAdmin`, `IngredienteAdmin` y `PlatoAdmin`).

---

## Paso 5 — Las migraciones

Genera las migraciones con el comando habitual.

1. **Migración Real (SQLite):** Ejecuta `python manage.py migrate` para crear las tablas del Admin y Usuarios en tu archivo local.
2. **Migración Fake (Supabase):** Para la app `menu`, debemos simular que las tablas existen pero sin intentar crearlas en Supabase. Ejecuta:

```bash
python manage.py migrate menu --fake --database supabase_ro
```

---

## Paso 6 — Crear el superusuario

Para poder entrar al admin, necesitas una cuenta de administrador. Django tiene un comando para crearlo:

```
python manage.py createsuperuser
```

Elige el nombre de usuario, email y contraseña que quieras.

---

## Paso 7 — Instalar dependencias

Para que Django pueda hablar con una base de datos PostgreSQL, necesita un "traductor" o driver. El más común es `psycopg2`. Si no lo instalas, Django te dará un error al intentar conectar.

Ejecuta este comando en tu terminal (dentro de tu entorno virtual):

```bash
pip install psycopg2-binary
```

---

## Paso 8 — Iniciar el servidor y verificar

Inicia el servidor de desarrollo y abre el panel de administración en el navegador:

```
python manage.py runserver
```

Dirección del admin: `http://127.0.0.1:8000/admin/`

Ingresa con el superusuario que creaste. Si todo está bien configurado, deberías ver las cuatro secciones (Categorias, Alergenos, Ingredientes, Platos) con los datos del restaurante cargados.

---

## Validación

La práctica está completa cuando puedes mostrar al profesor:

- El admin abierto en el navegador con los cuatro modelos visibles
- Al hacer clic en "Platos", la lista muestra los 13 platos con sus categorías y precios
- Al hacer clic en cualquier plato, se ven todos sus datos incluyendo los ingredientes

No hay entrega de archivos. La validación es en pantalla.

---

## Solución de problemas comunes

Si al entrar al Admin y hacer clic en un modelo ves un error, no te asustes. Generalmente es uno de estos dos:

### 1. "Relation '...' does not exist"

**Qué significa:** Django está buscando una tabla que no existe con ese nombre.
**Solución:** Revisa el `db_table` dentro de la clase `Meta`. Debe ser exactamente igual al nombre de la tabla en Postgres (por ejemplo, `'menu_plato'`).

### 2. "Column '...' does not exist"

**Qué significa:** Django encontró la tabla, pero dentro de ella no hay una columna con el nombre que definiste en tu modelo.
**Solución:** Revisa el nombre del atributo en tu clase. Django usa el nombre del atributo como nombre de columna. Por ejemplo, si definiste `desc = models.TextField()` pero en la base de datos la columna se llama `descripcion`, fallará.

---

## Repositorio de consulta

Si te quedas atascado o quieres comparar tu solución final, puedes consultar el código de referencia en este repositorio:

🔗 [https://github.com/arielrosenmann94/modulo7_clase1](https://github.com/arielrosenmann94/modulo7_clase1)

---

## 🚀 Desafío para Avanzados

Si ya lograste ver los datos en el Admin, intenta resolver estas 10 preguntas conceptuales y técnicas. No requieren programar más, sino investigar y entender qué está pasando "bajo el capó":

1. **El Misterio de la Tabla ManyToMany:** En tu código solo definiste un campo en `Plato`. ¿Cómo sabe Django que existe una tabla llamada `menu_plato_ingredientes` sin que se lo digas explícitamente?
2. **Filtros en el Admin:** ¿Cómo podrías agregar una barra de búsqueda en el Admin para buscar platos por el nombre de sus ingredientes? (Investiga `search_fields` con doble guion bajo).
3. **El superpoder de `ReadOnlyField`:** Si el usuario es de solo lectura, ¿cómo podrías hacer que en el Admin todos los campos aparezcan como "solo lectura" automáticamente para evitar que el alumno intente editar y reciba un error de Postgres?
4. **Custom QuerySets:** ¿Cómo podrías hacer que el Admin de Platos, por defecto, **solo** muestre los platos que están disponibles, ocultando los que no tienen stock, sin que el usuario tenga que filtrar manualmente?
5. **Formato de Moneda:** En el `list_display` del Admin, el precio se ve como un número plano. ¿Cómo podrías crear un método en el modelo para que se vea con el signo `$` y puntos de miles?
6. **Contador de Relaciones:** ¿Cómo podrías mostrar en la lista de Categorías una columna que diga cuántos platos tiene cada una?
7. **La importancia de `__str__`:** Si quitas el método `__str__` de tus modelos, ¿cómo se verían los ingredientes dentro del formulario de un Plato? ¿Por qué esto es un problema de usabilidad?
8. **Seguridad en la Base de Datos:** Si el usuario es de solo lectura en Postgres, ¿por qué Django sigue mostrándote el botón "Añadir"? ¿Dónde vive la lógica que decide mostrar o no ese botón?
9. **Rendimiento (Select Related):** Si tienes 100 platos y cada uno muestra su categoría en la lista del Admin, Django está haciendo 101 consultas a la base de datos (problema N+1). ¿Cómo se soluciona esto en el `ModelAdmin`?
10. **Exploración de Metadatos:** ¿Existe alguna forma de que Django lea la base de datos de Supabase y te escriba el código de `models.py` automáticamente? (Investiga el comando `inspectdb`).

---
