# 🎓 Solución Paso a Paso: PokéParty Optimizer (Edición Django)

---

> _"El objetivo de esta guía no es solo mostrarte el código, sino explicarte **por qué** cada decisión se toma de esa forma. Cuando entiendas el 'por qué', podrás construir cualquier proyecto por tu cuenta."_

---

## 📁 Repositorio de referencia del profesor

> 🔗 **[github.com/arielrosenmann94/pokeparty_django](https://github.com/arielrosenmann94/pokeparty_django)**
>
> Úsalo como guía de consulta **después** de intentar la solución por tu cuenta.

---

## 📋 Antes de empezar: ¿Qué vamos a construir?

Vamos a construir una aplicación web completa en Django que:

1. Se conecta a la **PokeAPI** (una API pública real) para obtener datos de Pokémon.
2. Permite **capturar Pokémon aleatorios** filtrando por tipo.
3. Los **persiste en base de datos** para que sobrevivan al refrescar la página.
4. Gestiona un equipo principal (**Party**, máximo 6) y una reserva (**PC Box**).
5. Permite **ordenar y optimizar** el equipo basándose en estadísticas reales.

> 📊 **Dato real**: La PokeAPI recibe más de 350 millones de peticiones mensuales, convirtiéndola en una de las APIs públicas más utilizadas del mundo para aprendizaje de desarrollo web.
>
> _Fuente: PokeAPI GitHub Repository — estadísticas de uso 2025_

---

---

# PASO 1 — Preparar el entorno de trabajo

---

## ¿Por qué un entorno virtual?

Cada proyecto Python debe vivir en su propia "burbuja" de dependencias. Si instalas librerías globalmente, eventualmente un proyecto necesitará la versión 3 de una librería mientras otro necesita la versión 4, y se producen conflictos difíciles de diagnosticar.

```bash
# 1. Crear el entorno virtual (una carpeta aislada con su propio Python)
python -m venv venv

# 2. Activarlo (esto modifica tu PATH para usar el Python del entorno)
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# 3. Instalar las dependencias que necesitamos
pip install django requests
```

**¿Por qué `requests`?** Django sabe manejar peticiones que llegan _hacia_ tu servidor, pero no incluye herramientas para hacer peticiones _desde_ tu servidor hacia otra API externa. La librería `requests` llena ese vacío de forma elegante.

---

## Crear el proyecto y la aplicación

```bash
# Crear el proyecto Django (el punto final indica "en este directorio")
django-admin startproject pokeparty .

# Crear la aplicación donde vivirá toda nuestra lógica
python manage.py startapp core
```

**¿Por qué separar proyecto de aplicación?** El **proyecto** (`pokeparty/`) contiene la configuración global (settings, URLs raíz). La **aplicación** (`core/`) contiene la lógica de negocio (modelos, vistas, templates). Esta separación permite reutilizar aplicaciones entre proyectos distintos y mantener el código organizado.

---

## Registrar la aplicación

En `pokeparty/settings.py`, debemos decirle a Django que nuestra app existe:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # ← Nuestra aplicación de Pokémon
]
```

**¿Por qué es obligatorio?** Django no escanea automáticamente las carpetas. Si no registras tu app, los modelos no se detectan, las migraciones no se generan y los templates no se encuentran.

---

---

# PASO 2 — Diseñar el modelo de datos

---

## ¿Por qué empezar por el modelo?

En Django, el modelo define la **estructura de la base de datos**. Es la base sobre la que se construye todo lo demás. Si el modelo está bien diseñado, las vistas y templates fluyen naturalmente. Si está mal diseñado, todo lo demás se complica.

## Archivo: `core/models.py`

```python
from django.db import models


