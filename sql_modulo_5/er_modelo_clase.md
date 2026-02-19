<!-- =========================================================
Archivo: er_modelo_clase.md
Tema: Modelo Entidad-Relación — Teoría Completa
Partes: Parte 1 (ER base) + Parte 2 (Transformación y Normalización)
========================================================= -->

# 🗺️ El Modelo Entidad-Relación — De la Idea a la Base de Datos

---

---

# 📚 PARTE 1 — El Modelo Conceptual

---

## 🗺️ ¿Qué vamos a aprender hoy?

| Tema                           | Pregunta clave                                         |
| ------------------------------ | ------------------------------------------------------ |
| 🧩 Modelo ER                   | ¿Cómo represento la realidad en un diagrama?           |
| 🔎 Abstracción                 | ¿Cómo simplifico un problema complejo?                 |
| 🔗 Relaciones                  | ¿Cómo se conectan las cosas entre sí?                  |
| 🏷️ Atributos                   | ¿Qué información necesito guardar?                     |
| 💪 Entidades fuertes y débiles | ¿Cuáles son independientes y cuáles dependen de otras? |
| 🔄 Reglas de transformación    | ¿Cómo paso de un diagrama a tablas SQL?                |
| 📐 Normalización               | ¿Cómo evito datos repetidos y problemas?               |

---

---

## 1️⃣ ¿Qué es el Modelo Entidad-Relación?

---

### La analogía: El plano del arquitecto 🏗️

Imagina que quieres construir una casa. **¿Empezarías a poner ladrillos sin un plano?**

No. Primero dibujas un plano que muestra:

- Cuántas habitaciones hay
- Cómo se conectan entre sí
- Qué tamaño tiene cada una
- Dónde van las puertas y ventanas

**El Modelo Entidad-Relación (ER) es el PLANO de tu base de datos.**

Antes de escribir una sola línea de SQL, necesitas **diseñar** qué información vas a guardar y cómo se relaciona.

---

### Definición formal

> El modelo ER es un enfoque para representar de forma **visual y abstracta** la estructura de datos y las relaciones entre entidades de un sistema.

En español simple:

```
Modelo ER = un DIBUJO que muestra
             QUÉ cosas existen en tu sistema
             y CÓMO se conectan entre sí
```

---

### Los 3 componentes del modelo ER

| Componente   | ¿Qué es?                                     | Representación visual |
| ------------ | -------------------------------------------- | --------------------- |
| **Entidad**  | Un objeto o concepto del mundo real          | 📦 Rectángulo         |
| **Atributo** | Una propiedad o característica de la entidad | ⭕ Óvalo / Elipse     |
| **Relación** | Una conexión entre dos o más entidades       | 🔷 Rombo              |

---

### Ejemplo visual: Biblioteca

```
     ┌──────────┐          ┌──────────┐          ┌──────────┐
     │  AUTOR   │──────────│ escribió │──────────│  LIBRO   │
     └──────────┘          └──────────┘          └──────────┘
       │                                            │
       ├── nombre                                   ├── título
       ├── nacionalidad                             ├── ISBN
       └── fecha_nac                                ├── año
                                                    └── editorial
```

- **Entidades**: Autor, Libro (rectángulos)
- **Relación**: "escribió" (rombo)
- **Atributos**: nombre, título, ISBN... (los que cuelgan de cada entidad)

---

---

## 2️⃣ El Proceso de Abstracción

---

### ¿Qué es abstraer?

> Abstraer = **simplificar la realidad** quedándote solo con la información que importa para tu sistema.

---

### La analogía: El mapa 🗺️

Un mapa de Santiago NO muestra cada piedra, cada árbol, cada persona caminando. Muestra solo lo que necesitas: **calles, estaciones de metro, comunas.**

Cuando diseñas una base de datos, haces lo mismo:

