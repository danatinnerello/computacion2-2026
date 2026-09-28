'''
import signal

def mi_manejador(signum, frame):
    """
    Función manejador de señal.

    Args:
        signum: número de la señal recibida
        frame: frame del stack donde se interrumpió (para debugging)
    """
    print(f"Recibí señal {signum}")

# Registrar el manejador
signal.signal(signal.SIGTERM, mi_manejador)

# También podemos usar constantes especiales:
signal.signal(signal.SIGUSR1, signal.SIG_IGN)  # Ignorar la señal
signal.signal(signal.SIGUSR2, signal.SIG_DFL)  # Restaurar acción por defecto

'''

#ctrl + c amigable

'''
import signal
import sys

def salir_limpiamente(sig, frame):
    print("\nRecibí Ctrl+C, limpiando...")
    # Aquí podés cerrar archivos, conexiones, etc.
    sys.exit(0)

signal.signal(signal.SIGINT, salir_limpiamente)

print("Presioná Ctrl+C para salir limpiamente")
while True:
    pass
    
'''

#Recargar configuración con SIGHUP

import os
import signal
import time

config = {"valor": "inicial"}

def recargar_config(sig, frame):
    global config
    print("Recargando configuración...")
    # En la vida real, leerías de un archivo
    config["valor"] = f"recargado a las {time.ctime()}"
    print(f"Nueva configuración: {config}")

signal.signal(signal.SIGHUP, recargar_config)

print(f"PID: {os.getpid()}")
print("Enviá 'kill -HUP <pid>' para recargar config")

while True:
    print(f"Config actual: {config['valor']}")
    time.sleep(5)