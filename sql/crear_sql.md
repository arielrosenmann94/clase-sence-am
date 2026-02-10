<!-- =========================================================
Archivo: sql.md
Tema: SQL Básico — Tablas, PK, FK y cambios (curso introductorio)
========================================================= -->

# SQL Básico (curso) — Crear tablas, PK, FK y modificar tablas

Este documento enseña lo esencial para:

1. Crear tablas con SQL
2. Usar **clave primaria (PK)**
3. Usar **clave foránea (FK)**
4. Conocer **tipos de datos** básicos
5. Modificar tablas: agregar columnas, renombrar, cambiar tipos
6. Agregar una FK después (cuando la tabla ya existe)
7. Entender casos típicos sin complejidad extra

> Enfoque: **simple, pedagógico y práctico**.  
> Pensado para estudiantes que recién comienzan.

---

## 0) Ideas base

- Una **tabla** es como una planilla: columnas + filas.
- Cada **fila** es un registro (ej: un producto).
- Cada **columna** es un dato del registro (ej: nombre, precio).
- La base de datos debe proteger los datos con reglas:
  - **PK**: identifica una fila de forma única.
  - **FK**: obliga a que una relación apunte a algo que exista.

---

## 1) Tipos de datos básicos

> Regla simple: elige un tipo de dato según lo que guardas.

### 1.1 Números

- `INT` / `INTEGER`: números enteros (0, 1, 10, 500)
- `BIGINT`: enteros grandes (cuando los IDs crecen mucho)
- `NUMERIC(10,2)`: números con decimales exactos (ideal para dinero)
  - `(10,2)` significa: hasta 10 dígitos en total, 2 decimales
  - Ej: 12345678.90

### 1.2 Texto

- `VARCHAR(50)`: texto corto (hasta 50 caracteres)
- `TEXT`: texto más largo (sin límite práctico)
  > Regla simple: si sabes un máximo razonable, usa `VARCHAR(n)`.

### 1.3 Fechas y hora

- `DATE`: fecha (2026-02-10)
- `TIMESTAMP`: fecha + hora (2026-02-10 15:30:00)

### 1.4 Booleano

- `BOOLEAN`: verdadero/falso (`true`/`false`)

---

## 2) ¿Qué es un CONSTRAINT (restricción)?

Un **constraint** es una regla que la base de datos aplica para evitar datos inválidos.

Los más comunes:

- `PRIMARY KEY` (PK): único y no nulo
- `FOREIGN KEY` (FK): apunta a otra tabla
- `NOT NULL`: campo obligatorio
- `UNIQUE`: no se repite
- `DEFAULT`: valor por defecto
- `CHECK`: condición lógica (ej: cantidad > 0)

> Idea simple: una constraint es un “guardia” que revisa si el dato cumple las reglas.

---

## 3) El uso de DEFAULT (Valores por defecto)

La restricción **DEFAULT** permite asignar un valor automático a una columna cuando no especificamos nada al insertar una fila.

### 3.1 ¿Para qué sirve?

- **Ahorrar tiempo**: No tienes que escribir valores que suelen ser siempre iguales (ej: la fecha de hoy, o el estado "activo").
- **Evitar errores**: Asegura que la columna tenga un dato válido aunque el programador olvide enviarlo.

### 3.2 Ejemplo en la creación

Al crear la tabla, indicas el valor por defecto después del tipo de dato:

```sql
CREATE TABLE usuarios (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  pais VARCHAR(50) DEFAULT 'Chile',   -- Si no se pone país, será 'Chile'
  es_admin BOOLEAN DEFAULT false      -- Por defecto no es admin
);
```

### 3.3 ¿Cómo funciona con INSERT?

Si insertas especificando todas las columnas, usas tu valor:

```sql
INSERT INTO usuarios (id, nombre, pais) VALUES (1, 'Ana', 'Perú');
-- Resultado: Ana, Perú, false (usa el default de es_admin)
```

Si **omites** la columna, la base de datos pone el DEFAULT:

```sql
INSERT INTO usuarios (id, nombre) VALUES (2, 'Juan');
-- Resultado: Juan, 'Chile', false (usa ambos defaults)
```

También puedes usar la palabra clave `DEFAULT` explícitamente:

```sql
INSERT INTO usuarios (id, nombre, pais) VALUES (3, 'Pedro', DEFAULT);
-- Resultado: Pedro, 'Chile', false
```

---

## 4) El uso de CHECK (Validaciones personalizadas)

La restricción **CHECK** sirve para poner reglas personalizadas a los datos de una columna. La base de datos rechazará cualquier intento de insertar algo que no cumpla la regla.

