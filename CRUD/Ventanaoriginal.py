# Importar Bibliotecas
#1
from tkinter import *
from tkinter import ttk,messagebox



################ Desarrollo de la Interfaz Grafica #############################
################################################################################
root=Tk()
root.title("APLICACION CRUD CON BASE DE DATOS")
root.configure(background='lightblue')
root.geometry("600x435")

#iconos
# Cargar imágenes
imagen_buscar = PhotoImage(file="imagenes/buscar.png")
imagen_crear = PhotoImage(file="imagenes/crear.png")
imagen_mostrar = PhotoImage(file="imagenes/mostrar.png")
imagen_actualizar = PhotoImage(file="imagenes/actualizar.png")
imagen_eliminar = PhotoImage(file="imagenes/eliminar.png")

miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miSalario=StringVar()
miFechaContratacion=StringVar()
miEmpresa=StringVar()

################################## Tabla ################################
cabecera=["Nombre", "Apellido", "Salario", "Fecha Contratacion", "Empresa"]

tree=ttk.Treeview(height=10, columns=('#0','#1','#2','#3','#4'))
tree.place(x=0, y=210)
tree.column('#0', width=132)
tree.heading('#0', text=cabecera[0], anchor=CENTER)
tree.column('#1', width=132)
tree.heading('#1', text=cabecera[1], anchor=CENTER)
tree.column('#2', width=80)
tree.heading('#2', text=cabecera[2], anchor=CENTER)
tree.column('#3', width=130)
tree.heading('#3', text=cabecera[3], anchor=CENTER)
tree.column('#4', width=126)
tree.heading('#4', text=cabecera[4], anchor=CENTER)


tree.bind("<Button-1>",)


###################### Colocar widgets en la VISTA ######################
menubar=Menu(root)
menubasedat=Menu(menubar,tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos",)
menubasedat.add_command(label="Eliminar Base de Datos",)
menubasedat.add_command(label="Salir",)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="Resetear Campos", )
ayudamenu.add_command(label="Acerca",)
menubar.add_cascade(label="Ayuda",menu=ayudamenu)

seleccionarbasemenu=Menu(menubar, tearoff=0)
seleccionarbasemenu.add_command(label="Colaboradores")
seleccionarbasemenu.add_command(label="Departamento")
seleccionarbasemenu.add_command(label="Empresa")
menubar.add_cascade(label="Elegir tabla", menu=seleccionarbasemenu)
############## Creando etiquetas y cajas de texto ###########################

l1=Label(root, text="COLABORADORES", background='lightblue').place(x=250,y=10)

e1=Entry(root, textvariable=miId)

l2=Label(root, text="Nombre", background='lightblue').place(x=50,y=50)
e2=Entry(root, textvariable=miNombre, width=19).place(x=100, y=50)

l3=Label(root, text="Apellido", background='lightblue').place(x=240,y=50)
e3=Entry(root, textvariable=miApellido, width=19).place(x=290, y=50)

l4=Label(root, text="Salario", background='lightblue').place(x=50,y=80)
e4=Entry(root, textvariable=miSalario, width=10).place(x=100, y=80)

l5=Label(root, text="USD", background='lightblue').place(x=150,y=80)

l6=Label(root, text="Fecha contratacion", background='lightblue').place(x=190,y=80)
e6=Entry(root, textvariable=miFechaContratacion, width=17).place(x=300, y=80)

l7=Label(root, text="Empresa", background='lightblue').place(x=50,y=110)
e7=Entry(root, textvariable=miEmpresa, width=50).place(x=100, y=110)



################# Creando botones #########################################
b0=Button(root, text="Buscar Registro", image=imagen_buscar, bg="orange",).place(x=450, y=50)
b1=Button(root, text="Crear Registro",  image=imagen_crear, bg="green",).place(x=50, y=155)
b2=Button(root, text="Actualizar Registro", image=imagen_actualizar, bg="orange",).place(x=180, y=155)
b3=Button(root, text="Mostrar Lista", image=imagen_mostrar,bg="orange",).place(x=320, y=155)
b4=Button(root, text="Eliminar Registro", image=imagen_eliminar, bg="red").place(x=450, y=155)

root.config(menu=menubar)
root.mainloop()