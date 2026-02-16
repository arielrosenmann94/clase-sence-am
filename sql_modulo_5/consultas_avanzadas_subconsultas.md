# 🔍 Consultas Avanzadas con Subconsultas — Detective SQL

> **Tablas utilizadas:** `curso`, `evaluacion`, `nota`, `alumno`, `inscripcion`
>
> Estas 3 consultas combinan **subconsultas**, **CTEs**, **funciones de agregación** y **filtros condicionales avanzados**.

---

## 📌 Pregunta 21 — Ranking por Sede (solo alumnos activos)

### Enunciado

Para cada sede, calcula el promedio de nota considerando **solo alumnos ACTIVO** y **solo notas de evaluaciones cuya ponderación sea mayor al promedio global de ponderación** (comparación con subconsulta).

**Tablas mínimas:** `curso` + `evaluacion` + `nota` + `alumno` (4).

---

### Solución

```sql
SELECT
    c.sede,                                       -- 1
    ROUND(AVG(n.nota), 2)  AS promedio_sede,      -- 2
    COUNT(DISTINCT a.id_alumno) AS total_alumnos,  -- 3
    COUNT(n.id_nota)           AS total_notas      -- 4
FROM nota n                                        -- 5
JOIN evaluacion e  ON e.id_evaluacion = n.id_evaluacion  -- 6
JOIN curso c       ON c.id_curso      = e.id_curso       -- 7
JOIN alumno a      ON a.id_alumno     = n.id_alumno      -- 8
WHERE a.estado = 'ACTIVO'                                -- 9
  AND e.ponderacion > (                                  -- 10
        SELECT AVG(ponderacion)                          -- 11
        FROM evaluacion                                  -- 12
      )                                                  -- 13
GROUP BY c.sede                                          -- 14
ORDER BY promedio_sede DESC;                              -- 15
```

---

### Explicación línea a línea

|   Línea   | Código                                                          | ¿Qué hace?                                                                                                                                                                                                           |
| :-------: | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   **1**   | `c.sede`                                                        | Selecciona la columna `sede` de la tabla `curso`. Es la dimensión por la que vamos a agrupar los resultados.                                                                                                         |
|   **2**   | `ROUND(AVG(n.nota), 2) AS promedio_sede`                        | Calcula el **promedio** de todas las notas del grupo y lo redondea a 2 decimales. El alias `promedio_sede` le da un nombre legible a la columna resultante.                                                          |
|   **3**   | `COUNT(DISTINCT a.id_alumno) AS total_alumnos`                  | Cuenta los alumnos **únicos** (sin repetir) que participan en ese grupo. `DISTINCT` es clave porque un mismo alumno puede tener muchas notas.                                                                        |
|   **4**   | `COUNT(n.id_nota) AS total_notas`                               | Cuenta el **total de registros de notas** que entraron al cálculo del promedio de esa sede.                                                                                                                          |
|   **5**   | `FROM nota n`                                                   | Establece `nota` como la tabla principal de la consulta. `n` es un **alias** para escribir menos.                                                                                                                    |
|   **6**   | `JOIN evaluacion e ON e.id_evaluacion = n.id_evaluacion`        | Une cada nota con su evaluación correspondiente. Esto nos permite acceder a `ponderacion`, `tipo` y al `id_curso` de esa evaluación.                                                                                 |
|   **7**   | `JOIN curso c ON c.id_curso = e.id_curso`                       | Une la evaluación con su curso. Así obtenemos la **sede** del curso al que pertenece la evaluación.                                                                                                                  |
|   **8**   | `JOIN alumno a ON a.id_alumno = n.id_alumno`                    | Une la nota con el alumno que la obtuvo. Necesario para filtrar por `estado` del alumno.                                                                                                                             |
|   **9**   | `WHERE a.estado = 'ACTIVO'`                                     | **Primer filtro:** solo consideramos notas de alumnos cuyo estado sea `'ACTIVO'`. Los suspendidos y retirados quedan fuera.                                                                                          |
| **10-13** | `AND e.ponderacion > (SELECT AVG(ponderacion) FROM evaluacion)` | **Segundo filtro con subconsulta:** se compara la ponderación de cada evaluación contra el **promedio global de ponderación** de TODAS las evaluaciones. Solo entran las evaluaciones "pesadas" (mayor al promedio). |
| **11-12** | `SELECT AVG(ponderacion) FROM evaluacion`                       | Esta es la **subconsulta escalar**: calcula UN solo número (el promedio global de ponderación). PostgreSQL ejecuta esto una vez y usa ese valor para comparar en cada fila.                                          |
|  **14**   | `GROUP BY c.sede`                                               | Agrupa todas las filas resultantes por sede. Sin esto, `AVG` y `COUNT` calcularían sobre todo el dataset completo.                                                                                                   |
|  **15**   | `ORDER BY promedio_sede DESC`                                   | Ordena los resultados de **mayor a menor** promedio, creando así el **ranking**. La sede con mejor promedio aparece primero.                                                                                         |