### 4.1 ¿Para qué sirve?

- **Validar formatos**: Asegurar que un texto tenga ciertos caracteres.
- **Rangos numéricos**: Evitar precios negativos o edades imposibles.

### 4.2 Ejemplo: Restringir a números (1-9) y la letra 'k'

Este es el caso típico para un dígito verificador (DV) en Chile:

```sql
CREATE TABLE alumnos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  dv CHAR(1) CHECK (dv IN ('1','2','3','4','5','6','7','8','9','k','K'))
);
```

**Explicación de la regla:**

- `dv IN (...)`: Significa "el valor debe estar dentro de esta lista".
- Agregamos `'K'` (mayúscula) por si acaso, para que sea más flexible.

### 4.3 Otros ejemplos comunes de CHECK

- **Precios positivos:** `CHECK (precio > 0)`
- **Edad mínima:** `CHECK (edad >= 18)`

### 4.4 Ejemplo Avanzado: Impedir el uso de números

Si quieres que una columna (por ejemplo, un nombre) **no tenga ningún número**, puedes usar expresiones regulares (Regex):

```sql
CREATE TABLE personas (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) CHECK (nombre !~ '[0-9]')
);
```

- `!~`: Significa "que NO contenga".
- `'[0-9]'`: Representa cualquier número del 0 al 9.
- **Traducción**: "Nombre no debe contener ningún número en ninguna parte".

---

## 5) Crear una tabla (estructura básica)

### 5.1 Fórmula general

```sql
CREATE TABLE nombre_tabla (
  columna1 TIPO,
  columna2 TIPO,
  columna3 TIPO
);
```

- Se separa por comas.
- Termina con `;`.
- Cada columna tiene nombre + tipo + opcionalmente reglas.

---

## 6) Clave primaria (PK) — lo más importante

### 6.1 ¿Qué hace la PK?

- Identifica cada fila de manera única.
- Evita duplicados del identificador.
- Permite que otras tablas se relacionen correctamente.

### 6.2 Regla del curso

✅ Una tabla tiene solo 1 PK.
Puede ser:

- PK simple (una columna), o
- PK compuesta (2+ columnas juntas), pero sigue siendo una sola PK.

### 6.3 PK simple (forma más simple)

```sql
CREATE TABLE clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);
```

### 6.4 PK autogenerada (si tu DB lo soporta)

En PostgreSQL se suele usar `BIGSERIAL`:

```sql
CREATE TABLE clientes (
  id BIGSERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);
```

Ventaja: no tienes que inventar IDs manualmente, la DB los genera.

---

## 7) Clave foránea (FK) — relación entre tablas

### 7.1 ¿Qué hace una FK?

Una FK obliga a que un valor exista en otra tabla.
Ejemplo real:

- `productos.id_categoria` debe existir en `categorias.id`
- Traducción humana: “no puedes poner una categoría que no existe”.

### 7.2 Regla importante

Una FK solo puede apuntar a una columna que sea:

- `PRIMARY KEY` o
- `UNIQUE`

---

## 8) Ejemplo principal del curso (Categorías y Productos)

### 8.1 Crear tabla padre: categorias

```sql
CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);
```

### 8.2 Crear tabla hija: productos con FK

```sql
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  id_categoria INT,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);
```

**Explicación simple**
`productos.id_categoria` puede ser:

- un número que exista en `categorias.id`, o
- `NULL` (si permitimos productos sin categoría)

Si quieres que sea obligatorio:

```sql
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  id_categoria INT NOT NULL,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);
```

---

## 9) INSERT (agregar filas) — forma simple

### 9.1 Insertar en tabla padre

```sql
INSERT INTO categorias (id, nombre)
VALUES (1, 'Bebidas');
```

### 9.2 Insertar en tabla hija (con FK válida)

```sql
INSERT INTO productos (id, nombre, id_categoria)
VALUES (1, 'Agua 1L', 1);
```

### 9.3 ¿Qué pasa si pongo una FK que no existe?

Si intentas:

```sql
INSERT INTO productos (id, nombre, id_categoria)
VALUES (2, 'Producto X', 999);
```

La base debe rechazarlo porque `categorias.id = 999` no existe.

---

## 10) Cómo verificar que una tabla existe y ver su estructura

### 10.1 En PostgreSQL (psql)

- Listar tablas: `\dt`
- Ver estructura de una tabla: `\d productos`
  (Esto sirve para confirmar PK, FK, tipos de datos y reglas).

### 10.2 En DBeaver (visual)

- Refresh conexión
- Expandir: Schemas → public → Tables
- Click en la tabla → pestaña Columns / Constraints

