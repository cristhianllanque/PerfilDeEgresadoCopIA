# Entregable 2: Planificación de Seguridad (Alineado con CE0321)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Entregable:** Entregable 2: Planificación de Seguridad (CE0321)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo
Este documento presenta el plan de seguridad de la información desarrollado para proteger los activos críticos que dan soporte al sistema **CopIA**. Bajo las directrices de estándares internacionales como ISO 27001 e ISO 27005, se identifican y clasifican los activos de información del sistema, se realiza un análisis de riesgos detallado para prever vectores de ataque, se estructuran las políticas de seguridad organizacional que rigen al equipo y se definen formalmente los roles de supervisión y ejecución técnica mediante una matriz RACI.

---

## Sección 1: Identificación y Clasificación de Activos Críticos

De acuerdo con las directrices de seguridad de la información (ISO 27001), los activos del sistema CopIA se clasifican según su nivel de confidencialidad, integridad y disponibilidad (C-I-D), asignando una escala de valoración del 1 al 5 (donde 5 es crítico):

| ID Activo | Nombre del Activo | Tipo de Activo | Descripción | Conf. | Integ. | Disp. | Valoración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ACT-01** | Base de Datos MySQL | Datos / Software | Contiene el histórico de alertas de fatiga e información de los conductores. | 4 | 5 | 4 | **Crítico (5)** |
| **ACT-02** | API REST FastAPI | Software / Servicio | Endpoint que recibe la telemetría IoT de toda la flota en tiempo real. | 3 | 4 | 5 | **Alto (4)** |
| **ACT-03** | Raspberry Pi Client | Hardware Edge | Dispositivo físico embebido en la cabina del camión que procesa video en tiempo real. | 3 | 4 | 4 | **Medio (3)** |
| **ACT-04** | Streaming de Video | Datos / Canal | Feed de video MJPEG del conductor en vivo desde el camión al operador. | 5 | 3 | 3 | **Crítico (5)** |
| **ACT-05** | Credenciales de Acceso | Información | Contraseñas hash de operadores y tokens de comunicación. | 5 | 5 | 4 | **Crítico (5)** |

---

## Sección 2: Matriz de Análisis de Riesgos (ISO 27005 / NIST)

Se evalúa la probabilidad (P) y el impacto (I) en una escala de 1 a 5. El score de riesgo final se calcula como: $R = P \times I$ (Riesgo Crítico: 15–25, Medio: 6–12, Bajo: 1–5).

| ID | Amenaza | Vulnerabilidad | Impacto | P | I | R | Mitigación Propuesta |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Intercepción de datos biométricos** | Comunicación en texto plano (HTTP/WS) entre Raspberry y el Servidor. | Fuga de privacidad y video del conductor. | 4 | 4 | **16** | Implementar HTTPS mediante certificados TLS 1.3 forzados. |
| **R-02** | **Acceso no autorizado a la base de datos** | Conexión de base de datos sin contraseña o acceso root remoto habilitado. | Destrucción de base de datos o robo de registros. | 3 | 5 | **15** | Hardening de MySQL: deshabilitar root remoto, contraseñas seguras y firewall de puerto 3306. |
| **R-03** | **Sabotaje del Hardware en Cabina** | Puertos USB expuestos en la Raspberry Pi dentro de la cabina. | Manipulación física del sistema o del sensor de cámara. | 3 | 3 | **9** | Enjaular físicamente el gabinete de la Raspberry Pi con cerradura bajo llave. |
| **R-04** | **Denegación de Servicio (DoS) en API** | Falta de rate-limiting (límite de peticiones) en la API REST de telemetría. | Pérdida de telemetría de toda la flota de transporte. | 2 | 4 | **8** | Implementar rate-limiting por IP en Nginx y balanceo de carga en pfSense. |

---

## Sección 3: Políticas de Seguridad Organizacional

Para respaldar los controles técnicos y mitigar los riesgos identificados, se definen las siguientes políticas de cumplimiento obligatorio:

* **Política de Control de Acceso (Principio de Mínimo Privilegio)**: Todo acceso administrativo al entorno de gestión (VLAN 40) o a los servidores requiere autenticación multifactor (MFA). Se prohíbe terminantemente el uso de cuentas genéricas o compartidas.
* **Política de Gestión de Contraseñas**: Las credenciales de operadores y administradores de base de datos deben tener una longitud mínima de 14 caracteres (alfanuméricos con símbolos) y forzar su rotación cada 90 días.
* **Política de Respaldos y Continuidad**: Se realizarán copias de seguridad incrementales diarias y completas semanales del activo crítico ACT-01 (Base de Datos MySQL). Estos backups serán cifrados (AES-256) y almacenados en un repositorio offline o servidor externo aislado para garantizar su recuperación ante incidentes de ransomware.

---

## Sección 4: Roles y Responsabilidades (RACI)

Para garantizar la correcta ejecución de los controles de seguridad, se define la siguiente matriz de responsabilidades:

* **Roles**:
  * **CISO**: Director de Seguridad de la Información (Aprobador final).
  * **DevOps / NetAdmin**: Administrador de Redes y Despliegue (Ejecutor).
  * **DBA**: Administrador de Base de Datos (Responsable de almacenamiento y hardening de datos).
  * **Operador**: Usuario del Dashboard (Consultor/Informado).

| Actividad / Control de Seguridad | CISO | DevOps / NetAdmin | DBA | Operador |
| :--- | :---: | :---: | :---: | :---: |
| Definición de Políticas de Seguridad | **A** | **C** | **C** | **I** |
| Hardening de Base de Datos MySQL | **A** | **C** | **R** | **I** |
| Renovación de Certificados SSL/TLS | **I** | **R** | **I** | **I** |
| Gestión de Parches de Sistemas Operativos | **A** | **R** | **R** | **I** |
| Auditoría de Intentos de Login Fallidos | **A** | **R** | **I** | **I** |

*Leyenda: **R**: Responsible (Ejecuta), **A**: Accountable (Aprueba/Dueño), **C**: Consulted (Consulta), **I**: Informed (Informado).*

---

## Anexos
1. **Modelos de Formularios de Políticas**: Borradores para la firma de aceptación de la política de contraseñas por los administradores.
2. **Plantilla de Análisis FMEA**: Análisis preliminar de modo de falla y efectos para el hardware vehicular.