```
Un auto Toyota Corolla 2022, patente ABCD-12:
  Color rojo, 45.000 km, motor 1.8L, asientos de tela,
  tiene un rayón en la puerta, huele a pino, suena un
  ruidito raro al frenar, el dueño le puso stickers...

Base de datos de un TALLER MECÁNICO:
  Toyota Corolla → patente, modelo, año, kilometraje
  (el color de los stickers NO importa para el taller)

Base de datos de un SEGURO DE AUTO:
  Toyota Corolla → patente, dueño, valor comercial, siniestros
  (el kilometraje NO importa para el seguro)
```

**Abstraer = quedarte SOLO con lo relevante para tu sistema.** El mismo auto guarda datos distintos según quién lo necesite.

---

### Niveles de abstracción en bases de datos

```
┌─────────────────────────────────────────┐
│         NIVEL CONCEPTUAL                │  ← Modelo ER (diagramas)
│  "¿QUÉ datos necesito?"                │     Lo más abstracto
├─────────────────────────────────────────┤
│         NIVEL LÓGICO                    │  ← Tablas, columnas, tipos
│  "¿CÓMO organizo los datos?"           │     Estructura concreta
├─────────────────────────────────────────┤
│         NIVEL FÍSICO                    │  ← Archivos, índices, disco
│  "¿DÓNDE se guardan los datos?"        │     Lo más técnico
└─────────────────────────────────────────┘
```

Hoy nos movemos entre el nivel **conceptual** (diagramas ER) y el nivel **lógico** (tablas SQL).

---

### Los 4 pilares de una base de datos

| Pilar         | ¿Qué es?                                                        | Ejemplo                                               |
| ------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| **Tablas**    | Estructuras que almacenan datos en filas y columnas             | La tabla `clientes` con nombre, email, teléfono       |
| **Esquemas**  | La definición de la estructura (columnas, tipos, restricciones) | `nombre VARCHAR(80) NOT NULL`                         |
| **Consultas** | Instrucciones SQL para interactuar con los datos                | `SELECT * FROM clientes WHERE activo = true`          |
| **Vistas**    | Consultas guardadas que actúan como "tablas virtuales"          | Una vista que muestra solo clientes activos con deuda |

---

---

## 3️⃣ Entidades y Atributos en Detalle

---

### ¿Qué es una entidad?

Una entidad es **cualquier cosa del mundo real que queremos registrar** en nuestra base de datos.

```
🏢 Sistema de RRHH        →  Empleado, Departamento, Cargo
🏥 Sistema de Clínica      →  Paciente, Doctor, Cita, Diagnóstico
🛒 Sistema de E-commerce   →  Producto, Cliente, Orden, Pago
🏫 Sistema de Universidad  →  Estudiante, Profesor, Curso, Nota
```

**Regla de oro:** Si puedes decir "necesito guardar información sobre **\_**", entonces es una entidad.

---

### ¿Qué es un atributo?

Un atributo es una **propiedad o característica** de una entidad.

| Entidad       | Atributos                                  |
| ------------- | ------------------------------------------ |
| 👤 Estudiante | nombre, email, fecha_nacimiento, dirección |
| 👨‍🏫 Profesor   | nombre, título, especialidad               |
| 📘 Curso      | nombre, código, descripción, créditos      |

**Cada atributo tiene un TIPO DE DATO** (texto, número, fecha, booleano, etc.).

---

### Tipos de atributos

| Tipo             | Descripción                  | Ejemplo                                        |
| ---------------- | ---------------------------- | ---------------------------------------------- |
| **Simple**       | Un solo valor indivisible    | `nombre = 'Juan'`                              |
| **Compuesto**    | Se puede dividir en partes   | `dirección` → calle + número + comuna + ciudad |
| **Derivado**     | Se calcula a partir de otros | `edad` se calcula con `fecha_nacimiento`       |
| **Multivaluado** | Puede tener varios valores   | `teléfonos` → puede tener varios               |

---

### El Identificador Único (Clave Primaria)

Todo registro en una tabla necesita ser **identificable de forma única**. Para eso existe la **clave primaria (PK)**.

```
¿Puedo usar el nombre como identificador?

  María López   ← ¿Cuál María López? Puede haber 50
  María López   ← No sirve como identificador ❌

¿Y el RUT?

  12.345.678-9  ← Único en todo Chile ✅

¿Y un ID autoincremental?

  1, 2, 3, 4... ← Siempre único ✅ (la opción más común)
```

