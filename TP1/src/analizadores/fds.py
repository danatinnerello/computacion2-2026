from time import sleep, time


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "cantidad_fds": len(info["fds"]),
            "fds": info["fds"]
        })

    procesos.sort(key=lambda p: p["cantidad_fds"], reverse=True)
    return procesos


def proceso_fds(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        if "snapshot" in snapshot_compartido:
            resultado = analizar(snapshot_compartido["snapshot"])
            snapshot_compartido["fds"] = {"datos": resultado, "ts": time()}

        sleep(intervalos.get("fds", 5))