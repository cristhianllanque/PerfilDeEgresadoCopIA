# Entregable 5: Presentación, Video Pitch y Sustentación Final

## Portada
- **Título del sistema:** CopAI - Asistente de Conducción AI (Edge & Central Server)
- **Nombre del estudiante:** Cristhian Edy Llanque Tipo - Christian Wilbert Salas Yupanqui - Frank Diego Choquehuanca
- **Semestre:** X
- **Fecha:** Julio 2026

---

## Resumen Ejecutivo
**Problema:** Los accidentes de flotas de transporte pesado causados por la fatiga y el micro-sueño de los conductores generan pérdidas humanas invaluables y millones de dólares en daños materiales anualmente. Las soluciones actuales dependen de conectividad a internet constante, fallando en carreteras alejadas.
**Solución:** CopAI es un ecosistema IoT e Inteligencia Artificial (Edge-to-Cloud). Procesa video en tiempo real dentro del vehículo usando una Raspberry Pi 5 y alertas auditivas inmediatas, mientras sincroniza telemetría GPS con un panel de control corporativo (Vue.js + FastAPI) vía redes celulares.
**Valor esperado:** Reducir la siniestralidad de flotas en un 80% mediante prevención proactiva, validado por el interés inicial de empresas como *Hayna Roque* (flota de 150 a 300 unidades).

---

## Sección 1: Presentación de la Solución

### 1.1 Contexto del Problema y Stakeholders
- **Contexto:** El transporte de carga pesada exige largas jornadas laborales. La fatiga humana (pestañeos prolongados, bostezos) es el enemigo silencioso de las carreteras (Zonas Cero).
- **Stakeholders (Usuarios):** 
  - *Conductores:* Usuarios finales en cabina que necesitan alertas no intrusivas pero efectivas.
  - *Administradores de Flota / Prevencionistas de Riesgo:* Operadores que monitorean las rutas desde la central térmica/base logística.

### 1.2 Alcance y Funcionalidades Principales
El alcance del proyecto cubre la creación del hardware-software (Nodo Edge) y la plataforma en la nube.
- **Detección Biométrica Local:** Cálculo del PERCLOS y EAR mediante IA sin necesidad de conexión a internet.
- **Alarma Text-to-Speech:** Advertencias de voz directas ("Alerta, fatiga detectada").
- **Telemetría GPS Asíncrona:** Captura de ubicación exacta del micro-sueño a través del módulo SIM7600G-H.
- **Monitoreo Web:** Panel administrativo Vue.js con métricas y gráficas (ECharts).

---

## Sección 2: Demostración del Sistema (Guion de Demo)

Para la sustentación presencial, se ejecutará el siguiente flujo en vivo:
1. **Arranque:** Se encenderá la Raspberry Pi y el orquestador local en la Laptop (`server_dashboard.py`).
2. **Simulación de Conducción:** El estudiante Cristhian Llanque se pondrá frente a la cámara web de la Raspberry Pi simulando manejar.
3. **Trigger Crítico:** Cristhian cerrará los ojos por más de 1.5 segundos. El jurado escuchará la voz de la Raspberry Pi emitiendo la alerta en vivo.
4. **Verificación Cloud:** Inmediatamente, se proyectará la pantalla del Dashboard Web (Vue.js), donde el jurado verá aparecer el punto rojo en el mapa GPS y el registro del evento en la base de datos MySQL/Firebase.

---

## Sección 3: Sustento Técnico (Decisiones de Arquitectura)

Esta sección justifica *por qué* construimos el sistema así.

### 3.1 Justificación de Decisiones
- **¿Por qué Edge Computing y no Cloud Computing para la IA?** Enviar video en vivo de docenas de camiones a un servidor AWS consumiría todo el ancho de banda 4G y tendría latencia. Procesar el video localmente en la Raspberry Pi garantiza que la alarma suene en **milisegundos**, incluso si el camión pasa por un túnel sin señal (Zona Ciega).
- **¿Por qué MediaPipe y no YOLO/OpenCV puro?** MediaPipe cuenta con modelos cuantizados (TFLite) que extraen 468 puntos faciales gastando apenas un 50% de CPU en procesadores ARM (Raspberry Pi), sin necesitar tarjetas de video (GPUs) costosas.

