import mmap
import os

# Crear un archivo con tamaño fijo
ruta = "/tmp/mi_mmap.bin"
tamaño = 1024  # 1 KB

with open(ruta, "wb") as f:
    f.write(b'\x00' * tamaño)  # Llenar con ceros

# Ahora sí, mapearlo
with open(ruta, "r+b") as f:
    mm = mmap.mmap(f.fileno(), tamaño)

    # Escribir datos
    mm[0:12] = b"Hola, mmap! "

    # Leer datos
    mm.seek(0)
    print(mm.read(12))  # b'Hola, mmap!'

    mm.close()

# Limpiar
os.unlink(ruta)