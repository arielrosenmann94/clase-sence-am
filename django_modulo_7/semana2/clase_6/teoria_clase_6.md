# 🌌 Módulo 7 — Clase 6

## Migraciones en Django: El Control de Versiones de tu Base de Datos

> **AE 7.4** — Utiliza migraciones para la propagación de cambios al esquema de base de datos acorde al framework Django.

---

## 🗺️ Índice    

| #     | Tema                                         |
| ----- | -------------------------------------------- |
| **1** | Recap: ¿Dónde estamos?                       |
| **2** | ¿Qué es una migración? (La versión profunda) |
| 2.1   | La analogía del arquitecto                   |
| 2.2   | ¿Qué problema resuelven?                     |
| 2.3   | ¿Qué hay dentro de un archivo de migración?  |
| **3** | Los 3 Comandos que Debes Dominar             |
| 3.1   | `makemigrations` — Detectar los cambios      |
| 3.2   | `migrate` — Aplicar los cambios              |
| 3.3   | `showmigrations` — Diagnosticar el estado    |
| **4** | El Flujo Completo: De Modelo a Tabla         |
| 4.1   | Crear un modelo nuevo                        |
| 4.2   | Modificar un modelo existente                |
| 4.3   | Eliminar un campo                            |
| **5** | Cómo Django Sabe Qué Migraciones Ya Aplicó   |
| **6** | Errores Comunes y Cómo Resolverlos           |
| 6.1   | "No changes detected"                        |
| 6.2   | "Column does not exist"                      |
| 6.3   | "Conflicting migrations"                     |
| 6.4   | "You are trying to add a non-nullable field" |
| **7** | Buenas Prácticas Profesionales               |
| **8** | Tabla Resumen                                |

---

---

# 📚 1. Recap: ¿Dónde Estamos?

En la Clase 1 aprendimos que `makemigrations` genera instrucciones y `migrate` las aplica. Eso fue la superficie. Hoy vamos a entender **qué hay debajo**: qué contienen esos archivos, cómo Django controla qué se aplicó y qué no, y cómo resolver los problemas que aparecen cuando las cosas se complican.

| Lo que ya sabemos                  | Lo que vamos a profundizar hoy                          |
| :--------------------------------- | :------------------------------------------------------ |
| `makemigrations` genera un archivo | ¿Qué hay DENTRO de ese archivo?                         |
| `migrate` crea las tablas          | ¿Cómo sabe Django qué ya aplicó y qué falta?            |
| Si no migramos, la app falla       | ¿Cuáles son los errores específicos y cómo se arreglan? |
| Las migraciones son importantes    | ¿Cuáles son las buenas prácticas profesionales?         |

---

---

# 🔧 2. ¿Qué es una Migración? (La Versión Profunda)

---

## 2.1 La Analogía del Arquitecto

Imagina que eres un arquitecto trabajando en un edificio. Cada vez que el cliente pide un cambio ("agrega un baño", "quita esa pared", "pon una ventana más grande"), tú no destruyes el edificio y lo construyes de nuevo. En vez de eso, creas un **plano de la modificación** y se lo entregas al equipo de construcción.

En Django funciona exactamente igual:

```
TÚ (el arquitecto)           →  Modificas el modelo en Python
makemigrations (el plano)     →  Genera el archivo con las instrucciones del cambio
migrate (la construcción)     →  Aplica esas instrucciones a la base de datos real
```

Cada archivo de migración es como un plano de obra: documenta exactamente QUÉ cambió, CUÁNDO se creó, y en QUÉ ORDEN se debe aplicar.

---

## 2.2 ¿Qué Problema Resuelven?

Antes de que existieran las migraciones, los desarrolladores tenían que modificar la base de datos a mano escribiendo SQL directo. Esto generaba problemas graves:

