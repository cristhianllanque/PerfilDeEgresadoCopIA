# Entregable 3: Diseño Físico y Lógico del Centro de Datos (Alineado con CE0331)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Competencia:** CE0331 - Diseño de Centro de Datos y Sizing
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo

El núcleo de procesamiento central de CopIA no reside en la nube (Cloud Pública), sino en un modelo *On-Premise* debido a normativas estrictas de soberanía de datos y latencia. Este documento detalla la ingeniería detrás del Centro de Datos Corporativo que albergará las bases de datos de telemetría y el portal web de monitoreo.

El diseño del Datacenter se alinea conceptualmente con las exigencias del nivel **Tier III del Uptime Institute**, garantizando redundancia en la ruta de energía y enfriamiento, permitiendo el mantenimiento concurrente sin detener las operaciones logísticas de los camiones. Se expone un análisis minucioso de *Capacity Planning* (Dimensionamiento), proyectando el crecimiento exponencial del volumen de video y telemetría a lo largo de un horizonte de dos años. Finalmente, se diseña la distribución del Rack (Elevación) y la estrategia de virtualización mediante Hypervisores Tipo 1 (Proxmox VE), asegurando el aislamiento granular de los servicios críticos (Bases de datos vs. Frontend).

---

## Sección 1: Cumplimiento Normativo TIER III (Uptime Institute)

Para un sistema que previene accidentes de tránsito en tiempo real, el tiempo de inactividad (downtime) es inaceptable. Por ello, la sala de servidores se ha diseñado basándose en los parámetros de la clasificación **Tier III (Mantenimiento Concurrente)**.

### 1.1 Justificación Matemática de Disponibilidad
El nivel Tier III garantiza una disponibilidad del **99.982%** anual. Esto se traduce en un máximo de **1.6 horas de inactividad permitida por año**.
Para lograr esto, la infraestructura debe poseer $$N+1$$ en su diseño electromecánico:
* **Energía (Power):** El Datacenter cuenta con dos acometidas eléctricas (Subestación comercial A y B). Internamente, posee un Generador Diésel y dos bancos de UPS de doble conversión. Los servidores críticos poseen fuentes redundantes (Dual Power Supply), cada una conectada a una PDU diferente.
* **Enfriamiento (Cooling):** Se utilizan unidades de aire acondicionado de precisión tipo CRAC (Computer Room Air Conditioning). Si la sala requiere 2 unidades para mantener 21°C, se instalan 3 ($$N+1$$). Así, el fallo de un compresor no eleva la temperatura del Rack.

### 1.2 Subsistema de Extinción de Incendios
Al albergar datos críticos de la empresa, no se pueden usar rociadores de agua (Sprinklers) sobre los servidores. El diseño contempla:
* Sensores de humo fotoeléctricos bajo el piso falso y sobre el techo raso.
* Extinción por gas **FM-200 (HFC-227ea)**, un agente limpio que suprime el fuego mediante inhibición química en menos de 10 segundos sin dejar residuos conductivos ni dañar los discos duros mecánicos.

---

## Sección 2: Elevación de Rack y Layout (Datacenter físico)

La organización física es crucial para el flujo de aire frío y la administración del cableado. Se utilizará un Gabinete estándar EIA-310 de 42 Unidades de Rack (42U).

### 2.1 Distribución Frontal (Elevación del Rack)

| Unidad (U) | Componente Instalado | Función | Consumo (W) Estimado |
| :--- | :--- | :--- | :--- |
| **U42 - U41** | *Vacío* (Reservado para crecimiento) | Expansión futura | 0W |
| **U40 - U39** | Panel de Parcheo Óptico (ODF) | Terminación de la fibra óptica del ISP | 0W |
| **U38** | Organizador de Cables Horizontal | Mantenimiento de Patch Cords | 0W |
| **U37** | Cisco Catalyst 9300 (Switch Core) | Enrutamiento Inter-VLAN | 350W |
| **U36** | Cisco Catalyst 1000 (Switch Mgt) | Red de administración (Out of Band) | 50W |
| **U35 - U33** | *Separación Térmica (Blind Panels)* | Evita mezcla de aire caliente/frío | 0W |
| **U32 - U31** | Netgate 6100 (FW Activo y Pasivo) | Clúster HA de Firewalls pfSense | 100W |
| **U30 - U25** | *Vacío* (Reservado) | Expansión futura | 0W |
| **U24 - U23** | Servidor Dell PowerEdge R750 (Nodo 1) | Hypervisor Proxmox (App & Web) | 700W |
| **U22 - U21** | Servidor Dell PowerEdge R750 (Nodo 2) | Hypervisor Proxmox (Base de Datos) | 700W |
| **U20 - U17** | SAN Storage (Dell PowerVault ME5) | Almacenamiento iSCSI crudo | 600W |
| **U16 - U05** | *Vacío* (Reservado) | Expansión futura | 0W |
| **U04 - U01** | Doble Banco UPS (APC Smart-UPS 3kVA) | Energía ininterrumpida de piso | --- |

