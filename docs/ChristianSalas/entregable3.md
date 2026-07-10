# ENTREGABLE 3: MEJORA DE PROCESOS

Evalúa: CE013 – Gestión de Procesos

## CE0131 – Identificación y Caracterización de Procesos Organizacionales

### 1.1 Catálogo de Procesos de Huaynaroque
| Código | Proceso | Nivel | Área Responsable | Criticidad |
|---|---|---|---|---|
| P01 | Asignación de conductores a rutas | Operativo | Operaciones | Alta |
| P02 | Monitoreo de conductores durante la ruta | Operativo | Operaciones / TI | Alta |
| P03 | Registro y gestión de incidentes viales | Operativo | Operaciones / Legal | Alta |
| P04 | Control de llegada y salida de vehículos | Operativo | Operaciones | Media |
| P05 | Mantenimiento preventivo de vehículos | Soporte | Mantenimiento | Alta |
| P06 | Liquidación de viajes y facturación | Administrativo | Administración | Media |
| P07 | Gestión de conductores (contratación, capacitación) | RRHH | Recursos Humanos | Media |
| P08 | Reporte de seguridad vial al MTC/SUTRAN | Regulatorio | Gerencia / Legal | Alta |

### 1.2 Proceso Seleccionado para Mejora
**Proceso foco: P02 – Monitoreo de conductores durante la ruta**
Justificación: Es el proceso con mayor impacto en la seguridad vial y el que presenta las brechas tecnológicas más críticas. Su automatización mediante CopIA representa el mayor retorno de valor para la organización.

### 1.3 Ficha de Caracterización del Proceso P02
| Atributo | Descripción |
|---|---|
| Nombre del proceso | Monitoreo de conductores durante la ruta |
| Objetivo | Detectar y gestionar estados de fatiga, somnolencia o distracción en conductores activos |
| Alcance | Desde el inicio del viaje hasta la llegada al destino |
| Entradas | Conductor asignado, vehículo con cámara, ruta planificada |
| Salidas | Registro de incidentes, alertas generadas, reporte de seguridad |
| Actividades principales | Captura de imagen, análisis de fatiga, generación de alerta, notificación a supervisor, registro del evento |
| Actores involucrados | Conductor, supervisor de flota, sistema CopIA, gerencia |
| Sistemas de soporte | CopIA DMS (propuesto), Firebase GPS, Dashboard React |
| Frecuencia | Continua (24/7 durante operación vehicular) |
| Indicadores actuales | N° accidentes por fatiga / mes; tiempo de respuesta ante incidente (manual) |
| Problemas identificados | Monitoreo manual e intermitente; sin registro digital de eventos; latencia alta en respuesta a incidentes |

## CE0132 – Modelado de Procesos AS-IS (Situación Actual)

### 2.1 Descripción Narrativa del Proceso Actual
En la actualidad, el monitoreo de conductores en Huaynaroque se realiza de forma manual y reactiva. El supervisor de operaciones llama periódicamente por teléfono o WhatsApp al conductor para verificar su estado. No existe ningún sistema automatizado de detección de fatiga. Si el conductor sufre un accidente por somnolencia, la respuesta es posterior al evento (reporte, atención médica, gestión del siniestro).

### 2.2 Flujo del Proceso AS-IS
| Paso | Actividad | Actor | Herramienta | Problema |
|---|---|---|---|---|
| 1 | Supervisor asigna ruta y conductor al inicio del día | Supervisor | Planilla Excel | Sin trazabilidad digital |
| 2 | Conductor inicia viaje sin registro de estado inicial | Conductor | Ninguna | Sin línea base de estado |
| 3 | Supervisor llama al conductor cada 2-3 horas | Supervisor | Celular/WhatsApp | Monitoreo intermitente |
| 4 | Conductor reporta estado verbalmente | Conductor | Celular | Información subjetiva; sin evidencia |
| 5 | Si hay incidente: conductor llama o para el vehículo | Conductor | Celular | Respuesta reactiva |
| 6 | Supervisor gestiona el incidente manualmente | Supervisor | Celular/Planilla | Demora en respuesta; sin registro formal |
| 7 | Se registra el incidente en planilla al final del día | Supervisor | Excel | Registro tardío; sin análisis preventivo |
| 8 | Gerencia revisa reportes semanales de incidentes | Gerencia | Excel/Reunión | Sin visibilidad en tiempo real |

### 2.3 Indicadores del Proceso AS-IS
| Indicador | Valor Actual | Fuente |
|---|---|---|
| Tiempo de detección de fatiga | No aplica (sin detección automática) | N/A |
| Tiempo de respuesta ante incidente | > 15 minutos (manual) | Estimado operacional |
| Frecuencia de monitoreo activo | 1 llamada cada 2-3 horas | Práctica actual |
| N° accidentes por fatiga / mes | [40-50] | Registros históricos empresa |
| Costo promedio por siniestro | S/. [12148.11] | Área administrativa |
| % de eventos registrados digitalmente | 0% | Sin sistema digital |

### 2.4 Diagrama BPMN AS-IS
*[Diagrama BPMN del proceso AS-IS – Insertar diagrama exportado desde Bizagi, Camunda Modeler o draw.io]*

## CE0133 – Modelado de Procesos TO-BE (Propuesta de Mejora)

### 3.1 Descripción del Proceso Propuesto con CopIA
Con la implementación de CopIA, el proceso de monitoreo de conductores se transforma de reactivo-manual a proactivo-automatizado. La detección de fatiga ocurre en tiempo real mediante visión artificial en la Raspberry Pi del vehículo. Las alertas se generan automáticamente tanto en la cabina (audio/visual) como en el servidor central, notificando al supervisor de forma inmediata.