| Sin migraciones                                         | Con migraciones                                       |
| :------------------------------------------------------ | :---------------------------------------------------- |
| Alguien modifica el modelo pero olvida actualizar la BD | Django detecta automáticamente los cambios            |
| Cada desarrollador tiene una BD diferente               | Todos aplican los mismos archivos en el mismo orden   |
| No hay registro de qué cambió                           | Cada cambio queda documentado en un archivo con fecha |
| Pasar cambios a producción es manual y riesgoso         | Un solo comando aplica todos los cambios pendientes   |
| Si algo sale mal, no hay forma fácil de volver atrás    | Las migraciones se pueden revertir                    |

> 💡 **Momento de reflexión:** Las migraciones son a la base de datos lo que Git es al código. Git registra cada cambio en tus archivos. Las migraciones registran cada cambio en la estructura de tu base de datos.

---

## 2.3 ¿Qué Hay Dentro de un Archivo de Migración?

Cuando ejecutas `makemigrations`, Django crea un archivo Python dentro de la carpeta `migrations/` de tu app. Veamos qué contiene:

```python
# migrations/0001_initial.py
# ↑ Django lo nombra automáticamente: 0001 = número de orden, initial = es la primera

from django.db import migrations, models
# ↑ Importa las herramientas que necesita para ejecutar las operaciones

class Migration(migrations.Migration):
    # ↑ Cada archivo de migración es una clase que hereda de Migration

    initial = True
    # ↑ Marca que esta es la primera migración de la app

    dependencies = [
    ]
    # ↑ Lista de migraciones que DEBEN aplicarse ANTES que esta.
    #   Si esta migración depende de otra app (ej: auth), aparece aquí.
    #   Django las aplica en el orden correcto automáticamente.

    operations = [
        migrations.CreateModel(
            name='Cliente',
            # ↑ El nombre del modelo que estamos creando

            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                # ↑ Django agrega el campo 'id' automáticamente

                ('nombre', models.CharField(max_length=100)),
                # ↑ Cada campo del modelo aparece aquí con su tipo exacto

                ('mail', models.EmailField(max_length=254)),

                ('activo', models.BooleanField(default=True)),
            ],
        ),
        # ↑ CreateModel = "crea esta tabla en la BD"
    ]
```

### Los tipos de operaciones más comunes

| Operación     | ¿Qué hace?                               | ¿Cuándo aparece?                               |
| :------------ | :--------------------------------------- | :--------------------------------------------- |
| `CreateModel` | Crea una tabla nueva                     | Cuando agregas un modelo nuevo                 |
| `AddField`    | Agrega una columna a una tabla existente | Cuando agregas un campo a un modelo existente  |
| `RemoveField` | Elimina una columna                      | Cuando borras un campo del modelo              |
| `AlterField`  | Modifica las propiedades de una columna  | Cuando cambias max_length, null, default, etc. |
| `RenameField` | Cambia el nombre de una columna          | Cuando renombras un campo                      |
| `DeleteModel` | Elimina una tabla completa               | Cuando borras un modelo entero                 |
| `AddIndex`    | Crea un índice en la tabla               | Cuando agregas índices en `Meta.indexes`       |

> ⚠️ **Regla de oro:** NUNCA modifiques manualmente un archivo de migración que ya fue aplicado. Si necesitas cambiar algo, crea una nueva migración con los cambios. Modificar migraciones aplicadas puede corromper la base de datos de todo el equipo.

---

---

# 🛠️ 3. Los 3 Comandos que Debes Dominar

---

## 3.1 `makemigrations` — Detectar los Cambios

Este comando compara el estado actual de tus modelos en Python con el estado de la última migración generada. Si encuentra diferencias, crea un nuevo archivo de migración.

```bash
python manage.py makemigrations
```

**Ejemplo de salida:**

```
Migrations for 'wallet':
  wallet/migrations/0002_cliente_telefono.py
    - Add field telefono to cliente
```

Django te dice exactamente:

- En qué app detectó cambios (`wallet`)
- Qué archivo creó (`0002_cliente_telefono.py`)
- Qué cambio detectó (`Add field telefono to cliente`)

### Generar migraciones para una app específica

Si tienes varias apps y solo quieres generar migraciones para una:

```bash
python manage.py makemigrations wallet
# Solo analiza la app 'wallet'
```

