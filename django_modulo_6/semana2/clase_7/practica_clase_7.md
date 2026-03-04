# 🐍 Django — Módulo 6 · Clase 7

## Práctica: Formularios para el CV — Guía de sugerencias

---

> _"Un CV estático muestra quién eres. Un CV con formularios muestra cómo construyes. Esa diferencia vale más que cualquier línea del perfil."_

---

## Contexto

Continuamos con el proyecto de CV iniciado en la clase 6. En esta clase aprendiste Django Forms — la herramienta que permite que tu sitio capture y procese información del visitante.

Los datos del CV (experiencia, habilidades, proyectos) se administran desde el **admin de Django**, no hace falta crear formularios para eso. Los formularios que mostramos a continuación son para la **interacción con el visitante del sitio**: reclutadores, clientes, colaboradores.

Esta sección es una **guía de sugerencias**. Durante la clase implementaremos alguno según el avance grupal.

---

---

# Formularios recomendados para un CV de programador

---

## 1. Formulario de contacto ⭐ Prioritario

El más importante de cualquier portfolio. Permite que un reclutador o cliente te escriba directamente desde el sitio sin abrir su cliente de correo.

**Campos sugeridos:**

| Campo           | Tipo Django                       | Notas                                                         |
| --------------- | --------------------------------- | ------------------------------------------------------------- |
| Nombre completo | `CharField`                       | Obligatorio, max 80 caracteres                                |
| Email           | `EmailField`                      | Para poder responder                                          |
| Asunto          | `ChoiceField`                     | "Propuesta laboral", "Proyecto freelance", "Consulta", "Otro" |
| Mensaje         | `CharField` con `Textarea` widget | Obligatorio, max 1000 caracteres                              |

**¿`forms.Form` o `ModelForm`?**
→ `forms.Form` — el mensaje puede enviarse por email desde la vista sin necesitar un modelo. Si quisieras historial de mensajes en el admin, ahí pasaría a `ModelForm`.

**Flujo:**

```
/contacto/    → muestra el formulario (GET)
              → valida y confirma el envío (POST)
/contacto/gracias/  → página de confirmación
```

---

## 2. Suscripción a novedades / disponibilidad

Permite que un visitante deje su email para que lo notifiques cuando estés disponible para nuevos proyectos o cuando publiques algo nuevo.

**Campos sugeridos:**

| Campo           | Tipo Django   | Notas                                                                   |
| --------------- | ------------- | ----------------------------------------------------------------------- |
| Email           | `EmailField`  | Obligatorio                                                             |
| Tipo de interés | `ChoiceField` | "Empleo full-time", "Freelance", "Mentoría", "Solo seguir el portfolio" |

**¿`forms.Form` o `ModelForm`?**
→ `ModelForm` — los emails tienen que quedar guardados para poder usarlos después. Se consultan desde el admin.

---

## 3. Solicitud de CV completo

Algunos developers no publican el CV completo públicamente — lo envían solo a quienes lo soliciten. Un formulario simple permite filtrar quiénes piden acceso.

**Campos sugeridos:**

| Campo                  | Tipo Django                | Notas                       |
| ---------------------- | -------------------------- | --------------------------- |
| Nombre                 | `CharField`                | Obligatorio                 |
| Email                  | `EmailField`               | A dónde enviar el CV        |
| Empresa u organización | `CharField`                | Opcional (`required=False`) |
| Motivo                 | `CharField` con `Textarea` | Breve, max 300 caracteres   |

**¿`forms.Form` o `ModelForm`?**
→ Puede ser cualquiera: `forms.Form` si solo dispara un email, `ModelForm` si queres llevar registro de las solicitudes en el admin.

---

## 4. Feedback sobre proyectos

Si el portfolio incluye proyectos con links o demos, un formulario de feedback permite que el visitante deje su opinión sobre un proyecto específico.

**Campos sugeridos:**

| Campo      | Tipo Django                | Notas                            |
| ---------- | -------------------------- | -------------------------------- |
| Proyecto   | `ChoiceField`              | Lista de proyectos del portfolio |
| Valoración | `ChoiceField`              | Escala `1` a `5`                 |
| Comentario | `CharField` con `Textarea` | Opcional                         |

**¿`forms.Form` o `ModelForm`?**
→ `ModelForm` — el feedback tiene valor si se puede consultar después desde el admin.

---

---

# ¿Cuál implementar?

| Formulario      | Dificultad | Impacto en el portfolio                       |
| --------------- | ---------- | --------------------------------------------- |
| Contacto        | ★☆☆        | ⬆⬆⬆ Alto — lo primero que busca un reclutador |
| Suscripción     | ★★☆        | ⬆⬆ Medio — demuestra que el sitio es activo   |
| Solicitud de CV | ★☆☆        | ⬆⬆ Medio — genera conversación                |
| Feedback        | ★★☆        | ⬆ Bajo — útil pero no prioritario             |

**Recomendación**: empezar por el formulario de contacto. Cubre exactamente lo que vimos en la teoría y es lo más valorado en un portfolio real.

---

# Estructura sugerida en el proyecto

```
mi_cv/
├── contacto/              ← nueva app para el formulario
│   ├── forms.py           ← ContactoForm
│   ├── views.py           ← contacto_view
│   └── urls.py            ← path('contacto/', ...)
├── templates/
│   └── contacto/
│       ├── contacto.html  ← form con {% csrf_token %}
│       └── gracias.html   ← confirmación post-envío
```

O más simple: dentro de la app del CV existente si el proyecto es pequeño y no se quiere crear una app separada para un solo formulario.

---

> Esta guía es orientativa. El objetivo es que identifiques qué formularios tienen sentido para tu proyecto y puedas tomar esa decisión con criterio.

---
