# Entregable 1: Implementación y Testing de Red (Alineado con CE0312 y CE0313)

## Portada
* **Título del Proyecto:** CopIA - Asistente de Conducción AI (Edge & Central Server)
* **Línea de Evaluación:** CE03: Infraestructura Tecnológica
* **Entregable:** Entregable 1: Implementación y Testing de Red (CE0312 y CE0313)
* **Responsable:** Frank Choquehuanca
* **Semestre:** X
* **Fecha:** Julio 2026

---

## Resumen Ejecutivo
Este entregable presenta la implementación física y lógica de la red corporativa del sistema **CopIA**, así como el protocolo de pruebas de conectividad y rendimiento del canal celular e inter-VLAN. Se detallan los comandos reales utilizados para configurar switches L2, subinterfaces y enrutamiento inter-VLAN (Router-on-a-Stick) en dispositivos Cisco, la implementación de Listas de Control de Acceso (ACL) para aislar activos críticos de información, y la configuración del agente SNMP con Zabbix Server 7.0 para el monitoreo en tiempo real de los nodos vehiculares y la red corporativa.

---

## Sección 1: Configuración de Dispositivos (Cisco CLI)

### Configuración de VLANs y Puertos Troncales en el Switch L2:
```ios
! Crear las VLANs en el switch
Switch# configure terminal
Switch(config)# vlan 10
Switch(config-vlan)# name VLAN_FLOTA
Switch(config-vlan)# exit
Switch(config)# vlan 20
Switch(config-vlan)# name VLAN_DB
Switch(config-vlan)# exit
Switch(config)# vlan 30
Switch(config-vlan)# name VLAN_DMZ
Switch(config-vlan)# exit
Switch(config)# vlan 40
Switch(config-vlan)# name VLAN_MGT
Switch(config-vlan)# exit

! Configurar el puerto de subida al Router/Firewall como Troncal (802.1Q)
Switch(config)# interface gigabitEthernet 0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20,30,40
Switch(config-if)# no shutdown

! Asignar puerto para la Raspberry Pi (Flota)
Switch(config)# interface fastEthernet 0/10
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10

! Asignar puerto para el Servidor Base de Datos
Switch(config)# interface fastEthernet 0/20
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 20

! Asignar puerto para el Servidor API / DMZ
Switch(config)# interface fastEthernet 0/30
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 30
```

---

## Sección 2: Implementación de Direccionamiento y Routing

### Configuración de Interfaces y Enrutamiento Inter-VLAN en el Router L3 (Router-on-a-Stick):
```ios
Router# configure terminal
Router(config)# interface gigabitEthernet 0/0
Router(config-if)# no shutdown

! Configurar subinterfaz para VLAN 10 (Flota)
Router(config)# interface gigabitEthernet 0/0.10
Router(config-subif)# encapsulation dot1Q 10
Router(config-subif)# ip address 10.100.10.1 255.255.255.0

! Configurar subinterfaz para VLAN 20 (Base de Datos)
Router(config)# interface gigabitEthernet 0/0.20
Router(config-subif)# encapsulation dot1Q 20
Router(config-subif)# ip address 192.168.20.1 255.255.255.0

! Configurar subinterfaz para VLAN 30 (DMZ)
Router(config)# interface gigabitEthernet 0/0.30
Router(config-subif)# encapsulation dot1Q 30
Router(config-subif)# ip address 192.168.30.1 255.255.255.0

! Configurar subinterfaz para VLAN 40 (Gestión)
Router(config)# interface gigabitEthernet 0/0.40
Router(config-subif)# encapsulation dot1Q 40
Router(config-subif)# ip address 192.168.40.1 255.255.255.0
```

---

## Sección 3: Controles de Acceso y Estándares (ACL)

