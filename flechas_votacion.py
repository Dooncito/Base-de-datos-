import pymysql
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time
from conexion import crear_conexion
import random

# Variables globales
user_id = None
partida_id = 1  # Game ID or session ID
tiempo_voto = 20  # Voting duration in seconds
votacion_activa = False  # Voting flag
tiempo_inicio_votacion = None  # Voting start time

# Get Command ID from the database (comandos_referencia table)
def obtener_id_comando(direccion):
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                query = "SELECT ID_comando FROM comandos_referencia WHERE comando = %s"
                cursor.execute(query, (direccion,))
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]
                else:
                    print(f"Error: No se encontró el ID para el comando: {direccion}")
                    return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener ID del comando: {e}")
        finally:
            conexion.close()
    return None

# Register the vote using the stored procedure
def registrar_voto(direccion):
    if votacion_activa:
        conexion = crear_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Call stored procedure registrar_voto
                    cursor.callproc('registrar_voto', (user_id, direccion, partida_id))
                    conexion.commit()
                    print(f"Voto registrado: {direccion} por el usuario {user_id}")
            except pymysql.MySQLError as e:
                print(f"Error al registrar el voto: {e}")
            finally:
                conexion.close()
    else:
        messagebox.showerror("Error", "La votación no está activa en este momento. Espere el próximo ciclo.")


# Call the stored procedure to count votes and register the result
def contar_y_registrar_resultado():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                # Call stored procedure contar_y_registrar_resultado
                cursor.callproc('contar_y_registrar_resultado', (partida_id, tiempo_inicio_votacion))
                resultado = cursor.fetchone()
                print(resultado)
                # Check if the result is NULL
                if resultado and resultado[0]:
                    comando_ganador = resultado[0]
                else:
                    # If no result, assign "up" as the default command
                    movimiento=random.choice(["right","left","up","down"])
                    comando_ganador = obtener_id_comando(movimiento)
                    print("No hubo votos. Ejecutando el comando al azar: ", movimiento)

                print(f"Resultado registrado: {comando_ganador}")
        except pymysql.MySQLError as e:
            print(f"Error al contar los votos: {e}")
        finally:
            conexion.close()


# Call the stored procedure to clean up the old votes
def limpiar_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.callproc('limpiar_votos', (partida_id,))
                conexion.commit()
                print("Votos antiguos eliminados.")
        except pymysql.MySQLError as e:
            print(f"Error al limpiar los votos: {e}")
        finally:
            conexion.close()

# Handle voting process
def votar(direction):
    registrar_voto(direction)

# Voting timer and reset mechanism
def iniciar_votacion():
    global votacion_activa, tiempo_inicio_votacion
    votacion_activa = True
    tiempo_inicio_votacion = datetime.now()
    print("Inicia la votación. Los usuarios tienen 20 segundos para votar.")

    time.sleep(tiempo_voto)
    votacion_activa = False
    print("Tiempo de votación finalizado. Contando votos...")
    lock_table_votos()
    contar_y_registrar_resultado()
    unlock_table_votos()
    limpiar_votos()
    reset_votacion()

def lock_table_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("LOCK TABLES votos WRITE;")
                conexion.commit()
                print("Table votos locked for writing.")
        except pymysql.MySQLError as e:
            print(f"Error al bloquear la tabla votos: {e}")
        finally:
            conexion.close()

def unlock_table_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("UNLOCK TABLES;")
                conexion.commit()
                print("Table votos unlocked.")
        except pymysql.MySQLError as e:
            print(f"Error al desbloquear la tabla votos: {e}")
        finally:
            conexion.close()

def reset_votacion():
    print("Preparando la próxima votación...")
    time.sleep(5)
    iniciar_votacion()

# Panel de flechas para votación
def tkinter_controls(id_usuario):
    global user_id
    user_id=id_usuario
    ventana = Tk()
    ventana.title("Votación del Juego")
    ventana.geometry("200x200")

    btn_up = Button(ventana, text="↑", command=lambda: votar('up'), width=5, height=2)
    btn_up.pack(side=TOP, pady=5)

    btn_down = Button(ventana, text="↓", command=lambda: votar('down'), width=5, height=2)
    btn_down.pack(side=BOTTOM, pady=5)

    btn_left = Button(ventana, text="←", command=lambda: votar('left'), width=5, height=2)
    btn_left.pack(side=LEFT, padx=5)

    btn_right = Button(ventana, text="→", command=lambda: votar('right'), width=5, height=2)
    btn_right.pack(side=RIGHT, padx=5)

    threading.Thread(target=iniciar_votacion).start()

    ventana.mainloop()
