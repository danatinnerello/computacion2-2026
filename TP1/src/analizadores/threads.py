def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        status = info["status"]

        proceso = {
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "threads": int(
                status.get("Threads", "0")
            )
        }

        procesos.append(proceso)

    procesos.sort(
        key=lambda p: p["threads"],
        reverse=True
    )

    return procesos