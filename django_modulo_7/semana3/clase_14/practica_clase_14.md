# Práctica Clase 14: Laboratorio de Investigación DevSecOps y Hardening

## Introducción a la Práctica

¡Bienvenidos al laboratorio de Ciberseguridad Defensiva y Análisis Forense! En esta sesión, nos enfocaremos en la **protección estructural, el análisis de incidentes (Blue Team) y la auditoría** de plataformas construidas con Django. La cultura DevSecOps nos exige no solo parchear código, sino **investigar profundamente cómo y por qué ocurren las brechas**, para diseñar arquitecturas resilientes bajo el paradigma Zero Trust.

A lo largo de este documento investigativo, enfrentarán **3 casos de estudio ficticios** ambientados en el ecosistema corporativo chileno, todos modelados bajo vectores de ataque y vulnerabilidades documentadas globalmente (OWASP, MITRE ATT&CK, NIST).

> [!IMPORTANT]
> **Aviso Pedagógico e Instrucciones Generales:**
>
> - Ninguna de las empresas o proyectos mencionados aquí existe en la realidad; toda similitud es puramente coincidente. **No uses entidades reales para prácticas ofensivas.**
> - Sus respuestas **no deben ser código suelto**, sino reportes técnicos profesionales: diagnósticos de causa raíz, memorandos ejecutivos y tablas de hallazgos.
> - **Requisito Obligatorio:** Toda afirmación debe sustentarse con fuentes oficiales tangibles (ej: [OWASP Top 10](https://owasp.org/www-project-top-ten/), [NVD/NIST](https://nvd.nist.gov/), [MITRE ATT&CK](https://attack.mitre.org/), o [Documentación oficial de Django](https://docs.djangoproject.com/en/stable/topics/security/)).

---

## Caso 1: Análisis Forense de Logs (Autopsia de un Ciberataque)

**Contexto del Incidente:**

Es madrugada en el centro de operaciones de **"Comercio Oceánico SpA"**, un prominente retail electrónico nacional. El sistema de monitoreo de infraestructura (APM) dispara múltiples alertas críticas: el uso de CPU de los servidores web se satura repentinamente y decenas de usuarios legítimos reportan que sus cuentas han sido bloqueadas preventivamente.

El equipo de Respuesta a Incidentes (CSIRT) te hace entrega íntegra del archivo de _Access Logs_ del balanceador de carga (Nginx) y la aplicación Django para que realices una **autopsia forense** y determines el origen y alcance del ataque.

<details>
<summary><strong>📋 Haz clic aquí para expandir los Logs Extraídos — Evidencia Forense Oficial</strong></summary>

```text
[14/Oct/2026:03:01:10 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:11 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:12 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:13 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:14 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:15 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:16 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:17 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:18 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:19 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:20 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:21 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:22 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:23 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:24 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:25 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:26 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:27 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:28 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:29 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:30 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:31 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:32 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:33 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:34 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:35 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:36 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:37 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:38 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:39 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:40 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:41 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:42 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:43 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:44 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:45 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:46 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:47 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:48 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:49 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:50 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:51 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:52 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:01:53 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:54 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:01:55 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:56 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:57 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:01:58 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:01:59 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:00 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:01 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:02 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:03 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:04 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:05 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:06 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:07 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:08 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:09 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:10 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:11 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:12 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:13 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:14 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:15 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:16 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:17 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:18 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:19 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:20 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:21 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:22 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:23 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:24 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:25 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:26 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:27 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:28 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:29 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:30 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:31 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:32 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:33 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:34 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:35 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:36 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:37 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:38 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:39 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:40 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:41 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:42 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:43 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:44 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:45 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:46 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:47 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:48 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:49 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:50 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:51 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:52 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:53 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:54 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:55 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:02:56 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:02:57 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:02:58 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:02:59 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:00 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:01 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:02 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:03 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:04 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:05 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:06 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:07 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:08 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:09 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:10 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:11 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:12 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:13 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:14 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:15 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:16 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:17 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:18 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:19 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:20 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:21 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:22 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:23 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:24 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:25 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:26 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:27 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:28 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:29 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:30 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:31 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:32 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:33 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:34 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:35 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:36 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:37 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:38 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:39 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:40 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:41 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:42 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:43 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:44 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:45 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:46 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:47 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:48 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:49 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:50 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:51 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:52 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:03:53 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:54 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:55 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:56 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:03:57 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:03:58 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:03:59 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:00 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:01 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:02 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:03 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:04 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:05 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:06 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:07 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:08 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:09 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:10 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:11 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:12 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:13 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:14 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:15 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:16 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:17 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:18 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:19 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:20 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:21 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:22 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:23 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:24 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:25 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:26 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:27 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:28 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:29 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:30 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:31 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:32 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:33 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:34 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:35 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:36 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:37 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:38 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:39 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:40 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:41 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:42 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:43 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:44 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:45 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:46 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:47 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:48 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:49 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:50 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:51 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:04:52 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:53 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:54 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:04:55 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:56 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:04:57 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:58 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:04:59 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:00 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:01 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:02 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:03 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:04 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:05 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:06 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:07 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:08 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:09 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:10 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:11 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:12 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:13 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:14 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:15 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:16 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:17 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:18 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:19 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:20 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:21 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:22 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:23 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:24 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:25 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:26 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:27 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:28 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:29 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:30 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:31 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:32 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:33 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:34 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:35 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:36 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:37 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:38 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:39 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:40 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:41 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:42 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:43 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:44 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:45 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:46 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:47 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:05:48 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:49 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:50 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:51 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:52 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:53 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:05:54 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:55 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:56 -0300] 198.51.100.22 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:57 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:05:58 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:05:59 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:06:00 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:06:01 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:06:02 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:06:03 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:06:04 -0300] 203.0.113.50 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:06:05 -0300] 198.51.100.99 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:06:06 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "Mozilla/5.0 (Macintosh;)" "-"
[14/Oct/2026:03:06:07 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "curl/7.68.0" "-"
[14/Oct/2026:03:06:08 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:06:09 -0300] 192.0.2.14 - POST /api/v1/auth/login/ HTTP/1.1 401 45 "python-requests/2.25.1" "-"
[14/Oct/2026:03:06:55 -0300] 203.0.113.45 - POST /api/v1/auth/login/ HTTP/1.1 200 128 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:06:57 -0300] 203.0.113.45 - GET /api/v1/user/configuracion_admin/ HTTP/1.1 200 1024 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
[14/Oct/2026:03:07:05 -0300] 203.0.113.45 - POST /api/v1/user/exportar_base_datos/ HTTP/1.1 200 4505600 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "-"
```

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

Una institución descentralizada ficticia, la **"Agencia de Innovación Social de Chile"**, está próxima a relanzar un portal interno de gestión ciudadana llamado _"Sistema de Consultas Públicas (SiConP)"_, cuyo código ha estado congelado y sin mantenimiento técnico por más de tres años.

Previo al pase a producción en la nube gubernamental, la Contraloría de TI les exige a ustedes —en el rol de Ingenieros SecOps Auditores Externos— realizar un **Software Composition Analysis (SCA)** exhaustivo del archivo `requirements.txt`. El objetivo es identificar vulnerabilidades conocidas (CVE) en librerías obsoletas y detectar posibles amenazas a la cadena de suministro de software (_Supply Chain Attacks / Typosquatting_), antes de firmar el certificado de aptitud para producción.

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
>
> - Base de datos CVE del NIST: https://nvd.nist.gov/
> - CVE Mitre: https://cve.mitre.org/
> - OWASP Software Component Verification Standard (SCVS): https://owasp.org/www-project-software-component-verification-standard/

### Preguntas de Investigación (Caso 2)

Realiza una labor de cacería de amenazas y redacta tu reporte estructurado para la Contraloría:

1.  **Auditoría de Vulnerabilidades Críticas (CVE):** Investiga en bases de datos como el **NIST NVD** o **CVE Mitre** las alertas de seguridad documentadas para estas tres versiones exactas presentes en el proyecto: `Django==3.0.1`, `Pillow==8.1.0` y `PyJWT==1.7.1`. Para cada una presenta: el **Código CVE** asociado, la **descripción del vector de explotación en español** (¿Inyección SQL? ¿Ejecución Remota de Código? ¿Evasión de Autenticación?), el **nivel CVSS** (crítico, alto, medio) y la **versión mínima segura** recomendada para parchear hoy. _(Hint: busca `Django 3.0.1 CVE`, `Pillow 8.1.0 CVE RCE`, `PyJWT 1.7.1 algorithm confusion`)._

2.  **Amenazas a la Cadena de Suministro (Typosquatting):** Al final de la lista de requerimientos, identifica al menos **tres paquetes cuyo nombre genera alerta extrema** por imitar librerías legítimas populares o contener nombres de dominio geográfico inusual. Basándote en investigaciones publicadas sobre ataques de _Supply Chain_ en PyPI (ej. las alertas de _Sonatype Nexus Intelligence_ o los reportes de _Socket.dev_), explica: (a) qué ejecuta silenciosamente el bloque `setup.py` o `install_requires` de estas librerías maliciosas durante un `pip install`, y (b) qué nivel de acceso al sistema operativo del contenedor Docker o servidor obtiene ese código.

3.  **Integración Continua DevSecOps (Automatización SCA):** Para que esta auditoría no dependa de la memoria o disponibilidad de un analista humano, ¿qué herramientas automatizadas gratuitas (ej. _GitHub Dependabot_, _pip-audit_, _Safety CLI_, _Trivy_ o _OWASP Dependency-Check_) integrarías en el flujo CI/CD de GitHub Actions o GitLab CI? Explica brevemente cómo funcionan a nivel de _Pipeline_: ¿en qué etapa del ciclo se ejecutan?, ¿cómo hacen fallar el despliegue ante un `CRITICAL` CVE encontrado?, ¿qué artefacto de reporte generan?

---

## Caso 3: Consultoría de Riesgos Estratégicos (Arquitectura Zero Trust en Django)

**Contexto de la Consultoría:**

Ustedes son el equipo de consultores técnicos élite para **"Cordillera Paytech S.A."**, una promisoria StartUp Fintech nacional ficticia que gestiona transferencias entre PYMES, liquidación de sueldos y micro-inversiones ciudadanas. Faltan días para el lanzamiento masivo en producción.

Durante un exhaustivo comité de riesgos convocado por el Directorio, el Oficial de Seguridad de la Información (CISO) levanta alertas inminentes sobre fallas fundacionales en la arquitectura:

- Los clientes operarán habitualmente desde **redes Wi-Fi públicas** en cafeterías o estaciones de metro de Santiago, quedando expuestos a interceptaciones _Man-in-the-Middle_ (MITM) y secuestros de sesión (_Session Hijacking_).
- La **Base de Datos PostgreSQL transaccional** —que almacena todos los registros financieros y RUTs de clientes— está instalada en la **misma subred pública** de internet que los servidores web Nginx, sin ninguna capa de aislamiento.
- El **100% de los desarrolladores** (seis personas) utilizan cuentas `is_superuser=True` todos los días directamente sobre el entorno de **Producción**, sin cuentas separadas ni roles granulares.

El Desarrollador Jefe descarta al CISO con desdén: _"Es excesivamente alarmista. Pagamos un Certificado SSL de primera línea; el navegador muestra el 'Candado' y las claves viajan cifradas. Además, somos seis desarrolladores nomás, es absurdamente impráctico usar cuentas limitadas en la admin de Django. El candado y el Superadmin bastan."_

> [!IMPORTANT]
> Este caso requiere aplicar el **Modelo de Madurez Zero Trust** (CISA Zero Trust Maturity Model). Fuente obligatoria: https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf

### Preguntas de Investigación (Caso 3)

Tomando postura como Consultor Senior de Seguridad, redacta el memorándum técnico completo a la Junta Directiva demoliendo la arrogancia del _Lead Developer_:

1.  **El Mito del "Candado Mágico" — SSL Stripping y HSTS:** Demuestra al Directorio por qué "tener el candado de HTTPS" es insuficiente cuando un usuario tipea `cordillerapaytech.cl` a mano (sin `https://`) desde una red pública comprometida. Explica técnicamente qué es un ataque **SSL Stripping** (tipificado dentro de MITM, aprox. 2009, técnica de Moxie Marlinspike) y cómo opera en el primer viaje HTTP no seguro antes del redireccionamiento. Luego, explica cómo la variable `SECURE_HSTS_SECONDS` de _Django Security Middleware_, combinada con `SECURE_HSTS_PRELOAD = True` y la inclusión en el _HSTS Preload List_ de Chrome/Firefox, anula definitivamente este vector obligando al navegador a conectarse **siempre** en HTTPS.

2.  **Blindaje de Cookies de Autorización — Session & CSRF Hardening:** El robo de identificadores de sesión en redes aeroportuarias o cafeterías es frecuente si las cookies no están correctamente blindadas. Para cada una de las siguientes tres variables de `settings.py`, explica el impacto técnico individual que tiene activarlas y qué vector de ataque concreto neutralizan:
    - `SESSION_COOKIE_SECURE = True` → ¿Qué impide exactamente a nivel de transmisión HTTP/HTTPS?
    - `SESSION_COOKIE_HTTPONLY = True` → ¿Qué ataque de capa de aplicación (Layer 7) bloquea?
    - `CSRF_COOKIE_SAMESITE = "Strict"` → ¿Cómo previene las peticiones forjadas desde dominios externos?

3.  **Arquitectura de Red Cloud Segura — VPC y Segmentación (Three-Tier Architecture):** Argumentando el axioma central de Zero Trust _"Nunca confíes, siempre verifica — y asume que ya fuiste comprometido"_, critica técnica y contundentemente la decisión de instalar la base de datos transaccional financiera en la misma **Public Subnet** expuesta a internet que los servidores Nginx. Describe el diseño de red recomendado usando tres capas lógicas suficientemente aisladas:
    - **Capa 1 (DMZ):** Load Balancer público / Nginx como Edge.
    - **Capa 2 (Private App Subnet):** Instancias de la API Django/Gunicorn, sin IP pública directa.
    - **Capa 3 (Isolated DB Subnet):** Motor PostgreSQL exclusivamente en red privada, accesible solo desde la Capa 2 vía Security Groups / Network ACLs.
      Explica qué es un _NAT Gateway_ y su rol en este modelo, y menciona qué normativa financiera chilena o internacional podría exigir legalmente esta segmentación (pista: PCI-DSS, CMF).

4.  **Minimización de Superficie Operativa — Principio de Mínimo Privilegio (PoLP):** Destruye el argumento del _Lead Developer_ sobre "la velocidad del Superusuario". Primero, explica el riesgo real de una **amenaza interna** (_Insider Threat_) y qué ocurre con los 6 accesos de Producción si uno de los desarrolladores es víctima de un ataque de phishing y su credencial es comprometida. Luego, propón un esquema de roles usando el sistema nativo de **Grupos y Permisos granulares del _Django Admin Site_** con al menos dos grupos diferenciados:
    - Grupo `Soporte_Niv_01`: Solo lectura sobre modelos no financieros (ej: tickets, usuarios).
    - Grupo `Finanzas_Auditoria`: Lectura sobre modelos transaccionales, sin capacidad de eliminar ni exportar.
      Indica qué permisos Django (`add`, `change`, `delete`, `view`) asignarías individualmente a cada grupo y por qué.