---

### 🧠 Conceptos clave de esta consulta

- **Subconsulta escalar:** Una subconsulta que retorna **un solo valor**. Se puede usar directamente en el `WHERE` como si fuera un número.
- **Cadena de JOINs:** Nota → Evaluación → Curso + Nota → Alumno. Cada JOIN agrega una tabla y sus columnas al resultado.
- **`DISTINCT` en COUNT:** Evita contar al mismo alumno varias veces cuando tiene múltiples notas.

---

---

## 📌 Pregunta 23 — Cursos "difíciles" por tasa de reprobación

### Enunciado

Lista los **5 cursos con mayor porcentaje de notas < 4.0**, considerando solo inscripciones `VIGENTE` o `FINALIZADA` y solo evaluaciones tipo `PRUEBA` o `PROYECTO`. Debe incluir una subconsulta o CTE que calcule la tasa por curso.

**Tablas mínimas:** `curso` + `evaluacion` + `nota` + `inscripcion` (4).

---

### Solución

```sql
WITH tasa_reprobacion AS (                                      -- 1
    SELECT                                                      -- 2
        c.id_curso,                                             -- 3
        c.nombre,                                               -- 4
        c.sede,                                                 -- 5
        COUNT(n.id_nota)                        AS total_notas, -- 6
        COUNT(n.id_nota) FILTER (WHERE n.nota < 4.0) AS reprobadas, -- 7
        ROUND(                                                  -- 8
            COUNT(n.id_nota) FILTER (WHERE n.nota < 4.0) * 100.0 -- 9
            / NULLIF(COUNT(n.id_nota), 0),                      -- 10
            2                                                   -- 11
        ) AS porcentaje_reprobacion                             -- 12
    FROM nota n                                                 -- 13
    JOIN evaluacion e   ON e.id_evaluacion = n.id_evaluacion    -- 14
    JOIN curso c        ON c.id_curso      = e.id_curso         -- 15
    JOIN inscripcion i  ON i.id_alumno     = n.id_alumno        -- 16
                       AND i.id_curso      = c.id_curso         -- 17
    WHERE e.tipo IN ('PRUEBA', 'PROYECTO')                      -- 18
      AND i.estado IN ('VIGENTE', 'FINALIZADA')                 -- 19
    GROUP BY c.id_curso, c.nombre, c.sede                       -- 20
)                                                               -- 21
SELECT                                                          -- 22
    nombre,                                                     -- 23
    sede,                                                       -- 24
    total_notas,                                                -- 25
    reprobadas,                                                 -- 26
    porcentaje_reprobacion                                      -- 27
FROM tasa_reprobacion                                           -- 28
WHERE total_notas >= 5                                          -- 29
ORDER BY porcentaje_reprobacion DESC                            -- 30
LIMIT 5;                                                        -- 31
```

---

### Explicación línea a línea

