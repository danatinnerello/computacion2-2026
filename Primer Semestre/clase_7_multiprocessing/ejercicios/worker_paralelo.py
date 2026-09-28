#!/usr/bin/env python3
"""5 workers en paralelo."""

from multiprocessing import Process
import time
import random
import os


def worker(numero):
    espera = random.uniform(0.5, 2)
    print(f"Worker {numero} (PID={os.getpid()}) "
          f"trabajando durante {espera:.2f} segundos")
    time.sleep(espera)
    print(f"Worker {numero} terminó")


if __name__ == "__main__":
    procesos = []
    inicio = time.time()
    # Crear y lanzar 5 procesos
    for i in range(5):
        p = Process(target=worker, args=(i + 1,))
        procesos.append(p)
        p.start()

    # Esperar a todos
    for p in procesos:
        p.join()

    fin = time.time()

    print(f"\nTodos los workers terminaron")
    print(f"Tiempo total: {fin - inicio:.2f} segundos")