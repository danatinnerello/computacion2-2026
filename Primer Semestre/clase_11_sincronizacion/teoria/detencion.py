import threading
import time

detener = threading.Event()

def worker_cancelable(id):
    print(f"[Worker {id}] Iniciado")
    i = 0
    while not detener.is_set():
        print(f"[Worker {id}] Iteración {i}")
        i += 1
        # wait() con timeout permite chequear periódicamente sin polling activo
        detener.wait(timeout=1.0)
    print(f"[Worker {id}] Detenido limpiamente")


workers = [threading.Thread(target=worker_cancelable, args=(i,)) for i in range(3)]
for t in workers: t.start()

time.sleep(3)
print("\n=== Solicitando detención de todos los workers ===\n")
detener.set()

for t in workers: t.join()
print("Todos terminaron")



import threading

evento = threading.Event()

evento.set()            # señala (estado = True)
print(evento.is_set())  # True
evento.clear()          # resetea (estado = False)
print(evento.is_set())  # False

# wait() retorna True si fue señalado, False si timeout
evento.set()
print(evento.wait(timeout=1.0))   # True, inmediato