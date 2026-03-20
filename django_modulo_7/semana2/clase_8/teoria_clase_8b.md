# 🚀 Módulo 7 — Clase 8b

## Guía Completa Pre-Deploy: Todo lo que Hay que Verificar Antes de Poner Django en Producción

> **Transversal** — Esta guía aplica a cualquier proyecto Django que vayan a publicar. No importa si es un CV, una tienda, o una API — estos pasos son los mismos.
>
> ⚠️ Esta clase es 100% teórica y conversacional. Es la guía que van a consultar **cada vez** que tengan que hacer deploy de un proyecto real.

---

## 🗺️ Índice

| #      | Tema                                                              |
| ------ | ----------------------------------------------------------------- |
| **1**  | ¿Qué es un Deploy? (Y Por Qué da Miedo)                         |
| **2**  | La Analogía: Mudarse de Casa                                     |
| **3**  | Fase 1 — Código Limpio y Funcional                               |
| **4**  | Fase 2 — Configuración de Producción (`settings.py`)             |
| **5**  | Fase 3 — Variables de Entorno y Secretos                         |
| **6**  | Fase 4 — Base de Datos                                           |
| **7**  | Fase 5 — Archivos Estáticos y Media                              |
| **8**  | Fase 6 — Seguridad (OWASP y Django)                              |
| **9**  | Fase 7 — Dependencias y `requirements.txt`                       |
| **10** | Fase 8 — Git, `.gitignore` y Control de Versiones                |
| **11** | Fase 9 — Testing: ¿Funciona Todo?                                |
| **12** | Fase 10 — El Servidor: ¿Dónde Vive tu App?                      |
| **13** | Fase 11 — DNS y Dominio                                          |
| **14** | Fase 12 — HTTPS y Certificados SSL                               |
| **15** | Fase 13 — Monitoreo y Logs Post-Deploy                           |
| **16** | El Mega-Checklist: Todo en Una Página                             |
| **17** | Los 10 Errores de Deploy Más Comunes (y Cómo Evitarlos)          |
| **18** | Diagrama: El Flujo Completo de Deploy                             |

---

---

> _"Todos tienen un plan hasta que hacen deploy por primera vez a producción."_
>
> — Adaptación libre de Mike Tyson, aplicada a software

---

---

# 😰 1. ¿Qué es un Deploy? (Y Por Qué da Miedo)

---

**Deploy** = poner tu aplicación en un servidor accesible desde internet para que cualquier persona pueda usarla.

Mientras desarrollas, tu app vive en `localhost:8000`. Solo tú la ves. Cuando haces deploy, tu app vive en `www.miapp.com`. **Todo el mundo** la ve.

### ¿Por qué da miedo?

Porque en desarrollo puedes romper todo y nadie se entera. En producción, si algo falla:

| En desarrollo                      | En producción                                      |
| :--------------------------------- | :------------------------------------------------- |
| Solo tú ves los errores            | Tus usuarios ven los errores                       |
| `DEBUG = True` te ayuda            | `DEBUG = True` expone tu código al mundo            |
| La base de datos tiene datos falsos | La base de datos tiene datos **reales** de personas |
| Si se cae, refrescas y listo       | Si se cae, pierdes usuarios y dinero               |
| Sin tráfico                        | Potencialmente miles de requests por minuto         |

> 💡 **La buena noticia:** el deploy no es magia negra. Es un proceso con pasos. Si los sigues en orden, funciona. Esta guía es esa receta.

---

---

# 🏠 2. La Analogía: Mudarse de Casa

---

Hacer deploy es como **mudarse de departamento**. Desarrollar es vivir en tu depto actual (cómodo, desordenado, nadie te ve). Deploy es mudarte a un departamento nuevo donde van a venir visitas.

```
DESARROLLO (tu depto actual)              PRODUCCIÓN (depto nuevo, con visitas)
─────────────────────────                  ─────────────────────────────────────
✅ Puedes dejar ropa en el sillón          ❌ Tiene que estar ordenado
✅ La puerta puede estar sin llave         ❌ Necesitas cerraduras (seguridad)
✅ Si se corta la luz, prendes una vela    ❌ Necesitas generador (uptime)
✅ Solo tú sabes dónde está todo           ❌ Otros tienen que entender la estructura
✅ Si se rompe algo, lo arreglas mañana    ❌ Si se rompe algo, es AHORA
```

### Las fases de la mudanza

```
📦 Fase 1: Empacar bien         →  Código limpio, sin prints de debug
🔑 Fase 2: Cambiar cerraduras   →  Configuración de seguridad
📋 Fase 3: Hacer inventario     →  requirements.txt, dependencias
🚚 Fase 4: Contratar la mudanza →  Elegir servidor (hosting)
🏗️ Fase 5: Instalar servicios   →  Base de datos, archivos estáticos
🔐 Fase 6: Sistema de alarma    →  HTTPS, headers de seguridad
📬 Fase 7: Cambiar dirección    →  DNS, dominio
✅ Fase 8: Verificar que todo llegó → Testing en producción
```

