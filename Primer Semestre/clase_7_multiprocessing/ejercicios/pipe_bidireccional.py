#!/usr/bin/env python3
"""Ping-Pong con multiprocessing.Pipe."""

from multiprocessing import Process, Pipe
import time
import os


def hijo(conn):
    """Proceso hijo."""
    for i in range(5):
        # Esperar mensaje del padre
        mensaje = conn.recv()
        print(f"[HIJO {os.getpid()}] recibió: {mensaje}")
        time.sleep(1)
        # Responder
        respuesta = f"pong {i+1}"
        conn.send(respuesta)
    conn.close()


if __name__ == "__main__":
    # Crear pipe bidireccional
    padre_conn, hijo_conn = Pipe()
    # Crear proceso hijo
    p = Process(target=hijo, args=(hijo_conn,))
    p.start()
    # Ping-Pong
    for i in range(5):
        mensaje = f"ping {i+1}"
        print(f"[PADRE {os.getpid()}] envía: {mensaje}")
        padre_conn.send(mensaje)
        # Esperar respuesta
        respuesta = padre_conn.recv()
        print(f"[PADRE] recibió: {respuesta}")
    # Cerrar conexión
    padre_conn.close()
    # Esperar hijo
    p.join()
    print("\nComunicación finalizada")