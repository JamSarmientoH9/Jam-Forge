from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Desarrollo de la Interfaz Gráfica
root = Tk()
root.title("APLICACION CRUD CON BASE DE DATOS")
root.configure(background='lightblue')
root.geometry("1000x600")

# Cargar imágenes (asegúrate de tener las imágenes en la carpeta "imagenes" dentro del directorio actual)
imagen_buscar = PhotoImage(file="imagenes/buscar.png")
imagen_crear = PhotoImage(file="imagenes/crear.png")
imagen_mostrar = PhotoImage(file="imagenes/mostrar.png")
imagen_actualizar = PhotoImage(file="imagenes/actualizar.png")
imagen_eliminar = PhotoImage(file="imagenes/eliminar.png")

# Variables de control para los Entry
miNombre = StringVar()
miApellido = StringVar()
miEmail = StringVar()
miTelefono = StringVar()
miDepartamentoID = StringVar()
miEmpresaID = StringVar()
miDireccion = StringVar()

# Variable para almacenar el nombre de la tabla seleccionada
tabla_seleccionada = StringVar()

# Diccionario para almacenar los widgets
widgets = {}

# Crear Treeviews
tree_colaboradores = ttk.Treeview(root, columns=("ColaboradorID", "Nombre", "Apellido", "Email", "Telefono", "DepartamentoID"), show='headings')
tree_colaboradores.heading("ColaboradorID", text="ColaboradorID")
tree_colaboradores.heading("Nombre", text="Nombre")
tree_colaboradores.heading("Apellido", text="Apellido")
tree_colaboradores.heading("Email", text="Email")
tree_colaboradores.heading("Telefono", text="Telefono")
tree_colaboradores.heading("DepartamentoID", text="DepartamentoID")

tree_empresas = ttk.Treeview(root, columns=("EmpresaID", "Nombre", "Direccion", "Telefono", "Email"), show='headings')
tree_empresas.heading("EmpresaID", text="EmpresaID")
tree_empresas.heading("Nombre", text="Nombre")
tree_empresas.heading("Direccion", text="Direccion")
tree_empresas.heading("Telefono", text="Telefono")
tree_empresas.heading("Email", text="Email")

tree_departamentos = ttk.Treeview(root, columns=("DepartamentoID", "Nombre", "EmpresaID"), show='headings')
tree_departamentos.heading("DepartamentoID", text="DepartamentoID")
tree_departamentos.heading("Nombre", text="Nombre")
tree_departamentos.heading("EmpresaID", text="EmpresaID")

