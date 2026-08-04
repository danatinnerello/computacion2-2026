from time import sleep, time

from procfs import leer_threads
from shared import recibir_ultimo


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
        try:
            rss_kb = int(status.get("VmRSS", "0 kB").split()[0])
        except (ValueError, IndexError):
            rss_kb = 0

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
            "rss_kb": rss_kb,
        })

    procesos.sort(key=lambda p: p["cpu_pct"], reverse=True)
    return procesos


def proceso_resumen(cola_entrada, cola_resultados, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior = None

    while True:
        intervalo = intervalos.get("resumen", 2)
        actual = recibir_ultimo(cola_entrada, timeout=intervalo)
        if actual is not None:
            resultado = analizar(actual, anterior)
            cola_resultados.put(("resumen", resultado, time()))
            anterior = actual

        sleep(intervalo)