*Nota Técnica: Las unidades UPS más pesadas siempre deben ir en el fondo (U01-U04) para bajar el centro de gravedad del Rack y evitar volcamientos ante sismos (Estándar NEBS).*

---

## Sección 3: Capacity Planning y Dimensionamiento (Sizing)

El hardware adquirido no se basa en suposiciones, sino en proyecciones matemáticas del crecimiento del negocio.

### 3.1 Sizing de Procesamiento (CPU y RAM)
Para soportar la ingesta concurrente de 150 vehículos, la arquitectura lógica en Proxmox se divide en tres Máquinas Virtuales (VMs) principales:

| Máquina Virtual | Función (Rol) | vCPU Asignados | RAM Asignada | SO Base |
| :--- | :--- | :--- | :--- | :--- |
| **VM-Nginx-API** | Proxy Reverso y Gateway de la API REST. | 8 Cores | 16 GB | Ubuntu Server 24.04 |
| **VM-MySQL-DB** | Base de datos relacional para Telemetría. | 16 Cores | 64 GB | Ubuntu Server 24.04 |
| **VM-Zabbix-Mon**| Servidor central de recolección SNMP/Alertas. | 4 Cores | 8 GB | Ubuntu Server 24.04 |

El Servidor Físico (Dell R750) cuenta con 2 procesadores Intel Xeon Gold (64 Cores totales) y 256 GB de RAM, lo que nos deja un **margen de crecimiento libre del 50%** para instanciar futuras VMs sin comprar hardware nuevo.

### 3.2 Sizing de Almacenamiento (Proyección a 1 Año para 150 Vehículos)

El cálculo del disco duro es el aspecto más crítico. Debemos prever el crecimiento (Data Growth) de los registros JSON y los recortes de video para la flota actual de 150 vehículos.

* **Telemetría JSON:**
  * Estimación de ingesta constante generada por los 150 vehículos operando en rutas nacionales.
  * Volumen proyectado anual: **0.42 TB anuales**.

* **Grabación de Eventos Críticos (Video MJPEG):**
  * Estimación de almacenamiento de clips de 15 segundos ante detecciones de fatiga severa (micro-sueños).
  * Volumen proyectado anual: **1.10 TB anuales**.

**Consolidación de Capacidad:**
* **Almacenamiento Útil Requerido:** 0.42 TB + 1.10 TB = **1.52 TB útiles**.
* **Almacenamiento Bruto Requerido (RAID 10 + Overhead):** Para obtener 1.52 TB útiles en un arreglo RAID 10 (donde la capacidad se reduce a la mitad por el espejo), y sumando un overhead del sistema de archivos ZFS, se requieren matemáticamente **3.96 TB brutos** en discos físicos.

Para satisfacer esta demanda y permitir un futuro escalamiento a mediano plazo, se utilizará un arreglo de discos **RAID 10 (Striping + Mirroring)**. 
* Se comprarán **4 discos SAS de 4 TB** cada uno.
* Capacidad Total Bruta = **16 TB brutos**.
* Capacidad Efectiva (RAID 10) = **8 TB utilizables**.

Esto asegura que el Datacenter resistirá holgadamente los 1.52 TB proyectados para este año y soportará el crecimiento operativo ininterrumpido sin necesidad de agregar discos al chasis a corto plazo.

---

## Sección 4: Arquitectura de Virtualización Lógica

El hardware físico está abstraído mediante el hypervisor Tipo 1 **Proxmox VE (Virtual Environment)**, de código abierto, lo que evita costos de licenciamiento de VMware ESXi.

### 4.1 Datastores y Segmentación Lógica
Proxmox utilizará **LVM-Thin** y **ZFS** como sistemas de archivos para las máquinas virtuales.
* **Storage Pool OS (ZFS RAID 1):** Discos de estado sólido (NVMe) de alta velocidad exclusivos para alojar el sistema operativo de las máquinas virtuales (arranques rápidos).
* **Storage Pool DATA (RAID 10 SAS):** Discos mecánicos empresariales diseñados para soportar millones de ciclos de lectura/escritura (IOPS) de la base de datos MySQL, donde reside verdaderamente la información masiva del proyecto CopIA.

### 4.2 Análisis de Riesgos y Puntos Únicos de Falla (SPOF) en Virtualización

**Beneficios:** La separación lógica en Proxmox garantiza un aislamiento de seguridad (Sandboxing); si la VM de la API (VLAN 30) es comprometida, el atacante no tiene acceso directo al sistema de archivos de la base de datos (VLAN 20).

**Riesgos Técnicos (SPOF Físico):** Al consolidar las tres máquinas virtuales (API, BD, Monitoreo) en un único servidor Dell R750, un fallo crítico de la placa madre destruiría la operatividad total del sistema simultáneamente.

**Mitigación:** Se contempla en el Roadmap de infraestructura la futura adquisición de un segundo servidor Dell R750 para habilitar un clúster de Alta Disponibilidad (Proxmox HA), permitiendo la migración en vivo de las VMs.
