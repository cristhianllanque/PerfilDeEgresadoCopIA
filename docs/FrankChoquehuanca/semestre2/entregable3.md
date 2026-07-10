# Entregable 3: Implementación y Control de Centro de Datos (Alineado con CE0332 y CE0333)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Entregable:** Entregable 3: Implementación y Control de Centro de Datos (CE0332 y CE0333)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo
Este entregable detalla la implementación física y las configuraciones de control operativas del Centro de Datos del sistema **CopIA**. Se documentan los comandos reales utilizados para desplegar y verificar el almacenamiento en RAID 10 mediante la utilidad `mdadm` en Linux, las reglas de firewall local (iptables) que aíslan el servidor de base de datos a nivel de sistema operativo, las métricas del Acuerdo de Nivel de Servicio (SLA, RTO, RPO), y la evaluación cuantitativa de la eficiencia energética (PUE) del Datacenter local.

---

## Sección 1: Configuración de Servidores y Servicios

Para impedir que hosts externos o de la DMZ tengan acceso directo a puertos sensibles de administración de la base de datos (puerto TCP 3306), se configuran políticas restrictivas de firewall local mediante **iptables** en el servidor MySQL (192.168.20.10):

### Comandos de iptables en el servidor MySQL:
```bash
# 1. Establecer políticas por defecto a DROP
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# 2. Permitir tráfico de loopback y conexiones ya establecidas (VITAL para updates)
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 3. Permitir SSH (22) desde la red de gestión (VLAN 40) para el administrador
sudo iptables -A INPUT -p tcp -s 192.168.40.0/24 --dport 22 -j ACCEPT

# 4. Permitir conexiones a MySQL (3306) desde la IP de FastAPI
sudo iptables -A INPUT -p tcp -s 192.168.30.20 --dport 3306 -m state --state NEW -j ACCEPT

# 5. Permitir ICMP (ping) para Zabbix
sudo iptables -A INPUT -p icmp -s 192.168.40.50 -j ACCEPT

# 6. Guardar la configuración para persistir tras reinicios
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

---

## Sección 2: Implementación de Almacenamiento y Respaldos (RAID 10)

Durante el montaje físico de los discos SAS, se ejecuta la utilidad `mdadm` en Linux para construir el volumen de almacenamiento seguro RAID 10:

### Comandos de creación y verificación del RAID 10:
```bash
# 1. Crear el arreglo RAID 10 con 4 particiones de discos físicos
sudo mdadm --create --verbose /dev/md0 --level=10 --raid-devices=4 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1

# 2. Crear el sistema de archivos EXT4 en el volumen RAID creado
sudo mkfs.ext4 -F /dev/md0

# 3. Montar el volumen en el directorio de MySQL y agregarlo al fstab
sudo mount /dev/md0 /var/lib/mysql
echo "/dev/md0  /var/lib/mysql  ext4  defaults,nofail,noatime  0  2" | sudo tee -a /etc/fstab

# 4. Devolver la propiedad del directorio al usuario mysql
sudo chown -R mysql:mysql /var/lib/mysql
sudo chmod 700 /var/lib/mysql

# 5. Reiniciar el servicio para que tome el nuevo almacenamiento
sudo systemctl restart mysql

# 6. Verificar el estado operativo y de sincronización del arreglo RAID 10
cat /proc/mdstat
```
*La salida de `/proc/mdstat` debe mostrar que el arreglo está activo (`active raid10`) y con todos los dispositivos online (`[UUUU]`).*

---

## Sección 3: Definición de SLA y Monitoreo

Para los operadores de monitoreo en la oficina central, se define formalmente el siguiente Acuerdo de Nivel de Servicio:

* **SLA de Disponibilidad**: **99.9% mensual** (Tiempo máximo de indisponibilidad tolerada de **43.8 minutos al mes**).
* **Métrica de Pérdida de Datos (RPO - Recovery Point Objective)**: Máximo **10 segundos** de pérdida de telemetría gracias al almacenamiento en disco local del cliente en cabina ante desconexiones.
* **Tiempo de Recuperación de Servicio (RTO - Recovery Time Objective)**: Menos de **15 minutos** para restaurar el servicio de API ante una caída severa del servidor mediante failover automatizado de la máquina virtual en Proxmox High Availability.

---

## Sección 4: Procedimientos Operativos y Eficiencia (PUE)

El indicador **PUE (Power Usage Effectiveness)** define la eficiencia energética global del centro de datos local:

$$\text{PUE} = \frac{\text{Energía Total Consumida por el Datacenter}}{\text{Energía Consumida por Equipos de TI}}$$

* **Consumo de Equipos de TI (Servidores, Switches, Firewall)**: $4.5\text{ kW}$
* **Consumo de Infraestructura de Soporte (Aire acondicionado de precisión, UPS, Iluminación)**: $3.1\text{ kW}$
* **Energía Total del Datacenter**: $4.5\text{ kW} + 3.1\text{ kW} = 7.6\text{ kW}$
* **Cálculo del PUE de la propuesta**:
  $$\text{PUE} = \frac{7.6\text{ kW}}{4.5\text{ kW}} = \mathbf{1.69}$$
* **Análisis de Eficiencia**: Un PUE de 1.69 es calificado como "Eficiente" para datacenters locales de escala media. Para optimizarlo hacia 1.45 en la fase operativa, se implementará un esquema de contención de pasillos fríos y calientes, lo que mejorará el coeficiente de transferencia de calor y reducirá el consumo del sistema de refrigeración de precisión.

---

## Anexos
1. **Reportes de Verificación `/proc/mdstat`**: Capturas del estado del RAID 10 durante simulaciones de desconexión de disco.
2. **Histórico de Logs de SLA**: Reporte mensual consolidado del tiempo de actividad de la API FastAPI.
