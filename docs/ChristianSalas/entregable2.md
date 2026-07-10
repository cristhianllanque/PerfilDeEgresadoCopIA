# ENTREGABLE 2: PLAN DE GESTIÓN INTEGRAL

Evalúa: CE012 – Gestión de Proyectos

## CE0121 – Acta de Constitución del Proyecto (Project Charter)

| ACTA DE CONSTITUCIÓN DEL PROYECTO | |
|---|---|
| Nombre del Proyecto | CopIA – Sistema de Monitoreo de Conductores (DMS) para Huaynaroque |
| Código del Proyecto | COPIA-2026-GTI-001 |
| Fecha de Elaboración | Junio 2026 |
| Sponsor / Patrocinador | Alfredo Jesus Quispe Ccapa – Gerente General de Huaynaroque |
| Project Manager | Christian Wilbert Salas Yupanqui |
| Equipo del Proyecto | Christian Salas Yupanqui, Cristhian Llanque Tipo, Frank Choquehuanca Huayhua |
| Docentes supervisores | Abel Huanca |
| Presupuesto preliminar | S/. 295,524.17 |
| Fecha de inicio | 20/07/2026 |
| Fecha de fin estimada | 20/12/2026 |

### Descripción del Proyecto
CopIA es un Driver Monitoring System (DMS) que integra procesamiento local en Raspberry Pi (edge computing) con visión artificial para detectar somnolencia en conductores, y una API central en la nube (FastAPI/AWS) para monitoreo de flota en tiempo real, respaldado por un panel de control web (React + Vite).

### Objetivos del Proyecto
- Implementar el sistema CopIA en el 100% de la flota de Huaynaroque.
- Reducir los incidentes por fatiga del conductor en un 40% en el primer año.
- Garantizar monitoreo en tiempo real de toda la flota mediante dashboard centralizado.
- Cumplir con los requisitos de seguridad vial establecidos por el MTC y SUTRAN.

### Alcance Preliminar
**INCLUYE:**
- Desarrollo e implementación del módulo edge en Raspberry Pi (main.py, raspberry_client.py, raspberry_gui.py).
- Despliegue de la API central FastAPI (api_main.py) en servidor AWS.
- Integración con Firebase Realtime Database para sincronización GPS.
- Dashboard web React para administradores de flota.
- Capacitación al personal técnico y operativo.

**NO INCLUYE:**
- Mantenimiento preventivo de vehículos.
- Modificación del sistema de gestión ERP existente (si hubiera).
- Instalación de hardware de comunicaciones (antenas, routers) en vehículos.

### Restricciones y Supuestos
| Restricciones | Supuestos |
|---|---|
| Presupuesto fijo definido por la gerencia | Los vehículos tienen acceso a conectividad 4G en rutas principales |
| Plazo de implementación máximo: [5] meses | Los conductores recibirán capacitación antes del despliegue |
| Uso de infraestructura AWS con límite de costo mensual | La gerencia proveerá acceso a los vehículos para instalación |
| El sistema debe ser compatible con Raspberry Pi 4 | Firebase estará disponible con plan Spark o Blaze según necesidad |

### Criterios de Éxito
- Sistema operativo al 99% del tiempo durante el primer mes post-implementación.
- Detección de somnolencia con precisión mayor al 85% en condiciones reales.
- Aceptación del sistema por parte de los conductores mayor al 80%.
- Dashboard accesible desde navegador web sin latencia mayor a 3 segundos.

## CE0122 – Plan de Gestión del Proyecto

### 2.1 Enfoque Metodológico
El proyecto CopIA adoptará un enfoque híbrido: planificación predictiva (PMBOK) para las fases de diseño e infraestructura, y gestión ágil (Scrum) para el desarrollo iterativo del software (edge, API y frontend).

### 2.2 Gestión del Alcance
El alcance será controlado mediante un proceso formal de gestión de cambios. Cualquier modificación al alcance deberá ser aprobada por el PM y el sponsor antes de su implementación. Se utilizará una EDT/WBS para desglosar el trabajo y un diccionario de entregables para definir criterios de aceptación.

### 2.3 Gestión del Tiempo
El cronograma se gestionará mediante un diagrama de Gantt con hitos claramente definidos. Se realizarán revisiones semanales del avance y se aplicará análisis de valor ganado (EVM) para el control del proyecto.

### 2.4 Gestión de Costos
Se establecerá una línea base de costos desde el inicio del proyecto. Se controlará la ejecución presupuestal mensualmente, con alertas ante variaciones mayores al 10% del presupuesto planificado.

