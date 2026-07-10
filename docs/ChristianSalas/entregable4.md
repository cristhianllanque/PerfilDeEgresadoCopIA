# ENTREGABLE 4: SOLUCIÓN TÉCNICA INTEGRADA

Evalúa: CE014 – Gestión de Sistemas de Información

## CE0141 – Mapa del Ecosistema de Sistemas de Información

### 1.1 Sistemas de Información Actuales (Inventario)
| Sistema | Categoría | Función Principal | Integración Actual | Estado |
|---|---|---|---|---|
| Planillas Excel de viajes | Gestión operativa | Control de rutas y conductores | Ninguna | Operativo |
| Sistema de facturación legacy | ERP básico | Emisión de comprobantes | Ninguna | Operativo |
| WhatsApp Business | Comunicación | Coordinación con conductores | Ninguna | Operativo (informal) |
| GPS básico (independiente) | Rastreo vehicular | Ubicación de vehículos | Ninguna (aislado) | Operativo parcial |
| Firebase Realtime DB | GPS en tiempo real | Sincronización de ubicación GPS | CopIA (propuesto) | Por integrar |
| CopIA DMS | DMS / IA | Monitoreo de fatiga del conductor | Firebase + AWS | En desarrollo |

### 1.2 Mapa del Ecosistema TO-BE
| Capa | Sistema / Componente | Rol | Tecnología |
|---|---|---|---|
| IoT / Edge | CopIA Edge (Raspberry Pi) | Captura, análisis y alerta local | Python, OpenCV, PyTorch |
| Comunicación | API REST (FastAPI) | Hub de integración central | FastAPI, JWT, MJPEG |
| Datos | PostgreSQL | Persistencia de eventos y sesiones | SQLAlchemy ORM |
| Datos en tiempo real | Firebase Realtime Database | GPS y ubicación vehicular | Firebase SDK |
| Infraestructura | AWS EC2 / Cloud | Hosting del servidor central | AWS, Docker |
| Presentación | Dashboard React | Interfaz de administradores | React, Vite, Tailwind |
| Comunicación externa | SUTRAN / MTC API (futuro) | Reporte regulatorio automático | REST API (pendiente) |

## CE0142 – Arquitectura Conceptual del Sistema de Información

### 2.1 Descripción de la Arquitectura
CopIA implementa una arquitectura de tres capas (Edge – Cloud – Frontend) con un patrón cliente-servidor distribuido. El procesamiento primario ocurre en el edge (Raspberry Pi) para garantizar baja latencia en las alertas locales, mientras que el servidor central en la nube actúa como hub de integración, persistencia y distribución de información.

### 2.2 Componentes Principales y sus Responsabilidades
| Componente | Módulo/Archivo | Responsabilidad Principal |
|---|---|---|
| Edge – Captura | main.py | Orquestador principal del cliente edge; inicia todos los subsistemas |
| Edge – Análisis IA | app.core.copia_system.CopIASystem | Motor de IA para cálculo de EAR, MAR, PERCLOS, PITCH/YAW y Risk Score |
| Edge – Cliente | raspberry_client.py | Transmisión de telemetría y snapshots al servidor central vía HTTP |
| Edge – Interfaz | raspberry_gui.py | GUI local en cabina: alertas visuales y sonoras para el conductor |
| Cloud – API | api_main.py (FastAPI) | Endpoint central: recibe telemetría, gestiona estado de flota, streaming MJPEG |
| Cloud – BD | PostgreSQL + SQLAlchemy | Persistencia de SesionConduccion, EventoFatiga, datos de conductores |
| Cloud – GPS | sync_firebase_gps() | Proceso en segundo plano: sincroniza ubicación GPS desde Firebase |
| Cloud – Streaming | /api/video_feed | Convierte snapshots base64 en flujo MJPEG para dashboard |
| Frontend | React + Vite + Tailwind | Dashboard: mapa de flota, alertas en vivo, ranking de riesgo, analytics |

### 2.3 Diagrama de Arquitectura del Sistema
*[Insertar diagrama de arquitectura – Recomendado: Modelo C4 (Nivel 2: Contenedores) exportado desde draw.io o Structurizr]*

