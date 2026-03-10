# 🏁 Django — Módulo 6 · Cierre de Unidad

## Semanas 1 y 2 — Todo lo que construiste

---

> _"No aprendiste comandos. Aprendiste a pensar como una computadora que sirve a personas."_

---

---

# PARTE I — EL MAPA DE ARCHIVOS DE DJANGO

---

> En un proyecto Django cada archivo tiene una única responsabilidad. Este es el mapa completo.

---

## Archivos del proyecto (la carpeta raíz)

| Archivo            | Qué es                                                                                                                    | Cuándo se usa                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `manage.py`        | El punto de entrada de todos los comandos de Django. Conecta tu terminal con el proyecto.                                 | Siempre: para correr el servidor, migraciones, crear usuarios, abrir el shell.          |
| `requirements.txt` | Lista de todas las librerías que el proyecto necesita para funcionar, con sus versiones exactas. `pip freeze > requirements.txt`                        | Al compartir el proyecto o desplegarlo en producción: `pip install -r requirements.txt` |
| `.env`             | Archivo de variables de entorno que guarda información sensible: claves secretas, contraseñas de base de datos, API keys. | Siempre en producción. Nunca se sube al repositorio (está en `.gitignore`).             |
| `db.sqlite3`       | La base de datos del proyecto en desarrollo. Un archivo binario que SQLite gestiona automáticamente.                      | Solo en desarrollo local. En producción se reemplaza por PostgreSQL u otro motor.       |

---

## Archivos de configuración (`config/` o el directorio del proyecto)

| Archivo       | Qué es                                                                                                                   | Cuándo se usa                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `settings.py` | El cerebro de la configuración. Define apps instaladas, base de datos, templates, idioma, zona horaria, seguridad y más. | Al inicio del proyecto y cada vez que se agrega una app, una librería o cambia la config. |
| `urls.py`     | El directorio telefónico del proyecto. Asocia cada URL con la vista que la maneja.                                       | Al agregar cualquier nueva URL o incluir las URLs de una app nueva.                       |
| `wsgi.py`     | Interfaz entre el servidor web y el proyecto Django para producción tradicional (sincrónica).                            | En producción al desplegar en servidores como Gunicorn o uWSGI.                           |
| `asgi.py`     | Interfaz asíncrona para Django 3+. Permite manejar WebSockets, HTTP/2 y alta concurrencia.                               | En producción con servidores como Uvicorn o Daphne para apps con tiempo real.             |

---

## Archivos de cada app

| Archivo                 | Qué es                                                                                                                       | Cuándo se usa                                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `models.py`             | Define la estructura de los datos: qué tablas existen, qué columnas tienen y cómo se relacionan entre sí.                    | Al diseñar el sistema de datos. Cada cambio requiere `makemigrations` y `migrate`.                       |
| `views.py`              | La lógica de cada página. Recibe la solicitud HTTP, consulta datos y decide qué responder: HTML, JSON o redirección.         | Al crear cualquier nueva página o endpoint de la aplicación.                                             |
| `urls.py`               | El directorio de URLs de la app. Define qué URL lleva a qué vista dentro de esta app específicamente.                        | Al agregar vistas nuevas. Se incluye en el `urls.py` del proyecto con `include()`.                       |
| `admin.py`              | Registra los modelos en el panel administrativo y configura cómo se presentan: columnas, filtros, buscadores, inlines.       | Al querer gestionar un modelo desde el panel. También para personalizar su apariencia.                   |
| `forms.py`              | Define formularios HTML con validación en Python: campos, reglas de validación, mensajes de error y procesamiento del POST.  | Al necesitar formularios personalizados. Los `ModelForm` generan el formulario desde el modelo.          |
| `serializers.py`        | Convierte objetos Python (modelos) a formatos de intercambio como JSON o XML, y viceversa. Exclusivo de APIs REST.           | Al construir una API con Django REST Framework para que otras apps consuman los datos.                   |
| `signals.py`            | Funciones que se ejecutan automáticamente cuando ocurre un evento en la base de datos, sin modificar la vista que lo causó.  | Para auditoría, notificaciones, sincronización o efectos secundarios desacoplados.                       |
| `apps.py`               | Configura la aplicación: su nombre, su campo auto-generado por defecto y el método `ready()` para activar signals y hooks.   | Al activar signals o al personalizar el comportamiento de carga de la app.                               |
| `tests.py`              | Pruebas automatizadas que verifican que las vistas, modelos y formularios se comportan como se espera.                       | En proyectos profesionales: cada vez que se agrega una funcionalidad nueva.                              |
| `middleware.py`         | Código que intercepta cada request antes de llegar a la vista y cada response antes de salir. Opera como un filtro global.   | Para logging, autenticación personalizada, cabeceras de seguridad o rate limiting.                       |
| `context_processors.py` | Funciones que agregan variables al contexto de todos los templates automáticamente, sin pasarlas desde cada vista.           | Para variables globales: usuario activo, configuración del sitio, mensajes del sistema.                  |
| `managers.py`           | Clases que extienden el ORM para agregar consultas personalizadas y reutilizables al modelo.                                 | Al necesitar consultas complejas o repetidas: `Producto.objects.disponibles()`.                          |
| `mixins.py`             | Clases que encapsulan comportamiento reutilizable para agregar a vistas de clase mediante herencia múltiple.                 | Al necesitar verificaciones o comportamiento compartido entre múltiples vistas.                          |
| `permissions.py`        | Define clases de permisos personalizados para DRF o para vistas de clase, más granulares que los permisos nativos de Django. | En APIs REST al necesitar reglas de acceso que los permisos automáticos no cubren.                       |
| `validators.py`         | Funciones que validan un valor específico y lanzan `ValidationError` si no cumple las reglas del negocio.                    | Al necesitar validaciones personalizadas en campos de modelos o formularios.                             |
| `utils.py`              | Funciones auxiliares que no pertenecen a ninguna capa específica: formateo de texto, cálculos, helpers generales.            | Al tener lógica utilitaria que se repite en varias partes del proyecto.                                  |
| `tasks.py`              | Tareas asíncronas que se ejecutan en segundo plano, fuera del ciclo de la request HTTP.                                      | Para enviar emails, procesar archivos, llamar APIs externas: con Celery o `background_task` en Django 6. |
| `exceptions.py`         | Define excepciones personalizadas del proyecto para comunicar errores de negocio de forma clara y específica.                | When the default Django/DRF exceptions don't express the domain error clearly enough.                    |