### Ver el SQL ANTES de aplicar

Si quieres ver qué SQL va a ejecutar una migración sin aplicarla:

```bash
python manage.py sqlmigrate wallet 0002
```

**Ejemplo de salida:**

```sql
ALTER TABLE "wallet_cliente" ADD COLUMN "telefono" varchar(15) DEFAULT '' NOT NULL;
ALTER TABLE "wallet_cliente" ALTER COLUMN "telefono" DROP DEFAULT;
```

Esto te permite revisar exactamente qué va a hacer Django en la base de datos antes de ejecutarlo.

---

## 3.2 `migrate` — Aplicar los Cambios

Este comando toma todas las migraciones que todavía NO se han aplicado y las ejecuta en orden contra la base de datos.

```bash
python manage.py migrate
```

**Ejemplo de salida:**

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, wallet
Running migrations:
  Applying wallet.0002_cliente_telefono... OK
```

Django muestra cada migración que aplica y si fue exitosa (`OK`) o falló.

### Aplicar migraciones de una sola app

```bash
python manage.py migrate wallet
# Solo aplica migraciones pendientes de la app 'wallet'
```

### Revertir una migración (volver atrás)

Si aplicaste una migración y te diste cuenta de que estuvo mal, puedes volver al estado anterior:

```bash
python manage.py migrate wallet 0001
# Revierte todo lo que se hizo DESPUÉS de la migración 0001
```

Django ejecuta la operación inversa: si la migración 0002 agregó una columna, la reversión la elimina.

> ⚠️ **Cuidado:** Revertir una migración puede causar pérdida de datos. Si la migración agregó una columna y ya guardaste datos en ella, al revertir esos datos se pierden.

---

## 3.3 `showmigrations` — Diagnosticar el Estado

Este comando muestra TODAS las migraciones del proyecto y si están aplicadas o no:

```bash
python manage.py showmigrations
```

**Ejemplo de salida:**

```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
wallet
 [X] 0001_initial
 [ ] 0002_cliente_telefono    ← Esta NO está aplicada todavía
```

| Símbolo | Significado                                                |
| :------ | :--------------------------------------------------------- |
| `[X]`   | Migración aplicada (ya está en la BD)                      |
| `[ ]`   | Migración pendiente (existe el archivo pero NO se ejecutó) |

> 💡 **Consejo:** Cuando algo falla, lo primero que debes hacer es ejecutar `showmigrations` para ver el estado real. Muchos errores se resuelven simplemente aplicando migraciones pendientes.

---

---

# 🔄 4. El Flujo Completo: De Modelo a Tabla

---

## 4.1 Crear un Modelo Nuevo

```
Paso 1: Escribir el modelo en models.py
   ↓
Paso 2: python manage.py makemigrations
   ↓    (Django genera el archivo 0001_initial.py)
Paso 3: python manage.py migrate
   ↓    (Django crea la tabla en la BD)
Paso 4: Verificar con showmigrations que aparezca [X]
```

---

## 4.2 Modificar un Modelo Existente

Imagina que después de crear el modelo `Cliente`, el cliente pide que agreguemos un campo `telefono`:

**Paso 1 — Modificar el modelo:**

```python
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email  = models.EmailField()
    activo = models.BooleanField(default=True)
    telefono = models.CharField(max_length=15, blank=True, default='')
    # ↑ Nuevo campo. blank=True para que formularios no lo exijan.
    #   default='' para que los clientes existentes tengan un valor inicial.
