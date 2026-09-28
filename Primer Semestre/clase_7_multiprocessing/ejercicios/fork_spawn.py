from multiprocessing import Process, set_start_method
import multiprocessing
import time
import os

NUM_PROCESOS = 100

def tarea():
    """Trabajo simple."""
    pass

def medir_tiempo(metodo):
    # Configurar método de creación
    multiprocessing.set_start_method(metodo, force=True)

    procesos = []

    inicio = time.time()

    # Crear procesos
    for _ in range(NUM_PROCESOS):
        p = Process(target=tarea)
        procesos.append(p)
        p.start()

    # Esperar procesos
    for p in procesos:
        p.join()

    fin = time.time()

    return fin - inicio


if __name__ == "__main__":

    print(f"PID principal: {os.getpid()}")
    print(f"Procesos a crear: {NUM_PROCESOS}\n")

    # Medir fork
    tiempo_fork = medir_tiempo("fork")

    print(f"fork  -> {tiempo_fork:.4f} segundos")

    # Medir spawn
    tiempo_spawn = medir_tiempo("spawn")

    print(f"spawn -> {tiempo_spawn:.4f} segundos")