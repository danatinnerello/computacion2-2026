import threading

# Estructura compartida
datos = {"contador": 0, "suma": 0}

def actualizar(valor):
    # Las dos operaciones deberían ser atómicas
    datos["contador"] += 1
    datos["suma"] += valor
    # Si se interrumpe entre ambas, los datos quedan inconsistentes

# Lanzar 100 threads incrementando
hilos = [threading.Thread(target=actualizar, args=(10,)) for _ in range(100)]
for h in hilos: h.start()
for h in hilos: h.join()

print(f"contador: {datos['contador']}, suma: {datos['suma']}")
# Esperado: contador=100, suma=1000
# Real: puede salir cualquier cosa menor