class Pokemon(models.Model):
    """
    Representa un Pokémon capturado desde la PokeAPI.
    
    ¿Por qué estos campos?
    - ext_id: Necesitamos un identificador que coincida con la PokeAPI
      para evitar duplicados. Un Pokémon no puede existir dos veces.
    - en_party: Un booleano simple para separar Party de PC Box.
      Es más eficiente que tener dos tablas separadas.
    """
    
    # Identificación
    ext_id = models.IntegerField(unique=True)  # unique=True evita duplicados
    nombre = models.CharField(max_length=100)
    imagen_url = models.URLField()
    tipo = models.CharField(max_length=50)
    
    # Stats del Pokémon (todos vienen de la PokeAPI)
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    sp_attack = models.IntegerField(default=0)
    sp_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    
    # ¿Está en el equipo activo o en la reserva?
    en_party = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"

    def __str__(self):
        return f"{self.nombre.capitalize()} (#{self.ext_id})"

    @property
    def total_power(self):
        """
        ¿Por qué una @property y no un campo en la BD?
        
        Porque este valor se CALCULA a partir de otros campos.
        Si lo guardáramos como campo, tendríamos datos redundantes
        y el riesgo de que se desincronicen. Con @property, 
        siempre se calcula en tiempo real.
        
        Fórmula: totalPower = hp + attack + defense + sp_attack + sp_defense + speed
        """
        return self.hp + self.attack + self.defense + self.sp_attack + self.sp_defense + self.speed
```

---

## Aplicar las migraciones

```bash
# Paso 1: Django lee tu modelo y genera un archivo SQL de migración
python manage.py makemigrations

# Paso 2: Django ejecuta ese archivo contra la base de datos
python manage.py migrate
```

**¿Qué pasa internamente?** `makemigrations` compara el estado actual de tus modelos con el estado anterior y genera un "diff" (archivo de migración). `migrate` aplica ese diff a la base de datos real. Esto permite tener un historial completo de cambios en tu esquema.

---

---

# PASO 3 — Conectar con la PokeAPI

---

## ¿Por qué un archivo separado para servicios?

Es una **buena práctica de ingeniería** separar la lógica que se comunica con servicios externos en su propio archivo. Las razones son:

1. **Responsabilidad única**: Las vistas manejan la lógica web; los servicios manejan la comunicación externa.
2. **Facilidad de testing**: Puedes testear la lógica de la API sin necesidad de levantar el servidor Django.
3. **Reutilización**: Si mañana necesitas acceder a la PokeAPI desde otra vista o un comando de management, ya tienes la función lista.

## Archivo: `core/services.py`

```python
import requests
import random


# Lista de tipos disponibles en la PokeAPI
# ¿Por qué definirla aquí? Porque es una constante del dominio
# que se usa tanto en las vistas como en los templates.
TIPOS_POKEMON = [
    'fire', 'water', 'grass', 'electric', 'psychic',
    'ghost', 'normal', 'fighting', 'flying', 'poison',
    'ground', 'rock', 'bug', 'dragon', 'steel',
    'ice', 'dark', 'fairy',
]


def obtener_pokemon_aleatorio_por_tipo(tipo_pokemon):
    """
    Conecta con la PokeAPI y devuelve los datos de un Pokémon
    aleatorio del tipo solicitado.
    
    ¿Cómo funciona la PokeAPI?
    
    Paso 1: /api/v2/type/{tipo} → devuelve una LISTA de todos
    los Pokémon de ese tipo (solo nombres y URLs).
    
    Paso 2: Elegimos uno al azar de esa lista.
    
    Paso 3: /api/v2/pokemon/{id} → devuelve los DETALLES
    completos de ese Pokémon (stats, sprites, etc.)
    
    Son DOS peticiones HTTP, no una. La primera para filtrar
    por tipo, la segunda para obtener los detalles.
    """
    
    # === PETICIÓN 1: Obtener la lista de Pokémon del tipo ===
    url_tipo = f"https://pokeapi.co/api/v2/type/{tipo_pokemon.lower()}"
    respuesta = requests.get(url_tipo)
    
    # Si la API falla, retornamos None en vez de crashear
    if respuesta.status_code != 200:
        return None
    
    data = respuesta.json()
    lista_pokemon = data['pokemon']  # Lista de diccionarios
    
    # Si no hay Pokémon de ese tipo (caso raro), retornamos None
    if not lista_pokemon:
        return None
    
    # === ELECCIÓN ALEATORIA ===
    # random.choice() elige un elemento al azar de la lista
    elegido = random.choice(lista_pokemon)
    url_detalle = elegido['pokemon']['url']
    
    # === PETICIÓN 2: Obtener detalles del Pokémon elegido ===
    respuesta_detalle = requests.get(url_detalle)
    
    if respuesta_detalle.status_code != 200:
        return None
    
    pokemon_data = respuesta_detalle.json()
    
    # === EXTRAER STATS ===
    # La PokeAPI devuelve los stats así:
    # [{"stat": {"name": "hp"}, "base_stat": 45}, ...]
    # 
    # Necesitamos transformarlo a un diccionario plano:
    # {"hp": 45, "attack": 49, ...}
    #
    # El replace('-', '_') convierte "special-attack" en "special_attack"
    # para que coincida con nuestros campos del modelo.
    stats = {}
    for stat_entry in pokemon_data['stats']:
        nombre_stat = stat_entry['stat']['name'].replace('-', '_')
        valor_stat = stat_entry['base_stat']
        stats[nombre_stat] = valor_stat
    
    # === CONSTRUIR EL RESULTADO ===
    # Retornamos un diccionario limpio que se puede usar
    # directamente para crear o actualizar el modelo.
    return {
        'ext_id': pokemon_data['id'],
        'nombre': pokemon_data['name'],
        'imagen_url': pokemon_data['sprites']['other']['home']['front_default']
                      or pokemon_data['sprites']['front_default'],
        'tipo': tipo_pokemon,
        'hp': stats.get('hp', 0),
        'attack': stats.get('attack', 0),
        'defense': stats.get('defense', 0),
        'sp_attack': stats.get('special_attack', 0),
        'sp_defense': stats.get('special_defense', 0),
        'speed': stats.get('speed', 0),
    }