# Función para conectar a la base de datos y obtener datos de la tabla seleccionada
def cargar_datos(tabla):
    tabla_seleccionada.set(tabla)
    actualizar_titulo_tabla()
    limpiar_treeview()
    # Conexión a la base de datos
    conn = sqlite3.connect("RecursosHumanos.db")
    cursor = conn.cursor()

    # Ocultar todos los widgets
    ocultar_widgets()

    # Ocultar todos los treeviews
    tree_colaboradores.place_forget()
    tree_departamentos.place_forget()
    tree_empresas.place_forget()
    
    # Coordenadas base para centrar los widgets
    base_x_left = 150
    base_x_right = 500
    base_y = 70

    y_increment = 40
    
    # Configurar campos de entrada según la tabla seleccionada
    if tabla == "colaborador":
        widgets['nombre_label'].place(x=base_x_left, y=base_y)
        widgets['nombre_entry'].place(x=base_x_left + 100, y=base_y)
        
        widgets['telefono_label'].place(x=base_x_right, y=base_y)
        widgets['telefono_entry'].place(x=base_x_right + 150, y=base_y)
        
        widgets['apellido_label'].place(x=base_x_left, y=base_y + y_increment)
        widgets['apellido_entry'].place(x=base_x_left + 100, y=base_y + y_increment)
        
        widgets['departamento_id_label'].place(x=base_x_right, y=base_y + y_increment)
        widgets['departamento_id_entry'].place(x=base_x_right + 150, y=base_y + y_increment)
        
        widgets['email_label'].place(x=base_x_left, y=base_y + 2 * y_increment)
        widgets['email_entry'].place(x=base_x_left + 100, y=base_y + 2 * y_increment)
        
        # Función para crear un nuevo registro
        def crear_registro_colaborador():
            tabla = tabla_seleccionada.get()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            if tabla == "colaborador":
                nombre = miNombre.get().strip()
                apellido = miApellido.get().strip()
                email = miEmail.get().strip()
                telefono = miTelefono.get().strip()
                departamento_id = miDepartamentoID.get().strip()

                if not nombre or not apellido or not email or not telefono or not departamento_id:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return 

                # Insertar el nuevo registro en la tabla Colaborador
                cursor.execute("INSERT INTO Colaborador (Nombre, Apellido, Email, Telefono, DepartamentoID) VALUES (?, ?, ?, ?, ?)",
                            (nombre, apellido, email, telefono, departamento_id))

                conn.commit()

                # Insertar el nuevo registro en el Treeview
                cursor.execute("SELECT * FROM Colaborador WHERE rowid = last_insert_rowid()")
                new_row = cursor.fetchone()
                tree_colaboradores.insert("", END, values=new_row)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para actualizar un registro seleccionado
        def actualizar_registro_colaborador():
            try:
                item = tree_colaboradores.selection()[0]
                valores = tree_colaboradores.item(item, "values")

                nombre = miNombre.get().strip()
                apellido = miApellido.get().strip()
                email = miEmail.get().strip()
                telefono = miTelefono.get().strip()
                departamento_id = miDepartamentoID.get().strip()

                # Verificar que todos los campos estén llenos
                if not nombre or not apellido or not email or not telefono or not departamento_id:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                # Conexión a la base de datos
                conn = sqlite3.connect("RecursosHumanos.db")
                cursor = conn.cursor()

                # Actualizar el registro en la tabla Colaborador
                cursor.execute(
                    "UPDATE Colaborador SET Nombre=?, Apellido=?, Email=?, Telefono=?, DepartamentoID=? WHERE ColaboradorID=?",
                    (nombre, apellido, email, telefono, departamento_id, valores[0]))

                conn.commit()

                # Actualizar datos en el Treeview
                cargar_datos("colaborador")

                # Cerrar conexión
                cursor.close()
                conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para actualizar.")

        # Función para mostrar la lista completa de Colaboradores
        def mostrar_lista_colaboradores():
            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Ejecutar la consulta SQL y llenar el Treeview con los resultados
            cursor.execute("SELECT * FROM Colaborador")
            registros = cursor.fetchall()
            
            for registro in registros:
                tree_colaboradores.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para eliminar un registro seleccionado
        def eliminar_registro_colaborador():
            try:
                item = tree_colaboradores.selection()[0]
                valores = tree_colaboradores.item(item, "values")

                respuesta = messagebox.askyesno("Eliminar", "¿Estás seguro de que quieres eliminar este registro?")
                if respuesta:
                    # Conexión a la base de datos
                    conn = sqlite3.connect("RecursosHumanos.db")
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Colaborador WHERE ColaboradorID=?", (valores[0],))

                    conn.commit()

                    # Eliminar el registro del Treeview
                    tree_colaboradores.delete(item)

                    # Cerrar conexión
                    cursor.close()
                    conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para eliminar.")

        # Función para buscar colaboradores por nombre y apellido
        def buscar_colaboradores():
            nombre = widgets['nombre_entry'].get().strip()
            apellido = widgets['apellido_entry'].get().strip()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Consulta SQL para buscar colaboradores por nombre y apellido
            cursor.execute("SELECT * FROM Colaborador WHERE Nombre LIKE ? AND Apellido LIKE ?", ('%' + nombre + '%', '%' + apellido + '%'))
            registros = cursor.fetchall()

            for registro in registros:
                tree_colaboradores.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()

        tree_colaboradores.place(x=50, y=250)
        Button(root, text="Buscar Colaborador", image=imagen_buscar, bg="orange", command=buscar_colaboradores).place(x=900, y=200)
        Button(root, text="Crear Registro", image=imagen_crear, bg="green", command=crear_registro_colaborador).place(x=500, y=200)
        Button(root, text="Actualizar Registro", image=imagen_actualizar, bg="orange", command=actualizar_registro_colaborador).place(x=600, y=200)
        Button(root, text="Mostrar Lista", image=imagen_mostrar, bg="orange", command=mostrar_lista_colaboradores).place(x=700, y=200)
        Button(root, text="Eliminar Registro", image=imagen_eliminar, bg="red", command=eliminar_registro_colaborador).place(x=800, y=200)

    elif tabla == "empresa":
        widgets['nombre_label'].place(x=400, y=base_y)
        widgets['nombre_entry'].place(x=500, y=base_y)
        widgets['direccion_label'].place(x=400, y=base_y + y_increment)
        widgets['direccion_entry'].place(x=500, y=base_y + y_increment)
        widgets['telefono_label'].place(x=760, y=base_y)
        widgets['telefono_entry'].place(x=700 + 150, y=base_y)
        widgets['email_label'].place(x=760, y=base_y + y_increment)
        widgets['email_entry'].place(x=850, y=base_y + y_increment)

        # Función para crear un nuevo registro
        def crear_registro_empresa():
            tabla = tabla_seleccionada.get()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            if tabla == "empresa":
                nombre = miNombre.get().strip()
                direccion = miDireccion.get().strip()
                telefono = miTelefono.get().strip()
                email = miEmail.get().strip()

                if not nombre or not direccion or not telefono or not email:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return 

                # Insertar el nuevo registro en la tabla Empresa
                cursor.execute("INSERT INTO Empresa (Nombre, Direccion, Telefono, Email) VALUES (?, ?, ?, ?)",
                            (nombre, direccion, telefono, email))

                conn.commit()

                # Insertar el nuevo registro en el Treeview
                cursor.execute("SELECT * FROM Empresa WHERE rowid = last_insert_rowid()")
                new_row = cursor.fetchone()
                tree_empresas.insert("", END, values=new_row)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para actualizar un registro seleccionado
        def actualizar_registro_empresa():
            try:
                item = tree_empresas.selection()[0]
                valores = tree_empresas.item(item, "values")

                nombre = miNombre.get().strip()
                direccion = miDireccion.get().strip()
                telefono = miTelefono.get().strip()
                email = miEmail.get().strip()

                # Verificar que todos los campos estén llenos
                if not nombre or not direccion or not telefono or not email:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                # Conexión a la base de datos
                conn = sqlite3.connect("RecursosHumanos.db")
                cursor = conn.cursor()

                # Actualizar el registro en la tabla Empresa
                cursor.execute(
                    "UPDATE Empresa SET Nombre=?, Direccion=?, Telefono=?, Email=? WHERE EmpresaID=?",
                    (nombre, direccion, telefono, email, valores[0]))

                conn.commit()

                # Actualizar datos en el Treeview
                cargar_datos("empresa")

                # Cerrar conexión
                cursor.close()
                conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para actualizar.")

        # Función para mostrar la lista completa de Empresas
        def mostrar_lista_empresas():
            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Ejecutar la consulta SQL y llenar el Treeview con los resultados
            cursor.execute("SELECT * FROM Empresa")
            registros = cursor.fetchall()
            
            for registro in registros:
                tree_empresas.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para eliminar un registro seleccionado
        def eliminar_registro_empresa():
            try:
                item = tree_empresas.selection()[0]
                valores = tree_empresas.item(item, "values")

                respuesta = messagebox.askyesno("Eliminar", "¿Estás seguro de que quieres eliminar este registro?")
                if respuesta:
                    # Conexión a la base de datos
                    conn = sqlite3.connect("RecursosHumanos.db")
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Empresa WHERE EmpresaID=?", (valores[0],))

                    conn.commit()

                    # Eliminar el registro del Treeview
                    tree_empresas.delete(item)

                    # Cerrar conexión
                    cursor.close()
                    conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para eliminar.")

        # Función para buscar empresas por nombre, dirección y teléfono
        def buscar_empresas():
            nombre = widgets['nombre_entry'].get().strip()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Consulta SQL para buscar empresas por nombre
            cursor.execute("SELECT * FROM Empresa WHERE Nombre LIKE ?",
                        ('%' + nombre + '%',))
            registros = cursor.fetchall()

            for registro in registros:
                tree_empresas.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()

        tree_empresas.place(x=50, y=250)
        Button(root, text="Buscar Registro", image=imagen_buscar, bg="orange", command=buscar_empresas).place(x=900, y=200)
        Button(root, text="Crear Registro", image=imagen_crear, bg="green", command=crear_registro_empresa).place(x=500, y=200)
        Button(root, text="Actualizar Registro", image=imagen_actualizar, bg="orange", command=actualizar_registro_empresa).place(x=600, y=200)
        Button(root, text="Mostrar Lista", image=imagen_mostrar, bg="orange", command=mostrar_lista_empresas).place(x=700, y=200)
        Button(root, text="Eliminar Registro", image=imagen_eliminar, bg="red", command=eliminar_registro_empresa).place(x=800, y=200)

    elif tabla == "departamento":
        widgets['nombre_label'].place(x=400, y=base_y)
        widgets['nombre_entry'].place(x=500, y=base_y)
        widgets['empresa_id_label'].place(x=400, y=base_y + y_increment)
        widgets['empresa_id_entry'].place(x=500, y=base_y + y_increment)

        # Función para crear un nuevo registro
        def crear_registro_departamento():
            tabla = tabla_seleccionada.get()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            if tabla == "departamento":
                nombre = miNombre.get().strip()
                empresa_id = miEmpresaID.get().strip()

                if not nombre or not empresa_id:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return 

                # Insertar el nuevo registro en la tabla Departamento
                cursor.execute("INSERT INTO Departamento (Nombre, EmpresaID) VALUES (?, ?)",
                            (nombre, empresa_id))

                conn.commit()

                # Insertar el nuevo registro en el Treeview
                cursor.execute("SELECT * FROM Departamento WHERE rowid = last_insert_rowid()")
                new_row = cursor.fetchone()
                tree_departamentos.insert("", END, values=new_row)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para actualizar un registro seleccionado
        def actualizar_registro_departamento():
            try:
                item = tree_departamentos.selection()[0]
                valores = tree_departamentos.item(item, "values")

                nombre = miNombre.get().strip()
                empresa_id = miEmpresaID.get().strip()

                # Verificar que todos los campos estén llenos
                if not nombre or not empresa_id:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                # Conexión a la base de datos
                conn = sqlite3.connect("RecursosHumanos.db")
                cursor = conn.cursor()

                # Actualizar el registro en la tabla Departamento
                cursor.execute(
                    "UPDATE Departamento SET Nombre=?, EmpresaID=? WHERE DepartamentoID=?",
                    (nombre, empresa_id, valores[0]))

                conn.commit()

                # Actualizar datos en el Treeview
                cargar_datos("departamento")

                # Cerrar conexión
                cursor.close()
                conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para actualizar.")

        # Función para mostrar la lista completa de Departamentos
        def mostrar_lista_departamentos():
            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Ejecutar la consulta SQL y llenar el Treeview con los resultados
            cursor.execute("SELECT * FROM Departamento")
            registros = cursor.fetchall()
            
            for registro in registros:
                tree_departamentos.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()

        # Función para eliminar un registro seleccionado
        def eliminar_registro_departamento():
            try:
                item = tree_departamentos.selection()[0]
                valores = tree_departamentos.item(item, "values")

                respuesta = messagebox.askyesno("Eliminar", "¿Estás seguro de que quieres eliminar este registro?")
                if respuesta:
                    # Conexión a la base de datos
                    conn = sqlite3.connect("RecursosHumanos.db")
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Departamento WHERE DepartamentoID=?", (valores[0],))

                    conn.commit()

                    # Eliminar el registro del Treeview
                    tree_departamentos.delete(item)

                    # Cerrar conexión
                    cursor.close()
                    conn.close()
            except IndexError:
                messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        # Función para buscar departamentos por nombre
        def buscar_departamentos():
            nombre = widgets['nombre_entry'].get().strip()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Limpiar el Treeview antes de cargar nuevos datos
            limpiar_treeview()

            # Consulta SQL para buscar departamentos por nombre
            cursor.execute("SELECT * FROM Departamento WHERE Nombre LIKE ?",
                        ('%' + nombre + '%',))
            registros = cursor.fetchall()

            for registro in registros:
                tree_departamentos.insert("", END, values=registro)

            # Cerrar conexión
            cursor.close()
            conn.close()
            
        tree_departamentos.place(x=50, y=250)
        Button(root, text="Buscar Registro", image=imagen_buscar, bg="orange", command=buscar_departamentos).place(x=900, y=200)
        Button(root, text="Crear Registro", image=imagen_crear, bg="green", command=crear_registro_departamento).place(x=500, y=200)
        Button(root, text="Actualizar Registro", image=imagen_actualizar, bg="orange", command=actualizar_registro_departamento).place(x=600, y=200)
        Button(root, text="Mostrar Lista", image=imagen_mostrar, bg="orange", command=mostrar_lista_departamentos).place(x=700, y=200)
        Button(root, text="Eliminar Registro", image=imagen_eliminar, bg="red", command=eliminar_registro_departamento).place(x=800, y=200)

    # Ejecutar la consulta SQL y llenar el Treeview con los resultados
    cursor.execute(f"SELECT * FROM {tabla}")
    registros = cursor.fetchall()
    for registro in registros:
        if tabla == "colaborador":
            tree_colaboradores.insert("", END, values=registro)
        elif tabla == "empresa":
            tree_empresas.insert("", END, values=registro)
        elif tabla == "departamento":
            tree_departamentos.insert("", END, values=registro)

    # Cerrar conexión
    cursor.close()
    conn.close()

