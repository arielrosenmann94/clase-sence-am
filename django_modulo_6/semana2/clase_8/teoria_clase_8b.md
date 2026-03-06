# 🔐 Django — Módulo 6 · Clase 8B

## Seguridad web: lo que nadie enseña hasta que te hackean

---

> _"Escribir código que funciona es una habilidad. Escribir código que funciona y que nadie puede romper es otra — y empieza por saber qué haría alguien si quisiera romperlo."_

---

## Por qué importa esto ahora

Hoy construyeron formularios. Un formulario es la primera forma en que usuarios externos pueden enviar datos a la aplicación. Eso es exactamente lo que busca un atacante: un lugar donde meter datos que la aplicación no espera.

No se necesita ser experto en seguridad. Se necesita conocer los errores más comunes — porque la mayoría de las brechas no vienen de ataques sofisticados. Vienen de errores predecibles que alguien cometió sin saberlo.

**OWASP** (Open Web Application Security Project) es una fundación sin fines de lucro que estudia miles de aplicaciones reales y publica cada pocos años los 10 problemas de seguridad más frecuentes. Esta es la lista **2025**.

---

---

# OWASP Top 10 — 2025

---

## A01 — Broken Access Control (Control de acceso roto)

### El problema

El usuario puede hacer cosas que no debería poder hacer.

### El escenario concreto

Imaginen que construyeron un CV con un panel de edición en `/cv/editar/`. Para protegerlo, pusieron un botón "Editar" que solo aparece si el usuario está logueado. Pero la URL `/cv/editar/` no verifica si el usuario tiene permiso — solo el botón está oculto.

Cualquier persona que conozca la URL puede acceder directamente desde el navegador, sin tocar el botón.

**El error**: proteger la _vista_ en el HTML pero no proteger la _vista_ en Python.

### Otro ejemplo habitual

Una tienda online guarda el precio en un campo oculto del formulario:

```html
<input type="hidden" name="precio" value="500" />
```

Un usuario inspecciona el HTML, cambia el valor a `1`, envía el formulario. Si la vista confía en ese dato, cobra $1 por un producto de $500.

### En Django

```python
# MAL: solo oculta el botón en el template
# BIEN: verificar en la vista
from django.contrib.auth.decorators import login_required

@login_required
def editar_cv(request):
    ...
```

> **Regla**: todo lo que no debería verse o hacerse tiene que estar protegido en el servidor, no solo en el template.

---

## A02 — Security Misconfiguration (Configuración incorrecta)

### El problema

El software es seguro en teoría pero está mal configurado en la práctica.

### El escenario concreto

Un developer termina su app Django y la sube al servidor de producción. No cambia nada de la configuración de desarrollo. El resultado:

- `DEBUG = True` → Cualquier error muestra el código fuente completo, las variables del servidor, las rutas de archivos y las configuraciones. Un atacante que provoca un error intencional recibe un mapa detallado de la aplicación.
- `SECRET_KEY = 'mi-clave-secreta-123'` en el código que se sube a GitHub → Los tokens de sesión son predecibles.
- El panel de administración sigue en `/admin/` sin cambios → Es la primera URL que cualquier script automático prueba.

### Qué se ve cuando DEBUG está activo

Cuando ocurre un error con `DEBUG = True`, Django muestra una página con el traceback completo. En desarrollo es útil. En producción, le dice al atacante exactamente qué línea de código falló, qué variables existen y qué estructura tiene el proyecto.

### En Django

```python
# settings.py en producción SIEMPRE:
DEBUG = False
ALLOWED_HOSTS = ['midominio.com']
SECRET_KEY = os.environ.get('SECRET_KEY')   # nunca hardcodeada
```

Django tiene un comando que detecta problemas comunes antes de publicar:

```
python manage.py check --deploy
```

---

## A03 — Software Supply Chain Failures (Fallas en la cadena de suministro)

### El problema

El código que se instala desde internet (librerías, paquetes, dependencias) puede contener código malicioso sin que nadie lo note.

### El escenario concreto

Un developer instala una librería de Python llamada `django-utils-plus` con `pip install`. La librería existe, tiene documentación, tiene 5000 descargas. Pero alguien publicó esa librería con un nombre parecido al de una librería legítima (`django-utils`), y dentro del código de instalación hay un script que copia las variables de entorno del servidor y las envía a un servidor externo.

Esto se llama **typosquatting** — nombres de paquetes deliberadamente parecidos a los reales para engañar a quien escribe mal.

### El caso famoso

En 2021, un investigador publicó miles de paquetes falsos en PyPI (el repositorio de Python) con nombres que imitaban librerías internas de empresas como Apple, Microsoft y Tesla. Muchos servidores los instalaron automáticamente.

