#!/usr/bin/env python3
"""Proceso que lee de memoria compartida via archivo."""
import mmap
import struct
import time

ARCHIVO = "/tmp/compartido.bin"
TAMAÑO = 256

with open(ARCHIVO, "r+b") as f:
    mm = mmap.mmap(f.fileno(), TAMAÑO)

    ultimo = ""
    for _ in range(15):
        mm.seek(0)
        largo = struct.unpack('i', mm.read(4))[0]
        if largo > 0:
            mensaje = mm.read(largo).decode()
            if mensaje != ultimo:
                print(f"[LECTOR] Leí: {mensaje}")
                ultimo = mensaje
        time.sleep(0.5)

    mm.close()