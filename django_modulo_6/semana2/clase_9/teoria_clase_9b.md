# 🔀 Django — Módulo 6 · Clase 9b

## Cómo trabaja un programador profesional hoy

---

> _"El código que escribes es solo el 30% del trabajo. El otro 70% es cómo lo organizas, versionas y comunicas."_

---

## ¿De qué trata esta clase?

Un developer en el mundo real no trabaja solo ni en forma lineal.
Trabaja en paralelo con otros, con herramientas que le ayudan a pensar, y con un sistema de control de versiones que actúa como red de seguridad.

Esta clase cubre el ciclo completo:

```
Entender la tarea
      ↓
Abrir una rama
      ↓
Escribir código con ayuda de IA
      ↓
Hacer commits con sentido
      ↓
Push y Pull Request
      ↓
Review y merge
      ↓
Volver a empezar
```

---

---

# Parte I — Git y GitHub: la diferencia

---

> Mucha gente los confunde. Son herramientas distintas con roles distintos.

---

## Git

**Git** es un programa que vive en tu computadora.
Registra los cambios en el código a lo largo del tiempo.

```
tu computadora
   └── git → guarda historial de cambios localmente
```

No necesita internet. No necesita otros.
Funciona aunque estés solo.

## GitHub

**GitHub** es una plataforma web donde se sube ese historial.
Permite colaborar, revisar código, abrir issues y trabajar en equipo.

```
tu computadora (git)
       ↓ push
   GitHub (repositorio remoto)
       ↓ pull
otras computadoras (git de tus compañeros)
```

**Analogía:**
Git es el cuaderno donde anotás los cambios.
GitHub es el servidor donde todos tienen acceso a ese cuaderno.

---

---

# Parte II — El flujo base de trabajo

---

> Antes de escribir código, hay un ritual. No es burocracia — es lo que evita conflictos y pérdida de trabajo.

---

## El flujo completo paso a paso

### Paso 1 — Siempre partir de `main` actualizada

Antes de empezar cualquier tarea nueva:

```bash
git checkout main           # cambiarse a la rama principal
git pull origin main        # descargar los últimos cambios del servidor
```

**¿Por qué?** Si otros hicieron cambios mientras trabajabas en otra cosa,
tu `main` local puede estar desactualizada. Partir de código viejo = conflictos asegurados.

---

### Paso 2 — Crear una rama para la tarea

```bash
git checkout -b feature/login-page
#             ↑ crea la rama Y se cambia a ella en un solo comando
```

Cada tarea tiene su propia rama. No se trabaja directamente sobre `main`.

---

### Paso 3 — Escribir el código

Aquí entra el trabajo real: editar archivos, probar en el browser, iterar.

---

### Paso 4 — Ver qué cambió

```bash
git status      # qué archivos cambiaron
git diff        # ver las líneas exactas que cambiaron
```

Antes de hacer un commit, revisar qué está por guardarse.

---

### Paso 5 — Agregar los archivos al commit

```bash
git add nombre_del_archivo.py    # agregar un archivo específico
git add .                        # agregar TODOS los archivos modificados
```

**Recomendación profesional:** preferir `git add nombre_archivo` en lugar de `git add .`
para ser consciente de exactamente qué va en cada commit.

---

### Paso 6 — Hacer el commit

```bash
git commit -m "feat: agrega formulario de login con validación"
```

---

### Paso 7 — Subir la rama a GitHub

```bash
git push origin feature/login-page
```

---

### Paso 8 — Abrir un Pull Request en GitHub

Desde la interfaz de GitHub, se abre un PR (Pull Request):
se propone mergear `feature/login-page` → `main`.
El equipo revisa el código, sugiere cambios, aprueba.

---

### Paso 9 — Merge y limpieza

Una vez aprobado y mergeado:

```bash
git checkout main
git pull origin main          # actualizar local con el merge
git branch -d feature/login-page   # opcional: borrar la rama local
```

---

---

# Parte III — Cómo nombrar las ramas

---

> No todos los equipos llaman las ramas igual. Lo que importa no es el formato exacto, sino tener uno y que todos lo usen.

---

## Por qué importa el nombre

