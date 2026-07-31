from time import sleep, time

from procfs import resumir_segmentos


def kb(valor):
    try:
        return int(valor.split()[0])
    except (ValueError, IndexError):
        return 0


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        status = info["status"]
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "usuario": info.get("usuario", "?"),
            "VmSize": status.get("VmSize", "0 kB"),
            "VmRSS": status.get("VmRSS", "0 kB"),
            "VmData": status.get("VmData", "0 kB"),
            "VmStk": status.get("VmStk", "0 kB"),
            "VmExe": status.get("VmExe", "0 kB"),
            "VmLib": status.get("VmLib", "0 kB"),
            "VmHWM": status.get("VmHWM", "0 kB"),
            "VmSwap": status.get("VmSwap", "0 kB"),
            "minflt": info["stat"].get("minflt", 0),
            "majflt": info["stat"].get("majflt", 0),
            "segmentos": resumir_segmentos(pid),
        })

    procesos.sort(key=lambda p: kb(p["VmRSS"]), reverse=True)
    return procesos


def proceso_memoria(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        if "snapshot" in snapshot_compartido:
            resultado = analizar(snapshot_compartido["snapshot"])
            snapshot_compartido["memoria"] = {"datos": resultado, "ts": time()}

        sleep(intervalos.get("memoria", 3))