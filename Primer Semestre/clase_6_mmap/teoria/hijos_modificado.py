#!/usr/bin/env python3
"""Hijos calculan sumas parciales usando mmap."""
import mmap
import os
import struct

NUM_HIJOS = 4
TAMAÑO_POR_HIJO = 64
TAMAÑO_TOTAL = NUM_HIJOS * TAMAÑO_POR_HIJO

mm = mmap.mmap(-1, TAMAÑO_TOTAL)

hijos = []

RANGO = 25  # cada hijo suma 25 números

for i in range(NUM_HIJOS):
    pid = os.fork()

    if pid == 0:
        offset = i * TAMAÑO_POR_HIJO

        # calcular rango
        inicio = i * RANGO + 1
        fin = (i + 1) * RANGO

        suma = sum(range(inicio, fin + 1))

        # escribir datos
        struct.pack_into('i', mm, offset, i)                 # id
        struct.pack_into('i', mm, offset + 4, os.getpid())   # pid
        struct.pack_into('i', mm, offset + 8, suma)          # resultado

        os._exit(0)

    else:
        hijos.append(pid)

# Padre espera
for pid in hijos:
    os.waitpid(pid, 0)

# Leer resultados
print("=== Resultados parciales ===")
suma_total = 0

for i in range(NUM_HIJOS):
    offset = i * TAMAÑO_POR_HIJO

    hijo_id = struct.unpack_from('i', mm, offset)[0]
    hijo_pid = struct.unpack_from('i', mm, offset + 4)[0]
    suma = struct.unpack_from('i', mm, offset + 8)[0]

    suma_total += suma

    print(f"Hijo {hijo_id} (PID {hijo_pid}) sumó: {suma}")

print(f"\n=== Suma total === {suma_total}")

mm.close()
