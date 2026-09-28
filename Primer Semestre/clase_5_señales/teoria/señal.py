'''
import signal
import time

def mi_manejador(signum, frame):
    """Esta función se ejecuta cuando llega la señal."""
    print(f"\n¡Recibí la señal {signum}!")
    print("Pero voy a seguir ejecutando...")

# Registrar el manejador para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, mi_manejador)

print("Presioná Ctrl+C para enviar SIGINT")
print("El programa no terminará porque tenemos un manejador")

while True:
    print(".", end="", flush=True)
    time.sleep(1)

'''

'''
import signal

# Ver todas las señales disponibles
for name in dir(signal):
    if name.startswith("SIG") and not name.startswith("SIG_"):
        signum = getattr(signal, name)
        if isinstance(signum, int):
            print(f"{name:12} = {signum}")


'''

import os
import signal

# Enviar señal a un proceso específico
os.kill(pid, signal.SIGTERM)

# Enviar señal a un grupo de procesos
os.killpg(pgid, signal.SIGTERM)

# Enviarse una señal a sí mismo
os.kill(os.getpid(), signal.SIGUSR1)

# También existe signal.raise_signal (Python 3.8+)
signal.raise_signal(signal.SIGUSR1)