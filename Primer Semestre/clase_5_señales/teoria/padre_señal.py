import os
import signal
import time

hijos_terminados = []

def manejador_sigchld(sig, frame):
    """Recoge hijos terminados de forma no bloqueante."""
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break  # No hay más hijos terminados
            codigo = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1
            hijos_terminados.append((pid, codigo))
            print(f"[SIGCHLD] Hijo {pid} terminó con código {codigo}")
        except ChildProcessError:
            break  # No hay hijos

signal.signal(signal.SIGCHLD, manejador_sigchld)

# Crear varios hijos que terminan en diferentes momentos
for i in range(3):
    pid = os.fork()
    if pid == 0:
        time.sleep(i + 1)  # Cada hijo duerme diferente tiempo
        print(f"[HIJO {i}] Terminando...")
        os._exit(i)

# El padre hace otras cosas mientras los hijos trabajan
print("[PADRE] Haciendo trabajo...")
for _ in range(5):
    print(f"[PADRE] Hijos terminados hasta ahora: {len(hijos_terminados)}")
    time.sleep(1)

print(f"[PADRE] Resumen final: {hijos_terminados}")