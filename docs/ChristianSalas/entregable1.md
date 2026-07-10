# Entregable 1: Diagnóstico Organizacional y Alineamiento Estratégico


- **Evalúa:** CE011 – Gobierno e Innovación de TI
- **Competencias:** CE0111 – CE0115
- **Proyecto:** CopIA – Driver Monitoring System (DMS) – Huaynaroque
- **Equipo:** Christian Wilbert Salas Yupanqui | Cristhian Eddy Llanque Tipo | Frank Diego Choquehuanca Huayhua
- **Docentes:** Abel Huanca
- **Universidad:** Universidad Peruana Unión – Filial Juliaca | 2026

---

## CE0111 - Diagnóstico Organizacional.
### Contexto Organizacional
Huaynaroque es una empresa de transporte terrestre de carga y pasajeros ubicada en la región de Puno, Perú. Opera una flota de vehículos pesados en rutas interprovinciales, enfrentando retos de competitividad, seguridad vial y eficiencia operativa en un mercado nacional altamente informal y competido.
- **Sector:** Transporte terrestre interprovincial / logística de carga
- **Tamaño estimado de flota:** 150 vehículos
- **Alcance geográfico:** Región Puno y rutas nacionales (Juliaca, Arequipa, Cusco, Lima)

### Estructura Organizacional
Huaynaroque cuenta con una estructura organizacional vertical con las siguientes áreas funcionales:

- Gerencia General
- Gerencia de Operaciones (gestión de flota y conductores)
- Área de Mantenimiento Vehicular
- Área Administrativa y Contable
- Área de Recursos Humanos
- Área de Tecnologías de Información (incipiente)

### Cadena de Valor

| Actividad Primaria | Descripción |
|---|---|
| Logística de entrada | Asignación de rutas, planificación de viajes y carga de combustible |
| Operaciones | Conducción de vehículos, control de tiempos y registro de incidentes |
| Logística de salida | Entrega de carga/pasajeros, liquidación de viajes |
| Marketing y ventas | Captación de clientes corporativos y particulares |
| Servicio posventa | Gestión de reclamos, seguimiento de satisfacción del cliente |
| Infraestructura TI | Gestión incipiente de sistemas; sin DMS implementado |
| RRHH | Contratación y capacitación de conductores |

### Mapa de Stakeholders

| Stakeholder | Tipo | Interés / Necesidad |
|---|---|---|
| Gerencia General | Interno | Reducir accidentes y costos operativos |
| Conductores | Interno | Recibir alertas oportunas; evitar sanciones |
| Equipo de monitoreo | Interno | Supervisar flota en tiempo real |
| Área de TI | Interno | Gestionar e implementar el DMS |
| Clientes (empresas) | Externo | Garantía de entrega segura y a tiempo |
| MTC / SUTRAN | Externo/Regulador | Cumplimiento de normativa de seguridad vial |
| Compañías aseguradoras | Externo | Reducción de siniestros y reclamos |
| Comunidades en ruta | Externo | Seguridad vial en carreteras |

### Análisis Estratégico
**Misión:** Brindar servicios de transporte terrestre seguros, confiables y eficientes, conectando personas y mercancías en las principales rutas del sur del Perú.
**Visión:** Ser la empresa de transporte líder en el sur del Perú al 2030, reconocida por su innovación tecnológica, seguridad vial y compromiso con el cliente.

**Objetivos Estratégicos:**

- Reducir en un 40% los accidentes por fatiga del conductor en los próximos 12 meses.
- Incrementar la eficiencia operativa de la flota mediante monitoreo en tiempo real.
- Cumplir con regulaciones de seguridad vial del MTC y SUTRAN.
- Digitalizar los procesos de gestión de conductores y viajes.

### Análisis FODA

