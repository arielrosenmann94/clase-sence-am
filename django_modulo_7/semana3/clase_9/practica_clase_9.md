# 🚀 Práctica Clase 9: Sistema CRUD Completo para una Clínica Veterinaria Ficticia

## Contexto del Proyecto

> "El 73% de las empresas pequeñas aún gestionan datos de clientes en hojas de cálculo, lo que causa pérdidas de información y errores humanos frecuentes."
> — _Fuente: McKinsey Digital, Small Business Technology Report (2024)_

La **Clínica Veterinaria "PatasFelices"** (empresa ficticia) necesita digitalizar urgentemente su sistema de gestión. Actualmente llevan todo en cuadernos y planillas Excel: datos de dueños, mascotas, y consultas médicas. Pierden fichas, duplican información y no pueden buscar historiales.

Tu misión: construir desde cero una aplicación Django funcional que les permita gestionar estos datos con operaciones CRUD completas, accesibles desde el navegador.

---

## Objetivos de la Práctica

- [ ] Crear un proyecto Django completo desde cero con múltiples modelos relacionados.
- [ ] Separar la configuración en `base.py`, `development.py` y `production.py`.
- [ ] Configurar variables de entorno con `.env` para proteger datos sensibles.
- [ ] Conectar SQLite en desarrollo y Supabase (PostgreSQL) en producción.
- [ ] Implementar vistas basadas en clases para todas las operaciones CRUD.
- [ ] Crear templates HTML funcionales con formularios protegidos por CSRF.
- [ ] Configurar el enrutamiento completo de la aplicación.
- [ ] Registrar modelos en el admin con personalización básica.
- [ ] Verificar el flujo completo: crear, listar, editar y eliminar registros desde el navegador.

---

## 📁 Fase 1: Cimientos del Proyecto

> "La arquitectura de software es como los cimientos de un edificio: invisible para el usuario, pero si está mal hecha, todo lo que construyas encima se derrumba."
> — _Fuente: Robert C. Martin, Clean Architecture (2017)_

### Instrucciones:

1. Crea un proyecto Django llamado `veterinaria_patasfelices`.
2. Crea una aplicación llamada `fichas`.
3. Registra la app en `INSTALLED_APPS`.
4. Crea la carpeta `templates/fichas/` y configura `DIRS` en `settings.py`.
5. Ejecuta el servidor y verifica que el cohete de Django aparezca.

### Estructura esperada al terminar esta fase:

```
veterinaria_patasfelices/
├── manage.py
├── veterinaria_patasfelices/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── fichas/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── ...
└── templates/
    └── fichas/
```

---

## ⚙️ Fase 2: Separación de Settings y Variables de Entorno

> "El 45% de las brechas de seguridad en aplicaciones web se deben a configuraciones incorrectas o credenciales expuestas en el código fuente."
> — _Fuente: OWASP Top 10 Report (2024)_

En un proyecto profesional **nunca** se usa el mismo `settings.py` para desarrollo y producción. Vamos a dividir la configuración en tres archivos y proteger los datos sensibles con variables de entorno.

### Paso 1: Instalar dependencias

Instala los siguientes paquetes con `pip install`:

| Paquete           | ¿Para qué sirve?                                              |
| :---------------- | :------------------------------------------------------------ |
| `python-dotenv`   | Cargar variables de entorno desde un archivo `.env`           |
| `dj-database-url` | Convertir una URL de base de datos en la configuración Django |
| `psycopg2-binary` | Driver para conectar Python con PostgreSQL (Supabase)         |

### Paso 2: Crear la carpeta `settings/`

Dentro de tu carpeta de configuración (`veterinaria_patasfelices/`), transforma el archivo `settings.py` en una **carpeta** con la siguiente estructura.

Puedes usar comandos como `mkdir`, `mv` y `touch` en tu terminal para lograr esto:
- Crea la carpeta `settings`.
- Mueve el `settings.py` original a `settings/base.py`.
- Crea los archivos `__init__.py`, `development.py` y `production.py` dentro de la nueva carpeta `settings`.

### Estructura resultante:

```
veterinaria_patasfelices/
├── settings/                  ← Ahora es una CARPETA
│   ├── __init__.py            ← Elige qué entorno cargar
│   ├── base.py                ← Configuración COMÚN
│   ├── development.py         ← Solo desarrollo (SQLite)
│   └── production.py          ← Solo producción (Supabase)
├── urls.py
├── wsgi.py
└── asgi.py
```