# Función para cargar los datos seleccionados en los campos de entrada
def cargar_datos_seleccionados(event):
    try:
        tabla = tabla_seleccionada.get()
        if tabla == "colaborador":
            item = tree_colaboradores.selection()[0]
            valores = tree_colaboradores.item(item, "values")
            miNombre.set(valores[1])
            miApellido.set(valores[2])
            miEmail.set(valores[3])
            miTelefono.set(valores[4])
            miDepartamentoID.set(valores[5])
        elif tabla == "empresa":
            item = tree_empresas.selection()[0]
            valores = tree_empresas.item(item, "values")
            miNombre.set(valores[1])
            miDireccion.set(valores[2])
            miTelefono.set(valores[3])
            miEmail.set(valores[4])
        elif tabla == "departamento":
            item = tree_departamentos.selection()[0]
            valores = tree_departamentos.item(item, "values")
            miNombre.set(valores[1])
            miEmpresaID.set(valores[2])
    except IndexError:
        pass

# Vincular la función de cargar datos a los eventos de selección de los Treeviews
tree_colaboradores.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)
tree_empresas.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)
tree_departamentos.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)

# Función para limpiar el Treeview
def limpiar_treeview():
    for tree in [tree_colaboradores, tree_empresas, tree_departamentos]:
        for item in tree.get_children():
            tree.delete(item)

