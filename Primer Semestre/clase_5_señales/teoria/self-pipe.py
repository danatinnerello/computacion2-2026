import os
import signal
import select

# Crear pipe para notificaciones de señales
signal_read, signal_write = os.pipe()

# Hacer write non-blocking
import fcntl
flags = fcntl.fcntl(signal_write, fcntl.F_GETFL)
fcntl.fcntl(signal_write, fcntl.F_SETFL, flags | os.O_NONBLOCK)

def manejador(sig, frame):
    # Solo escribir un byte al pipe (async-signal-safe)
    try:
        os.write(signal_write, b"x")
    except BlockingIOError:
        pass  # Pipe lleno, no importa

signal.signal(signal.SIGINT, manejador)
signal.signal(signal.SIGTERM, manejador)

print("Esperando señales o eventos...")
print(f"PID: {os.getpid()}")

while True:
    # select espera en el pipe (y otros fds si los hubiera)
    readable, _, _ = select.select([signal_read], [], [], 1.0)

    if signal_read in readable:
        os.read(signal_read, 1024)  # Consumir los bytes
        print("Señal detectada! Procesando de forma segura...")
        break

    print("Tick...")

print("Terminando limpiamente")