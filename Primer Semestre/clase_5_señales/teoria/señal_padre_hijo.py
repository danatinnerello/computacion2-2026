import os
import signal
import time

pid = os.fork()

if pid == 0:
    # Hijo
    def manejador(sig, frame):
        print(f"[HIJO] Recibí señal {sig}")

    signal.signal(signal.SIGUSR1, manejador)

    print(f"[HIJO] PID {os.getpid()}, esperando señales...")
    while True:
        signal.pause()  # Esperar hasta recibir una señal

else:
    # Padre
    time.sleep(1)  # Dar tiempo al hijo de configurar su manejador

    print(f"[PADRE] Enviando SIGUSR1 al hijo {pid}")
    os.kill(pid, signal.SIGUSR1)

    time.sleep(1)

    print(f"[PADRE] Enviando SIGTERM al hijo")
    os.kill(pid, signal.SIGTERM)

    os.wait()
    print("[PADRE] Hijo terminado")