**Regla:** La PK debe ser **única**, **no nula** y **no debe cambiar** en el tiempo.

---

---

## 4️⃣ Tipos de Relaciones

---

### ¿Qué es una relación?

Una relación describe **cómo se conectan dos entidades entre sí**.

Las relaciones se nombran con **verbos** que describen la conexión:

- Un cliente **realiza** pedidos
- Un profesor **enseña** cursos
- Un libro **pertenece a** una categoría

---

### Los 4 tipos de relaciones

---

### 🔗 Uno a Uno (1:1)

> Una entidad A se relaciona con **exactamente una** entidad B, y viceversa.

```
┌──────────┐    1         1    ┌──────────┐
│ PERSONA  │───────────────────│ PASAPORTE│
└──────────┘                   └──────────┘

  Juan Pérez  ←→  Pasaporte ABC123
  Ana Torres  ←→  Pasaporte DEF456
```

**Ejemplos reales:**

- Una persona tiene **un** pasaporte, y ese pasaporte pertenece a **una** persona
- Un país tiene **una** capital, y esa capital pertenece a **un** país
- Un empleado tiene **un** contrato vigente

**¿Cuándo se usa?** Cuando quieres separar información por seguridad o por organización, aunque podrían estar en la misma tabla.

---

### 🔗 Uno a Muchos (1:N)

> Una entidad A se relaciona con **muchas** entidades B, pero cada B pertenece a **una sola** A.

```
┌──────────┐    1         N    ┌──────────┐
│  CLIENTE │───────────────────│  PEDIDO  │
└──────────┘                   └──────────┘

  Juan Pérez  → Pedido #001
  Juan Pérez  → Pedido #002
  Juan Pérez  → Pedido #003
  Ana Torres  → Pedido #004
```

**Ejemplos reales:**

- Un cliente tiene **muchos** pedidos, pero cada pedido pertenece a **un** cliente
- Un departamento tiene **muchos** empleados, pero cada empleado está en **un** departamento
- Una categoría tiene **muchas** películas, pero cada película tiene **una** categoría

**Es la relación más común en bases de datos.**

---

### 🔗 Muchos a Uno (N:1)

> Es lo mismo que 1:N pero visto desde el otro lado.

```
┌──────────┐    N         1    ┌──────────┐
│  PEDIDO  │───────────────────│  CLIENTE │
└──────────┘                   └──────────┘

  "Muchos pedidos pertenecen a un mismo cliente"
```

Es simplemente la perspectiva inversa de 1:N. **Si A→B es 1:N, entonces B→A es N:1.**

---

### 🔗 Muchos a Muchos (N:M)

> Muchas entidades A se relacionan con muchas entidades B.

```
┌──────────┐    N         M    ┌──────────┐
│ESTUDIANTE│───────────────────│  CURSO   │
└──────────┘                   └──────────┘

  Juan  → Matemáticas, Física, Química
  Ana   → Matemáticas, Historia
  Pedro → Física, Química, Historia
```

**Ejemplos reales:**

- Un estudiante cursa **muchas** asignaturas, y cada asignatura tiene **muchos** estudiantes
- Un actor actúa en **muchas** películas, y cada película tiene **muchos** actores
- Un producto pertenece a **muchas** categorías, y cada categoría tiene **muchos** productos

---

### ¿Cómo se implementa N:M en SQL?

**No se puede implementar directamente.** Se necesita una **tabla intermedia** (también llamada tabla pivote o tabla de unión):

```
┌──────────┐         ┌──────────────┐         ┌──────────┐
│ESTUDIANTE│────1:N──│ INSCRIPCIÓN  │──N:1────│  CURSO   │
└──────────┘         └──────────────┘         └──────────┘
                       │
                       ├── id_estudiante (FK)
                       ├── id_curso (FK)
                       └── fecha_inscripcion
```

La tabla `inscripcion` convierte una relación N:M en **dos relaciones 1:N**.

