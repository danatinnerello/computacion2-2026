import threading
import time

class MiThread(threading.Thread):
    def __init__(self, nombre, duracion):
        super().__init__()
        self.nombre = nombre
        self.duracion = duracion
        self.resultado = None

    def run(self):
        """Este método se ejecuta cuando llamás start()."""
        print(f"[{self.nombre}] Trabajando...")
        time.sleep(self.duracion)
        self.resultado = f"Completado en {self.duracion}s"
        print(f"[{self.nombre}] {self.resultado}")

# Crear y ejecutar
t = MiThread("Worker", 2)
t.start()
t.join()
print(f"Resultado: {t.resultado}")