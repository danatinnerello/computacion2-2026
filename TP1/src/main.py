# src/main.py

from procfs import *

print("Primeros 10 PIDs:")
print(obtener_pids()[:10])

print("\nMemoria:")
mem = leer_meminfo()
print(f"MemTotal: {mem['MemTotal']} kB")
print(f"MemFree : {mem['MemFree']} kB")

print("\nCPU:")
print(leer_cpu_global())

pid = obtener_pids()[0]

print(f"\nProceso {pid}")
print(leer_stat(pid))

print("\nStatus:")
print(leer_status(pid)["Name"])

print("\nCmdline:")
print(leer_cmdline(pid))