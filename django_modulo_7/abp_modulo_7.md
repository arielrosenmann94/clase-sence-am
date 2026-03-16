# 📋 Evaluación del Módulo 7 — Acceso a Datos con Django

# 🏦 Proyecto: Alke Wallet

---

> 📎 **Documento original de la evaluación:**
>
> [Abrir en Google Docs](https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true)
>
> `https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true`

---

## 🎯 ¿De qué se trata?

La empresa fintech ficticia **Alke Financial** necesita una aplicación web para gestionar información de usuarios y operaciones financieras básicas. Tu trabajo es construir esa aplicación desde cero usando **Django + SQLite**, aplicando todo lo aprendido en las clases del módulo.

---

## 📦 ¿Qué debes entregar al final?

| #   | Entregable                                  | Formato                   |
| --- | ------------------------------------------- | ------------------------- |
| 1   | Proyecto Django completo                    | Carpeta comprimida `.zip` |
| 2   | Documento explicativo de tu modelo de datos | `.md` o `.pdf`            |
| 3   | Capturas de pantalla de la app funcionando  | Dentro del documento      |

---

---

# 🚶 Paso a Paso: Lo que Debes Hacer (En Orden)

---

## Paso 1 — Crear el Proyecto Django

Crea un proyecto Django nuevo. Dentro del proyecto, crea una aplicación (app) que represente la wallet.

**Lo que se va a revisar:**

- Que el proyecto exista y se pueda ejecutar con `python manage.py runserver` sin errores.

---

## Paso 2 — Verificar la Base de Datos

Tu proyecto debe usar **SQLite**, que es la base de datos que Django trae por defecto. No necesitas instalar nada adicional.

**Lo que debes hacer:**

- Abre tu archivo `settings.py` y confirma que la sección `DATABASES` apunte a SQLite.
- Al ejecutar el proyecto por primera vez, Django generará automáticamente un archivo `.sqlite3`. Ese archivo ES tu base de datos.

**Lo que se va a revisar:**

- Que la configuración en `settings.py` sea correcta.
- Que el archivo `.sqlite3` exista y se incluya en la entrega.

---

## Paso 3 — Diseñar y Crear los Modelos

Los modelos son las clases Python que representan las tablas de tu base de datos. Piensa en qué datos necesita una empresa fintech tipo wallet para funcionar.

**Lo que debes hacer:**

- Crear los modelos necesarios dentro de `models.py` de tu aplicación.
- Cada modelo debe tener campos con los tipos de datos que correspondan (`CharField`, `IntegerField`, `DecimalField`, `DateTimeField`, `BooleanField`, etc.).
- Cada campo debe tener las restricciones apropiadas (largo máximo, si puede ser nulo, si debe ser único, valores por defecto).

**Lo que se va a revisar:**

- Que los modelos representen correctamente el dominio de una wallet financiera.
- Que los tipos de campo y restricciones tengan sentido.
- Que el código sea legible y siga las convenciones de Django.

---

## Paso 4 — Establecer Relaciones entre Modelos

Los modelos no existen solos. En una aplicación real, las entidades se conectan entre sí.

**Lo que debes hacer:**

- Conectar tus modelos usando los campos de relación de Django: `ForeignKey`, `OneToOneField` o `ManyToManyField`, según corresponda a la lógica de tu aplicación.
- Definir qué pasa cuando se elimina un registro relacionado (parámetro `on_delete`).

**Lo que se va a revisar:**

- Que las relaciones sean lógicas y coherentes.
- Que `on_delete` esté definido en cada relación que lo requiera.

---

## Paso 5 — Generar y Aplicar Migraciones

Las migraciones convierten tus modelos de Python en tablas reales dentro de la base de datos.

**Lo que debes hacer:**

- Ejecutar el comando que genera las migraciones a partir de tus modelos.
- Ejecutar el comando que aplica esas migraciones a la base de datos.
- Si después de la primera migración modificas un modelo, debes volver a generar y aplicar una nueva migración.

**Lo que se va a revisar:**

- Que los archivos de migración existan dentro de la carpeta `migrations/` de tu app.
- Que las migraciones se apliquen sin errores.
- Que las tablas en la base de datos correspondan a tus modelos.

