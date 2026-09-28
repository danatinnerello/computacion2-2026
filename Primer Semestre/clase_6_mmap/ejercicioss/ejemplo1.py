import os 
import time 

v = 5
pid = os.fork()

if pid == 0:
    v = 3
    print(f"Soy el hijo, mi PID es {os.getpid()} , el valor de v es {v} id: {id(v)}")

else:
    os.wait()
    print(f"mi PID es {os.getpid()}, y el valor de v es {v} id: {id(v)} ") 
    

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



