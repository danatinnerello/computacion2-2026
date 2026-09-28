import mmap
import os
import struct
import time

# Crear región compartida: un entero de 4 bytes
TAMAÑO = 4
mm = mmap.mmap(-1, TAMAÑO)

pid = os.fork()

if pid == 0:
    # === HIJO ===
    # Incrementar el valor 5 veces
    for i in range(5):
        mm.seek(0)
        valor_actual = struct.unpack('i', mm.read(4))[0]
        nuevo_valor = valor_actual + 1
        mm.seek(0)
        mm.write(struct.pack('i', nuevo_valor))
        print(f"[HIJO] Valor incrementado a: {nuevo_valor}")
        time.sleep(0.5)
    os._exit(0)

else:
    # === PADRE ===
    os.wait()
    mm.seek(0)
    valor_final = struct.unpack('i', mm.read(4))[0]
    print(f"[PADRE] Valor final: {valor_final}")  # 5
    mm.close()