|   Línea   | Código                                                                        | ¿Qué hace?                                                                                                                                                                                                                                      |
| :-------: | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   **1**   | `WITH tasa_reprobacion AS (`                                                  | Inicia un **CTE (Common Table Expression)**. Es como crear una tabla temporal con nombre que solo existe durante esta consulta. El nombre `tasa_reprobacion` será referenciado después.                                                         |
|   **2**   | `SELECT`                                                                      | Inicio del SELECT interno del CTE.                                                                                                                                                                                                              |
|   **3**   | `c.id_curso`                                                                  | Selecciona el ID del curso para agrupar.                                                                                                                                                                                                        |
|   **4**   | `c.nombre`                                                                    | Selecciona el nombre del curso para mostrarlo en el resultado final.                                                                                                                                                                            |
|   **5**   | `c.sede`                                                                      | Incluye la sede para contexto adicional.                                                                                                                                                                                                        |
|   **6**   | `COUNT(n.id_nota) AS total_notas`                                             | Cuenta **todas** las notas válidas en ese curso (solo las que pasaron los filtros).                                                                                                                                                             |
|   **7**   | `COUNT(n.id_nota) FILTER (WHERE n.nota < 4.0) AS reprobadas`                  | **Cuenta condicional**: solo cuenta las notas que son **menores a 4.0** (reprobadas). `FILTER (WHERE ...)` es una función de PostgreSQL que permite contar/sumar solo filas que cumplan una condición, **sin afectar el resto de la consulta**. |
| **8-12**  | `ROUND(... * 100.0 / NULLIF(..., 0), 2) AS porcentaje_reprobacion`            | Calcula el **porcentaje**: (reprobadas × 100) ÷ total. `NULLIF(COUNT(...), 0)` evita la **división por cero** — si el total es 0, retorna `NULL` en vez de un error. `ROUND(..., 2)` redondea a 2 decimales.                                    |
|  **13**   | `FROM nota n`                                                                 | Tabla principal: las notas.                                                                                                                                                                                                                     |
|  **14**   | `JOIN evaluacion e ON e.id_evaluacion = n.id_evaluacion`                      | Une nota con su evaluación para acceder al tipo y al curso.                                                                                                                                                                                     |
|  **15**   | `JOIN curso c ON c.id_curso = e.id_curso`                                     | Une evaluación con curso para obtener nombre y sede.                                                                                                                                                                                            |
| **16-17** | `JOIN inscripcion i ON i.id_alumno = n.id_alumno AND i.id_curso = c.id_curso` | Une con inscripción usando **dos condiciones**: mismo alumno Y mismo curso. Esto asegura que solo consideramos notas de alumnos **inscritos en ese curso específico**.                                                                          |
|  **18**   | `WHERE e.tipo IN ('PRUEBA', 'PROYECTO')`                                      | **Filtro 1:** solo evaluaciones de tipo PRUEBA o PROYECTO. Excluye QUIZ y TAREA.                                                                                                                                                                |
|  **19**   | `AND i.estado IN ('VIGENTE', 'FINALIZADA')`                                   | **Filtro 2:** solo inscripciones activas o terminadas. Excluye las ANULADAS.                                                                                                                                                                    |
|  **20**   | `GROUP BY c.id_curso, c.nombre, c.sede`                                       | Agrupa por curso. Todas las columnas no-agregadas del SELECT deben ir aquí.                                                                                                                                                                     |
|  **21**   | `)`                                                                           | Cierra el CTE.                                                                                                                                                                                                                                  |
| **22-27** | `SELECT nombre, sede, total_notas, reprobadas, porcentaje_reprobacion`        | La consulta principal lee del CTE como si fuera una tabla normal.                                                                                                                                                                               |
|  **28**   | `FROM tasa_reprobacion`                                                       | Referencia al CTE creado arriba.                                                                                                                                                                                                                |
|  **29**   | `WHERE total_notas >= 5`                                                      | Filtro de relevancia: solo cursos con al menos 5 notas para que el porcentaje sea significativo.                                                                                                                                                |
|  **30**   | `ORDER BY porcentaje_reprobacion DESC`                                        | Ordena de mayor a menor tasa de reprobación. Los cursos más "difíciles" quedan arriba.                                                                                                                                                          |
|  **31**   | `LIMIT 5`                                                                     | Toma solo los **5 primeros** (los 5 peores).                                                                                                                                                                                                    |

