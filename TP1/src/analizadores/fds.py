def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        proceso = {
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "fds": info["fds"]
        }

        procesos.append(proceso)

    procesos.sort(
        key=lambda p: p["fds"],
        reverse=True
    )

    return procesos