```sql
-- La tabla intermedia:
CREATE TABLE inscripciones (
  id              SERIAL PRIMARY KEY,
  id_estudiante   INT NOT NULL REFERENCES estudiantes(id),
  id_curso        INT NOT NULL REFERENCES cursos(id),
  fecha           TIMESTAMP DEFAULT NOW()
);
```

---

### Resumen visual de relaciones

```
1:1     Persona ──── Pasaporte       (uno tiene uno)
1:N     Cliente ──── Pedidos         (uno tiene muchos)
N:1     Pedidos ──── Cliente         (muchos pertenecen a uno)
N:M     Estudiante ──── Curso        (muchos con muchos → tabla intermedia)
```

---

---

## 5️⃣ Entidades Fuertes y Débiles

---

### La analogía: El inquilino y el edificio 🏢

Un **edificio** existe por sí solo. Tiene dirección, nombre, dueño.

Un **departamento** dentro del edificio... ¿puede existir sin el edificio? **No.** El "Depto 501" no tiene sentido si no sabes DE QUÉ edificio.

- **Edificio** = Entidad fuerte (independiente)
- **Departamento** = Entidad débil (depende del edificio)

---

### Definición

| Tipo                  | Característica                                                                  | Ejemplo                                                |
| --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Entidad fuerte** 💪 | Existe por sí sola. Tiene su propia PK independiente.                           | Cliente, Producto, Empleado                            |
| **Entidad débil** 🤝  | Depende de otra entidad para existir. Su PK incluye la FK de la entidad fuerte. | Detalle de pedido, Copia de libro, Habitación de hotel |

---

### Diferencias clave

| Aspecto                     | Entidad Fuerte         | Entidad Débil                        |
| --------------------------- | ---------------------- | ------------------------------------ |
| **¿Existe sola?**           | ✅ Sí                  | ❌ No, depende de otra               |
| **Clave primaria**          | Propia e independiente | Combinada (su FK + un discriminante) |
| **Si se borra el padre...** | No afecta a nadie      | La entidad débil pierde sentido      |
| **Representación ER**       | Rectángulo simple      | Rectángulo con doble borde           |

---

### Ejemplo: Librería

```
  Entidad FUERTE                    Entidad DÉBIL
┌──────────────┐              ╔══════════════════╗
│    LIBRO     │──── 1:N ─────║  COPIA DE LIBRO  ║
│              │              ║                  ║
│  libro_id PK │              ║  libro_id FK     ║
│  título      │              ║  nro_copia       ║
│  autor       │              ║  estado           ║
│  año         │              ║  ubicacion        ║
└──────────────┘              ╚══════════════════╝

  "Harry Potter" existe como concepto.
  "La copia #3 de Harry Potter" NO existe sin saber de qué libro hablamos.
```

La PK de `copia_libro` sería **(libro_id + nro_copia)** → una clave compuesta que incluye la FK.

---

---

---

# 📚 PARTE 2 — Del Diagrama a la Base de Datos

---

---

## 6️⃣ Modelo Conceptual vs Modelo Relacional

---

### ¿Cuál es la diferencia?

Son **dos formas de ver lo mismo**, pero en distintos niveles de detalle:

| Aspecto         | Modelo Conceptual                     | Modelo Relacional                              |
| --------------- | ------------------------------------- | ---------------------------------------------- |
| **¿Qué es?**    | Diagrama abstracto (ER)               | Tablas concretas en SQL                        |
| **Nivel**       | Alto nivel, sin detalles técnicos     | Bajo nivel, con tipos de datos y restricciones |
| **Público**     | Para TODOS (cliente, jefe, diseñador) | Para TÉCNICOS (desarrolladores, DBAs)          |
| **Muestra**     | Entidades, atributos, relaciones      | Tablas, columnas, PKs, FKs, tipos              |
| **Herramienta** | Dibujo (papel, Lucidchart, Draw.io)   | SQL (CREATE TABLE)                             |

---

### Ejemplo lado a lado