---

### 🧠 Conceptos clave de esta consulta

- **CTE (`WITH ... AS`):** Permite escribir consultas complejas de forma **modular y legible**. Primero calculas los datos intermedios, luego los consumes.
- **`FILTER (WHERE ...)`:** Exclusivo de PostgreSQL. Permite hacer agregaciones condicionales sin necesidad de `CASE WHEN` dentro del `COUNT`.
- **`NULLIF(valor, 0)`:** Función de protección contra división por cero. Si `valor = 0`, retorna `NULL`, y cualquier operación con `NULL` da `NULL` (no un error).
- **JOIN con doble condición:** Al unir con `inscripcion`, se necesitan dos columnas porque la relación alumno-curso requiere ambas claves.

---

---

## 📌 Pregunta 24 — Alumnos top consistentes (mínimo de rendimiento)

### Enunciado

Encuentra los alumnos que cumplan **todas** estas condiciones:

1. Tienen **≥ 8 notas** registradas.
2. Su promedio es **≥ 5.5**.
3. **Ninguna** de sus notas es menor al promedio del curso en el que fue evaluado (comparación con subconsulta correlacionada o CTE + JOIN).

**Tablas mínimas:** `alumno` + `nota` + `evaluacion` + `curso` (4).

---

### Solución

```sql
WITH promedios_curso AS (                                        -- 1
    SELECT                                                       -- 2
        e.id_curso,                                              -- 3
        ROUND(AVG(n.nota), 2) AS promedio_curso                  -- 4
    FROM nota n                                                  -- 5
    JOIN evaluacion e ON e.id_evaluacion = n.id_evaluacion       -- 6
    GROUP BY e.id_curso                                          -- 7
),                                                               -- 8
resumen_alumno AS (                                              -- 9
    SELECT                                                       -- 10
        a.id_alumno,                                             -- 11
        a.nombre,                                                -- 12
        a.apellido,                                              -- 13
        a.estado,                                                -- 14
        COUNT(n.id_nota)       AS total_notas,                   -- 15
        ROUND(AVG(n.nota), 2)  AS promedio_alumno,               -- 16
        MIN(n.nota)            AS nota_minima,                   -- 17
        MAX(n.nota)            AS nota_maxima                    -- 18
    FROM alumno a                                                -- 19
    JOIN nota n      ON n.id_alumno     = a.id_alumno            -- 20
    GROUP BY a.id_alumno, a.nombre, a.apellido, a.estado         -- 21
    HAVING COUNT(n.id_nota) >= 8                                 -- 22
       AND AVG(n.nota) >= 5.5                                    -- 23
)                                                                -- 24
SELECT                                                           -- 25
    ra.nombre,                                                   -- 26
    ra.apellido,                                                 -- 27
    ra.estado,                                                   -- 28
    ra.total_notas,                                              -- 29
    ra.promedio_alumno,                                          -- 30
    ra.nota_minima,                                              -- 31
    ra.nota_maxima                                               -- 32
FROM resumen_alumno ra                                           -- 33
WHERE NOT EXISTS (                                               -- 34
    SELECT 1                                                     -- 35
    FROM nota n2                                                 -- 36
    JOIN evaluacion e2  ON e2.id_evaluacion = n2.id_evaluacion   -- 37
    JOIN promedios_curso pc ON pc.id_curso  = e2.id_curso        -- 38
    WHERE n2.id_alumno = ra.id_alumno                            -- 39
      AND n2.nota < pc.promedio_curso                            -- 40
)                                                                -- 41
ORDER BY ra.promedio_alumno DESC,                                -- 42
         ra.total_notas DESC;                                    -- 43
```

