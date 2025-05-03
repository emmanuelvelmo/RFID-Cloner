import tkinter
from tkinter import ttk
import os

class vent_princ:
    def __init__(self):
        # VENTANA PRINCIPAL
        # Configuración inicial de la ventana principal
        self.instancia_princ = tkinter.Tk()
        self.instancia_princ.title("RFID Cloner")
        self.instancia_princ.configure(bg = "white")
        
        # Añadir padding general a toda la ventana
        self.instancia_princ['padx'] = 5
        self.instancia_princ['pady'] = 5

        # MENÚ SUPERIOR
        # Crea la barra de menú principal
        barra_menu = tkinter.Menu(self.instancia_princ)
        
        # Crea el menú Archivo con su opción Guardar
        menu_archivo = tkinter.Menu(barra_menu, tearoff = 0)
        menu_archivo.add_command(label = "Guardar", command = self.guardar_datos)
        
        # Añade el menú Archivo a la barra principal
        barra_menu.add_cascade(label = "Archivo", menu = menu_archivo)
        self.instancia_princ.config(menu = barra_menu)

        # SECCIÓN DE BOTONES
        # Marco contenedor para los botones Leer/Escribir
        self.marco_botones = tkinter.Frame(self.instancia_princ, bg = "white")
        self.marco_botones.pack(fill = tkinter.X, padx = 5, pady = 5)
        
        # Botón para leer datos
        self.boton_leer = tkinter.Button(self.marco_botones, text = "Leer")
        self.boton_leer.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X, padx = (0, 2))
        
        # Botón para escribir datos
        self.boton_escribir = tkinter.Button(self.marco_botones, text = "Escribir")
        self.boton_escribir.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X, padx = (2, 0))

        # ÁREA DE TEXTO
        # Caja de texto para mostrar información
        self.caja_texto = tkinter.Text(self.instancia_princ, font = ("Arial", 11), height = 3, bg = "white", fg = "black", bd = 1)
        self.caja_texto.pack(fill = tkinter.X, padx = 5, pady = 5)

        # BARRA DE ESTADO
        # Etiqueta para mostrar el estado de las operaciones
        self.label_status = tkinter.Label(self.instancia_princ, text = "", bg = "#eeeeee", fg = "#444444", font = ("Arial", 11))
        self.label_status.pack(fill = tkinter.X,padx = 5, pady = 5)
        
        # Línea divisoria visual
        self.linea_div = tkinter.Frame(self.instancia_princ, height = 1, bg = "#d3d3d3")
        self.linea_div.pack(fill = tkinter.X, padx = 5, pady = 5)

        # FORMULARIO DE DATOS
        # Marco principal para el formulario
        self.marco_formulario = tkinter.Frame(self.instancia_princ, bg = "white")
        self.marco_formulario.pack(fill = tkinter.X, padx = 5, pady = 5, expand = True)

        # Columna para el campo Usuario
        self.col_usuario = tkinter.Frame(self.marco_formulario, bg = "white")
        self.col_usuario.pack(side = tkinter.LEFT, expand = True, fill = tkinter.BOTH, padx = (0, 4))
        
        self.label_usuario = tkinter.Label(self.col_usuario, text = "Usuario", bg = "white", anchor = "w", font = ("Arial", 11))
        self.label_usuario.pack(fill = tkinter.X, pady = (0, 4))
        
        self.caja_usuario = tkinter.Entry(self.col_usuario, font = ("Arial", 11), bg = "white", fg = "black", bd = 1)
        self.caja_usuario.pack(fill = tkinter.BOTH, expand = True)

        # Columna para el campo Código
        self.col_codigo = tkinter.Frame(self.marco_formulario, bg = "white")
        self.col_codigo.pack(side = tkinter.LEFT, expand = True, fill = tkinter.BOTH, padx = 4)
        
        self.label_codigo = tkinter.Label(self.col_codigo, text = "Código", bg = "white", anchor = "w", font = ("Arial", 11))
        self.label_codigo.pack(fill = tkinter.X, pady = (0, 4))
        
        self.caja_código = tkinter.Entry(self.col_codigo, font = ("Arial", 11), bg = "white", fg = "black", bd = 1)
        self.caja_código.pack(fill = tkinter.BOTH, expand = True)

        # Columna para el botón Agregar
        self.col_boton = tkinter.Frame(self.marco_formulario, bg = "white")
        self.col_boton.pack(side = tkinter.LEFT, expand = True, fill = tkinter.BOTH, padx = (4, 0))
        
        self.label_vacio = tkinter.Label(self.col_boton, text = "", bg = "white", anchor = "w", font = ("Arial", 11))
        self.label_vacio.pack(fill = tkinter.X, pady = (0, 4))
        
        self.boton_agregar = tkinter.Button(self.col_boton, text = "Agregar")
        self.boton_agregar.pack(fill = tkinter.BOTH, expand = True)

        # TABLA DE DATOS
        # Marco contenedor para la tabla
        self.marco_tabla = tkinter.Frame(self.instancia_princ, bg = "white")
        self.marco_tabla.pack(fill = tkinter.BOTH, expand = True, padx = 5, pady = 5)

        # Barra de desplazamiento vertical
        self.scroll_tabla = tkinter.Scrollbar(self.marco_tabla)
        self.scroll_tabla.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        # Configuración de la tabla (Treeview)
        self.tabla = ttk.Treeview(self.marco_tabla, columns = ("Usuario", "Código"), show = "headings", yscrollcommand = self.scroll_tabla.set, height = 8)
        
        self.tabla.pack(fill = tkinter.BOTH, expand = True)

        # Vincula la scrollbar con la tabla
        self.scroll_tabla.config(command = self.tabla.yview)

        # Configura las columnas de la tabla
        self.tabla.heading("Usuario", text = "Usuario", anchor = "center")
        self.tabla.heading("Código", text = "Código", anchor = "center")

        self.tabla.column("Usuario", anchor = "center", width = 100)
        self.tabla.column("Código", anchor = "center", width = 100)

        # MENÚ CONTEXTUAL
        # Menú que aparece al hacer clic derecho en la tabla
        self.menu_contextual = tkinter.Menu(self.instancia_princ, tearoff = 0)
        self.menu_contextual.add_command(label = "Eliminar", command = self.eliminar_fila_seleccionada)
        
        self.tabla.bind("<Button-3>", self.mostrar_menu_contextual)

        # Carga los datos iniciales desde el archivo
        self.cargar_datos()
    
    # FUNCIONES
    # Cargar datos del archivo de texto hacia la tabla
    def cargar_datos(self):
        # Carga los datos desde el archivo data.txt a la tabla
        archivo_val = "data.txt"
        
        if os.path.exists(archivo_val):
            with open(archivo_val, "r", encoding = "utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    
                    if "-" in linea:
                        nombre, código = linea.split("-", 1)
                        self.tabla.insert("", "end", values = (nombre.strip(), código.strip()))
        else:
            self.label_status.config(text = "Datos no encontrados")
    
    # Mostrar el menú contextual en tabla
    def mostrar_menu_contextual(self, event):
        # Muestra el menú contextual al hacer clic derecho en una celda
        region = self.tabla.identify("region", event.x, event.y)
        
        if region == "cell":
            iid = self.tabla.identify_row(event.y)
            
            if iid:
                self.tabla.selection_set(iid)
                self.menu_contextual.post(event.x_root, event.y_root)

    # Eliminar filas de la tabla
    def eliminar_fila_seleccionada(self):
        # Elimina la fila seleccionada de la tabla
        seleccion = self.tabla.selection()
        
        for item in seleccion:
            self.tabla.delete(item)

    # Guardar tabla en archivo de texto
    def guardar_datos(self):
        # Guarda los datos de la tabla en el archivo data.txt
        datos = self.tabla.get_children()
        
        with open("data.txt", "w", encoding = "utf-8") as f:
            for item in datos:
                nombre, código = self.tabla.item(item)["values"]
                f.write(f"{nombre}-{código}\n")
        
        self.label_status.config(text = "Datos guardados")
    
    # Agregar campos a la tabla
    def agregar_datos_tabla():
        # Tomar los textos de los campos
        
        
        # Verificar que ambos campos no sean nulos y estén en el formato correcto
        
        
        # Agregar datos en la tabla
        
    
    # Leer datos desde una tarjeta
    def leer_rfid():
        # Leer RFID
        
        
        # Mostrar código en etiqueta de estado
        
    
    # Escribir datos a una tarjeta
    def escribir_rfid():
        # Escribir RFID
        
        
        # Actualizar etiqueta de estado
        
    
# Punto de entrada de la aplicación
if __name__ == "__main__":
    vent_princ = vent_princ()
    vent_princ.instancia_princ.mainloop()