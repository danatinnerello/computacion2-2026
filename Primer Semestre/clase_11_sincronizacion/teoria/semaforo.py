import threading
import time
import random

# Máximo 3 conexiones simultáneas
pool_conexiones = threading.Semaphore(3)

def usar_conexion(id):
    print(f"[{id}] Esperando conexión...")
    with pool_conexiones:
        print(f"[{id}] Conectado")
        time.sleep(random.uniform(1, 2))  # Trabajo con la conexión
        print(f"[{id}] Desconectando")


# 10 threads compiten por las 3 conexiones disponibles
hilos = [threading.Thread(target=usar_conexion, args=(i,)) for i in range(10)]
for t in hilos: t.start()
for t in hilos: t.join()
print("Todos terminaron")