import mmap

with open("ejemplo.txt", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    # Como archivo:
    mm.seek(0)
    linea = mm.readline()
    print(f"Primera línea: {linea}")

    # Como bytearray (slicing):
    datos = mm[10:20]
    print(f"Bytes 10-20: {datos}")

    # Buscar patrones:
    pos = mm.find(b"palabra")
    if pos != -1:
        print(f"Encontrado en posición {pos}")

    # Tamaño:
    print(f"Tamaño: {mm.size()} bytes")

    # Redimensionar (si es un archivo real):
    mm.resize(2048)

    mm.close()