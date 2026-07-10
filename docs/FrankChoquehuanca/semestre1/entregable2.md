# Entregable 2: Planificación de Seguridad (Alineado con CE0321)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Competencia:** CE0321 - Planificación de Seguridad de la Información
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo

El presente documento aborda la estrategia integral de ciberseguridad y gestión de riesgos para la infraestructura del proyecto **CopIA**. Tratándose de un sistema que procesa telemetría de vehículos pesados y video en vivo, la disponibilidad y confidencialidad de los datos son críticas. Cualquier disrupción en el flujo de telemetría podría impedir la alerta oportuna de fatiga, derivando en riesgos mortales, mientras que la filtración de video interno de la cabina supondría graves violaciones a las leyes de protección de datos personales.

Por consiguiente, este entregable desarrolla un marco de gestión de riesgos fundamentado en la norma **ISO/IEC 27005**, identificando, evaluando y tratando las amenazas que acechan tanto a los nodos Edge (cabina del camión) como al Datacenter central. Asimismo, se establecen las políticas de seguridad organizacionales obligatorias y el diseño de los controles técnicos preventivos, detectivos y correctivos que blindarán la arquitectura contra amenazas internas (insider threats) y externas.

---

## Sección 1: Gestión y Evaluación de Riesgos (ISO/IEC 27005)

La metodología adoptada para la evaluación del riesgo calcula el impacto en base a la Probabilidad de ocurrencia (P) multiplicada por el Impacto operativo/legal (I), generando un Nivel de Riesgo (NR). $$NR = P \times I$$. La escala utilizada para ambas variables va del 1 al 5. Todo riesgo con $$NR \ge 15$$ es considerado inaceptable y exige tratamiento inmediato.

### 1.1 Matriz de Identificación de Activos Críticos

Antes de evaluar el riesgo, se debe clasificar el valor de lo que se protege.

| Código Activo | Descripción del Activo | Ubicación Física | Confidencialidad | Integridad | Disponibilidad |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ACT-01** | Servidor de Base de Datos MySQL | Datacenter | Alta | Alta | Alta |
| **ACT-02** | Nodos IoT (Raspberry Pi 4) | Cabina de Flota | Media | Media | Alta |
| **ACT-03** | Túneles IPSec e Infraestructura de Red | Datacenter y Edge | Alta | Alta | Crítica |
| **ACT-04** | Datos Crudos (Telemetría y Videos) | Cabina y Datacenter | Alta | Crítica | Media |

### 1.2 Matriz Expandida de Evaluación de Riesgos

La siguiente tabla resume los 15 vectores de ataque y vulnerabilidades más severas detectadas en el modelo de amenazas de CopIA, abarcando espectros lógicos, físicos y humanos.

