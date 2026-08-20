import threading
import time
import random

class ReadWriteLock:
    """Lock que permite múltiples lectores O un solo escritor."""

    def __init__(self):
        self.readers = 0
        self.resource_lock = threading.Lock()   # protege el recurso
        self.readers_lock = threading.Lock()    # protege el contador

    def acquire_read(self):
        with self.readers_lock:
            self.readers += 1
            if self.readers == 1:
                # El primer lector toma el lock del recurso
                self.resource_lock.acquire()

    def release_read(self):
        with self.readers_lock:
            self.readers -= 1
            if self.readers == 0:
                # El último lector libera el recurso
                self.resource_lock.release()

    def acquire_write(self):
        self.resource_lock.acquire()

    def release_write(self):
        self.resource_lock.release()


# Uso con context managers
class ReadContext:
    def __init__(self, rwlock): self.rwlock = rwlock
    def __enter__(self): self.rwlock.acquire_read()
    def __exit__(self, *args): self.rwlock.release_read()

class WriteContext:
    def __init__(self, rwlock): self.rwlock = rwlock
    def __enter__(self): self.rwlock.acquire_write()
    def __exit__(self, *args): self.rwlock.release_write()


rwlock = ReadWriteLock()
datos = {"valor": 0}

def lector(id):
    for _ in range(3):
        with ReadContext(rwlock):
            print(f"[Lector {id}] leyendo: {datos}")
            time.sleep(0.1)
        time.sleep(random.uniform(0.1, 0.3))

def escritor(id):
    for i in range(3):
        with WriteContext(rwlock):
            datos["valor"] = i * 100 + id
            print(f"[Escritor {id}] escribió: {datos}")
            time.sleep(0.2)
        time.sleep(random.uniform(0.2, 0.5))


hilos = (
    [threading.Thread(target=lector, args=(i,)) for i in range(3)] +
    [threading.Thread(target=escritor, args=(i,)) for i in range(2)]
)
for t in hilos: t.start()
for t in hilos: t.join()
