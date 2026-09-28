'''
import signal

class TimeoutError(Exception):
    pass

def timeout_handler(sig, frame):
    raise TimeoutError("Operación excedió el tiempo límite")

def con_timeout(funcion, timeout_segundos, *args, **kwargs):
    """Ejecuta una función con timeout."""
    # Guardar manejador anterior
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)

    # Programar alarma
    signal.alarm(timeout_segundos)

    try:
        resultado = funcion(*args, **kwargs)
    finally:
        # Cancelar alarma y restaurar manejador
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

    return resultado

# Uso
def operacion_lenta():
    import time
    print("Iniciando operación lenta...")
    time.sleep(10)
    return "completado"

try:
    resultado = con_timeout(operacion_lenta, 3)
    print(f"Resultado: {resultado}")
except TimeoutError as e:
    print(f"Timeout: {e}")

'''

import signal
import time

contador = 0

def alarma_periodica(sig, frame):
    global contador
    contador += 1
    print(f"Tick #{contador}")

signal.signal(signal.SIGALRM, alarma_periodica)

# setitimer(ITIMER_REAL, interval, initial)
# Dispara cada 0.5 segundos, empezando en 0.5 segundos
signal.setitimer(signal.ITIMER_REAL, 0.5, 0.5)

print("Alarma configurada cada 0.5 segundos")
print("Presioná Ctrl+C para salir")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    signal.setitimer(signal.ITIMER_REAL, 0)  # Cancelar timer
    print(f"\nTerminando. Total de ticks: {contador}")