---

### Explicación línea a línea

|   Línea   | Código                                                       | ¿Qué hace?                                                                                                                                                                                            |
| :-------: | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   **1**   | `WITH promedios_curso AS (`                                  | Inicia el **primer CTE**. Aquí calcularemos el promedio de nota de cada curso. Este promedio será el "piso" contra el que comparamos.                                                                 |
|  **2-4**  | `SELECT e.id_curso, ROUND(AVG(n.nota), 2) AS promedio_curso` | Para cada curso, calcula el promedio de **todas** las notas de ese curso redondeado a 2 decimales.                                                                                                    |
|  **5-6**  | `FROM nota n JOIN evaluacion e ON ...`                       | Une notas con evaluaciones para saber a qué curso pertenece cada nota.                                                                                                                                |
|   **7**   | `GROUP BY e.id_curso`                                        | Agrupa por curso: un promedio por curso.                                                                                                                                                              |
|   **8**   | `,`                                                          | La coma separa múltiples CTEs. Puedes encadenar tantos `WITH` como necesites.                                                                                                                         |
|   **9**   | `resumen_alumno AS (`                                        | Inicia el **segundo CTE**. Aquí calculamos las estadísticas del alumno y aplicamos los filtros de cantidad y promedio.                                                                                |
| **10-14** | `SELECT a.id_alumno, a.nombre, a.apellido, a.estado`         | Selecciona datos identificatorios del alumno.                                                                                                                                                         |
|  **15**   | `COUNT(n.id_nota) AS total_notas`                            | Cuenta cuántas notas tiene el alumno en total.                                                                                                                                                        |
|  **16**   | `ROUND(AVG(n.nota), 2) AS promedio_alumno`                   | Calcula su promedio general.                                                                                                                                                                          |
|  **17**   | `MIN(n.nota) AS nota_minima`                                 | La nota más baja del alumno (útil para contexto).                                                                                                                                                     |
|  **18**   | `MAX(n.nota) AS nota_maxima`                                 | La nota más alta (contexto adicional).                                                                                                                                                                |
| **19-20** | `FROM alumno a JOIN nota n ON ...`                           | Une alumno con sus notas.                                                                                                                                                                             |
|  **21**   | `GROUP BY a.id_alumno, a.nombre, a.apellido, a.estado`       | Agrupa por alumno.                                                                                                                                                                                    |
|  **22**   | `HAVING COUNT(n.id_nota) >= 8`                               | **Condición 1:** solo alumnos con **8 o más notas**. `HAVING` filtra **después** de agrupar (a diferencia de `WHERE` que filtra antes).                                                               |
|  **23**   | `AND AVG(n.nota) >= 5.5`                                     | **Condición 2:** solo alumnos con promedio **≥ 5.5**. Se puede usar `AVG()` directamente en `HAVING` porque estamos filtrando grupos.                                                                 |
|  **24**   | `)`                                                          | Cierra el segundo CTE.                                                                                                                                                                                |
| **25-32** | `SELECT ra.nombre, ra.apellido, ...`                         | La consulta principal selecciona los datos del resumen de alumnos que ya pasaron las condiciones 1 y 2.                                                                                               |
|  **33**   | `FROM resumen_alumno ra`                                     | Lee del segundo CTE.                                                                                                                                                                                  |
|  **34**   | `WHERE NOT EXISTS (`                                         | **Condición 3 — la más importante:** `NOT EXISTS` verifica que **NO exista** ninguna fila que cumpla la subconsulta interna. Si la subconsulta retorna al menos 1 fila, el alumno queda **excluido**. |
|  **35**   | `SELECT 1`                                                   | En un `EXISTS`, lo que seleccionas no importa. `SELECT 1` es una convención que dice "solo me interesa saber si hay filas, no qué contienen".                                                         |
| **36-37** | `FROM nota n2 JOIN evaluacion e2 ON ...`                     | Busca todas las notas de este alumno con sus evaluaciones.                                                                                                                                            |
|  **38**   | `JOIN promedios_curso pc ON pc.id_curso = e2.id_curso`       | Une con el primer CTE para obtener el **promedio del curso** correspondiente.                                                                                                                         |
|  **39**   | `WHERE n2.id_alumno = ra.id_alumno`                          | **Correlación:** conecta la subconsulta con la consulta principal. Para cada alumno de `resumen_alumno`, busca SUS notas.                                                                             |
|  **40**   | `AND n2.nota < pc.promedio_curso`                            | La condición que buscamos **que NO exista**: ¿hay alguna nota del alumno que sea **menor** al promedio de su curso? Si la hay, el alumno **no es "consistente"**.                                     |
|  **41**   | `)`                                                          | Cierra el `NOT EXISTS`.                                                                                                                                                                               |
| **42-43** | `ORDER BY ra.promedio_alumno DESC, ra.total_notas DESC`      | Ordena los alumnos consistentes: primero por mejor promedio, luego por cantidad de notas.                                                                                                             |