```
MODELO CONCEPTUAL (Diagrama ER):

  ┌──────────┐        ┌──────────┐        ┌──────────┐
  │ USUARIO  │──1:N──│  PEDIDO  │──N:1──│ PRODUCTO │
  └──────────┘        └──────────┘        └──────────┘
    nombre              fecha               nombre
    email               total               precio
                                            stock
```

```sql
-- MODELO RELACIONAL (SQL):

CREATE TABLE usuarios (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80) NOT NULL,
  email   VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE productos (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(100) NOT NULL,
  precio  NUMERIC(10,2) NOT NULL,
  stock   INT NOT NULL DEFAULT 0
);

CREATE TABLE pedidos (
  id          SERIAL PRIMARY KEY,
  id_usuario  INT NOT NULL REFERENCES usuarios(id),
  fecha       TIMESTAMP DEFAULT NOW(),
  total       NUMERIC(10,2) NOT NULL
);
```

**El modelo conceptual dice QUÉ. El modelo relacional dice CÓMO.**

---

---

## 7️⃣ Reglas de Transformación

---

### ¿Qué son?

Son las **recetas** para convertir un diagrama ER en tablas SQL. Es un proceso mecánico: si sigues las reglas, el resultado es correcto.

---

### Regla 1: Entidad → Tabla

> Cada entidad del diagrama se convierte en una tabla.

```
Diagrama ER:          SQL:
┌──────────┐          CREATE TABLE clientes (
│ CLIENTE  │    →       ...
└──────────┘          );
```

---

### Regla 2: Atributo → Columna

> Cada atributo de la entidad se convierte en una columna con su tipo de dato.

```
Diagrama ER:                    SQL:
  nombre (texto)          →     nombre VARCHAR(80) NOT NULL
  email (texto único)     →     email VARCHAR(120) UNIQUE
  fecha_nac (fecha)       →     fecha_nac DATE
  activo (sí/no)          →     activo BOOLEAN DEFAULT TRUE
```

---

### Regla 3: Identificador → Clave Primaria

> El identificador único de cada entidad se convierte en la PRIMARY KEY.

```
Diagrama ER:                    SQL:
  ID (identificador)      →     id SERIAL PRIMARY KEY
```

---

### Regla 4: Relación 1:N → Clave Foránea

> La relación se implementa poniendo una FK en la tabla del lado "muchos".

```
Diagrama ER:                    SQL:
  Cliente ──1:N── Pedido  →     CREATE TABLE pedidos (
                                  ...
                                  id_cliente INT NOT NULL,
                                  FOREIGN KEY (id_cliente) REFERENCES clientes(id)
                                );
```

**¿Dónde va la FK?** Siempre en la tabla del lado N (el hijo, el "muchos").

---

### Regla 5: Relación N:M → Tabla Intermedia

> Se crea una nueva tabla con las FKs de ambas entidades.

```
Diagrama ER:                        SQL:
  Estudiante ──N:M── Curso    →     CREATE TABLE inscripciones (
                                      id SERIAL PRIMARY KEY,
                                      id_estudiante INT REFERENCES estudiantes(id),
                                      id_curso INT REFERENCES cursos(id)
                                    );
```

---

### Regla 6: Nombres y convenciones

| Convención                           | Ejemplo bueno      | Ejemplo malo             |
| ------------------------------------ | ------------------ | ------------------------ |
| Tablas en **plural**, minúsculas     | `clientes`         | `Cliente`, `CLIENTES`    |
| Columnas en **singular**, snake_case | `fecha_registro`   | `FechaRegistro`, `FECHA` |
| PKs como `id` o `tabla_id`           | `id`, `cliente_id` | `ID_CLIENTE`, `pk`       |
| FKs con prefijo `id_`                | `id_cliente`       | `cliente`, `fk_cli`      |

---

### Ejemplo completo de transformación

**Diagrama ER de una Universidad:**

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  ESTUDIANTE  │──N:M───│ INSCRIPCIÓN  │───N:1───│    CURSO     │
│              │         │              │         │              │
│  id PK       │         │ fecha        │         │  id PK       │
│  nombre      │         │ nota         │         │  nombre      │
│  email       │         │              │         │  descripcion │
└──────────────┘         └──────────────┘         └──────────────┘
                                                        │
                                                       N:1
                                                        │
                                                  ┌──────────────┐
                                                  │   PROFESOR   │
                                                  │              │
                                                  │  id PK       │
                                                  │  nombre      │
                                                  │  titulo      │
                                                  └──────────────┘