| ID Riesgo | Descripción de la Amenaza | Vector de Ataque / Causa | Prob. | Imp. | Nivel (P x I) | Tratamiento / Controles a Implementar |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Robo físico del nodo IoT Edge. | Delincuencia común al estar el camión estacionado. | 4 | 3 | **12** | Encriptación de disco en la Raspberry Pi (LUKS). Deshabilitar puertos USB. |
| **RSK-02** | Pérdida de cobertura móvil celular. | Zonas de sombra topográfica en carreteras interprovinciales. | 5 | 4 | **20** | **INACEPTABLE.** Módem Dual-SIM con script de failover automático entre operadoras (Ej. Claro/Movistar). |
| **RSK-03** | Intercepción de video en tránsito. | Man-in-the-Middle (MitM) en la red 4G pública. | 2 | 5 | **10** | Cifrado mandatorio AES-256 GCM mediante túnel IPSec IKEv2. |
| **RSK-04** | Denegación de Servicio (DDoS) al API. | Redes botnet atacando la IP pública del Datacenter. | 3 | 5 | **15** | **INACEPTABLE.** Reglas de GeoIP Block en pfSense y limitación de peticiones (Rate Limiting) en Nginx. |
| **RSK-05** | Inyección SQL a la base de datos. | Vulnerabilidad no parcheada en el backend FastAPI. | 2 | 5 | **10** | Uso estricto de ORMs (SQLAlchemy), bloqueo de puerto 3306 al exterior (Segmentación VLAN 20). |
| **RSK-06** | Infección por Ransomware. | Phishing al administrador de red del Datacenter. | 3 | 5 | **15** | **INACEPTABLE.** Política de Backups 3-2-1 inmutables, aislamiento de segmento de gestión (VLAN 40). |
| **RSK-07** | Falla de energía eléctrica en el Datacenter. | Apagón general de la ciudad o falla de subestación. | 2 | 5 | **10** | Implementación de UPS de doble conversión y generador diésel de respaldo (Tier III compliance). |
| **RSK-08** | Falla catastrófica del Router Core. | Fallo de hardware (quemadura de placa o fuente). | 2 | 5 | **10** | Configuración de Clúster de Alta Disponibilidad Activo-Pasivo usando CARP en firewalls pfSense. |
| **RSK-09** | Acceso no autorizado por ex-empleados. | Falla en revocar credenciales tras renuncia/despido. | 3 | 4 | **12** | Integración con Active Directory / LDAP para centralizar la baja de usuarios inmediatamente. |
| **RSK-10** | Interrupción por parcheo fallido (Downtime). | Aplicación de actualización de SO defectuosa en MySQL. | 4 | 3 | **12** | Entorno de *Staging* mandatorio. Rollback de snapshots en el hypervisor Proxmox antes de aplicar. |
| **RSK-11** | Daño por exceso de temperatura. | Falla del sistema de aire acondicionado del Datacenter. | 2 | 4 | **8** | Monitoreo térmico por SNMP. Apagado automático ordenado (Graceful Shutdown) a los 35°C ambientales. |
| **RSK-12** | Fuerza bruta contra puertos SSH (Puerto 22). | Scanners automáticos (Shodan) rastreando el pfSense. | 5 | 3 | **15** | **INACEPTABLE.** Cambio de puerto por defecto. Deshabilitar logueo de `root`. Autenticación obligatoria por llaves RSA/Ed25519 (cero contraseñas). |
| **RSK-13** | Corrupción de bases de datos por hardware. | Sectores defectuosos o falla mecánica en discos duros. | 2 | 5 | **10** | Implementación de arreglos RAID 10 (Hardware) o ZFS con paridad para la base de datos. |
| **RSK-14** | Fuga de datos de telemetría (Insider Threat). | DBA malicioso extrae un dump de la DB para la competencia. | 1 | 5 | **5** | Implementar Data Loss Prevention (DLP). Auditar todas las consultas SELECT intensivas con Zabbix. |
| **RSK-15** | Manipulación del código del script en Edge. | Conductor interviene físicamente el script para evitar que reporte la fatiga. | 2 | 4 | **8** | Firma criptográfica de scripts (Secure Boot). Inmutabilidad del sistema operativo en la Raspberry. |

---

## Sección 2: Diseño de Controles de Ciberseguridad

Para tratar los riesgos mencionados, se ha diseñado una arquitectura defensiva en capas.

### 2.1 Controles Perimetrales e IDS/IPS
* **Stateful Packet Inspection (pfSense):** El firewall evaluará el estado de las conexiones. Todo tráfico entrante hacia la VLAN 10, 20 y 40 estará bloqueado por defecto ("Deny All").
* **Intrusion Prevention System (Snort/Suricata):** Se habilitarán reglas en modo "Bloqueo" en el pfSense para detectar y abortar ataques conocidos (ej. escaneos de Nmap agresivos, firmas de malware) provenientes de la WAN.
* **Geobloqueo (pfBlockerNG):** Dado que la flota de camiones opera exclusivamente en territorio nacional, el firewall descartará a nivel de kernel cualquier paquete TCP/UDP cuyo origen IP radique en Rusia, China, Corea del Norte o países ajenos a las operaciones logísticas.

