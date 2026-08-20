import threading

# Variable compartida
saldo = 1000

def retirar(cantidad):
    global saldo
    if saldo >= cantidad:
        # Ventana de vulnerabilidad: otro thread puede modificar saldo aquí
        saldo -= cantidad
        return True
    return False

# Lanzar 10 threads que intentan retirar simultáneamente
hilos = [threading.Thread(target=retirar, args=(200,)) for _ in range(10)]
for h in hilos: h.start()
for h in hilos: h.join()

print(f"Saldo final: {saldo}")  # ¡Puede ser negativo!