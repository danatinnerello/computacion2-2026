def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        status = info["status"]

        proceso = {
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "SigPnd": status.get("SigPnd", "0"),
            "ShdPnd": status.get("ShdPnd", "0"),
            "SigBlk": status.get("SigBlk", "0"),
            "SigIgn": status.get("SigIgn", "0"),
            "SigCgt": status.get("SigCgt", "0")
        }

        procesos.append(proceso)

    return procesos