import threading
import time
import random

class BufferAcotado:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.buffer = []
        self.condition = threading.Condition()

    def put(self, item):
        with self.condition:
            while len(self.buffer) >= self.capacidad:
                print(f"Buffer lleno ({len(self.buffer)}/{self.capacidad}), productor espera...")
                self.condition.wait()

            self.buffer.append(item)
            print(f"+ {item}  buffer: {len(self.buffer)}/{self.capacidad}")
            self.condition.notify_all()

    def get(self):
        with self.condition:
            while len(self.buffer) == 0:
                print("Buffer vacío, consumidor espera...")
                self.condition.wait()

            item = self.buffer.pop(0)
            print(f"- {item}  buffer: {len(self.buffer)}/{self.capacidad}")
            self.condition.notify_all()
            return item


buffer = BufferAcotado(3)

def productor(id):
    for i in range(5):
        time.sleep(random.uniform(0.1, 0.5))
        buffer.put(f"item-{id}-{i}")

def consumidor(id):
    for _ in range(5):
        time.sleep(random.uniform(0.2, 0.6))
        buffer.get()


productores = [threading.Thread(target=productor, args=(i,)) for i in range(2)]
consumidores = [threading.Thread(target=consumidor, args=(i,)) for i in range(2)]

for t in productores + consumidores:
    t.start()
for t in productores + consumidores:
    t.join()

print("Todos terminaron")