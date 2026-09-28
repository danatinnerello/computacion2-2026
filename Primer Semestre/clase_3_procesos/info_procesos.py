#!/usr/bin/env python3
import os
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <PID>")
        sys.exit(1)

    pid = sys.argv[1]
    base = f"/proc/{pid}"

    if not os.path.exists(base):
        print("PID no existe")
        sys.exit(1)

    # cmdline
    try:
        with open(f"{base}/cmdline") as f:
            cmd = f.read().replace('\x00', ' ')
            print(f"Comando: {cmd}")
    except:
        print("No se pudo leer cmdline")

    # status
    print("\nStatus:")
    try:
        with open(f"{base}/status") as f:
            for linea in f:
                if any(k in linea for k in ["Name", "State", "VmSize"]):
                    print(linea.strip())
    except:
        print("No se pudo leer status")

    # file descriptors
    print("\nFile descriptors abiertos:")
    try:
        fds = os.listdir(f"{base}/fd")
        for fd in fds:
            ruta = os.readlink(f"{base}/fd/{fd}")
            print(f"{fd} -> {ruta}")
    except:
        print("No se pudo leer fd")

if __name__ == "__main__":
    main()