---

## Paso 6 — Construir las Vistas y Templates para CRUD

Tu aplicación debe permitir realizar las 4 operaciones fundamentales desde la interfaz web (no solo desde el Admin o el Shell):

### ➕ Crear (Create)

- Un formulario en el navegador que permita agregar nuevos registros.
- Al enviar el formulario, los datos deben guardarse en la base de datos.

### 👁️ Leer (Read)

- Una página que liste los registros almacenados.
- Una página que muestre el detalle de un registro individual.

### ✏️ Actualizar (Update)

- Un formulario que permita editar un registro existente.
- Al guardar, los cambios deben reflejarse en la base de datos.

### 🗑️ Eliminar (Delete)

- Un mecanismo (botón o enlace) que permita borrar un registro.
- El registro debe desaparecer de la base de datos después de eliminar.

**Lo que se va a revisar:**

- Que las 4 operaciones funcionen desde el navegador.
- Que las vistas usen el ORM de Django para interactuar con la base de datos.
- Que los templates muestren los datos correctamente.
- Que el flujo sea: Template → Vista → ORM → Base de Datos (y de vuelta).

---

## Paso 7 — Configurar las URLs

Cada vista necesita una URL que la conecte con el navegador.

**Lo que debes hacer:**

- Definir las rutas en el archivo `urls.py` de tu aplicación.
- Cada operación CRUD debe tener su propia URL.

**Lo que se va a revisar:**

- Que todas las URLs funcionen y lleven a la vista correcta.
- Que las rutas sean limpias y descriptivas.

---

## Paso 8 — Probar Todo

Antes de entregar, verifica que todo funcione como esperas.

**Lista de verificación final:**

- [ ] ¿El proyecto se ejecuta sin errores con `runserver`?
- [ ] ¿Los modelos tienen campos y relaciones correctas?
- [ ] ¿Las migraciones se aplican sin errores?
- [ ] ¿Puedo CREAR un registro desde el navegador?
- [ ] ¿Puedo VER una lista de registros?
- [ ] ¿Puedo ver el DETALLE de un registro?
- [ ] ¿Puedo EDITAR un registro existente?
- [ ] ¿Puedo ELIMINAR un registro?
- [ ] ¿Los datos persisten después de cada operación?

---

## Paso 9 — Escribir el Documento Explicativo

Crea un archivo `.md` o `.pdf` que contenga:

1. **Tu modelo de datos:** Qué modelos creaste, qué campos tiene cada uno y cómo se relacionan.
2. **Las operaciones que implementaste:** Describe brevemente cómo funciona cada operación CRUD.
3. **Capturas de pantalla:** Evidencia visual de tu aplicación funcionando (la lista, el formulario de creación, la edición, la eliminación).

---

## Paso 10 — Comprimir y Entregar

Comprime toda la carpeta del proyecto en un archivo `.zip` o `.rar` y entrégalo junto con tu documento explicativo. (si no se entregan dentro de un .zip o .rar no se pueden reviar por la naturaleza del entorno de evaluacion )

Si entregas un pdf debe estar fuera el repositorio fuera del zip como un archivo aparte, soo los .md van dentro del mismo .zip o .rar que representan el repositorio.

---

---

# ⚠️ Errores Frecuentes que Debes Evitar

| Error                                          | Consecuencia                                                |
| ---------------------------------------------- | ----------------------------------------------------------- |
| Crear modelos pero no aplicar migraciones      | La base de datos no tendrá tablas y la app fallará          |
| Olvidar `on_delete` en las ForeignKey          | Django no te deja crear la migración                        |
| Hacer CRUD solo desde el Admin o el Shell      | El requerimiento pide que funcione desde vistas y templates |
| No incluir el archivo `.sqlite3` en la entrega | El evaluador no podrá ver tus datos de prueba               |
| No incluir capturas de pantalla                | Falta evidencia de funcionamiento                           |
| Poner lógica de base de datos en los templates | Rompe la arquitectura de Django                             |

---

> 📎 **Documento original de la evaluación:**
>
> [Abrir en Google Docs](https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true)
>
> `https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true`

---
