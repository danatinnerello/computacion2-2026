import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:           # primera comprobación SIN lock (rápido)
            with cls._lock:
                if cls._instance is None:   # segunda comprobación CON lock (correcto)
                    cls._instance = cls()
        return cls._instance

# Uso desde múltiples threads
import threading
def crear():
    s = Singleton.get_instance()
    print(f"{threading.current_thread().name}: instancia = {id(s)}")

hilos = [threading.Thread(target=crear) for _ in range(5)]
for t in hilos: t.start()
for t in hilos: t.join()
# Todos ven el mismo id() (misma instancia)