El nombre de una rama es la primera información que tiene el equipo sobre qué se está construyendo.
Un buen nombre evita preguntas. Un nombre malo genera confusión y errores de merge.

---

## Las corrientes más comunes en la industria

Hay varias convenciones usadas en proyectos reales. Cada una tiene su lógica.
Lo más probable es que en distintos empleos o proyectos open source veas variantes de estas.

---

### Corriente 1 — `tipo/descripcion` (la más extendida)

La que más se ve hoy en proyectos modernos y en documentación de Git.

```
tipo/descripcion-en-kebab-case
```

```bash
feature/login-con-google
fix/precio-negativo-en-carrito
hotfix/token-jwt-expirado
refactor/vistas-de-autenticacion
chore/actualizar-dependencias
docs/guia-de-instalacion
test/cobertura-de-permisos
```

**Prefijos más comunes:**

| Prefijo     | Uso                                            |
| ----------- | ---------------------------------------------- |
| `feature/`  | Funcionalidad nueva                            |
| `fix/`      | Corrección de bug                              |
| `hotfix/`   | Bug crítico en producción que no puede esperar |
| `refactor/` | Mejorar código sin cambiar comportamiento      |
| `chore/`    | Mantenimiento: deps, CI, configuraciones       |
| `docs/`     | Solo documentación                             |
| `test/`     | Solo tests                                     |
| `backup/`   | Para respaldos en desarrolo                    |

**Variante con número de ticket:** muchos equipos incluyen el ID del issue o tarjeta:

```bash
feature/123-login-con-google       # 123 = número de issue en GitHub
fix/JIRA-456-precio-negativo       # JIRA-456 = ticket en Jira
```

Esto permite trazar directamente de la rama al ticket de trabajo.

---

### Corriente 2 — Solo el nombre del feature (sin prefijo)

Más simple, usada en proyectos pequeños o equipos que ya tienen todo claro por el contexto.

```bash
login-con-google
precio-negativo-carrito
jwt-expiration-fix
```

**Ventaja:** más corto, menos burocrático.
**Desventaja:** no se puede distinguir a simple vista si es una feature, un fix o un refactor.

---

### Corriente 3 — `nombreapellido/tipo-descripcion` (por developer)

Usada en equipos donde varias personas trabajan en paralelo sobre las mismas áreas.
El nombre de la persona va primero — así al listar las ramas en GitHub se agrupan por developer.

```bash
pedrorojas/feature-login-personalizado
marialopez/fix-precio-carrito
juangarcia/refactor-autenticacion
```

Algunos equipos combinan esta corriente con la de tipo/descripción:

```bash
pedrorojas/feature/login-personalizado    # nombre + tipo + descripción
marialopez/fix/precio-negativo-carrito
```

Y otros la simplifican con solo iniciales:

```bash
pr/feature-login-personalizado    # pr = Pedro Rojas
ml/fix-carrito
```

**Ventaja:** al listar ramas en GitHub, se ven agrupadas por developer — útil en equipos de 5+ personas.
**Desventaja:** si Pedro termina y otra persona toma la tarea, el nombre de rama queda desactualizado.
**¿Cuándo usarla?** Cuando el equipo es grande y varios developers trabajan en la misma app al mismo tiempo.

---

### Corriente 4 — GitFlow (proyectos enterprise o con releases planificados)

GitFlow es un modelo más complejo con ramas de larga duración y un flujo definido.
Se ve en empresas grandes con ciclos de release bloqueados.

```
main           ← producción (solo código estable y taggeado)
develop        ← integración continua de features
feature/...    ← una rama por feature, sale de develop
release/1.2.0  ← preparación de un release (bug fixes finales)
hotfix/...     ← sale de main, se mergea a main Y a develop
```

```bash
git checkout develop
git checkout -b feature/login-con-google   # sale de develop, no de main
# ... trabajo ...
git checkout develop
git merge feature/login-con-google         # se integra a develop
```

**¿Cuándo se usa GitFlow?**

- Equipos con múltiples versiones en producción al mismo tiempo
- Software con releases formales (ej: apps móviles, librerías con semver)
- Empresas con QA y ambientes de staging separados

