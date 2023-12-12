import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # Importar Image y ImageTk de la biblioteca Pillow
import hashlib
from database.database import Database
from games.Conecta4.Mitablero import TableroConecta4
# Diccionarios para almacenar los usuarios registrados en cada lado
MiDataBase = Database()

# Variable global para rastrear intentos fallidos de inicio de sesión
intentos_fallidos = 0

usuario1 = None
usuario2 = None

UsersRegistes = False

# Función para registrar un nuevo usuario


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


def abrir_ventana_modal(usuario):
    # Crear una nueva ventana Toplevel (ventana modal)
    ventana_modal = tk.Toplevel(root)
    ventana_modal.title("Ventana Modal")

    Titulo = tk.Label(ventana_modal, text="Actualizando contraseña")
    Titulo.pack()

    # Variables para almacenar las contraseñas
    oldpass_var = tk.StringVar()
    newpass_var = tk.StringVar()

    # Widget de entrada para la contraseña antigua
    entrada_password_old = tk.Entry(ventana_modal, textvariable=oldpass_var)
    entrada_password_old.pack(pady=10)

    # Widget de entrada para la contraseña nueva
    entrada_password_new = tk.Entry(ventana_modal, textvariable=newpass_var)
    entrada_password_new.pack(pady=10)

    boton_texto = tk.Button(ventana_modal, text="OK", command=lambda: MiDataBase.updatePassword(
        usuario, hash_password(oldpass_var.get()), hash_password(newpass_var.get())))
    boton_texto.pack(pady=5)


def register(user_entry, password_entry):
    user = user_entry.get()
    password = hash_password(password_entry.get())
    print(MiDataBase.createPlayer(user, password))

# Función para iniciar sesión


def jugar(usuario1, usuario2):
    root = tk.Tk()
    juego = TableroConecta4(root, usuario1, usuario2)
    juego.ejecutar()


def login(user_entry, password_entry, button_jugar):
    global intentos_fallidos, usuario1, usuario2, UsersRegistes

    user = user_entry.get()
    password = hash_password(password_entry.get())
    exist = MiDataBase.loginPlayer(user, password)

    if exist:
        if UsersRegistes == False:
            usuario1 = user
            print(f"Login - user: {user}, Login successful")
            UsersRegistes = True
        elif UsersRegistes:
            usuario2 = user
            print(f"Login - user: {user}, Login successful")
            UsersRegistes = None
        else:
            print("Ya hay dos usuarios registrados")

        # Si ambos usuarios han iniciado sesión, activar el botón "Jugar"
        if UsersRegistes == None:
            button_jugar.config(
                state=tk.NORMAL, command=lambda: jugar(usuario1, usuario2))

        return True
    else:
        print("Login - Usuario no registrado o contraseña incorrecta")
        intentos_fallidos += 1

        if intentos_fallidos == 3:
            print("Demasiados intentos fallidos. Cerrando el programa.")
            root.destroy()  # Cierra la ventana principal y finaliza el programa

        return False

# Función para gestionar la apertura de archivos


def gestionar_archivo():
    # Ruta a la carpeta de imágenes (ajusta la ruta según la estructura de tu proyecto)
    carpeta_imagenes = "../images/"
    archivo = filedialog.askopenfilename(initialdir=carpeta_imagenes, filetypes=[
                                         ("Imágenes", "*.jpg *.png")])

    if archivo:
        ventana_superior = tk.Toplevel()
        imagen_origen = Image.open(archivo)
        imagen_tk = ImageTk.PhotoImage(imagen_origen)

        etiqueta_imagen = tk.Label(ventana_superior, image=imagen_tk)
        etiqueta_imagen.image = imagen_tk
        etiqueta_imagen.pack()

# Función para crear la interfaz de usuario


def create_user_interface(root, color, usuarioIniciado, userInput):
    frame = tk.Frame(root, background=color)

    # Estilo para los widgets ttk
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 14, "bold"),
                    foreground="black", background=color)
    style.configure("TButton", font=("Helvetica", 12, "bold"),
                    foreground="black", background="gray")

    # Creación de widgets
    label_user = ttk.Label(frame, text="Usuario:")
    user_entry = ttk.Entry(frame, font=("Helvetica", 12))

    label_password = ttk.Label(frame, text="Contraseña:")
    entry_password = ttk.Entry(frame, show="*", font=("Helvetica", 12))

    button_register = ttk.Button(
        frame, text="Registrar", command=lambda: register(user_entry, entry_password))

    if not hasattr(root, "button_jugar"):
        setattr(root, "button_jugar", ttk.Button(
            frame, text="Jugar", state=tk.DISABLED))

    button_login = ttk.Button(frame, text="Iniciar Sesión", command=lambda: login(
        user_entry, entry_password, root.button_jugar) or usuarioIniciado)

    button_select_icon = ttk.Button(
        frame, text="Seleccionar icono", command=gestionar_archivo)

    button_edit_contrasena = ttk.Button(
        frame, text="Editar contraseña", command=lambda: abrir_ventana_modal(label_user["text"]))

    # Organización de los widgets en la cuadrícula
    label_user.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    user_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
    label_password.grid(row=1, column=0, pady=10, padx=10, sticky="w")
    entry_password.grid(row=1, column=1, pady=10, padx=10, sticky="w")
    button_register.grid(row=2, column=0, columnspan=2,
                         pady=10, padx=10, sticky="we")
    button_login.grid(row=3, column=0, columnspan=2,
                      pady=10, padx=10, sticky="we")
    button_select_icon.grid(row=4, column=0, columnspan=2,
                            pady=10, padx=10, sticky="we")
    # Modificación: Agregar botón "Jugar" solo una vez
    root.button_jugar.grid(row=8, column=1, columnspan=2,
                           pady=10, padx=10, sticky="we")
    button_edit_contrasena.grid(
        row=6, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    return frame

# Función principal para mostrar la interfaz gráfica


def mostrar_gui():
    global userLeft, userRight, usuario1, usuario2

    # Crear la ventana principal
    global root
    root = tk.Tk()
    root.title("Login")
    root.geometry("800x600")
    root.resizable(False, False)

    # Crear marcos para el lado izquierdo y derecho
    frame_left = create_user_interface(
        root, "#66a3ff", False, usuario1)  # Azul claro
    frame_right = create_user_interface(
        root, "#99cc99", False, usuario2)  # Verde claro

    # Empaquetar los marcos en la ventana principal
    frame_left.pack(side="left", fill="both", expand=True)
    frame_right.pack(side="right", fill="both", expand=True)

    # Iniciar la aplicación
    root.mainloop()