**Descripción textual del flujo:**
1. Raspberry Pi captura video del conductor → CopIASystem analiza métricas de fatiga.
2. Si Risk Score > umbral → Alerta local (audio + GUI) en cabina del conductor.
3. raspberry_client.py envía telemetría JSON + snapshot base64 → POST /api/telemetry.
4. api_main.py actualiza fleet_status en memoria → Si evento crítico: persiste en PostgreSQL.
5. sync_firebase_gps actualiza coordenadas GPS desde Firebase → fleet_status.
6. Dashboard React consulta /api/status → Muestra mapa + niveles de riesgo en tiempo real.
7. Supervisor solicita /api/video_feed → Recibe stream MJPEG del conductor.

## CE0143 – Modelo de Integración de Sistemas y Flujos de Información

### 3.1 Diagrama de Flujo de Información
*[Insertar diagrama de flujo de datos (DFD Nivel 1) del sistema CopIA – exportado desde draw.io o Lucidchart]*

### 3.2 Contratos de Integración (API Endpoints Principales)
| Endpoint | Método | Descripción | Datos de Entrada | Datos de Salida |
|---|---|---|---|---|
| /api/telemetry | POST | Recepción de telemetría del edge | JSON: ear, mar, perclos, pitch, yaw, risk_score, snapshot_b64, lat, lng | 200 OK / 4xx Error |
| /api/status | GET | Estado en vivo de toda la flota | Token JWT (header) | JSON: fleet_status (todos los vehículos) |
| /api/video_feed/{vehicle_id} | GET | Stream MJPEG del conductor | vehicle_id (path), Token JWT | multipart/x-mixed-replace (MJPEG) |
| /api/login | POST | Autenticación de conductor/supervisor | JSON: username, password | JSON: access_token (JWT) |
| /api/trip/start | POST | Inicio de sesión de conducción | JSON: conductor_id, vehiculo_id, ruta | JSON: sesion_id |
| /api/trip/end | POST | Fin de sesión de conducción | JSON: sesion_id | JSON: resumen de eventos |
| /api/analytics/ranking | GET | Ranking de riesgo por conductor | Token JWT, período (query) | JSON: ranking de conductores |

### 3.3 Flujo de Integración con Firebase GPS
- Firebase Realtime Database almacena la ubicación GPS de cada vehículo bajo la ruta: /vehicles/{vehicle_id}/location.
- El proceso sync_firebase_gps() en api_main.py escucha cambios en tiempo real mediante Firebase SDK.
- Las coordenadas actualizadas se integran en el fleet_status en memoria del servidor FastAPI.
- El dashboard React las visualiza en un mapa interactivo (Google Maps / Leaflet).

## CE0144 – Plan de Implementación y Gestión del Sistema

### 4.1 Fases de Implementación
| Fase | Actividades | Duración | Responsable |
|---|---|---|---|
| Fase 1: Preparación | Configuración de AWS, Firebase, entorno de desarrollo; adquisición de hardware | Semanas 1-2 | Equipo TI |
| Fase 2: Desarrollo Edge | Implementación de main.py, CopIASystem, raspberry_client.py, raspberry_gui.py | Semanas 3-6 | Equipo Dev |
| Fase 3: Desarrollo Cloud | API FastAPI: endpoints telemetría, GPS sync, streaming, autenticación, analytics | Semanas 4-8 | Equipo Dev |
| Fase 4: Desarrollo Frontend | Dashboard React: mapa, monitoreo, alertas, video, rankings | Semanas 6-10 | Equipo Dev |
| Fase 5: Integración | Pruebas de integración edge-cloud-frontend; ajuste de umbrales IA | Semanas 11-12 | Equipo Dev + QA |
| Fase 6: Piloto | Despliegue en 3 vehículos de prueba; recolección de retroalimentación | Semanas 13-14 | Equipo + Operaciones |
| Fase 7: Despliegue | Instalación en flota completa; capacitación final | Semanas 15-16 | Equipo + RRHH |

### 4.2 Plan de Gestión de Cambios
- Todo cambio en requerimientos deberá documentarse en un Formulario de Solicitud de Cambio (FSC).
- El PM evaluará el impacto en tiempo, costo y alcance antes de aprobar cualquier cambio.
- Los cambios aprobados se reflejarán en el backlog del sprint correspondiente.
- Se mantendrá un registro de cambios (change log) actualizado en el repositorio Git.

