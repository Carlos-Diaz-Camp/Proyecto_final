import tkinter as tk
import random
from tkinter import messagebox

class MatrizAritmeticaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juego Matriz Aritmética")
        self.root.geometry("400x400")

        self.crear_interfaz()

        self.root.mainloop()

    def crear_interfaz(self):
        # Etiqueta y entrada para el número de participaciones
        self.label_participaciones = tk.Label(self.root, text="Número de rondas:")
        self.label_participaciones.pack()
        self.entry_participaciones = tk.Entry(self.root)
        self.entry_participaciones.pack()

        # Etiqueta y entrada para el tamaño del tablero
        self.label_tamano = tk.Label(self.root, text="Ingrese el tamaño de la matriz(n*n):")
        self.label_tamano.pack()
        self.entry_tamano = tk.Entry(self.root)
        self.entry_tamano.pack()

        # Etiqueta y entradas para los nombres de los jugadores
        self.label_nombres = tk.Label(self.root, text="Nombres de los jugadores:")
        self.label_nombres.pack()
        self.entry_nombre1 = tk.Entry(self.root)
        self.entry_nombre1.pack()
        self.entry_nombre2 = tk.Entry(self.root)
        self.entry_nombre2.pack()

        # Botón para iniciar el juego
        self.button_iniciar = tk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego)
        self.button_iniciar.pack()

    def iniciar_juego(self):
        # Obtener el número de participaciones y el tamaño del tablero
        participaciones = int(self.entry_participaciones.get())
        tamano = int(self.entry_tamano.get())

        # Obtener los nombres de los jugadores
        nombre1 = self.entry_nombre1.get()
        nombre2 = self.entry_nombre2.get()
        self.nombres = [nombre1, nombre2]

        # Crear el tablero de juego
        self.tablero = self.crear_tablero(tamano)

        # Crear la interfaz del juego
        self.crear_interfaz_juego()

        # Iniciar el juego
        self.participaciones = 0
        self.puntajes = [0, 0]
        self.turno = 0
        self.mostrar_puntajes()
        self.mostrar_turno()
        self.siguiente_turno()

    def crear_tablero(self, tamano):
        tablero = []
        for _ in range(tamano):
            fila = [random.randint(0, 11) for _ in range(tamano)]
            tablero.append(fila)
        return tablero

    def crear_interfaz_juego(self):
        # Ocultar la interfaz de configuración
        self.label_participaciones.pack_forget()
        self.entry_participaciones.pack_forget()
        self.label_tamano.pack_forget()
        self.entry_tamano.pack_forget()
        self.label_nombres.pack_forget()
        self.entry_nombre1.pack_forget()
        self.entry_nombre2.pack_forget()
        self.button_iniciar.pack_forget()

        # Crear el marco para la interfaz del juego
        self.frame_juego = tk.Frame(self.root)
        self.frame_juego.pack()

        # Etiqueta para mostrar el tablero
        self.label_tablero = tk.Label(self.frame_juego)
        self.label_tablero.pack()

        # Etiqueta para mostrar los puntajes
        self.label_puntajes = tk.Label(self.frame_juego, text="Puntajes:")
        self.label_puntajes.pack()

        # Etiqueta para mostrar el turno
        self.label_turno = tk.Label(self.frame_juego, text="Turno:")
        self.label_turno.pack()

    def mostrar_puntajes(self):
        puntajes_texto = f"{self.nombres[0]}: {self.puntajes[0]}   {self.nombres[1]}: {self.puntajes[1]}"
        self.label_puntajes.config(text=puntajes_texto)

    def mostrar_turno(self):
        turno_texto = f"Turno de: {self.nombres[self.turno]}"
        self.label_turno.config(text=turno_texto)

    def siguiente_turno(self):
        self.participaciones += 1

        if self.participaciones > int(self.entry_participaciones.get()):
            self.mostrar_resultado_final()
        else:
            self.mostrar_puntajes()
            self.mostrar_turno()
            self.crear_tablero_interactivo()

    def crear_tablero_interactivo(self):
        tamano = len(self.tablero)
        self.botones = []
        for i in range(tamano):
            fila_botones = []
            for j in range(tamano):
                boton = tk.Button(self.label_tablero, text="", width=4, height=2, command=lambda i=i, j=j: self.revelar_numero(i, j))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def revelar_numero(self, fila, columna):
        numero = self.tablero[fila][columna]
        vecinos = self.obtener_vecinos(fila, columna)
        suma_vecinos = sum(vecinos)
        operacion = f"({'+'.join(map(str, vecinos))})*{numero}"
        self.operacion_actual = operacion

        # Ocultar los botones
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero)):
                self.botones[i][j].config(text="", state=tk.DISABLED)

        # Mostrar el número seleccionado y sus vecinos
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero)):
                if (i == fila and j == columna) or (i, j) in self.obtener_posiciones_vecinos(fila, columna):
                    self.botones[i][j].config(text=str(self.tablero[i][j]), bg="gray", fg="white")
                else:
                    self.botones[i][j].config(text="", bg="white")

        self.mostrar_operacion(operacion)

    def obtener_vecinos(self, fila, columna):
        vecinos = []
        for i, j in self.obtener_posiciones_vecinos(fila, columna):
            vecinos.append(self.tablero[i][j])
        return vecinos

    def obtener_posiciones_vecinos(self, fila, columna):
        posiciones = []
        tamano = len(self.tablero)
        for i in range(max(0, fila - 1), min(fila + 2, tamano)):
            for j in range(max(0, columna - 1), min(columna + 2, tamano)):
                posiciones.append((i, j))
        return posiciones

    def mostrar_operacion(self, operacion):
        self.label_operacion = tk.Label(self.frame_juego, text=operacion)
        self.label_operacion.pack()

        self.crear_opciones_respuesta()

    def crear_opciones_respuesta(self):
        opciones = self.generar_opciones_respuesta()

        self.frame_opciones = tk.Frame(self.frame_juego)
        self.frame_opciones.pack()

        for i, opcion in enumerate(opciones):
            boton = tk.Button(self.frame_opciones, text=str(opcion), width=4, height=2, command=lambda opcion=opcion: self.verificar_respuesta(opcion))
            boton.pack(side=tk.LEFT)

    def generar_opciones_respuesta(self):
        resultado = eval(self.operacion_actual)
        opciones = [resultado]
        while len(opciones) < 4:
            opcion = random.randint(resultado - 10, resultado + 10)
            if opcion != resultado and opcion not in opciones:
                opciones.append(opcion)
        random.shuffle(opciones)
        return opciones

    def verificar_respuesta(self, respuesta):
        resultado = eval(self.operacion_actual)
        if respuesta == resultado:
            self.puntajes[self.turno] += 3
            messagebox.showinfo("Respuesta Correcta", "¡Respuesta correcta!")
        else:
            messagebox.showinfo("Respuesta Incorrecta", f"Respuesta incorrecta. La respuesta correcta es {resultado}")

        self.label_operacion.pack_forget()
        self.frame_opciones.pack_forget()

        self.siguiente_turno()

    def mostrar_resultado_final(self):
        messagebox.showinfo("Fin del Juego", f"El juego ha terminado.\n Resultado final:\n\n{self.nombres[0]}: {self.puntajes[0]}\n{self.nombres[1]}: {self.puntajes[1]}")
        self.root.destroy()


if __name__ == "__main__":
    juego = MatrizAritmeticaGUI()