### 2.2 Hardening de Servidores e Infraestructura
* **Criptografía en Tránsito:** Todo el tráfico entre las cabinas y el Datacenter navegará cifrado por túneles **IPSec IKEv2** (Algoritmo AES-256-GCM con SHA-256 para integridad de paquetes). El tráfico web de la API usará certificados TLS 1.3 gestionados por Let's Encrypt.
* **Hardening de MySQL (Capa Base de Datos):** 
    * Eliminación absoluta del acceso externo (solo escucha en `127.0.0.1` o `192.168.20.x`).
    * Ejecución del demonio bajo un usuario de Linux sin privilegios de root (`mysql:mysql`).
    * Cifrado transparente de tablas en reposo (Transparent Data Encryption - TDE) para prevenir el acceso a los datos si los discos físicos son sustraídos.

---

## Sección 3: Políticas Organizacionales y Normativas

El mejor hardware del mercado es inútil frente al error humano. Para regir el comportamiento de los administradores y usuarios, se han redactado formalmente los siguientes estatutos.

### 3.1 Política Oficial de Gestión de Accesos y Contraseñas
**Código de Documento:** POL-SEC-001 | **Estado:** Vigente
**1. Objetivo:** Establecer los lineamientos criptográficos y de comportamiento para el resguardo de las credenciales de acceso a toda infraestructura tecnológica del Proyecto CopIA.
**2. Alcance:** Esta política es obligatoria y vinculante para el 100% de los empleados, contratistas, y proveedores (terceros) que posean acceso a las redes del Datacenter o a los dispositivos Edge.
**3. Requisitos Técnicos Obligatorios:**
* **Longitud y Complejidad:** Las contraseñas administrativas no serán menores a catorce (14) caracteres alfanuméricos y deberán incluir símbolos especiales. Queda prohibido usar palabras del diccionario.
* **Rotación Forzada:** El sistema obligará el cambio de credenciales de Active Directory cada 60 días.
* **MFA (Multi-Factor Authentication):** Todo acceso remoto VPN para teletrabajo requerirá obligatoriamente un segundo factor temporal (TOTP) utilizando Google Authenticator o Microsoft Authenticator. Ninguna contraseña es suficiente por sí sola.
* **Prohibición de Credenciales Compartidas:** El acceso a los servidores mediante usuarios genéricos (ej. `admin` o `root`) está terminantemente prohibido. Toda acción debe estar ligada a un usuario nominativo (ej. `fchoquehuanca`) para mantener el registro forense (Non-repudiation).
**4. Sanciones Disciplinarias:**
Compartir una contraseña administrativa o eludir los mecanismos MFA constituye una violación de Nivel 1. El comité de seguridad aplicará sanciones que van desde la suspensión temporal hasta el despido justificado y posibles acciones legales si deriva en una brecha de datos.

### 3.2 Matriz RACI: Roles y Responsabilidades de Ciberseguridad

Para garantizar que el monitoreo y mantenimiento no queden en el abandono, se define la asignación de responsabilidades:
* **R (Responsible):** Quien hace el trabajo.
* **A (Accountable):** Quien asume la responsabilidad legal/gerencial (Aprueba).
* **C (Consulted):** Quien proporciona información útil.
* **I (Informed):** Quien debe ser notificado tras la finalización.

| Tarea de Ciberseguridad | CISO (Jefe de Seguridad) | Administrador de Red | Administrador de BD (DBA) | Conductor del Camión |
| :--- | :--- | :--- | :--- | :--- |
| **Revisión de logs del Firewall y Zabbix** | I | R | I | - |
| **Aplicación de parches de seguridad en Ubuntu** | C | R | A | - |
| **Respaldo semanal de la base de datos** | A | C | R | - |
| **Reporte de pérdida o robo del nodo IoT (Raspberry)** | A | I | - | R |
| **Auditoría semestral de accesos y permisos** | R | C | C | - |
| **Respuesta a incidentes (Brecha de Datos confirmada)** | R | C | C | - |
