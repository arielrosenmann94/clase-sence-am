# 🐍 Django — Módulo 6 · Clase 6

## Práctica: Mi Curriculum Vitae en Django

---

> _"Antes de escribir una línea de código, el buen desarrollador diseña. Antes de diseñar, pregunta."_

---

## Contexto

Vas a construir tu propio **Curriculum Vitae** como una aplicación web en Django. El resultado final es un sitio que muestra tu información personal, tu experiencia, tus habilidades y cualquier sección que consideres relevante — todo con contenido dinámico, templates con herencia y archivos estáticos.

Pero primero hay que pensar.

---

---

# Fase 1 — Preguntas de diseño

> **No escribas código todavía.** Respondé estas preguntas en papel, en un documento o en el bloc de notas. Las respuestas son la base del proyecto.

---

## 🧠 Sobre el contenido

1. **¿Qué información quieres mostrar en tu CV?**
   Pensá en las secciones clásicas de un curriculum real:
   - ¿Datos personales? ¿Cuáles incluirías y cuáles no?
   - ¿Experiencia laboral? ¿Cómo organizarías cada entrada?
   - ¿Educación? ¿Qué campos tiene cada estudio?
   - ¿Habilidades o tecnologías? ¿Cómo las mostrarías — lista, porcentaje, íconos?
   - ¿Proyectos personales? ¿Tendrías link y descripción?
   - ¿Idiomas? ¿Cómo representarías el nivel?

2. **¿Qué secciones son listas** (muchos ítems que iterar con `{% for %}`) **y cuáles son dato único** (nombre, foto, email)?

3. **¿Qué información vas a mostrar en la página principal?** Haz una lista simple:
   - ¿Qué datos son únicos (uno solo, como tu nombre o tu foto)?
   - ¿Qué datos son una lista (varios ítems, como habilidades o estudios)?

   Ejemplo de lo que podrías escribir:

   > Nombre: dato único | Habilidades: lista de varias | Experiencia: lista con empresa, rol y año

---

## 🏗️ Sobre la estructura del proyecto

4. **¿Cómo vas a llamar a tu proyecto Django y a tu app?**
   Recuerda las convenciones: minúsculas, sin espacios, en inglés si se puede.

5. **¿Qué páginas va a tener el sitio?**
   Pensá en las rutas: `'/'`, `'/habilidades/'`, `'/proyectos/'` — o ¿todo en una sola página?

6. **¿Qué bloques va a necesitar tu `base.html`?**
   Mínimo: `title`, `content`. ¿Necesitás alguno más?

7. **¿Qué archivos estáticos vas a usar?**
   - ¿Una foto de perfil?
   - ¿CSS propio para personalizar el diseño?
   - ¿Algún JS?

---

## 🎨 Sobre el diseño

8. **¿Qué paleta de colores te representa?** Pensá en un color principal y uno de acento.

9. **¿La navegación va a ser un menú con links a secciones o a páginas separadas?**

10. **¿Qué template de Bootstrap vas a usar como punto de partida?** ¿O vas a construir el diseño tú mismo sobre la grilla de Bootstrap?

---

> ✏️ **Tomá nota de todas estas respuestas. El paso siguiente va a pedírtelas.**

---

---

# Fase 2 — Diseño técnico (antes del código)

Con las respuestas de la Fase 1, completa este documento técnico:

---

## Mi diseño

### Nombre del proyecto

```
Proyecto: _______________
App:      _______________
```

### Páginas y rutas

| URL | Vista    | Template      | Descripción                           |
| --- | -------- | ------------- | ------------------------------------- |
| `/` | `inicio` | `inicio.html` | Página principal con datos personales |
|     |          |               |                                       |
|     |          |               |                                       |

### ¿Qué datos va a tener disponibles la página principal?

Escribe en palabras simples qué información va a mostrar esa página. Ejemplo:

```
- Nombre completo (uno solo)
- Título profesional (uno solo)
- Lista de habilidades (varias)
- Lista de experiencias (varias, cada una con empresa, cargo y año)
```

### Estructura del proyecto

```
mi_proyecto/
├── mi_app/
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html
│   └── mi_app/
│       └── inicio.html
├── static/
│   ├── css/
│   ├── images/
│   └── js/
└── manage.py
```

¿Cambiás algo de esta estructura? ¿Por qué?

---

> ✅ **Cuando tengas el diseño claro, pasá a la Fase 3.**

---

---

# Fase 3 — Construcción: El orden lógico del programador

---

> El orden en que se construye una aplicación define cuán fácil será encontrar un error si algo falla. Vamos a seguir el flujo profesional: de afuera hacia adentro (Entorno → Configuración → Rutas → Lógica → Templates).

---

## 1. Preparación del terreno (Entorno)

Antes de crear el primer archivo Django, necesitamos un espacio de trabajo aislado y limpio.

- **1.1** Crea una carpeta exclusiva para este proyecto en tu computadora.
- **1.2** Crea el **entorno virtual (venv)** dentro de esa carpeta.
- **1.3** **Activa** el entorno virtual (verifica que veas el prefijo `(venv)` en tu terminal).
- **1.4** Instala **Django** usando pip.
- **1.5** (Opcional pero recomendado) Crea un archivo `requirements.txt` con la versión de Django instalada.