### Paso 3: Crear el archivo `.env`

En la **raíz del proyecto** (donde está `manage.py`), crea un archivo `.env` con las siguientes variables:
- `DJANGO_ENV` — para elegir entorno (`development` o `production`)
- `SECRET_KEY` — clave secreta del proyecto (genera una nueva, no uses la que viene por defecto)
- `DEBUG` — `True` en desarrollo
- `DATABASE_URL` — la URL de conexión a PostgreSQL (la obtienes de Supabase)

Crea también un `.env.example` con los mismos campos pero **sin datos reales** — este archivo SÍ va a Git como referencia para otros desarrolladores.

### Paso 3.5: Crear el archivo `.gitignore`

En la **raíz del proyecto**, crea un archivo `.gitignore` que excluya al menos:

| Archivo / Carpeta       | ¿Por qué se ignora?                                |
| :---------------------- | :------------------------------------------------- |
| `.env`                  | Contiene credenciales y datos sensibles             |
| `db.sqlite3`            | Base de datos local, no debe subirse al repo        |
| `__pycache__/`          | Archivos compilados de Python                       |
| `*.pyc`                 | Bytecode de Python                                  |
| `venv/` o `.venv/`      | Entorno virtual — cada dev crea el suyo             |
| `*.log`                 | Archivos de log                                     |