```

**Paso 2 — Generar la migración:**

```bash
python manage.py makemigrations
# Salida: wallet/migrations/0002_cliente_telefono.py
#         - Add field telefono to cliente
```

**Paso 3 — Aplicar la migración:**

```bash
python manage.py migrate
# Salida: Applying wallet.0002_cliente_telefono... OK
```

**Paso 4 — Verificar:**

```bash
python manage.py showmigrations wallet
# wallet
#  [X] 0001_initial
#  [X] 0002_cliente_telefono   ← Aplicada
```

---

## 4.3 Eliminar un Campo

Si decidimos que ya no necesitamos el campo `telefono`:

**Paso 1:** Eliminar la línea del modelo.
**Paso 2:** `makemigrations` → Django genera una migración con `RemoveField`.
**Paso 3:** `migrate` → Django ejecuta `ALTER TABLE ... DROP COLUMN ...`.

> ⚠️ **Importante:** Al eliminar un campo, todos los datos almacenados en esa columna se pierden definitivamente. Asegúrate de hacer un respaldo antes si los datos son importantes.

---

---

# 🧠 5. Cómo Django Sabe Qué Migraciones Ya Aplicó

Django mantiene una tabla especial en la base de datos llamada `django_migrations`. Cada vez que ejecutas `migrate` y una migración se aplica exitosamente, Django agrega una fila a esta tabla:

```
Tabla: django_migrations
┌────┬──────────┬──────────────────────────┬─────────────────────────┐
│ id │ app      │ name                     │ applied                 │
├────┼──────────┼──────────────────────────┼─────────────────────────┤
│ 1  │ admin    │ 0001_initial             │ 2025-03-01 10:00:00     │
│ 2  │ auth     │ 0001_initial             │ 2025-03-01 10:00:00     │
│ 3  │ wallet   │ 0001_initial             │ 2025-03-15 14:30:00     │
│ 4  │ wallet   │ 0002_cliente_telefono    │ 2025-03-17 09:15:00     │
└────┴──────────┴──────────────────────────┴─────────────────────────┘
```

Cuando ejecutas `migrate`, Django:

1. Lee todos los archivos de migración de la carpeta `migrations/`.
2. Consulta la tabla `django_migrations` para ver cuáles ya están registradas.
3. Las que NO están en la tabla → las aplica.
4. Las que YA están en la tabla → las salta.

> 💡 **Por eso `showmigrations` funciona:** compara los archivos de la carpeta `migrations/` con las filas de la tabla `django_migrations`. Si un archivo existe pero no tiene fila → aparece como `[ ]`.

---

---

# 🚨 6. Errores Comunes y Cómo Resolverlos

---

## 6.1 "No changes detected"

**Cuándo aparece:**

```bash
python manage.py makemigrations
# No changes detected
```

**Causas más frecuentes:**

| Causa                                                           | Solución                                                                               |
| :-------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| La app no está en `INSTALLED_APPS`                              | Agregarla en `settings.py`                                                             |
| Guardaste el archivo pero no lo importaste correctamente        | Verificar que el modelo esté importado en `__init__.py` si usas `models/` como paquete |
| No hay diferencias reales entre el modelo y la última migración | Revisar que realmente hayas cambiado algo                                              |

```bash
# Truco: forzar que Django busque en una app específica
python manage.py makemigrations wallet
```

---

## 6.2 "Column does not exist" / "no such column"

**Cuándo aparece:** Al intentar usar la app (acceder a una vista, cargar el admin, ejecutar una consulta).

**Causa:** El modelo tiene un campo que no existe en la base de datos porque la migración no fue aplicada.

**Solución:**

```bash
# Paso 1: Ver qué migraciones están pendientes
python manage.py showmigrations

# Paso 2: Aplicar las pendientes
python manage.py migrate
```

---

## 6.3 "Conflicting migrations"

**Cuándo aparece:** Cuando dos desarrolladores crearon migraciones diferentes al mismo tiempo y las fusionaron (merge) en Git.

**Ejemplo:**

```
wallet/migrations/
├── 0001_initial.py
├── 0002_cliente_telefono.py    ← Desarrollador A
├── 0002_cliente_direccion.py   ← Desarrollador B (mismo número!)
```

**Solución:**

```bash
python manage.py makemigrations --merge
# Django crea una migración 0003 que combina ambas
```

---

## 6.4 "You are trying to add a non-nullable field"

**Cuándo aparece:** Al agregar un campo nuevo que no puede ser NULL y no tiene valor por defecto.

**Ejemplo:** Agregas `telefono = models.CharField(max_length=15)` sin `default` ni `null=True`.

Django pregunta: _"Los clientes que ya existen en la BD no tienen teléfono. ¿Qué valor les pongo?"_

```
You are trying to add a non-nullable field 'telefono' to cliente
without a default; we can't do that.
Please select a fix:
 1) Provide a one-off default now
 2) Quit, and let me add a default in models.py