### Qué hacer

- Verificar que la librería que se instala es la correcta antes de instalar
- No copiar comandos `pip install` de foros sin verificar el nombre exacto
- En proyectos importantes: usar `pip-audit` para detectar vulnerabilidades conocidas en las dependencias instaladas

### Django lo cubre con

Django en si mismo no puede controlar qué librerías adicionales instala el developer. Pero hay mecanismos en el ecosistema:

```bash
# Fijar versiones exactas en requirements.txt
Django==5.0.3
Pillow==10.2.0
# Si alguien instala una versión diferente, el proyecto lo rechaza

# Auditar vulnerabilidades conocidas en las dependencias instaladas
pip install pip-audit
pip-audit
# Muestra si alguna librería tiene CVEs (vulnerabilidades publicadas) conocidos
```

La práctica de tener un `requirements.txt` con versiones fijas no es solo para reproducibilidad — también es una defensa: asegura que todos corren exactamente las mismas versiones auditadas.

---

## A04 — Cryptographic Failures (Fallas criptográficas)

### El problema

Datos sensibles viajan o se guardan sin protección adecuada.

### El escenario concreto — contraseñas

Una app guarda las contraseñas de los usuarios directamente en la base de datos como texto:

```
| usuario | contraseña        |
|---------|-------------------|
| juan    | contraseña123     |
| maria   | miperro2024       |
```

Si alguien accede a la base de datos (por una brecha, por un backup mal protegido, por un desarrollador deshonesto), tiene acceso inmediato a la contraseña de cada usuario — y como el 60% de las personas reusan contraseñas, también tiene acceso a sus emails y redes sociales.

### El escenario concreto — tráfico

Una app que funciona por HTTP sin HTTPS envía los formularios de login en texto plano. Cualquier persona en la misma red WiFi puede ver el usuario y la contraseña que viajan en el request.

### En Django

Django hashea las contraseñas automáticamente con PBKDF2 + salt. Lo que se guarda en la base de datos se ve así:

```
pbkdf2_sha256$600000$randomsalt$HashedPassword==
```

No se puede revertir al texto original. Si alguien roba la base de datos, no obtiene las contraseñas reales.

> **Regla**: nunca guardar contraseñas como texto. Siempre usar HTTPS en producción. Nunca poner el `SECRET_KEY` en el código que se sube a repositorios.

---

## A05 — Injection (Inyección)

### El problema

El atacante manda datos que la aplicación ejecuta como si fueran instrucciones propias.

### El escenario concreto — SQL Injection

Un formulario de login tiene dos campos: usuario y contraseña. La aplicación construye el query así:

```python
# CÓDIGO PELIGROSO — nunca hacer esto
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

El atacante escribe como nombre de usuario:

```
admin' --
```

El query resultante es:

```sql
SELECT * FROM users WHERE username='admin' --' AND password='cualquiercosa'
```

El `--` es un comentario en SQL. Todo lo que viene después se ignora. La consulta devuelve el usuario `admin` sin verificar la contraseña. El atacante entró.

### En Django

El ORM de Django **nunca construye SQL con strings del usuario**. Usa queries parametrizadas automáticamente:

```python
# Esto es lo que hace Django internamente — el valor se pasa separado del query
User.objects.filter(username=username, password=password)
```

El motor de la base de datos recibe la estructura del query y el valor por separado. El valor nunca puede modificar la estructura.

> **Regla**: nunca usar `cursor.execute()` con strings del usuario concatenados. Siempre usar el ORM o queries parametrizadas.

---

## A06 — Insecure Design (Diseño inseguro)

### El problema

La vulnerabilidad está en la idea, no en el código. Aunque el código esté perfecto, el diseño hace imposible ser seguro.

### El escenario concreto

Una app de recuperación de contraseña funciona así:

1. El usuario escribe su email
2. La app envía un link para resetear la contraseña
3. El link nunca expira

Un atacante que accede al email de alguien en ese momento (una computadora desbloqueada, un backup de email) puede usar ese link semanas después.

Otro ejemplo: un sistema que requiere que la contraseña esté guardada como texto plano porque otra parte del sistema "necesita leerla". El diseño hace imposible una protección básica.

**La lección**: la seguridad tiene que pensarse desde el diseño, no agregarse al final. ¿El link de reset debería tener expiración? ¿Sí — cuánto tiempo? ¿Podría usarse más de una vez? Esas preguntas se responden en el papel, antes de escribir código.

### Django lo cubre con

Django incluye un sistema de reset de contraseña listo para usar que ya implementa las decisiones de diseño correctas:

- El link expira despues de un tiempo configurable (`PASSWORD_RESET_TIMEOUT`, por defecto 3 dias)
- El link es de un solo uso — si ya se usó, no puede usarse de nuevo
- El token incluye un hash del hash de la contraseña actual, asi que si la contraseña ya fue cambiada, el link viejo queda inválido automáticamente

```python
# En urls.py — Django provee estas vistas sin necesidad de código propio
from django.contrib.auth import urls as auth_urls