### 4.3 Plan de Continuidad Operativa
| Escenario de falla | Impacto | Estrategia de recuperación | RTO |
|---|---|---|---|
| Falla del servidor AWS | Sin monitoreo centralizado | Raspberry Pi continúa alertas locales; reconexión automática al recuperarse | < 5 min |
| Falla de Raspberry Pi en vehículo | Sin monitoreo en ese vehículo | Protocolo de swap; unidad de reemplazo en 24h | 24 horas |
| Pérdida de conectividad 4G | Sin telemetría en tiempo real | Cola local en Raspberry Pi; sincronización diferida al recuperar conectividad | < 30 min |
| Falla de Firebase GPS | Sin actualización de ubicación | Último GPS conocido; alerta al supervisor; GPS independiente como backup | < 1 hora |
| Brecha de seguridad en API | Exposición de datos | Rotación inmediata de tokens JWT; auditoría de logs; notificación a usuarios | < 2 horas |

## CE0145 – Indicadores de Uso, Valor y Mejora del Sistema

### 5.1 KPIs del Sistema de Información CopIA
| Código | KPI | Fórmula de Cálculo | Meta | Período |
|---|---|---|---|---|
| SI-01 | Disponibilidad del sistema | (Tiempo activo / Tiempo total) × 100 | > 99% | Mensual |
| SI-02 | Latencia de telemetría | Tiempo entre captura y registro en BD | < 2 segundos | Continua |
| SI-03 | Precisión del modelo de detección | Accuracy = (VP + VN) / Total | > 85% | Mensual |
| SI-04 | Tasa de eventos de fatiga detectados | N° eventos / total horas conducidas | Benchmark | Semanal |
| SI-05 | Cobertura de la flota monitoreada | (Vehículos activos / total flota) × 100 | 100% | Diaria |
| SI-06 | Tiempo promedio de alerta al supervisor | Tiempo desde evento hasta notificación | < 30 seg | Por evento |
| SI-07 | Uso del dashboard por administradores | N° sesiones activas / día | > [X] sesiones | Diaria |
| SI-08 | Reducción de incidentes viales | (Incid. mes anterior - actual) / anterior × 100 | > 40% anual | Mensual |
| SI-09 | ROI del sistema | (Beneficios - Costo) / Costo × 100 | > 100% en 12m | Anual |
| SI-10 | Satisfacción del equipo de monitoreo | Encuesta de usabilidad (escala 1-5) | > 4.0 / 5.0 | Semestral |

### 5.2 Tablero de Control de Valor del Sistema
| Dimensión de Valor | Indicador Clave | Estado Inicial (AS-IS) | Meta (TO-BE) | Período de Medición |
|---|---|---|---|---|
| Seguridad vial | Accidentes por fatiga / mes | [40-50] | Reducción 40% | Mensual |
| Eficiencia operativa | Tiempo de respuesta a incidentes | > 15 min | < 2 min | Por evento |
| Cobertura tecnológica | Flota con DMS activo | 0% | 100% | Al despliegue |
| Cumplimiento normativo | Eventos auditables registrados | 0% | 100% | Al go-live |
| Valor financiero | Reducción de costo por siniestros | Línea base | - 30% | Anual |
| Satisfacción del usuario | NPS conductores y supervisores | [] | > 70 | Semestral |

### 5.3 Plan de Mejora Continua
- **Ciclo 1 (Mes 1-3):** Ajuste de umbrales de EAR/MAR basado en datos reales de conductores de la flota.
- **Ciclo 2 (Mes 4-6):** Incorporación de alertas diferenciadas por nivel de riesgo (bajo/medio/alto/crítico).
- **Ciclo 3 (Mes 7-12):** Desarrollo de modelos predictivos de fatiga por conductor (ML sobre histórico).
- **Ciclo 4 (Año 2):** Integración con sistema de gestión de mantenimiento y ERP de la empresa.
- **Ciclo 5 (Año 3):** Plataforma abierta con API pública para integración con sistemas MTC/SUTRAN.
