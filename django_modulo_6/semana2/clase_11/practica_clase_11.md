# Django — Módulo 6 · Clase 11

## Práctica: Personalizar el Admin del CV

---

> _"El panel que Django te da es funcional desde el primer momento. Esta práctica lo convierte en tuyo."_

---

## ¿Qué vas a hacer?

En las clases anteriores construiste el modelo del CV y lo protegiste con login. Hoy vas a:

1. Registrar todos los modelos del CV en el admin
2. Personalizar cómo se ven en el panel (columnas, filtros, buscador)
3. Cambiar el nombre del panel para que diga tu nombre
4. Agregar un usuario editor con permisos limitados
5. Proteger la vista de edición del CV con el permiso correcto

La práctica usa exactamente los modelos que construiste durante la semana. Donde dice `NombreDelModelo` o `nombre_app`, reemplazalo con los nombres de tu proyecto.

---

---

# Paso 1 — Verificar que las migraciones están al día

---

**¿Por qué primero esto?** Antes de registrar modelos en el admin, la base de datos tiene que estar actualizada. Si tienes modelos sin migrar, el panel puede fallar.

En la terminal, con el entorno virtual activo:

```bash
python manage.py showmigrations
```

Verás una lista. Las migraciones aplicadas tienen `[X]`. Las que faltan tienen `[ ]`.

Si hay alguna pendiente:

```bash
python manage.py makemigrations
python manage.py migrate
```

Cuando todo tiene `[X]`, puedes continuar.

---

---

# Paso 2 — Registrar los modelos básicos del CV

---

**¿Por qué hace falta?** Los modelos existen en la base de datos, pero el admin no los conoce hasta que los registrás explícitamente.

Abre el archivo `admin.py` de tu app del CV. Probablemente está casi vacío:

```python
# tu_app/admin.py  — estado actual (solo tiene esto)
from django.contrib import admin
```

Importá todos tus modelos y registralos:

```python
# tu_app/admin.py  — después del Paso 2

from django.contrib import admin
from .models import CV, Experiencia, Educacion, Habilidad
# ↑ reemplazá con los nombres reales de tus modelos

admin.site.register(CV)
admin.site.register(Experiencia)
admin.site.register(Educacion)
admin.site.register(Habilidad)
```

**¿Qué vas veamos ahora?**

Corre el servidor, andá a `http://127.0.0.1:8000/admin/` e ingresá como superusuario. Vas veamos una nueva sección con el nombre de tu app y dentro los modelos que registraste.

> 💡 Si la lista muestra «CV object (1)», «Experiencia object (1)»... significa que le falta el método `__str__` a tus modelos. En el siguiente paso lo resolvemos.

---

---

# Paso 3 — Agregar `__str__` a los modelos (si no lo tienen)

---

**¿Por qué?** Sin `__str__`, el admin muestra nombres genéricos imposibles de distinguir. Con él, muestra texto real.

Abre `models.py` y verifica que cada modelo tenga `__str__`. Si no lo tiene, agregalo:

```python
# tu_app/models.py — agregar __str__ a cada modelo

class CV(models.Model):
    nombre     = models.CharField(max_length=100)
    titulo     = models.CharField(max_length=200)
    # ... tus campos ...

    def __str__(self):
        return self.nombre   # ← devuelve el campo más descriptivo del modelo

class Experiencia(models.Model):
    empresa    = models.CharField(max_length=100)
    cargo      = models.CharField(max_length=100)
    desde      = models.DateField()
    hasta      = models.DateField(null=True, blank=True)
    # ... tus campos ...

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

class Educacion(models.Model):
    institucion = models.CharField(max_length=100)
    titulo      = models.CharField(max_length=100)
    # ... tus campos ...

    def __str__(self):
        return f"{self.titulo} — {self.institucion}"

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    nivel  = models.CharField(max_length=50)   # ej: 'Básico', 'Intermedio', 'Avanzado'
    # ... tus campos ...

    def __str__(self):
        return f"{self.nombre} ({self.nivel})"
```

> No necesitás migrar por agregar `__str__`. Ese método no crea columnas — solo define cómo se muestra el objeto.

---

---

# Paso 4 — Personalizar la vista de cada modelo con `ModelAdmin`

---

**¿Por qué?** El registro básico funciona, pero la lista tiene una sola columna. Con `ModelAdmin` agregás columnas, buscador y filtros en pocas líneas.

Reemplazá el contenido de `admin.py` con la versión personalizada:

