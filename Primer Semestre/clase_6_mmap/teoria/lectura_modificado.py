#!/usr/bin/env python3
"""Crear archivo, mapearlo, buscar y reemplazar con mmap."""
import mmap

ruta = "/tmp/mmap_test.txt"

# Crear archivo con 5 líneas
with open(ruta, "wb") as f:
    f.write(b"Linea 1: Hola mundo\n")
    f.write(b"Linea 2: Python es genial\n")
    f.write(b"Linea 3: Me gusta programar\n")
    f.write(b"Linea 4: Computacion II\n")
    f.write(b"Linea 5: Fin del archivo\n")

# Abrir en modo lectura/escritura
with open(ruta, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    print("=== Contenido original ===")
    print(mm[:].decode())

    # Buscar palabra
    palabra = b"Python"
    nueva = b"PYTHON"   # mismo largo (6 bytes)

    pos = mm.find(palabra)

    if pos == -1:
        print("No se encontró la palabra")
    else:
        print(f"Encontrado en posición: {pos}")

        # Reemplazar
        mm.seek(pos)
        mm.write(nueva)

    #  Ver resultado en memoria
    mm.seek(0)
    print("\n=== Después del cambio ===")
    print(mm[:].decode())

    mm.close()