```

> 📊 **Dato real**: La PokeAPI tiene datos de más de 1.300 Pokémon y más de 800 movimientos. Es completamente gratuita y no requiere autenticación, lo que la convierte en una herramienta ideal para aprender consumo de APIs.
>
> _Fuente: PokeAPI Docs — https://pokeapi.co/docs/v2_

---

---

# PASO 4 — La lógica de negocio en las vistas

---

## ¿Qué hace cada vista?

Tenemos tres funciones principales:

1. **`index`** → Muestra la página principal con la Party y la PC Box.
2. **`capturar`** → Recibe el tipo seleccionado, busca un Pokémon aleatorio y lo guarda.
3. **`optimizar_equipo`** → Reorganiza Party y PC Box para tener los 6 más fuertes.
4. **`ordenar_por_stat`** → Permite ordenar la vista por un stat específico.

## Archivo: `core/views.py`

```python
from django.shortcuts import render, redirect
from .models import Pokemon
from .services import obtener_pokemon_aleatorio_por_tipo, TIPOS_POKEMON


def index(request):
    """
    Vista principal — Muestra Party y PC Box.
    
    ¿Por qué separamos los querysets con filter()?
    Porque la Party tiene en_party=True y la PC Box tiene 
    en_party=False. Es más eficiente hacer dos consultas filtradas
    que traer todo y separar en Python.
    """
    # Obtener el parámetro de ordenamiento (si existe)
    ordenar_por = request.GET.get('ordenar', None)
    
    # Definir el orden según el parámetro recibido
    # ¿Por qué el signo menos (-)?
    # En Django ORM, el prefijo "-" significa orden DESCENDENTE.
    # Queremos los más altos primero.
    orden_validos = {
        'hp': '-hp',
        'attack': '-attack',
        'defense': '-defense',
        'speed': '-speed',
        'sp_attack': '-sp_attack',
        'sp_defense': '-sp_defense',
    }
    
    orden = orden_validos.get(ordenar_por, '-hp')  # Por defecto: HP
    
    party = Pokemon.objects.filter(en_party=True).order_by(orden)
    pc_box = Pokemon.objects.filter(en_party=False).order_by(orden)
    
    contexto = {
        'party': party,
        'pc_box': pc_box,
        'tipos': TIPOS_POKEMON,
        'orden_actual': ordenar_por or 'hp',
    }
    
    return render(request, 'core/index.html', contexto)


