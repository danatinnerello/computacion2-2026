import signal
import threading
import time

def manejador(sig, frame):
    print(f"Señal recibida en thread {threading.current_thread().name}")

signal.signal(signal.SIGINT, manejador)

def worker():
    while True:
        print(f"Worker {threading.current_thread().name} trabajando")
        time.sleep(1)

# Crear threads
threads = []
for i in range(2):
    t = threading.Thread(target=worker, name=f"Worker-{i}")
    t.daemon = True
    t.start()
    threads.append(t)

print("Threads creados. Ctrl+C para enviar señal.")
print("Observá que la señal llega al thread principal")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Saliendo...")


'''
import signal
import threading

def thread_sin_signals():
    # Bloquear todas las señales en este thread
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})

    while True:
        print("Thread trabajando (señales bloqueadas)")
        time.sleep(1)
        '''