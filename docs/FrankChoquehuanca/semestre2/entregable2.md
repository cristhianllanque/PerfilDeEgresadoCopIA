# Entregable 2: Implementación, Monitoreo y Ética de Seguridad (Alineado con CE0322, CE0323 y CE0324)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Entregable:** Entregable 2: Implementación, Monitoreo y Ética de Seguridad (CE0322, CE0323 y CE0324)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo
Este entregable detalla la implementación de controles técnicos de seguridad para mitigar riesgos críticos detectados en la fase de planeación, el plan de monitoreo continuo de seguridad y la declaración ética bajo el Código de Conducta Profesional de la ACM para proteger la privacidad e integridad de los datos biométricos de los conductores de la flota. Se documentan las configuraciones de cifrado en tránsito SSL/TLS con Nginx, el hardening de la base de datos MySQL, la automatización de parches en la flota Edge y en servidores locales, y las métricas KPI utilizadas para evaluar de forma continua el estado de seguridad de la infraestructura.

---

## Sección 1: Implementación de Controles Técnicos

### A. Cifrado en Tránsito (HTTPS/TLS) en Nginx
Para evitar la intercepción de video y telemetría en tránsito (Riesgo R-01), se configura **Nginx** como un proxy reverso que intercepta el puerto público 443, forzando TLS 1.3 y redirigiendo localmente al puerto 8000 de FastAPI.

#### Archivo de Configuración de Nginx `/etc/nginx/sites-available/copia.conf`:
```nginx
server {
    listen 80;
    server_name api.copia.transporte.com;
    return 301 https://$host$request_uri; # Redireccionar HTTP a HTTPS automáticamente
}

server {
    listen 443 ssl http2;
    server_name api.copia.transporte.com;

    # Certificados SSL emitidos por Let's Encrypt CA
    ssl_certificate /etc/letsencrypt/live/api.copia.transporte.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.copia.transporte.com/privkey.pem;

    # Forzar TLS 1.2 y TLS 1.3 con suites de cifrado seguras (ECDHE)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000; # Redirección interna a Uvicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### B. Hardening de la Base de Datos MySQL
Para asegurar la base de datos MySQL (ACT-01), se deshabilita la posibilidad de que el usuario `root` inicie sesión de forma remota, se obliga a usar SSL/TLS en las conexiones por red y se modifica el archivo `/etc/mysql/my.cnf`.

#### Modificaciones al Archivo `/etc/mysql/my.cnf` (Bloqueo de red y SSL):
```ini
[mysqld]
# Enlazar únicamente a la interfaz de la VLAN 20 de base de datos
bind-address = 192.168.20.10

# Deshabilitar la resolución DNS inversa para mitigar ataques DoS
skip-name-resolve

# Forzar cifrado SSL/TLS para todos los clientes conectados por red
require_secure_transport = ON
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem
```

#### Sentencias SQL de Configuración de Usuarios (Mínimo Privilegio):
```sql
-- 1. Eliminar acceso de root remoto y local sin contraseña
ALTER USER 'root'@'localhost' IDENTIFIED BY 'K9$mP2!xQ8zW';

-- 2. Eliminar usuarios anónimos y bases de datos de prueba
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.user WHERE User='';

-- 3. Crear usuario con privilegios mínimos para la aplicación FastAPI
CREATE USER 'copia_app'@'192.168.30.20' IDENTIFIED BY 'App_S3cur3_Pa$$w0rd' REQUIRE SSL;
GRANT SELECT, INSERT, UPDATE ON copia.* TO 'copia_app'@'192.168.30.20';