| FORTALEZAS | DEBILIDADES |
|---|---|
| Flota propia con rutas establecidas | Ausencia de sistema de monitoreo de conductores |
| Conductores con experiencia en rutas del sur | Procesos manuales de control de viajes |
| Relaciones comerciales con clientes corporativos | Alta tasa de incidentes por fatiga |
| Infraestructura de talleres propios | Baja madurez digital en gestión de TI |
| **OPORTUNIDADES** | **AMENAZAS** |
| Normativa MTC que exige sistemas de seguridad vial | Competencia con empresas que ya tienen DMS |
| Reducción de costos por siniestros con IA | Costo de implementación tecnológica |
| Acceso a soluciones IoT y cloud de bajo costo | Resistencia al cambio por parte de conductores |
| Creciente demanda de transporte seguro | Conectividad limitada en rutas remotas (altiplano) |

### Factores Críticos de Éxito
- Adopción del sistema por parte de los conductores y personal operativo.
- Conectividad de red 4G/LTE en las rutas de operación.
- Precisión del sistema de detección de somnolencia (EAR, MAR, PERCLOS).
- Capacitación continua del equipo de monitoreo.
- Integración correcta entre el edge (Raspberry Pi) y la nube (FastAPI).

### Diagnóstico Digital / TI

| Sistema | Función | Estado | Tecnología |
|---|---|---|---|
| Sistema de facturación | Emisión de comprobantes | Operativo | Software local legacy |
| Planillas Excel de viajes | Control manual de rutas y conductores | Operativo (manual) | MS Excel |
| WhatsApp Business | Comunicación con conductores | Operativo (informal) | App móvil |
| GPS externo (básico) | Rastreo vehicular básico | Parcial | Dispositivo independiente |
| CopIA DMS (propuesto) | Monitoreo de fatiga y somnolencia | En desarrollo | Raspberry Pi + FastAPI + React |

### Nivel de Madurez Digital

| Dimensión | Nivel (1–5) | Observación |
|---|---|---|
| Gestión de datos | 2 | Datos dispersos en Excel y WhatsApp; sin BD centralizada |
| Automatización de procesos | 1 | Procesos manuales sin soporte tecnológico |
| Conectividad e IoT | 2 | GPS básico; sin integración con sistemas centrales |
| Seguridad de la información | 1 | Sin políticas formales de seguridad TI |
| Analítica y toma de decisiones | 1 | Decisiones basadas en experiencia, sin datos |
| Cultura digital | 2 | Resistencia moderada al cambio tecnológico |

### Brechas Tecnológicas
- Ausencia de monitoreo en tiempo real del estado físico del conductor.
- Sin integración entre GPS, control de viajes y datos de seguridad.
- Falta de trazabilidad de eventos de fatiga y su correlación con accidentes.
- Infraestructura de TI sin servidor central ni arquitectura cloud.
- Sin procesos formales de backup ni continuidad operativa.

### Identificación del Problema
**Definición estructurada del problema:**
Huaynaroque carece de un sistema automatizado para detectar y gestionar estados de fatiga o somnolencia en sus conductores durante la operación de la flota. Esta ausencia genera un alto riesgo de accidentes viales, pérdidas económicas por siniestros, incumplimiento de normativas del MTC/SUTRAN y deterioro de la reputación empresarial.

**Causas Raíz:**

- No existe tecnología de visión artificial desplegada en los vehículos.
- El monitoreo de conductores es manual, esporádico e ineficiente.
- No hay un servidor central que centralice datos de toda la flota.
- Ausencia de cultura preventiva basada en datos en la organización.

**Impacto Estratégico:**

| Impacto | Descripción | Severidad |
|---|---|---|
| Accidentes por fatiga | Pérdida de vidas, daños materiales y sanciones legales | Alta |
| Pérdidas económicas | Costos de siniestros, seguros y reparaciones | Alta |
| Incumplimiento regulatorio | Multas por parte del MTC/SUTRAN | Media-Alta |
| Pérdida de clientes | Clientes corporativos exigen garantías de seguridad | Media |
| Reputación corporativa | Deterioro de imagen ante accidentes públicos | Alta |

