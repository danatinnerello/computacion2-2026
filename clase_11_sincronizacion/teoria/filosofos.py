import threading
import time
import random

NUM_FILOSOFOS = 5

class Filosofo(threading.Thread):
    def __init__(self, id, tenedores):
        super().__init__()
        self.id = id
        self.tenedores = tenedores
        # Índices de los tenedores, NO los locks
        self.izq = id
        self.der = (id + 1) % NUM_FILOSOFOS

    def run(self):
        for _ in range(3):
            self.pensar()
            self.comer()

    def pensar(self):
        print(f"Filósofo {self.id} piensa")
        time.sleep(random.uniform(0.1, 0.5))

    def comer(self):
        # Jerarquía de recursos: siempre tomar el tenedor de MENOR índice
        # primero. Esto rompe la espera circular.
        primero, segundo = sorted((self.izq, self.der))

        with self.tenedores[primero]:
            with self.tenedores[segundo]:
                print(f"Filósofo {self.id} come (tenedores {primero} y {segundo})")
                time.sleep(random.uniform(0.1, 0.3))


tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
filosofos = [Filosofo(i, tenedores) for i in range(NUM_FILOSOFOS)]

for f in filosofos: f.start()
for f in filosofos: f.join()
print("Todos terminaron de comer")