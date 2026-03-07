import sqlite3
# Datos dummy para la tabla principal
# Nota: id_grado, id_cargo, id_tipo, id_estado son los números que insertamos arriba
datos_personal = [
    (32160371, "Yusepe", "Moroso Rossi", "Calle 10, Casa 5", "yusepe@mail.com", "0412-1112233", "0012345", "Comuna A", "Ing. Sistemas", 4, 3, 1, 1),
    (25987654, "Beximar", "Rodriguez", "Av. Principal 12", "bexi@mail.com", "0414-9998877", "0054321", "Comuna B", "Lic. Administracion", 3, 1, 2, 1),
    (18456123, "Carlos", "Perez", "Barrio El Centro", "carlos@mail.com", "0416-5554433", "0099887", "Comuna C", "Bachiller", 1, 5, 1, 2)
]

query_insert = """
    INSERT INTO personal (
        cedula, nombres, apellidos, direccion, correo, telefono,
        carnet_patria, comuna, titulo_obtenido,
        id_grado, id_cargo, id_tipo_personal, id_estado_laboral
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


# SIEMPRE se debe trabjar usando los metodos de esta clase, se debe evitar a toda cosa usar funciones sqlite directas
# para evitar problemas
class ClaseDB:
    def __init__(self,nombre_db):
        self.conexion = sqlite3.connect(nombre_db)
        self.cursor = self.conexion.cursor()

    def crear_modelo_base(self):
        # activamos las claves foraneas
        self.conexion.execute("PRAGMA foreign_keys = ON")
        # Tablas maestras
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usuario(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS grado_instruccion(id_grado INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cargo(id_cargo INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tipo_personal(id_tipo_personal INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS estado_laboral(id_estado_laboral INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT)")

        # Tabla principal
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula INTEGER,
                nombres TEXT,
                apellidos TEXT,
                direccion TEXT,
                correo TEXT,
                telefono TEXT,
                carnet_patria TEXT,
                comuna TEXT,
                titulo_obtenido TEXT,
                id_grado INTEGER,
                id_cargo INTEGER,
                id_tipo_personal INTEGER,
                id_estado_laboral INTEGER,

                FOREIGN KEY (id_grado) REFERENCES grado_instruccion (id_grado),
                FOREIGN KEY (id_cargo) REFERENCES cargo (id_cargo),
                FOREIGN KEY (id_tipo_personal) REFERENCES tipo_personal (id_tipo_personal),
                FOREIGN KEY (id_estado_laboral) REFERENCES estado_laboral (id_estado_laboral)
            )
        """)


        # Grados de Instrucción
        grados = [("Bachiller",), ("Técnico Medio",), ("Licenciado",), ("Ingeniero",), ("Magister",)]
        self.cursor.executemany("INSERT INTO grado_instruccion (nombre) VALUES (?)", grados)

        # Cargos
        cargos = [("Analista",), ("Supervisor",), ("Gerente",), ("Asistente",), ("Obrero",)]
        self.cursor.executemany("INSERT INTO cargo (nombre) VALUES (?)", cargos)

        # Tipos de Personal
        tipos = [("Fijo",), ("Contratado",), ("Comisión de Servicio",)]
        self.cursor.executemany("INSERT INTO tipo_personal (nombre) VALUES (?)", tipos)

        # Estados Laborales
        estados = [("Activo",), ("Reposo",), ("Vacaciones",), ("Jubilado",)]
        self.cursor.executemany("INSERT INTO estado_laboral (descripcion) VALUES (?)", estados)

        self.conexion.commit()
    def print_tabla(self,tabla):  ### abandonado #### NO USAR
        self.cursor.execute(f"SELECT * FROM {tabla}")
        print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def consultar(self,sql,parametros=()):
        self.cursor.execute(sql,parametros)
        self.conexion.commit()
        return self.cursor.fetchall()

    def cerrar(self):
        self.conexion.close()

    def datos_prueba(self):
        self.cursor.executemany(query_insert, datos_personal)
        self.conexion.commit()

if __name__ == "__main__":
    from tkinter import messagebox
    print("================================")
    print("Ejecuta vews.py, no este archivo")
    messagebox.showinfo("Error","Por favor abra el archivo vews.py, no este")