## CE0112 - Alineamiento Estratégico.
### Alineamiento del Proyecto CopIA con los Objetivos Estratégicos

| Objetivo Estratégico | Cómo CopIA lo soporta |
|---|---|
| Reducir accidentes por fatiga en 40% | Detección en tiempo real de EAR, MAR, PERCLOS con alertas automáticas |
| Incrementar eficiencia operativa | Panel de control centralizado con métricas de toda la flota |
| Cumplir normativas MTC/SUTRAN | Registro persistente de eventos de fatiga y trazabilidad auditada |
| Digitalizar gestión de conductores | API REST + Firebase GPS + ranking de riesgo por conductor |

### Alineamiento con Estándares de Gobierno TI
- **PMBOK 7ª edición:** Gestión del proyecto bajo principios de valor, desempeño y partes interesadas.
- **COBIT 2019:** Marco de gobierno y gestión de TI aplicado a la toma de decisiones sobre el DMS.
- **ISO/IEC 27001:** Lineamientos de seguridad para protección de datos de conductores y telemetría.
- **ISO 39001:** Norma de sistema de gestión de la seguridad vial, directamente aplicable.

### Mapa de Alineamiento Estratégico (Strategic Alignment Model)

| Dimensión | Negocio | TI (CopIA) |
|---|---|---|
| Estrategia | Liderazgo en seguridad vial regional | DMS con IA para detección de fatiga |
| Procesos | Monitoreo manual de conductores | Monitoreo automatizado en tiempo real |
| Estructura | Área TI incipiente | Infraestructura edge-cloud escalable |
| Personas | Conductores y supervisores | Capacitación en uso del DMS y dashboard |

## CE0113 - Caso de Negocio.
*(Ver detalles completos en Entregable 2: Business Case)*

## CE0114 - Roadmap de Tecnología.
### Visión Tecnológica a 3 Años
El roadmap de CopIA contempla una evolución progresiva desde la implementación piloto hasta una plataforma de gestión de flota inteligente integrada con analítica avanzada y predicción de riesgos.

| Fase | Período | Hito Principal | Tecnología Clave |
|---|---|---|---|
| Fase 0: Piloto | Mes 1–3 | Implementación en 3 vehículos de prueba | Raspberry Pi 4, OpenCV, FastAPI |
| Fase 1: Despliegue | Mes 4–6 | Cobertura del 100% de la flota | AWS EC2, PostgreSQL, Firebase |
| Fase 2: Consolidación | Mes 7–12 | Dashboard avanzado + reportería automática | React, Chart.js, MJPEG streaming |
| Fase 3: Analítica | Año 2 | Predicción de riesgo por conductor (ML) | Python ML, modelos predictivos |
| Fase 4: Integración | Año 3 | Integración con ERP/TMS de flota | APIs REST, middleware de integración |

### Arquitectura Tecnológica Evolutiva
- **Corto plazo:** Edge (Raspberry Pi) → API REST (FastAPI/AWS) → Dashboard React.
- **Mediano plazo:** Incorporación de modelos ML para predicción de patrones de fatiga por conductor.
- **Largo plazo:** Integración con sistemas ERP, TMS y plataformas de seguros para automatización de reportes.

### Stack Tecnológico del Proyecto CopIA

| Capa | Tecnología | Rol en el sistema |
|---|---|---|
| Edge / IoT | Raspberry Pi 4 + Cámara USB/CSI | Captura y procesamiento local de video del conductor |
| Visión Artificial | OpenCV, MediaPipe / dlib | Extracción de landmarks faciales para EAR/MAR/PERCLOS |
| Modelos IA | CopIASystem (PyTorch/TensorFlow) | Clasificación de estados de somnolencia |
| Backend API | FastAPI (Python) | API REST central; recepción de telemetría y streaming MJPEG |
| Base de datos | PostgreSQL + SQLAlchemy | Persistencia de sesiones, eventos de fatiga y conductores |
| GPS en tiempo real | Firebase Realtime Database | Sincronización de ubicación GPS de la flota |
| Frontend | React + Vite + Tailwind CSS | Panel de control para administradores de flota |
| Infraestructura cloud | AWS EC2 / Render / Railway | Hosting del servidor central y API |
| Autenticación | JWT (JSON Web Tokens) | Seguridad de acceso a endpoints |
| Alertas locales | Audio + GUI Raspberry Pi (pygame/tkinter) | Alertas visuales y sonoras en cabina |

