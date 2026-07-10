# Entregable 2. Business Case del Proyecto:


- **Evalúa:** CE012 – Evaluación Financiera y Business Case de TI
- **Competencias:** CE0121 – CE0125
- **Proyecto:** CopIA – Driver Monitoring System (DMS) – Huaynaroque
- **Equipo:** Christian Wilbert Salas Yupanqui | Cristhian Eddy Llanque Tipo | Frank Diego Choquehuanca Huayhua
- **Docentes:** Abel Huanca
- **Universidad:** Universidad Peruana Unión – Filial Juliaca | 2026

---

## 2.1 Justificación del Proyecto
**Problema que se resuelve:**
Huaynaroque carece de un sistema automatizado para detectar y gestionar estados de fatiga o somnolencia en sus conductores durante la operación de la flota. Esta ausencia genera un alto riesgo de accidentes viales, pérdidas económicas por siniestros, incumplimiento de normativas del MTC/SUTRAN y deterioro de la reputación empresarial.

**Objetivos del proyecto (SMART):**

| # | Objetivo | Indicador | Meta | Plazo |
|---|---|---|---|---|
| 1 | Reducir accidentes por fatiga | N° accidentes/mes | -40% | 12 meses |
| 2 | Implementar DMS en flota | Vehículos con CopIA activo | 100% flota | 6 meses |
| 3 | Centralizar monitoreo | % conductores monitoreados en tiempo real | 100% | 6 meses |
| 4 | Cumplimiento normativo | Eventos auditables registrados | 100% | Al go-live |
| 5 | Reducir costo por siniestros | Costo anual de siniestros | -30% | 12 meses |

**Beneficios esperados:**
Reducción de costos por siniestros, disminución de primas de seguro, cumplimiento normativo, bienestar del conductor y mejora de imagen corporativa.

## 2.2 Análisis de Alternativas
**Alternativas tecnológicas consideradas:**

- Alt. A: Solución propia (CopIA)
- Alt. B: Software DMS comercial
- Alt. C: Sin intervención

**Criterios de evaluación:**
Costo inicial, adaptabilidad, integración GPS/Firebase, dependencia de proveedor, escalabilidad, y cumplimiento normativo.

**Matriz comparativa:**

| Criterio | Alt. A: Solución propia (CopIA) | Alt. B: Software DMS comercial | Alt. C: Sin intervención |
|---|---|---|---|
| Costo inicial | Medio (S/. 50,000) | Alto (licencias por vehículo) | Bajo (S/. 0) |
| Adaptabilidad | Alta (código propio) | Media (configuración limitada) | N/A |
| Integración GPS/Firebase | Nativa | Requiere middleware | N/A |
| Dependencia de proveedor | Ninguna | Alta | N/A |
| Escalabilidad | Alta (cloud AWS) | Media | N/A |
| Cumplimiento normativo | Sí (diseñado a medida) | Parcial | No cumple |
| Puntaje total (1–5) | 4.5 | 3.2 | 1.0 |

*Alternativa seleccionada: Alt. A – Solución propia CopIA.*

## 2.3 Evaluación de Beneficios

| Tipo | Beneficio | Valor Estimado / Impacto |
|---|---|---|
| Cuantificable | Reducción de costos por accidentes | S/. 60,000 / año |
| Cuantificable | Reducción de primas de seguro | S/. 15,000 / año |
| Cuantificable | Ahorro en multas MTC/SUTRAN | S/. 5,000 / año |
| Cualitativo | Mejora de imagen corporativa | Alto (impacto en retención) |
| Cualitativo | Bienestar y seguridad del conductor | Alto (reducción de estrés) |
| Cualitativo | Trazabilidad y auditoría de incidentes | Alto (respaldo legal) |

**Indicadores de valor:**
Reducción de siniestros, retorno de inversión y satisfacción del conductor.

## 2.4 Estimación de Costos

| Categoría | Ítem | Costo Estimado |
|---|---|---|
| Inversión inicial | Hardware (Raspberry Pi, cámaras, pantalla, GPS) | S/. 103,000 |
| Inversión inicial | Servidor cloud AWS (setup) | S/. 2,500 |
| Inversión inicial | Desarrollo e integración del sistema | S/. 15,000 |
| Inversión inicial | Capacitación del personal | S/. 2,500 |
| Costos operativos | Hosting cloud mensual (AWS) | S/. 400 / mes |
| Costos operativos | Conectividad 4G por vehículo | S/. 30 / mes (S/. 1,500/mes total) |
| Costos de mantenimiento | Actualizaciones de modelos IA y sistema | S/. 5,000 / año |
| **TOTAL ESTIMADO** | **(Inversión + Operación 1er año)** | **S/. 150,800** |

## 2.5 Riesgos Iniciales
**Identificación de riesgos estratégicos:**

- Baja conectividad en rutas rurales.
- Resistencia de conductores al monitoreo.
- Falsos positivos del modelo IA.
- Falla de hardware en campo.

**Evaluación preliminar de impacto:**

| Riesgo | Probabilidad | Impacto | Estrategia Preliminar |
|---|---|---|---|
| Baja conectividad en rutas | Alta | Alto | Procesamiento local en edge; cola de sincronización |
| Resistencia de conductores | Media | Alto | Capacitación y comunicación del beneficio |
| Falsos positivos modelo IA | Media | Medio | Calibración y ajuste de umbrales |
| Falla de hardware en campo | Media | Alto | Stock de reemplazo y procedimiento de swap |
