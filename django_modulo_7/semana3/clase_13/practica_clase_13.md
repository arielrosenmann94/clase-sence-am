# ⚔️ Challenge Técnico: PokéParty Optimizer

## 🎯 Objetivo

Construir una aplicación web que permita armar y optimizar una party Pokémon a partir de tipos y stats reales obtenidos desde la PokeAPI. La app debe permitir ordenar, comparar y optimizar equipos como si fueran productos buscando la mejor combinación posible.

---

## 🧱 Stack

- **Backend & Frontend**: Django (Templates + Vistas + ORM)
- **ORM / DB**: Django ORM + SQLite (o PostgreSQL si prefieres)
- **API pública**: PokeAPI ([https://pokeapi.co/](https://pokeapi.co/))
- **Puedes usar cualquier framework de frontend o adicional que quieras** (Bootstrap, Bulma, CSS puro, etc.)

---

## 🧩 Descripción General

1. El usuario selecciona un tipo de Pokémon (Agua, Fuego, Planta, etc).
2. La app obtiene un Pokémon aleatorio de ese tipo desde la API.
3. Ese Pokémon se agrega automáticamente a la Party (equipo principal).
4. La Party puede tener máximo 6 Pokémon. Si se agrega más de 6, los excedentes se envían automáticamente a la PC Box (reserva).
5. Cada Pokémon tiene stats (HP, Attack, Defense, Special Attack, etc.) obtenidos desde la PokeAPI.
6. El usuario puede ordenar la Party por cada stat individual o presionar 'Mejor equipo posible' que combina todos los stats para elegir los 6 Pokémon más poderosos.

---

## 🧮 Lógica de Optimización

Cada Pokémon tiene stats numéricos obtenidos desde la PokeAPI. Debe ser posible ordenar por un stat individual (attack, defense, etc.) y calcular un puntaje total combinado, por ejemplo:

```
totalPower = attack + defense + specialAttack + speed + hp
```

Cada cambio o captura debe actualizar la base de datos para persistir los datos. El botón 'Mejor equipo posible' debe reordenar la Party y PC Box para mostrar los 6 con mayor totalPower.

---

## 🎨 Frontend

- Selector de tipo de Pokémon
- Botón "Capturar Pokémon random"
- Sección Party (máximo 6): Cards con Pokémon ID, nombre, imagen, tipo y stats.
- Sección PC Box (Pokémon en reserva)
- Botones de acción: Ordenar por HP, Ordenar por Ataque, Ordenar por Defensa, Ordenar por Velocidad, Mejor equipo posible (sumatoria de todos los stats).

---

## 🧪 Ejemplo de Flujo Visual

1. Usuario elige "Fuego" → obtiene "Charizard" 🔥 → entra a la Party.
2. Elige "Eléctrico" → obtiene "Pikachu" ⚡ → entra a la Party.
3. Repite hasta tener más de 6 Pokémon → los extra van a la PC Box.
4. Hace clic en "Mejor equipo posible" → el sistema combina Party + PC Box y elige los 6 con mayor poder total.

---

## 🚀 Forma de entrega

Subir el proyecto a GitHub público.

### 📘 Instrucciones obligatorias

- Instrucciones de instalación y ejecución (`python -m venv venv`, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver`).
- Cómo conectar la base de datos: si usan SQLite pueden dejar la configuración por defecto; si prefieren PostgreSQL, incluir las instrucciones o un `docker-compose.yml` para levantar la base de datos localmente (Ejemplo de variables de entorno `.env.example`).
- Cómo ejecutar la app (`python manage.py runserver`).

---

## 🧭 Evaluación

- Integración correcta con PokeAPI
- Lógica de aleatoriedad, ordenamiento y optimización
- Uso de Django ORM y persistencia en BD
- Interfaz clara, ordenada y visualmente atractiva
- Cumplimiento del flujo completo
- Se evaluará principalmente la ejecución completa de lo solicitado y el cumplimiento funcional. Suma valor un buen diseño UX/UI, claridad visual y una propuesta creativa en la presentación.
