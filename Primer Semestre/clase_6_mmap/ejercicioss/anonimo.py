import mmap
import os

# Crear mmap anónimo de 1024 bytes
# tagname="" y fileno=-1 indican que es anónimo
mm = mmap.mmap(-1, 1024)

pid = os.fork()

if pid == 0:
    # Hijo
    mm.seek(0)
    mm.write(b"Mensaje del hijo!")
    os._exit(0)
else:
    # Padre
    os.wait()
    mm.seek(0)
    datos = mm.read(17)
    print(f"El padre leyó: {datos}")  # b'Mensaje del hijo!'
    mm.close()