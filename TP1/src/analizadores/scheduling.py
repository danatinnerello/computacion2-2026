def analizar(snapshot):

    procesos = []

    for pid, info in snapshot["procesos"].items():

        status = info["status"]

        proceso = {
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "cpus": status.get(
                "Cpus_allowed_list",
                "-"
            ),
            "voluntary": status.get(
                "voluntary_ctxt_switches",
                "0"
            ),
            "nonvoluntary": status.get(
                "nonvoluntary_ctxt_switches",
                "0"
            )
        }

        procesos.append(proceso)

    return procesos