> Vamos a recorrer **cada fase** con todo lo que hay que verificar.

---

---

# 🧹 3. Fase 1 — Código Limpio y Funcional

---

Antes de siquiera pensar en servidores, tu código tiene que estar **limpio**. No perfecto — limpio.

## Checklist de código

```
[ ] No hay prints de debugging en el código
    → Buscar: grep -rn "print(" en todo el proyecto
    → Los print() en producción pueden imprimir datos sensibles en los logs

[ ] No hay código comentado "por si acaso"
    → Si está comentado, bórralo. Git lo recuerda por ti.

[ ] No hay import de módulos que no se usan
    → Cada import innecesario es peso muerto

[ ] No hay contraseñas hardcodeadas en el código
    → Buscar: grep -rn "password" y grep -rn "SECRET"
    → TODO dato sensible va en variables de entorno

[ ] Las vistas que requieren login tienen @login_required o LoginRequiredMixin
    → Una vista sin protección es una puerta abierta

[ ] Los formularios validan los datos en el servidor (no solo en JS)
    → La validación de JavaScript se puede saltar con DevTools

[ ] No hay TODO o FIXME críticos sin resolver
    → grep -rn "TODO\|FIXME" para encontrarlos todos
```

### La analogía

> 🏠 **Mudanza:** No te llevas la basura a la casa nueva. Antes de empacar, tiras lo que no necesitas.

### Herramienta útil: `python manage.py check`

```bash
$ python manage.py check --deploy
System check identified some issues:

WARNINGS:
? (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting.
? (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True.
? (security.W012) SESSION_COOKIE_SECURE is not set to True.
...
```

> Este comando es tu **mejor amigo** antes de deploy. Revísalo, entiéndelo, arregla cada warning.

---

---

# ⚙️ 4. Fase 2 — Configuración de Producción (`settings.py`)

---

El `settings.py` de desarrollo y el de producción son **mundos diferentes**. Lo que te ayuda en desarrollo, te destruye en producción.

## Las 7 configuraciones críticas

### 1. `DEBUG = False` → **OBLIGATORIO**

```python
# ❌ EN PRODUCCIÓN ESTO ES UNA CATÁSTROFE:
DEBUG = True
# Cualquier error muestra: código fuente, variables, rutas, configuraciones

# ✅ EN PRODUCCIÓN SIEMPRE:
DEBUG = False
```

| `DEBUG = True`                                    | `DEBUG = False`                            |
| :------------------------------------------------ | :----------------------------------------- |
| Muestra traceback completo al usuario             | Muestra página de error genérica           |
| Expone variables de entorno en la página de error | No expone nada                             |
| Guarda TODAS las queries SQL en memoria           | No acumula queries → menos uso de RAM      |
| Sirve archivos estáticos automáticamente          | NO sirve estáticos → necesitas Nginx/CDN   |

> ⚠️ **Dato real:** En 2024, un investigador encontró **más de 2.000 sitios Django** con `DEBUG = True` en producción usando una simple búsqueda. Todos exponían su código fuente. _(Shodan.io, 2024)_

---

### 2. `SECRET_KEY` → Fuera del código

```python
# ❌ NUNCA:
SECRET_KEY = 'django-insecure-abc123-esta-clave-es-visible-en-github'

# ✅ SIEMPRE:
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
# o con django-environ:
SECRET_KEY = env('SECRET_KEY')
```

**¿Qué pasa si alguien obtiene tu `SECRET_KEY`?**

| Consecuencia                                   | Gravedad |
| :--------------------------------------------- | :------- |
| Puede falsificar cookies de sesión             | 🔴 Alta  |
| Puede hacerse pasar por cualquier usuario      | 🔴 Alta  |
| Puede firmar tokens de reset de contraseña     | 🔴 Alta  |
| Puede generar tokens CSRF válidos              | 🔴 Alta  |
| Tiene que regenerarse y TODOS los usuarios pierden su sesión | 🟡 Media |

---

### 3. `ALLOWED_HOSTS` → Solo tu dominio

```python
# ❌ EN PRODUCCIÓN NUNCA:
ALLOWED_HOSTS = ['*']  # acepta requests de CUALQUIER dominio

# ✅ EN PRODUCCIÓN:
ALLOWED_HOSTS = ['miapp.com', 'www.miapp.com']
```

---

### 4. `DATABASES` → Base de datos de producción

