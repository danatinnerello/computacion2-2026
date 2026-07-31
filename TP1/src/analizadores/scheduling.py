from time import sleep, time


def policy_name(policy):
    if policy == 0:
        return "OTHER"
    if policy == 1:
        return "FIFO"
    if policy == 2:
        return "RR"
    if policy == 3:
        return "BATCH"
    if policy == 5:
        return "IDLE"
    return str(policy)


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        stat = info["stat"]
        status = info["status"]
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or stat["comm"],
            "priority": stat.get("priority", "?"),
            "nice": stat.get("nice", "?"),
            "policy": policy_name(stat.get("policy", -1)),
            "rt_priority": status.get("Rt_priority", "?"),
            "pgid": stat.get("pgrp", "?"),
            "sid": stat.get("session", "?"),
            "cpus": status.get("Cpus_allowed_list", "-"),
            "voluntary": status.get("voluntary_ctxt_switches", "0"),
            "nonvoluntary": status.get("nonvoluntary_ctxt_switches", "0"),
            "utime": stat.get("utime", 0),
            "stime": stat.get("stime", 0),
        })
    return procesos


def proceso_scheduling(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        if "snapshot" in snapshot_compartido:
            resultado = analizar(snapshot_compartido["snapshot"])
            snapshot_compartido["scheduling"] = {"datos": resultado, "ts": time()}

        sleep(intervalos.get("scheduling", 10))