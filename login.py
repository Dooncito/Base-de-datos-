import pymysql
from tkinter import *
from tkinter import messagebox
from conexion import crear_conexion

# Variables globales
partida_id = 1  # Game ID or session ID

class LoginPage:
    def __init__(self):
        self.ventana_login = Tk()
        self.ventana_login.title("Login")
        self.ventana_login.geometry("300x200")

        self.label_nombre = Label(self.ventana_login, text="Nombre de Usuario:")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = Entry(self.ventana_login)
        self.entry_nombre.pack(pady=5)

        self.btn_login = Button(self.ventana_login, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        self.btn_registro = Button(self.ventana_login, text="Registrar", command=self.abrir_registro)
        self.btn_registro.pack(pady=5)

        self.inicio_correcto=False
        self.user_id=None

        self.ventana_login.mainloop()

    def abrir_registro(self):
        self.ventana_login.withdraw()
        RegistroPage(self)

    def mostrar_ventana_login(self):
        self.ventana_login.deiconify()

    def login(self):
        nombre_usuario = self.entry_nombre.get()
        if nombre_usuario:
            self.verificar_login(nombre_usuario)

    # User login verification
    def verificar_login(self, nombre_usuario):
        conexion = crear_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    query = "SELECT ID_usuario FROM usuarios WHERE nombre_usuario = %s"
                    cursor.execute(query, (nombre_usuario,))
                    resultado = cursor.fetchone()
                    if resultado:
                        self.user_id = resultado[0]
                        messagebox.showinfo("Login", f"Bienvenido, {nombre_usuario}!")
                        self.ventana_login.destroy()
                        print("llegamos al final")
                        self.inicio_correcto = True
                    else:
                        messagebox.showerror("Error", "Usuario no encontrado.")
            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"Error en el login: {e}")
            finally:
                conexion.close()

# GUI for user registration
class RegistroPage:
    def __init__(self, login_page):
        self.login_page=login_page
        self.ventana_registro = Toplevel()
        self.ventana_registro.title("Registro de Usuario")
        self.ventana_registro.geometry("300x200")

        self.label_nombre = Label(self.ventana_registro, text="Nombre de Usuario:")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = Entry(self.ventana_registro)
        self.entry_nombre.pack(pady=5)

        self.btn_registrar = Button(self.ventana_registro, text="Registrar", command=self.registrar)
        self.btn_registrar.pack(pady=10)

    def registrar(self):
        nombre_usuario = self.entry_nombre.get()
        if nombre_usuario:
            self.registrar_usuario(nombre_usuario)
            self.ventana_registro.destroy()
            self.login_page.mostrar_ventana_login()

    # User registration
    def registrar_usuario(self,nombre_usuario):
        conexion = crear_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
                    resultado = cursor.fetchone()
                    if resultado:
                        messagebox.showerror("Error", "El usuario ya existe.")
                    else:
                        query = "INSERT INTO usuarios (nombre_usuario) VALUES (%s)"
                        cursor.execute(query, (nombre_usuario,))
                        conexion.commit()
                        messagebox.showinfo("Registro", f"Usuario '{nombre_usuario}' registrado correctamente.")
            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"Error al registrar el usuario: {e}")
            finally:
                conexion.close()