```python
# ❌ SQLite en producción (no está diseñado para concurrencia):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ PostgreSQL en producción:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

| SQLite                              | PostgreSQL                                 |
| :---------------------------------- | :----------------------------------------- |
| Un solo archivo                     | Servidor dedicado                          |
| No maneja bien múltiples usuarios   | Diseñado para concurrencia                 |
| Perfecto para desarrollo            | Estándar de la industria en producción     |
| No necesita instalación             | Necesita instalación y configuración       |

---

### 5. Cookies seguras

```python
# En producción con HTTPS:
SESSION_COOKIE_SECURE = True      # Cookie de sesión solo viaja por HTTPS
CSRF_COOKIE_SECURE = True         # Cookie CSRF solo viaja por HTTPS
SESSION_COOKIE_HTTPONLY = True     # JavaScript no puede leer la cookie de sesión
CSRF_COOKIE_HTTPONLY = True        # JavaScript no puede leer la cookie CSRF
```

---

### 6. Headers de seguridad

```python
SECURE_BROWSER_XSS_FILTER = True            # Activa filtro XSS del navegador
SECURE_CONTENT_TYPE_NOSNIFF = True           # Evita que el navegador adivine el tipo MIME
X_FRAME_OPTIONS = 'DENY'                    # Impide que tu sitio se meta en un iframe
SECURE_HSTS_SECONDS = 31536000              # Fuerza HTTPS por 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True       # Incluye subdominios en HSTS
SECURE_HSTS_PRELOAD = True                  # Permite entrar en la lista de HSTS preload
SECURE_SSL_REDIRECT = True                  # Redirige HTTP → HTTPS automáticamente
```

---

### 7. Logging en producción

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

> 💡 **Sin logs, no sabes qué pasa en producción.** Es como manejar de noche sin luces.

---

### Patrón recomendado: separar settings

```
config/
├── settings/
│   ├── __init__.py      # importa el settings correcto
│   ├── base.py          # todo lo común (INSTALLED_APPS, etc.)
│   ├── development.py   # DEBUG=True, SQLite, sin HTTPS
│   └── production.py    # DEBUG=False, PostgreSQL, seguridad
```

```python
# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.environ.get('DOMAIN')]
# ... todas las configs de seguridad
```

---

---

# 🔐 5. Fase 3 — Variables de Entorno y Secretos

---

> Esta fase conecta directamente con lo que vimos en la **clase 6b** sobre `.env` files.

## ¿Qué NUNCA debe estar en el código?

```
❌ SECRET_KEY
❌ Contraseñas de base de datos
❌ API keys de terceros (Stripe, AWS, SendGrid...)
❌ Tokens de acceso
❌ Credenciales de email
❌ Cualquier dato que, si alguien lo ve, pueda causar daño
```

## ¿Dónde van?

```
✅ En un archivo .env (NUNCA en git)
✅ En variables de entorno del servidor
✅ En un servicio de secretos (AWS Secrets Manager, Vault)
```

## El patrón `.env` + `.env.example`

```bash
# .env (NUNCA SE SUBE A GIT — está en .gitignore)
SECRET_KEY=una-clave-ultra-secreta-generada-aleatoriamente
DB_NAME=mi_base_datos
DB_USER=mi_usuario
DB_PASSWORD=contraseña-super-segura
DEBUG=False
ALLOWED_HOSTS=miapp.com,www.miapp.com
```

```bash
# .env.example (SÍ SE SUBE A GIT — es la plantilla)
SECRET_KEY=cambiar-esta-clave
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Checklist de secretos

```
[ ] El archivo .env existe y tiene todos los valores reales
[ ] El archivo .env está en .gitignore
[ ] El archivo .env.example existe con valores de ejemplo
[ ] SECRET_KEY es única y fue generada aleatoriamente
[ ] Las credenciales de la base de datos están en .env
[ ] Ningún secreto aparece en el código fuente
[ ] Verificar con: grep -rn "SECRET_KEY\|PASSWORD\|API_KEY" (excluyendo .env)
```

> ⚠️ **El caso real:** En 2023, un developer subió sus credenciales de AWS a GitHub. Bots automáticos las detectaron en **menos de 5 minutos** y generaron más de **$50,000 USD** en cargos de minería de criptomonedas antes de que el developer se diera cuenta. _(Fuente: TheRegister, 2023)_

---

---

# 🗄️ 6. Fase 4 — Base de Datos

---

## Checklist de base de datos

```
[ ] Las migraciones están al día
    → python manage.py makemigrations --check
    → Si dice "No changes detected" → OK
    → Si crea migraciones nuevas → hay cambios sin migrar

[ ] Todas las migraciones se aplicaron
    → python manage.py showmigrations
    → Todas deben tener [X], ninguna sin aplicar [ ]

[ ] La base de datos de producción es PostgreSQL (no SQLite)
    → SQLite no soporta escrituras concurrentes

[ ] Hay un plan de backups
    → ¿Cada cuánto se hace backup? ¿Dónde se guardan?
    → Sin backup, un error puede borrar AÑOS de datos

[ ] Los datos sensibles están cifrados o hasheados
    → Contraseñas: Django las hashea automáticamente ✅
    → Datos personales: considerar cifrado adicional

[ ] No hay datos de prueba en la base de producción
    → Usuarios "test@test.com", productos "asdf", etc.
```

### El comando más importante antes de deploy

```bash
# Verifica que no hay migraciones pendientes
python manage.py migrate --check
# Si dice "Unapplied migration(s)" → hay que migrar primero
```

### La analogía

> 🏠 **Mudanza:** La base de datos es tu mueblería. No te llevas los muebles rotos a la casa nueva. Y pones seguro en el bodegaje.

