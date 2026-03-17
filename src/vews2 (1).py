import tkinter as tk
from tkinter import ttk, messagebox
from database2 import *

class Star():
    def __init__(self):
        self.rootapp = tk.Tk()
        self.rootapp.geometry("1500x800")
        
        self.header_frame = tk.Frame(self.rootapp)
        self.header_frame.pack(side="top",fill="x")
        self.tree_frame = tk.Frame(self.rootapp)
        self.tree_frame.pack(side="top",fill="both",expand=True)
        self.crear_header_widgets()
        self.crear_tree_widgets()
        self.refrescar_tree()

    def crear_mostrar_ventana(self):
        self.ventana_mostrar = tk.Toplevel(self.rootapp)
        self.ventana_mostrar.geometry("400x700")

        campos = ("cedula","nombres","apellidos","fecha de nacimiento","edad","direccion","correo","telefono","carnet de la patria", "Grado Instruccion","titulo obtenido", "fecha de ingreso", "años de servicio", "comuna", "cargo","codigo de dependencia","Categoria Personal", "Estado Laboral")
        registro = db.consultar("SELECT cedula,nombres,apellidos,fecha_nacimiento,edad,direccion,correo,telefono,carnet_patria,grado_instruccion,titulo_obtenido,fecha_ingreso,anos_servicio,comuna,cargo,codigo_dependencia,categoria,estado_laboral FROM vista_personal_detallada WHERE cedula=(?)",(self.entry_cedula.get(),))
        datos = registro[0]
        for i,campo in enumerate(campos):
            label = tk.Label(self.ventana_mostrar,text=campo)
            label.grid(row=i,column=0)

            entry = tk.Entry(self.ventana_mostrar)
            entry.grid(row=i,column=1)
            entry.insert(0,datos[i])
            entry.config(state="readonly")
    
    def crear_header_widgets(self):
        self.boton_refrescar = tk.Button(self.header_frame,text="Refrescar",command=self.refrescar_tree)
        self.boton_refrescar.grid(row=0,column=0)
        self.entry_cedula = tk.Entry(self.header_frame)
        self.entry_cedula.grid(row=0,column=1)
        self.boton_buscar = tk.Button(self.header_frame,text="Buscar",command=self.buscar_cedula)
        self.boton_buscar.grid(row=0,column=2)
        self.boton_nuevo = tk.Button(self.header_frame,text="Nuevo")
        self.boton_nuevo.grid(row=0,column=3)
        self.boton_modificar = tk.Button(self.header_frame,text="Modificar")
        self.boton_modificar.grid(row=0,column=4)
        self.boton_eliminar = tk.Button(self.header_frame,text="Eliminar")
        self.boton_eliminar.grid(row=0,column=5)
    
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
        busqueda = self.entry_cedula.get()
        existe = db.consultar("SELECT 1 FROM personal WHERE cedula=(?)",(busqueda,))
        if existe:
            messagebox.showinfo("Yay","Se encontro!!!!")
            self.crear_mostrar_ventana()
        else:
            messagebox.showinfo("huh","no se encontro...")



app = Star()
app.rootapp.mainloop()