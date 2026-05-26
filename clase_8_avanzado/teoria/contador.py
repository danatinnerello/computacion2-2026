from multiprocessing import Process, Value

def incrementar(contador, cantidad):
    for _ in range(cantidad):
        # get_lock() previene race conditions (lo vemos formalmente en clase 10)
        with contador.get_lock():
            contador.value += 1

if __name__ == "__main__":
    # Tipos: 'i' = int, 'd' = double, 'b' = byte, etc.
    contador = Value('i', 0)

    procesos = [Process(target=incrementar, args=(contador, 10000))
                for _ in range(4)]

    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    print(f"Contador final: {contador.value}")  # 40000