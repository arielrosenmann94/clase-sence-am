# 📋 Evaluación Integradora: Alke Wallet

> **Módulo:** Fundamentos de Bases de Datos Relacionales
> **Proyecto:** Diseño e implementación de la base de datos de una billetera virtual (similar a Mach o Tenpo)

---

## 🎯 Contexto del Proyecto

Eres parte de un equipo de desarrollo al que se le asignó la siguiente tarea: **Alke Wallet** necesita que se diseñe su base de datos relacional. El sistema debe permitir que los usuarios puedan:

- Almacenar y gestionar sus saldos o criptomonedas
- Realizar transferencias entre usuarios
- Consultar el historial de movimientos

El objetivo de esta evaluación es diseñar el modelo, crear las tablas y ejecutar las consultas necesarias para que el sistema funcione correctamente.

---

## 📦 Entregables

### Archivos a entregar

| Archivo                 | Formato aceptado                    | Contenido                                         |
| ----------------------- | ----------------------------------- | ------------------------------------------------- |
| **Documento principal** | `.docx` (Word) o `.md` (Markdown)   | Todas las sentencias SQL + capturas de pantalla   |
| **Script SQL**          | `.sql`                              | El archivo con todo el código listo para ejecutar |
| **Diagrama ER**         | `.png`, `.jpg`, `.pdf` o fotografía | El modelo Entidad-Relación del sistema            |

> [!TIP]
> Puede entregar la tarea en **Word** (`.docx`) o en **Markdown** (`.md`), según le resulte más cómodo. Si opta por Markdown, puede escribirlo directamente desde VS Code.

### Contenido obligatorio del documento

| #   | Elemento                 | Descripción                                                             |
| --- | ------------------------ | ----------------------------------------------------------------------- |
| 1   | **Creación de la BD**    | La sentencia SQL para crear la base de datos `AlkeWallet`               |
| 2   | **Creación de tablas**   | El DDL (`CREATE TABLE`) de las 3 tablas, con sus claves y restricciones |
| 3   | **Inserción de datos**   | El DML (`INSERT`) con datos de prueba en las 3 tablas                   |
| 4   | **Consultas requeridas** | Las 5 consultas SQL detalladas más abajo                                |
| 5   | **Transaccionalidad**    | Demostrar el uso de `START TRANSACTION`, `COMMIT` y `ROLLBACK`          |
| 6   | **Diagrama ER**          | El diagrama completo mostrando cómo se relacionan las tablas            |
| 7   | **Capturas de pantalla** | Evidencia visual de que las sentencias se ejecutaron correctamente      |

> [!IMPORTANT]
> El documento debe estar **ordenado y bien etiquetado**, paso a paso. Debe ser claro y comprensible.

---

## 🗂️ Las 3 Entidades (Tablas)

Se deben diseñar las siguientes tablas con sus atributos. Prestar atención a los tipos de datos, claves y restricciones correspondientes.

### Tabla `usuario`

| Atributo             | Rol            |
| -------------------- | -------------- |
| `user_id`            | Clave primaria |
| `nombre`             | —              |
| `correo_electronico` | —              |
| `contraseña`         | —              |
| `saldo`              | —              |

### Tabla `moneda`

| Atributo          | Rol            |
| ----------------- | -------------- |
| `currency_id`     | Clave primaria |
| `currency_name`   | —              |
| `currency_symbol` | —              |

### Tabla `transaccion` (registra los movimientos de saldo)

| Atributo           | Rol                       |
| ------------------ | ------------------------- |
| `transaction_id`   | Clave primaria            |
| `sender_user_id`   | Clave foránea → `usuario` |
| `receiver_user_id` | Clave foránea → `usuario` |
| `importe`          | —                         |
| `transaction_date` | —                         |

> [!TIP]
> **Analice con cuidado las relaciones:** ¿Cómo se vincula un usuario con la moneda que está utilizando? Si una de las consultas solicita "la moneda elegida por un usuario", ¿qué columna adicional sería necesario agregar?

---

## ✅ Requerimientos Paso a Paso

### Paso 1 — Crear la Base de Datos

- Crear la base de datos `AlkeWallet` (con `CREATE DATABASE`)
- Seleccionarla para comenzar a utilizarla
- Verificar su creación con `SHOW DATABASES;`

📸 **Captura de pantalla:** mostrar que la base de datos existe.

---

### Paso 2 — Crear las 3 Tablas (DDL)

Diseñar las tablas `usuario`, `moneda` y `transaccion` considerando:

- Seleccionar los **tipos de datos** apropiados para cada columna
- Definir correctamente las **claves primarias** (`PRIMARY KEY`)
- Establecer las **claves foráneas** (`FOREIGN KEY`) donde corresponda
- Aplicar restricciones de integridad: `NOT NULL`, `UNIQUE`, `DEFAULT`, según convenga
- Respetar el **orden de creación** (primero las tablas independientes, luego las que dependen de otras)

📸 **Captura de pantalla:** resultado del `DESCRIBE` de cada tabla.

---

