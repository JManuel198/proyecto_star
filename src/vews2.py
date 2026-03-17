import os
import tkinter as tk
from tkinter import ttk, messagebox
from database2 import *

class Star():
    def __init__(self,es_director=False):
        self.rootapp = tk.Tk()
        self.rootapp.geometry("1500x800")
        self.rootapp.title("Sistema Administrativo de Registros")
        
        self.superUsuario = es_director

        self.header_frame = tk.Frame(self.rootapp)
        self.header_frame.pack(side="top",fill="x")
        self.tree_frame = tk.Frame(self.rootapp)
        self.tree_frame.pack(side="top",fill="both",expand=True)
        self.crear_header_widgets()
        self.crear_tree_widgets()
        self.refrescar_tree()

    def crear_mostrar_ventana(self):
        self.ventana_mostrar = tk.Toplevel(self.rootapp)
        self.ventana_mostrar.geometry("450x700")

        campos = ("cedula","nombres","apellidos","fecha de nacimiento","edad","direccion","correo","telefono","carnet de la patria", "Grado Instruccion","titulo obtenido", "fecha de ingreso", "años de servicio", "comuna", "cargo","codigo de dependencia","Categoria Personal", "Estado Laboral")
        registro = db.consultar("SELECT cedula,nombres,apellidos,fecha_nacimiento,edad,direccion,correo,telefono,carnet_patria,grado_instruccion,titulo_obtenido,fecha_ingreso,anos_servicio,comuna,cargo,codigo_dependencia,categoria,estado_laboral FROM vista_personal_detallada WHERE cedula=(?)",(self.entry_cedula.get(),))
        datos = registro[0]
        for i,campo in enumerate(campos):
            label = tk.Label(self.ventana_mostrar,text=campo)
            label.grid(row=i,column=0)

            entry = tk.Entry(self.ventana_mostrar,width=25)
            entry.grid(row=i,column=1,pady=5,padx=3)
            valor_limpio = datos[i] if datos[i] is not None else ""
            entry.insert(0, valor_limpio)
            entry.config(state="readonly")
        cerrar = tk.Button(self.ventana_mostrar,text="Cerrar",command=self.ventana_mostrar.destroy)
        cerrar.grid(row=20,column=2)
    
    def crear_nuevo_ventana(self):
        self.ventana_nuevo = tk.Toplevel(self.rootapp)
        self.ventana_nuevo.geometry("700x600")

        grados_instruccion = db.consultar("SELECT id_grado_instruccion, descripcion FROM Grado_instruccion")
        self.mapa_grados = {desc: idx for idx, desc in grados_instruccion}
        estado_laboral = db.consultar("SELECT id_estado_laboral, nombre FROM Estado_laboral")
        self.mapa_estado_laboral = {desc: idx for idx, desc in estado_laboral}
        categoria_personal = db.consultar("SELECT id_categoria_personal, nombre FROM Categoria_personal")
        self.mapa_categoria = {desc: idx for idx, desc in categoria_personal}
        
        campos = ("Cedula","Nombres","Apellidos","Fecha de Nacimiento","Direccion","Correo","Telefono","Carnet de la Patria", "Grado de instruccion","Titulo obtenido", "Fecha de ingreso","Comuna","Cargo","Categoria Personal", "Estado Laboral")
        for i,campo in enumerate(campos):
            label = tk.Label(self.ventana_nuevo,text=campo)
            label.grid(row=i,column=0,padx=3,pady=3)

        self.ent_cedula = tk.Entry(self.ventana_nuevo)
        self.ent_cedula.grid(row=0,column=1)
        tk.Label(self.ventana_nuevo,text="Solo números. Ej: 17276333").grid(row=0,column=2)

        self.ent_nombres = tk.Entry(self.ventana_nuevo)
        self.ent_nombres.grid(row=1,column=1)

        self.ent_apellidos = tk.Entry(self.ventana_nuevo)
        self.ent_apellidos.grid(row=2,column=1)

        self.ent_fecha_nacimiento = tk.Entry(self.ventana_nuevo)
        self.ent_fecha_nacimiento.grid(row=3,column=1)
        tk.Label(self.ventana_nuevo,text="Formato: AAAA-MM-DD").grid(row=3,column=2)

        self.ent_direccion = tk.Entry(self.ventana_nuevo)
        self.ent_direccion.grid(row=4,column=1)

        self.ent_correo = tk.Entry(self.ventana_nuevo)
        self.ent_correo.grid(row=5,column=1)

        self.ent_telefono = tk.Entry(self.ventana_nuevo)
        self.ent_telefono.grid(row=6,column=1)

        self.ent_carnet_patria = tk.Entry(self.ventana_nuevo)
        self.ent_carnet_patria.grid(row=7,column=1)

        self.cb_grados = ttk.Combobox(self.ventana_nuevo,values=list(self.mapa_grados.keys()),state="readonly")
        self.cb_grados.grid(row=8,column=1)

        self.ent_titulo = tk.Entry(self.ventana_nuevo)
        self.ent_titulo.grid(row=9,column=1)

        self.ent_fecha_ingreso = tk.Entry(self.ventana_nuevo)
        self.ent_fecha_ingreso.grid(row=10,column=1)

        self.ent_comuna = tk.Entry(self.ventana_nuevo)
        self.ent_comuna.grid(row=11,column=1)

        self.ent_cargo = tk.Entry(self.ventana_nuevo)
        self.ent_cargo.grid(row=12,column=1)

        self.cb_categoria = ttk.Combobox(self.ventana_nuevo,values=list(self.mapa_categoria.keys()),state="readonly")
        self.cb_categoria.grid(row=13,column=1)

        self.cb_estado = ttk.Combobox(self.ventana_nuevo,values=list(self.mapa_estado_laboral.keys()),state="readonly")
        self.cb_estado.grid(row=14,column=1)

        # Agregamos el comando al botón
        boton_guardar = tk.Button(self.ventana_nuevo, text="Guardar", bg="#40a02b", fg="white", 
                                 command=self.guardar_registro_bd)
        boton_guardar.grid(row=20, column=1, pady=10)
    
    def preparar_edicion(self):
        cedula = self.entry_cedula.get().strip()
        if not cedula:
            messagebox.showerror("Error", "Por favor introduzca una cedula en el campo")
            return
        registro = db.consultar("SELECT * FROM Personal WHERE cedula = ?", [cedula])
        
        if registro:
            datos = registro[0] # [id, cedula, nombres, apellidos, fecha_nac, edad, dir, correo, tel, carnet, titulo, fecha_ing, anos, comuna, cargo, cod, id_g, id_c, id_e]
            
            # Abrimos una ventana gemela a la de "Nuevo"
            self.crear_nuevo_ventana()
            self.ventana_nuevo.title(f"Modificar Registro de: {cedula}")
            
            self.ent_cedula.insert(0, datos[1])
            self.ent_cedula.config(state="disabled") # Bloqueamos la cédula para no romper la PK
            
            self.ent_nombres.insert(0, datos[2])
            self.ent_apellidos.insert(0, datos[3])
            self.ent_fecha_nacimiento.insert(0, datos[4] if datos[4] else "")
            self.ent_direccion.insert(0, datos[6] if datos[6] else "")
            self.ent_correo.insert(0, datos[7] if datos[7] else "")
            self.ent_telefono.insert(0, datos[8] if datos[8] else "")
            self.ent_carnet_patria.insert(0, datos[9] if datos[9] else "")
            self.ent_titulo.insert(0, datos[10] if datos[10] else "")
            self.ent_fecha_ingreso.insert(0, datos[11] if datos[11] else "")
            self.ent_comuna.insert(0, datos[13] if datos[13] else "")
            self.ent_cargo.insert(0, datos[14] if datos[14] else "")

            # Auto seleccion de los combohbox

            id_a_grado = {v: k for k, v in self.mapa_grados.items()}
            id_a_cat = {v: k for k, v in self.mapa_categoria.items()}
            id_a_est = {v: k for k, v in self.mapa_estado_laboral.items()}

            self.cb_grados.set(id_a_grado.get(datos[16], ""))
            self.cb_categoria.set(id_a_cat.get(datos[17], ""))
            self.cb_estado.set(id_a_est.get(datos[18], ""))

            # Cambiar el comportamiento del botón Guardar (no tocar)
            for child in self.ventana_nuevo.winfo_children():
                if isinstance(child, tk.Button) and child["text"] == "Guardar":
                    child.config(text="Actualizar datos", command=self.actualizar_registro_bd)

    def actualizar_registro_bd(self):
        # Desbloqueamos temporalmente para leer el valor
        self.ent_cedula.config(state="normal")
        cedula = self.ent_cedula.get()
        self.ent_cedula.config(state="disabled")

        try:
            id_grado = self.mapa_grados.get(self.cb_grados.get())
            id_cat = self.mapa_categoria.get(self.cb_categoria.get())
            id_est = self.mapa_estado_laboral.get(self.cb_estado.get())

            # Tupla de datos para el UPDATE
            datos_update = (
                self.ent_nombres.get(),
                self.ent_apellidos.get(),
                self.ent_fecha_nacimiento.get(),
                self.ent_direccion.get(),
                self.ent_correo.get(),
                self.ent_telefono.get(),
                self.ent_carnet_patria.get(),
                self.ent_titulo.get(),
                self.ent_fecha_ingreso.get(),
                self.ent_comuna.get(),
                self.ent_cargo.get(),
                id_grado,
                id_cat,
                id_est,
                cedula # El WHERE
            )

            sql = """UPDATE Personal SET 
                        nombres=?, apellidos=?, fecha_nacimiento=?, direccion=?, 
                        correo=?, telefono=?, carnet_patria=?, titulo_obtenido=?, 
                        fecha_ingreso=?, comuna=?, cargo=?, id_grado_instruccion=?, 
                        id_categoria_personal=?, id_estado_laboral=?
                     WHERE cedula=?"""

            db.consultar(sql, datos_update)
            
            messagebox.showinfo("Éxito", "Los datos han sido actualizados correctamente.", parent=self.ventana_nuevo)
            self.refrescar_tree()
            self.ventana_nuevo.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el registro: {e}", parent=self.ventana_nuevo)
    
    def guardar_registro_bd(self):
        cedula = self.ent_cedula.get().strip()

        # 1. Validaciones básicas
        if not cedula.isdigit():
            messagebox.showwarning("Error", "La cédula debe ser numérica",parent=self.ventana_nuevo)
            return

        # 2. Verificar si la cédula ya existe (Tu requerimiento especial)
        existe = db.consultar("SELECT 1 FROM Personal WHERE cedula = ?", [cedula])
        if existe:
            messagebox.showerror("Cédula Duplicada", f"La cédula {cedula} ya se encuentra registrada en el sistema.",parent=self.ventana_nuevo)
            return

        # 3. Traducir Combos a IDs
        try:
            id_grado = self.mapa_grados.get(self.cb_grados.get())
            id_cat = self.mapa_categoria.get(self.cb_categoria.get())
            id_est = self.mapa_estado_laboral.get(self.cb_estado.get())

            if not all([id_grado, id_cat, id_est]):
                messagebox.showwarning("Faltan datos", "Por favor selecciona opciones en todos los menús desplegables",parent=self.ventana_nuevo)
                return

            # 4. Preparar la tupla de datos (Orden exacto de la tabla Personal)
            datos = (
                cedula,
                self.ent_nombres.get(),
                self.ent_apellidos.get(),
                self.ent_fecha_nacimiento.get(),
                self.ent_direccion.get(),
                self.ent_correo.get(),
                self.ent_telefono.get(),
                self.ent_carnet_patria.get(),
                self.ent_titulo.get(),
                self.ent_fecha_ingreso.get(),
                self.ent_comuna.get(),
                self.ent_cargo.get(),
                id_grado,
                id_cat,
                id_est
            )

            # 5. Ejecutar el INSERT
            sql = """INSERT INTO Personal (
                cedula, nombres, apellidos, fecha_nacimiento, direccion, 
                correo, telefono, carnet_patria, titulo_obtenido, fecha_ingreso, 
                comuna, cargo, id_grado_instruccion, id_categoria_personal, id_estado_laboral
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

            db.consultar(sql, datos)
            
            messagebox.showinfo("Éxito", "Registro guardado exitosamente",parent=self.ventana_nuevo)
            self.refrescar_tree() # Actualiza la tabla principal
            self.ventana_nuevo.destroy() # Cierra el formulario

        except Exception as e:
            messagebox.showerror("Error Crítico", f"No se pudo guardar en la base de datos: {e}")


    def borrar_registro(self):
        cedula = self.entry_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Atencion", "El campo de cédula está vacío")
            return 

        if not cedula.isdigit():
            messagebox.showwarning("Atencion","Por favor introduzca un valor valido")
            return
        
        existe = db.consultar("SELECT 1 FROM Personal WHERE cedula = ?", [cedula])
        if not existe:
            messagebox.showerror("Error", "Esa cédula no existe en la base de datos")
            return

        confirmar = messagebox.askyesno("Confirmacion","¿Esta Seguro que desea eliminar este registro?")
        if confirmar:
            db.consultar("DELETE FROM Personal WHERE cedula = ?",(cedula,))
            
            messagebox.showinfo("Exito","El registro fue eliminado con exito")
            self.refrescar_tree()
            self.entry_cedula.delete(0, tk.END)

    def crear_header_widgets(self):
        self.boton_refrescar = tk.Button(self.header_frame,text="󰑐 Refrescar",command=self.refrescar_tree,font=("RobotoMono Nerd Font", 11, "bold"))
        self.boton_refrescar.grid(row=0,column=0)
        self.entry_cedula = tk.Entry(self.header_frame,font=("RobotoMono Nerd Font", 11, "bold"))
        self.entry_cedula.grid(row=0,column=1)
        self.boton_buscar = tk.Button(self.header_frame,text="󰍉 Buscar",command=self.buscar_cedula,font=("RobotoMono Nerd Font", 11, "bold"))
        self.boton_buscar.grid(row=0,column=2)
        self.boton_nuevo = tk.Button(self.header_frame,text="󰐕 Nuevo",command=self.crear_nuevo_ventana,font=("RobotoMono Nerd Font", 11, "bold"),bg="#40a02b",fg="white")
        self.boton_modificar = tk.Button(self.header_frame,text="󰏫 Modificar",command=self.preparar_edicion,font=("RobotoMono Nerd Font", 11, "bold"),bg="#7287fd",fg="white")
        self.boton_eliminar = tk.Button(self.header_frame,text="󰆴 Eliminar",command=self.borrar_registro,bg="#e64553",fg="white",font=("RobotoMono Nerd Font", 11, "bold"))

        if self.superUsuario == True:
            self.boton_nuevo.grid(row=0,column=3)
            self.boton_eliminar.grid(row=0,column=5)
            self.boton_modificar.grid(row=0,column=4)

    
    def crear_tree_widgets(self):
        self.tree_columnas = ("cedula","nombres","apellidos","categoria","anos","estado",)
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree['show'] = 'headings'
        self.tree['columns'] = self.tree_columnas
        self.tree.heading("cedula",text="Cedula")
        self.tree.heading("nombres",text="Nombres")
        self.tree.heading("apellidos",text="Apellidos")
        self.tree.heading("categoria",text="Categoria de Empleado")
        self.tree.heading("anos",text="Años de Servicio")
        self.tree.heading("estado",text="Estado Laboral")

        self.tree.pack(fill="both",expand=True)
    
    def refrescar_tree(self):
        for registro in self.tree.get_children():
            self.tree.delete(registro)
        
        for registro in db.consultar("SELECT cedula, nombres, apellidos, categoria, anos_servicio, estado_laboral FROM vista_personal_detallada"):
            self.tree.insert("", "end", values=registro)

    def buscar_cedula(self):
        busqueda = self.entry_cedula.get().strip()
        if not busqueda:
            messagebox.showwarning("Error","Por favor introduza una cedula")
            return
        
        existe = db.consultar("SELECT 1 FROM personal WHERE cedula=(?)",(busqueda,))
        if existe:
            self.crear_mostrar_ventana()
        else:
            messagebox.showwarning("Error","No se encontro la cedula")

if __name__ == "__main__":
    def iniciar_sesion():
        # IMPORTANTE: Usamos nombres distintos para el Widget y el Texto
        # Si haces 'nombre = nombre.get()', pierdes el acceso al widget Entry
        usuario_txt = entry_nombre.get().strip()
        pass_txt = entry_password.get().strip()

        if not usuario_txt or not pass_txt:
            messagebox.showwarning("Atención", "Por favor llene todos los campos", parent=login)
            return

        # Consulta segura para verificar credenciales
        # Buscamos exactamente ese usuario y esa clave
        consulta = db.consultar("SELECT nombre FROM Usuario WHERE nombre = ? AND password = ?", (usuario_txt, pass_txt))
        
        if consulta:
            # Si la consulta devuelve algo, los datos son válidos
            rol = consulta[0][0] # Obtenemos el nombre del usuario (ej: 'Director')
            
            # Destruimos la ventana de login antes de lanzar la principal
            login.destroy()
            
            # Si el usuario es "Director", pasamos True para permisos especiales
            app = Star(es_director=(rol == "Director"))
            app.rootapp.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos", parent=login)
    
    login = tk.Tk()
    login.title("Login - STAR")
    
    frame_titulo = tk.Frame(login)
    frame_titulo.pack(padx=40, pady=5)
    frame_entry = tk.Frame(login)
    frame_entry.pack(padx=40, pady=5)

    try:
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(directorio_actual, "logo.png")
        logo = tk.PhotoImage(file=ruta_imagen)
        image_logo = tk.Label(frame_titulo, image=logo)
        image_logo.grid(row=0, column=0)
    except Exception:
        tk.Label(frame_titulo, text="[Logo no encontrado]").grid(row=0, column=0)

    tk.Label(frame_titulo, text="Sistema Administrativo de Registros", 
             font=("RobotoMono Nerd Font", 12, "bold")).grid(row=1, column=0, pady=10)

    tk.Label(frame_entry, text="Nombre: ").grid(row=0, column=0)
    entry_nombre = tk.Entry(frame_entry) # Cambiamos el nombre de la variable
    entry_nombre.grid(row=0, column=1, pady=5)

    tk.Label(frame_entry, text="Contraseña: ").grid(row=1, column=0)
    entry_password = tk.Entry(frame_entry, show="*") # Ocultamos la clave
    entry_password.grid(row=1, column=1, pady=5)

    ingresar = tk.Button(login, text="󰍂 Ingresar", command=iniciar_sesion, bg="#40a02b", fg="white")
    ingresar.pack(pady=10)

    login.mainloop()