---

## 2. Los cimientos (Scaffolding)

Ahora generamos la estructura básica que Django necesita para arrancar.

- **2.1** Crea el **proyecto** Django (recuerda usar el punto `.` al final para no crear carpetas extra).
- **2.2** Crea la **aplicación** específica para tu CV.
- **2.3** Registra tu nueva app en el archivo `settings.py` (sección `INSTALLED_APPS`).
- **2.4** Ejecuta tu primer `runserver` para verificar que la página de bienvenida de Django aparece correctamente.

---

## 3. Configuración del motor (Settings)

Antes de programar las vistas, preparamos el proyecto para manejar archivos y plantillas.

- **3.1** Configura la variable `STATIC_URL` y añade `STATICFILES_DIRS` para decirle a Django dónde vas a guardar tu CSS e imágenes.
- **3.2** Configura la carpeta global de `TEMPLATES` en el diccionario `TEMPLATES` dentro de `settings.py` para poder usar un `base.html` centralizado.
- **3.3** Crea físicamente las carpetas `static/` (con sus subcarpetas `css/` e `images/`) y la carpeta `templates/` en la raíz del proyecto.

---

## 4. El sistema de navegación (Routing)

Definimos las "direcciones" de nuestro sitio.

- **4.1** En el `urls.py` del **proyecto**, usa la función `include` para derivar las rutas hacia tu aplicación.
- **4.2** Crea el archivo `urls.py` dentro de tu **aplicación**.
- **4.3** Registra la ruta vacía `''` en el `urls.py` de la app y asígnale un nombre (`name='inicio'`).

---

## 5. El cerebro de la operación (Views & Logic)

Aquí es donde defines qué datos va a tener tu CV. Recuerda que en esta fase no usamos base de datos todavía.

- **5.1** Crea una función en `views.py` para tu página principal.
- **5.2** Dentro de la función, crea un diccionario llamado `contexto`.
- **5.3** Llena ese diccionario con toda la información de tu CV (nombre, título, lista de habilidades, lista de experiencias, etc.).
- **5.4** Haz que la función retorne un `render` que use tu template y le pase este diccionario.

---

## 6. La cara visible (Templates & Static)

Finalmente, armamos lo que el usuario va veamos.

- **6.1** Crea `base.html`. Debe tener la estructura HTML5 completa, el CDN de Bootstrap, un Navbar, un Footer y al menos dos bloques (`title` y `content`).
- **6.2** Crea el template `inicio.html`. Lo primero que debe hacer es usar `{% extends %}` para heredar de `base.html`.
- **6.3** Dentro del bloque de contenido, usa las variables de tu contexto `{{ variable }}` para mostrar la información.
- **6.4** Usa etiquetas `{% for %}` para recorrer tus listas de habilidades o proyectos.
- **6.5** Usa etiquetas `{% if %}` para mostrar información solo si existe (por ejemplo, redes sociales o foto).
- **6.6** Carga tus archivos estáticos: usa `{% load static %}` al principio del archivo y la etiqueta `{% static %}` para tu CSS y tu foto de perfil.

---

## 7. Pulido y Verificación

- **7.1** Verifica que todos los links del Navbar usen la etiqueta `{% url %}`.
- **7.2** Crea un archivo CSS personalizado para ajustar colores y márgenes que Bootstrap no cubra.
- **7.3** Crea un template para el error 404 y configura `settings.py` para probarlo (temporalmente con `DEBUG = False`).
- **7.4** Revisa el CV en modo celular. ¿Es responsivo? Asegúrate de usar las clases de grilla de Bootstrap (`container`, `row`, `col`).

---

---

# Criterios de evaluación

| Criterio                  | Descripción                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| ✅ Herencia de templates  | `base.html` con bloques, templates hijos que lo extienden         |
| ✅ Contenido dinámico     | Contexto con datos reales pasado desde la vista                   |
| ✅ Estructuras de control | Al menos un `{% if %}` y un `{% for %}` funcionales               |
| ✅ Archivos estáticos     | Bootstrap + CSS propio + al menos una imagen con `{% static %}`   |
| ✅ Navegación             | Todos los links con `{% url %}`, sin URLs hardcodeadas            |
| ✅ Diseño                 | El CV tiene coherencia visual y muestra la información claramente |
| ✅ Sin errores            | El servidor corre sin excepciones                                 |

---

## Preguntas de cierre — para pensar después de terminar

- ¿Qué sección te costó más? ¿Por qué?
- ¿Cómo agregarías una segunda página de "Proyectos" sin repetir el navbar y el footer?
- Si quisieras que los datos del CV fueran editables desde el admin de Django sin tocar el código, ¿qué cambiarías?
- ¿Qué parte del diseño pasarías a JavaScript si el CV tuviese formulario de contacto?

---

> _"Un portfolio bien hecho es la primera muestra de tu trabajo como desarrollador. Quien lo ve, no solo lee tu experiencia — ve cómo pensás y cómo construís."_

---
