# 🧪 Práctica Clase 6 — Challenge Fullstack

# 🔴🟢🔵 Sistema de Agendamiento: Laboratorio del Profesor Oak

---

## 💼 Escenario

> **Contexto:** Estás postulando a un puesto de **Desarrollador Fullstack Junior**. Como parte del proceso de selección, te piden completar el siguiente challenge técnico en **1 hora y 30 minutos**.
>
> El equipo de desarrollo evaluará: la calidad de tus modelos, el correcto uso de migraciones, que el flujo funcione de punta a punta, y la creatividad de tu solución visual.
>
> **No hay diseño entregado.** Tú decides el frontend. Se espera una visual acorde a la temática con animaciones que hagan la experiencia memorable.

---

## 📋 Brief del Proyecto

El **Profesor Oak** necesita un sistema web para que los nuevos entrenadores puedan **agendar una cita** en su laboratorio y **reservar su criatura inicial**.

Las criaturas disponibles son:

| Criatura          | Tipo   |
| :---------------- | :----- |
| 🔥 **Charmander** | Fuego  |
| 🌿 **Bulbasaur**  | Planta |
| 💧 **Squirtle**   | Agua   |

El Profesor Oak tiene **horarios disponibles durante la semana** (por ejemplo: Lunes 10:00, Lunes 14:00, Martes 09:00, etc.). Cada horario tiene un **cupo limitado** de entrenadores que puede atender.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│              DJANGO ADMIN               │
│  (Solo el Profesor Oak accede aquí)     │
│                                         │
│  → Administrar criaturas disponibles    │
│  → Configurar horarios de la semana     │
│  → Ver todas las reservas agendadas     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│            FRONTEND TEMÁTICO            │
│   (Los entrenadores acceden aquí)       │
│                                         │
│  → Registrarse con usuario y contraseña │
│  → Elegir su criatura inicial           │
│  → Elegir un horario disponible         │
│  → Confirmar la reserva                 │
│  → Ver su reserva confirmada            │
└─────────────────────────────────────────┘
```

---

---

# 🎫 Tickets de Trabajo

---

## TICKET 1 — Modelos y Base de Datos

**Prioridad:** Alta

Crea los modelos necesarios para el sistema. Piensa en qué entidades necesitas y cómo se relacionan.

**Requisitos de negocio:**

- Cada **criatura** tiene: nombre, tipo (fuego/planta/agua), descripción y una imagen o emoji representativo.
- Los **horarios disponibles** son bloques de tiempo configurados por el Profesor Oak. Cada horario tiene: día de la semana, hora de inicio, hora de fin, y un cupo máximo de entrenadores que puede atender en ese bloque.
- Cada **reserva** conecta a un entrenador (usuario registrado) con una criatura y un horario. La reserva debe registrar la fecha en que se creó.
- Un entrenador solo puede tener **UNA reserva**. No puede reservar dos criaturas ni dos horarios.
- Un horario no puede tener más reservas que su cupo máximo.

**Criterio de aceptación:**

- Los modelos están definidos correctamente con relaciones coherentes.
- Cada campo tiene el tipo de dato y restricciones apropiadas.
- `makemigrations` y `migrate` se ejecutan sin errores.
- `showmigrations` muestra todo en `[X]`.

---

## TICKET 2 — Configuración del Admin

**Prioridad:** Alta
**Depende de:** Ticket 1

Registra los modelos en el Admin de Django para que el Profesor Oak pueda gestionar todo desde ahí.

**Requisitos:**

- Debe poder crear, editar y eliminar criaturas.
- Debe poder crear y configurar horarios disponibles (día, hora, cupo).
- Debe poder ver todas las reservas con: nombre del entrenador, criatura elegida, horario, y fecha de reserva.
- Las reservas deben mostrarse ordenadas por fecha.

**Criterio de aceptación:**

- Acceder a `/admin/` y gestionar los 3 modelos sin problemas.
- Cargar las 3 criaturas iniciales (Charmander, Bulbasaur, Squirtle).
- Cargar al menos 6 horarios distribuidos en la semana.

---

## TICKET 3 — Registro e Inicio de Sesión

**Prioridad:** Alta
**Depende de:** Ticket 2

Los entrenadores deben poder registrarse y entrar al sistema con su usuario y contraseña.

**Requisitos:**

- Página de **registro** con: nombre de usuario y contraseña.
- Página de **login**.
- Al registrarse exitosamente, el entrenador inicia sesión automáticamente y es redirigido al flujo de agendamiento.
- Puedes usar el sistema de autenticación de Django (`django.contrib.auth`).

**Criterio de aceptación:**

- Un usuario nuevo puede registrarse y quedar logueado.
- Un usuario existente puede hacer login.
- Las páginas de registro y login deben tener visual acorde a la temática.

---

## TICKET 4 — Paso 1: Elegir Criatura

**Prioridad:** Alta
**Depende de:** Ticket 3

Una vez logueado, el entrenador ve las criaturas disponibles y elige una.

**Requisitos:**

- Mostrar las 3 criaturas con su nombre, tipo, descripción y una visual representativa.
- Cada criatura debe tener una **animación** o efecto visual que la haga destacar (hover, aparición, brillo, etc.).
- El entrenador hace clic en una criatura para seleccionarla y avanza al paso 2.
- Solo se muestran criaturas que todavía estén disponibles.

**Criterio de aceptación:**

- Las criaturas se muestran con diseño temático y animaciones.
- Al hacer clic se avanza al paso 2 con la criatura seleccionada.

---

## TICKET 5 — Paso 2: Elegir Horario

**Prioridad:** Alta
**Depende de:** Ticket 4

El entrenador ve los horarios disponibles de la semana y elige uno.

**Requisitos:**

- Mostrar los horarios disponibles en formato de calendario semanal, lista, o grilla (tú decides la presentación).
- Cada horario debe mostrar: día, hora, y cuántos cupos quedan.
- **No mostrar** horarios que ya estén llenos (cupo agotado).
- Al seleccionar un horario, se avanza al paso 3 (confirmación).

**Criterio de aceptación:**

- Solo se muestran horarios con cupo disponible.
- Se indica cuántos cupos quedan en cada horario.
- Al seleccionar se avanza a la confirmación.

---

## TICKET 6 — Paso 3: Confirmación y Agendamiento

**Prioridad:** Alta
**Depende de:** Ticket 5

El entrenador ve un resumen de su selección y confirma.

**Requisitos:**

- Mostrar un resumen con:
  - Nombre del entrenador (tomado del usuario logueado).
  - Criatura elegida (con su visual).
  - Horario elegido (día y hora).
- Botón **"🎯 Confirmar Reserva"**.
- Al confirmar:
  - Se crea la reserva en la base de datos.
  - Se descuenta un cupo del horario seleccionado.
  - Se redirige a una página de éxito con un mensaje temático y una animación de celebración.
- Si el entrenador ya tiene una reserva, no puede crear otra. Mostrar un mensaje indicándolo.

**Criterio de aceptación:**

- La reserva se guarda correctamente en la BD.
- El cupo del horario se actualiza.
- No se pueden crear reservas duplicadas.
- La página de éxito tiene una animación o efecto visual de celebración.

---

## TICKET 7 — Vista: Mi Reserva

**Prioridad:** Media
**Depende de:** Ticket 6

El entrenador debe poder ver su reserva agendada en cualquier momento.

**Requisitos:**

- Mostrar los datos de la reserva: criatura, horario, fecha de reserva.
- Visual temática.
- Si el entrenador no tiene reserva, mostrar un mensaje invitándolo a agendar.
- La consulta a la BD debe usar `select_related` para evitar el problema N+1.

**Criterio de aceptación:**

- La vista muestra la reserva correctamente.
- Se usa `select_related` o `prefetch_related`.

---

---

## 🎨 Requisitos de Frontend

El diseño debe ser **acorde a la temática**. Esto implica:

- **Paleta de colores** inspirada en el universo (rojos, verdes, azules, amarillos).
- **Tipografía** que se sienta aventurera o de videojuego (busca en Google Fonts).
- **Animaciones mínimas obligatorias:**
  - Hover en las criaturas (escala, brillo, rebote, o lo que inventes).
  - Transición entre pasos del flujo.
  - Animación de celebración al confirmar la reserva.
- **Responsive:** Debe verse bien en celular y en pantalla grande.
- Puedes usar emojis, CSS puro, o descargar imágenes libres para representar las criaturas.

> 💡 No se evalúa que sea perfecto. Se evalúa que haya **intención de diseño temático** y que el flujo sea usable desde el celular.

---

## 📊 Tabla de Evaluación

| Criterio                  | Peso | Qué se revisa                                                  |
| :------------------------ | :--- | :------------------------------------------------------------- |
| **Modelos y relaciones**  | 15%  | Modelos correctos, relaciones coherentes, `on_delete`          |
| **Migraciones**           | 10%  | Todas aplicadas sin error                                      |
| **Admin funcional**       | 10%  | Los 3 modelos gestionables desde `/admin/`                     |
| **Registro y Login**      | 10%  | Funciona el registro, login y sesión                           |
| **Flujo de agendamiento** | 25%  | Los 3 pasos funcionan de punta a punta                         |
| **Validaciones**          | 10%  | Cupo respetado, no duplicar reservas                           |
| **Frontend temático**     | 15%  | Colores, tipografía, animaciones, responsive                   |
| **Optimización ORM**      | 5%   | Uso de `select_related` / `prefetch_related`                   |

---

## 📦 Entregable

Para completar el challenge, debes entregar:

1. **Repositorio público en GitHub** con todo el código del proyecto. El link debe estar accesible y el repositorio debe tener un `README.md` básico con instrucciones para ejecutar el proyecto.

2. **Video explicativo de máximo 5 minutos** donde muestres:
   - El sistema funcionando (flujo completo: registro → elegir criatura → elegir horario → confirmar reserva).
   - El Admin de Django con los modelos cargados.
   - Una explicación breve de las decisiones técnicas que tomaste (modelos, relaciones, cómo resolviste el frontend).

> 💡 El video no necesita edición profesional. Puede ser una grabación de pantalla con tu voz explicando. Lo que importa es que se vea el software funcionando y que puedas explicar tu código.

---
