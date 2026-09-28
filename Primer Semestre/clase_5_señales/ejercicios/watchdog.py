import subprocess
import sys
import time

def run_watchdog(command):
    while True:
        print(f"[WATCHDOG] Iniciando proceso: {' '.join(command)}")
        
        try:
            # Lanza el proceso hijo
            process = subprocess.Popen(command)

            # Espera a que termine
            return_code = process.wait()

            print(f"[WATCHDOG] El proceso terminó con código {return_code}")

        except Exception as e:
            print(f"[WATCHDOG] Error al ejecutar el proceso: {e}")

        print("[WATCHDOG] Reiniciando en 2 segundos...\n")
        time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python watchdog.py <comando> [args...]")
        sys.exit(1)

    command = sys.argv[1:]
    run_watchdog(command)