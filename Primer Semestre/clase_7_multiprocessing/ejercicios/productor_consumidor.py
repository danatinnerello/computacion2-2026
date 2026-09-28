#!/usr/bin/env python3
"""Productor - Consumidor con multiprocessing.Queue."""

from multiprocessing import Process, Queue
import time
import random


def productor(queue):
    """Genera 10 items."""
    for i in range(1, 11):
        item = f"item-{i}"
        print(f"[PRODUCTOR] Generando {item}")
        queue.put(item)
        time.sleep(random.uniform(0.3, 1))

    # Señal de finalización
    queue.put(None)
    print("[PRODUCTOR] Terminó")


def consumidor(queue):
    """Consume items de la cola."""
    while True:
        item = queue.get()
        # Verificar fin
        if item is None:
            break
        print(f"    [CONSUMIDOR] Procesando {item}")
        time.sleep(random.uniform(0.5, 1.5))
    print("    [CONSUMIDOR] Terminó")


if __name__ == "__main__":
    queue = Queue()
    # Crear procesos
    p_productor = Process(target=productor, args=(queue,))
    p_consumidor = Process(target=consumidor, args=(queue,))

    # Iniciar procesos
    p_productor.start()
    p_consumidor.start()

    # Esperar procesos
    p_productor.join()
    p_consumidor.join()

    print("\nPrograma finalizado")