def capturar(request):
    """
    Captura un Pokémon aleatorio del tipo seleccionado.
    
    ¿Por qué verificamos que sea POST?
    Porque esta vista MODIFICA datos (crea registros en la BD).
    Las buenas prácticas HTTP dicen que las operaciones de 
    escritura deben usar POST, no GET. GET es solo para lectura.
    
    ¿Por qué usamos update_or_create?
    Porque si el usuario captura un Pikachu y luego captura otro
    Pikachu, no queremos duplicados. update_or_create busca por
    ext_id: si existe, lo actualiza; si no existe, lo crea.
    """
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        pokemon_data = obtener_pokemon_aleatorio_por_tipo(tipo)
        
        if pokemon_data:
            # === LÓGICA DE LOS 6 CUPOS ===
            # Contamos cuántos Pokémon están actualmente en la Party
            cantidad_en_party = Pokemon.objects.filter(en_party=True).count()
            
            # Si hay menos de 6, el nuevo entra directo.
            # Si ya hay 6, va a la PC Box (en_party=False).
            entra_a_party = cantidad_en_party < 6
            
            # Guardamos en la base de datos
            Pokemon.objects.update_or_create(
                ext_id=pokemon_data['ext_id'],  # Campo de búsqueda
                defaults={                       # Campos a crear/actualizar
                    'nombre': pokemon_data['nombre'],
                    'imagen_url': pokemon_data['imagen_url'],
                    'tipo': pokemon_data['tipo'],
                    'hp': pokemon_data['hp'],
                    'attack': pokemon_data['attack'],
                    'defense': pokemon_data['defense'],
                    'sp_attack': pokemon_data['sp_attack'],
                    'sp_defense': pokemon_data['sp_defense'],
                    'speed': pokemon_data['speed'],
                    'en_party': entra_a_party,
                }
            )
    
    # ¿Por qué redirect en vez de render?
    # Usamos el patrón POST-Redirect-GET (PRG).
    # Si hiciéramos render, al refrescar la página el navegador
    # re-enviaría el POST y capturaría otro Pokémon sin querer.
    return redirect('index')


def optimizar_equipo(request):
    """
    Reorganiza la Party y PC Box para tener los 6 Pokémon
    con mayor totalPower en el equipo activo.
    
    ¿Por qué traemos todos a Python en vez de calcularlo en SQL?
    Porque total_power es una @property de Python, no un campo
    en la base de datos. Para calcularlo en SQL necesitaríamos
    usar annotate() con F() expressions. Ambos enfoques son 
    válidos, pero para este ejercicio la forma con Python es 
    más legible y didáctica.
    
    Fórmula: totalPower = hp + attack + defense + sp_attack + sp_defense + speed
    """
    # 1. Traemos TODOS los Pokémon de la BD a memoria
    todos_los_pokemon = list(Pokemon.objects.all())
    
    # 2. Ordenamos en Python por total_power (de mayor a menor)
    todos_los_pokemon.sort(key=lambda p: p.total_power, reverse=True)
    
    # 3. Los 6 primeros son los más poderosos
    ids_mejores = [p.id for p in todos_los_pokemon[:6]]
    
    # 4. Actualizamos la BD en DOS operaciones masivas
    # Primero: TODOS van a PC Box
    Pokemon.objects.all().update(en_party=False)
    # Después: Solo los 6 mejores van a Party
    Pokemon.objects.filter(id__in=ids_mejores).update(en_party=True)
    
    # ¿Por qué dos updates y no un loop?
    # Porque update() ejecuta UNA sola consulta SQL para todos
    # los registros. Un loop haría N consultas (una por Pokémon).
    # Esto se llama "bulk update" y es mucho más eficiente.
    
    return redirect('index')
```

---

---

# PASO 5 — Configurar las URLs

---

## ¿Cómo llegan las peticiones a nuestras vistas?

Django usa un sistema de **rutas** (URLs) para decidir qué vista debe responder a cada URL del navegador. Necesitamos conectar tres URLs a nuestras tres vistas.

## Archivo: `pokeparty/urls.py` (archivo raíz del proyecto)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include() delega las URLs de la app core a su propio archivo
    # ¿Por qué no poner todo aquí? Porque si tu proyecto crece
    # y tiene 5 apps, este archivo se volvería imposible de leer.
    path('', include('core.urls')),
]
```

## Archivo: `core/urls.py` (NUEVO — crear este archivo)

```python
from django.urls import path
from . import views

# ¿Por qué cada URL tiene un name?
# Porque en los templates usamos {% url 'nombre' %} en vez de
# escribir la URL directamente. Si mañana cambias '/capturar/'
# por '/catch/', solo modificas AQUÍ y todo sigue funcionando.

urlpatterns = [
    path('', views.index, name='index'),
    path('capturar/', views.capturar, name='capturar'),
    path('optimizar/', views.optimizar_equipo, name='optimizar_equipo'),
]
```

---

---

# PASO 6 — Construir la interfaz visual (Template)

---

## ¿Por qué el template está en `core/templates/core/`?

Django busca templates dentro de cada app registrada, en una carpeta llamada `templates/`. La sub-carpeta `core/` evita conflictos de nombres si tienes múltiples apps con un template llamado `index.html`.

