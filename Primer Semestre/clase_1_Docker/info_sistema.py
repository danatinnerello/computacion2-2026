import sys
import os
import platform

def mostrar_info():
    print("=== INFO DEL SISTEMA ===\n")

    # Versión de Python
    print(f"Python versión: {sys.version}\n")

    # Sistema operativo
    print(f"Sistema operativo: {platform.system()}")
    print(f"Versión: {platform.version()}")
    print(f"Release: {platform.release()}\n")

    # CPUs
    print(f"Cantidad de CPUs: {os.cpu_count()}\n")

    # Memoria (solo Linux)
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if "MemAvailable" in line:
                    print(f"Memoria disponible: {line.strip()}")
                    break
    except:
        print("Memoria disponible: No se pudo obtener\n")

    # Variables de entorno PYTHON*
    print("\nVariables de entorno (PYTHON*):")
    for key, value in os.environ.items():
        if key.startswith("PYTHON"):
            print(f"{key} = {value}")

if __name__ == "__main__":
    mostrar_info()