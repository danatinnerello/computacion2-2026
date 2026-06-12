# src/main.py

from recolector import recolectar

snapshot = recolectar()

print("Procesos:", len(snapshot["procesos"]))
print("CPU:", snapshot["cpu"])
print("Memoria total:", snapshot["memoria"]["MemTotal"])