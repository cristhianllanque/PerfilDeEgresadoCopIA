# Arquitectura de Infraestructura Tecnológica - CopIA (CE03)

Este directorio contiene toda la documentación técnica de infraestructura que da soporte al sistema de monitoreo de fatiga **CopIA**, dividida por semestres académicos y alineada con las competencias de la carrera de Ingeniería de Sistemas.

---

## Estructura del Directorio

### [Semestre 1: Diseño Preliminar](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre1/)
1. **[Entregable 1: Diseño de Red (CE0311)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre1/entregable1.md)**:
   * Detalla el levantamiento de requerimientos de red (concurrencia y anchos de banda para 150 vehículos).
   * Presenta la topología lógica (IPSec VPN y segmentación por VLANs).
   * Incorpora el análisis de redundancia física y el cumplimiento de estándares internacionales (IEEE 802.1Q, TIA/EIA-568-D).
2. **[Entregable 2: Planificación de Seguridad (CE0321)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre1/entregable2.md)**:
   * Identifica y clasifica los activos críticos de información bajo directrices ISO 27001.
   * Contiene la matriz de riesgos bajo la norma ISO 27005 / NIST.
   * Define las políticas de seguridad organizacional y la matriz de responsabilidades RACI.
3. **[Entregable 3: Diseño de Centro de Datos (CE0331)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre1/entregable3.md)**:
   * Detalla la arquitectura de Datacenter compatible con Tier III (Uptime Institute).
   * Contiene el dimensionamiento matemático detallado (sizing) del almacenamiento RAID 10 para soportar la telemetría de la flota actual de 150 vehículos (y escalabilidad a 500).
   * Describe el esquema de virtualización sobre Proxmox VE.

### [Semestre 2: Implementación y Operación](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre2/)
1. **[Entregable 1: Implementación y Testing de Red (CE0312/13)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre2/entregable1.md)**:
   * Presenta los comandos reales de configuración Cisco CLI para switches L2 y router L3.
   * Detalla las listas de control de acceso (ACL) aplicadas en el firewall/router para aislar la base de datos y permitir salida segura a Firebase.
   * Define el plan de monitoreo SNMP con Zabbix y las pruebas de rendimiento de red (iperf3, latencia, packet loss).
2. **[Entregable 2: Seguridad y Ética ACM (CE0322/23/24)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre2/entregable2.md)**:
   * Detalla la configuración de controles técnicos de seguridad (cifrado TLS en Nginx proxy y hardening MySQL).
   * Describe la automatización de parches de seguridad (cronjobs, unattended-upgrades).
   * Define los KPIs de seguridad y escaneos de vulnerabilidades con OpenVAS.
   * Presenta la declaración de ética ACM respecto al monitoreo biométrico y retención de datos.
3. **[Entregable 3: Implementación y Control de Centro de Datos (CE0332/33)](file:///c:/PerfilDeEgresadoCopIA/docs/FrankChoquehuanca/semestre2/entregable3.md)**:
   * Presenta la configuración local de red y aislamiento a nivel de OS mediante iptables.
   * Contiene los comandos del gestor de discos `mdadm` para el aprovisionamiento de RAID 10.
   * Define los acuerdos de nivel de servicio (SLA, RTO, RPO).
   * Evalúa la eficiencia energética mediante el cálculo del indicador PUE.

---

## Relación entre el Software CopIA y su Infraestructura

```
                      +---------------------------------------+
                      |         CopIA Edge Client (IoT)       |
                      |    (Raspberry Pi en 150 camiones)     |
                      +-------------------+-------------------+
                                          |
                                          v (IPSec VPN / LTE)
                                          |
                      +-------------------+-------------------+
                      |      Firewall Perimetral (pfSense)     |
                      |   (Redirección de puertos y ACLs)     |
                      +-------------------+-------------------+
                                          |
                                          v (VLAN DMZ / Red Local)
                                          |
                      +-------------------+-------------------+
                      |         CopIA FastAPI Backend         |
                      |        (Servidor Virtualizado)        |
                      +-------------------+-------------------+
                                          |
                                          v (VLAN DB / MySQL)
                                          |
                      +-------------------+-------------------+
                      |        Base de Datos (MySQL RAID)     |
                      +---------------------------------------+
```