### Paso 3 — Insertar Datos de Prueba (DML)

Ingresar datos en las 3 tablas para poder realizar las consultas:

- Al menos **3 monedas** distintas
- Al menos **4 usuarios** con datos variados
- Al menos **5 transacciones** entre los usuarios

📸 **Captura de pantalla:** resultado de `SELECT * FROM` en cada tabla para verificar los datos ingresados.

---

### Paso 4 — Las 5 Consultas Obligatorias

Escribir y ejecutar las siguientes consultas:

| #   | Consulta                                                             | Tipo              |
| --- | -------------------------------------------------------------------- | ----------------- |
| 1   | Obtener el **nombre de la moneda** elegida por un usuario específico | `SELECT` + `JOIN` |
| 2   | Traer **todas las transacciones** registradas                        | `SELECT`          |
| 3   | Ver todas las transacciones realizadas por **un único usuario**      | `SELECT` + filtro |
| 4   | **Actualizar** el correo electrónico de un usuario                   | `UPDATE`          |
| 5   | **Eliminar** los datos de una transacción (la fila completa)         | `DELETE`          |

📸 **Captura de pantalla:** el resultado de cada consulta ejecutada.

> [!NOTE]
> Para las consultas 4 y 5 (`UPDATE` y `DELETE`), incluir una captura del estado **antes** y **después** para verificar que el cambio se aplicó correctamente.

---

### Paso 5 — Transaccionalidad (ACID)

Demostrar el uso correcto de transacciones en SQL:

- Realizar una **transferencia de saldo** entre dos usuarios utilizando:
  - `START TRANSACTION`
  - Las sentencias necesarias (descontar de uno, agregar al otro y registrar el movimiento)
  - `COMMIT` para confirmar la operación
- Provocar un error intencional (por ejemplo, un **error de clave foránea**) y revertirlo con `ROLLBACK`

📸 **Captura de pantalla:** de la consola mostrando que el `COMMIT` o el `ROLLBACK` se ejecutaron correctamente.

---

### Paso 6 — Diagrama Entidad-Relación (ER)

Elaborar el diagrama del sistema. Se puede utilizar cualquiera de las siguientes herramientas:

- **DBeaver**
- [dbdiagram.io](https://dbdiagram.io)
- [drawSQL](https://drawsql.app)
- La extensión draw.io en VS Code
- ✏️ **A mano** — es válido siempre que la letra sea legible y el diagrama esté bien presentado con una fotografía clara.

**El diagrama debe mostrar obligatoriamente:**

- Las 3 tablas con todos sus campos
- Las relaciones entre ellas (indicando el tipo: 1:N, N:M, etc.)
- Las PK y FK claramente identificadas

📸 **Captura de pantalla o exportación** del diagrama.

---

## 🔧 Herramientas Sugeridas

| Herramienta                               | Utilidad                                       |
| ----------------------------------------- | ---------------------------------------------- |
| DBeaver                                   | Para ejecutar las sentencias SQL               |
| Visual Studio Code                        | Para organizar el archivo `.sql`               |
| Herramienta ER (dbdiagram, drawSQL, etc.) | Para construir el diagrama de la base de datos |

---

## 📊 Criterios de Evaluación

### Aspectos Técnicos

| Criterio                   | Descripción                                                                    |
| -------------------------- | ------------------------------------------------------------------------------ |
| **Diseño de la BD**        | Tablas correctamente estructuradas y tipos de datos apropiados                 |
| **Integridad de datos**    | Uso correcto de `NOT NULL`, `UNIQUE` y `DEFAULT`                               |
| **Claves primarias**       | Todas las `PRIMARY KEY` presentes y bien definidas                             |
| **Integridad referencial** | Las `FOREIGN KEY` correctamente establecidas y las tablas vinculadas           |
| **DDL**                    | Los comandos `CREATE DATABASE` y `CREATE TABLE` funcionan sin errores          |
| **DML**                    | Los comandos `INSERT`, `SELECT`, `UPDATE` y `DELETE` se ejecutan correctamente |

### Aspectos Estructurales (ACID)

| Propiedad        | Significado                                           | Cómo demostrarlo                            |
| ---------------- | ----------------------------------------------------- | ------------------------------------------- |
| **A**tomicidad   | La transacción se realiza completa o no se realiza    | `START TRANSACTION` + `COMMIT` / `ROLLBACK` |
| **C**onsistencia | Las reglas de integridad se respetan en todo momento  | Restricciones `FK`, `NOT NULL`, `UNIQUE`    |
| **I**solamiento  | Las transacciones no interfieren entre sí             | Uso correcto del bloque de transacciones    |
| **D**urabilidad  | Los cambios confirmados persisten de forma permanente | Los datos permanecen después del `COMMIT`   |

---

> **💼 Portafolio:** Este proyecto es una excelente oportunidad para el portafolio profesional. Se recomienda dedicarle especial atención al diseño y presentación, ya que puede ser de gran utilidad al buscar las primeras oportunidades laborales o al destacar el trabajo realizado.
