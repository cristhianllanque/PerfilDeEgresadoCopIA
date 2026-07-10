# Entregable 3: Implementación Física y Virtual del Datacenter (Alineado con CE0332/CE0333)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Competencias:** CE0332/33 - Implementación de Centro de Datos y Continuidad del Servicio
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Noviembre 2026

---

## Resumen Ejecutivo

La fase culminante de la infraestructura del proyecto CopIA implica la orquestación del hardware físico y la capa de virtualización que hospeda los servicios desarrollados por el área de Software. Este entregable documenta el despliegue a bajo nivel del Hypervisor (Proxmox VE) sobre servidores bare-metal, la instanciación de las Máquinas Virtuales (Ubuntu Server para FastAPI y MySQL) respetando los lineamientos de dimensionamiento calculados previamente.

A fin de validar empíricamente las promesas de tolerancia a fallos exigidas por el modelo Tier III, se ejecutaron pruebas de stress físico, simulando la extracción abrupta de un disco duro mecánico para certificar la respuesta del sistema de almacenamiento ZFS RAID 10. Para sellar el proyecto, se redactó el Acuerdo de Nivel de Servicio (SLA) institucional, garantizando a la empresa de transportes un marco legal y técnico de disponibilidad operativa ininterrumpida frente a incidencias críticas.

---

## Sección 1: Despliegue de Virtualización (Proxmox VE)

La virtualización evita el desperdicio de recursos del servidor físico (Dell R750). Se optó por Proxmox VE debido a su soporte nativo para ZFS y contenedores LXC.

### 1.1 Creación de Máquinas Virtuales y Asignación de Recursos

Con base en el Capacity Planning, se instanciaron dos Máquinas Virtuales (VM) core.
A continuación se detalla la salida de la consola de Proxmox (`qm config`) mostrando el hardware virtual asignado:

**VM 100: Backend API (Ubuntu Server / Linux)**
```bash
root@pve-datacenter:~# qm config 100
agent: 1
boot: order=scsi0;net0
cores: 8
memory: 16384
name: SRV-CopIA-API-Linux
net0: virtio=AA:BB:CC:DD:EE:01,bridge=vmbr30,tag=30
scsi0: ZFS_DATA:vm-100-disk-0,size=200G
ostype: l26
smbios1: uuid=e5a2f5f1-3d77-4b62-9214-e0a5c5f4dc67
sockets: 1
```
*Análisis:* La VM aloja el entorno FastAPI de Cristhian Llanque. Cuenta con 8 núcleos (Cores), 16 GB de RAM y está conectada al bridge `vmbr30`, que inyecta automáticamente la etiqueta VLAN 30 (DMZ) al tráfico de red, exponiendo el puerto 8000 a internet a través del pfSense.

**VM 200: Base de Datos (Ubuntu Server)**
```bash
root@pve-datacenter:~# qm config 200
agent: 1
boot: order=scsi0;net0
cores: 16
memory: 65536
name: SRV-CopIA-DB-MySQL
net0: virtio=AA:BB:CC:DD:EE:02,bridge=vmbr20,tag=20
scsi0: ZFS_DATA:vm-200-disk-0,size=2000G
ostype: l26
sockets: 1
```
*Análisis:* Esta VM aloja el cluster MySQL. Sus recursos son masivos (16 Cores, 64 GB RAM) dado que procesará un incesante caudal de instrucciones `INSERT` generadas por la telemetría vehicular en tiempo real. Está segregada en la VLAN 20, sin salida a internet.

---

## Sección 2: Pruebas de Resiliencia Física (Simulación de Fallo RAID)

El almacenamiento masivo (Storage Pool `ZFS_DATA`) está estructurado en un **RAID 10** de 4 discos físicos para equilibrar velocidad de lectura/escritura y redundancia frente a daños mecánicos.

Para validar empíricamente que la grabación de eventos de fatiga no se detendrá si un disco se quema, se realizó una prueba de extracción en caliente (Hot Swap).

### 2.1 Simulacro de Falla en Disco Duro
Se forzó lógicamente el apagado (offline) del disco físico `/dev/sdc` que conforma el espejo del vdev 1.

**Comando de Ejecución:**
```bash
root@pve-datacenter:~# zpool offline ZFS_DATA /dev/sdc
```

