import threading
import time
import random

inicio = threading.Event()

def corredor(id):
    print(f"[Corredor {id}] En la línea de partida...")
    inicio.wait()  # Bloquea hasta que inicio.set()
    print(f"[Corredor {id}] ¡Arrancó!")
    tiempo = random.uniform(1, 3)
    time.sleep(tiempo)
    print(f"[Corredor {id}] Llegó en {tiempo:.2f}s")


corredores = [threading.Thread(target=corredor, args=(i,)) for i in range(5)]
for t in corredores: t.start()

# Dar tiempo a que todos lleguen a la línea
time.sleep(1)

print("\n=== PREPARADOS... LISTOS... YA! ===\n")
inicio.set()  # Todos arrancan simultáneamente

for t in corredores: t.join()