```

**Resultado en SQL:**

```sql
CREATE TABLE estudiantes (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80) NOT NULL,
  email   VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE profesores (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80) NOT NULL,
  titulo  VARCHAR(50)
);

CREATE TABLE cursos (
  id            SERIAL PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  descripcion   TEXT,
  id_profesor   INT NOT NULL,
  FOREIGN KEY (id_profesor) REFERENCES profesores(id)
);

CREATE TABLE inscripciones (
  id              SERIAL PRIMARY KEY,
  id_estudiante   INT NOT NULL,
  id_curso        INT NOT NULL,
  fecha           TIMESTAMP DEFAULT NOW(),
  nota            NUMERIC(3,1),
  FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),
  FOREIGN KEY (id_curso) REFERENCES cursos(id)
);
```

---

---

## 8️⃣ Normalización de Datos

---

### ¿Qué es normalizar?

> Normalizar = **organizar las tablas para eliminar datos repetidos** y evitar problemas de consistencia.

---

### La analogía: La mudanza 📦

Imagina que tienes UNA caja enorme con TODA tu ropa mezclada: poleras con calcetines, pantalones con gorros. ¿Qué haces?

**Organizas en cajas separadas:**

- Caja 1: Poleras
- Caja 2: Pantalones
- Caja 3: Calcetines

Normalizar una base de datos es lo mismo: **separar los datos en tablas lógicas** para que cada tabla tenga UN tema claro.

---

### ¿Qué pasa si NO normalizas?

```
Tabla "todo_junto" (MAL):

