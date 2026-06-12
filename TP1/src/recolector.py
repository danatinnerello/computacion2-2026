# src/recolector.py

from procfs import (
    obtener_pids,
    leer_cpu_global,
    leer_meminfo,
    leer_stat,
)

def recolectar():
    snapshot = {
        "cpu": leer_cpu_global(),
        "memoria": leer_meminfo(),
        "procesos": {}
    }

    for pid in obtener_pids():
        try:
            snapshot["procesos"][pid] = leer_stat(pid)
        except (FileNotFoundError, ProcessLookupError):
            pass

    return snapshot