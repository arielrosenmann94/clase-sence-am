# 🦖 Desafío: Jurassic SQL - Sobrevive al Parque

¡Bienvenido a su primer día de trabajo, Arquitecto de Datos! 🦕

## 📖 La Historia

Eres el nuevo encargado de la base de datos de **"Jurassic SQL"**, un moderno parque de diversiones con dinosaurios reales que, lamentablemente, tiene un pésimo historial de seguridad.

El antiguo informático fue devorado por un T-Rex porque la base de datos del sistema de jaulas falló. Antes del trágico accidente, solo alcanzó a dejar el **Modelo conceptual (Entidad-Relación)** dibujado a mano en una pizarra. El objetivo es transformar ese diseño conceptual en código SQL real para que el parque pueda abrir mañana y el sistema funcione correctamente.

Si el sistema falla... los velociraptors están hambrientos y saben abrir puertas. 🚪🦖

---

## 🗺️ El Diagrama en la Pizarra (Modelo Conceptual)

Aquí tienes el diagrama original que te dejaron, tal como se dibujó en la clase teórica sobre modelos de Entidad-Relación (Nivel Lógico).

```text
       ┌──────────┐                                  ┌──────────┐
       │ Especie  │ 1 ─────────────────────────── N │ Recinto  │
       └──────────┘                                  └──────────┘
             │ 1                                           │ 1
             │                                             │
             │ N                                           │ N
       ┌──────────┐                                  ┌──────────┐
       │Dinosaurio│ M ─────────────────────────── N │ Empleado │
       └──────────┘            "Cuidado"             └──────────┘
             │ 1                                           │ 1
             │                                             │
             │ N                                           │ N
       ┌──────────┐                                  ┌──────────┐
       │Incidente │                                  │ Vehículo │
       └──────────┘                                  └──────────┘
```

> ⚠️ **Nota del anterior informático:** "¡Cuidado con la tabla de Cuidado! Los dinosaurios se comen a la gente si no respetas las reglas..."

---

## 📋 Las Reglas del Negocio (Mapeo a la realidad)

1. **Especies**: Solo necesitamos saber su `id`, su `nombre_cientifico` (ej: _Tyrannosaurus rex_), y un booleano `es_carnivoro` (Sí/No).
2. **Recintos**: Tienen un `id`, su `nombre` (ej: "Jaula Norte"), y si tienen un `voltaje_reja` máximo activo o no.
3. **Dinosaurios**: Tienen un `id`, un `nombre_cariñoso` (ej: "Rexy"), el `peso_kg` estimado, y la `fecha_nacimiento`.
   - **Relaciones**: Un dinosaurio pertenece indudablemente a **una sola Especie**, y vive encerrado en **un solo Recinto**.
4. **Incidentes**: A veces los dinosaurios se escapan o atacan. Necesitamos su `id`, `fecha`, una `descripcion` de lo que pasó, y un `nivel_gravedad` (Bajo, Medio, Catástrofe).
   - **Relación**: Un incidente siempre es culpa de **un solo Dinosaurio**. (Aunque un dinosaurio inquieto causa incontables incidentes).
5. **Empleados**: El valiente personal del parque. Tienen `id`, `nombre_completo`, y un número de `nivel_acceso` (del 1 al 5).
6. **Vehículos**: Jeeps para revisar el parque y huir rápido. Tienen una `patente` alfanumérica (esta será la Primary Key) y un texto para `modelo`.
   - **Relación**: Para mantener el orden, cada vehículo está asignado como responsabilidad a **un solo Empleado**. ¡Un empleado veterano puede ser el responsable de múltiples vehículos para su equipo!
7. **La Relación CUIDADO**: Y aquí viene la política estricta. Para que los dinosaurios no se apeguen a un solo humano (y se lo coman el día que falte), la política de seguridad dicta que: **Un Empleado siempre cuida a MUCHOS Dinosaurios**, y **un Dinosaurio siempre debe ser cuidado por MUCHOS Empleados distintos**.

---

## 🎯 Tu Misión (El Ejercicio)

Abra el editor de SQL y escriba un _Script_ completo con las sentencias `CREATE TABLE` correspondientes para transformar este modelo conceptual en un **modelo relacional** funcional.

**Lista de verificación:**

- [ ] Crear todas las tablas, asignando tipos de datos lógicos (como `INT`, `VARCHAR`, `DATE`, `BOOLEAN`).
- [ ] Cada tabla debe tener su respectiva clave primaria (`PRIMARY KEY`).
- [ ] Todas las entidades deben estar correctamente vinculadas con claves foráneas (`FOREIGN KEY`) donde corresponda, para que nada quede "suelto".

### 🚫 LA REGLA DE ORO (Trampa Conceptual)

Observe la relación transversal entre **Empleado** y **Dinosaurio**. El diagrama indica en la pizarra $M:N$.

_¿Es posible escribir una relación `Muchos a Muchos` directamente colocando una clave foránea dentro de la tabla Empleado o dentro de la tabla Dinosaurio? ¿O acaso eso generaría un problema que requiere aplicar una "regla de transformación" especial, tal como se estudió en clase?_

¡Construya todo lo que sea necesario para evitar que Jurassic SQL acabe en bancarrota!
