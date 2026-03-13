import sqlite3

class DB():
    def __init__(self, nombre_db):
        # Permitir que las llaves foráneas funcionen en SQLite
        self.conexion = sqlite3.connect(nombre_db)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conexion.cursor()
    
    def consultar(self, sql, datos=()):
        self.cursor.execute(sql, datos)
        self.conexion.commit()
        # Se agregan los paréntesis () para ejecutar la función fetchall
        return self.cursor.fetchall()

    def cerrar(self):
        # Se agrega 'self' para poder acceder a la conexión
        self.conexion.close()

    def crear_esquema(self):
        # 1. Creación de tablas base
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Usuario (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, password TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Grado_instruccion (id_grado_instruccion INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Estado_laboral (id_estado_laboral INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Categoria_personal (id_categoria_personal INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
        
        # 2. Tabla Personal con nombres de columnas corregidos
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Personal (
                                    id_personal INTEGER PRIMARY KEY AUTOINCREMENT,
                                    cedula INT UNIQUE NOT NULL,
                                    nombres TEXT NOT NULL,
                                    apellidos TEXT NOT NULL,
                                    fecha_nacimiento DATE,
                                    edad INTEGER,
                                    direccion TEXT,
                                    correo TEXT,
                                    telefono TEXT,
                                    carnet_patria TEXT,
                                    titulo_obtenido TEXT,
                                    fecha_ingreso DATE,
                                    anos_servicio INTEGER,
                                    comuna TEXT,
                                    cargo TEXT,
                                    codigo_dependencia TEXT,
                                    id_grado_instruccion INTEGER,
                                    id_categoria_personal INTEGER,
                                    id_estado_laboral INTEGER,
                                    FOREIGN KEY (id_grado_instruccion) REFERENCES Grado_instruccion(id_grado_instruccion),
                                    FOREIGN KEY (id_categoria_personal) REFERENCES Categoria_personal(id_categoria_personal),
                                    FOREIGN KEY (id_estado_laboral) REFERENCES Estado_laboral(id_estado_laboral)
                                    )""")

        # 3. Creación de la Vista (para devolver nombres en lugar de IDs)
        self.cursor.execute("DROP VIEW IF EXISTS vista_personal_detallada")
        self.cursor.execute("""
            CREATE VIEW vista_personal_detallada AS 
            SELECT 
                p.id_personal, p.cedula, p.nombres, p.apellidos, p.cargo,
                g.descripcion AS grado_instruccion,
                c.nombre AS categoria,
                e.nombre AS estado_laboral,
                p.fecha_ingreso, p.anos_servicio
            FROM Personal p
            LEFT JOIN Grado_instruccion g ON p.id_grado_instruccion = g.id_grado_instruccion
            LEFT JOIN Categoria_personal c ON p.id_categoria_personal = c.id_categoria_personal
            LEFT JOIN Estado_laboral e    ON p.id_estado_laboral = e.id_estado_laboral;
        """)

        # 4. Triggers para automatizar Edad y Años de Servicio
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS calcular_datos_insert AFTER INSERT ON Personal
            BEGIN
                UPDATE Personal SET 
                edad = (strftime('%Y', 'now') - strftime('%Y', NEW.fecha_nacimiento)) - (strftime('%m-%d', 'now') < strftime('%m-%d', NEW.fecha_nacimiento)),
                anos_servicio = (strftime('%Y', 'now') - strftime('%Y', NEW.fecha_ingreso)) - (strftime('%m-%d', 'now') < strftime('%m-%d', NEW.fecha_ingreso))
                WHERE id_personal = NEW.id_personal;
            END;
        """)
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS generar_codigo_dependencia
            AFTER INSERT ON Personal
            BEGIN
                UPDATE Personal
                SET codigo_dependencia = 'DEP-' || printf('%03d', NEW.id_personal)
                WHERE id_personal = NEW.id_personal 
                AND (codigo_dependencia IS NULL OR codigo_dependencia = '');
            END;
        """)

    def datos_prueba(self):
        # Usamos ignore para evitar errores si los datos ya existen
        self.cursor.execute("INSERT OR IGNORE INTO Grado_instruccion (descripcion) VALUES ('No Graduado'),('Bachiller'),('Técnico Medio'),('Universitario'),('Postgrado')")
        self.cursor.execute("INSERT OR IGNORE INTO Estado_laboral (nombre) VALUES ('Activo'),('Reposo')")
        self.cursor.execute("INSERT OR IGNORE INTO Categoria_personal (nombre) VALUES ('Administrativo'),('Obrero'),('Docente'),('Directivo')")
        
        # Insertar personal de prueba (dejando edad y años en 0 para que el trigger los calcule)
        self.cursor.execute("""INSERT OR IGNORE INTO Personal (
            cedula, nombres, apellidos, fecha_nacimiento, fecha_ingreso, 
            id_grado_instruccion, id_categoria_personal, id_estado_laboral
        ) VALUES 
        ('12345678', 'Yusepe', 'Rossi', '1985-05-20', '2015-01-15', 3, 1, 1),
        ('87654321', 'Beximar', 'Escalona', '1992-11-03', '2018-03-10', 3, 3, 1),
        ('11223344', 'Grober', 'Smith', '1970-08-25', '2000-06-01', 1, 2, 2)""")

# --- Ejecución del programa ---
db = DB(":memory:") # Cambiado de :memory: a un archivo para que lo veas
db.crear_esquema()
db.datos_prueba()

# CONSULTA CLAVE: Usamos la VISTA para ver nombres en lugar de IDs
print("-" * 30)
print("REPORTE DETALLADO (USANDO JOINS/VISTA):")
resultados = db.consultar("SELECT * FROM vista_personal_detallada")
for fila in resultados:
    print(fila)