urlpatterns = [
    path('accounts/', include(auth_urls)),
    # incluye: login, logout, password_change, password_reset
]
```

> Usar el sistema de autenticación de Django en lugar de construir uno propio es, en si mismo, una decisión de diseño seguro.

---

## A07 — Authentication Failures (Fallas de autenticación)

### El problema

El sistema permite que alguien acceda como otra persona.

### Los escenarios concretos

**Fuerza bruta sin límite**: un formulario de login que no tiene límite de intentos. Un script puede probar millones de combinaciones de contraseñas hasta encontrar la correcta. Esto se llama ataque de fuerza bruta.

**Sesiones que no expiran**: el usuario cierra la pestaña pero la sesión sigue activa indefinidamente. Alguien que accede a esa computadora horas después sigue logueado.

**"Recordarme" predecible**: un token de "recordarme" que es simplemente el ID del usuario codificado en base64. Cualquiera puede calcular el token de otro usuario.

**No invalidar sesión al cerrar sesión**: la app borra la cookie del browser pero no invalida la sesión en el servidor. El token sigue funcionando si alguien lo tiene guardado.

### En Django

El sistema de autenticación de Django maneja correctamente la mayoría de estos casos: sesiones firmadas, logout que invalida la sesión en el servidor, protección contra fijación de sesión.

El error más común de los desarrolladores junior es **construir autenticación propia** en lugar de extender la de Django, introduciendo todos estos problemas que Django ya resuelve.

### Django lo cubre con

| Problema                       | Solución de Django                                                                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fuerza bruta sin limite        | Django no incluye limitador por defecto, pero `django-axes` o `django-ratelimit` se integran en minutos                                           |
| Sesiones que no expiran        | `SESSION_COOKIE_AGE` configura la duración. Por defecto, 2 semanas. `SESSION_EXPIRE_AT_BROWSER_CLOSE = True` expira al cerrar el browser          |
| Token "recordarme" predecible  | Las cookies de sesión de Django están firmadas con HMAC usando `SECRET_KEY` — no se pueden falsificar sin conocer la clave                        |
| Sesión no invalidada al cerrar | `logout(request)` de Django elimina la sesión del servidor, no solo la cookie del browser                                                         |
| Contraseñas débiles            | `AUTH_PASSWORD_VALIDATORS` en `settings.py` — Django trae validadores para largo mínimo, similitud con el nombre de usuario y contraseñas comunes |

```python
# settings.py — validadores de contraseña activos por defecto
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## A08 — Software or Data Integrity Failures (Fallas de integridad)

### El problema

La aplicación no verifica que los datos o el código que recibe sean legítimos.

### El escenario concreto

Un e-commerce procesa pagos. Los datos del pago llegan en un objeto serializado (un formato que convierte objetos Python a texto y viceversa). La aplicación deserializa el objeto sin verificarlo.

Un atacante modifica el objeto serializado durante el proceso de pago. En lugar de pagar $500, el objeto dice $1. La aplicación lo procesa sin preguntar.

### El caso con datos de formularios

Imaginen un formulario donde uno de los campos es `rol_usuario` y los valores posibles son `cliente` o `admin`. Si ese campo viene del formulario (del lado del cliente) y la aplicación lo acepta sin verificar, cualquier usuario puede enviarse el rol `admin`.

> **Regla**: los datos que determinan permisos o precios nunca deben venir de formularios del cliente. Se calculan o se leen desde la base de datos en el servidor.

### Django lo cubre con

Django ofrece tres niveles de validación de integridad de datos:

**1. Validación de tipo en el modelo** — si el campo es `DecimalField`, Django rechaza cualquier valor que no sea un número válido antes de guardarlo.

**2. Validadores en el modelo** — se pueden definir reglas que se ejecutan antes de cualquier `save()`:

```python
from django.core.exceptions import ValidationError

def precio_positivo(valor):
    if valor <= 0:
        raise ValidationError('El precio debe ser mayor a cero.')

class Producto(models.Model):
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[precio_positivo]
    )
```

**3. `clean()` en el modelo** — para reglas que involucran varios campos:

```python
class Reserva(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField()

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser anterior al inicio.')
```

Estas validaciones corren antes de `save()` — incluso si alguien inserta datos directamente sin pasar por el formulario.

---

## A09 — Security Logging and Alerting Failures (Fallas de registro y alertas)

### El problema

Nadie sabe que algo malo ocurrió — o se enteran semanas después.

### El escenario concreto

Un atacante intenta 50.000 combinaciones de contraseñas en el formulario de login de la app. Sin logs, nadie lo sabe. El atacante eventualmente encuentra una que funciona y tiene acceso.

Sin alertas, esa cuenta comprometida puede estar siendo usada durante semanas mientras el developer no tiene idea de que algo pasó.

### La estadística

El tiempo promedio entre que ocurre una brecha y que se detecta es **197 días** (IBM, 2024). En ese tiempo, el atacante tiene acceso.

### Qué debería registrarse como mínimo

- Intentos de login fallidos (especialmente muchos consecutivos desde la misma IP)
- Cambios en datos sensibles (contraseñas, emails, roles)
- Errores 403 y 404 repetidos (pueden indicar alguien escaneando URLs)
- Accesos desde IPs desconocidas a áreas sensibles

### En Django

```python
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            logger.warning(
                f"Intento de login fallido para: {request.POST.get('username')} "
                f"desde IP: {request.META.get('REMOTE_ADDR')}"
            )
```

---

## A10 — Mishandling of Exceptional Conditions (Manejo incorrecto de errores)

### El problema

La aplicación no sabe qué hacer cuando algo sale mal y expone información o entra en un estado inseguro.

### El escenario concreto

Un formulario recibe un archivo. La aplicación intenta abrirlo y procesarlo. Si el archivo está corrupto, Python lanza una excepción. Si nadie captura esa excepción, Django (en producción, con DEBUG = False) devuelve un error 500 genérico — pero en desarrollo, con DEBUG = True, devuelve toda la información del servidor.

Otro caso: un endpoint que recibe un ID de usuario como número entero. El atacante manda el texto `"abc"` en lugar de un número. Si la vista no maneja ese error, la aplicación crashea y puede revelar información de la infraestructura.

### Por qué importa

Los atacantes exploran cómo responde una aplicación ante inputs inesperados. Un error 500 puede ser el primer indicio de que algo es explotable. Una app que maneja sus errores con gracia no entrega esa información.

### En Django

```python
def detalle_producto(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
    except Producto.DoesNotExist:
        # Respuesta controlada — no expone qué ocurrió internamente
        return render(request, '404.html', status=404)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return render(request, '500.html', status=500)
```

> **Regla**: anticipar qué puede salir mal y decidir explícitamente qué mostrar cuando ocurre. Los errores no controlados son regalos para quien explora la aplicación.

---

---

# Lo que Django protege automáticamente

---

Django fue diseñado con seguridad como principio. Estas protecciones están activas desde el primer `django-admin startproject`:

| Vulnerabilidad             | Cómo Django la protege                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| SQL Injection              | El ORM usa queries parametrizadas — nunca concatena strings del usuario en SQL                           |
| CSRF                       | El `{% csrf_token %}` genera un token único por sesión que verifica cada POST                            |
| XSS                        | El motor de templates escapa automáticamente `{{ variable }}` — convierte `<script>` en texto inofensivo |
| Contraseñas en texto plano | Hashea con PBKDF2 + salt automáticamente al usar `set_password()`                                        |
| Sesiones predecibles       | Las cookies de sesión están firmadas con `SECRET_KEY`                                                    |
| Clickjacking               | El header `X-Frame-Options` impide que el sitio sea embebido en iframes de otros dominios                |

**El mensaje importante**: Django no puede proteger contra todo. Pero las vulnerabilidades más básicas — las que aparecen en el OWASP Top 10 — ya tienen solución integrada. El error más común es desactivarlas por accidente o construir alternativas propias peores.

---

# Cierre

---

Los formularios que construyeron hoy son la interfaz entre su aplicación y el mundo exterior. Cada campo de texto es una posible entrada de datos inesperados. Cada URL es una puerta que alguien podría intentar abrir sin invitación.

El OWASP Top 10 no es una lista de ataques exóticos de películas. Es la lista de los errores que cometen constantemente developers que no conocían el problema. Ahora lo conocen.

La seguridad empieza por una pregunta simple en cada decisión de diseño: **¿qué pasaría si alguien mandara aquí algo que yo no esperaba?**

> _"Un sistema seguro no es aquel al que nadie puede entrar. Es aquel donde, si alguien entra, no puede hacer daño — y alguien se da cuenta enseguida."_

---
