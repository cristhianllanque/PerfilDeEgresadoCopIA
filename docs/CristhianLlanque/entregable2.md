# Entregable 2: Plataforma de Datos del Sistema

## Portada
- **Título del sistema:** CopAI - Asistente de Conducción AI (Edge & Central Server)
- **Nombre del estudiante:** Cristhian Edy Llanque Tipo - Christian Wilbert Salas Yupanqui - Frank Diego Choquehuanca
- **Semestre:** X
- **Fecha:** Julio 2026

---

## Resumen Ejecutivo
El presente documento detalla la arquitectura, modelado y administración de la Plataforma de Datos del sistema **CopAI**. La persistencia de la información es el pilar que permite la toma de decisiones preventivas en la gestión de flotas. Para ello, se ha implementado un esquema híbrido: **MySQL** (Relacional) actuando como el Core Data Warehouse en el Servidor Central para garantizar la integridad ACID y relaciones complejas (Conductores, Incidentes, Rutas, Usuarios), complementado con **Firebase** (NoSQL) para telemetría ágil en tiempo real.

Se exponen los Modelos Entidad-Relación, scripts de definición (DDL), y manipulación de datos (DML). Además, para garantizar el rendimiento (CE022), se han programado Triggers para alertas automatizadas a nivel base de datos, Procedimientos Almacenados (Stored Procedures) para la ingesta masiva de telemetría del GPS SIM7600G-H y métricas de MediaPipe (PERCLOS/EAR), y esquemas de seguridad basados en Roles para auditoría estricta.

---

## Sección 1: Modelo de Datos

### 1.1 Modelo Lógico (Entidad-Relación)
El sistema está normalizado hasta la Tercera Forma Normal (3FN).

**Entidades Principales:**
- **Conductores:** Almacena la identidad y credenciales para el Login en el Nodo Edge.
- **Incidentes_Fatiga:** Registra cada alerta disparada por el Motor IA (MediaPipe), incluyendo PERCLOS, EAR, e información geoespacial.
- **Vehiculos_Rutas:** Asignación logística de los viajes.
- **Administradores:** Usuarios con acceso al Dashboard Web en Vue.js.

![Modelo Entidad-Relacion](../imagenesllanque/modelo_er.png)
*(Instrucción: Toma una captura de pantalla de la vista "Diseñador" de phpMyAdmin o MySQL Workbench mostrando las tablas unidas por líneas)*

### 1.2 Diccionario de Datos

**Tabla: `Conductores`**

| Campo | Tipo de Dato | Longitud | Restricciones | Descripción |
|:---|:---|:---|:---|:---|
| id_conductor | INT | - | PK, AUTO_INCREMENT | Identificador único del conductor. |
| dni | VARCHAR | 15 | UNIQUE, NOT NULL | Documento de identidad. |
| nombre_completo| VARCHAR | 100| NOT NULL | Nombres y apellidos. |
| password_hash | VARCHAR | 255| NOT NULL | Contraseña encriptada para el Login Edge. |
| estado_activo | BOOLEAN | - | DEFAULT TRUE | Indica si el conductor está habilitado. |

**Tabla: `Incidentes_Fatiga`**

| Campo | Tipo de Dato | Longitud | Restricciones | Descripción |
|:---|:---|:---|:---|:---|
| id_incidente | INT | - | PK, AUTO_INCREMENT | ID único de la alerta. |
| id_conductor | INT | - | FK (Conductores) | Conductor asociado al evento. |
| fecha_hora | DATETIME | - | DEFAULT CURRENT_TIMESTAMP | Momento exacto del micro-sueño. |
| valor_perclos | FLOAT | - | NOT NULL | Porcentaje de cierre ocular (MediaPipe). |
| valor_ear | FLOAT | - | NOT NULL | Eye Aspect Ratio exacto al momento. |
| latitud | DECIMAL | 10,8 | NOT NULL | Coordenada GPS (Módulo SIM7600G-H). |
| longitud | DECIMAL | 11,8 | NOT NULL | Coordenada GPS (Módulo SIM7600G-H). |
| velocidad_kmh | INT | - | NOT NULL | Velocidad del vehículo en el incidente. |

---

## Sección 2: Implementación de Base de Datos

### 2.1 Scripts de Definición de Datos (DDL)
A continuación, el script de creación del esquema principal garantizando integridad referencial.

```sql
CREATE DATABASE IF NOT EXISTS copia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE copia_db;

CREATE TABLE Conductores (
    id_conductor INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Incidentes_Fatiga (
    id_incidente INT AUTO_INCREMENT PRIMARY KEY,
    id_conductor INT NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_perclos FLOAT NOT NULL,
    valor_ear FLOAT NOT NULL,
    latitud DECIMAL(10,8) NOT NULL,
    longitud DECIMAL(11,8) NOT NULL,
    velocidad_kmh INT NOT NULL,
    FOREIGN KEY (id_conductor) REFERENCES Conductores(id_conductor) ON DELETE CASCADE
);

-- Creación de Índice para optimizar búsquedas geoespaciales y por fechas en el Dashboard
CREATE INDEX idx_fecha ON Incidentes_Fatiga(fecha_hora);
CREATE INDEX idx_conductor ON Incidentes_Fatiga(id_conductor);
```