**¿Cuándo NO usar GitFlow?**

- Proyectos web con deploys frecuentes (todos los días o varias veces al día)
- Equipos chicos que no necesitan múltiples versiones en paralelo
- Startups donde la velocidad es prioritaria

---

### Corriente 5 — Trunk-based development (la corriente más moderna)

Opuesto a GitFlow. Las ramas viven muy poco tiempo — horas, no días.

```bash
git checkout -b feat/login   # rama de vida corta: máximo 1-2 días
# ... trabajo mínimo e incremental ...
git push origin feat/login
# PR → review rápida → merge → borrar rama
```

**Principio clave:** commit pequeño, merge rápido, nunca acumular trabajo.
**Ventaja:** menos conflictos de merge, integración continua real.
**Desventaja:** requiere feature flags y disciplina alta del equipo.

---

## ¿Cuál usar?

| Contexto                             | Recomendación                                     |
| ------------------------------------ | ------------------------------------------------- |
| Primer proyecto propio o freelance   | `tipo/descripcion` — simple y clara               |
| Equipo chico, deploy frecuente       | `tipo/descripcion` o trunk-based                  |
| Enterprise con releases planificados | GitFlow                                           |
| Equipo con Jira o sistema de tickets | `tipo/TICKET-descripcion`                         |
| Open source con muchos contributors  | `tipo/descripcion`, a veces `usuario/descripcion` |

**La regla que aplica siempre sin importar la corriente:**

```
Lo importante no es EL formato. Es que TODOS en el equipo usen EL MISMO.
Un equipo con convención propia > un equipo sin convención.
```

---

## La convención que vamos a usar en este curso

Para los proyectos de este módulo usamos:

```
tipo/descripcion-en-kebab-case
```

Con estos prefijos:

```bash
feature/  →  funcionalidad nueva
fix/      →  corrección de bug
refactor/ →  mejora de código existente
docs/     →  documentación
test/     →  tests
```

---

## ¿Cuándo crear una rama nueva?

Una rama por tarea. Siempre.

| Situación                 | Acción                                            |
| ------------------------- | ------------------------------------------------- |
| Feature nueva             | `git checkout -b feature/nombre-feature`          |
| Bug reportado             | `git checkout -b fix/descripcion-bug`             |
| Bug urgente en producción | `git checkout -b hotfix/descripcion` desde `main` |
| Refactorización           | `git checkout -b refactor/que-se-refactoriza`     |
| Dos tareas a la vez       | Dos ramas distintas — nunca mezclar               |

**Una rama = una tarea.**
Si en la misma rama hay "agrego login" y "arreglo el bug del carrito" → nadie puede hacer review por separado, nadie puede revertir uno sin el otro.

---

---

# Parte IV — Cómo y cuándo hacer commits

---

> Un commit es una foto del código en un momento. Si se hacen bien, el historial cuenta la historia del proyecto.

---

## La regla principal

**Un commit = un cambio lógico completo.**

No importa el tamaño. Importa que tenga sentido solo.

```
✅ "feat: agrega modelo de Producto con sus campos"
✅ "fix: corrige validación del campo precio (no acepta negativos)"
✅ "test: agrega test para editar Producto sin permiso"

❌ "cambios"
❌ "wip"
❌ "arreglos varios"
❌ "jajaja"
```

---

## Cuándo hacer un commit

No hay una respuesta de tiempo ("cada hora", "cada X líneas").
La respuesta correcta es: **cuando el código está en un estado estable con un cambio concreto.**

| Momento para comittear                             | Momento para NO comittear           |
| -------------------------------------------------- | ----------------------------------- |
| El modelo nuevo está completo y la migración corre | El código tiene errores de sintaxis |
| El formulario valida y guarda correctamente        | La feature está a medias            |
| El bug está corregido y los tests pasan            | "Voy a almorzar, guardo lo que hay" |
| Agregué un test que cubre el caso nuevo            | Código comentado que se va a borrar |

**Frecuencia recomendada para principiantes:** al menos un commit por sesión de trabajo,
pero idealmente uno cada vez que completás una pieza funcional (un modelo, una vista, un template, un test).

