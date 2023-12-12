import tkinter as tk
from tkinter import messagebox


class TableroConecta4:
    def __init__(self, root, user1, user2):
        # Inicialización de la ventana principal y el tablero del juego
        self.ventana = root
        self.ventana.title("Conecta 4")
        self.user1 = user1
        self.user2 = user2
        self.ganador = None

        self.tablero = []
        for i in range(7):
            x = []
            for j in range(6):
                x.append(0)
            self.tablero.append(x)

        self.numero_ficha_actual = 1

        # Creación de la interfaz gráfica
        self.etiqueta_usuario1 = tk.Label(
            self.ventana, text=f"{self.user1}", font=("Helvetica", 16))
        self.etiqueta_usuario1.grid(row=3, column=0, columnspan=3)

        self.etiqueta_usuario2 = tk.Label(
            self.ventana, text=f"{self.user2}", font=("Helvetica", 16))
        self.etiqueta_usuario2.grid(row=3, column=4, columnspan=3)

        self.crear_interfaz()

    def cambiar_turno_etiqueta(self):
        # Cambia la etiqueta del turno al jugador correspondiente
        if self.numero_ficha_actual == 1:
            self.etiqueta_usuario2.config(text=f"Turno de {self.user2}")
            self.etiqueta_usuario1.config(text="")
        else:
            self.etiqueta_usuario1.config(text=f"Turno de {self.user1}")
            self.etiqueta_usuario2.config(text="")

    def ejecutar(self):
        # Inicia el bucle principal de la interfaz gráfica
        self.ventana.mainloop()

    def crear_interfaz(self):
        # Creación de los botones de columna en la parte superior
        self.botones = []
        for i in range(7):
            btn = tk.Button(self.ventana, text=str(
                i), command=lambda col=i: self.click_col(col))
            btn.grid(row=0, column=i)
            self.botones.append(btn)

        # Agrega una etiqueta para mostrar el estado del tablero
        self.etiqueta_tablero = tk.Label(self.ventana, text="")
        self.etiqueta_tablero.grid(row=1, columnspan=7)

        # Ajusta el tamaño del Canvas a una resolución de 900 x 800
        canvas_ancho = 900
        canvas_alto = 800

        # Agrega un Canvas para dibujar el tablero
        self.canvas_tablero = tk.Canvas(
            self.ventana, width=canvas_ancho, height=canvas_alto, bg='white')
        self.canvas_tablero.grid(row=2, columnspan=7)

        # Dibuja el tablero inicial
        self.dibujar_tablero()

    def dibujar_tablero(self):
        # Borra el contenido actual del Canvas y dibuja el tablero y fichas actualizado
        self.canvas_tablero.delete("all")
        columna_ancho = self.canvas_tablero.winfo_width() // 7
        fila_alto = self.canvas_tablero.winfo_height() // 6

        for i in range(7):
            for j in range(6):
                x1 = i * columna_ancho
                y1 = j * fila_alto
                x2 = x1 + columna_ancho
                y2 = y1 + fila_alto
                self.canvas_tablero.create_rectangle(
                    x1, y1, x2, y2, outline="black")
                if self.tablero[i][j] == 1:
                    self.canvas_tablero.create_oval(
                        x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                elif self.tablero[i][j] == 2:
                    self.canvas_tablero.create_oval(
                        x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="yellow")

    def click_col(self, col):
        # Maneja el evento de clic en una columna
        fila = self.obtener_fila_disponible(col)
        if fila is not None:
            self.addFicha(self.numero_ficha_actual, col, fila)
            self.dibujar_tablero()
            self.actualizar()
            self.cambiar_turno_etiqueta()

            if self.verificar_victoria(self.numero_ficha_actual):
                if (self.numero_ficha_actual == 1):
                    self.ganador = self.user1
                    self.ventana.destroy()
                    messagebox.showinfo(
                        "Victoria", f"¡Jugador {self.ganador} ha ganado!")
                elif (self.numero_ficha_actual == 2):
                    self.ganador = self.user2
                    self.ventana.destroy()
                    messagebox.showinfo(
                        "Victoria", f"¡Jugador {self.ganador} ha ganado!")
            # Cambia al siguiente jugador
            self.numero_ficha_actual = 3 - self.numero_ficha_actual

    def obtener_fila_disponible(self, col):
        # Devuelve la fila disponible en una columna
        for i in range(5, -1, -1):
            if self.tablero[col][i] == 0:
                return i
        return None

    def addFicha(self, num, col, fila):
        # Coloca una ficha en el tablero
        self.tablero[col][fila] = num

    def actualizar(self):
        # Actualiza la etiqueta con el nuevo estado del tablero
        tablero_str = ""  # Puedes personalizar esta cadena según sea necesario
        self.etiqueta_tablero.config(text=tablero_str)

    def verificar_victoria(self, num):
        # Verifica si hay una victoria en horizontal, vertical o diagonal
        # Verificar en horizontal
        for i in range(6):
            for j in range(4):
                if all(self.tablero[j + k][i] == num for k in range(4)):
                    return True

        # Verificar en vertical
        for i in range(7):
            for j in range(3):
                if all(self.tablero[i][j + k] == num for k in range(4)):
                    return True

        # Verificar en diagonal hacia arriba \
        for i in range(3, 6):
            for j in range(4):
                if all(self.tablero[j + k][i - k] == num for k in range(4)):
                    return True

        # Verificar en diagonal hacia abajo /
        for i in range(3):
            for j in range(4):
                if all(self.tablero[j + k][i + k] == num for k in range(4)):
                    return True

        return False