# Función para ocultar todos los widgets
def ocultar_widgets():
    for widget in widgets.values():
        widget.place_forget()

# Función para actualizar el título de la tabla
def actualizar_titulo_tabla():
    tabla = tabla_seleccionada.get()
    root.title(f"APLICACION CRUD CON BASE DE DATOS - {tabla.upper()}")

# Crear Treeviews
tree_colaboradores = ttk.Treeview(root, columns=("colaboradorID", "Nombre", "Apellido", "Email", "Telefono", "DepartamentoID"), show='headings')
for col in tree_colaboradores["columns"]:
    tree_colaboradores.heading(col, text=col)

tree_empresas = ttk.Treeview(root, columns=("empresaID", "Nombre", "Direccion", "Telefono", "Email"), show='headings')
for col in tree_empresas["columns"]:
    tree_empresas.heading(col, text=col)

tree_departamentos = ttk.Treeview(root, columns=("departamentoID", "Nombre", "EmpresaID"), show='headings')
for col in tree_departamentos["columns"]:
    tree_departamentos.heading(col, text=col)

# Crear etiquetas y campos de entrada (Entries) para cada columna
widgets['nombre_label'] = Label(root, text="Nombre")
widgets['nombre_entry'] = Entry(root, textvariable=miNombre)

widgets['apellido_label'] = Label(root, text="Apellido")
widgets['apellido_entry'] = Entry(root, textvariable=miApellido)

