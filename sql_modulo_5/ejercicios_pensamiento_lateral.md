# 🧠 Desafíos de Pensamiento Lateral en SQL

¡Bienvenidos a los desafíos lógicos! Aquí no gana quien escribe el SQL más largo ni quien memoriza las funciones más raras. Aquí gana quien entiende los conjuntos de datos y encuentra **soluciones creativas a problemas poco comunes**.

Cada ejercicio tiene un **escenario**, un **script y datos de prueba** para crear las tablas en el motor SQL, y una **restricción** (una regla de oro que no puede romperse).

Prepárese para pensar "fuera de la caja" 📦.

---

## ✈️ Desafío 1: El misterio del vuelo sobrevendido

### 📖 La historia

Tienes una tabla con 10 personas confirmadas para un vuelo. El avión es pequeño y por problemas de sobrecarga, **solo pueden subir 7 pasajeros**.
Lamentablemente, el sistema de check-in falló y nadie sabe quién llegó primero. La aerolínea decide algo drástico: van a dejar abajo a los 3 pasajeros que tengan el **equipaje más pesado**.

### 🛠️ Preparación de datos (Copia y pega en tu motor SQL)

```sql
CREATE TABLE lateral_vuelo_pasajeros (
    id_pasajero SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    peso_equipaje_kg NUMERIC(5,2)
);

INSERT INTO lateral_vuelo_pasajeros (nombre, peso_equipaje_kg) VALUES
('Ana', 12.5),
('Bruno', 25.0), -- Muy pesado
('Carlos', 8.0),
('Diana', 22.5), -- Muy pesado
('Elena', 15.0),
('Fernando', 30.0), -- Muy pesado
('Gabriela', 10.5),
('Hugo', 18.0),
('Inés', 5.0),
('Javier', 14.0);
```

### 🎯 El objetivo

Escribe una consulta SQL que devuelva a los **7 pasajeros que SÍ viajarán** (los 7 con menor peso de equipaje).

### 🚫 LA REGLA DE ORO (Restricción)

**No se puede usar `ORDER BY`, `LIMIT`, `TOP` ni `FETCH FIRST`.**
_(Técnicamente `ORDER BY peso_equipaje_kg ASC LIMIT 7` lo resuelve en 2 segundos, pero está prohibido para este ejercicio)._

> **💡 Pista analógica:** Si no es posible ordenarlos de menor a mayor para cortar la lista... ¿cómo se sabría si el equipaje de una persona en particular está entre los 3 más pesados de todos? Intente comparar la tabla consigo misma.

---

## 🌙 Desafío 2: El guardián del turno nocturno

### 📖 La historia

Tienes los registros de las tarjetas magnéticas de entrada y salida de un edificio corporativo del día viernes. El guardia de seguridad juró que el edificio quedó vacío a las 22:00 hrs.
Sin embargo, el lunes en la mañana encontraron evidencia de que **alguien se quedó encerrado adentro todo el fin de semana**.

### 🛠️ Preparación de datos (Copia y pega en tu motor SQL)

```sql
CREATE TABLE lateral_registros_edificio (
    id_registro SERIAL PRIMARY KEY,
    empleado VARCHAR(50),
    hora_evento TIME,
    tipo_evento VARCHAR(10) CHECK (tipo_evento IN ('ENTRADA', 'SALIDA'))
);

INSERT INTO lateral_registros_edificio (empleado, hora_evento, tipo_evento) VALUES
('Lorena', '08:00', 'ENTRADA'),
('Mateo', '08:15', 'ENTRADA'),
('Lorena', '13:00', 'SALIDA'),  -- Lorena sale a almorzar
('Lorena', '14:00', 'ENTRADA'), -- Lorena vuelve
('Mateo', '18:00', 'SALIDA'),   -- Mateo se va a casa
('Lorena', '19:30', 'SALIDA'),  -- Lorena termina su turno
('Pedro', '20:00', 'ENTRADA'),  -- Pedro entra tarde por un problema
('Pedro', '21:00', 'SALIDA'),   -- Pedro sale a fumar
('Pedro', '21:15', 'ENTRADA');  -- Pedro vuelve a entrar... y no sale.
```

### 🎯 El objetivo

Escribe una consulta SQL que te devuelva **exclusivamente el nombre** de la persona que se quedó encerrada en el edificio el fin de semana.
_Ojo: Como ves en los datos, una persona puede entrar y salir varias veces en el mismo día._

### 🚫 LA REGLA DE ORO (Restricción)

No se cuenta con un campo de "estado actual", solo el registro de eventos. Se debe resolver usando agrupaciones lógicas, **no es posible buscar manualmente en los datos** (imagine que la tabla tiene 1 millón de registros).

> **💡 Pista analógica:** Si alguien entró al edificio y nunca salió... ¿qué relación matemática simple existe entre la cantidad de veces que realizó 'ENTRADA' y la cantidad de veces que realizó 'SALIDA'?

---

## 🧨 Desafío 3: La venganza del becario

### 📖 La historia

Un becario muy confundido entró a la base de datos de RRHH y ejecutó un comando destructivo:
`UPDATE lateral_rrhh_hoy SET sueldo = 0 WHERE id_empleado = 103;`

Afortunadamente, el administrador de la base de datos tenía un respaldo intocable creado la noche anterior.

### 🛠️ Preparación de datos (Copia y pega en tu motor SQL)

```sql
-- La tabla de ayer (EL RESPALDO INTACTO)
CREATE TABLE lateral_rrhh_ayer (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento VARCHAR(50),
    sueldo NUMERIC(10,2)
);

INSERT INTO lateral_rrhh_ayer VALUES
(101, 'Alicia', 'Ventas', 1500.00),
(102, 'Roberto', 'IT', 2000.00),
(103, 'Carmen', 'Finanzas', 1800.00),
(104, 'David', 'Ventas', 1550.00);

-- La tabla de hoy (ARRUINADA POR EL BECARIO)
CREATE TABLE lateral_rrhh_hoy (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento VARCHAR(50),
    sueldo NUMERIC(10,2)
);

-- Nota cómo el sueldo de Carmen (103) está en 0
INSERT INTO lateral_rrhh_hoy VALUES
(101, 'Alicia', 'Ventas', 1500.00),
(102, 'Roberto', 'IT', 2000.00),
(103, 'Carmen', 'Finanzas', 0.00),
(104, 'David', 'Ventas', 1550.00);
```

### 🎯 El objetivo

Como analista de datos, **no sabes qué registro fue modificado** (imagina que son 10,000 empleados y no sabes que fue el 103 ni que fue Carmen).
Escribe una consulta que compare ambas tablas y te devuelva **exactamente el registro original de ayer** que difiere de la tabla de hoy, para así saber qué dato restaurar.

### 🚫 LA REGLA DE ORO (Restricción)

**No se puede usar la cláusula `WHERE` ni un `JOIN` DE NINGÚN TIPO.**

> **💡 Pista analógica:** Si se tienen dos bolsas, una blanca y una negra, cada una con 4 pelotas, y se sabe que 3 de ellas son idénticas en ambas bolsas pero 1 es diferente. ¿Qué operación de la teoría de conjuntos permite extraer las que son exactamente iguales y quedarse solo con la diferencia?
