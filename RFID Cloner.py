import tkinter
from tkinter import ttk
import os
import threading
import time
import RPi.GPIO as GPIO
from MFRC522 import MFRC522
 
class vent_princ:
    def __init__(self):
        # Raspberry Pi 4 con RFID-MFRC522 (GPIO 8 - SDA, GPIO 11 - SCLK, GPIO 17 - RST, GPIO 10 - MOSI, GPIO 9 - MISO)
        self.lector_val = MFRC522()
       
        # Buffer de la tabla
        self.datos_tabla = []
       
        # VENTANA PRINCIPAL
        # Configuración inicial de la ventana principal
        self.instancia_princ = tkinter.Tk()
        self.instancia_princ.title("RFID Cloner")
        self.instancia_princ.configure(bg = "white")
       
        # Añadir padding general a toda la ventana
        self.instancia_princ['padx'] = 4
        self.instancia_princ['pady'] = 4
 
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
        self.marco_botones.pack(fill = tkinter.X, padx = 4, pady = 4)
       
        # Botón para leer datos
        self.boton_leer = tkinter.Button(self.marco_botones, text = "Leer", command = self.iniciar_lectura_rfid)
        self.boton_leer.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X, padx = (0, 2))
       
        # Botón para escribir datos
        self.boton_escribir = tkinter.Button(self.marco_botones, text = "Escribir")
        self.boton_escribir.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X, padx = (2, 0))
 
        # ÁREA DE TEXTO
        # Caja de texto para mostrar información
        self.caja_texto = tkinter.Text(self.instancia_princ, font = ("Arial", 11), height = 2, bg = "white", fg = "black", bd = 1)
        self.caja_texto.pack(fill = tkinter.X, padx = 4, pady = 4)
 
        # BARRA DE ESTADO
        # Etiqueta para mostrar el estado de las operaciones
        self.label_status = tkinter.Label(self.instancia_princ, text = "", bg = "#eeeeee", fg = "#444444", font = ("Arial", 11))
        self.label_status.pack(fill = tkinter.X,padx = 4, pady = 4)
       
        # Línea divisoria visual
        self.linea_div = tkinter.Frame(self.instancia_princ, height = 1, bg = "#d3d3d3")
        self.linea_div.pack(fill = tkinter.X, padx = 4, pady = 4)
 
        # FORMULARIO DE DATOS
        # Marco principal para el formulario
        self.marco_formulario = tkinter.Frame(self.instancia_princ, bg = "white")
        self.marco_formulario.pack(fill = tkinter.X, padx = 4, pady = 4, expand = True)
 
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
       
        # BARRA DE BÚSQUEDA
        self.barra_busqueda = tkinter.Frame(self.instancia_princ, bg = "white")
        self.barra_busqueda.pack(fill = tkinter.X, padx = 4, pady = 4)
 
        self.caja_busqueda = tkinter.Entry(self.barra_busqueda, font = ("Arial", 11), bg = "white", fg = "gray", bd = 1)
        self.caja_busqueda.insert(0, "Buscar...")
        self.caja_busqueda.bind("<FocusIn>", self.eliminar_placeholder)
        self.caja_busqueda.bind("<FocusOut>", self.agregar_placeholder)
        self.caja_busqueda.bind("<KeyRelease>", self.buscar_en_tabla)
        self.caja_busqueda.pack(fill = tkinter.X, expand = True)
       
        # TABLA DE DATOS
        # Marco contenedor para la tabla
        self.marco_tabla = tkinter.Frame(self.instancia_princ, bg = "white")
        self.marco_tabla.pack(fill = tkinter.BOTH, expand = True, padx = 4, pady = 4)
 
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
        self.menu_contextual.add_command(label = "Seleccionar código", command = self.seleccionar_codigo)
       
        self.tabla.bind("<Button-3>", self.mostrar_menu_contextual)
       
        # Cierra el menú contextual si se hace clic fuera
        self.instancia_princ.bind("<Button-1>", lambda event: self.menu_contextual.unpost())
        self.instancia_princ.bind("<Button-2>", lambda event: self.menu_contextual.unpost())
        self.instancia_princ.bind("<Button-3>", self.mostrar_menu_contextual)
       
        # ACCIONES
        self.boton_leer.config(command = self.iniciar_lectura_rfid)
        self.boton_escribir.config(command = self.iniciar_escritura_rfid)
        self.boton_agregar.config(command = self.agregar_datos_tabla)
       
        # Carga los datos iniciales desde el archivo
        self.cargar_datos()
 
    # FUNCIONES
    # Elimina el texto del placeholder cuando el usuario hace clic en la caja de búsqueda
    def eliminar_placeholder(self, event):
        if self.caja_busqueda.get() == "Buscar...":
            self.caja_busqueda.delete(0, tkinter.END)
            self.caja_busqueda.config(fg = "black")
   
    # Restaura el placeholder si la caja de búsqueda queda vacía al perder el foco
    def agregar_placeholder(self, event):
        if not self.caja_busqueda.get():
            self.caja_busqueda.insert(0, "Buscar...")
            self.caja_busqueda.config(fg = "gray")
   
    # Filtra en tiempo real los datos actualmente visibles en la tabla, sin leer desde el archivo
    def buscar_en_tabla(self, event):
        filtro = self.caja_busqueda.get().strip().lower()
 
        # Limpiar el placeholder si está presente
        if filtro == "buscar...":
            filtro = ""
 
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
 
        # Filtrar desde la lista interna actualizada
        for nombre, codigo in self.datos_tabla:
            if filtro in nombre.lower() or filtro in codigo.lower():
                self.tabla.insert("", "end", values = (nombre, codigo))
   
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
                        tupla = (nombre.strip(), código.strip())
                       
                        self.tabla.insert("", "end", values=tupla)
                        self.datos_tabla.append(tupla)
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
            valores = self.tabla.item(item)["values"]
           
            if valores in self.datos_tabla:
                self.datos_tabla.remove(tuple(valores))
           
            self.tabla.delete(item)
   
    # Seleccionar código de fila seleccionada
    def seleccionar_codigo(self):
        # Variable para el valor del código
        codigo_celda = ""
       
        # Obtener la fila seleccionada en la tabla
        seleccion = self.tabla.selection()
 
        if seleccion:
            # Obtener el primer ítem seleccionado
            item = seleccion[0]
           
            # Obtener el valor de la columna "Código" de la fila seleccionada
            codigo_celda = self.tabla.item(item)["values"][1]
           
            # Actualizar caja de texto con código seleccionado
            self.caja_texto.delete("1.0", tkinter.END)
            self.caja_texto.insert(tkinter.END, codigo_celda)
           
            # Actualizar caja de código con código seleccionado
            self.caja_código.delete(0, tkinter.END)
            self.caja_código.insert(0, codigo_celda)
   
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
    def agregar_datos_tabla(self):
        # Obtener los valores de los campos de usuario y código
        usuario = self.caja_usuario.get()
        codigo = self.caja_código.get()
       
        # Verificar que ambos campos no sean vacíos
        if not usuario or not codigo:
            self.label_status.config(text = "Error: Debe completar ambos campos")
           
            return
       
        # Verificar que el código no tenga más de 16 carácteres
        if len(codigo) > 16:
            self.label_status.config(text = "Error: No más de 16 carácteres")
           
            return
       
        # Si los datos son válidos, agregar la fila a la tabla
        self.tabla.insert("", "end", values = (usuario, codigo))
       
        # Agrega datos a la lista interna
        self.datos_tabla.append((usuario, codigo))
 
    # Leer datos desde una tarjeta RFID
    def leer_rfid(self):
        self.label_status.config(text = "Aproxime tarjeta...")
       
        while True:
            # Esperar la tarjeta
            (status, tag_type) = self.lector_val.MFRC522_Request(self.lector_val.PICC_REQIDL)
           
            if status == self.lector_val.MI_OK:
                # Leer el UID
                (status, uid) = self.lector_val.MFRC522_Anticoll()
               
                if status == self.lector_val.MI_OK:
                    # Convertir el UID a cadena
                    codigo_rfid = ''.join([str(i) for i in uid])
                   
                    # Mostrar código en etiqueta de estado
                    self.label_status.config(text = f"Código leído: {codigo_rfid}")
                   
                    # Actualizar caja de texto con código RFID
                    self.caja_texto.delete("1.0", tkinter.END)
                    self.caja_texto.insert(tkinter.END, codigo_rfid)
                   
                    # Actualizar caja de código con código RFID
                    self.caja_código.delete(0, tkinter.END)
                    self.caja_código.insert(0, codigo_rfid)
                   
                    break
                else:
                    self.label_status.config(text = "Error de lectura")
           
            time.sleep(0.5)
   
    # Iniciar lectura RFID en un hilo
    def iniciar_lectura_rfid(self):
        # Iniciar el hilo para leer la tarjeta RFID
        threading.Thread(target = self.leer_rfid, daemon = True).start()
 
    # Proceso que realiza la escritura en la tarjeta RFID
    def escribir_rfid(self, codigo_rfid):
        # Esperamos por la tarjeta RFID
        self.label_status.config(text = "Aproxime tarjeta...")
 
        while True:
            # Esperar la tarjeta
            (status, tag_type) = self.lector_val.MFRC522_Request(self.lector_val.PICC_REQIDL)
           
            if status == self.lector_val.MI_OK:
                # Leer el UID
                (status, uid) = self.lector_val.MFRC522_Anticoll()
 
                if status == self.lector_val.MI_OK:
                    # Autenticar el bloque (usamos el bloque 8 como ejemplo - Sector 2, Bloque 0)
                    bloque = 8
                    clave = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # Clave por defecto
                   
                    # Autenticar
                    status = self.lector_val.MFRC522_Auth(self.lector_val.PICC_AUTHENT1A, bloque, clave, uid)
                   
                    if status == self.lector_val.MI_OK:
                        # Convertir el código a bytes y rellenar con espacios si es necesario
                        datos = list(codigo_rfid.ljust(16)[:16].encode('ascii'))
                       
                        # Escribir en el bloque
                        status = self.lector_val.MFRC522_Write(bloque, datos)
                       
                        if status == self.lector_val.MI_OK:
                            # Confirmación de escritura
                            self.label_status.config(text = f"Código escrito: {codigo_rfid}")
                           
                            # Actualizar caja de código con código de caja de texto
                            self.caja_código.delete(0, tkinter.END)
                            self.caja_código.insert(0, codigo_rfid)
                           
                            # Detener la comunicación con la tarjeta
                            self.lector_val.MFRC522_StopCrypto1()
                           
                            break
                        else:
                            self.label_status.config(text = "Error al escribir")
                    else:
                        self.label_status.config(text = "Error de autenticación")
                   
                    break
                else:
                    self.label_status.config(text = "Error de lectura")
           
            time.sleep(0.5)
 
    # Escribir datos a una tarjeta RFID
    def iniciar_escritura_rfid(self):
        # Obtener el código a escribir desde la caja de texto
        codigo_rfid = self.caja_texto.get("1.0", tkinter.END).strip()
       
        # Verificar que el código no tenga más de 16 carácteres
        if len(codigo_rfid) > 16:
            self.label_status.config(text = "Error: No más de 16 carácteres")
           
            return
        elif len(codigo_rfid) == 0:
            self.label_status.config(text = "Error: Ingrese código")
           
            return
       
        # Iniciar el proceso de escritura en un hilo para no bloquear la interfaz
        threading.Thread(target = self.escribir_rfid, args = (codigo_rfid,), daemon = True).start()
 
# Punto de entrada de la aplicación
if __name__ == "__main__":
    vent_princ = vent_princ()
    vent_princ.instancia_princ.mainloop()
