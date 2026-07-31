import copy
from time import sleep, time

from procfs import leer_threads


def analizar(snapshot, anterior):
    procesos = []
    anterior_procs = anterior.get("procesos", {}) if anterior else {}

    for pid, info in snapshot["procesos"].items():
        stat = info["stat"]
        status = info["status"]
        previous = anterior_procs.get(pid)
        cpu_jiffies = 0
        if previous:
            cpu_jiffies = (stat["utime"] + stat["stime"]) - (
                previous["stat"]["utime"] + previous["stat"]["stime"]
            )

        threads = leer_threads(pid)
        procesos.append({
            "pid": pid,
            "ppid": status.get("PPid", "?"),
            "uid": status.get("Uid", "?").split()[0],
            "gid": status.get("Gid", "?").split()[0],
            "usuario": info.get("usuario", "?"),
            "estado": stat["state"],
            "threads": len(threads),
            "comando": info["cmdline"] or stat["comm"],
            "cpu_jiffies": cpu_jiffies,
            "cpu_pct": snapshot.get("cpu_pct", {}).get(pid, 0.0),
        })

    procesos.sort(key=lambda p: p["cpu_pct"], reverse=True)
    return procesos


def proceso_resumen(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior = None

    while True:
        if "snapshot" in snapshot_compartido:
            actual = copy.deepcopy(snapshot_compartido["snapshot"])
            resultado = analizar(actual, anterior)
            snapshot_compartido["resumen"] = {"datos": resultado, "ts": time()}
            anterior = actual

        sleep(intervalos.get("resumen", 2))