---

### 🧠 Conceptos clave de esta consulta

- **Múltiples CTEs encadenados:** Se pueden definir varios CTEs separados por coma. El segundo CTE puede usar (o no) al primero. La consulta final usa ambos.
- **`HAVING` vs `WHERE`:**
  - `WHERE` filtra **filas individuales** antes de agrupar.
  - `HAVING` filtra **grupos** después de agrupar. Por eso puede usar `COUNT()`, `AVG()`, etc.
- **`NOT EXISTS` + subconsulta correlacionada:** La subconsulta se ejecuta **una vez por cada fila** de la consulta principal. Es la forma SQL estándar de decir "no hay ningún registro que cumpla X". Es más eficiente que alternativas con `NOT IN` cuando hay `NULL` involucrados.
- **Subconsulta correlacionada:** La cláusula `WHERE n2.id_alumno = ra.id_alumno` hace que la subconsulta "sepa" de qué alumno estamos hablando en cada iteración.

---

---

## 🗺️ Resumen Visual — Flujo de Tablas

```
Pregunta 21:
nota ──JOIN──▶ evaluacion ──JOIN──▶ curso (→ sede)
  │
  └────JOIN──▶ alumno (→ estado ACTIVO)

  + Subconsulta escalar en WHERE: AVG(ponderacion)

─────────────────────────────────────────────────

Pregunta 23:
nota ──JOIN──▶ evaluacion ──JOIN──▶ curso (→ nombre, sede)
  │
  └────JOIN──▶ inscripcion (→ estado VIGENTE/FINALIZADA)

  + CTE para calcular tasa de reprobación por curso

─────────────────────────────────────────────────

Pregunta 24:
CTE 1: nota ──JOIN──▶ evaluacion ──GROUP BY──▶ promedio_curso
CTE 2: alumno ──JOIN──▶ nota ──HAVING──▶ filtros (≥8, ≥5.5)

Consulta final: CTE2 + NOT EXISTS(nota + evaluacion + CTE1)
```

---

## 📚 Glosario Rápido

| Concepto                       | Descripción                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| **Subconsulta escalar**        | Retorna **un solo valor**. Se usa en `WHERE`, `SELECT` o `HAVING`.         |
| **CTE**                        | `WITH nombre AS (...)` — tabla temporal que solo vive durante la consulta. |
| **`FILTER (WHERE ...)`**       | Agregación condicional exclusiva de PostgreSQL.                            |
| **`NULLIF(a, b)`**             | Retorna `NULL` si `a = b`. Útil para evitar división por cero.             |
| **`NOT EXISTS`**               | Retorna `TRUE` si la subconsulta **no produce filas**.                     |
| **Subconsulta correlacionada** | Subconsulta que referencia columnas de la consulta externa.                |
| **`HAVING`**                   | Filtra **grupos** (post-`GROUP BY`), puede usar funciones de agregación.   |
| **`DISTINCT` en COUNT**        | Cuenta sin repetir valores duplicados.                                     |
