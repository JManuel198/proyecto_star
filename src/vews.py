from database import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Star():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("2000x1000")

        self.header_frame = tk.Frame(self.root, bg="lightgray")
        self.header_frame.pack(side="top",fill="x")
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(side="top",fill="both",expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        self.crear_widgets_header()
        self.crear_widgets_tree()

    def crear_widgets_header(self):
        self.boton_refrescar = tk.Button(self.header_frame,text="refrescar",command=self.refrescar_tree)
        self.boton_refrescar.grid(row=0,column=0)

        self.boton_mostrar = tk.Button(self.header_frame,text="Mostrar",command=self.ventana_mostrar)
        self.boton_mostrar.grid(row=0,column=1)
        self.boton_nuevo = tk.Button(self.header_frame,text="Nuevo",command=lambda:messagebox.showinfo("Work in Progress","Aqui se mostrara la ventana"))
        self.boton_nuevo.grid(row=0,column=2)
        self.boton_modificar = tk.Button(self.header_frame,text="Modificar",command=lambda:messagebox.showinfo("Work in Progress","Aqui se mostrara la ventana"))
        self.boton_modificar.grid(row=0,column=3)
        self.boton_borrar = tk.Button(self.header_frame,text="Eliminar",command=lambda:messagebox.showinfo("Work in Progress","Aqui se mostrara la ventana"))
        self.boton_borrar.grid(row=0,column=4)

    def crear_widgets_tree(self):
        self.tree_columnas = ('codigo','cedula','nombres','apellidos','direccion','correo','telefono','carnet_patria','comuna','titulo_obtenido','id_grado','id_cargo','id_tipo_personal','id_estado_laboral')
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree['show'] = "headings"
        self.tree['columns'] = self.tree_columnas
        self.tree.heading("codigo",text="ID")
        self.tree.column("codigo",width=3)
        self.tree.heading("cedula",text="Cedula")
        self.tree.column("cedula",width=70)
        self.tree.heading("nombres",text="Nombres")
        self.tree.heading("apellidos",text="Apellidos")
        self.tree.heading("direccion",text="Direccion")
        self.tree.heading("telefono",text="Telefono")
        self.tree.heading("correo",text="Correo")
        self.tree.heading("carnet_patria",text="C. Patria")
        self.tree.heading("comuna",text="Comuna")
        self.tree.heading("titulo_obtenido",text="Titulo")
        self.tree.heading("id_grado",text="Grado")
        self.tree.heading("id_cargo",text="Cargo")
        self.tree.heading("id_tipo_personal",text="Tipo de Personal")
        self.tree.heading("id_estado_laboral",text="Estado")

        self.tree.grid(row=0,column=0)
        self.refrescar_tree()

    def ventana_mostrar(self):
        self.ventana_mostrar = tk.Toplevel(self.root)
        self.ventana_mostrar.title("Nueva ventana")
        self.ventana_mostrar.geometry("200x200")

        self.ventana_mostrar.grab_set()
        self.ventana_label = tk.Label(self.ventana_mostrar,text="Esta es la ventana que muestra la informacion en solo lectura")
        self.ventana.grid(row=0,column=0)

    def refrescar_tree(self):
        for registro in self.tree.get_children():
            self.tree.delete(registro)

        for registro in db.consultar("SELECT * FROM personal"):
            print(registro)
            self.tree.insert("","end",values=registro)


db = ClaseDB(":memory:")
db.crear_modelo_base()
db.datos_prueba()

aplicacion = Star()
aplicacion.root.mainloop()
db.cerrar