---

## Carpetas especiales

| Carpeta         | Qué contiene                                                                                                          | Cuándo se usa                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `migrations/`   | Archivos generados automáticamente que describen cada cambio al esquema de la base de datos, en orden cronológico.    | Se genera sola con `makemigrations`. Nunca se edita a mano.                               |
| `templates/`    | Archivos HTML que use el sistema de templates de Django. Pueden extender otros templates o incluir partiales.         | Al crear cualquier página visible. Se puede tener una global y una por app.               |
| `static/`       | Archivos CSS, JavaScript e imágenes que el navegador descarga directamente, sin pasar por Django.                     | Para el diseño visual del proyecto. En producción se sirven con `whitenoise` o un CDN.    |
| `media/`        | Archivos subidos por los usuarios: fotos de perfil, documentos, imágenes de productos.                                | Al usar `ImageField` o `FileField` en un modelo. Requiere configuración en `settings.py`. |
| `fixtures/`     | Archivos JSON o YAML con datos de prueba o iniciales que se pueden cargar en la base de datos con un comando.         | Para poblar la BD en desarrollo o para pruebas automatizadas con datos consistentes.      |
| `management/`   | Comandos personalizados de Django que se corren con `python manage.py mi_comando`.                                    | Para tareas de mantenimiento, carga de datos o automatizaciones propias del proyecto.     |
| `templatetags/` | Filtros y tags personalizados para el Django Template Language, que se usan con `{% load mi_tag %}` en los templates. | Al necesitar transformaciones de datos o lógica de presentación reutilizable en HTML.     |

---

---

# PARTE II — MÁS ALLÁ DEL CÓDIGO

---

> Lo siguiente no entra en ningún examen. Pero es quizás lo más importante de todo el módulo.

---

## Lo que realmente aprendiste en estas dos semanas

Aprendiste comandos. Aprendiste sintaxis. Aprendiste qué archivos van dónde.

Pero eso no es lo que te va a diferenciar.

Lo que te va a diferenciar es algo que este módulo te enseñó sin nombrarlo: **pensar en términos de responsabilidades**.

Cada archivo de Django existe porque alguien decidió que una parte del sistema no debería saber demasiado sobre las otras. El modelo no sabe que existe el template. La vista no sabe cómo está guardado el dato en la base de datos. El admin no sabe qué vistas públicas existen.

Esa separación no es un capricho técnico. Es una **ética del código**.

Un sistema donde todas las partes están mezcladas es un sistema donde nadie puede trabajar sin romper algo. Un sistema bien separado es un sistema donde varias personas pueden trabajar en paralelo, con confianza, sin pisarse.