```
core/
├── templates/
│   └── core/
│       └── index.html     ← Aquí vive nuestro template
├── models.py
├── views.py
├── services.py
└── urls.py
```

## Archivo: `core/templates/core/index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokéParty Optimizer ⚔️</title>
    
    <!-- Google Fonts: tipografía moderna y profesional -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* ============================================
           VARIABLES CSS (Design Tokens)
           ============================================
           ¿Por qué variables? Porque si mañana quieres
           cambiar el color primario, solo lo cambias en
           UN lugar y se aplica en TODA la app.
        */
        :root {
            --bg-dark: #0f0f23;
            --bg-card: rgba(255, 255, 255, 0.06);
            --bg-card-hover: rgba(255, 255, 255, 0.12);
            --text-primary: #e0e0e0;
            --text-secondary: #8b8b9e;
            --accent-fire: #ff6b35;
            --accent-water: #4fc3f7;
            --accent-electric: #ffd54f;
            --accent-optimize: #7c4dff;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --shadow-glow: 0 0 20px rgba(124, 77, 255, 0.15);
            --radius: 16px;
            --radius-sm: 10px;
        }

        /* ============================================
           RESET Y BASE
           ============================================ */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 16px;
        }

        /* ============================================
           LAYOUT PRINCIPAL
           ============================================
           max-width limita el ancho en pantallas grandes
           (TVs, monitores ultra-wide) para que el contenido
           no se estire de forma ilegible.
        */
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* ============================================
           HEADER
           ============================================ */
        header {
            text-align: center;
            padding: 24px 0 32px;
        }

        header h1 {
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-fire), var(--accent-electric));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        header p {
            color: var(--text-secondary);
            margin-top: 8px;
            font-size: clamp(0.85rem, 2vw, 1rem);
        }

        /* ============================================
           PANEL DE CONTROLES
           ============================================
           flex-wrap: wrap permite que los botones bajen
           a la siguiente línea en pantallas pequeñas.
        */
        .controls {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 32px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(10px);
        }

        .controls-group {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }

        /* ============================================
           BOTONES Y SELECT
           ============================================ */
        select, button {
            font-family: 'Outfit', sans-serif;
            padding: 10px 18px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-subtle);
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.25s ease;
        }

        select {
            background: var(--bg-dark);
            color: var(--text-primary);
        }

        .btn-capture {
            background: linear-gradient(135deg, var(--accent-fire), #e84393);
            color: white;
            border: none;
        }

        .btn-capture:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
        }

        .btn-optimize {
            background: linear-gradient(135deg, var(--accent-optimize), #2196f3);
            color: white;
            border: none;
        }

        .btn-optimize:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-glow);
        }

        .btn-sort {
            background: var(--bg-card);
            color: var(--text-primary);
        }

        .btn-sort:hover, .btn-sort.active {
            background: var(--bg-card-hover);
            border-color: var(--accent-water);
            color: var(--accent-water);
        }

        /* ============================================
           SECCIONES
           ============================================ */
        .section-title {
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-subtle);
        }

        /* ============================================
           GRID RESPONSIVO DE CARDS
           ============================================
           Esta es la clave de la responsividad:
           
           - En celulares: 1 columna (minmax de 260px)
           - En tablets: 2 columnas
           - En desktop: 3 columnas
           - En TV: hasta 4 o 5 columnas
           
           auto-fill + minmax hace TODO esto automáticamente
           sin necesidad de media queries.
        */
        .pokemon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 48px;
        }

        /* ============================================
           CARDS DE POKÉMON
           ============================================ */
        .pokemon-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius);
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .pokemon-card:hover {
            transform: translateY(-6px);
            background: var(--bg-card-hover);
            box-shadow: var(--shadow-glow);
        }

        .pokemon-card img {
            width: 140px;
            height: 140px;
            object-fit: contain;
            margin-bottom: 12px;
            /* La animación sutil le da vida a la interfaz */
            transition: transform 0.3s ease;
        }

        .pokemon-card:hover img {
            transform: scale(1.1);
        }

        .pokemon-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .pokemon-card .pokemon-id {
            color: var(--text-secondary);
            font-size: 0.8rem;
        }

        .pokemon-card .pokemon-type {
            display: inline-block;
            background: rgba(255, 107, 53, 0.15);
            color: var(--accent-fire);
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            margin: 8px 0;
        }

        /* ============================================
           STATS BAR
           ============================================
           Las barras visuales hacen que los stats sean
           comparables de un vistazo, en vez de solo números.
        */
        .stats-container {
            text-align: left;
            margin-top: 12px;
        }

        .stat-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
            font-size: 0.75rem;
        }

        .stat-label {
            width: 30px;
            color: var(--text-secondary);
            font-weight: 600;
            text-align: right;
        }

        .stat-bar-bg {
            flex: 1;
            height: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            overflow: hidden;
        }

        .stat-bar-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.5s ease;
        }

        .stat-value {
            width: 28px;
            text-align: right;
            color: var(--text-secondary);
        }

        .total-power {
            margin-top: 10px;
            font-weight: 700;
            font-size: 0.9rem;
            color: var(--accent-electric);
        }

        /* ============================================
           PC BOX — ligeramente atenuada para diferenciar
           ============================================ */
        .pc-box-section {
            opacity: 0.75;
            transition: opacity 0.3s ease;
        }

        .pc-box-section:hover {
            opacity: 1;
        }

        /* ============================================
           ESTADO VACÍO
           ============================================ */
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-style: italic;
        }

        /* ============================================
           FORM INLINE
           ============================================ */
        .capture-form {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: center;
        }
    </style>
