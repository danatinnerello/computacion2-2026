import threading
import time

def contar(n):
    """Tarea CPU-bound."""
    total = 0
    for i in range(n):
        total += i
    return total

N = 50_000_000

# Secuencial
inicio = time.time()
contar(N)
contar(N)
print(f"Secuencial: {time.time() - inicio:.2f}s")

# Con threads (NO es más rápido por el GIL!)
inicio = time.time()
t1 = threading.Thread(target=contar, args=(N,))
t2 = threading.Thread(target=contar, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Threads: {time.time() - inicio:.2f}s")