from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Desarrollo de la Interfaz Gráfica
root = Tk()
root.title("APLICACION CRUD CON BASE DE DATOS")
root.configure(background='lightblue')
root.geometry("800x435")

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


# Frame para contener los campos de entrada
entry_frame = Frame(root, bg='lightblue')
entry_frame.place(x=50, y=50)

# Variable para almacenar el nombre de la tabla seleccionada
tabla_seleccionada = StringVar()

# Función para conectar a la base de datos y obtener datos de la tabla seleccionada
def cargar_datos(tabla):
    tabla_seleccionada.set(tabla)
    actualizar_titulo_tabla()
    limpiar_treeview()

    # Conexión a la base de datos
    conn = sqlite3.connect("RecursosHumanos.db") 
    cursor = conn.cursor()

    # Configurar campos de entrada según la tabla seleccionada
    limpiar_campos()
    if tabla == "Colaboradores":
        Label(entry_frame, text="Nombre", background='lightblue').grid(row=0, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miNombre, width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(entry_frame, text="Apellido", background='lightblue').grid(row=0, column=2, padx=5, pady=5)
        Entry(entry_frame, textvariable=miApellido, width=30).grid(row=0, column=3, padx=5, pady=5)

        Label(entry_frame, text="Email", background='lightblue').grid(row=1, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miEmail, width=30).grid(row=1, column=1, padx=5, pady=5)

        Label(entry_frame, text="Teléfono", background='lightblue').grid(row=1, column=2, padx=5, pady=5)
        Entry(entry_frame, textvariable=miTelefono, width=30).grid(row=1, column=3, padx=5, pady=5)

        Label(entry_frame, text="DepartamentoID", background='lightblue').grid(row=2, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miDepartamentoID, width=30).grid(row=2, column=1, padx=5, pady=5)

        cursor.execute("SELECT * FROM Colaborador")
        registros = cursor.fetchall()

        cabecera = ["N", "Nombre", "Apellido", "Email", "Teléfono", "DepartamentoID"]
        tree.config(columns=["0", "1", "2", "3", "4", "5"])
        for i, col in enumerate(cabecera):
            tree.heading(f'#{i}', text=col)

    elif tabla == "Departamento":
        Label(entry_frame, text="DepartamentoID", background='lightblue').grid(row=0, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miDepartamentoID, width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(entry_frame, text="Nombre", background='lightblue').grid(row=1, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miNombre, width=30).grid(row=1, column=1, padx=5, pady=5)

        Label(entry_frame, text="EmpresaID", background='lightblue').grid(row=2, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miEmpresaID, width=30).grid(row=2, column=1, padx=5, pady=5)

        cursor.execute("SELECT * FROM Departamento")
        registros = cursor.fetchall()

        cabecera = ["N", "DepartamentoID", "Nombre", "EmpresaID"]
        tree.config(columns=["0", "1", "2", "3"])
        for i, col in enumerate(cabecera):
            tree.heading(f'#{i}', text=col)

    elif tabla == "Empresa":
        Label(entry_frame, text="EmpresaID", background='lightblue').grid(row=0, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miEmpresaID, width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(entry_frame, text="Nombre", background='lightblue').grid(row=1, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miNombre, width=30).grid(row=1, column=1, padx=5, pady=5)

        Label(entry_frame, text="Dirección", background='lightblue').grid(row=2, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miDireccion, width=30).grid(row=2, column=1, padx=5, pady=5)

        Label(entry_frame, text="Teléfono", background='lightblue').grid(row=3, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miTelefono, width=30).grid(row=3, column=1, padx=5, pady=5)

        Label(entry_frame, text="E-mail", background='lightblue').grid(row=4, column=0, padx=5, pady=5)
        Entry(entry_frame, textvariable=miEmail, width=30).grid(row=4, column=1, padx=5, pady=5)

        cursor.execute("SELECT * FROM Empresa")
        registros = cursor.fetchall()

        cabecera = ["N", "EmpresaID", "Nombre", "Dirección", "Teléfono", "Email"]
        tree.config(columns=["0", "1", "2", "3", "4", "5"])
        for i, col in enumerate(cabecera):
            tree.heading(f'#{i}', text=col)

    # Insertar registros en el Treeview
    for registro in registros:
        tree.insert("", END, values=registro)

    # Cerrar conexión
    cursor.close()
    conn.close()

# Función para crear un nuevo registro
def crear_registro():
    tabla = tabla_seleccionada.get()

    # Conexión a la base de datos
    conn = sqlite3.connect("RecursosHumanos.db")
    cursor = conn.cursor()

    if tabla == "Colaboradores":
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

    elif tabla == "Departamento":
        departamento_id = miDepartamentoID.get().strip()
        nombre = miNombre.get().strip()
        empresa_id = miEmpresaID.get().strip()

        if not departamento_id or not nombre or not empresa_id:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Insertar el nuevo registro en la tabla Departamento
        cursor.execute("INSERT INTO Departamento (DepartamentoID, Nombre, EmpresaID) VALUES (?, ?, ?)",
                       (departamento_id, nombre, empresa_id))

    elif tabla == "Empresa":
        empresa_id = miEmpresaID.get().strip()
        nombre = miNombre.get().strip()
        direccion = miDireccion.get().strip()
        telefono = miTelefono.get().strip()
        email = miEmail.get().strip()

        if not empresa_id or not nombre or not direccion or not telefono or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Insertar el nuevo registro en la tabla Empresa
        cursor.execute("INSERT INTO Empresa (EmpresaID, Nombre, Dirección, Telefono, E-mail) VALUES (?, ?, ?, ?, ?)",
                       (empresa_id, nombre, direccion, telefono, email))

    conn.commit()

    # Limpiar campos después de la creación
    limpiar_campos() 

    # Actualizar datos en el Treeview
    cargar_datos(tabla) 

    # Cerrar conexión
    cursor.close()
    conn.close()

# Función para buscar registros por nombre y apellido
def buscar_registro():
    nombre_buscar = miNombre.get().strip()
    apellido_buscar = miApellido.get().strip()

    tabla = tabla_seleccionada.get() 

    # Conexión a la base de datos
    conn = sqlite3.connect("RecursosHumanos.db")
    cursor = conn.cursor()

    if tabla == "Colaboradores":
        cursor.execute("SELECT * FROM Colaborador WHERE Nombre LIKE ? OR Apellido LIKE ?", (f'%{nombre_buscar}%', f'%{apellido_buscar}%'))
    elif tabla == "Departamento":
        cursor.execute("SELECT * FROM Departamento WHERE Nombre LIKE ?", (f'%{nombre_buscar}%',))
    elif tabla == "Empresa":
        cursor.execute("SELECT * FROM Empresa WHERE Nombre LIKE ?", (f'%{nombre_buscar}%',))

    registros = cursor.fetchall()

    # Limpiar el Treeview antes de mostrar los resultados
    limpiar_treeview()

    # Mostrar los resultados en el Treeview
    for registro in registros:
        tree.insert("", END, values=registro)

    # Cerrar conexión
    cursor.close()
    conn.close()

# Función para eliminar un registro seleccionado
def eliminar_registro():
    try:
        item = tree.selection()[0]
        valores = tree.item(item, "values")

        respuesta = messagebox.askyesno("Eliminar", "¿Estás seguro de que quieres eliminar este registro?")
        if respuesta:
            tabla = tabla_seleccionada.get()

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            if tabla == "Colaboradores":
                cursor.execute("DELETE FROM Colaborador WHERE ColaboradorID=?", (valores[0],))
            elif tabla == "Departamento":
                cursor.execute("DELETE FROM Departamento WHERE DepartamentoID=?", (valores[0],))
            elif tabla == "Empresa":
                cursor.execute("DELETE FROM Empresa WHERE EmpresaID=?", (valores[0],))

            conn.commit()

            # Eliminar el registro del Treeview
            tree.delete(item)

            # Cerrar conexión
            cursor.close()
            conn.close()
    except IndexError:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")

# Función para actualizar un registro seleccionado
def actualizar_registro():
    try:
        tabla = tabla_seleccionada.get()

        if tabla == "Colaboradores":
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

            # Obtener el registro seleccionado en el Treeview
            item = tree.selection()[0]
            valores = tree.item(item, "values")

            # Actualizar el registro en la tabla Colaborador
            cursor.execute(
                "UPDATE Colaborador SET Nombre=?, Apellido=?, Email=?, Telefono=?, DepartamentoID=? WHERE ColaboradorID=?",
                (nombre, apellido, email, telefono, departamento_id, valores[0]))

            conn.commit()

            # Limpiar campos después de la actualización
            limpiar_campos()

            # Actualizar datos en el Treeview
            cargar_datos("Colaboradores")

            # Cerrar conexión
            cursor.close()
            conn.close()

        elif tabla == "Departamento":
            departamento_id = miDepartamentoID.get().strip()
            nombre = miNombre.get().strip()
            empresa_id = miEmpresaID.get().strip()

            # Verificar que todos los campos estén llenos
            if not departamento_id or not nombre or not empresa_id:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Obtener el registro seleccionado en el Treeview
            item = tree.selection()[0]
            valores = tree.item(item, "values")

            # Actualizar el registro en la tabla Departamento
            cursor.execute("UPDATE Departamento SET DepartamentoID=?, Nombre=?, EmpresaID=? WHERE DepartamentoID=?",
                           (departamento_id, nombre, empresa_id, valores[0]))

            conn.commit()

            # Limpiar campos después de la actualización
            limpiar_campos()

            # Actualizar datos en el Treeview
            cargar_datos("Departamento")

            # Cerrar conexión
            cursor.close()
            conn.close()

        elif tabla == "Empresa":
            empresa_id = miEmpresaID.get().strip()
            nombre = miNombre.get().strip()
            direccion = miDireccion.get().strip()
            telefono = miTelefono.get().strip()
            email = miEmail.get().strip()

            # Verificar que todos los campos estén llenos
            if not empresa_id or not nombre or not direccion or not telefono or not email:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Conexión a la base de datos
            conn = sqlite3.connect("RecursosHumanos.db")
            cursor = conn.cursor()

            # Obtener el registro seleccionado en el Treeview
            item = tree.selection()[0]
            valores = tree.item(item, "values")

            # Actualizar el registro en la tabla Empresa
            cursor.execute("UPDATE Empresa SET EmpresaID=?, Nombre=?, Dirección=?, Telefono=?, `E-mail`=? WHERE EmpresaID=?",
                           (empresa_id, nombre, direccion, telefono, email, valores[0]))

            conn.commit()

            # Limpiar campos después de la actualización
            limpiar_campos()

            # Actualizar datos en el Treeview
            cargar_datos("Empresa")

            # Cerrar conexión
            cursor.close()
            conn.close()

    except IndexError:
        messagebox.showerror("Error", "Selecciona un registro para actualizar.")

# Función para limpiar el Treeview
def limpiar_treeview():
    tree.delete(*tree.get_children())

# Función para limpiar los campos de entrada
def limpiar_campos():
    miNombre.set("")
    miApellido.set("")
    miEmail.set("")
    miTelefono.set("")
    miDepartamentoID.set("")
    miEmpresaID.set("")
    miDireccion.set("")

# Función para actualizar el título de la tabla según la tabla seleccionada
def actualizar_titulo_tabla():
    tabla = tabla_seleccionada.get()
    if tabla == "Colaboradores":
        etiqueta_tabla.config(text="Tabla de Colaboradores", background='lightblue')
    elif tabla == "Departamento":
        etiqueta_tabla.config(text="Tabla de Departamento", background='lightblue')
    elif tabla == "Empresa":
        etiqueta_tabla.config(text="Tabla de Empresa", background='lightblue')

# Treeview para mostrar los datos
tree = ttk.Treeview(root, height=10)
tree.place(x=45, y=210)

# Configurar widgets en la vista
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos")
menubasedat.add_command(label="Eliminar Base de Datos")
menubasedat.add_command(label="Salir", command=root.quit)  # Agregar command para salir
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos")
ayudamenu.add_command(label="Acerca")
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

seleccionarbasemenu = Menu(menubar, tearoff=0)
seleccionarbasemenu.add_command(label="Colaboradores", command=lambda: cargar_datos("Colaboradores"))
seleccionarbasemenu.add_command(label="Departamento", command=lambda: cargar_datos("Departamento"))
seleccionarbasemenu.add_command(label="Empresa", command=lambda: cargar_datos("Empresa"))
menubar.add_cascade(label="Elegir tabla", menu=seleccionarbasemenu)

etiqueta_tabla = Label(root, text="Tabla de ", background='lightblue')
etiqueta_tabla.place(x=400, y=10)

Button(root, text="Buscar Registro", image=imagen_buscar, bg="orange", command=buscar_registro).place(x=570, y=50)
Button(root, text="Crear Registro", image=imagen_crear, bg="green", command=crear_registro).place(x=50, y=155)
Button(root, text="Actualizar Registro", image=imagen_actualizar, bg="orange", command=actualizar_registro).place(x=180, y=155)
Button(root, text="Mostrar Lista", image=imagen_mostrar, bg="orange", command=lambda: cargar_datos(tabla_seleccionada.get())).place(x=320, y=155)
Button(root, text="Eliminar Registro", image=imagen_eliminar, bg="red", command=eliminar_registro).place(x=450, y=155)

root.config(menu=menubar)
root.mainloop()
