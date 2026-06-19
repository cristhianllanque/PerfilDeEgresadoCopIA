import os

nav_structure = {
    "ce03": [
        ("entregable1.md", "CE0311 - Entregable 1: Diseño de Red"),
        ("entregable2.md", "CE0321 - Entregable 2: Planificación de Seguridad"),
        ("entregable3.md", "CE0331 - Entregable 3: Diseño de Centro de Datos"),
        ("entregable1-imp.md", "CE0312-CE0313 - Entregable 1: Implementación y Testing de Red"),
        ("entregable2-imp.md", "CE0322-CE0324 - Entregable 2: Implementación, Monitoreo y Ética de Seguridad"),
        ("entregable3-imp.md", "CE0332-CE0333 - Entregable 3: Implementación y Control de Centro de Datos"),
    ],
    "ce01": [
        ("entregable1.md", "CE0111-CE0115 - Entregable 1: Diagnóstico Organizacional y Alineamiento Estratégico"),
        ("entregable2.md", "CE0113 - Entregable 2: Business Case del Proyecto"),
        ("entregable3.md", "CE0121-CE0125 - Entregable 3: Plan de Gestión del Proyecto"),
        ("entregable4.md", "CE0131-CE0135 - Entregable 4: Modelado de Procesos AS-IS / TO-BE"),
        ("entregable5.md", "CE0141-CE0145 - Entregable 5: Propuesta de Solución TIC Integrada"),
    ],
    "ce02": [
        ("entregable1.md", "CE021 - Entregable 1: Requerimientos y Diseño del Sistema"),
        ("entregable2.md", "CE022 - Entregable 2: Plataforma de Datos del Sistema"),
        ("entregable3.md", "CE023 - Entregable 3: Sistema de Software Funcional Integrado"),
        ("entregable4.md", "CE024 - Entregable 4: Calidad, Operación y Evolución del Sistema"),
        ("entregable5.md", "CE0217 - Entregable 5: Presentación, Video pitch y Sustentación Final"),
    ]
}

base_dir = r"d:\PerfilDeEgresadoCopIA\docs"
for folder, files in nav_structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    for filename, title in files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nContenido para {title}...\n")
