# Práctica Clase 14: Laboratorio de Investigación DevSecOps y Hardening

## Introducción a la Práctica

¡Bienvenidos al laboratorio de Ciberseguridad Defensiva y Análisis Forense! En esta sesión, nos enfocaremos en la **protección estructural, el análisis de incidentes (Blue Team) y la auditoría** de plataformas construidas con Django. La cultura DevSecOps nos exige no solo parchear código, sino **investigar profundamente cómo y por qué ocurren las brechas**, para diseñar arquitecturas resilientes bajo el paradigma Zero Trust.

A lo largo de este documento investigativo, enfrentarán **3 casos de estudio ficticios** ambientados en el ecosistema corporativo chileno, todos modelados bajo vectores de ataque y vulnerabilidades documentadas globalmente (OWASP, MITRE ATT&CK, NIST).

> [!IMPORTANT]
> **Aviso Pedagógico e Instrucciones Generales:**
> *   Ninguna de las empresas o proyectos mencionados aquí existe en la realidad; toda similitud es puramente coincidente. **No uses entidades reales para prácticas ofensivas.**
> *   Sus respuestas **no deben ser código suelto**, sino reportes técnicos profesionales: diagnósticos de causa raíz, memorandos ejecutivos y tablas de hallazgos.
> *   **Requisito Obligatorio:** Toda afirmación debe sustentarse con fuentes oficiales tangibles (ej: [OWASP Top 10](https://owasp.org/www-project-top-ten/), [NVD/NIST](https://nvd.nist.gov/), [MITRE ATT&CK](https://attack.mitre.org/), o [Documentación oficial de Django](https://docs.djangoproject.com/en/stable/topics/security/)).

---



</details>

> [!NOTE]
> **Fuente de referencia obligatoria para este caso:** MITRE ATT&CK Enterprise Matrix — Tactic: Credential Access — Technique T1110 (Brute Force). Disponible en: https://attack.mitre.org/techniques/T1110/

### Preguntas de Investigación (Caso 1)

Responde de manera profesional y fundamentada en su totalidad:

1.  **Categorización del Vector de Ataque (MITRE ATT&CK):** Observando el volumen de peticiones iterativas provenientes de múltiples IP distintas, la rotación de User-Agents y la recurrencia sistemática del código HTTP `401` durante más de 300 intentos consecutivos en cuestión de minutos, ¿a qué **táctica y sub-técnica exacta** del framework MITRE ATT&CK corresponde este comportamiento? ¿Cómo lo diferencias de un simple ataque de Denegación de Servicio (DoS), cuyo objetivo no es obtener acceso sino colapsar el servicio?

2.  **Identificación de Impacto Crítico:** Analiza detenidamente las últimas tres líneas del registro. El código HTTP `200` a las `03:06:55` indica éxito en el inicio de sesión (acceso no autorizado confirmado). ¿Qué información específica obtuvo el atacante en la petición `GET /api/v1/user/configuracion_admin/` y qué magnitud de catástrofe de datos desencadena la respuesta de `4.3 MB` en el endpoint `POST /api/v1/user/exportar_base_datos/` a las `03:07:05`? Argumenta el impacto regulatorio considerando la **Ley N° 19.628 de Protección de Datos Personales** de Chile.

3.  **Contramedidas Defensivas en Django REST Framework:** Considerando que la API víctima está construida con Django REST Framework (DRF), ¿cuáles son **tres mecanismos defensivos específicos** que estuvieron fallidos o ausentes en el endpoint `/api/v1/auth/login/` y que hubiesen frenado el ataque antes del quinto intento fallido? Investiga y cita la documentación oficial de DRF sobre `DEFAULT_THROTTLE_RATES`, y al menos una librería de terceros certificada (ej: `django-axes`, `django-ratelimit`).

4.  **Respuesta al Incidente — Blue Team Playbook:** Si estuvieras a cargo de la contención inmediata a las `03:08 AM` al notar que la extracción masiva de la base de datos ya ocurrió, ¿cuáles son los **dos pasos más urgentes y obligatorios** para: (a) aislar al atacante impidiendo más exfiltración, y (b) preservar la cadena de custodia de la evidencia digital en servidores Linux sin destruir los artefactos volátiles en memoria?

---

## Caso 2: Cazadores de Dependencias (Auditoría de Vulnerabilidades Reales - SCA)

**Contexto del Proyecto:**

Una institución descentralizada ficticia, la **"Agencia de Innovación Social de Chile"**, está próxima a relanzar un portal interno de gestión ciudadana llamado *"Sistema de Consultas Públicas (SiConP)"*, cuyo código ha estado congelado y sin mantenimiento técnico por más de tres años.

Previo al pase a producción en la nube gubernamental, la Contraloría de TI les exige a ustedes —en el rol de Ingenieros SecOps Auditores Externos— realizar un **Software Composition Analysis (SCA)** exhaustivo del archivo `requirements.txt`. El objetivo es identificar vulnerabilidades conocidas (CVE) en librerías obsoletas y detectar posibles amenazas a la cadena de suministro de software (*Supply Chain Attacks / Typosquatting*), antes de firmar el certificado de aptitud para producción.

A continuación, el manifiesto íntegro de librerías del proyecto legado:

```text
amqp==5.1.1
asgiref==3.5.2
beautifulsoup4==4.11.1
boto3==1.24.89
botocore==1.27.89
celery==5.2.7
certifi==2022.9.24
cffi==1.15.1
charset-normalizer==2.1.1
click==8.1.3
cryptography==38.0.1
Django==3.0.1
django-cors-headers==3.13.0
django-redis==5.2.0
djangorestframework==3.13.1
gunicorn==20.1.0
idna==3.4
jmespath==1.0.1
kombu==5.2.4
Pillow==8.1.0
psycopg2-binary==2.9.3
pycparser==2.21
PyJWT==1.7.1
python-dateutil==2.8.2
pytz==2022.4
redis==4.3.4
requests==2.28.1
s3transfer==0.6.0
six==1.16.0
sqlparse==0.4.2
urllib3==1.26.12
vine==5.0.0
# -- Dependencias sospechosas / posible Typosquatting / Supply Chain Risk --
django-cors-headers-patch==1.0.0
cryptoliba-chile==0.0.1
chile-datos-rut==1.0.0
requests-chile==2.28.1
```

> [!NOTE]
> **Fuentes de referencia obligatorias para este caso:**
> - Base de datos CVE del NIST: https://nvd.nist.gov/
> - CVE Mitre: https://cve.mitre.org/
> - OWASP Software Component Verification Standard (SCVS): https://owasp.org/www-project-software-component-verification-standard/

### Preguntas de Investigación (Caso 2)

Realiza una labor de cacería de amenazas y redacta tu reporte estructurado para la Contraloría:

1.  **Auditoría de Vulnerabilidades Críticas (CVE):** Investiga en bases de datos como el **NIST NVD** o **CVE Mitre** las alertas de seguridad documentadas para estas tres versiones exactas presentes en el proyecto: `Django==3.0.1`, `Pillow==8.1.0` y `PyJWT==1.7.1`. Para cada una presenta: el **Código CVE** asociado, la **descripción del vector de explotación en español** (¿Inyección SQL? ¿Ejecución Remota de Código? ¿Evasión de Autenticación?), el **nivel CVSS** (crítico, alto, medio) y la **versión mínima segura** recomendada para parchear hoy. *(Hint: busca `Django 3.0.1 CVE`, `Pillow 8.1.0 CVE RCE`, `PyJWT 1.7.1 algorithm confusion`).*

2.  **Amenazas a la Cadena de Suministro (Typosquatting):** Al final de la lista de requerimientos, identifica al menos **tres paquetes cuyo nombre genera alerta extrema** por imitar librerías legítimas populares o contener nombres de dominio geográfico inusual. Basándote en investigaciones publicadas sobre ataques de *Supply Chain* en PyPI (ej. las alertas de *Sonatype Nexus Intelligence* o los reportes de *Socket.dev*), explica: (a) qué ejecuta silenciosamente el bloque `setup.py` o `install_requires` de estas librerías maliciosas durante un `pip install`, y (b) qué nivel de acceso al sistema operativo del contenedor Docker o servidor obtiene ese código.

3.  **Integración Continua DevSecOps (Automatización SCA):** Para que esta auditoría no dependa de la memoria o disponibilidad de un analista humano, ¿qué herramientas automatizadas gratuitas (ej. *GitHub Dependabot*, *pip-audit*, *Safety CLI*, *Trivy* o *OWASP Dependency-Check*) integrarías en el flujo CI/CD de GitHub Actions o GitLab CI? Explica brevemente cómo funcionan a nivel de *Pipeline*: ¿en qué etapa del ciclo se ejecutan?, ¿cómo hacen fallar el despliegue ante un `CRITICAL` CVE encontrado?, ¿qué artefacto de reporte generan?

---

## Caso 3: Consultoría de Riesgos Estratégicos (Arquitectura Zero Trust en Django)

**Contexto de la Consultoría:**

Ustedes son el equipo de consultores técnicos élite para **"Cordillera Paytech S.A."**, una promisoria StartUp Fintech nacional ficticia que gestiona transferencias entre PYMES, liquidación de sueldos y micro-inversiones ciudadanas. Faltan días para el lanzamiento masivo en producción.

Durante un exhaustivo comité de riesgos convocado por el Directorio, el Oficial de Seguridad de la Información (CISO) levanta alertas inminentes sobre fallas fundacionales en la arquitectura:

- Los clientes operarán habitualmente desde **redes Wi-Fi públicas** en cafeterías o estaciones de metro de Santiago, quedando expuestos a interceptaciones *Man-in-the-Middle* (MITM) y secuestros de sesión (*Session Hijacking*).
- La **Base de Datos PostgreSQL transaccional** —que almacena todos los registros financieros y RUTs de clientes— está instalada en la **misma subred pública** de internet que los servidores web Nginx, sin ninguna capa de aislamiento.
- El **100% de los desarrolladores** (seis personas) utilizan cuentas `is_superuser=True` todos los días directamente sobre el entorno de **Producción**, sin cuentas separadas ni roles granulares.

El Desarrollador Jefe descarta al CISO con desdén: *"Es excesivamente alarmista. Pagamos un Certificado SSL de primera línea; el navegador muestra el 'Candado' y las claves viajan cifradas. Además, somos seis desarrolladores nomás, es absurdamente impráctico usar cuentas limitadas en la admin de Django. El candado y el Superadmin bastan."*

> [!IMPORTANT]
> Este caso requiere aplicar el **Modelo de Madurez Zero Trust** (CISA Zero Trust Maturity Model). Fuente obligatoria: https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf

### Preguntas de Investigación (Caso 3)

Tomando postura como Consultor Senior de Seguridad, redacta el memorándum técnico completo a la Junta Directiva demoliendo la arrogancia del *Lead Developer*:

1.  **El Mito del "Candado Mágico" — SSL Stripping y HSTS:** Demuestra al Directorio por qué "tener el candado de HTTPS" es insuficiente cuando un usuario tipea `cordillerapaytech.cl` a mano (sin `https://`) desde una red pública comprometida. Explica técnicamente qué es un ataque **SSL Stripping** (tipificado dentro de MITM, aprox. 2009, técnica de Moxie Marlinspike) y cómo opera en el primer viaje HTTP no seguro antes del redireccionamiento. Luego, explica cómo la variable `SECURE_HSTS_SECONDS` de *Django Security Middleware*, combinada con `SECURE_HSTS_PRELOAD = True` y la inclusión en el *HSTS Preload List* de Chrome/Firefox, anula definitivamente este vector obligando al navegador a conectarse **siempre** en HTTPS.

2.  **Blindaje de Cookies de Autorización — Session & CSRF Hardening:** El robo de identificadores de sesión en redes aeroportuarias o cafeterías es frecuente si las cookies no están correctamente blindadas. Para cada una de las siguientes tres variables de `settings.py`, explica el impacto técnico individual que tiene activarlas y qué vector de ataque concreto neutralizan:
    - `SESSION_COOKIE_SECURE = True` → ¿Qué impide exactamente a nivel de transmisión HTTP/HTTPS?
    - `SESSION_COOKIE_HTTPONLY = True` → ¿Qué ataque de capa de aplicación (Layer 7) bloquea?
    - `CSRF_COOKIE_SAMESITE = "Strict"` → ¿Cómo previene las peticiones forjadas desde dominios externos?

3.  **Arquitectura de Red Cloud Segura — VPC y Segmentación (Three-Tier Architecture):** Argumentando el axioma central de Zero Trust *"Nunca confíes, siempre verifica — y asume que ya fuiste comprometido"*, critica técnica y contundentemente la decisión de instalar la base de datos transaccional financiera en la misma **Public Subnet** expuesta a internet que los servidores Nginx. Describe el diseño de red recomendado usando tres capas lógicas suficientemente aisladas:
    - **Capa 1 (DMZ):** Load Balancer público / Nginx como Edge.
    - **Capa 2 (Private App Subnet):** Instancias de la API Django/Gunicorn, sin IP pública directa.
    - **Capa 3 (Isolated DB Subnet):** Motor PostgreSQL exclusivamente en red privada, accesible solo desde la Capa 2 vía Security Groups / Network ACLs.
    Explica qué es un *NAT Gateway* y su rol en este modelo, y menciona qué normativa financiera chilena o internacional podría exigir legalmente esta segmentación (pista: PCI-DSS, CMF).

4.  **Minimización de Superficie Operativa — Principio de Mínimo Privilegio (PoLP):** Destruye el argumento del *Lead Developer* sobre "la velocidad del Superusuario". Primero, explica el riesgo real de una **amenaza interna** (*Insider Threat*) y qué ocurre con los 6 accesos de Producción si uno de los desarrolladores es víctima de un ataque de phishing y su credencial es comprometida. Luego, propón un esquema de roles usando el sistema nativo de **Grupos y Permisos granulares del *Django Admin Site*** con al menos dos grupos diferenciados:
    - Grupo `Soporte_Niv_01`: Solo lectura sobre modelos no financieros (ej: tickets, usuarios).
    - Grupo `Finanzas_Auditoria`: Lectura sobre modelos transaccionales, sin capacidad de eliminar ni exportar.
    Indica qué permisos Django (`add`, `change`, `delete`, `view`) asignarías individualmente a cada grupo y por qué.