---

## El formato de Conventional Commits

El estándar de la industria para escribir mensajes de commit:

```
tipo(scope): descripcion breve en presente

[cuerpo opcional — más detalle si es necesario]

[footer opcional — referencia a issue: Closes #42]
```

### Los tipos

| Tipo       | Qué cambió                                      |
| ---------- | ----------------------------------------------- |
| `feat`     | Nueva funcionalidad                             |
| `fix`      | Corrección de bug                               |
| `docs`     | Documentación                                   |
| `style`    | Formateo (espacios, comas) sin cambio de lógica |
| `refactor` | Código mejorado sin cambiar el comportamiento   |
| `test`     | Agregar o corregir tests                        |
| `chore`    | Tareas de mantenimiento (deps, configs, CI)     |

### Ejemplos reales

```bash
git commit -m "feat(auth): agrega vista de login con LoginView"
git commit -m "fix(auth): corrige redirección al 403 cuando no hay sesión"
git commit -m "feat(productos): agrega modelo Producto y migración"
git commit -m "test(productos): agrega test de creación de Producto"
git commit -m "docs: agrega README con instrucciones de instalación"
git commit -m "chore: actualiza Django a 5.1.2"
```

### El scope (entre paréntesis)

El scope es opcional pero ayuda muchísimo en proyectos grandes.
Dice en qué parte del sistema se hizo el cambio:

```bash
feat(auth):      → cambio en la autenticación
fix(carrito):    → corrección en el carrito de compras
test(api):       → test en la capa de API
```

---

## Lo que NO se commitea nunca

```bash
# .gitignore — estos archivos nunca deben subir a GitHub
.env              # variables de entorno con contraseñas y claves
__pycache__/      # archivos compilados de Python
*.pyc             # bytecode
db.sqlite3        # base de datos local (en desarrollo)
media/            # archivos subidos por usuarios (van en S3 o similar)
venv/             # entorno virtual — cada developer instala el suyo
node_modules/     # dependencias de frontend
.DS_Store         # metadatos de macOS
```

**Si alguien sube el `.env` a GitHub con contraseñas reales → seguridad comprometida.**
Esto ocurre más seguido de lo que parece y es una de las causas más comunes de brechas de seguridad en proyectos pequeños.

---

---

# Parte V — Cómo se trabaja con IA hoy

---

> La IA no reemplaza al developer — amplifica lo que ya sabe.

---

## El flujo con IA integrada

```
Tarea clara
    ↓
Pensar el diseño (qué modelo, qué vista, qué lógica)
    ↓
Pedirle a la IA que genere el esqueleto
    ↓
Leer, entender y ajustar el código generado
    ↓
Probar en el proyecto real
    ↓
Comittear lo que funciona, con un mensaje descriptivo
```

**El developer sigue siendo responsable de entender lo que commitea.**
Un commit con código que no se entiende es una deuda técnica futura.

---

## Cómo hacer buenos prompts para generar código

La diferencia entre un prompt vago y uno preciso es enorme:

```
❌ Vago:
"Dame código de login en Django"

✅ Preciso:
"Necesito una vista de login en Django usando LoginView de django.contrib.auth.views,
con un template que extiende base.html, que incluya el campo hidden 'next',
y que después del login exitoso redirija a /dashboard/. Usamos Bootstrap 5."
```

**Cuanta más contexto, mejor el resultado.**
Los prompts buenos incluyen: framework, versión, qué ya existe, qué restricciones hay, qué se espera como resultado.

---

## Lo que la IA hace bien y lo que no

| La IA hace bien                        | La IA falla frecuentemente en            |
| -------------------------------------- | ---------------------------------------- |
| Esqueletos CRUD completos              | Lógica de negocio compleja del dominio   |
| Templates con HTML/CSS                 | Tests que cubren edge cases reales       |
| Explicar conceptos                     | El estado actual de TU base de datos     |
| Traducir entre lenguajes               | Bugs que dependen de datos de producción |
| Refactorizar código dado               | Decisiones arquitectónicas a largo plazo |
| Escribir tests a partir de código dado | Qué es lo correcto para TU negocio       |