## CE0115 - Matriz de Riesgos Estratégicos.
### Metodología de Evaluación
Se utiliza la metodología ISO 31000 para la identificación, análisis y evaluación de riesgos. La puntuación de riesgo se calcula como: Riesgo = Probabilidad × Impacto (escala 1–5 en ambos ejes).

| ID | Riesgo | Categoría | Prob. (1–5) | Imp. (1–5) | Score | Nivel | Estrategia de Mitigación | Responsable |
|---|---|---|---|---|---|---|---|---|
| R01 | Baja conectividad 4G en altiplano | Técnico | 4 | 4 | 16 | ALTO | Procesamiento local en Raspberry Pi; sincronización offline con cola de eventos | Área TI |
| R02 | Rechazo del sistema por conductores | Humano | 3 | 4 | 12 | ALTO | Plan de gestión del cambio; incentivos por buen desempeño | RRHH + Gerencia |
| R03 | Falsos positivos de fatiga (alarmas falsas) | Técnico/IA | 3 | 3 | 9 | MEDIO | Calibración de umbrales EAR/MAR por conductor; entrenamiento continuo del modelo | Área TI |
| R04 | Falla de hardware en campo | Operativo | 3 | 4 | 12 | ALTO | Protocolo de reemplazo rápido; stock mínimo de unidades de respaldo | Operaciones |
| R05 | Brecha de seguridad en transmisión de datos | Seguridad | 2 | 5 | 10 | ALTO | TLS en todas las comunicaciones; autenticación JWT; auditoría de logs | Área TI |
| R06 | Sobrecarga del servidor FastAPI | Técnico | 2 | 4 | 8 | MEDIO | Auto-scaling en AWS; límite de rate en endpoints de telemetría | Área TI |
| R07 | Incumplimiento de normativa MTC | Regulatorio | 2 | 5 | 10 | ALTO | Monitoreo de cambios normativos; asesoría legal periódica | Gerencia |
| R08 | Rotación de personal técnico clave | Humano | 2 | 4 | 8 | MEDIO | Documentación técnica exhaustiva; knowledge base del sistema | RRHH |
| R09 | Desactualización del modelo IA | Técnico/IA | 2 | 3 | 6 | MEDIO | Ciclos de reentrenamiento trimestrales con nuevos datos de campo | Área TI |
| R10 | Resistencia de la gerencia al costo | Organizacional | 2 | 3 | 6 | MEDIO | Business case sólido con ROI documentado; presentación ejecutiva | PM del Proyecto |

### Mapa de Calor de Riesgos

| Impacto \ Probabilidad | 1 – Raro | 2 – Poco probable | 3 – Posible | 4 – Probable | 5 – Casi seguro |
|---|---|---|---|---|---|
| **5 – Catastrófico** | | R05, R07 | | | |
| **4 – Mayor** | | R04, R06, R08 | R02 | R01 | |
| **3 – Moderado** | | R09, R10 | R03 | | |
| **2 – Menor** | | | | | |
| **1 – Insignificante**| | | | | |– Raro | 2 – Poco probable | 3 – Posible | 4 – Probable | 5 – Casi seguro |
|---|---|---|---|---|---|
| **5 – Catastrófico** | | R05, R07 | | | |
| **4 – Mayor** | | R04, R06, R08 | R02 | R01 | |
| **3 – Moderado** | | R09, R10 | R03 | | |
| **2 – Menor** | | | | | |
| **1 – Insignificante**| | | | | |
