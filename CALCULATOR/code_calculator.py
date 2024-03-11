# Importar las clases Button, Tk, Frame, Entry y END del módulo tkinter
from tkinter import Button, Tk, Frame, Entry, END

# Crear una instancia de la clase Tk para la ventana principal
ventana = Tk()

# Configurar las dimensiones de la ventana principal
ventana.geometry('274x328')

# Configurar el color de fondo de la ventana principal
ventana.config(bg="white")

# Configurar el icono de la ventana principal
ventana.iconbitmap(bitmap='icono.ico')

# Desactivar la capacidad de redimensionar la ventana principal
ventana.resizable(0, 0)

# Establecer el título de la ventana principal
ventana.title('Calculadora')

# Definir una subclase de Button llamada HoverButton con funcionalidad adicional
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Método que se activa cuando el cursor entra en el botón
    def on_enter(self, e):
        self["background"] = self.defaultBackground

    # Método que se activa cuando el cursor sale del botón
    def on_leave(self, e):
        self["background"] = self.defaultBackground

# Inicializar la variable global i con el valor -1
i = -1

def obtener(dato):
    global i  # Accede a la variable global 'i'
    i += 1  # Incrementa 'i' en 1
    Resultado.insert(i, dato)  # Inserta el dato en la posición 'i' del Entry Resultado
def operacion():
    global i  # Accede a la variable global 'i'
    ecuacion = Resultado.get()  # Obtiene la expresión matemática del Entry Resultado
    if i != 0:  # Si la posición del cursor no es 0
        try:
            result = str(eval(ecuacion))  # Evalúa la expresión y la convierte a string
            Resultado.delete(0, END)  # Borra todo el contenido del Entry Resultado
            Resultado.insert(0, result)  # Inserta el resultado en el Entry Resultado
            longitud = len(result)  # Obtiene la longitud del resultado
            i = longitud  # Actualiza la posición del cursor
        except:
            result = 'ERROR'  # En caso de error, establece el resultado como 'ERROR'
            Resultado.delete(0, END)  # Borra todo el contenido del Entry Resultado
            Resultado.insert(0, result)  # Inserta 'ERROR' en el Entry Resultado
    else:
        pass  # No hace nada si la posición del cursor es 0
def borrar_uno():
    global i  # Accede a la variable global 'i'
    if i == -1:  # Si la posición del cursor es -1
        pass  # No hace nada
    else:
        Resultado.delete(i, last=None)  # Borra el carácter en la posición 'i' del Entry Resultado
        i -= 1  # Decrementa la posición del cursor
def borrar_todo():
    Resultado.delete(0, END)  # Borra todo el contenido del Entry Resultado
    # i=0  # Podría ser una opción restablecer la posición del cursor a 0 aquí, pero está comentado

# Crear un marco dentro de la ventana principal con fondo negro y relieve levantado
frame = Frame(ventana, bg='black', relief="raised")
# Colocar el marco en la posición (column=0, row=0) con un relleno de 6 píxeles horizontalmente y 3 píxeles verticalmente
frame.grid(column=0, row=0, padx=6, pady=3)

# Crear un Entry dentro del marco para mostrar el resultado de la calculadora
Resultado = Entry(frame, bg='#9EF8E8', width=18, relief='groove', font='Montserrat 16', justify='right')
# Colocar el Entry en la fila 0 del marco, abarcando 4 columnas, con un relleno de 3 píxeles verticalmente y 1 píxel horizontalmente,
# y aumentar el tamaño del padding interno en 1 píxel verticalmente y horizontalmente
Resultado.grid(columnspan=4, row=0, pady=3, padx=1, ipadx=1, ipady=1)

# Crear un botón personalizado HoverButton en el marco con el texto "1" y otras propiedades específicas
Button1 = HoverButton(frame, text="1", borderwidth=2, height=2, width=5,
                      font=('Comic sens MC', 12, 'bold'), relief="raised", activebackground="aqua", bg='#999AB8',
                      anchor="center", command=lambda: obtener(1))
# Colocar el botón en la fila 1 y columna 0 del marco, con un relleno de 1 píxel verticalmente y 3 píxeles horizontalmente
Button1.grid(column=0, row=1, pady=1, padx=3)

# Crear un botón personalizado HoverButton en el marco con el texto "2" y otras propiedades específicas
Button2 = HoverButton(frame, text="2", height=2, width=5,
                      font=('Comic sens MC', 12, 'bold'), borderwidth=2, relief="raised", activebackground="aqua",
                      bg='#999AB8',
                      anchor="center", command=lambda: obtener(2))
# Colocar el botón en la fila 1 y columna 1 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button2.grid(column=1, row=1, pady=1, padx=1)

# Crear un botón personalizado HoverButton en el marco con el texto "3" y otras propiedades específicas
Button3 = HoverButton(frame, text="3", height=2, width=5,
                      font=('Comic sens MC', 12, 'bold'), borderwidth=2, relief="raised", activebackground="aqua",
                      bg='#999AB8',
                      anchor="center", command=lambda: obtener(3))
# Colocar el botón en la fila 1 y columna 2 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
# Colocar el Button3 en la columna 2 y fila 1 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button3.grid(column=2, row=1, pady=1, padx=1)

# Crear un HoverButton para borrar un único carácter del resultado
Button_borrar = HoverButton(frame, text="⌫", height=2, width=5,
                            font=('Comic sens MC', 12, 'bold'), borderwidth=2, relief="raised", activebackground="red",
                            bg='#FD0371', anchor="center", command=lambda: borrar_uno())
