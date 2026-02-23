# 📋 Evaluación Integradora: Alke Wallet

> **Módulo:** Fundamentos de Bases de Datos Relacionales
> **Proyecto:** Diseño e implementación de la base de datos de una billetera virtual (similar a Mach o Tenpo)

---

## 🎯 Contexto del Proyecto

Usted forma parte de un equipo de desarrollo al que se le ha encomendado la siguiente misión: **Alke Wallet** requiere el diseño de su base de datos relacional. El sistema debe permitir que los usuarios puedan:

- Almacenar y gestionar su saldo en moneda local o criptomonedas
- Realizar transferencias entre usuarios
- Consultar el historial de movimientos y transacciones

Su tarea consiste en construir el modelo de datos, crear las tablas correspondientes y elaborar las consultas necesarias para el funcionamiento del sistema.

---

## 📦 Entregables

### Archivos requeridos

| Archivo                 | Formato aceptado                    | Contenido                                                   |
| ----------------------- | ----------------------------------- | ----------------------------------------------------------- |
| **Documento principal** | `.docx` (Word) o `.md` (Markdown)   | Todas las sentencias SQL junto con las capturas de pantalla |
| **Script SQL**          | `.sql`                              | Archivo con el código completo listo para su ejecución      |
| **Diagrama ER**         | `.png`, `.jpg`, `.pdf` o fotografía | El Modelo Entidad-Relación del sistema                      |

> [!TIP]
> El documento puede entregarse en **Word** (`.docx`) o en **Markdown** (`.md`), según la preferencia y comodidad del estudiante. La opción Markdown puede redactarse directamente desde VS Code.

### Contenido obligatorio del documento

| #   | Elemento                 | Descripción                                                         |
| --- | ------------------------ | ------------------------------------------------------------------- |
| 1   | **Creación de la BD**    | Sentencia SQL para crear la base de datos `AlkeWallet`              |
| 2   | **Creación de tablas**   | DDL (`CREATE TABLE`) de las 3 tablas con sus claves y restricciones |
| 3   | **Inserción de datos**   | DML (`INSERT`) con datos de prueba en las 3 tablas                  |
| 4   | **Consultas requeridas** | Las 5 consultas SQL detalladas más adelante                         |
| 5   | **Transaccionalidad**    | Demostración del uso de `START TRANSACTION`, `COMMIT` y `ROLLBACK`  |
| 6   | **Diagrama ER**          | Diagrama completo que refleje las relaciones entre entidades        |
| 7   | **Capturas de pantalla** | Evidencia visual de la ejecución correcta de cada paso              |

> [!IMPORTANT]
> El documento debe estar **estructurado y correctamente etiquetado**, paso a paso y en orden. Se espera claridad y prolijidad en su presentación.

---

## 🗂️ Las 3 Entidades (Tablas)

Se deben construir las siguientes tablas con sus atributos correspondientes. Preste especial atención a los tipos de datos, claves y restricciones que considere pertinentes.

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

### Tabla `transaccion` (La que registra los movimientos de fondos)

| Atributo           | Rol                       |
| ------------------ | ------------------------- |
| `transaction_id`   | Clave primaria            |
| `sender_user_id`   | Clave foránea → `usuario` |
| `receiver_user_id` | Clave foránea → `usuario` |
| `importe`          | —                         |
| `transaction_date` | —                         |

> [!TIP]
> **Reflexione sobre las relaciones:** ¿De qué manera se vincula un usuario con la moneda que utiliza? Si una de las consultas solicita "la moneda elegida por un usuario en particular", ¿qué columna adicional debería incorporarse al diseño?

---

## ✅ Requerimientos Paso a Paso

### Paso 1 — Crear la Base de Datos

- Crear la base de datos `AlkeWallet` mediante `CREATE DATABASE`
- Seleccionarla para comenzar a trabajar
- Verificar su existencia con `SHOW DATABASES;`

📸 **Captura de pantalla:** evidencia de que la base de datos fue creada correctamente.

---

### Paso 2 — Crear las 3 Tablas (DDL)

Construir las tablas `usuario`, `moneda` y `transaccion` teniendo en cuenta:

- La elección adecuada de **tipos de datos** para cada columna
- La correcta definición de **claves primarias** (`PRIMARY KEY`)
- El establecimiento de **claves foráneas** (`FOREIGN KEY`) donde corresponda
- La aplicación de restricciones que garanticen la integridad: `NOT NULL`, `UNIQUE`, `DEFAULT`, según se considere pertinente
- El **orden de creación** (primero las tablas independientes, luego las dependientes)

📸 **Captura de pantalla:** resultado del `DESCRIBE` de cada tabla.

---

### Paso 3 — Inserción de Datos de Prueba (DML)

Insertar registros en las 3 tablas a fin de poder ejecutar las consultas posteriores:

- Al menos **3 monedas** distintas
- Al menos **4 usuarios** con datos de ejemplo
- Al menos **5 transacciones** entre distintos usuarios

📸 **Captura de pantalla:** resultado de `SELECT * FROM` en cada tabla para verificar los datos insertados.

---

### Paso 4 — Las 5 Consultas Obligatorias

Elabore y ejecute las siguientes consultas:

| #   | Consulta                                                                   | Tipo              |
| --- | -------------------------------------------------------------------------- | ----------------- |
| 1   | Obtener el **nombre de la moneda** seleccionada por un usuario determinado | `SELECT` + `JOIN` |
| 2   | Listar **todas las transacciones** registradas en el sistema               | `SELECT`          |
| 3   | Ver todas las transacciones realizadas por **un único usuario**            | `SELECT` + filtro |
| 4   | **Modificar** el correo electrónico de un usuario                          | `UPDATE`          |
| 5   | **Eliminar** los datos de una transacción específica (fila completa)       | `DELETE`          |

📸 **Captura de pantalla:** resultado de cada consulta ejecutada correctamente.

> [!NOTE]
> Para las consultas 4 y 5 (`UPDATE` y `DELETE`), incluya una captura del estado **antes** y otra **después** de la operación, de modo que sea posible verificar que el cambio se aplicó correctamente.

---

### Paso 5 — Transaccionalidad (ACID)

Demuestre que comprende el funcionamiento de las transacciones en SQL:

- Realice una **transferencia de fondos** entre dos usuarios utilizando:
  - `START TRANSACTION`
  - Las sentencias necesarias (descontar del emisor, acreditar al receptor y registrar el movimiento)
  - `COMMIT` para confirmar la operación
- Produzca deliberadamente un error (por ejemplo, una **violación de clave foránea**) y deshaga la operación mediante `ROLLBACK`

📸 **Captura de pantalla:** consola mostrando que el `COMMIT` o el `ROLLBACK` se ejecutaron correctamente.

---

### Paso 6 — Diagrama Entidad-Relación (ER)

Elabore el diagrama que represente el modelo de datos del sistema. Puede utilizar cualquiera de las siguientes herramientas:

- **DBeaver**
- [dbdiagram.io](https://dbdiagram.io)
- [drawSQL](https://drawsql.app)
- La extensión draw.io en VS Code
- ✏️ **Diagrama a mano** — es válido siempre que sea legible y esté correctamente fotografiado.

**El diagrama debe mostrar obligatoriamente:**

- Las 3 tablas con todos sus campos
- Las relaciones entre ellas (identificando si son 1:N, N:M, etc.)
- Las claves primarias y foráneas claramente señaladas

📸 **Captura o exportación** del diagrama.

---

## 🔧 Herramientas Recomendadas

| Herramienta                               | Propósito                                     |
| ----------------------------------------- | --------------------------------------------- |
| DBeaver                                   | Ejecución de sentencias SQL                   |
| Visual Studio Code                        | Redacción y organización del archivo `.sql`   |
| Herramienta ER (dbdiagram, drawSQL, etc.) | Construcción del diagrama de la base de datos |

---

## 📊 Criterios de Evaluación

### Aspectos Técnicos

| Criterio                   | Descripción                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| **Diseño de la BD**        | Tablas correctamente construidas con tipos de datos apropiados              |
| **Integridad de datos**    | Uso adecuado de `NOT NULL`, `UNIQUE` y `DEFAULT`                            |
| **Claves primarias**       | Presencia y correcta definición de `PRIMARY KEY` en todas las tablas        |
| **Integridad referencial** | `FOREIGN KEY` correctamente declaradas y relaciones entre tablas coherentes |
| **DDL**                    | Correcto funcionamiento de `CREATE DATABASE` y `CREATE TABLE`               |
| **DML**                    | Correcto funcionamiento de `INSERT`, `SELECT`, `UPDATE` y `DELETE`          |

### Aspectos Estructurales (ACID)

| Propiedad        | Significado                                           | Evidencia esperada                          |
| ---------------- | ----------------------------------------------------- | ------------------------------------------- |
| **A**tomicidad   | La transacción se ejecuta completa o no se ejecuta    | `START TRANSACTION` + `COMMIT` / `ROLLBACK` |
| **C**onsistencia | Las reglas de integridad se respetan en todo momento  | Restricciones `FK`, `NOT NULL`, `UNIQUE`    |
| **I**solamiento  | Las transacciones no interfieren entre sí             | Uso correcto del bloque transaccional       |
| **D**urabilidad  | Los cambios confirmados persisten de forma permanente | Datos presentes tras el `COMMIT`            |

---

> **💼 Portafolio profesional:** Este proyecto constituye un material de valor para el portafolio de cada estudiante. Se recomienda cuidar la presentación y destacar las decisiones de diseño más relevantes, ya que puede resultar de utilidad en procesos de selección laboral.
