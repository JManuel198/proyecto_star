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

        self.boton_mostrar = tk.Button(self.header_frame,text="Mostrar",command=self.verificar_cedula)
        self.boton_mostrar.grid(row=0,column=2)

        self.textbox_buscar = tk.Entry(self.header_frame)
        self.textbox_buscar.grid(row=0,column=1)

        self.boton_nuevo = tk.Button(self.header_frame,text="Nuevo")
        self.boton_nuevo.grid(row=0,column=3)

        self.boton_modificar = tk.Button(self.header_frame,text="Modificar")
        self.boton_modificar.grid(row=0,column=4)

        self.boton_borrar = tk.Button(self.header_frame,text="Eliminar")
        self.boton_borrar.grid(row=0,column=5)

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

    def ventana_movimientos(self):
        self.ventana_mostrar = tk.Toplevel(self.root)
        self.ventana_mostrar.title("Nueva ventana")
        self.ventana_mostrar.geometry("800x500")
        self.ventana_mostrar.grab_set()

        self.movimientos_widgets()

    def movimientos_widgets(self):
        self.movimientos_datos()
        self.movimientos_labels()

    def movimientos_datos(self):
        registro = db.consultar("SELECT * FROM personal WHERE cedula=(?)",(self.textbox_buscar.get(),))
        print(registro)
        self.mostrar_cedula = tk.Label(self.ventana_mostrar,text=registro[0][1]).grid(row=0,column=1)  # Cedula
        self.mostrar_nombres = tk.Label(self.ventana_mostrar,text=registro[0][2]).grid(row=1,column=1) # Nombres
        self.mostrar_apellidos = tk.Label(self.ventana_mostrar,text=registro[0][3]).grid(row=2,column=1)
        self.mostrar_direccion = tk.Label(self.ventana_mostrar,text=registro[0][4]).grid(row=3,column=1)
        self.mostrar_correo = tk.Label(self.ventana_mostrar,text=registro[0][5]).grid(row=4,column=1)
        self.mostrar_telefono = tk.Label(self.ventana_mostrar,text=registro[0][6]).grid(row=5,column=1)
        self.mostrar_carnet = tk.Label(self.ventana_mostrar,text=registro[0][7]).grid(row=6,column=1)
        self.mostrar_comuna = tk.Label(self.ventana_mostrar,text=registro[0][8]).grid(row=7,column=1)

    def movimientos_labels(self):
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Cedula: ").grid(row=0,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Nombre: ").grid(row=1,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Apellidos: ").grid(row=2,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Direccion: ").grid(row=3,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Correo: ").grid(row=4,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="N. Telf: ").grid(row=5,column=0)
        self.nombres_label = tk.Label(self.ventana_mostrar,text="Carnet P.: ").grid(row=6,column=0)






    def refrescar_tree(self):
        for registro in self.tree.get_children():
            self.tree.delete(registro)

        for registro in db.consultar("SELECT * FROM personal"):
            # print(registro)
            self.tree.insert("","end",values=registro)

    def verificar_cedula(self):
        self.cedula_buscar = int(self.textbox_buscar.get())
        cedulas_db = []
        for fila in db.consultar("SELECT cedula FROM personal"):
            cedulas_db.append(fila[0])
            # print(cedulas_db)
        if self.cedula_buscar in cedulas_db:
            messagebox.showinfo("Yay","EXISTE!!!11!!")
            self.ventana_movimientos()

        else:
            messagebox.showinfo("No encontrado","No se encontro en la base de datos.")

if __name__ == "__main__":
    db = ClaseDB(":memory:")
    db.crear_modelo_base()
    db.datos_prueba()

    aplicacion = Star()
    aplicacion.root.mainloop()
    db.cerrar()