---

---

# 📁 7. Fase 5 — Archivos Estáticos y Media

---

En desarrollo, Django sirve los archivos estáticos automáticamente (CSS, JS, imágenes). **En producción, Django NO los sirve.** Necesitas que otro servicio lo haga (Nginx, WhiteNoise, CDN).

## ¿Qué son los archivos estáticos?

```
ESTÁTICOS (static/)                     MEDIA (media/)
─────────────────                       ──────────────
CSS, JavaScript, imágenes del diseño    Archivos que suben los usuarios
NO cambian con el uso                   Cambian constantemente
Se recopilan con collectstatic          Se guardan donde configures
Ejemplo: logo.png, styles.css          Ejemplo: foto_perfil.jpg, cv.pdf
```

## Configuración para producción

```python
# settings/production.py

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # aquí collectstatic los recopila

# Archivos media (subidos por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## El comando `collectstatic`

```bash
# Recopila TODOS los archivos estáticos de todas las apps
# en una sola carpeta (STATIC_ROOT) para que Nginx los sirva
python manage.py collectstatic

# Te va a pedir confirmación:
# "This will overwrite existing files! Are you sure? (yes/no)"
# → yes
```

## Opción simple: WhiteNoise

Si no quieres configurar Nginx solo para estáticos, **WhiteNoise** permite que Django los sirva eficientemente:

```bash
pip install whitenoise
```

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← justo después de SecurityMiddleware
    # ... resto de middlewares
]

# Compresión y cache automáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Checklist de archivos

```
[ ] STATIC_ROOT está configurado
[ ] python manage.py collectstatic funciona sin errores
[ ] Los archivos estáticos se sirven correctamente en producción
[ ] MEDIA_ROOT está configurado si hay uploads de usuarios
[ ] Los archivos media tienen permisos de escritura en el servidor
[ ] Las imágenes de usuarios no se sirven desde una ruta ejecutable
```

---

---

# 🛡️ 8. Fase 6 — Seguridad (OWASP y Django)

---

> Esta fase conecta directamente con la **clase 8b del módulo 6** sobre OWASP Top 10.

## Checklist rápido de seguridad

```
[ ] DEBUG = False
[ ] SECRET_KEY única y en variable de entorno
[ ] ALLOWED_HOSTS especifica solo tu dominio
[ ] CSRF protección activa ({% csrf_token %} en todos los forms POST)
[ ] SESSION_COOKIE_SECURE = True
[ ] CSRF_COOKIE_SECURE = True
[ ] SECURE_SSL_REDIRECT = True
[ ] SECURE_HSTS_SECONDS configurado
[ ] X_FRAME_OPTIONS = 'DENY'
[ ] python manage.py check --deploy no muestra errores críticos
[ ] No hay vistas sensibles sin @login_required
[ ] No hay datos sensibles en campos ocultos de formularios
[ ] No se usa cursor.execute() con strings concatenados del usuario
[ ] Las contraseñas se hashean (Django lo hace automáticamente)
[ ] AUTH_PASSWORD_VALIDATORS está configurado
```

### El test definitivo

```bash
$ python manage.py check --deploy

# Si no da WARNINGS ni ERRORS → tu configuración de seguridad es correcta
# Si da WARNINGS → léelos uno por uno y arregla cada uno
```

> 💡 **Regla de oro:** Si `python manage.py check --deploy` da 0 warnings, tu configuración básica de seguridad está bien. No es garantía total, pero cubre el 80% de los errores comunes.

---

---

# 📦 9. Fase 7 — Dependencias y `requirements.txt`

---

## ¿Por qué importa?

Tu proyecto funciona en tu máquina porque tiene todas las librerías instaladas. El servidor no tiene nada. Necesitas decirle **exactamente** qué instalar y en qué versión.

## Generar el requirements.txt

```bash
# Forma básica:
pip freeze > requirements.txt

# El archivo se ve así:
Django==5.1.5
Pillow==10.2.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
whitenoise==6.6.0
```

## Checklist de dependencias

```
[ ] requirements.txt existe y está actualizado
[ ] Las versiones están fijadas (== no >=)
    → Django==5.1.5 ✅
    → Django>=5.0 ❌ (puede instalar una versión incompatible)

[ ] No hay librerías de desarrollo en requirements.txt
    → Separar: requirements.txt (producción) y requirements-dev.txt (desarrollo)
    → Ejemplo: django-debug-toolbar va en dev, NO en producción

[ ] pip-audit no reporta vulnerabilidades
    → pip install pip-audit && pip-audit
    → Revisa si alguna librería tiene CVEs conocidos

[ ] El entorno virtual está limpio
    → No tiene librerías de otros proyectos
