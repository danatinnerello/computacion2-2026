#!/usr/bin/env python3
"""
Ejecutor de comandos en paralelo.
Uso: python3 paralelo.py "cmd1" "cmd2" ...
"""
import os
import sys
import time

def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} comando1 [comando2 ...]")
        sys.exit(1)

    comandos = sys.argv[1:]
    procesos = {}  # pid -> comando

    inicio = time.time()

    # Crear procesos hijos
    for cmd in comandos:
        pid = os.fork()

        if pid == 0:
            # PROCESO HIJO
            partes = cmd.split()
            try:
                os.execvp(partes[0], partes)
            except Exception as e:
                print(f"Error ejecutando {cmd}: {e}")
                os._exit(1)
        else:
            # PROCESO PADRE
            procesos[pid] = cmd
            print(f"[{pid}] Iniciado: {cmd}")

    # Esperar a que terminen todos
    exitosos = 0
    fallidos = 0

    while procesos:
        pid, status = os.wait()

        codigo = os.WEXITSTATUS(status)
        cmd = procesos.pop(pid)

        print(f"[{pid}] Terminado: {cmd} (código: {codigo})")

        if codigo == 0:
            exitosos += 1
        else:
            fallidos += 1

    fin = time.time()
    total = fin - inicio

    # Resumen final
    print("\nResumen:")
    print(f"- Comandos ejecutados: {len(comandos)}")
    print(f"- Exitosos: {exitosos}")
    print(f"- Fallidos: {fallidos}")
    print(f"- Tiempo total: {total:.2f}s")


if __name__ == "__main__":
    main()


#mas control sobre los procesos
#mas compleja y propensa a errores (olvidar esperar, manejo de zombies, etc)
