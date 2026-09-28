'''

import signal
import sys
import time
import os

class Servidor:
    def __init__(self):
        self.ejecutando = True
        self.conexiones = []

        # Registrar manejadores
        signal.signal(signal.SIGTERM, self._manejar_shutdown)
        signal.signal(signal.SIGINT, self._manejar_shutdown)
        signal.signal(signal.SIGHUP, self._manejar_reload)

    def _manejar_shutdown(self, sig, frame):
        print(f"\nRecibí {signal.Signals(sig).name}, iniciando shutdown...")
        self.ejecutando = False

    def _manejar_reload(self, sig, frame):
        print("Recargando configuración...")
        # Recargar config aquí

    def cerrar_conexiones(self):
        print(f"Cerrando {len(self.conexiones)} conexiones...")
        # Cerrar conexiones aquí

    def ejecutar(self):
        print(f"Servidor iniciado (PID {os.getpid()})")

        while self.ejecutando:
            print("Procesando...")
            time.sleep(1)

        self.cerrar_conexiones()
        print("Servidor terminado limpiamente")

if __name__ == "__main__":
    servidor = Servidor()
    servidor.ejecutar()
'''
import os
import signal
import time

workers = []
ejecutando = True

def terminar_workers(sig, frame):
    global ejecutando
    print("\nTerminando workers...")
    ejecutando = False
    for pid in workers:
        os.kill(pid, signal.SIGTERM)

signal.signal(signal.SIGINT, terminar_workers)
signal.signal(signal.SIGTERM, terminar_workers)

# Crear workers
for i in range(3):
    pid = os.fork()
    if pid == 0:
        # Worker
        while True:
            print(f"[Worker {os.getpid()}] trabajando")
            time.sleep(1)
    else:
        workers.append(pid)

# Supervisor
print(f"Supervisor PID: {os.getpid()}")
print(f"Workers: {workers}")

while ejecutando and workers:
    # Recoger workers terminados
    try:
        pid, status = os.waitpid(-1, os.WNOHANG)
        if pid > 0:
            workers.remove(pid)
            print(f"Worker {pid} terminó")
    except ChildProcessError:
        break
    time.sleep(0.5)

# Esperar a todos
for pid in workers:
    os.waitpid(pid, 0)

print("Todos los workers terminados")