# Colocar el botón de borrar en la columna 3 y fila 1 del marco, con un relleno de 2 píxeles verticalmente y 2 píxeles horizontalmente
Button_borrar.grid(column=3, row=1, pady=2, padx=2)

# Crear un HoverButton para el número 4 con propiedades específicas
Button4 = HoverButton(frame, text="4", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(4))
# Colocar el botón de 4 en la columna 0 y fila 2 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button4.grid(column=0, row=2, pady=1, padx=1)

# Crear un HoverButton para el número 5 con propiedades específicas
Button5 = HoverButton(frame, text="5", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(5))
# Colocar el botón de 5 en la columna 1 y fila 2 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button5.grid(column=1, row=2, pady=1, padx=1)

# Crear un HoverButton para el número 6 con propiedades específicas
Button6 = HoverButton(frame, text="6", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(6))
# Colocar el botón de 6 en la columna 2 y fila 2 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button6.grid(column=2, row=2, pady=1, padx=1)

# Crear un HoverButton para el operador de suma con propiedades específicas
Button_mas = HoverButton(frame, text="+", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                         borderwidth=2, relief="raised", activebackground="#FEEF02", bg='#2A16F7', anchor="center",
                         command=lambda: obtener('+'))
# Colocar el botón de suma en la columna 3 y fila 2 del marco, con un relleno de 2 píxeles verticalmente y 2 píxeles horizontalmente
Button_mas.grid(column=3, row=2, pady=2, padx=2)

# Crear un HoverButton para el número 7 con propiedades específicas
Button7 = HoverButton(frame, text="7", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(7))
# Colocar el botón de 7 en la columna 0 y fila 3 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button7.grid(column=0, row=3, pady=1, padx=1)

# Crear un HoverButton para el número 8 con propiedades específicas
Button8 = HoverButton(frame, text="8", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(8))

# Colocar el Button8 en la columna 1 y fila 3 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button8.grid(column=1, row=3, pady=1, padx=1)

# Crear un HoverButton para el número 9 con propiedades específicas
Button9 = HoverButton(frame, text="9", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(9))
# Colocar el botón de 9 en la columna 2 y fila 3 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button9.grid(column=2, row=3, pady=1, padx=1)

# Crear un HoverButton para el operador de resta con propiedades específicas
Button_menos = HoverButton(frame, text="-", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="#FEEF02", bg='#2A16F7', anchor="center",
                            command=lambda: obtener('-'))
# Colocar el botón de resta en la columna 3 y fila 3 del marco, con un relleno de 2 píxeles verticalmente y 2 píxeles horizontalmente
Button_menos.grid(column=3, row=3, pady=2, padx=2)

# Crear un HoverButton para el número 0 con propiedades específicas
Button0 = HoverButton(frame, text="0", height=5, width=5, font=('Comic sens MC', 12, 'bold'),
                      borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                      command=lambda: obtener(0))
# Colocar el botón de 0 en la columna 0, ocupando 2 filas y en la fila 4 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button0.grid(column=0, rowspan=2, row=4, pady=1, padx=1)

# Crear un HoverButton para el punto decimal con propiedades específicas
Button_punto = HoverButton(frame, text=".", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="aqua", bg='#999AB8', anchor="center",
                            command=lambda: obtener('.'))
# Colocar el botón de punto en la columna 1 y fila 4 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button_punto.grid(column=1, row=4, pady=1, padx=1)

# Crear un HoverButton para el operador de división con propiedades específicas
Button_entre = HoverButton(frame, text="÷", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="#FEEF02", bg='#2A16F7', anchor="center",
                            command=lambda: obtener('/'))
# Colocar el botón de división en la columna 2 y fila 4 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button_entre.grid(column=2, row=4, pady=1, padx=1)

# Crear un HoverButton para el operador de multiplicación con propiedades específicas
Button_por = HoverButton(frame, text="x", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="#FEEF02", bg='#2A16F7', anchor="center",
                            command=lambda: obtener('*'))
# Colocar el botón de multiplicación en la columna 3 y fila 4 del marco, con un relleno de 2 píxeles verticalmente y 2 píxeles horizontalmente
Button_por.grid(column=3, row=4, pady=2, padx=2)

# Crear un HoverButton para el operador de igual con propiedades específicas
Button_igual = HoverButton(frame, text="=", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="#16FD03", bg='#2FEC71', anchor="center",
                            command=lambda: operacion())
# Colocar el botón de igual en la columna 1 y fila 5 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button_igual.grid(column=1, row=5, pady=1, padx=1)

# Crear un HoverButton para el operador de raíz cuadrada con propiedades específicas
Button_raiz = HoverButton(frame, text="√", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="#FEEF02", bg='#2A16F7', anchor="center",
                            command=lambda: obtener('**(1/2)'))
# Colocar el botón de raíz cuadrada en la columna 2 y fila 5 del marco, con un relleno de 1 píxel verticalmente y 1 píxel horizontalmente
Button_raiz.grid(column=2, row=5, pady=1, padx=1)

# Crear un HoverButton para el botón de borrar todo con propiedades específicas
Button_borrar = HoverButton(frame, text="C", height=2, width=5, font=('Comic sens MC', 12, 'bold'),
                            borderwidth=2, relief="raised", activebackground="red", bg='#FD5603', anchor="center",
                            command=lambda: borrar_todo())
# Colocar el botón de borrar todo en la columna 3 y fila 5 del marco, con un relleno de 2 píxeles verticalmente y 2 píxeles horizontalmente
Button_borrar.grid(column=3, row=5, pady=2, padx=2)

# Iniciar el bucle principal de la aplicación de la GUI
ventana.mainloop()

