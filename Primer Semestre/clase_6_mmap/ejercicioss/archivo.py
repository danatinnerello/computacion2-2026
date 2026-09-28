import mmap

# Abrir un archivo existente
with open("datos.txt", "r+b") as f:
    # Mapear todo el archivo a memoria
    mm = mmap.mmap(f.fileno(), 0)  # 0 = mapear todo el archivo

    # Leer como si fuera un archivo
    print(mm.readline())

    # Acceder como si fuera un array de bytes
    print(mm[0:10])

    # Modificar directamente
    mm[0:5] = b"HOLA!"

    # Los cambios se escriben al archivo
    mm.flush()
    mm.close()


#parametros importantes

with open("datos.bin", "r+b") as f:
    mm = mmap.mmap(
        f.fileno(),        # File descriptor
        0,                 # Tamaño (0 = todo el archivo)
        access=mmap.ACCESS_WRITE,  # Permisos
        offset=0           # Desde dónde empezar a mapear
    )