### 3.2 Limitaciones y Trade-offs (Deuda Técnica)
- **Túnel Ngrok:** Actualmente usamos Ngrok para evadir el NAT estricto de los chips 4G. *Limitación:* La URL cambia. *Mitigación actual:* Script dinámico de reconexión. *Plan a futuro:* Migrar a un servidor VPN (WireGuard).

### 3.3 Plan de Evolución
Escalabilidad para el cliente **Hayna Roque**: 
- Integración con OBD-II para medir frenadas del camión. 
- Aprendizaje Federado para reentrenar la IA sin extraer videos de los conductores por privacidad.

---

## Sección 4: Defensa ante Jurado (Guía de Argumentación)

### 4.1 Posibles Preguntas del Jurado y Respuestas Clave
- **Jurado:** *"¿Qué pasa si la Raspberry Pi pierde conexión a internet en medio del desierto?"*
  - **Respuesta:** "Esa es la ventaja de nuestra arquitectura Edge. La detección de fatiga y la alarma de voz funcionan 100% offline. El GPS guardará la coordenada localmente y, cuando el camión recupere señal 3G/4G, sincronizará (Push) la alerta al servidor central".
- **Jurado:** *"¿Es seguro enviar los datos de toda una flota por internet móvil?"*
  - **Respuesta:** "Sí. Aplicamos JWT Stateless para el panel de administración, contraseñas encriptadas con Bcrypt, y el túnel entre el camión y nuestro backend FastAPI viaja sobre TLS 1.3, evitando ataques Man-in-the-Middle".

### 4.2 Síntesis Final del Aporte
CopAI demuestra que el hardware de bajo costo combinado con modelos matemáticos de Inteligencia Artificial optimizados puede democratizar la seguridad industrial, salvando vidas en las carreteras peruanas/latinoamericanas.

---

## Anexos

### 5.1 Guion Oficial para el Video Pitch (3 Minutos)
*(Instrucción: Lee este guion frente a la cámara mostrando partes de tu sistema).*

**[0:00 - 0:30] El Problema (Gancho)**
"¿Sabían que el micro-sueño al volante de vehículos pesados causa miles de muertes al año? Hola, somos el equipo creador de CopAI. Las soluciones de IA actuales necesitan internet rápido para enviar video a la nube, pero en nuestras carreteras, la señal se pierde. Si un conductor se queda dormido en una zona ciega, el sistema tradicional falla."

**[0:30 - 1:30] La Solución (Arquitectura Edge)**
"Por eso creamos CopAI, un Asistente de Conducción Edge-to-Cloud. En lugar de depender de la nube, le dimos un 'cerebro' propio a cada camión usando una Raspberry Pi 5. Nuestro sistema lee 468 puntos faciales en tiempo real y calcula el nivel de fatiga. Si cierras los ojos, la alarma suena en menos de 500 milisegundos, ¡tengas internet o no!"

**[1:30 - 2:30] El Ecosistema Corporativo**
"Pero no nos quedamos en el camión. Cuando hay señal, nuestro módulo SIM7600 envía la telemetría exacta (GPS y velocidad) a nuestro Servidor Central programado en FastAPI y MySQL. Los prevencionistas de riesgo pueden ver las alertas en vivo en un Panel Administrativo web de alta velocidad hecho con Vue.js, protegido por encriptación bancaria y JWT."

**[2:30 - 3:00] Cierre Comercial**
"CopAI no es solo un prototipo. Hemos mitigado vulnerabilidades críticas bajo estándares OWASP y diseñado un despliegue automatizado. Ya hemos captado el interés de empresas como Hayna Roque para flotas de hasta 300 unidades. CopAI previene accidentes hoy y prepara el camino para el IoT vehicular del futuro. Gracias."

### 5.2 Enlaces del Proyecto
- **Repositorio de Código:** [https://github.com/cristhianllanque/Equipo-CopIA](https://github.com/cristhianllanque/Equipo-CopIA)
- **Enlace al Pitch (YouTube / Drive):** *(Pegar link aquí una vez grabado)*
