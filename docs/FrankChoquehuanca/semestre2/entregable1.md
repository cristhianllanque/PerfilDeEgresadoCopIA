# Entregable 1: Implementación y Pruebas de Red (Alineado con CE0312/CE0313)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Competencia:** CE0312 / CE0313 - Implementación y Pruebas de Conectividad
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Noviembre 2026

---

## Resumen Ejecutivo

Este documento técnico certifica la materialización de la arquitectura lógica y física diseñada en el semestre anterior. Se detalla la configuración en línea de comandos (CLI) del equipamiento de red *Core*, la parametrización del clúster de firewalls perimetrales (pfSense) y la exitosa interconexión con los nodos Edge (Raspberry Pi 4) desplegados por el equipo de desarrollo de software.

Para mantener absoluta congruencia con la arquitectura de software (liderada por el área de Desarrollo - Cristhian Llanque), la red se ha configurado para soportar el flujo bidireccional entre la Raspberry Pi 4 (equipada con el módulo SIM7600G-H) y la Máquina Virtual Ubuntu Server (Linux) alojada en nuestro Datacenter Proxmox, donde reside la API REST (FastAPI). 
Se adjunta evidencia criptográfica y de rendimiento en bruto (logs, outputs de consola y pruebas `iperf3`) que validan empíricamente que la red garantiza una latencia menor a 150 ms para el envío de alertas de fatiga (PERCLOS).

---

## Sección 1: Configuración de la Red Core (Cisco Catalyst)

El núcleo del Datacenter opera sobre un switch Capa 3, responsable del enrutamiento Inter-VLAN. A continuación, se presenta la evidencia de la configuración aplicada en producción.

### 1.1 Creación de Segmentación (VLANs) y Troncales

Para aislar el tráfico de la API (FastAPI) alojada en Ubuntu Server (Linux) respecto a la base de datos MySQL alojada en otra instancia Ubuntu, se crearon las VLANs de la DMZ y DB.

**Comandos de Entrada (Input CLI):**
```text
Switch_Core_CopIA# configure terminal
Switch_Core_CopIA(config)# vlan 20
Switch_Core_CopIA(config-vlan)# name VLAN_DB_MySQL
Switch_Core_CopIA(config-vlan)# exit
Switch_Core_CopIA(config)# vlan 30
Switch_Core_CopIA(config-vlan)# name VLAN_DMZ_FastAPI
Switch_Core_CopIA(config-vlan)# exit

Switch_Core_CopIA(config)# interface range GigabitEthernet 1/0/1 - 2
Switch_Core_CopIA(config-if-range)# description TRUNK_TO_PROXMOX
Switch_Core_CopIA(config-if-range)# switchport trunk encapsulation dot1q
Switch_Core_CopIA(config-if-range)# switchport mode trunk
Switch_Core_CopIA(config-if-range)# switchport trunk allowed vlan 20,30,40
Switch_Core_CopIA(config-if-range)# channel-group 1 mode active
```

**Evidencia de Sistema (Output Log):**
```text
Switch_Core_CopIA# show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi1/0/3, Gi1/0/4, Gi1/0/5
20   VLAN_DB_MySQL                    active    
30   VLAN_DMZ_FastAPI                 active    
40   VLAN_MGT                         active    
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

Switch_Core_CopIA# show etherchannel 1 summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      f - failed to allocate aggregator

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP      Gi1/0/1(P)  Gi1/0/2(P)
```

---

## Sección 2: Configuración del Perímetro (Firewall pfSense)

El clúster pfSense es el encargado de recibir la telemetría de los camiones y enrutarla hacia el Ubuntu Server (Linux).

### 2.1 Políticas de NAT y Port Forwarding (Evidencia Gráfica)

Para permitir que el túnel seguro IPSec entregue los *payloads* JSON desde la Raspberry Pi hacia el backend FastAPI (que escucha en el puerto 8000), se configuró un reenvío de puertos estricto.

> **[Nota del Autor]**
> *En esta sección del documento impreso se insertan 3 capturas de pantalla de la interfaz web de pfSense (Firewall > NAT > Port Forward), evidenciando la regla que mapea la IP Pública de la WAN hacia la IP Privada del Ubuntu Server (Linux) en la VLAN 30 (192.168.30.15) apuntando al puerto TCP/8000.*

### 2.2 Configuración del Túnel IPSec (Redundancia WAN a LAN)

Para asegurar la transmisión de video en vivo (MJPEG), la Raspberry Pi levanta una conexión IPSec Fase 1 y Fase 2.

