import threading
import time

barrera = threading.Barrier(3)

def worker(id, delay):
    time.sleep(delay)
    try:
        barrera.wait(timeout=2.0)
        print(f"[{id}] Pasó la barrera")
    except threading.BrokenBarrierError:
        print(f"[{id}] Barrera rota: alguien no llegó")

hilos = [
    threading.Thread(target=worker, args=(0, 0.5)),
    threading.Thread(target=worker, args=(1, 1.0)),
    threading.Thread(target=worker, args=(2, 5.0)),  # éste tarda demasiado
]
for t in hilos: t.start()
for t in hilos: t.join()