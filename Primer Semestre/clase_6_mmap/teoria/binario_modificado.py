#!/usr/bin/env python3
"""Almacenar registros con mmap."""
import mmap
import struct
import os

ARCHIVO = "/tmp/registros.bin"
NUM_REGISTROS = 5
FORMATO = 'i f 20s'
TAM_REG = struct.calcsize(FORMATO)
TAMAÑO = NUM_REGISTROS * TAM_REG

#  Crear archivo con tamaño fijo
with open(ARCHIVO, "wb") as f:
    f.write(b'\x00' * TAMAÑO)

with open(ARCHIVO, "r+b") as f:
    mm = mmap.mmap(f.fileno(), TAMAÑO)

    # Escribir registros
    print("=== Escribiendo registros ===")

    datos = [
        (1, 8.5, "Ana"),
        (2, 7.0, "Luis"),
        (3, 9.2, "Maria"),
        (4, 6.8, "Pedro"),
        (5, 10.0, "Sofia")
    ]

    for i, (id_, nota, nombre) in enumerate(datos):
        offset = i * TAM_REG

        # convertir nombre a bytes y rellenar a 20 bytes
        nombre_bytes = nombre.encode().ljust(20, b'\x00')

        struct.pack_into(FORMATO, mm, offset, id_, nota, nombre_bytes)

        print(f"Registro {i}: id={id_}, nota={nota}, nombre={nombre}")

    #  Leer registros
    print("\n=== Leyendo registros ===")

    for i in range(NUM_REGISTROS):
        offset = i * TAM_REG

        id_, nota, nombre_bytes = struct.unpack_from(FORMATO, mm, offset)

        # limpiar los \x00 del nombre
        nombre = nombre_bytes.rstrip(b'\x00').decode()

        print(f"Registro {i}: id={id_}, nota={nota}, nombre={nombre}")

    mm.close()

# (opcional) borrar archivo
os.unlink(ARCHIVO)