### 2.5 Gestión de Calidad
| Área de Calidad | Criterio | Herramienta |
|---|---|---|
| Código fuente | Cobertura de pruebas > 80% | pytest, unittest |
| API | Latencia < 200ms en endpoints críticos | Postman, Apache JMeter |
| Modelo IA | Precisión de detección > 85% | Métricas de accuracy, F1-score |
| Documentación | 100% de entregables según plantilla UPeU | Revisión docente |
| Seguridad | 0 vulnerabilidades críticas en auditoría | OWASP ZAP, revisión de código |

### 2.6 Gestión de Comunicaciones
| Información | Audiencia | Frecuencia | Canal |
|---|---|---|---|
| Reporte de avance semanal | PM + Docentes | Semanal | Email / Teams |
| Estado de sprints | Equipo de desarrollo | Diario (standup) | WhatsApp / Discord |
| Reporte ejecutivo | Sponsor / Gerencia | Mensual | Presentación PPT |
| Alertas de riesgo | PM + Sponsor | Al detectarse | Email urgente |
| Entregables académicos | Docentes UPeU | Según cronograma | Campus virtual |

## CE0123 – WBS y Cronograma del Proyecto

### 3.1 Estructura de Desglose del Trabajo (WBS)
| ID | Entregable / Paquete de Trabajo |
|---|---|
| **1.0** | **PROYECTO COPIA – DMS Huaynaroque** |
| 1.1 | Gestión del Proyecto |
| 1.1.1 | Planificación y constitución del proyecto |
| 1.1.2 | Monitoreo y control del proyecto |
| 1.1.3 | Cierre del proyecto |
| 1.2 | Análisis y Diseño del Sistema |
| 1.2.1 | Levantamiento de requerimientos |
| 1.2.2 | Diseño de arquitectura edge-cloud |
| 1.2.3 | Diseño de base de datos (PostgreSQL) |
| 1.2.4 | Diseño de interfaz del dashboard (Figma) |
| 1.3 | Desarrollo del Módulo Edge (Raspberry Pi) |
| 1.3.1 | Implementación de captura de video (OpenCV) |
| 1.3.2 | Integración del modelo CopIASystem |
| 1.3.3 | Cálculo de métricas EAR, MAR, PERCLOS |
| 1.3.4 | Sistema de alertas locales (audio/visual) |
| 1.3.5 | Cliente de transmisión de telemetría (raspberry_client.py) |
| 1.4 | Desarrollo del Servidor Central (FastAPI) |
| 1.4.1 | Configuración de infraestructura AWS |
| 1.4.2 | API de recepción de telemetría (/api/telemetry) |
| 1.4.3 | Integración con Firebase GPS |
| 1.4.4 | Streaming de video MJPEG (/api/video_feed) |
| 1.4.5 | Endpoints de gestión de conductores y sesiones |
| 1.4.6 | Módulo de analytics y ranking de riesgo |
| 1.5 | Desarrollo del Frontend (Dashboard) |
| 1.5.1 | Mapa de flota en tiempo real |
| 1.5.2 | Panel de monitoreo por conductor |
| 1.5.3 | Visualización de alertas y video en vivo |
| 1.5.4 | Módulo de reportes y estadísticas |
| 1.6 | Integración y Pruebas |
| 1.6.1 | Pruebas unitarias por módulo |
| 1.6.2 | Pruebas de integración edge-cloud |
| 1.6.3 | Pruebas de rendimiento y carga |
| 1.6.4 | Pruebas de aceptación con usuarios |
| 1.7 | Despliegue y Capacitación |
| 1.7.1 | Instalación en vehículos (piloto 3 unidades) |
| 1.7.2 | Capacitación a conductores y supervisores |
| 1.7.3 | Despliegue completo en flota |
| 1.8 | Documentación y Entregables Académicos |
| 1.8.1 | Documentación técnica del sistema |
| 1.8.2 | Manual de usuario y operaciones |
| 1.8.3 | Entregables GTI (E1–E4) |

### 3.2 Cronograma General (Hitos Principales)
| Hito | Descripción | Semana |
|---|---|---|
| H1 | Aprobación del Project Charter | S1 |
| H2 | Diseño de arquitectura completado | S3 |
| H3 | Módulo edge funcional (detección local) | S6 |
| H4 | API central desplegada en AWS | S8 |
| H5 | Dashboard con mapa y telemetría en vivo | S10 |
| H6 | Integración completa edge-cloud-frontend | S12 |
| H7 | Pruebas de aceptación con 3 vehículos piloto | S14 |
| H8 | Despliegue completo en flota | S16 |
| H9 | Sustentación final UPeU | S16 |

## CE0124 – Análisis Económico y Evaluación de Viabilidad