---

## La IA y Git: el error más común

```
❌ Ciclo incorrecto:
1. Pedir código a la IA
2. Pegar el código
3. Funciona (o no)
4. Commitear "cambios de IA"

✅ Ciclo correcto:
1. Entender qué hay que hacer
2. Pedir a la IA el esqueleto
3. Leer y ajustar el código
4. Probar que funciona
5. Comittear con un mensaje descriptivo de LO QUE HACE el código
```

El mensaje del commit no describe cómo se generó el código sino qué hace.

---

---

# Parte VI — Pull Requests y Code Review

---

> Un PR no es solo "subir código". Es comunicar qué cambiaste y por qué.

---

## Qué es un Pull Request

Un PR es una propuesta formal para incorporar los cambios de una rama a `main`.
Antes de mergear, el equipo (o el mismo developer en proyectos chicos) revisa el código.

```
feature/login-page
        ↓
    [ Pull Request ]
        ↓
   Code Review
        ↓
    Correcciones (si las hay)
        ↓
    Aprobado → Merge → main
```

---

## Cómo escribir un buen PR

Un buen PR tiene:

```markdown
## ¿Qué hace este PR?

Agrega la vista de login usando LoginView de Django,
con template propio y redirección a /dashboard/ tras el login.

## ¿Por qué se hizo así?

Se usó LoginView en lugar de una vista manual para aprovechar
el manejo de sesiones y CSRF que ya tiene Django.

## Cómo probarlo

1. Ir a /login/
2. Ingresar usuario y contraseña válidos
3. Verificar que redirige a /dashboard/
4. Verificar que con credenciales incorrectas muestra el error
```

---

## Code Review: qué buscar

| En el review, revisar                              | No revisar                                 |
| -------------------------------------------------- | ------------------------------------------ |
| ¿El código hace lo que dice el PR?                 | El estilo personal del developer           |
| ¿Hay edge cases no manejados?                      | Si usaría otra librería "mejor"            |
| ¿Hay datos sensibles hardcodeados?                 | Cosas que no afectan al funcionamiento     |
| ¿Los tests cubren el caso principal?               | La forma de escribir variables si es clara |
| ¿Hay una `PermissionDenied` sin `@login_required`? | —                                          |

---

---

# Parte VII — El programador que quieras ser

---

> El código se aprende. El criterio también.
> La diferencia entre alguien que sabe programar y alguien que trabaja bien en un equipo
> no está en cuánto código escriben — está en cómo lo organizan, cómo lo documentan
> y cómo lo comunican.

---

## No hace falta ser senior para trabajar bien

Todo lo que vimos en esta clase — ramas, commits, PRs — no requiere años de experiencia.
Requiere hábito. Y el hábito se construye desde el primer proyecto.

Alguien que recién empieza y ya trabaja con ramas, commits descriptivos y PRs
comunica una cosa muy clara al equipo: **entiende que el código no es tuyo — es del equipo.**

Esa mentalidad es la que distingue a un developer que crece rápido de uno que tarda años en aprender lo que debería haber aprendido desde el principio.

---

## Lo que el historial dice de tú

Cuando alguien entra a un proyecto nuevo, una de las primeras cosas que hace es:

```bash
git log --oneline
```

Ese historial habla por tú aunque no estés. Dice si trabajaste con orden, si pensaste los cambios, si trabajaste en equipo o solo acumulaste código.

```bash
# Historial que da confianza:
a3f2c1e feat(auth): agrega LoginView con redirección a /dashboard/
9b7d4f2 fix(auth): corrige redirección al login cuando el 403 no tiene sesión
2e1a8c4 feat(perfil): agrega PerfilView con LoginRequiredMixin
d5f9b1a test(perfil): verifica que el perfil solo es accesible con sesión activa

# Historial que genera desconfianza:
91b3a2d cosas
f4c1d3e wip
aa2b3c4 más
3d9e1f5 listo
```

No hay que esperar a estar en un equipo grande para escribir el primer tipo de historial.
Se puede empezar hoy, en el primer proyecto propio.

---

## Las herramientas cambian. Los principios no.

