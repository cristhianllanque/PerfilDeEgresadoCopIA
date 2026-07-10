# Entregable 2: Controles, Monitoreo y Análisis Ético-Legal (Alineado con CE0322/CE0323/CE0341)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Competencias:** CE0322/23 (Implementación de Seguridad) / CE0341 (Ética de la Profesión)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Noviembre 2026

---

## Resumen Ejecutivo

Este documento abarca la fase defensiva y de observabilidad de la infraestructura de CopIA. Una vez que la red (Entregable 1) fue establecida para soportar la arquitectura de software, se procedió a auditarla. Mediante escaneos de vulnerabilidades, se identificaron brechas (CVEs) en los servicios expuestos, las cuales fueron mitigadas mediante técnicas de *Hardening* y la implementación de un Web Application Firewall (WAF). 

En paralelo, se desplegó un sistema de monitoreo proactivo centralizado (Zabbix) para supervisar tanto la salud de los nodos vehiculares (Raspberry Pi) como del Datacenter (Ubuntu Server / Linux), asegurando la continuidad del negocio. Finalmente, dado que el sistema recolecta datos biométricos e imágenes de ciudadanos en tiempo real (PERCLOS), se desarrolló un profundo análisis de responsabilidad profesional, amparado en el Código de Ética de la ACM y en el marco legal vigente de protección de datos personales.

---

## Sección 1: Auditoría de Vulnerabilidades y Hardening

Siguiendo el principio de "Asumir la Brecha" (Assume Breach), se ejecutó un escáner de vulnerabilidades (OpenVAS/Greenbone) contra el servidor Ubuntu (Linux) que hospeda la API (FastAPI) y la Base de Datos (MySQL) antes de su paso a producción.

### 1.1 Reporte de Vulnerabilidades Encontradas

A continuación, se resume un extracto del log de auditoría generado por OpenVAS, enfocado en el segmento DMZ (VLAN 30):

| Host Objetivo | Puerto/Servicio | Vulnerabilidad (CVE / NVTE) | Nivel CVSS v3.1 | Descripción del Hallazgo |
| :--- | :--- | :--- | :--- | :--- |
| 192.168.30.15 | TCP 3306 (MySQL) | CVE-2023-21912 | **Alto (7.5)** | Base de datos expuesta sin cifrado SSL. Posible intercepción de credenciales en texto plano. |
| 192.168.30.15 | TCP 8000 (HTTP) | Falta de Cabeceras HSTS | **Medio (5.3)** | El framework FastAPI no está forzando HTTPS mediante cabeceras de seguridad estrictas. |
| 192.168.30.15 | TCP 22 (SSH) | CVE-2021-41617 | **Medio (4.4)** | OpenSSH permite autenticación por contraseña. Susceptible a fuerza bruta externa. |

### 1.2 Ejecución de Controles (Mitigación)

Frente a los hallazgos críticos de la auditoría, se ejecutaron las siguientes medidas de contención (Hardening):

**A. Bastionado de Base de Datos MySQL (Cierre de CVE-2023-21912)**
Se procedió a aislar la base de datos de telemetría y a forzar conexiones encriptadas. Se modificó el archivo de configuración `my.cnf`:
```ini
[mysqld]
# Deshabilitar escucha externa
bind-address = 127.0.0.1
# Forzar cifrado TLS 1.3
require_secure_transport = ON
tls_version = TLSv1.2,TLSv1.3
ssl-ca = /etc/mysql/certs/ca-cert.pem
ssl-cert = /etc/mysql/certs/server-cert.pem
ssl-key = /etc/mysql/certs/server-key.pem
```

