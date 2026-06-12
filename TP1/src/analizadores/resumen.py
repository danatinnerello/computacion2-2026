def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        stat = info["stat"]
        status = info["status"]

        proceso = {
            "pid": pid,
            "ppid": status.get("PPid", "?"),
            "uid": status.get("Uid", "?").split()[0],
            "gid": status.get("Gid", "?").split()[0],
            "estado": stat["state"],
            "threads": status.get("Threads", "0"),
            "comando": info["cmdline"] or stat["comm"]
        }

        procesos.append(proceso)

    return procesos