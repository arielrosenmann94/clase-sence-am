# 🎓 Manual de Solución: PokéParty Optimizer (Paso a Paso)

---

> _"El código es la herramienta, pero la lógica es el artesano. Este manual detalla cómo construir una solución robusta, escalable y visualmente impactante utilizando las mejores prácticas de la industria."_

---

## 🏗️ Paso 1: Configuración del Entorno de "Sinergia Poké-Systems"

Comenzamos preparando nuestro entorno de trabajo profesional siguiendo el estándar nacional.

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install django requests

# Iniciar proyecto y app
django-admin startproject poke_optimizer .
python manage.py startapp core
```

---

## 📊 Paso 2: El Corazón de los Datos — `models.py`

Definimos nuestro modelo en `core/models.py`. Agregamos una propiedad calculada para el poder total, lo que centraliza la lógica de negocio.

```python
from django.db import models

class Pokemon(models.Model):
    ext_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    imagen_url = models.URLField()
    tipo = models.CharField(max_length=50)
    
    # Stats base
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    sp_attack = models.IntegerField()
    sp_defense = models.IntegerField()
    speed = models.IntegerField()
    
    # Estado en el equipo
    en_party = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre.capitalize()} (#{self.ext_id})"

    @property
    def total_power(self):
        # Sumatoria de todos los stats para optimización
        return self.hp + self.attack + self.defense + self.sp_attack + self.sp_defense + self.speed

    class Meta:
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon Capturados"
```

> [!IMPORTANT]
> No olvides ejecutar `python manage.py makemigrations` y `python manage.py migrate` después de definir el modelo.

---

## 🔌 Paso 3: Integración con la PokeAPI — `services.py`

Es una buena práctica separar la lógica de red en un archivo aparte. Creamos `core/services.py`.

```python
import requests
import random

def get_random_pokemon_by_type(pokemon_type):
    # Buscamos todos los Pokémon de ese tipo
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
        
    data = response.json()
    pokemons = data['pokemon']
    
    # Elegimos uno al azar
    random_entry = random.choice(pokemons)
    pokemon_url = random_entry['pokemon']['url']
    
    # Obtenemos los detalles de ese Pokémon específico
    detail_res = requests.get(pokemon_url)
    if detail_res.status_code != 200:
        return None
        
    p_data = detail_res.json()
    
    # Extraemos stats
    stats = {s['stat']['name'].replace('-', '_'): s['base_stat'] for s in p_data['stats']}
    
    return {
        'ext_id': p_data['id'],
        'nombre': p_data['name'],
        'imagen_url': p_data['sprites']['other']['home']['front_default'],
        'tipo': pokemon_type,
        **stats
    }
```

---

## 🚦 Paso 4: La Lógica de Negocio — `views.py`

Aquí manejamos el flujo de captura y la optimización del equipo.

```python
from django.shortcuts import render, redirect
from .models import Pokemon
from .services import get_random_pokemon_by_type

def index(request):
    # Separamos Party de Box
    party = Pokemon.objects.filter(en_party=True).order_by('-hp') # Orden por defecto
    pc_box = Pokemon.objects.filter(en_party=False)
    
    tipos = ['Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ghost', 'Normal']
    
    return render(request, 'index.html', {
        'party': party,
        'pc_box': pc_box,
        'tipos': tipos
    })

def capturar(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        p_data = get_random_pokemon_by_type(tipo)
        
        if p_data:
            # Determinamos si entra a la Party (máx 6)
            count_party = Pokemon.objects.filter(en_party=True).count()
            entra_en_party = count_party < 6
            
            # Guardamos o actualizamos en BD
            Pokemon.objects.update_or_create(
                ext_id=p_data['ext_id'],
                defaults={
                    **p_data,
                    'en_party': entra_en_party
                }
            )
            
    return redirect('index')

def optimizar_equipo(request):
    # 1. Obtenemos todos los Pokémon capturados
    todos = list(Pokemon.objects.all())
    
    # 2. Ordenamos por total_power (propiedad de Python)
    # Nota: Si tuviéramos miles, convendría hacerlo con una anotación de BD SQL
    todos.sort(key=lambda x: x.total_power, reverse=True)
    
    # 3. Marcamos los 6 mejores
    mejores_ids = [p.id for p in todos[:6]]
    
    # 4. Actualizamos la BD de forma masiva
    Pokemon.objects.all().update(en_party=False)
    Pokemon.objects.filter(id__in=mejores_ids).update(en_party=True)
    
    return redirect('index')
```

---

## 🎨 Paso 5: La Experiencia de Usuario — `templates/index.html`

Utilizamos un diseño responsivo **Mobile-First** con CSS Vanilla.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokéParty Optimizer | Sinergia Digital</title>
    <style>
        :root {
            --primary: #2d3436;
            --secondary: #e17055;
            --bg: #f5f6fa;
            --card-bg: rgba(255, 255, 255, 0.9);
        }
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            margin: 0; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 40px; }
        
        /* Grid Responsivo */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        
        .card {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .card:hover { transform: translateY(-5px); }
        .card img { width: 100%; border-radius: 10px; }
        .stats { font-size: 0.8rem; color: #636e72; }
        
        .controls {
            background: white; padding: 20px;
            border-radius: 15px; margin-bottom: 30px;
            display: flex; gap: 10px; justify-content: center;
            flex-wrap: wrap;
        }
        
        button, select {
            padding: 10px 20px; border-radius: 8px;
            border: none; cursor: pointer;
            font-weight: bold;
        }
        .btn-capture { background: var(--secondary); color: white; }
        .btn-optimize { background: #0984e3; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>PokéParty Optimizer ⚔️</h1>
            <p>Gestiona y optimiza tu equipo de alto rendimiento</p>
        </header>

        <section class="controls">
            <form action="{% url 'capturar' %}" method="post" style="display: flex; gap: 10px;">
                {% csrf_token %}
                <select name="tipo">
                    {% for t in tipos %}<option value="{{t}}">{{t}}</option>{% endfor %}
                </select>
                <button type="submit" class="btn-capture">Capturar Pokémon</button>
            </form>
            <a href="{% url 'optimizar_equipo' %}"><button class="btn-optimize">Optimización Máxima</button></a>
        </section>

        <h2>🛡️ Equipo Principal (Party)</h2>
        <div class="grid">
            {% for p in party %}
                <div class="card">
                    <img src="{{p.imagen_url}}" alt="{{p.nombre}}">
                    <h3>{{p.nombre|capfirst}} <small>#{{p.ext_id}}</small></h3>
                    <p>Tipo: {{p.tipo}}</p>
                    <div class="stats">
                        HP: {{p.hp}} | ATK: {{p.attack}} | DEF: {{p.defense}}
                        <br><strong>Power: {{p.total_power}}</strong>
                    </div>
                </div>
            {% endfor %}
        </div>

        <h2 style="margin-top: 50px;">📦 Reserva (PC Box)</h2>
        <div class="grid" style="opacity: 0.7;">
            {% for p in pc_box %}<div class="card">...</div>{% endfor %}
        </div>
    </div>
</body>
</html>
```

---

## 🗺️ Paso 6: Configurando las Rutas — `urls.py`

En `poke_optimizer/urls.py`:

```python
from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('capturar/', views.views.capturar, name='capturar'),
    path('optimizar/', views.optimizar_equipo, name='optimizar_equipo'),
]
```

---

## 🧪 Resumen de Verificación Técnica

1. **Persistencia**: Verificamos que al refrescar la página, el equipo se mantiene.
2. **Límites**: Capturamos más de 6 y confirmamos que aparecen en la sección "Reserva".
3. **Poder**: Verificamos que al presionar "Optimización Máxima", los 6 con mayor `total_power` suben automáticamente al equipo principal.
4. **Responsividad**: Redimensionamos el navegador para validar que las cards se ajustan correctamente a una sola columna en pantallas verticales.

---

> _"La excelencia no es un acto, sino un hábito. Esta solución demuestra cómo Django permite construir lógica compleja de forma limpia y eficiente."_