**B. Bastionado de FastAPI (Cierre de Cabeceras Inseguras)**
Trabajando en conjunto con el área de Software, se instruyó colocar un Proxy Reverso (Nginx) delante del servidor Uvicorn/FastAPI. Se insertaron las siguientes directivas de seguridad en `nginx.conf`:
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Content-Security-Policy "default-src 'self';" always;
```
Con estas configuraciones, el escáner de OpenVAS arrojó un reporte limpio (0 vulnerabilidades críticas o altas) en la reevaluación.

---

## Sección 2: Monitoreo Proactivo (Zabbix y Alertas)

Para cumplir con el SLA (Acuerdo de Nivel de Servicio) de disponibilidad de CopIA, se instaló **Zabbix 6.0 LTS**. Este sistema permite visualizar telemetría de hardware antes de que ocurra una falla catastrófica.

### 2.1 Configuración de Ítems y Plantillas (Templates)
* **Template OS Linux SNMP:** Aplicado al nodo Edge (Raspberry Pi). Mide asíncronamente el uso de CPU (debido al procesamiento intensivo de MediaPipe) y la temperatura térmica del SoC ARM.
* **Template OS Linux Agent:** Instalado en la Máquina Virtual del Datacenter. Mide el consumo de memoria RAM de la API FastAPI y la latencia de lectura/escritura en disco de la base de datos MySQL.

### 2.2 Triggers (Disparadores de Alertas)
Se configuraron expresiones lógicas para detonar alertas preventivas.
* **Trigger 1 (Pérdida de Comunicación Edge):** 
  `last(/CopIA-Edge-Camion01/icmpping) = 0`
  *Gravedad:* Alta. Significa que el túnel IPSec o la red 4G del camión ha caído.
* **Trigger 2 (Sobrecalentamiento Edge):** 
  `avg(/CopIA-Edge-Camion01/sensor.temp,5m) > 80`
  *Gravedad:* Advertencia. La Raspberry Pi superó los 80°C durante 5 minutos continuos procesando video, riesgo de *Thermal Throttling*.
* **Trigger 3 (Saturación de Base de Datos):** 
  `last(/CopIA-UbuntuServer/mysql.connections) > 500`
  *Gravedad:* Desastre. Posible ataque DDoS sobre la API que está saturando el pool de conexiones.

### 2.3 Sistema de Notificaciones (Telegram Webhook)
> **[Nota del Autor]**
> *En esta sección del documento impreso se insertan capturas de pantalla de la app móvil de Telegram, mostrando al bot "CopIA_NOC_Bot" enviando mensajes de alerta en tiempo real a los administradores de infraestructura con el texto: `PROBLEM: High CPU utilization on Ubuntu Server FastAPI`.*

---

## Sección 3: Análisis Ético y Legalidad (Ética ACM)

La recolección masiva de métricas fisiológicas (PERCLOS, Movimiento Ocular) y de coordenadas geográficas en tiempo real (SIM7600G) sitúa al proyecto CopIA en un escenario crítico respecto a la privacidad. Si bien el fin es salvaguardar la vida humana, los medios técnicos deben regirse bajo principios de deontología profesional.

### 3.1 Marco Legal de Protección de Datos Personales
Las leyes modernas (como el RGPD europeo o leyes homólogas latinoamericanas de Protección de Datos Personales) tipifican la ubicación GPS en tiempo real y el reconocimiento facial como **Datos Personales Sensibles**. 

**Implicancias para CopIA:**
1. **Consentimiento Informado:** El conductor debe firmar una cláusula anexa a su contrato laboral donde acepta expresamente ser monitoreado mediante IA por motivos de salud y seguridad ocupacional.
2. **Principio de Proporcionalidad:** La cámara de la Raspberry Pi **únicamente graba a demanda o ante un evento de fatiga**. Está prohibido por ley grabar y almacenar audio y video del interior de la cabina las 24 horas, ya que constituiría una vigilancia intrusiva y acoso laboral (Micromanagement).
3. **Derecho al Olvido (Borrado):** El diseño de la base de datos MySQL debe poseer rutinas (CRON jobs) que purguen y anonimicen de forma automatizada los videos y datos de telemetría de un chofer luego de 60 días, a menos que exista un requerimiento policial por accidente.

### 3.2 Principios del Código de Ética de la ACM
El despliegue de esta arquitectura se basa en las directrices de la Association for Computing Machinery (ACM):

* **Principio 1.1: Contribuir a la sociedad y al bienestar humano.**
  El propósito fundamental de CopIA es reducir la tasa de fatalidad en las carreteras. No obstante, al implementar MediaPipe para visión artificial, se asume la responsabilidad ética de garantizar que el algoritmo funcione con igual precisión sin importar la etnia, color de piel o uso de lentes del conductor (mitigación de sesgos algorítmicos).
* **Principio 1.2: Evitar el Daño.**
  Una brecha de datos (fuga del servidor Ubuntu) que exponga videos de conductores durmiéndose podría arruinar sus carreras profesionales y afectar psicológicamente a sus familias. Por ello, la inversión en cortafuegos pfSense, segmentación de VLANs y cifrado IPSec (documentados en los Entregables anteriores) no es un lujo técnico, sino un **deber moral ineludible** para evitar el daño a terceros.
* **Principio 1.7: Respetar la Privacidad.**
  La arquitectura descentralizada (Edge Computing) respeta este principio. Al procesar el 90% de la inferencia IA de manera local dentro del camión y enviar solo una cadena JSON de alerta al Datacenter, se minimiza masivamente la exposición de la intimidad visual del transportista frente a operadores administrativos en la nube.
