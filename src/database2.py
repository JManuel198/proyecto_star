import sqlite3
# No toquen la base de datos, funciona y no se ni como, no domino SQL todavia pero parece funcionar decentemente
class DB():
    def __init__(self, nombre_db):
        self.conexion = sqlite3.connect(nombre_db)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conexion.cursor()
    
    def consultar(self, sql, datos=()):
        self.cursor.execute(sql, datos)
        self.conexion.commit()
        return self.cursor.fetchall()

    def cerrar(self):
        self.conexion.close()

    def crear_esquema(self):
        # 1. Creación de tablas base
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Usuario (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, password TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Grado_instruccion (id_grado_instruccion INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Estado_laboral (id_estado_laboral INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Categoria_personal (id_categoria_personal INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
        
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

        self.cursor.execute("DROP VIEW IF EXISTS vista_personal_detallada")
        self.cursor.execute("""
    CREATE VIEW vista_personal_detallada AS 
    SELECT 
        p.cedula, 
        p.nombres, 
        p.apellidos, 
        p.fecha_nacimiento, 
        p.edad, 
        p.direccion, 
        p.correo, 
        p.telefono, 
        p.carnet_patria, 
        p.titulo_obtenido, 
        p.fecha_ingreso, 
        p.anos_servicio, 
        p.comuna, 
        p.cargo,
        p.codigo_dependencia,
        g.descripcion AS grado_instruccion,
        c.nombre AS categoria,
        e.nombre AS estado_laboral
    FROM Personal p
    LEFT JOIN Grado_instruccion g ON p.id_grado_instruccion = g.id_grado_instruccion
    LEFT JOIN Categoria_personal c ON p.id_categoria_personal = c.id_categoria_personal
    LEFT JOIN Estado_laboral e    ON p.id_estado_laboral = e.id_estado_laboral;
""")

        # Triggers de edad y años de servicio, no tocar 
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
                SET codigo_dependencia = 'PAEZ-' || printf('%03d', NEW.id_personal)
                WHERE id_personal = NEW.id_personal 
                AND (codigo_dependencia IS NULL OR codigo_dependencia = '');
            END;
        """)

        self.cursor.execute("INSERT OR IGNORE INTO Grado_instruccion (id_grado_instruccion, descripcion) VALUES (1, 'No Graduado'), (2, 'Bachiller'), (3, 'Tecnico Medio'), (4, 'Universitario'), (5,'Postgrado')")
        self.cursor.execute("INSERT OR IGNORE INTO Estado_laboral (id_estado_laboral, nombre) VALUES (1, 'Activo'), (2, 'Reposo')")
        self.cursor.execute("INSERT OR IGNORE INTO Categoria_personal (id_categoria_personal, nombre) VALUES (1, 'No graduado'), (2, 'Docente I'), (3, 'Docente II'), (4, 'Docente III'),(5, 'Docente IV'),(6, 'Docente V'),(7, 'Docente VI'),(8, 'Docente III'),(9, 'TSU I'),(10, 'TSU II'),(11, 'Profesional I'),(12, 'Profesional II'),(13,'Profesional III'),(14,'Obrero I'),(15,'Obrero II'),(16, 'Aseador I'),(17, 'Aseador II'),(18, 'Mensajero'),(19, 'Portero'),(20, 'Vigilante'),(21, 'Otro')")
        self.cursor.execute("INSERT OR IGNORE INTO Usuario (nombre,password) VALUES ('Director','clave'),('Administrador','sexo')")
    def datos_prueba(self):
            personal_data = [
                ('12345678', 'Yusepe', 'Rossi', '1985-05-20', 'Av. Intercomunal Casa 10', 'yrossi@email.com', '0412-1112233', '10002233', 'Ingeniero de Sistemas', '2015-01-15', 'Comuna Central', 'Analista IT', 3, 1, 1),
                ('87654321', 'Beximar', 'Escalona', '1992-11-03', 'Calle 5 de Julio Edif. A', 'bescalona@email.com', '0414-4445566', '20005566', 'Lic. Educación', '2018-03-10', 'Comuna Norte', 'Docente de Aula', 3, 3, 1),
                ('11223344', 'Grober', 'Smith', '1970-08-25', 'Sector La Lucia Vereda 4', 'gsmith@email.com', '0416-7778899', '30008899', 'Bachiller Técnico', '2000-06-01', 'Comuna Sur', 'Mantenimiento', 1, 2, 2),
                ('20334455', 'Maria', 'Delgado', '1998-02-14', 'Res. Las Flores Apto 4-B', 'mdelgado@email.com', '0424-2223344', '40003344', 'Técnico Informática', '2022-05-20', 'Comuna Este', 'Secretaria', 2, 1, 1),
                ('9556677', 'Ricardo', 'Mendoza', '1975-12-30', 'Urb. El Parque Calle 2', 'rmendoza@email.com', '0412-9990011', '50000011', 'Magister Gerencia', '2010-09-01', 'Comuna Central', 'Director', 4, 4, 1)
            ]


            self.cursor.executemany("""
                INSERT OR REPLACE INTO Personal (
                    cedula, nombres, apellidos, fecha_nacimiento, direccion, 
                    correo, telefono, carnet_patria, titulo_obtenido, fecha_ingreso, 
                    comuna, cargo, id_grado_instruccion, id_categoria_personal, id_estado_laboral
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, personal_data)

            self.conexion.commit()
            self.conexion.commit()

db = DB(":memory:") 
db.crear_esquema()

