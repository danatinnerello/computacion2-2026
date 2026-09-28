import threading
import time

condition = threading.Condition()

def esperador():
    with condition:
        print("Esperando hasta 5 segundos...")
        resultado = condition.wait(timeout=5.0)
        if resultado:
            print("Condición notificada a tiempo")
        else:
            print("Timeout: no hubo notificación")

t = threading.Thread(target=esperador)
t.start()
# Nadie llama a notify(): el thread espera 5s y reporta timeout
t.join()