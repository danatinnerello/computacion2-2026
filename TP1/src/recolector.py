from time import sleep, time
import queue as _queue_mod

from procfs import (
    obtener_pids,
    leer_cpu_global,
    leer_meminfo,
    leer_stat,
    leer_status,
    leer_cmdline,
    leer_fds,
    leer_loadavg,
    leer_uptime,
    obtener_usuario,
)
from analizadores.cpu import calcular_cpu


def recolectar():
    snapshot = {
        "timestamp": time(),
        "cpu": leer_cpu_global(),
        "memoria": leer_meminfo(),
        "loadavg": leer_loadavg(),
    }

    uptime, boot_time = leer_uptime()
    snapshot["uptime"] = uptime
    snapshot["boot_time"] = boot_time
    snapshot["procesos"] = {}

    for pid in obtener_pids():
        try:
            status = leer_status(pid)
            uid = status.get("Uid", "0").split()[0]
            snapshot["procesos"][pid] = {
                "stat": leer_stat(pid),
                "status": status,
                "cmdline": leer_cmdline(pid),
                "fds": leer_fds(pid),
                "usuario": obtener_usuario(uid),
            }
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass

    return snapshot


def recolector_loop(colas_analizadores):
    """Proceso recolector: lee /proc y REPARTE el snapshot crudo a los 7
    analizadores por sus propias Queue (no escribe en el Manager.dict; ese
    es trabajo exclusivo del agregador). Usamos una cola por analizador
    porque una Queue normal solo entrega cada item a UN consumidor, y acá
    los 7 necesitan la misma foto del sistema."""
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior_snapshot = None

    while True:
        nuevo_snapshot = recolectar()

        if anterior_snapshot is not None:
            nuevo_snapshot["cpu_pct"] = calcular_cpu(anterior_snapshot, nuevo_snapshot)
        else:
            nuevo_snapshot["cpu_pct"] = {}

        for cola in colas_analizadores.values():
            try:
                cola.put_nowait(nuevo_snapshot)
            except _queue_mod.Full:
                # El analizador todavía no consumió el anterior; descartamos
                # la muestra más antigua para conservar siempre la más reciente.
                try:
                    cola.get_nowait()
                except _queue_mod.Empty:
                    pass
                try:
                    cola.put_nowait(nuevo_snapshot)
                except _queue_mod.Full:
                    pass

        anterior_snapshot = nuevo_snapshot
        sleep(1)