```

### Patrón de archivos de requirements

```
requirements/
├── base.txt          # Lo que necesitan TODOS los entornos
├── development.txt   # Solo desarrollo (debug-toolbar, etc.)
└── production.txt    # Solo producción (gunicorn, psycopg2, etc.)
```

```
# requirements/development.txt
-r base.txt
django-debug-toolbar==4.2.0
```

```
# requirements/production.txt
-r base.txt
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
```

---

---

# 📂 10. Fase 8 — Git, `.gitignore` y Control de Versiones

---

## ¿Qué NUNCA debe subirse a Git?

```gitignore
# .gitignore — MÍNIMO para un proyecto Django

# Entorno virtual
venv/
.venv/
env/

# Variables de entorno con secretos
.env

# Base de datos local
db.sqlite3
*.sqlite3

# Archivos compilados de Python
__pycache__/
*.py[cod]
*.pyc

# Archivos de media subidos por usuarios
media/

# Archivos estáticos recopilados
staticfiles/

# IDE y editor
.vscode/
.idea/
*.swp
*.swo

# Sistema operativo
.DS_Store
Thumbs.db

# Logs
*.log
```

## Checklist de Git

```
[ ] .gitignore existe y cubre todo lo de arriba
[ ] El archivo .env NO está en el historial de git
    → Verificar: git log --all --full-history -- .env
    → Si aparece: hay que limpiar el historial (git filter-branch)

[ ] No hay archivos grandes innecesarios en el repo
    → Imágenes pesadas, videos, backups de BD

[ ] El proyecto tiene un README.md con instrucciones de setup
    → Cómo instalar, cómo correr, cómo hacer deploy

[ ] Los commits tienen mensajes descriptivos
    → "fix bug" ❌ → "Fix: validación de email duplicado en formulario de registro" ✅
```

> ⚠️ **Dato importante:** Una vez que un archivo se sube a Git, **queda en el historial para siempre**, incluso si lo borras después. Si subiste un `.env` con un `SECRET_KEY`, esa clave está comprometida aunque la borres. Hay que regenerarla.

---

---

# 🧪 11. Fase 9 — Testing: ¿Funciona Todo?

---

## Niveles de testing antes de deploy

```
NIVEL 1: ¿La app arranca?
──────────────────────────
python manage.py check              → ¿Hay errores de configuración?
python manage.py migrate --check    → ¿Hay migraciones pendientes?
python manage.py collectstatic      → ¿Los estáticos se recopilan bien?

NIVEL 2: ¿Los tests pasan?
──────────────────────────
python manage.py test               → ¿Todos los tests unitarios pasan?

NIVEL 3: ¿Funciona como usuario?
──────────────────────────────────
Abrir cada página principal          → ¿Carga correctamente?
Enviar cada formulario               → ¿Procesa sin error?
Probar login / logout                → ¿Funciona?
Probar con datos extremos            → Vacíos, muy largos, caracteres especiales