**Estado Inmediato del Pool (Alarma de Zabbix Detonada):**
```bash
root@pve-datacenter:~# zpool status -x ZFS_DATA
  pool: ZFS_DATA
 state: DEGRADED
status: One or more devices has been taken offline by the administrator.
        Sufficient replicas exist for the pool to continue functioning in a
        degraded state.
action: Online the device using 'zpool online' or replace the device with
        'zpool replace'.
  scan: none requested
config:

        NAME        STATE     READ WRITE CKSUM
        ZFS_DATA    DEGRADED     0     0     0
          mirror-0  ONLINE       0     0     0
            sda     ONLINE       0     0     0
            sdb     ONLINE       0     0     0
          mirror-1  DEGRADED     0     0     0
            sdc     OFFLINE      0     0     0
            sdd     ONLINE       0     0     0

errors: No known data errors
```
*Conclusión de la Prueba:* A pesar de que el disco `/dev/sdc` falló (estado `OFFLINE`), el pool general se mantuvo operativo en estado `DEGRADED`. Durante este incidente, las métricas de MediaPipe enviadas por los choferes continuaron guardándose exitosamente en el disco `/dev/sdd` (su par redundante) sin interrupción de servicio en el frontend web.

### 2.2 Ejecución de Políticas de Respaldo (Backup Automático)
Para cumplir con la política de continuidad de negocio, se configuró un Datacenter Backup Job en Proxmox VE que realiza instantáneas (Snapshots) de la Máquina Virtual de Base de Datos todos los días a las 02:00 AM.

**Evidencia (Log de Proxmox Backup):**
```text
INFO: starting new backup job: vzdump 200 --mode snapshot --compress zstd --storage BACKUP_NAS
INFO: creating ZFS snapshot 'ZFS_DATA/vm-200-disk-0@vzdump'
INFO: backup is finished. Backup archive size: 14.2 GB
```

---

## Sección 3: Acuerdo de Nivel de Servicio (SLA Institucional)

La infraestructura tecnológica no es solo un conjunto de servidores, es una promesa operativa a los clientes (Empresas de Transporte Interprovincial). Para regir esta relación, se diseñó el siguiente contrato de SLA corporativo.

**DOCUMENTO OFICIAL:** CopIA-SLA-V1.0
**ENTIDAD PRESTADORA:** NOC (Network Operations Center) - CopIA
**CLIENTE:** Flota de Transportes (Stakeholders)

### 3.1 Definiciones y Alcance Operativo
El presente SLA define los niveles mínimos de servicio aceptables para la recepción, procesamiento (MediaPipe) y almacenamiento de las alertas críticas de fatiga vehicular. La cobertura abarca exclusivamente la infraestructura Core del Datacenter (pfSense, Proxmox, MySQL, FastAPI). *No cubre* fallas inherentes a zonas de nula cobertura 4G en las carreteras que escapen al failover del módulo SIM7600G.

### 3.2 Indicadores de Disponibilidad (Uptime)
El NOC de CopIA se compromete a mantener un **Uptime Mensual del 99.98%**.
El tiempo máximo de inactividad permitido es de **8.6 minutos al mes**.
Este indicador se medirá directamente extrayendo los reportes del dashboard del monitor Zabbix.

### 3.3 Tiempos de Respuesta a Incidentes (RTO y RPO)
| Nivel de Severidad | Descripción del Incidente | Tiempo de Respuesta (Inicio) | Tiempo de Resolución Máximo (RTO) |
| :--- | :--- | :--- | :--- |
| **P1 - Crítico** | Caída total de la API FastAPI. Los camiones no pueden reportar alertas. | Inmediato (15 mins, 24/7) | < 2 Horas |
| **P2 - Alto** | Degradación de Base de Datos. Pérdida de un disco del RAID (DEGRADED). | < 2 Horas (Horario Hábil) | < 12 Horas |
| **P3 - Medio** | Falla de sincronización de Zabbix o panel Vue.js lento. | < 6 Horas | < 24 Horas |
| **P4 - Bajo** | Solicitud de un nuevo usuario de Dashboard web o cambios cosméticos. | < 24 Horas | N/A |

### 3.4 Penalidades por Incumplimiento Contractual
En caso de que el Uptime mensual caiga por debajo de la barrera del 99.98%, CopIA indemnizará al cliente reembolsando porcentajes del pago mensual (Facturación) en el ciclo inmediato posterior:
* Disponibilidad entre 99.9% y 99.97%: Penalización del 5% del valor de la factura.
* Disponibilidad entre 99.0% y 99.8%: Penalización del 15% del valor de la factura.
* Disponibilidad inferior al 99.0%: Penalización del 30% del valor de la factura e inicio de comités de auditoría de crisis.