> 💡 **Tip:** Busca "gitignore django" en [gitignore.io](https://www.toptal.com/developers/gitignore) para generar uno más completo.

> ⚠️ **Si ya subiste el `.env` por accidente**, quitarlo del `.gitignore` no lo borra del historial. Investiga `git rm --cached .env` para corregirlo.

### Paso 4: Configurar `__init__.py`

En `settings/__init__.py` debes:
1. Importar `os` y `load_dotenv` de `dotenv`.
2. Llamar a `load_dotenv()` para que lea tu `.env`.
3. Leer la variable `DJANGO_ENV` con `os.getenv()`.
4. Según el valor, importar todos los settings de `production.py` o `development.py`.

> 📖 **Referencia:** Revisa cómo funciona el import `from .modulo import *` en la documentación de Python sobre paquetes.

### Paso 5: Limpiar `base.py`

En `base.py` (tu antiguo `settings.py`), haz estos cambios:

1. **Quita** la línea de `SECRET_KEY` hardcodeada y reemplázala leyéndola desde `os.getenv()` (con un valor por defecto inseguro solo para desarrollo).
2. **Quita** la línea `DEBUG = True` (cada entorno la define).
3. **Quita** el bloque `DATABASES` completo (cada entorno lo define).
4. **Deja todo lo demás**: `INSTALLED_APPS`, `MIDDLEWARE`, `TEMPLATES`, `AUTH_PASSWORD_VALIDATORS`, etc.

### Paso 6: Configurar `development.py` (SQLite)

Este archivo debe:
- Importar todo desde `base.py` con `from .base import *`
- Definir `DEBUG = True`
- Definir `ALLOWED_HOSTS` para localhost
- Configurar `DATABASES` para usar SQLite (el engine es `django.db.backends.sqlite3`)

> 📖 **Referencia:** Busca en la documentación de Django la sección de [DATABASES setting](https://docs.djangoproject.com/en/stable/ref/settings/#databases).

### Paso 7: Configurar `production.py` (Supabase PostgreSQL)

Este archivo debe:
- Importar todo desde `base.py`
- Definir `DEBUG = False`
- Leer `ALLOWED_HOSTS` desde variables de entorno
- Usar `dj_database_url.config()` para leer la `DATABASE_URL` del `.env` y configurar PostgreSQL con SSL

> 📖 **Referencia:** Revisa la documentación de [dj-database-url](https://pypi.org/project/dj-database-url/) para ver cómo se usa `config()`.

### Paso 8: Crear proyecto en Supabase

1. Entra a [https://supabase.com/](https://supabase.com/) y crea una cuenta gratuita.
2. Crea un nuevo proyecto.
3. Ve a **Project Settings → Database** y copia la **Connection String (URI)**.
4. Pégala en tu archivo `.env` como valor de `DATABASE_URL`.

### Paso 9: Verificar ambos entornos

**Verificar desarrollo (SQLite):**

```bash
# Asegúrate de que .env tiene DJANGO_ENV=development
python manage.py runserver
# Si funciona → ✅ desarrollo con SQLite OK
```

**Verificar producción (Supabase):**

```bash
# Cambia en .env: DJANGO_ENV=production
python manage.py migrate
# Si las migraciones se aplican en Supabase → ✅ producción OK
# Vuelve a cambiar a DJANGO_ENV=development para seguir trabajando
```

### Checklist de esta fase:

- [ ] Carpeta `settings/` creada con `__init__.py`, `base.py`, `development.py`, `production.py`.
- [ ] Archivo `.env` creado con `DJANGO_ENV`, `SECRET_KEY`, `DEBUG`, `DATABASE_URL`.
- [ ] Archivo `.env.example` creado (sin datos reales).
- [ ] `.env` agregado al `.gitignore`.
- [ ] `python manage.py runserver` funciona en modo `development` (SQLite).
- [ ] Migraciones se aplican correctamente en Supabase al cambiar a `production`.

---

## 📋 Fase 3: Modelado de Datos (Tres Modelos Relacionados)

> "Un modelo de datos bien diseñado es la inversión más rentable en un proyecto de software: reduce bugs, simplifica consultas y acelera el desarrollo futuro."
> — _Fuente: Martin Fowler, Patterns of Enterprise Application Architecture (2003)_

La clínica necesita registrar tres tipos de información relacionados entre sí:

### Modelo 1: `Dueno` (Dueño de la mascota)

| Campo       | Tipo         | Restricciones                  |
| :---------- | :----------- | :----------------------------- |
| `nombre`    | `CharField`  | `max_length=100`               |
| `rut`       | `CharField`  | `max_length=12`, `unique=True` |
| `telefono`  | `CharField`  | `max_length=20`                |
| `email`     | `EmailField` | `blank=True`                   |
| `direccion` | `TextField`  | `blank=True`                   |

### Modelo 2: `Mascota`

| Campo              | Tipo         | Restricciones                                |
| :----------------- | :----------- | :------------------------------------------- |
| `nombre`           | `CharField`  | `max_length=80`                              |
| `especie`          | `CharField`  | `max_length=50` (ej: "Perro", "Gato", "Ave") |
| `raza`             | `CharField`  | `max_length=80`, `blank=True`                |
| `fecha_nacimiento` | `DateField`  | `null=True`, `blank=True`                    |
| `dueno`            | `ForeignKey` | Relación con `Dueno`, `on_delete=CASCADE`    |

### Modelo 3: `ConsultaMedica`

| Campo         | Tipo            | Restricciones                                    |
| :------------ | :-------------- | :----------------------------------------------- |
| `mascota`     | `ForeignKey`    | Relación con `Mascota`, `on_delete=CASCADE`      |
| `fecha`       | `DateTimeField` | `auto_now_add=True`                              |
| `motivo`      | `CharField`     | `max_length=200`                                 |
| `diagnostico` | `TextField`     |                                                  |
| `tratamiento` | `TextField`     | `blank=True`                                     |
| `costo`       | `DecimalField`  | `max_digits=10`, `decimal_places=2`, `default=0` |

### Diagrama de relaciones:

```
Dueno ──── 1:N ────► Mascota ──── 1:N ────► ConsultaMedica
 │                     │                       │
 Un dueño tiene        Una mascota tiene       Cada consulta
 muchas mascotas       muchas consultas         pertenece a
                                                una mascota
```

### Tareas:

1. Define los tres modelos en `fichas/models.py`.
2. Agrega `__str__` a cada modelo para que sean legibles en el admin.
3. Agrega `class Meta` con `ordering` y `verbose_name` a cada modelo.
4. Ejecuta `makemigrations` y `migrate`.
5. Verifica con `showmigrations` que todo esté aplicado.

---

## 🔑 Fase 4: Panel de Administración Personalizado

> "Django admin no es solo una herramienta de desarrollo, es una interfaz de producción que el 42% de las startups usa como backoffice en sus primeras versiones."
> — _Fuente: Django Developers Survey, JetBrains (2024)_

No basta con registrar modelos. Un admin bien configurado hace que los datos sean fáciles de gestionar.

### Instrucciones:

1. Registra los tres modelos en `fichas/admin.py` usando el decorador `@admin.register()`.
2. Para cada modelo, crea una clase que herede de `admin.ModelAdmin` y personaliza:
   - `list_display`: los campos que quieres mostrar como columnas en la lista.
   - `search_fields`: los campos por los que se puede buscar.
3. Para `Dueno`, muestra `nombre`, `rut`, `telefono` y `email`.
4. Para `Mascota`, muestra `nombre`, `especie`, `raza` y el nombre del dueño.
5. Para `ConsultaMedica`, muestra `mascota`, `motivo`, `fecha` y `costo`.

> 📖 **Referencia:** Revisa la documentación de [ModelAdmin options](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options) para ver las opciones disponibles.

6. Crea un **superusuario** con `python manage.py createsuperuser` y verifica desde `/admin/` que puedes:
   - Crear al menos 2 dueños.
   - Crear al menos 3 mascotas (asociadas a los dueños).
   - Crear al menos 2 consultas médicas (asociadas a las mascotas).

---

## 🖥️ Fase 5: Vistas CRUD con Class-Based Views

> "Las vistas genéricas de Django reducen entre un 60% y un 80% el código necesario para operaciones CRUD estándar."
> — _Fuente: Two Scoops of Django, D. Feldroy & A. Feldroy (2024)_

Ahora vamos a crear las vistas para que el CRUD funcione desde el navegador, no solo desde el admin.

### Instrucciones:

Crea en `fichas/views.py` las siguientes vistas:

#### Para Dueños (5 vistas):

| Vista             | Clase Base   | Template esperado                  |
| :---------------- | :----------- | :--------------------------------- |
| `DuenoListView`   | `ListView`   | `fichas/dueno_list.html`           |
| `DuenoDetailView` | `DetailView` | `fichas/dueno_detail.html`         |
| `DuenoCreateView` | `CreateView` | `fichas/dueno_form.html`           |
| `DuenoUpdateView` | `UpdateView` | `fichas/dueno_form.html`           |
| `DuenoDeleteView` | `DeleteView` | `fichas/dueno_confirm_delete.html` |

#### Para Mascotas (5 vistas):

| Vista               | Clase Base   | Template esperado                    |
| :------------------ | :----------- | :----------------------------------- |
| `MascotaListView`   | `ListView`   | `fichas/mascota_list.html`           |
| `MascotaDetailView` | `DetailView` | `fichas/mascota_detail.html`         |
| `MascotaCreateView` | `CreateView` | `fichas/mascota_form.html`           |
| `MascotaUpdateView` | `UpdateView` | `fichas/mascota_form.html`           |
| `MascotaDeleteView` | `DeleteView` | `fichas/mascota_confirm_delete.html` |

### Tips:

- Usa `reverse_lazy('fichas:dueno_lista')` como `success_url`.
- En `fields`, incluye todos los campos editables (no `fecha_registro` ni `auto_now_add`).
- Para `MascotaCreateView` incluye el campo `dueno` en `fields` para que el usuario pueda seleccionar el dueño desde un dropdown.

---

## 🔗 Fase 6: Enrutamiento Completo

> "Una aplicación web sin rutas claras es como una ciudad sin señalética: los usuarios se pierden y abandonan."
> — _Fuente: Steve Krug, Don't Make Me Think (2014)_

### Instrucciones:

1. Crea el archivo `fichas/urls.py`.
2. Define un `app_name = 'fichas'` para el namespace.
3. Define las siguientes 10 rutas usando `path()` y `.as_view()`:

| URL                         | Vista                  | Name              |
| :-------------------------- | :--------------------- | :---------------- |
| `duenos/`                   | `DuenoListView`        | `dueno_lista`     |
| `duenos/<int:pk>/`          | `DuenoDetailView`      | `dueno_detalle`   |
| `duenos/nuevo/`             | `DuenoCreateView`      | `dueno_crear`     |
| `duenos/editar/<int:pk>/`   | `DuenoUpdateView`      | `dueno_editar`    |
| `duenos/eliminar/<int:pk>/` | `DuenoDeleteView`      | `dueno_eliminar`  |
| `mascotas/`                 | `MascotaListView`      | `mascota_lista`   |
| `mascotas/<int:pk>/`        | `MascotaDetailView`    | `mascota_detalle` |
| `mascotas/nuevo/`           | `MascotaCreateView`    | `mascota_crear`   |
| `mascotas/editar/<int:pk>/` | `MascotaUpdateView`    | `mascota_editar`  |
| `mascotas/eliminar/<int:pk>/`| `MascotaDeleteView`   | `mascota_eliminar`|

4. En el `urls.py` del proyecto, usa `include('fichas.urls')` para conectar las rutas de la app.

> 📖 **Referencia:** Revisa la sección de la teoría sobre enrutamiento y cómo funciona `<int:pk>` y `as_view()`.

---

## 🎨 Fase 7: Templates HTML con Formularios CSRF

> "El 85% de las vulnerabilidades web podrían evitarse implementando correctamente tokens CSRF y validación del lado del servidor."
> — _Fuente: OWASP, Web Application Security Testing Guide (2024)_

Crea los templates necesarios. Todos deben incluir `{% csrf_token %}` en los formularios.

### Template base (`templates/fichas/base.html`):

Crea un template base que todos los demás extiendan. Debe incluir:
- Estructura HTML5 con `lang="es"`, charset UTF-8 y viewport responsive.
- Un `<title>` con un `{% block title %}` para que cada página pueda personalizarlo.
- Estilos básicos para body, navegación, tablas, botones y formularios.
- Una barra de navegación `<nav>` con links a las listas de dueños y mascotas, y a los formularios de creación. Usa `{% url 'fichas:nombre_ruta' %}` para los links.
- Un `{% block content %}{% endblock %}` donde cada template hijo inyecta su contenido.

> 📖 **Referencia:** Revisa la sección de la teoría sobre templates y herencia de templates. Busca en la documentación de Django `template inheritance`.

### Templates a crear:

Ahora crea cada template. Todos deben extender de `base.html`:

#### 1. `dueno_list.html` — Lista de dueños

- Extiende de `base.html`.
- Muestra una tabla con columnas: Nombre, RUT, Teléfono, Email, Acciones.
- En "Acciones", agrega links de Ver, Editar y Eliminar usando `{% url %}`.
- Si no hay dueños, muestra un mensaje: "No hay dueños registrados aún."

#### 2. `dueno_detail.html` — Detalle de un dueño

- Muestra todos los datos del dueño.
- **Desafío:** Debajo de los datos del dueño, muestra una lista con las mascotas del dueño (`dueno.mascota_set.all`).
- Agrega botones para Editar y Eliminar el dueño.
- Agrega un link "Registrar mascota" para este dueño.

#### 3. `dueno_form.html` — Formulario para crear/editar dueño

- Usa `{{ form.as_p }}` para renderizar el formulario.
- Incluye `{% csrf_token %}`.
- Agrega un botón de "Guardar".
- Agrega un link "Cancelar" que vuelva a la lista.

#### 4. `dueno_confirm_delete.html` — Confirmación de eliminación

- Muestra un mensaje: "¿Estás seguro de que deseas eliminar al dueño **{{ object.nombre }}**?"
- Muestra un formulario con `{% csrf_token %}` y un botón "Confirmar eliminación".
- Agrega un link "Cancelar" que vuelva a la lista.

#### 5. Repite los templates para Mascotas:

- `mascota_list.html` — Tabla con: Nombre, Especie, Raza, Dueño, Acciones.
- `mascota_detail.html` — Datos de la mascota + lista de consultas médicas.
- `mascota_form.html` — Formulario con CSRF.
- `mascota_confirm_delete.html` — Confirmación de eliminación.

---

## ✅ Fase 8: Verificación Completa

> "Un software no probado es un software que no funciona — solo que aún no lo sabes."
> — _Fuente: Kent Beck, Test-Driven Development (2003)_

Ejecuta el servidor y verifica **cada uno** de los siguientes flujos:

### Checklist de verificación:

#### Dueños:

- [ ] Acceder a `/duenos/` muestra la lista (vacía o con datos).
- [ ] Hacer clic en "Nuevo Dueño" abre un formulario limpio.
- [ ] Llenar y enviar el formulario crea un dueño y redirige a la lista.
- [ ] Hacer clic en "Ver" abre el detalle del dueño con sus mascotas.
- [ ] Hacer clic en "Editar" abre el formulario con los datos cargados.
- [ ] Modificar un campo y guardar actualiza el registro.
- [ ] Hacer clic en "Eliminar" muestra la confirmación.
- [ ] Confirmar la eliminación borra el dueño y redirige a la lista.

#### Mascotas:

- [ ] Acceder a `/mascotas/` muestra la lista con el nombre del dueño.
- [ ] Crear una mascota permite seleccionar el dueño desde un dropdown.
- [ ] El detalle de la mascota muestra sus consultas médicas.
- [ ] Editar y eliminar funcionan correctamente.

#### Seguridad:

- [ ] Todos los formularios POST tienen `{% csrf_token %}`.
- [ ] Si quito el `{% csrf_token %}` del template y envío el formulario, Django devuelve error 403.

---

## 🌟 Bonus (Para quienes terminen antes)

> "La diferencia entre un desarrollador junior y uno senior no es que el senior sepa más, sino que el senior anticipa los problemas antes de que aparezcan."
> — _Fuente: The Pragmatic Programmer, Hunt & Thomas (2019)_

Si terminaste todo lo anterior, intenta estos desafíos adicionales:

### Bonus 1: CRUD de Consultas Médicas

Agrega las 5 vistas CRUD para `ConsultaMedica`:

- El formulario debe permitir seleccionar la mascota.
- La lista debe mostrar: mascota, motivo, fecha y costo.
- En el detalle de una mascota, agrega un link "Nueva consulta" que pase la mascota preseleccionada.

### Bonus 2: Agregar un template `inicio.html`

Crea una página de inicio (`/`) que muestre:

- Total de dueños registrados.
- Total de mascotas registradas.
- Total de consultas realizadas.
- Links rápidos para crear dueño, mascota y consulta.

> **Tip:** Usa una vista basada en función con `Dueno.objects.count()` y pasa los totales al template con el `context`.

### Bonus 3: Mensajes de éxito

Usa `django.contrib.messages` para mostrar un mensaje de éxito después de crear, editar o eliminar un registro. Investiga cómo sobreescribir el método `form_valid()` en las CBV para agregar el mensaje.

---

## 🔥 Requerimientos Avanzados

### Avanzado 1: Paginación
Implementa paginación en `DuenoListView` y `MascotaListView` para que muestren máximo 10 registros por página. Investiga `paginate_by` en las CBV y los controles de navegación en el template.

### Avanzado 2: Validaciones personalizadas en el modelo
Agrega un método `clean()` en el modelo `Dueno` que valide que el RUT tenga un formato válido (ej: `12.345.678-9`). Usa `ValidationError` de `django.core.exceptions`.

### Avanzado 3: Filtro de búsqueda en la lista
Agrega un campo de búsqueda en `dueno_list.html` que permita filtrar dueños por nombre o RUT. Sobreescribe `get_queryset()` en la vista para leer el parámetro `?q=` de la URL y filtrar los resultados.

---

## 📝 Resumen del Entregable

| #   | Requisito                                                                          | Estado |
| :-- | :--------------------------------------------------------------------------------- | :----- |
| 1   | Proyecto `veterinaria_patasfelices` creado y servidor funcional                    | [ ]    |
| 2   | App `fichas` registrada en `INSTALLED_APPS`                                        | [ ]    |
| 3   | Settings separados en `base.py`, `development.py` y `production.py`                | [ ]    |
| 4   | `.env` con variables de entorno + `.env.example` + `.gitignore` configurado        | [ ]    |
| 5   | Desarrollo con SQLite y producción con Supabase (PostgreSQL) verificados           | [ ]    |
| 6   | 3 modelos definidos con `__str__`, `Meta` y relaciones FK                          | [ ]    |
| 7   | Migraciones generadas y aplicadas                                                  | [ ]    |
| 8   | 3 modelos registrados en admin con `list_display` y `search_fields`                | [ ]    |
| 9   | 10 vistas CBV creadas (5 para Dueño + 5 para Mascota)                              | [ ]    |
| 10  | `urls.py` de la app con 10 rutas + incluido en el `urls.py` del proyecto           | [ ]    |
| 11  | 8 templates HTML creados (4 por modelo) + template base                            | [ ]    |
| 12  | Todos los formularios protegidos con `{% csrf_token %}`                            | [ ]    |
| 13  | Flujo CRUD completo verificado para Dueños y Mascotas desde el navegador           | [ ]    |
| 14  | `.gitignore` con `.env`, `db.sqlite3`, `__pycache__/`, `venv/`                     | [ ]    |

---

> [!IMPORTANT]
> **Para la próxima clase:** Necesitarás este proyecto funcionando. En la Clase 11 extenderemos la aplicación con funcionalidades más avanzadas del CRUD.