GitHub puede ser reemplazado por GitLab, Bitbucket o cualquier otra plataforma.
La IA puede mejorar, cambiar de nombre o funcionar distinto en dos años.

Pero estos principios van a seguir siendo válidos:

```
→ Una tarea = una rama
→ Un cambio lógico completo = un commit
→ El mensaje del commit describe qué hace, no cómo se hizo
→ Antes de empezar, actualizar
→ Nunca mezclar cambios de cosas distintas
→ El código que no se entiende es código que no se puede mantener
```

Aprender a trabajar bien con Git desde el principio es una inversión que se recupera
en cada proyecto, en cada entrevista y en cada equipo donde trabajés.

---

## Un último pensamiento

La IA puede generar código. Git guarda el historial.
Pero ninguna herramienta puede reemplazar el criterio de saber
**qué commitear, cuándo crear una rama y por qué este cambio importa**.

Eso lo aportás tú.

---

---

## Errores comunes en principiantes (y cómo evitarlos)

---

### ❌ Trabajar directo en `main`

```bash
# ¿qué salió mal?
git checkout main
# ... editar código ...
git commit -m "feat: perfil"
git push origin main    # ← esto rompe el flujo de todo el equipo
```

**Por qué es un problema:** `main` debería ser siempre código estable y revisado.
Si todos pushean directo a `main`, no hay forma de hacer review y cualquier bug va directo a producción.

**Solución:** Siempre `git checkout -b nombre-de-rama` antes de escribir código.

---

### ❌ Acumular cambios en un solo commit

```bash
git add .
git commit -m "todo el perfil"
# ↑ dentro hay: el modelo, la vista, el template, los tests, y también un cambio no relacionado en el carrito
```

**Por qué es un problema:** si hay que revertir el commit porque algo falló,
se pierde **todo** — incluyendo las partes que andaban bien.

**Solución:** commit por capa, commit por cambio lógico completo.

---

### ❌ Commitear el `.env`

```bash
git add .
git commit -m "más cambios"
# el .env con SECRET_KEY y contraseña de la BD acaba de subir a GitHub
```

**Por qué es un problema:** si el repositorio es público (o lo ve alguien ajeno),
las credenciales quedan expuestas. GitHub tiene bots que escanean repositorios buscando exactamente esto.

**Solución:** `.env` siempre en `.gitignore`. Verificar con `git status` antes de cada commit.

---

### ❌ Push sin entender qué se está subiendo

```bash
git add .
git push origin main
# ¿qué había en esos archivos? No sé exactamente.
```

**Solución:** `git status` y `git diff` antes de `git add`. `git add archivo_especifico` en lugar de `git add .`.

---

---

## El historial como documentación

Un historial bien mantenido responde "¿cuándo se agregó esto y por qué?" sin preguntar a nadie:

```bash
git log --oneline

a3f2c1e feat(perfil): agrega PerfilView con LoginRequiredMixin
9b7d4f2 feat(perfil): agrega template de perfil con datos del usuario
2e1a8c4 feat(perfil): registra URL /perfil/ en el sistema de rutas
d5f9b1a test(perfil): verifica que perfil solo es accesible con sesión activa
```

Versus el historial que no dice nada:

```bash
91b3a2d wip
f4c1d3e cambios
aa2b3c4 más cosas
3d9e1f5 listo
```

El segundo historial es inútil para el equipo. Y en seis meses, incluso para quien lo escribió.

---

## Reglas de oro

```
✅ Actualizar main antes de crear una rama nueva
✅ Una rama por tarea — nunca mezclar cambios de distintas cosas
✅ Entender la tarea antes de escribir código
✅ Commit por capa funcional: modelo, vista, template, test
✅ Mensajes de commit descriptivos: tipo(scope): qué hace
✅ git status y git diff antes de cada commit
✅ .env siempre en .gitignore
✅ La IA genera el esqueleto — tú entiendes y ajustás antes de commitear
✅ El PR describe qué hace el cambio y cómo probarlo
```

---

> _"El historial de Git es la memoria del equipo.
> Un commit bien escrito hoy es una hora de debugging ahorrada en seis meses."_

---