> Programar bien no es escribir código que funciona. Es escribir código que el próximo desarrollador puede entender, modificar y mejorar — incluso si ese próximo desarrollador sos tú mismo en seis meses.

---

## El admin de Django como declaración de valores

El panel de administración de Django existe porque sus creadores creyeron algo específico: **las personas que administran datos no deberían depender de los desarrolladores para hacer su trabajo**.

Antes de que existieran herramientas como el admin de Django, el flujo era así:

```
El administrador necesita actualizar un dato
         ↓
Le pide al desarrollador
         ↓
El desarrollador abre la base de datos
         ↓
Ejecuta el cambio a mano
         ↓
El administrador espera
```

Ese flujo tiene un problema de poder: una persona no puede hacer su trabajo sin la intermediación de otra. El admin de Django rompe esa dependencia. Le devuelve autonomía a quien administra los datos.

Cuando configurás correctamente el panel — con los permisos correctos, el acceso correcto para cada persona — estás haciendo algo más que programar. **Estás diseñando quién puede hacer qué, y quién no necesita pedir permiso para hacer su trabajo.**

Eso es diseño de sistemas. Y el diseño de sistemas es, en última instancia, diseño social.

---

## Los permisos como arquitectura de confianza

Un sistema sin permisos no es un sistema libre. Es un sistema inseguro.

Cuando defines que María puede editar pero no eliminar, que el grupo "Editores" puede ver pero no crear, que solo el superusuario puede cambiar contraseñas — estás construyendo **arquitectura de confianza**.

No es desconfianza en las personas. Es claridad sobre las responsabilidades.

Un médico en un hospital puede ver la historia clínica de sus pacientes. No puede ver la de los pacientes de otros médicos. No porque se desconfíe de él — sino porque la privacidad de un paciente es un derecho, y ese derecho se garantiza con código, no con buenas intenciones.

Los permisos en Django son exactamente eso: **derechos codificados**.

---

## Lo que distingue a un developer de un programador

Un **programador** escribe código que resuelve el problema de hoy.

Un **developer** escribe código que el equipo puede modificar mañana.

La diferencia no está en cuántas líneas escribe ni qué tan rápido. Está en qué tan bien entiende que el código es una herramienta de comunicación — no solo con la computadora, sino con los demás humanos que van a trabajar sobre ese mismo sistema.

El modelo separa los datos de la lógica. La vista separa la lógica de la presentación. El template separa la presentación del contenido. Las signals separan los efectos secundarios de las acciones que los causan.

Todo eso es **comunicación**. Comunicación de qué hace cada parte. Comunicación de dónde empieza una responsabilidad y dónde termina otra.

> Cuando terminás un módulo como este, no solo sabes más Django. Sabes pensar con más claridad sobre cómo las partes de un sistema se relacionan. Y esa habilidad — la de ver sistemas, no solo código — es la que se busca en el mundo profesional.

---

## El error que todos cometen al principio

Todos los developers novatos, sin excepción, comentan el mismo error: **poner demasiada lógica en el lugar equivocado**.

Lógica de negocio en el template. Consultas SQL en la vista. Validaciones en el modelo cuando deberían estar en el formulario. Todo junto, en el lugar más conveniente para el momento, sin pensar en el mañana.

No es culpa de nadie. Es la forma natural en que aprendemos: lo que funciona hoy tiene prioridad sobre lo que va a ser mantenible en seis meses.

La madurez como developer es el proceso de invertir esa prioridad. De empezar a preguntarte _"¿dónde corresponde que viva este código?"_ antes de preguntarte _"¿cómo hago que funcione?"_

Este módulo fue el primer paso en ese proceso.

---

## Una pregunta para llevarse

Al final de estas dos semanas, hay una sola pregunta que vale la pena hacerse:

> **¿Cuánto trabajo le haría falta a alguien que no vi nunca para entender, modificar y mejorar el código que escribe?**

Si la respuesta es "mucho" — sigue aprendiendo a separar responsabilidades.
Si la respuesta es "poco" — sigues en el camino correcto.

Ese número — el esfuerzo que le cuesta a otro entender lo que hiciste — es la medida real de la calidad de un sistema. No la velocidad. No la cantidad de líneas. No la elegancia del código. El esfuerzo del próximo.

Que ese número sea siempre lo más bajo posible.

---

> _"El mejor código que puedes escribir es el que no necesita explicación. El segundo mejor es el que tiene la explicación exacta donde tiene que estar."_

---