### 4.1 Presupuesto Detallado del Proyecto
| N° | Ítem | Unidad | Cant. | C. Unit. (S/.) | C. Total (S/.) |
|---|---|---|---|---|---|
| 1 | Raspberry Pi 4 | Und. | 150 | 1,200 | 180,000 |
| 2 | Cámara infrarroja | Und. | 150 | 300 | 45,000 |
| 3 | Pantalla | Und. | 150 | 200 | 30,000 |
| 4 | Localizador GPS | Und. | 150 | 270 | 40,500 |
| 5 | Botón de pánico | Und. | 150 | 50 | 7,500 |
| 6 | Servidor AWS EC2 (t3.medium, 6 meses) | Mes | 6 | 400 | 2,400 |
| 7 | Firebase Blaze Plan (si aplica) | Mes | 6 | 0 | 0 |
| 8 | Conectividad 4G SIM por vehículo (6 meses) | Mes/veh. | 900 | 30 | 27,000 |
| 9 | Horas de desarrollo del equipo | H/H | 500 | 30 | 15,000 |
| 10| Capacitación al personal | Sesión | 10 | 250 | 2,500 |
| 11| Contingencia (10% del total) | Global | 1 | 34,990 | 34,990 |
| | **TOTAL** | | | | S/. 384,890 |

### 4.2 Análisis de Viabilidad
| Dimensión | Evaluación | Conclusión |
|---|---|---|
| Viabilidad Técnica | El equipo domina Python, FastAPI, React, OpenCV y despliegue AWS. | VIABLE |
| Viabilidad Económica | ROI estimado positivo en 12 meses por reducción de siniestros. | VIABLE |
| Viabilidad Operativa | Sistema diseñado para operación 24/7 con mínima intervención humana. | VIABLE |
| Viabilidad Legal | Alineado con normativas MTC/SUTRAN de seguridad vial. | VIABLE |
| Viabilidad de Tiempo | Desarrollo paralelo por módulos; equipo de 3 personas. | VIABLE con riesgos |

### 4.3 Indicadores Financieros (Estimados)
| Indicador | Valor Estimado | Interpretación |
|---|---|---|
| VPN (Valor Presente Neto) | S/. 51971.17 | Positivo indica rentabilidad del proyecto |
| TIR (Tasa Interna de Retorno) | 15.11% | Debe superar la tasa de descuento de la empresa |
| ROI (Retorno sobre Inversión) | 25.65% | Calculado sobre ahorro en siniestros año 1 |
| Período de recuperación | 4.7 meses | Tiempo para recuperar la inversión inicial |

## CE0125 – Plan de Gestión de Riesgos del Proyecto

### 5.1 Proceso de Gestión de Riesgos
La gestión de riesgos del proyecto CopIA seguirá el proceso definido en el PMBOK 7ª edición: Planificar → Identificar → Análisis Cualitativo → Análisis Cuantitativo → Planificar Respuestas → Implementar Respuestas → Monitorear.

### 5.2 Matriz de Riesgos del Proyecto
| ID | Riesgo del Proyecto | Prob. | Imp. | Score | Tipo Respuesta | Plan de Acción |
|---|---|---|---|---|---|---|
| RP01 | Incompatibilidad de librerías Python en Raspberry Pi OS | 3 | 4 | 12 | Mitigar | Fijar versiones en requirements.txt; pruebas en entorno idéntico al de producción |
| RP02 | Latencia excesiva en streaming MJPEG | 3 | 3 | 9 | Mitigar | Optimizar resolución de frames; implementar buffer en FastAPI |
| RP03 | Cambios de alcance no controlados (scope creep) | 3 | 4 | 12 | Evitar | Comité de cambios formal; acta de aprobación obligatoria |
| RP04 | Pérdida de datos de telemetría por caída del servidor | 2 | 5 | 10 | Mitigar | Cola local en Raspberry Pi; reintento automático con exponential backoff |
| RP05 | Demoras en adquisición de hardware (Raspberry Pi) | 3 | 3 | 9 | Transferir | Proveedor alternativo identificado; compra anticipada |
| RP06 | Conflictos internos del equipo de desarrollo | 2 | 3 | 6 | Aceptar | Reuniones semanales de sincronización; rol de PM activo |
| RP07 | El modelo IA no alcanza la precisión requerida (>85%) | 3 | 4 | 12 | Mitigar | Fine-tuning con datos reales de conductores; ajuste de umbrales |
| RP08 | Incumplimiento de entregables académicos | 2 | 5 | 10 | Evitar | Cronograma con buffer; revisiones semanales con docentes |

### 5.3 Reservas de Contingencia
- Reserva de tiempo: 10% adicional sobre la duración estimada de cada sprint.
- Reserva de costo: S/. [34990] (10% del presupuesto total).
- Reserva de hardware: 2 unidades Raspberry Pi adicionales en stock.
