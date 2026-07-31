from time import time

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