```python
# tu_app/admin.py — versión con ModelAdmin

from django.contrib import admin
from .models import CV, Experiencia, Educacion, Habilidad

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display = ('nombre', 'titulo')
    # Campos donde busca el buscador
    search_fields = ('nombre', 'titulo')

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display  = ('empresa', 'cargo', 'desde', 'hasta')
    search_fields = ('empresa', 'cargo')
    # list_filter: panel de filtros a la derecha — ideal para fechas o campos con pocos valores
    list_filter   = ('desde',)
    ordering      = ('-desde',)
    # ordering con '-' delante → orden descendente (las más recientes primero)

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display  = ('institucion', 'titulo')
    search_fields = ('institucion', 'titulo')

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'nivel')
    search_fields = ('nombre',)
    list_filter   = ('nivel',)
    ordering      = ('nombre',)
```

**Guarda el archivo y recargá el admin.** La lista de cada modelo ahora muestra múltiples columnas y tiene buscador.

---

---

# Paso 5 — Ponerle tu nombre al panel

---

**¿Por qué?** El admin dice «Django administration» por defecto. Tres líneas lo personalizan.

Al **final** de `admin.py`, agrega:

```python
# tu_app/admin.py — agregar al final del archivo

admin.site.site_header = "Admin — Tu Nombre Aquí"
# ↑ el encabezado grande que aparece en todas las páginas del admin
# Ejemplo: "Admin — María García"

admin.site.site_title  = "Mi CV Admin"
# ↑ el título en la pestaña del navegador

admin.site.index_title = "Panel de Control del CV"
# ↑ el subtítulo en la página de inicio del admin
```

Recargá el admin. El encabezado ahora muestra tu nombre.

---

---

# Paso 6 — Crear un usuario editor con permisos limitados

---

**¿Por qué?** El superusuario tiene acceso total. Para dar acceso a un tercero (un mentor, un colaborador) es mejor crear un usuario específico con los permisos justos — sin poder borrar ni modificar usuarios.

**Desde el panel admin** (la forma visual):

1. Andá a `Admin → Autenticación → Usuarios → Agregar Usuario`
2. Completa el nombre de usuario y la contraseña
3. Guarda — te llevará a la página de detalles del usuario
4. Activa la casilla `Es staff` (sin esto, no puede entrar al admin)
5. Bajá a la sección **Permisos del usuario**
6. En el panel de la izquierda, busca los permisos de tu app y pasalos a la derecha:
   - `tu_app | cv | Can view cv`
   - `tu_app | experiencia | Can view experiencia`
   - `tu_app | educacion | Can view educacion`
   - `tu_app | habilidad | Can view habilidad`
7. Guarda

**Verificación:** Cerrá sesión con el superusuario y entra con el usuario editor. El panel mostrará solo los modelos con permiso `view` — sin botones de editar ni eliminar.

---

---

# Paso 7 — Crear un grupo para los editores

---

**¿Por qué grupos?** Si en el futuro le das acceso a más personas, no quieres repetir la asignación de permisos una por una. Un grupo centraliza los permisos.

**Desde el panel admin** (la forma visual):

1. Andá a `Admin → Autenticación → Grupos → Agregar Grupo`
2. Nombre del grupo: `Editores CV`
3. En el panel de permisos disponibles, busca y selecciona:
   - `tu_app | cv | Can change cv`
   - `tu_app | experiencia | Can add experiencia` + `Can change experiencia`
   - `tu_app | educacion | Can add educacion` + `Can change educacion`
   - `tu_app | habilidad | Can add habilidad` + `Can change habilidad`
4. Guarda el grupo

Ahora asignale el grupo al usuario editor:

1. Andá al usuario editor
2. En la sección `Grupos`, busca `Editores CV` y agregalo
3. Guarda

El usuario ahora hereda todos los permisos del grupo. Si el grupo cambia, el usuario lo refleja automáticamente.

---

---

# Paso 8 — Proteger la vista de edición con el permiso correcto

---

**¿Por qué?** En la clase 9 protegiste la vista del formulario con `@login_required`. Eso exige sesión, pero cualquier usuario logueado puede acceder. Ahora quieres que solo el superusuario (o quien tenga el permiso `change_cv`) pueda editar.

Abre `views.py` y reemplazá el decorador:

```python
# tu_app/views.py — antes (solo exige sesión)

from django.contrib.auth.decorators import login_required

@login_required
def editar_cv(request):
    ...
```

```python
# tu_app/views.py — después (exige sesión + permiso específico)

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('tu_app.change_cv', raise_exception=True)
# ↑ primero verifica sesión, después verifica el permiso
# raise_exception=True → si tiene sesión pero no permiso, muestra 403
# si fuera False → redirige al login (confuso para alguien que ya está logueado)
def editar_cv(request):
    ...
```

> ⚠️ El orden de los decoradores importa. En Python, los decoradores se aplican de abajo hacia arriba. `@login_required` al final significa que se verifica primero. `@permission_required` al final se verificaría primero — lo que causaría un error de permiso antes de saber si hay sesión activa.

**Verificación:**

- Entra como usuario editor (sin `change_cv`) → debe mostrar error 403
- Entra como superusuario → debe llegar al formulario

---

---

# Paso 9 — Crear la página de error 403

