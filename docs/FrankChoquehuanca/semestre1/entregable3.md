# Entregable 3: Diseño de Centro de Datos (Alineado con CE0331)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Entregable:** Entregable 3: Diseño de Centro de Datos (CE0331)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo
Este documento describe el diseño preliminar y dimensionamiento físico y de hardware del Centro de Datos de **CopIA**. Justifica el cumplimiento de los estándares de disponibilidad **Tier III (Uptime Institute)**, realiza el dimensionamiento matemático detallado (sizing) del almacenamiento RAID 10 para soportar la telemetría de 50, 100, la flota actual de 150, y la escalabilidad futura de 500 vehículos, y describe la estructura de virtualización propuesta sobre el hipervisor Proxmox para segregar de forma segura la API, Base de Datos e interfaces de gestión.

---

## Sección 1: Diseño de Arquitectura de Datacenter (Tier III)

Para asegurar la continuidad operativa de la plataforma de monitoreo de fatiga de la flota de transportes, se propone un Datacenter corporativo que cumpla con los estándares de **Tier III (Uptime Institute)**:

* **Disponibilidad**: $99.982\%$, lo que equivale a un tiempo de inactividad máximo tolerado de **1.6 horas al año** (95.9 minutos).
* **Mantenimiento Concurrente**: Toda la infraestructura física (alimentación eléctrica, refrigeración de precisión, cables, UPS) cuenta con rutas de distribución redundantes ($N+1$). Cualquier componente puede ser retirado para mantenimiento preventivo o correctivo sin afectar el funcionamiento del servidor central de CopIA.
* **Respaldo Energético**: Dos generadores diésel redundantes con autonomía mínima de 72 horas a plena carga y dos bancos de UPS independientes que cubren la conmutación de energía sin interrupción de micro-cortes.

---

## Sección 2: Dimensionamiento Matemático de Capacidad (Sizing)

Para justificar técnicamente los recursos necesarios, se realiza el cálculo de almacenamiento requerido a largo plazo basándonos en datos reales de funcionamiento del sistema CopIA.

### A. Parámetros del Tráfico de Datos
1. **Mensaje de Telemetría JSON**: Pesa **1.2 KB** en promedio. Se envía cada **3 segundos** por vehículo.
2. **Duración de la Conducción**: Se asume un promedio de **12 horas de conducción diarias** por camión, los 365 días del año.
3. **Imágenes de Alertas (Snapshots)**: Ante eventos de fatiga severa (alerta crítica de parpadeo largo o bostezo), el cliente envía una captura de rostro que pesa **35 KB**. Se calcula un promedio histórico de **50 alertas con foto al día** por camión.
4. **Período de Retención Requerido**: **1 año (365 días)** para auditorías de seguridad vial.
5. **Factor de Sobrecarga de Base de Datos**: Multiplicador de **1.5x** para contemplar índices SQL, tablas temporales e historial de sesiones de conducción.

### B. Cálculo de Almacenamiento por Vehículo
#### 1. Datos de Telemetría (MySQL):
$$\text{Mensajes por día} = \frac{12\text{ horas} \times 3600\text{ segundos}}{3\text{ segundos}} = 14,400\text{ mensajes/día}$$
$$\text{Tamaño de Telemetría Diario} = 14,400 \times 1.2\text{ KB} = 17,280\text{ KB} \approx 17.28\text{ MB/día}$$
$$\text{Telemetría con Índices y Logs (1.5x)} = 17.28\text{ MB} \times 1.5 = 25.92\text{ MB/día}$$

#### 2. Datos de Alertas con Imágenes (Archivos JPG):
$$\text{Tamaño de Fotos Diario} = 50\text{ alertas} \times 35\text{ KB} = 1,750\text{ KB} \approx 1.75\text{ MB/día}$$

#### 3. Almacenamiento Total por Vehículo al Año:
$$\text{Almacenamiento Total Diario} = 25.92\text{ MB} + 1.75\text{ MB} = 27.67\text{ MB/día}$$
$$\text{Almacenamiento Total Anual por Vehículo} = 27.67\text{ MB} \times 365\text{ días} = 10,100\text{ MB} \approx \mathbf{10.1\text{ GB/año}}$$

### C. Escenarios de Escalabilidad de la Flota

Utilizando el valor de **10.1 GB por vehículo al año**, proyectamos la capacidad necesaria para los escenarios de flota requeridos:

| Métrica / Escenario | 50 Vehículos | 100 Vehículos | 150 Vehículos (Flota Actual) | 500 Vehículos |
| :--- | :--- | :--- | :--- | :--- |
| **Almacenamiento Útil Requerido (1 año)** | $505\text{ GB} \approx 0.51\text{ TB}$ | $1,010\text{ GB} \approx 1.01\text{ TB}$ | $1,515\text{ GB} \approx 1.52\text{ TB}$ | $5,050\text{ GB} \approx \mathbf{5.05\text{ TB}}$ |
| **Ancho de Banda de Entrada (Telemetría)** | $160\text{ kbps}$ | $320\text{ kbps}$ | $480\text{ kbps}$ | $1,600\text{ kbps} \approx 1.6\text{ Mbps}$ |
| **Consumo de Memoria RAM (FastAPI Cache)** | $512\text{ MB}$ | $1\text{ GB}$ | $1.5\text{ GB}$ | $4\text{ GB}$ |

### D. Justificación de Configuración RAID 10 para Almacenamiento

Para garantizar la alta velocidad de escritura requerida por las transacciones de MySQL y una tolerancia a fallos redundante, se implementa un arreglo **RAID 10 (1+0)**. 

#### Cálculo de Capacidad Bruta en Disco para la Flota Actual (150 Vehículos):
1. **Espacio Útil Requerido**: $1.52\text{ TB}$.
2. **Margen de Seguridad de Almacenamiento (30%)**:
   $$\text{Espacio Útil Objetivo} = 1.52\text{ TB} \times 1.30 = \mathbf{1.98\text{ TB}}$$
3. **Eficiencia de Almacenamiento de RAID 10**: $50\%$ (debido al espejo o *mirroring* de discos).
   $$\text{Capacidad Bruta Requerida} = \frac{\text{Espacio Útil Objetivo}}{\text{Eficiencia}} = \frac{1.98\text{ TB}}{0.50} = \mathbf{3.96\text{ TB}}$$

#### Cálculo de Capacidad Bruta en Disco para el escenario futuro (500 Vehículos):
1. **Espacio Útil Requerido**: $5.05\text{ TB}$.
2. **Margen de Seguridad de Almacenamiento (30%)**: Para evitar que los discos superen el 70% de su capacidad total (evitando degradación de performance de MySQL):
   $$\text{Espacio Útil Objetivo} = 5.05\text{ TB} \times 1.30 = \mathbf{6.57\text{ TB}}$$
3. **Eficiencia de Almacenamiento de RAID 10**: $50\%$ (debido al espejo o *mirroring* de discos).
   $$\text{Capacidad Bruta Requerida} = \frac{\text{Espacio Útil Objetivo}}{\text{Eficiencia}} = \frac{6.57\text{ TB}}{0.50} = \mathbf{13.14\text{ TB}}$$

#### Configuración Propuesta:
Se adquieren **4 discos duros Enterprise SAS de 4 TB** cada uno.
* **Capacidad Bruta Total**: $4 \times 4\text{ TB} = 16\text{ TB}$.
* **Capacidad Útil en RAID 10**: $8\text{ TB}$ (Cumple holgadamente con los $1.98\text{ TB}$ requeridos para la flota actual de 150 vehículos, y con los $6.57\text{ TB}$ requeridos para el escenario futuro de 500 vehículos).

---

## Sección 3: Esquema de Virtualización (Hypervisor)

Se implementa el hypervisor bare-metal **Proxmox VE 8.2** sobre un servidor físico Dell PowerEdge R760 (con 32 cores físicos y 64 GB de RAM), dividiendo los recursos en Máquinas Virtuales (VM) aisladas para segregar los servicios:

```
+-------------------------------------------------------------+
|              Proxmox VE 8.2 Hypervisor (Dell R760)          |
+-------------------------------------------------------------+
   | (2 vCPUs, 4GB RAM)   | (4 vCPUs, 8GB RAM)   | (4 vCPUs, 16GB RAM)
   v                      v                      v
+------------------+   +------------------+   +------------------+
|      VM 101      |   |      VM 102      |   |      VM 103      |
|    AD/DNS/IAM    |   | FastAPI Web/APIs |   |    MySQL Server  |
|  (VLAN 40 - Mgt) |   |    (VLAN 30 - DMZ) |   |  (VLAN 20 - DB)  |
+------------------+   +------------------+   +------------------+
```

---

## Anexos
1. **Especificaciones del Servidor Dell PowerEdge R760**: Fichas técnicas de procesador Intel Xeon y memoria ECC.
2. **Layout de Racks del Datacenter**: Distribución física de servidores, switches y UPS en el gabinete del rack de 42U.