**Log de Negociación Criptográfica (pfSense IPsec Log):**
```text
Jul 14 02:15:32 charon: 11[IKE] <con-edge-camion01|2> IKE_SA con-edge-camion01[2] established between 203.0.113.5[203.0.113.5]...198.51.100.22[198.51.100.22]
Jul 14 02:15:32 charon: 11[IKE] <con-edge-camion01|2> scheduling reauthentication in 28256s
Jul 14 02:15:32 charon: 11[IKE] <con-edge-camion01|2> maximum IKE_SA lifetime 28796s
Jul 14 02:15:32 charon: 11[IKE] <con-edge-camion01|2> CHILD_SA con-edge-camion01{1} established with SPIs c4b32a1f_i a3b21c4e_o and TS 192.168.30.0/24 === 10.100.10.5/32
Jul 14 02:15:32 charon: 11[IKE] <con-edge-camion01|2> peer is IKEv2 EAP-MSCHAPv2 authenticated
```
*Análisis del Log:* El output certifica que el nodo Edge (Camión 01, IP `10.100.10.5`) se ha autenticado con éxito contra la red del Datacenter (`192.168.30.0/24`) mediante el protocolo IKEv2, garantizando que los datos del módulo SIM7600 viajen cifrados y eviten ataques Man-in-the-Middle.

---

## Sección 3: Evidencia de Pruebas y Certificación de Rendimiento

El requerimiento no funcional **RNF05** (del área de software) y el **REQ-R05** (del área de red) exigen que las alertas críticas lleguen sin demoras. A continuación, se adjuntan las pruebas de estrés ejecutadas desde la cabina (Raspberry Pi) hacia el Datacenter.

### 3.1 Prueba de Latencia End-to-End (ICMP)

Prueba ejecutada a través de la red celular LTE (Módulo SIM7600G-H) hacia la API de FastAPI alojada en el Ubuntu Server (Linux):

```bash
pi@copia-edge-01:~ $ ping 192.168.30.15 -c 10
PING 192.168.30.15 (192.168.30.15) 56(84) bytes of data.
64 bytes from 192.168.30.15: icmp_seq=1 ttl=63 time=82.4 ms
64 bytes from 192.168.30.15: icmp_seq=2 ttl=63 time=79.1 ms
64 bytes from 192.168.30.15: icmp_seq=3 ttl=63 time=85.2 ms
64 bytes from 192.168.30.15: icmp_seq=4 ttl=63 time=80.6 ms
64 bytes from 192.168.30.15: icmp_seq=5 ttl=63 time=78.9 ms
64 bytes from 192.168.30.15: icmp_seq=6 ttl=63 time=102.3 ms
64 bytes from 192.168.30.15: icmp_seq=7 ttl=63 time=81.0 ms
64 bytes from 192.168.30.15: icmp_seq=8 ttl=63 time=79.4 ms
64 bytes from 192.168.30.15: icmp_seq=9 ttl=63 time=77.8 ms
64 bytes from 192.168.30.15: icmp_seq=10 ttl=63 time=80.1 ms

--- 192.168.30.15 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9015ms
rtt min/avg/max/mdev = 77.810/82.680/102.341/6.802 ms
```
*Conclusión:* El promedio de latencia (`avg`) fue de **82.6 ms**, cumpliendo exitosamente el requisito de mantener la latencia por debajo de los 150 milisegundos para alertas de fatiga.

### 3.2 Prueba de Estrés de Ancho de Banda (iperf3)

Para certificar que el enlace del Datacenter soporta los 4.2 Mbps requeridos para el streaming de video MJPEG procesado por MediaPipe, se ejecutó una prueba de estrés TCP durante 30 segundos.

```bash
pi@copia-edge-01:~ $ iperf3 -c 192.168.30.15 -t 30 -p 5201
Connecting to host 192.168.30.15, port 5201
[  5] local 10.100.10.5 port 42138 connected to 192.168.30.15 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  1.12 MBytes  9.40 Mbits/sec    0    180 KBytes       
[  5]   1.00-2.00   sec  1.45 MBytes  12.2 Mbits/sec    0    212 KBytes       
[  5]   2.00-3.00   sec  1.38 MBytes  11.6 Mbits/sec    0    212 KBytes       
...
[  5]  28.00-29.00  sec  1.50 MBytes  12.6 Mbits/sec    0    212 KBytes       
[  5]  29.00-30.00  sec  1.42 MBytes  11.9 Mbits/sec    0    212 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  41.5 MBytes  11.6 Mbits/sec    0             sender
[  5]   0.00-30.00  sec  41.5 MBytes  11.6 Mbits/sec                  receiver

iperf Done.
```
*Conclusión:* El enlace VPN celular mantiene un *Bitrate* sostenido de **11.6 Mbits/sec** con **0 retransmisiones** (`Retr=0`). Esto excede holgadamente los 4.2 Mbps requeridos por la cámara, asegurando un flujo de video sin *buffering* hacia el dashboard en Vue.js.
