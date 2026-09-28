import threading
import time

def cuando_todos_llegan():
    print(">>> TODOS LLEGARON A LA BARRERA <<<")

barrera = threading.Barrier(3, action=cuando_todos_llegan)

def worker(id):
    print(f"[{id}] llegó")
    barrera.wait()
    print(f"[{id}] continúa")

hilos = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in hilos: t.start()
for t in hilos: t.join()