---

## 11) Modificar tablas con ALTER TABLE (cambios comunes)

### 11.1 Agregar una nueva columna

```sql
ALTER TABLE productos
ADD COLUMN precio NUMERIC(10,2);
```

### 11.2 Agregar una columna con DEFAULT

```sql
ALTER TABLE productos
ADD COLUMN activo BOOLEAN DEFAULT true;
```

### 11.3 Hacer una columna obligatoria (NOT NULL)

```sql
ALTER TABLE productos
ALTER COLUMN nombre SET NOT NULL;
```

> Nota: si ya tienes filas con NULL en esa columna, la DB te dará error.

---

## 12) Agregar una FK después (cuando la tabla ya existe)

Esto pasa mucho en clases:

1. Primero crean tablas sin FK.
2. Después quieren “agregar la relación”.

### 12.1 Si la columna ya existe

```sql
ALTER TABLE productos
ADD FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

### 12.2 Si la columna NO existe

```sql
ALTER TABLE productos
ADD COLUMN id_categoria INT;

ALTER TABLE productos
ADD FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

### 12.3 Problema típico: datos inválidos antes de crear la FK

Si ya hay productos con `id_categoria` que no existe, la FK no se puede crear.
Ejemplo de revisión:

```sql
SELECT id_categoria
FROM productos
WHERE id_categoria IS NOT NULL
  AND id_categoria NOT IN (SELECT id FROM categorias);
```

Solución simple: corregir esos valores o dejarlos NULL.

---

## 13) Renombrar tablas y columnas (simple)

### 13.1 Renombrar una columna

```sql
ALTER TABLE productos
RENAME COLUMN nombre TO nombre_producto;
```

### 13.2 Renombrar una tabla

```sql
ALTER TABLE productos
RENAME TO articulos;
```

---

## 14) Cambiar el tipo de dato de una columna (simple)

Ejemplo: aumentar el tamaño del nombre:

```sql
ALTER TABLE productos
ALTER COLUMN nombre_producto TYPE VARCHAR(120);
```

---

## 15) PK compuesta (explicación simple + ejemplo)

### 15.1 ¿Qué es PK compuesta?

- Es una PK formada por dos columnas juntas.
- Se usa mucho en tablas intermedias (relaciones muchos-a-muchos).

### 15.2 Ejemplo: una venta tiene muchos productos

Para esto NO se guarda una lista de IDs en una columna. Se crea una tabla “detalle”.

```sql
CREATE TABLE ventas (
  id INT PRIMARY KEY,
  fecha TIMESTAMP
);

CREATE TABLE venta_detalle (
  id_venta INT,
  id_producto INT,
  cantidad INT,
  PRIMARY KEY (id_venta, id_producto),
  FOREIGN KEY (id_venta) REFERENCES ventas(id),
  FOREIGN KEY (id_producto) REFERENCES productos(id)
);
```

**¿Por qué PK compuesta aquí?**
Porque la combinación (`id_venta`, `id_producto`) debe ser única: En una venta, un producto no debería aparecer repetido dos veces.

> En el curso: basta con entender que PK compuesta = “identidad por combinación”.

---

## 16) Errores comunes de estudiantes (y cómo evitarlos)

**Error 1: olvidar tipos de datos**
❌ Mal: `CREATE TABLE clientes (id, nombre);`
✅ Bien: `CREATE TABLE clientes (id INT, nombre VARCHAR(50));`

**Error 2: creer que FK puede ser “lista de ids”**
❌ Mal diseño: `producto_ids` guardando "1,2,3"
✅ Bien: tabla detalle/intermedia (`venta_detalle`)

**Error 3: FK apuntando a una columna sin PK/UNIQUE**
Si `clientes.id` no es PK o UNIQUE, la FK falla.
✅ Solución: Definir `clientes.id` como PRIMARY KEY o UNIQUE.

---

## 17) Diccionario (términos del curso)

- **SQL**: lenguaje para hablar con bases de datos.
- **Tabla**: estructura que guarda datos.
- **Fila/Registro**: un elemento guardado (un producto).
- **Columna/Campo**: un dato del registro (nombre, precio).
- **Tipo de dato**: define qué valores acepta una columna.
- **Constraint**: regla para validar datos.
- **PK (Primary Key)**: identificador único de cada fila.
- **FK (Foreign Key)**: columna que referencia otra tabla.
- **NOT NULL**: obligatorio.
- **UNIQUE**: no se repite.
- **DEFAULT**: valor por defecto.
- **ALTER TABLE**: modificar una tabla existente.
- **PK compuesta**: PK hecha de 2+ columnas juntas.