</head>
<body>
    <div class="container">
        
        <!-- ===== HEADER ===== -->
        <header>
            <h1>⚔️ PokéParty Optimizer</h1>
            <p>Captura, compara y optimiza tu equipo Pokémon ideal</p>
        </header>

        <!-- ===== CONTROLES DE CAPTURA ===== -->
        <section class="controls">
            <form action="{% url 'capturar' %}" method="post" class="capture-form">
                {% csrf_token %}
                <select name="tipo" id="tipo-select">
                    {% for t in tipos %}
                        <option value="{{ t }}">{{ t|title }}</option>
                    {% endfor %}
                </select>
                <button type="submit" class="btn-capture">🎯 Capturar Pokémon Random</button>
            </form>
            
            <a href="{% url 'optimizar_equipo' %}">
                <button type="button" class="btn-optimize">⚡ Mejor Equipo Posible</button>
            </a>
        </section>

        <!-- ===== BOTONES DE ORDENAMIENTO ===== -->
        <section class="controls">
            <span style="color: var(--text-secondary); font-size: 0.85rem;">Ordenar por:</span>
            <div class="controls-group">
                <a href="?ordenar=hp"><button type="button" class="btn-sort {% if orden_actual == 'hp' %}active{% endif %}">❤️ HP</button></a>
                <a href="?ordenar=attack"><button type="button" class="btn-sort {% if orden_actual == 'attack' %}active{% endif %}">⚔️ Ataque</button></a>
                <a href="?ordenar=defense"><button type="button" class="btn-sort {% if orden_actual == 'defense' %}active{% endif %}">🛡️ Defensa</button></a>
                <a href="?ordenar=speed"><button type="button" class="btn-sort {% if orden_actual == 'speed' %}active{% endif %}">💨 Velocidad</button></a>
                <a href="?ordenar=sp_attack"><button type="button" class="btn-sort {% if orden_actual == 'sp_attack' %}active{% endif %}">✨ Sp.Atk</button></a>
                <a href="?ordenar=sp_defense"><button type="button" class="btn-sort {% if orden_actual == 'sp_defense' %}active{% endif %}">🔮 Sp.Def</button></a>
            </div>
        </section>

        <!-- ===== PARTY (EQUIPO PRINCIPAL) ===== -->
        <h2 class="section-title">🛡️ Equipo Principal — Party ({{ party|length }}/6)</h2>

        {% if party %}
            <div class="pokemon-grid">
                {% for p in party %}
                    <div class="pokemon-card">
                        <img src="{{ p.imagen_url }}" alt="{{ p.nombre }}">
                        <h3>{{ p.nombre|capfirst }}</h3>
                        <span class="pokemon-id">#{{ p.ext_id }}</span>
                        <div>
                            <span class="pokemon-type">{{ p.tipo }}</span>
                        </div>
                        <div class="stats-container">
                            <div class="stat-row">
                                <span class="stat-label">HP</span>
                                <div class="stat-bar-bg">
                                    <div class="stat-bar-fill" style="width: {% widthratio p.hp 255 100 %}%; background: #ff6b6b;"></div>
                                </div>
                                <span class="stat-value">{{ p.hp }}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">ATK</span>
                                <div class="stat-bar-bg">
                                    <div class="stat-bar-fill" style="width: {% widthratio p.attack 255 100 %}%; background: #ffa502;"></div>
                                </div>
                                <span class="stat-value">{{ p.attack }}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">DEF</span>
                                <div class="stat-bar-bg">
                                    <div class="stat-bar-fill" style="width: {% widthratio p.defense 255 100 %}%; background: #ffd54f;"></div>
                                </div>
                                <span class="stat-value">{{ p.defense }}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">SPD</span>
                                <div class="stat-bar-bg">
                                    <div class="stat-bar-fill" style="width: {% widthratio p.speed 255 100 %}%; background: #4fc3f7;"></div>
                                </div>
                                <span class="stat-value">{{ p.speed }}</span>
                            </div>
                        </div>
                        <div class="total-power">⚡ Power Total: {{ p.total_power }}</div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="empty-state">
                <p>🎮 Tu equipo está vacío. ¡Captura tu primer Pokémon!</p>
            </div>
        {% endif %}

        <!-- ===== PC BOX (RESERVA) ===== -->
        <div class="pc-box-section">
            <h2 class="section-title">📦 Reserva — PC Box ({{ pc_box|length }})</h2>

            {% if pc_box %}
                <div class="pokemon-grid">
                    {% for p in pc_box %}
                        <div class="pokemon-card">
                            <img src="{{ p.imagen_url }}" alt="{{ p.nombre }}">
                            <h3>{{ p.nombre|capfirst }}</h3>
                            <span class="pokemon-id">#{{ p.ext_id }}</span>
                            <div>
                                <span class="pokemon-type">{{ p.tipo }}</span>
                            </div>
                            <div class="stats-container">
                                <div class="stat-row">
                                    <span class="stat-label">HP</span>
                                    <div class="stat-bar-bg">
                                        <div class="stat-bar-fill" style="width: {% widthratio p.hp 255 100 %}%; background: #ff6b6b;"></div>
                                    </div>
                                    <span class="stat-value">{{ p.hp }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">ATK</span>
                                    <div class="stat-bar-bg">
                                        <div class="stat-bar-fill" style="width: {% widthratio p.attack 255 100 %}%; background: #ffa502;"></div>
                                    </div>
                                    <span class="stat-value">{{ p.attack }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">DEF</span>
                                    <div class="stat-bar-bg">
                                        <div class="stat-bar-fill" style="width: {% widthratio p.defense 255 100 %}%; background: #ffd54f;"></div>
                                    </div>
                                    <span class="stat-value">{{ p.defense }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">SPD</span>
                                    <div class="stat-bar-bg">
                                        <div class="stat-bar-fill" style="width: {% widthratio p.speed 255 100 %}%; background: #4fc3f7;"></div>
                                    </div>
                                    <span class="stat-value">{{ p.speed }}</span>
                                </div>
                            </div>
                            <div class="total-power">⚡ Power Total: {{ p.total_power }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty-state">
                    <p>📭 No hay Pokémon en reserva todavía.</p>
                </div>
            {% endif %}
        </div>

    </div>
</body>
</html>
```

> **¿Por qué `{% widthratio p.hp 255 100 %}`?**  
> El stat máximo posible en la PokeAPI es 255. `widthratio` calcula el porcentaje proporcional: un Pokémon con 127 de HP tendría la barra al ~50%. Es un tag nativo de Django que evita hacer cálculos en JavaScript.

---

---

# PASO 7 — Verificación del flujo completo

---

## Levantar el servidor

```bash
# Asegúrate de tener las migraciones aplicadas
python manage.py migrate

# Levantar el servidor de desarrollo
python manage.py runserver
```

Abre tu navegador en `http://127.0.0.1:8000/` y deberías ver la interfaz vacía, lista para capturar.

---

## Lista de verificación paso a paso

Sigue estos pasos en orden para verificar que todo funciona:

### ✅ Verificación 1 — Captura básica

1. Selecciona "Fire" en el desplegable.
2. Presiona "Capturar Pokémon Random".
3. **Resultado esperado**: Aparece un Pokémon de tipo fuego en la sección Party con su imagen, nombre, stats y power total.
4. **¿Qué validamos?** Que la conexión con PokeAPI funciona, que el Pokémon se guarda en BD y que el template lo renderiza correctamente.

### ✅ Verificación 2 — Límite de 6

1. Captura 7 Pokémon (cualquier tipo).
2. **Resultado esperado**: Los primeros 6 aparecen en Party, el 7° aparece en PC Box.
3. **¿Qué validamos?** Que la lógica de `cantidad_en_party < 6` funciona.

### ✅ Verificación 3 — Persistencia

1. Cierra el navegador completamente.
2. Abre de nuevo `http://127.0.0.1:8000/`.
3. **Resultado esperado**: Todos tus Pokémon siguen ahí.
4. **¿Qué validamos?** Que la base de datos persiste los datos correctamente.

### ✅ Verificación 4 — Ordenamiento por stat

1. Presiona "⚔️ Ataque".
2. **Resultado esperado**: Los Pokémon de la Party se reordenan mostrando primero el de mayor ataque.
3. Presiona "💨 Velocidad".
4. **Resultado esperado**: Ahora se muestran ordenados por velocidad descendente.
5. **¿Qué validamos?** Que el parámetro GET `?ordenar=attack` llega a la vista y se aplica al queryset.

### ✅ Verificación 5 — Optimización máxima

1. Asegúrate de tener más de 6 Pokémon capturados (algunos en PC Box).
2. Presiona "⚡ Mejor Equipo Posible".
3. **Resultado esperado**: Los 6 Pokémon con mayor `totalPower` (suma de todos los stats) están ahora en Party. El resto baja a PC Box.
4. **¿Qué validamos?** Que la fórmula `totalPower = hp + attack + defense + sp_attack + sp_defense + speed` se aplica correctamente y que el intercambio entre Party y PC Box se persiste en la BD.

### ✅ Verificación 6 — Responsividad

1. Abre las DevTools del navegador (F12).
2. Activa el modo responsive (ícono de celular/tablet).
3. Prueba con anchos de 360px (celular), 768px (tablet) y 1920px (desktop).
4. **Resultado esperado**: Las cards se reorganizan automáticamente en 1, 2 o más columnas.
5. **¿Qué validamos?** Que `grid-template-columns: repeat(auto-fill, minmax(260px, 1fr))` hace su trabajo sin media queries.

---

---

# 📁 Estructura final del proyecto

---

```
pokeparty/
├── pokeparty/             # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py            # URL raíz → include('core.urls')
│   └── wsgi.py
├── core/                  # Nuestra aplicación
│   ├── templates/
│   │   └── core/
│   │       └── index.html # Template con todo el frontend
│   ├── models.py          # Modelo Pokemon
│   ├── views.py           # Vistas (index, capturar, optimizar)
│   ├── services.py        # Lógica de conexión con PokeAPI
│   └── urls.py            # URLs de la app
├── db.sqlite3             # Base de datos (se genera automáticamente)
├── manage.py
└── requirements.txt       # django, requests
```

---

---

# 🧠 Conceptos clave que aplicamos

---

| Concepto | ¿Dónde lo usamos? | ¿Por qué importa? |
|---|---|---|
| **Modelos Django** | `models.py` — clase `Pokemon` | Define la estructura de datos y la genera automáticamente en la BD |
| **@property** | `total_power` en el modelo | Evita datos redundantes calculando valores en tiempo real |
| **Consumo de API** | `services.py` — `requests.get()` | Habilita la comunicación servidor-a-servidor con servicios externos |
| **POST-Redirect-GET** | Vista `capturar` → `redirect('index')` | Previene re-envío accidental de formularios al refrescar |
| **update_or_create** | Vista `capturar` | Evita duplicados sin necesidad de verificar manualmente |
| **Bulk update** | Vista `optimizar_equipo` | Actualiza múltiples registros con una sola consulta SQL |
| **CSS Grid auto-fill** | Template — `.pokemon-grid` | Responsividad automática sin media queries |
| **widthratio** | Template — barras de stats | Cálculos proporcionales directamente en el template |

---

> _"Django no es solo un framework, es una forma de pensar. Cada pieza tiene su lugar: los datos en el modelo, la lógica en la vista, la presentación en el template. Cuando respetas esta separación, tu código escala y se mantiene limpio."_

> 📊 **Dato real**: Según la encuesta de Stack Overflow 2025, Django se mantiene entre los 5 frameworks web más utilizados a nivel mundial, con especial presencia en el sector fintech y gubernamental de América Latina.
>
> _Fuente: Stack Overflow, "2025 Developer Survey — Web Frameworks"_