NIVEL 4: ¿Funciona en el servidor?
──────────────────────────────────
Después de deploy, repetir nivel 3   → En la URL real, no en localhost
```

## Checklist de testing

```
[ ] python manage.py check no da errores
[ ] python manage.py check --deploy no da warnings críticos
[ ] python manage.py test pasa al 100%
[ ] Probé manualmente las funcionalidades principales
[ ] Probé con un navegador diferente
[ ] Probé en modo incógnito (sin caché)
[ ] Probé la versión móvil (responsive)
```

---

---

# 🖥️ 12. Fase 10 — El Servidor: ¿Dónde Vive tu App?

---

## Opciones de hosting para Django

| Plataforma         | Dificultad   | Costo          | Ideal para                          |
| :----------------- | :----------- | :------------- | :---------------------------------- |
| **Railway**        | ⭐ Fácil     | Gratis/Pago    | Proyectos pequeños, demos           |
| **Render**         | ⭐ Fácil     | Gratis/Pago    | Apps con base de datos              |
| **DigitalOcean**   | ⭐⭐ Medio   | Desde $5/mes   | Proyectos medianos                  |
| **AWS EC2**        | ⭐⭐⭐ Difícil | Variable       | Producción empresarial              |
| **Heroku**         | ⭐ Fácil     | Desde $5/mes   | Prototipado rápido                  |
| **VPS propio**     | ⭐⭐⭐ Difícil | Desde $3/mes   | Control total                       |

## ¿Qué necesita el servidor?

```
MÍNIMO PARA DJANGO EN PRODUCCIÓN:
─────────────────────────────────
✅ Python 3.10+
✅ pip (gestor de paquetes)
✅ Entorno virtual (venv)
✅ Base de datos (PostgreSQL)
✅ Servidor WSGI (Gunicorn)
✅ Servidor web reverso (Nginx) — opcional con algunos hosts
✅ Certificado SSL (Let's Encrypt — gratis)
```

## La arquitectura de producción

```
                    INTERNET
                       │
                       ▼
              ┌─────────────────┐
              │     NGINX       │  ← Sirve archivos estáticos
              │  (puerto 80/443)│  ← Maneja HTTPS
              │                 │  ← Redirige requests a Gunicorn
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    GUNICORN     │  ← Servidor WSGI
              │  (puerto 8000)  │  ← Ejecuta tu código Django
              │                 │  ← Maneja múltiples workers
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     DJANGO      │  ← Tu aplicación
              │   (tu código)   │  ← Procesa la lógica de negocio
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   POSTGRESQL    │  ← Base de datos
              │  (puerto 5432)  │  ← Almacena los datos
              └─────────────────┘
```

### ¿Por qué NO `python manage.py runserver` en producción?

| `runserver`                                | Gunicorn                                   |
| :----------------------------------------- | :----------------------------------------- |
| Un solo proceso, un solo hilo              | Múltiples workers en paralelo              |
| Se cae con carga media                     | Diseñado para manejar cientos de requests  |
| No tiene seguridad                         | Puede configurarse con timeouts y límites  |
| Es para **desarrollo**                     | Es para **producción**                     |

> ⚠️ **La documentación de Django lo dice explícitamente:** _"DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests."_ No es opinión — es una advertencia oficial.

---

---

# 🌐 13. Fase 11 — DNS y Dominio

---

## ¿Qué es un dominio?

Es la dirección legible: `www.miapp.com` en vez de `143.198.45.123`.

## Configuración básica de DNS

```
TIPO     NOMBRE           VALOR                    PARA QUÉ
─────    ──────           ─────                    ─────────
A        miapp.com        143.198.45.123           Apunta el dominio a la IP del servidor
CNAME    www.miapp.com    miapp.com                www redirige al dominio principal
```

## Checklist de dominio

```
[ ] El dominio está registrado y activo
[ ] Los registros DNS apuntan al servidor correcto
[ ] ALLOWED_HOSTS en Django incluye el dominio
[ ] La propagación DNS completó (puede tardar hasta 48h)
[ ] Tanto miapp.com como www.miapp.com funcionan
```

---

---

# 🔒 14. Fase 12 — HTTPS y Certificados SSL

---

## ¿Por qué HTTPS es obligatorio?

Sin HTTPS, **todo** lo que viaja entre el usuario y tu servidor va en texto plano. Contraseñas, datos personales, cookies — todo visible para cualquier persona en la misma red.

```
HTTP  (sin candado 🔓)              HTTPS (con candado 🔐)
─────────────────────                ──────────────────────
usuario: juan                        ◆◇▲●□◆◇▲●□◆◇▲●□
password: micontraseña123            ◆◇▲●□◆◇▲●□◆◇▲●□

↑ Cualquiera en la red WiFi          ↑ Cifrado. Nadie puede leerlo.
  puede leer esto.
```

## Certificado SSL gratuito con Let's Encrypt

```bash
# En un servidor con Nginx (Ubuntu/Debian):
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d miapp.com -d www.miapp.com

# Certbot:
# 1. Obtiene el certificado automáticamente
# 2. Configura Nginx para HTTPS
# 3. Se renueva automáticamente cada 90 días
```

## Checklist de HTTPS

```
[ ] Certificado SSL instalado y válido
[ ] HTTP redirige automáticamente a HTTPS
[ ] SECURE_SSL_REDIRECT = True en Django
[ ] SESSION_COOKIE_SECURE = True
[ ] CSRF_COOKIE_SECURE = True
[ ] Verificar en el navegador: candado verde en la barra de direcciones
```

---

---

# 📊 15. Fase 13 — Monitoreo y Logs Post-Deploy

---

Deploy no es el final. Es el **principio** de la operación.

## ¿Qué monitorear?

```
ERRORES          → ¿Hay errores 500 en los logs?
RENDIMIENTO      → ¿Las páginas cargan en menos de 3 segundos?
DISPONIBILIDAD   → ¿El sitio está arriba 24/7?
SEGURIDAD        → ¿Hay intentos de acceso sospechosos?
BASE DE DATOS    → ¿Las queries son eficientes? ¿Hay conexiones colgadas?
DISCO            → ¿Hay espacio suficiente? (logs y media crecen)
```

## Herramientas de monitoreo

| Herramienta          | ¿Qué hace?                                      | Costo           |
| :------------------- | :----------------------------------------------- | :-------------- |
| **Sentry**           | Captura errores automáticamente con contexto      | Gratis hasta 5k eventos/mes |
| **UptimeRobot**      | Te avisa si tu sitio se cae                      | Gratis          |
| **New Relic**        | Rendimiento detallado de la app                  | Gratis tier     |
| **Logs del servidor** | `tail -f /var/log/django/app.log`                | Gratis          |

## Checklist post-deploy

```
[ ] El sitio carga correctamente en la URL de producción
[ ] Los formularios funcionan (enviar uno de prueba)
[ ] Login y logout funcionan
[ ] Los archivos estáticos cargan (CSS, JS, imágenes)
[ ] Los uploads de usuarios funcionan (si aplica)
[ ] Los logs registran actividad correctamente
[ ] Hay un plan de backup activo para la base de datos
[ ] Alguien sabe cómo restaurar si algo falla
```

---

---

# ✅ 16. El Mega-Checklist: Todo en Una Página

---

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                  🚀 MEGA-CHECKLIST PRE-DEPLOY DJANGO                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📝 CÓDIGO                                                                   │
│  [ ] Sin prints de debugging                                                 │
│  [ ] Sin código comentado innecesario                                        │
│  [ ] Sin contraseñas hardcodeadas                                            │
│  [ ] Vistas protegidas con @login_required donde corresponda                │
│  [ ] Formularios con validación server-side                                  │
│                                                                              │
│  ⚙️ SETTINGS                                                                 │
│  [ ] DEBUG = False                                                           │
│  [ ] SECRET_KEY en variable de entorno                                       │
│  [ ] ALLOWED_HOSTS con dominio específico                                    │
│  [ ] Base de datos PostgreSQL configurada                                    │
│  [ ] Cookies seguras (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)            │
│  [ ] Headers de seguridad configurados                                       │
│  [ ] LOGGING configurado                                                     │
│                                                                              │
│  🔐 SECRETOS                                                                 │
│  [ ] Archivo .env con valores reales                                         │
│  [ ] .env en .gitignore                                                      │
│  [ ] .env.example con valores de ejemplo en git                              │
│  [ ] Ningún secreto en el código fuente                                      │
│                                                                              │
│  🗄️ BASE DE DATOS                                                            │
│  [ ] Migraciones al día (makemigrations --check)                             │
│  [ ] Todas las migraciones aplicadas (showmigrations)                        │
│  [ ] Plan de backups definido                                                │
│  [ ] Sin datos de prueba                                                     │
│                                                                              │
│  📁 ARCHIVOS                                                                 │
│  [ ] STATIC_ROOT configurado                                                 │
│  [ ] collectstatic funciona sin errores                                      │
│  [ ] MEDIA_ROOT configurado (si hay uploads)                                 │
│  [ ] WhiteNoise o Nginx sirviendo estáticos                                  │
│                                                                              │
│  🛡️ SEGURIDAD                                                                │
│  [ ] python manage.py check --deploy → 0 warnings                           │
│  [ ] CSRF activo en todos los formularios POST                               │
│  [ ] No hay SQL concatenado con input del usuario                            │
│  [ ] AUTH_PASSWORD_VALIDATORS configurado                                    │
│                                                                              │
│  📦 DEPENDENCIAS                                                             │
│  [ ] requirements.txt actualizado con versiones fijadas                      │
│  [ ] pip-audit sin vulnerabilidades                                          │
│  [ ] Sin librerías de desarrollo en producción                               │
│                                                                              │
│  📂 GIT                                                                      │
│  [ ] .gitignore completo                                                     │
│  [ ] .env nunca en el historial de git                                       │
│  [ ] README.md con instrucciones de setup                                    │
│                                                                              │
│  🧪 TESTING                                                                  │
│  [ ] python manage.py check → sin errores                                    │
│  [ ] python manage.py test → 100% pasan                                      │
│  [ ] Prueba manual de funcionalidades principales                            │
│  [ ] Prueba en móvil                                                         │
│                                                                              │
│  🖥️ SERVIDOR                                                                 │
│  [ ] Gunicorn como servidor WSGI (no runserver)                              │
│  [ ] Nginx como reverse proxy                                                │
│  [ ] Certificado SSL instalado (Let's Encrypt)                               │
│  [ ] HTTP redirige a HTTPS                                                   │
│                                                                              │
│  🌐 DOMINIO                                                                  │
│  [ ] DNS configurado correctamente                                           │
│  [ ] ALLOWED_HOSTS incluye el dominio                                        │
│  [ ] www y sin-www funcionan                                                  │
│                                                                              │
│  📊 POST-DEPLOY                                                              │
│  [ ] Sitio carga en la URL de producción                                     │
│  [ ] Formularios funcionan                                                   │
│  [ ] Archivos estáticos cargan                                               │
│  [ ] Logs registran correctamente                                            │
│  [ ] Backup automático activo                                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

---

# ❌ 17. Los 10 Errores de Deploy Más Comunes (y Cómo Evitarlos)

---

### Error 1: "Subí con `DEBUG = True`"

**Consecuencia:** Todo el mundo ve tu código fuente cuando hay un error.
**Solución:** `DEBUG = False` + `python manage.py check --deploy`.

---

### Error 2: "Mi `SECRET_KEY` está en GitHub"

**Consecuencia:** Cualquiera puede falsificar sesiones y hacerse pasar por admin.
**Solución:** Variable de entorno + `.gitignore` + regenerar la clave.

---

### Error 3: "Usé `runserver` en producción"

**Consecuencia:** Se cae con más de 5 usuarios simultáneos.
**Solución:** Gunicorn + Nginx.

---

### Error 4: "No hice `collectstatic`"

**Consecuencia:** El sitio carga sin CSS, sin JavaScript, sin imágenes. Todo roto visualmente.
**Solución:** `python manage.py collectstatic` + configurar WhiteNoise o Nginx.

---

### Error 5: "SQLite en producción"

**Consecuencia:** La base de datos se corrompe con escrituras simultáneas.
**Solución:** PostgreSQL.

---

### Error 6: "No tenía backups y se borró la base de datos"

**Consecuencia:** Pérdida total de datos. Irrecuperable.
**Solución:** Backup automático diario + guardar backups en otro servidor.

---

### Error 7: "No configuré HTTPS"

**Consecuencia:** Las contraseñas viajan en texto plano.
**Solución:** Let's Encrypt (gratis) + `SECURE_SSL_REDIRECT = True`.

---

### Error 8: "Las migraciones no estaban al día"

**Consecuencia:** Error 500 porque la base de datos no tiene las tablas/columnas que el código espera.
**Solución:** `python manage.py migrate` en el servidor antes de reiniciar la app.

---

### Error 9: "No puse `ALLOWED_HOSTS`"

**Consecuencia:** Django rechaza TODOS los requests con error 400.
**Solución:** `ALLOWED_HOSTS = ['midominio.com']`.

---

### Error 10: "No revisé los logs después de deploy"

**Consecuencia:** Errores silenciosos que afectan a usuarios durante días.
**Solución:** Revisar logs las primeras horas. Configurar alertas con Sentry.

---

---

# 🗺️ 18. Diagrama: El Flujo Completo de Deploy

---

```
           ┌─────────────────────────────────────────────────────────────┐
           │                    FLUJO DE DEPLOY                          │
           └─────────────────────────────────────────────────────────────┘

    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  CÓDIGO  │───▷│  CONFIG  │───▷│   GIT    │───▷│ SERVIDOR │
    │  LIMPIO  │    │ SEGURA   │    │  PUSH    │    │  SETUP   │
    └──────────┘    └──────────┘    └──────────┘    └──────────┘
         │               │               │               │
    ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Sin      │    │ DEBUG=   │    │ .gitignore│   │ Python   │
    │ prints   │    │ False    │    │ correcto │    │ Gunicorn │
    │ Sin      │    │ SECRET   │    │ .env NO  │    │ Nginx    │
    │ hardcode │    │ en .env  │    │ en git   │    │ PostgreSQL│
    └─────────┘    └──────────┘    └──────────┘    └──────────┘
                                                        │
                                                        ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │MONITOREO │◁───│  HTTPS   │◁───│   DNS    │◁───│  DEPLOY  │
    │  Y LOGS  │    │   SSL    │    │ DOMINIO  │    │ MIGRATE  │
    └──────────┘    └──────────┘    └──────────┘    │COLLECTST.│
         │                                          └──────────┘
    ┌─────────┐
    │ Sentry  │
    │ Logs    │
    │ Backups │
    │ Alertas │
    └─────────┘

    ✅ Si todo está verde → ¡TU APP ESTÁ EN PRODUCCIÓN!
```

---

---

# 🏁 Resumen de la Clase

---

## ✅ Lo que cubrimos hoy

| Fase                     | La idea clave                                                             |
| :----------------------- | :------------------------------------------------------------------------ |
| **Código limpio**        | Sin prints, sin hardcodes, sin código muerto                             |
| **Settings producción**  | `DEBUG=False`, `SECRET_KEY` en .env, cookies seguras                     |
| **Secretos**             | `.env` + `.env.example` + `.gitignore`                                   |
| **Base de datos**        | PostgreSQL, migraciones al día, backups                                  |
| **Archivos estáticos**   | `collectstatic` + WhiteNoise o Nginx                                     |
| **Seguridad**            | `check --deploy`, CSRF, headers, validación server-side                  |
| **Dependencias**         | `requirements.txt` con versiones fijadas                                 |
| **Git**                  | `.gitignore` completo, `.env` nunca en historial                         |
| **Testing**              | `check`, `test`, prueba manual, prueba móvil                             |
| **Servidor**             | Gunicorn + Nginx, NUNCA `runserver`                                      |
| **DNS y Dominio**        | Registros A/CNAME, `ALLOWED_HOSTS`                                       |
| **HTTPS**                | Let's Encrypt, certificado SSL, cookies seguras                          |
| **Monitoreo**            | Logs, Sentry, backups, alertas                                           |

---

> _"El deploy no es el final del proyecto. Es el momento en que el proyecto empieza a vivir de verdad. Prepáralo bien para que sobreviva."_

---

## 📚 Referencias (APA 7ª ed.)

Django Software Foundation. (2025). _Deployment checklist_. https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

Django Software Foundation. (2025). _How to deploy Django_. https://docs.djangoproject.com/en/stable/howto/deployment/

Django Software Foundation. (2025). _Settings reference_. https://docs.djangoproject.com/en/stable/ref/settings/

OWASP Foundation. (2025). _OWASP Top Ten_. https://owasp.org/www-project-top-ten/

Let's Encrypt. (2025). _Getting Started_. https://letsencrypt.org/getting-started/

Greenfeld, D. R., & Greenfeld, A. R. (2024). _Two Scoops of Django 5.x: Best Practices for the Django Web Framework_. Two Scoops Press. [Capítulo sobre Deployment]

IBM Security. (2024). _Cost of a Data Breach Report 2024_. https://www.ibm.com/reports/data-breach

---
