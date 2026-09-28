from multiprocessing import Process
import os

def trabajo_hijo():
    print(f"Hijo trabajando... PID={os.getpid()}")
    # Simular trabajo
    for i in range(3):
        print(f"  Hijo: paso {i+1}")
    print("Hijo terminando")

if __name__ == "__main__":
    print(f"Proceso original: PID={os.getpid()}")
    # Crear proceso hijo
    p = Process(target=trabajo_hijo)
    # Iniciar proceso
    p.start()
    print(f"Padre esperando al hijo {p.pid}...")
    # Esperar al hijo
    p.join()
    print(f"Padre: hijo terminó con código {p.exitcode}")