from time import sleep, time

from procfs import leer_threads


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        threads = leer_threads(pid)
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "cantidad": len(threads),
            "cpu_pct": snapshot.get("cpu_pct", {}).get(pid, 0.0),
            "threads": sorted(threads, key=lambda t: t["cpu"], reverse=True),
        })

    procesos.sort(key=lambda p: p["cantidad"], reverse=True)
    return procesos


def proceso_threads(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        if "snapshot" in snapshot_compartido:
            resultado = analizar(snapshot_compartido["snapshot"])
            snapshot_compartido["threads"] = {"datos": resultado, "ts": time()}

        sleep(intervalos.get("threads", 2))