---

**¿Por qué?** Sin un template propio, Django muestra una página de error genérica en inglés. Con un template propio, el error se integra al diseño del proyecto.

Crea el archivo `templates/403.html`:

```html
<!-- templates/403.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1">403</h1>
  <h2>Acceso denegado</h2>
  <p class="lead">No tienes los permisos necesarios para ver esta página.</p>
  <a href="/" class="btn btn-primary">Volver al CV</a>
</div>

{% endblock %}
```

Verifica que el archivo `templates/403.html` esté en el directorio de templates que Django reconoce. Chequeá en `settings.py` que `DIRS` incluya la carpeta:

```python
# settings.py
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        # ↑ debe apuntar a la carpeta donde está el 403.html
        ...
    },
]
```

---

---

# Paso 10 — Prueba final del flujo completo

---

Realizá cada verificación antes de marcarla como completada:

**Con el superusuario:**

- [ ] Entrar al admin → ver todos los modelos del CV con las columnas configuradas
- [ ] La lista de Experiencia muestra empresa, cargo, fechas ordenadas por fecha descendente
- [ ] El encabezado del admin muestra tu nombre (no «Django administration»)
- [ ] Se puede crear, editar y eliminar en todos los modelos
- [ ] La vista `/editar-cv/` es accesible

**Con el usuario editor:**

- [ ] Puede entrar al admin
- [ ] Solo ve los modelos con permiso asignado
- [ ] No ve el botón «Eliminar» en los modelos donde no tiene `delete_`
- [ ] La vista `/editar-cv/` devuelve error 403
- [ ] La página del 403 tiene el diseño del proyecto (no la página genérica)

**Sin sesión:**

- [ ] Intentar entrar a `/editar-cv/` sin sesión redirige al login
- [ ] Después del login, el sistema lleva de vuelta a `/editar-cv/`

---

---

# Checklist de entrega

---

- [ ] `admin.py` tiene todos los modelos del CV registrados con `@admin.register`
- [ ] Cada `ModelAdmin` tiene `list_display`, `search_fields` y `ordering` configurados
- [ ] El encabezado del admin muestra el nombre del estudiante
- [ ] Existe un usuario editor (no superusuario) con permisos limitados
- [ ] Existe el grupo `Editores CV` con los permisos correctos
- [ ] El usuario editor pertenece al grupo `Editores CV`
- [ ] La vista de edición del CV usa `@permission_required` además de `@login_required`
- [ ] Existe el template `templates/403.html` con el diseño del proyecto
- [ ] Al entrar con el editor y visitar `/editar-cv/` → muestra 403
- [ ] Al entrar sin sesión y visitar `/editar-cv/` → redirige al login

---

---

# Puntos de extensión (opcionales)

---

Si terminaste antes de tiempo, prueba cualquiera de estas mejoras:

**Extensión A — Inline de Habilidades en el CV**

Si el modelo `Habilidad` tiene una ForeignKey al `CV`, puedes editar las habilidades directamente desde la página del CV:

```python
# tu_app/admin.py

class HabilidadInline(admin.TabularInline):
    model   = Habilidad
    extra   = 1   # cuántos formularios vacíos mostrar

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'titulo')
    inlines      = [HabilidadInline]
    # ↑ las habilidades aparecen en la página de edición del CV
```

**Extensión B — Registrar el usuario con admin personalizado**

```python
# tu_app/admin.py

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class MiUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'is_staff', 'is_active')
    list_filter   = ('is_staff', 'is_active')

admin.site.unregister(User)          # desregistrar el default
admin.site.register(User, MiUserAdmin)  # registrar el personalizado
```

**Extensión C — Señal que registra cuándo se edita el CV**

Crea el archivo `tu_app/signals.py`:

```python
# tu_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CV

@receiver(post_save, sender=CV)
def al_guardar_cv(sender, instance, created, **kwargs):
    if created:
        print(f"CV creado: {instance.nombre}")
    else:
        print(f"CV actualizado: {instance.nombre}")
```

Y en `tu_app/apps.py`, activar las señales:

```python
# tu_app/apps.py

from django.apps import AppConfig

class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tu_app'

    def ready(self):
        import tu_app.signals
```

Al guardar el CV desde el admin, la terminal mostrará el mensaje.

---

## Preguntas para pensar después de terminar

- Si mañana le das acceso a un nuevo colaborador, ¿qué pasos harías para que tenga los mismos permisos que el editor? ¿Cuánto tiempo te tomaría con grupos vs. sin grupos?
- ¿Qué diferencia hay entre que la vista devuelva un 403 y que simplemente no muestre el formulario?
- Si alguien tiene `view_cv` pero no `change_cv`, ¿puede editar el CV desde el admin? ¿Y desde la vista pública?
- ¿En qué situación usarías un `TabularInline` en lugar de un `StackedInline` y vice versa?

---
