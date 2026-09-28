import threading
import time

condition = threading.Condition()
datos_disponibles = False
datos = None

def productor():
    global datos_disponibles, datos
    time.sleep(2)  # simular trabajo de producción

    with condition:
        datos = "datos producidos"
        datos_disponibles = True
        print("Productor: datos listos, notificando")
        condition.notify()  # notify_all() para despertar a todos

def consumidor(id):
    global datos_disponibles

    with condition:
        print(f"Consumidor {id}: esperando datos...")
        while not datos_disponibles:
            condition.wait()  # Libera el lock mientras espera
        print(f"Consumidor {id}: recibí '{datos}'")


t_prod = threading.Thread(target=productor)
t_cons = threading.Thread(target=consumidor, args=(1,))

t_cons.start()  # consumidor arranca primero, espera
t_prod.start()  # productor produce y notifica

t_prod.join()
t_cons.join()