### 2.2 Evidencia de Implementación
![Tablas en MySQL](../imagenesllanque/mysql_tablas.png)
*(Instrucción: Pon aquí una captura de pantalla de phpMyAdmin o de tu terminal ejecutando un `SHOW TABLES;` y un `DESCRIBE Incidentes_Fatiga;` para demostrar que sí se crearon).*

---

## Sección 3: Consultas y Programación en Base de Datos

### 3.1 Consultas SQL Relevantes (DML)
Para alimentar las gráficas estadísticas del Dashboard Web (Vue.js), FastAPI ejecuta consultas agregadas complejas:

**Consulta A: Conductores con mayor índice de fatiga en el último mes:**
```sql
SELECT c.nombre_completo, COUNT(i.id_incidente) as total_alertas, AVG(i.valor_perclos) as perclos_promedio
FROM Conductores c
JOIN Incidentes_Fatiga i ON c.id_conductor = i.id_conductor
WHERE i.fecha_hora >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
GROUP BY c.id_conductor
ORDER BY total_alertas DESC
LIMIT 5;
```

### 3.2 Procedimientos Almacenados (Stored Procedures)
Para asegurar transacciones rápidas cuando el Nodo Edge envía alertas por internet, la inserción se maneja mediante un SP que valida los datos antes de guardarlos.

```sql
DELIMITER //
CREATE PROCEDURE sp_registrar_incidente(
    IN p_dni VARCHAR(15),
    IN p_perclos FLOAT,
    IN p_ear FLOAT,
    IN p_lat DECIMAL(10,8),
    IN p_lon DECIMAL(11,8),
    IN p_vel INT
)
BEGIN
    DECLARE v_id_conductor INT;
    
    -- Obtener ID del conductor basado en el DNI que viene de la Raspberry Pi
    SELECT id_conductor INTO v_id_conductor FROM Conductores WHERE dni = p_dni AND estado_activo = 1;
    
    IF v_id_conductor IS NOT NULL THEN
        INSERT INTO Incidentes_Fatiga (id_conductor, valor_perclos, valor_ear, latitud, longitud, velocidad_kmh)
        VALUES (v_id_conductor, p_perclos, p_ear, p_lat, p_lon, p_vel);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Conductor no existe o inactivo';
    END IF;
END //
DELIMITER ;
```

### 3.3 Disparadores (Triggers)
Si un conductor registra más de 3 incidentes críticos en menos de 1 hora, la base de datos automáticamente cambia una bandera de riesgo (Lógica a nivel BD).

```sql
DELIMITER //
CREATE TRIGGER trg_alerta_recurrente
AFTER INSERT ON Incidentes_Fatiga
FOR EACH ROW
BEGIN
    DECLARE v_conteo INT;
    
    SELECT COUNT(*) INTO v_conteo 
    FROM Incidentes_Fatiga 
    WHERE id_conductor = NEW.id_conductor 
    AND fecha_hora >= DATE_SUB(NEW.fecha_hora, INTERVAL 1 HOUR);
    
    IF v_conteo >= 3 THEN
        -- Insertar en una tabla de auditoría para notificar al Administrador
        INSERT INTO Alertas_Administrador (mensaje, id_conductor) 
        VALUES ('RIESGO ALTO: 3 Alertas en 1 hora', NEW.id_conductor);
    END IF;
END //
DELIMITER ;
```

---

## Sección 4: Seguridad y Administración

### 4.1 Usuarios y Roles de Base de Datos
Para aplicar el principio de "Menor Privilegio", el API (FastAPI) no utiliza el usuario `root`. Se creó un usuario específico con permisos limitados a DML.

```sql
CREATE USER 'api_copia'@'localhost' IDENTIFIED BY 'PasswordSegura2026';
GRANT SELECT, INSERT, UPDATE ON copia_db.* TO 'api_copia'@'localhost';
REVOKE DROP, DELETE ON copia_db.* FROM 'api_copia'@'localhost';
FLUSH PRIVILEGES;
```

### 4.2 Estrategias de Respaldo y Recuperación
Se ha implementado un script automatizado `.bat` en el Servidor Central Windows que ejecuta un volcado completo de la base de datos todos los días a las 02:00 AM usando `mysqldump`.

**Comando de Respaldo (Backup):**
```bash
mysqldump -u root -p copia_db > "C:\CopIA_Backups\copia_db_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sql"
```

### 4.3 Evidencias de Monitoreo
![Monitoreo de BD](../imagenesllanque/mysql_monitoreo.png)
*(Instrucción: Toma una captura de pantalla del "Status" o "Monitor" de XAMPP/MySQL Workbench donde se vea el uso del servidor y conexiones activas).*

---

## Anexos

### 5.1 Capturas de Ejecución de Procedimientos
*(Instrucción: Insertar imagen ejecutando el Stored Procedure `CALL sp_registrar_incidente(...)` y mostrando el resultado "1 row affected").*

### 5.2 Diccionario de Datos Completo (PDF Adjunto)
Se anexa el reporte detallado generado desde el diseñador de bases de datos.