### Lista de Control de Acceso (ACL) para Aislar la Base de Datos (VLAN 20):
```ios
! Bloquear todo acceso directo a la BD (VLAN 20) desde la Flota (VLAN 10)
Router(config)# ip access-list extended LIMITAR_ACCESO_DB
Router(config-ext-nacl)# deny ip 10.100.10.0 0.0.0.255 192.168.20.0 0.0.0.255

! Permitir tráfico de la DMZ (VLAN 30) a la BD (VLAN 20) solo al puerto MySQL (3306)
Router(config-ext-nacl)# permit tcp 192.168.30.0 0.0.0.255 host 192.168.20.10 eq 3306
Router(config-ext-nacl)# deny ip any 192.168.20.0 0.0.0.255
Router(config-ext-nacl)# permit ip any any
Router(config-ext-nacl)# exit

! Aplicar la ACL en la subinterfaz de base de datos
Router(config)# interface gigabitEthernet 0/0.20
Router(config-subif)# ip access-group LIMITAR_ACCESO_DB out
```

### Configuración para salida segura a Firebase:
```ios
! Permitir tráfico seguro (HTTPS) hacia los servicios en la nube (Firebase) para persistencia dual
Router(config)# ip access-list extended SALIDA_FIREBASE
Router(config-ext-nacl)# permit tcp 10.100.10.0 0.0.0.255 any eq 443
Router(config-ext-nacl)# permit tcp 192.168.30.0 0.0.0.255 any eq 443
Router(config-ext-nacl)# exit

! Aplicar la ACL para permitir salida a Firebase desde la Flota
Router(config)# interface gigabitEthernet 0/0.10
Router(config-subif)# ip access-group SALIDA_FIREBASE in
```

---

## Sección 4: Pruebas y Monitoreo (Testing & SNMP)

### A. Monitoreo SNMP (Zabbix Server 7.0)
Para supervisar la infraestructura se despliega una máquina virtual con **Zabbix Server 7.0** en la VLAN 40, aplicando el protocolo **SNMP v3** con autenticación y cifrado (SHA y AES):
* **Switches y Routers**: Traps y polling SNMP registran:
  * Latencia de los enlaces WAN corporativos (Uptime).
  * Ancho de banda consumido en los puertos troncales del switch Core.
  * Pérdida de paquetes en las interfaces del Firewall.
* **Clientes Edge (Raspberry Pi)**: Monitoreados con agente SNMP ligero:
  * Estado de conexión del túnel VPN (Alarmas si está offline por más de 15 segundos).
  * Temperatura de la CPU de la Raspberry Pi (para prevenir fallos térmicos en cabina).
  * Porcentaje de uso del almacenamiento SD.

### B. Protocolo de Pruebas de Rendimiento
Para validar cuantitativamente el comportamiento de la red ante escenarios de degradación de señal móvil 4G/5G, se mide el tráfico WAN:

1. **Prueba de Latencia (Ping)**:
   * **Método**: Ejecución de pings continuos (1000 paquetes) desde la Raspberry Pi hacia la API en la DMZ.
   * **Métrica Aceptable**: Latencia promedio $< 120\text{ ms}$ y desviación estándar (Jitter) $< 15\text{ ms}$.
2. **Prueba de Pérdida de Paquetes**:
   * **Método**: Simulación de pérdida en canal WAN celular de 0.5%, 1% y 5% mediante herramientas de control de tráfico en Linux (`tc qdisc`).
   * **Métrica Aceptable**: El cliente de CopIA debe reconectar automáticamente y encolar la telemetría localmente sin caídas del sistema cuando la pérdida sea $\le 2\%$.
3. **Prueba de Throughput (iperf3)**:
   * **Método**: Ejecución de test TCP con `iperf3` desde la VLAN 10 hacia la VLAN 30.
   * **Métrica Aceptable**: Capacidad de canal real $> 15\text{ Mbps}$ bidireccional estable.

---

## Anexos
1. **Capturas de Ejecución de Pruebas**: Resultados reales de `iperf3` y salidas de comandos `ping`.
2. **Logs del Servidor Zabbix**: Muestra del panel de visualización y plantillas SNMP aplicadas.
