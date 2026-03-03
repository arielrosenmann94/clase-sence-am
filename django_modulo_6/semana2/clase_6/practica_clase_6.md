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

# Fase 3 — Construcción paso a paso

> Las instrucciones son intencionalmente breves. Usá lo que saben, la documentación y el error como guía.

---

**1.** Crea una carpeta para el proyecto en tu computadora.

**2.** Crea el entorno virtual dentro de esa carpeta.

**3.** Activa el entorno virtual.

**4.** Instala Django.

**5.** Verifica que la instalación fue correcta.

**6.** Crea el proyecto Django con el nombre que definiste en la Fase 2.

**7.** Crea la app con el nombre que definiste en la Fase 2.

**8.** Registrá la app en `settings.py`.

**9.** Configura los archivos estáticos en `settings.py` — las tres variables necesarias.

**10.** Configura la carpeta de templates en `settings.py`.

**11.** Crea la estructura de carpetas: `templates/`, `static/css/`, `static/images/`.

**12.** Crea `base.html` con la estructura base, Bootstrap vía CDN y los bloques que definiste en el diseño. El navbar debe tener links a todas las páginas que diseñaste.

**13.** Crea la vista principal en `views.py` con el contexto que diseñaste en la Fase 2.

**14.** Crea el archivo `urls.py` de la app y registrá la ruta principal.

**15.** Incluí las URLs de la app en el `urls.py` del proyecto.

**16.** Crea `inicio.html` — que extienda `base.html` y muestre los datos del contexto con variables, `{% if %}` y `{% for %}` donde corresponda.

**17.** Verifica que el servidor corre sin errores: `python manage.py runserver`.

**18.** Haz que al menos una sección use `{% for %}` para iterar sobre una lista (habilidades, proyectos, experiencia).

**19.** Haz que al menos una sección use `{% if %}` para mostrar u ocultar algo según una condición.

**20.** Añadí una imagen (foto de perfil u otra) usando `{% static %}` y `{% load static %}`.

**21.** Crea un archivo CSS propio en `static/css/` y aplicale al menos 3 estilos personalizados que complementen Bootstrap.

**22.** Asegúrate de que todos los links del navbar usen `{% url %}` con el nombre de la URL — ningún link hardcodeado.

**23.** Crea una página `404.html` que extienda `base.html` y muestre un mensaje amigable.

**24.** Navega a una URL inexistente para ver qué muestra Django. ¿Qué configuraría para que aparezca tu 404 personalizado?

**25.** Revisa el resultado en el navegador. ¿El diseño refleja lo que pensaste en la Fase 1?

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