```

**Solución:** Siempre define un valor por defecto o permite NULL en campos nuevos:

```python
# Opción A: valor por defecto
telefono = models.CharField(max_length=15, default='', blank=True)

# Opción B: permitir NULL
telefono = models.CharField(max_length=15, null=True, blank=True)
```

---

---

# ✅ 7. Buenas Prácticas Profesionales

---

### 1. Migraciones pequeñas y frecuentes

No acumules 10 cambios para una sola migración. Cada cambio → `makemigrations` → `migrate`. Esto hace que sea fácil revertir un cambio específico sin afectar los demás.

### 2. Siempre revisa antes de aplicar

```bash
# Ver qué SQL se va a ejecutar
python manage.py sqlmigrate wallet 0002

# Ver qué migraciones están pendientes
python manage.py showmigrations
```

### 3. NUNCA modifiques una migración ya aplicada

Si la migración 0001 ya fue aplicada (por ti o por alguien del equipo), no edites ese archivo. Crea una migración nueva con los cambios. Modificar migraciones aplicadas rompe la sincronización entre la BD y los archivos.

### 4. Incluye los archivos de migración en Git

Los archivos de la carpeta `migrations/` **sí se suben** al repositorio. Así todo el equipo tiene las mismas migraciones en el mismo orden.

### 5. Verifica el estado antes de cada deploy

```bash
python manage.py showmigrations
python manage.py migrate
```

### 6. Nuevos campos siempre con default o null

Cuando agregas un campo a un modelo que ya tiene datos, SIEMPRE define `default=` o `null=True`. De lo contrario, Django no sabe qué valor ponerle a los registros existentes.

---

---

# 🏁 8. Tabla Resumen

| Comando            | ¿Qué hace?                                                        | ¿Cuándo usarlo?                       |
| :----------------- | :---------------------------------------------------------------- | :------------------------------------ |
| `makemigrations`   | Genera un archivo de migración a partir de cambios en los modelos | Después de cada cambio en `models.py` |
| `migrate`          | Aplica las migraciones pendientes a la BD                         | Después de `makemigrations`           |
| `showmigrations`   | Muestra el estado de todas las migraciones                        | Para diagnosticar problemas           |
| `sqlmigrate app N` | Muestra el SQL que ejecutaría una migración                       | Para revisar antes de aplicar         |
| `migrate app N`    | Revierte a la migración número N                                  | Para deshacer una migración           |

| Concepto                 | Significado                                                                  |
| :----------------------- | :--------------------------------------------------------------------------- |
| **Archivo de migración** | Un archivo Python que describe UN cambio en la estructura de la BD           |
| **dependencies**         | Lista de migraciones que deben aplicarse ANTES que la actual                 |
| **operations**           | La lista de cambios que esta migración ejecuta (CreateModel, AddField, etc.) |
| **django_migrations**    | Tabla interna donde Django registra qué migraciones ya aplicó                |
| **`[X]`**                | Migración aplicada (está en la BD)                                           |
| **`[ ]`**                | Migración pendiente (el archivo existe pero no se ejecutó)                   |

---

## 📚 Bibliografía y Fuentes

- _Django Software Foundation. (2024). Migrations — Django documentation._ [https://docs.djangoproject.com/en/stable/topics/migrations/](https://docs.djangoproject.com/en/stable/topics/migrations/)
- _Django Software Foundation. (2024). Migration Operations._ [https://docs.djangoproject.com/en/stable/ref/migration-operations/](https://docs.djangoproject.com/en/stable/ref/migration-operations/)
- _Vitor Freitas. (2024). How to Reset Migrations — Simple is Better Than Complex._ [https://simpleisbetterthancomplex.com/](https://simpleisbetterthancomplex.com/)

---
