def kb(valor):
    """
    Convierte '1234 kB' -> 1234
    """

    try:
        return int(valor.split()[0])
    except (ValueError, IndexError):
        return 0


def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        status = info["status"]

        proceso = {
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "VmSize": status.get("VmSize", "0 kB"),
            "VmRSS": status.get("VmRSS", "0 kB"),
            "VmData": status.get("VmData", "0 kB"),
            "VmStk": status.get("VmStk", "0 kB"),
            "VmExe": status.get("VmExe", "0 kB"),
            "VmLib": status.get("VmLib", "0 kB"),
            "VmHWM": status.get("VmHWM", "0 kB"),
            "VmSwap": status.get("VmSwap", "0 kB")
        }

        procesos.append(proceso)

    procesos.sort(
        key=lambda p: kb(p["VmRSS"]),
        reverse=True
    )

    return procesos