widgets['email_label'] = Label(root, text="Email")
widgets['email_entry'] = Entry(root, textvariable=miEmail)

widgets['telefono_label'] = Label(root, text="Teléfono")
widgets['telefono_entry'] = Entry(root, textvariable=miTelefono)

widgets['departamento_id_label'] = Label(root, text="Departamento ID")
widgets['departamento_id_entry'] = Entry(root, textvariable=miDepartamentoID)

widgets['empresa_id_label'] = Label(root, text="Empresa ID")
widgets['empresa_id_entry'] = Entry(root, textvariable=miEmpresaID)

widgets['direccion_label'] = Label(root, text="Dirección")
widgets['direccion_entry'] = Entry(root, textvariable=miDireccion)

# Creación del menú
menubar = Menu(root)
root.config(menu=menubar)

# Crear el menú de selección de tablas
menu_seleccionar_tabla = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Seleccionar Tabla", menu=menu_seleccionar_tabla)
menu_seleccionar_tabla.add_command(label="Colaboradores", command=lambda: cargar_datos("colaborador"))
menu_seleccionar_tabla.add_command(label="Departamentos", command=lambda: cargar_datos("departamento"))
menu_seleccionar_tabla.add_command(label="Empresas", command=lambda: cargar_datos("empresa"))

root.mainloop()  