-- 4. Aplicar cambios
FLUSH PRIVILEGES;
```

---

## Sección 2: Gestión de Parches y Planes de Continuidad

### A. Políticas de Actualización y Parches de Sistemas Operativos
* **Flota Móvil (Raspberry Pi OS)**: Se programa un cronjob mensual en la flota para actualizar los paquetes de seguridad críticos, ejecutando de forma automatizada:
  ```bash
  sudo apt-get update && sudo apt-get install --only-upgrade -y raspberrypi-sys-mods raspi-config
  ```
* **Servidores del Datacenter (Ubuntu Server)**: Se implementa la utilidad `unattended-upgrades` para instalar actualizaciones de seguridad de forma diaria sin requerir intervención humana, reportando las fallas al servidor Zabbix.

### B. Planes de Continuidad de Negocio
Se configuran respaldos automatizados de la base de datos MySQL relacional a través de un script en Bash programado diariamente a las 02:00 AM. Los backups son cifrados localmente utilizando GPG con cifrado simétrico AES-256 antes de ser enviados por SSH/SFTP a un servidor de almacenamiento externo offline situado en una subred de gestión aislada.

---

## Sección 3: Monitoreo y Mejora (KPIs & Vulnerabilidades)

### A. KPIs de Seguridad de la Información
Para evaluar la efectividad de los controles de seguridad en producción se miden mensualmente los siguientes indicadores:

1. **Tasa de Intentos de Acceso Fallidos (TIAF)**:
   $$\text{TIAF} = \frac{\text{Intentos fallidos de inicio de sesión}}{\text{Intentos de inicio de sesión totales}} \times 100$$
   *Umbral esperado: $< 5\%$. Alertas críticas si supera el 10% (posible ataque de fuerza bruta).*
2. **Cobertura de Parches en Dispositivos Edge (CPDE)**:
   $$\text{CPDE} = \frac{\text{Raspberry Pi con parches de seguridad al día}}{\text{Total de Raspberry Pi activas}} \times 100$$
   *Umbral esperado: $100\%$ (Margen máximo de desfase: 15 días).*
3. **Exposición de Puertos Abiertos**: Auditoría semanal con Nmap en el firewall perimetral. El único puerto externo permitido debe ser el puerto TCP 443 (HTTPS). Cualquier otro puerto detectado abierto genera un ticket de incidente crítico en Zabbix.

### B. Escaneo Proactivo de Vulnerabilidades
Se ejecutan análisis de seguridad trimestrales utilizando la herramienta automatizada **OpenVAS** sobre los servidores virtuales de la DMZ (VLAN 30) y el servidor de base de datos MySQL (VLAN 20). Los resultados y CVEs detectados se priorizan en un plan de remediación de deudas de seguridad.

---

## Sección 4: Declaración Ética ACM

El diseño, despliegue e infraestructura del sistema CopIA se rigen por los principios generales del Código de Ética y Conducta Profesional de la ACM:

### Principio 1.2: Evitar Daño
* **Aplicación en CopIA**: El procesamiento de imágenes faciales para detectar fatiga tiene como único propósito salvaguardar la vida del conductor y de terceros en la vía pública, evitando accidentes de tránsito fatales. El sistema no emite juicios morales ni aplica sanciones automáticas sobre el conductor; solo genera alertas preventivas en tiempo real.

### Principio 1.4: Ser Justo y Tomar Medidas para No Discriminar
* **Aplicación en CopIA**: El motor de visión por computadora utiliza clasificadores geométricos faciales (EAR, MAR, Pitch) adaptativos y redes neuronales ligeras entrenadas con datasets de alta variabilidad racial y de género (CEW, MRL Eye Dataset). La calibración dinámica inicial (los primeros 12 segundos del conductor) evita sesgos o falsos positivos ocasionados por la estructura facial individual del conductor o el uso de anteojos recetados.

### Principio 1.6: Respetar la Privacidad
* **Aplicación en CopIA**: Este es el pilar central del diseño. El sistema CopIA **no almacena ni transmite la grabación continua de video del conductor**. Las imágenes capturadas solo se analizan de manera volátil en la memoria RAM de la Raspberry Pi de cabina. Únicamente se guardan y transmiten instantáneas (snapshots de 35 KB) cuando el algoritmo detecta un evento severo de fatiga (riesgo $> 88$), sirviendo exclusivamente como evidencia técnica inmutable para auditoría.

### Cumplimiento de Privacidad y Consentimiento
1. **Consentimiento Informado**: Antes de iniciar la conducción, el operador y el conductor deben firmar un documento de consentimiento informado que describe exactamente qué datos captura el sistema, cómo se procesan y con quién se comparten.
2. **Cifrado en Reposo**: Las instantáneas de eventos de fatiga y la base de datos MySQL centralizada se almacenan en volúmenes cifrados utilizando algoritmos estándar de la industria (**AES-256**) a nivel de sistema operativo y almacenamiento RAID.
3. **Política de Retención y Purga de Datos**:
   * Las instantáneas de video e imágenes se conservan en el Datacenter por un período máximo de **90 días**, tras lo cual un script automático de limpieza las elimina de forma permanente.
   * Los registros de telemetría numéricos (EAR, MAR, porcentaje de riesgo) se conservan por **1 año** para análisis estadísticos e informes de seguridad de la empresa de transporte, antes de ser purgados o anonimizados.

---

## Anexos
1. **Reportes del Escáner OpenVAS**: Resumen en PDF de las últimas pruebas ejecutadas sobre la red local.
2. **Modelo de Formulario de Consentimiento Firmado**: Plantilla del documento de aceptación para los conductores de la flota.