### 3.2 Flujo del Proceso TO-BE
| Paso | Actividad | Actor | Herramienta CopIA | Mejora |
|---|---|---|---|---|
| 1 | Conductor se registra en el sistema al iniciar el viaje | Conductor / CopIA | App / API (/login) | Trazabilidad desde el inicio |
| 2 | Cámara en cabina inicia captura continua de video | CopIA Edge | raspberry_client.py + OpenCV | Monitoreo 100% continuo |
| 3 | Sistema calcula EAR, MAR, PERCLOS y PITCH/YAW en tiempo real | CopIA Edge | CopIASystem (IA) | Detección objetiva en ms |
| 4 | Si Risk Score supera umbral: alerta local en cabina | CopIA Edge | Audio + GUI (raspberry_gui.py) | Intervención inmediata al conductor |
| 5 | Telemetría y snapshot se transmiten al servidor | CopIA Edge | raspberry_client.py → API | Registro continuo en nube |
| 6 | API registra evento de fatiga en BD PostgreSQL | CopIA Cloud | api_main.py + SQLAlchemy | Trazabilidad persistente |
| 7 | Dashboard notifica al supervisor en tiempo real | CopIA Cloud + Frontend | React Dashboard + /api/status | Respuesta en < 30 segundos |
| 8 | Supervisor actúa: contacta al conductor o escala | Supervisor | Dashboard + Celular | Decisión informada y oportuna |
| 9 | Video en vivo disponible para revisión del supervisor | CopIA Cloud | /api/video_feed (MJPEG) | Evidencia visual en tiempo real |
| 10 | Todos los eventos quedan registrados para auditoría | CopIA Cloud | BD + Analytics | Reportería automática MTC/SUTRAN |

### 3.3 Diagrama BPMN TO-BE
*[Diagrama BPMN del proceso TO-BE – Insertar diagrama exportado desde Bizagi, Camunda Modeler o draw.io]*

## CE0134 – Propuesta de Automatización mediante TIC

### 4.1 Mapa de Automatizaciones por Actividad
| Actividad Manual (AS-IS) | Automatización TIC (TO-BE) | Tecnología CopIA |
|---|---|---|
| Llamada telefónica para monitorear conductor | Detección continua por visión artificial | OpenCV + CopIASystem en Raspberry Pi |
| Reporte verbal del estado del conductor | Métricas objetivas EAR/MAR/PERCLOS | Algoritmos de visión facial |
| Alerta manual por parte del supervisor | Alerta automática en cabina (audio/visual) | raspberry_gui.py + altavoces |
| Registro manual en Excel post-facto | Registro automático en BD al detectar evento | SQLAlchemy + PostgreSQL |
| Revisión de reportes semanales | Dashboard en tiempo real 24/7 | React + FastAPI /api/status |
| Sin evidencia de incidentes | Video en vivo y snapshots almacenados | MJPEG streaming + AWS S3 |
| Sin seguimiento de ubicación en tiempo real | Mapa GPS en tiempo real por vehículo | Firebase Realtime DB |

### 4.2 Integración TIC con el Ecosistema Organizacional
- CopIA se integra nativamente con Firebase para GPS sin requerir sistemas adicionales.
- La API REST de CopIA puede conectarse en el futuro con el sistema de facturación para liquidación automática de viajes.
- Los datos de eventos de fatiga alimentan el módulo de analítica para decisiones de RRHH (ranking de conductores).
- Los reportes automáticos pueden exportarse en formato MTC-compatible para cumplimiento regulatorio.

## CE0135 – Indicadores de Desempeño y Evaluación de Impacto

### 5.1 KPIs del Proceso TO-BE
| KPI | Descripción | Fórmula | Meta | Frecuencia |
|---|---|---|---|---|
| KPI-01 | Tiempo de detección de fatiga | Tiempo desde cierre de ojos > umbral hasta alerta | < 3 segundos | Continua |
| KPI-02 | Tiempo de respuesta del supervisor | Tiempo desde alerta hasta acción del supervisor | < 2 minutos | Por evento |
| KPI-03 | Precisión del modelo IA | Verdaderos positivos / (VP + FP + FN) | > 85% | Mensual |
| KPI-04 | Tasa de reducción de incidentes | (Incidentes mes anterior - mes actual) / anterior | > 40% anual | Mensual |
| KPI-05 | Uptime del sistema CopIA | Horas activo / horas operativas × 100 | > 99% | Mensual |
| KPI-06 | Cobertura de monitoreo | Vehículos con CopIA activo / total flota | 100% | Diaria |
| KPI-07 | Eventos de fatiga por conductor | N° alertas generadas por conductor / mes | Benchmark interno | Mensual |
| KPI-08 | Costo por incidente post-implementación | Costo total siniestros / N° siniestros | Reducción 30% | Trimestral |

### 5.2 Análisis Comparativo AS-IS vs TO-BE
| Dimensión | AS-IS | TO-BE | Mejora Estimada |
|---|---|---|---|
| Tiempo de detección de fatiga | No aplicable (sin detección) | < 3 segundos | ∞ (nueva capacidad) |
| Frecuencia de monitoreo | 1 vez / 2-3 horas | Continuo (30 fps) | +99.9% cobertura |
| Tiempo de respuesta ante incidente | > 15 minutos | < 2 minutos | -87% en tiempo |
| Costo de gestión de incidentes | Alto (manual + reactivo) | Bajo (automático + preventivo) | Estimado -30 a -50% |
| Trazabilidad de eventos | 0% (sin registro digital) | 100% (BD + logs) | +100% |
| Calidad de información | Subjetiva (verbal) | Objetiva (métricas IA) | Alta confiabilidad |
| Cumplimiento normativo MTC | Parcial / informal | Total / auditada | Cumplimiento completo |