| pedido | cliente  | email_cliente   | producto   | precio | cantidad |
|--------|----------|-----------------|------------|--------|----------|
| 001    | Juan     | juan@mail.com   | Notebook   | 599990 | 1        |
| 002    | Juan     | juan@mail.com   | Mouse      | 15990  | 2        |
| 003    | Ana      | ana@mail.com    | Notebook   | 599990 | 1        |
| 004    | Juan     | juannuevo@mail  | Teclado    | 29990  | 1        |
```

**Problemas:**

1. **Redundancia**: "Juan" y "juan@mail.com" se repiten 3 veces
2. **Inconsistencia**: En el pedido 004, Juan tiene un email diferente → ¿Cuál es el correcto?
3. **Anomalía de eliminación**: Si borro el pedido 003, pierdo TODA la información de Ana
4. **Anomalía de actualización**: Si Juan cambia su email, debo actualizarlo en TODAS las filas

---

### Primera Forma Normal (1NF)

> **Regla**: Cada celda debe contener **un solo valor atómico** (indivisible).

**❌ Mal (viola 1NF):**

| estudiante | cursos                       |
| ---------- | ---------------------------- |
| Juan       | Matemáticas, Física, Química |
| Ana        | Historia, Inglés             |

**✅ Bien (cumple 1NF):**

| estudiante | curso       |
| ---------- | ----------- |
| Juan       | Matemáticas |
| Juan       | Física      |
| Juan       | Química     |
| Ana        | Historia    |
| Ana        | Inglés      |

**Receta para 1NF:** Si una celda tiene una lista separada por comas → separa en filas individuales.

---

### Segunda Forma Normal (2NF)

> **Regla**: Cumple 1NF + cada columna que **no es clave** debe depender de **toda** la clave primaria, no solo de una parte.

**❌ Mal (viola 2NF):**

Si la PK es **(nro_pedido + producto)**:

| nro_pedido | producto | cantidad | nombre_cliente |
| ---------- | -------- | -------- | -------------- |
| 001        | Notebook | 1        | Juan           |
| 001        | Mouse    | 2        | Juan           |
| 002        | Notebook | 1        | Ana            |

`nombre_cliente` depende SOLO de `nro_pedido`, no de la combinación completa. Eso viola 2NF.

**✅ Bien (cumple 2NF) → Separar en dos tablas:**

**Tabla `pedidos`:**

| nro_pedido | nombre_cliente |
| ---------- | -------------- |
| 001        | Juan           |
| 002        | Ana            |

**Tabla `detalle_pedidos`:**

| nro_pedido | producto | cantidad |
| ---------- | -------- | -------- |
| 001        | Notebook | 1        |
| 001        | Mouse    | 2        |
| 002        | Notebook | 1        |

**Receta para 2NF:** Si un dato depende solo de PARTE de la clave → muévelo a su propia tabla.

---

### Tercera Forma Normal (3NF)

> **Regla**: Cumple 2NF + ninguna columna no-clave debe depender de OTRA columna no-clave (dependencia transitiva).

**❌ Mal (viola 3NF):**

| empleado | departamento | ubicacion_depto |
| -------- | ------------ | --------------- |
| Juan     | Ventas       | Santiago        |
| Ana      | Marketing    | Valparaíso      |
| Pedro    | Ventas       | Santiago        |

`ubicacion_depto` depende de `departamento`, NO del empleado directamente. Es una **dependencia transitiva**: empleado → departamento → ubicación.

**✅ Bien (cumple 3NF) → Separar:**

**Tabla `empleados`:**

| empleado | departamento |
| -------- | ------------ |
| Juan     | Ventas       |
| Ana      | Marketing    |
| Pedro    | Ventas       |

**Tabla `departamentos`:**

| departamento | ubicacion  |
| ------------ | ---------- |
| Ventas       | Santiago   |
| Marketing    | Valparaíso |

**Receta para 3NF:** Si un dato depende de otro dato que NO es la clave → muévelo a su propia tabla.

---

### Resumen de las 3 Formas Normales

| Forma Normal | Problema que resuelve          | Regla resumida                                |
| ------------ | ------------------------------ | --------------------------------------------- |
| **1NF**      | Valores múltiples en una celda | Cada celda = un solo valor                    |
| **2NF**      | Dependencia parcial de la PK   | Todo depende de TODA la PK                    |
| **3NF**      | Dependencia entre no-claves    | Nada depende de otra columna que no sea la PK |

```
¿Tu tabla tiene listas en una celda?     → Aplica 1NF
¿Un dato depende solo de PARTE de la PK? → Aplica 2NF
¿Un dato depende de otro dato no-clave?  → Aplica 3NF
```

---

---

## 📋 Resumen General

---

### Del problema real a la base de datos: El camino completo

```
1. OBSERVAR la realidad
       ↓
2. ABSTRAER (quedarse con lo importante)
       ↓
3. MODELAR (diagrama ER: entidades + atributos + relaciones)
       ↓
4. TRANSFORMAR (aplicar reglas: entidades → tablas, relaciones → FKs)
       ↓
5. NORMALIZAR (eliminar redundancia: 1NF → 2NF → 3NF)
       ↓
6. IMPLEMENTAR (escribir SQL: CREATE TABLE)
```

---

### Tabla de conceptos clave

| Concepto              | Definición rápida                                   |
| --------------------- | --------------------------------------------------- |
| **Modelo ER**         | Diagrama que representa datos y relaciones          |
| **Entidad**           | Objeto del mundo real que queremos registrar        |
| **Atributo**          | Propiedad de una entidad                            |
| **Relación**          | Conexión entre entidades (1:1, 1:N, N:M)            |
| **PK**                | Clave primaria: identifica cada fila de forma única |
| **FK**                | Clave foránea: conecta una tabla con otra           |
| **Entidad fuerte**    | Independiente, tiene PK propia                      |
| **Entidad débil**     | Depende de otra, PK incluye FK del padre            |
| **Tabla intermedia**  | Resuelve relaciones N:M con dos FKs                 |
| **1NF**               | Un valor por celda                                  |
| **2NF**               | Todo depende de toda la PK                          |
| **3NF**               | Nada depende de columnas no-clave                   |
| **Modelo conceptual** | Diagrama abstracto (para todos)                     |
| **Modelo relacional** | Tablas SQL concretas (para técnicos)                |

---
