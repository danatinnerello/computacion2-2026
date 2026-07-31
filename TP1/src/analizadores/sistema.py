from collections import Counter
from time import sleep, time


def porcentaje(actual, anterior):
    delta = actual - anterior
    if anterior == 0:
        return 0.0
    return round(delta * 100.0 / anterior, 2)


def analizar(snapshot, anterior):
    datos = {}
    cpu = snapshot["cpu"]
    if anterior and "cpu" in anterior:
        total = sum(cpu.values())
        total_prev = sum(anterior["cpu"].values())
        datos["cpu_user"] = porcentaje(cpu["user"], anterior["cpu"]["user"])
        datos["cpu_system"] = porcentaje(cpu["system"], anterior["cpu"]["system"])
        datos["cpu_idle"] = porcentaje(cpu["idle"], anterior["cpu"]["idle"])
        datos["cpu_iowait"] = porcentaje(cpu["iowait"], anterior["cpu"]["iowait"])
    else:
        datos["cpu_user"] = datos["cpu_system"] = datos["cpu_idle"] = datos["cpu_iowait"] = 0.0

    datos["loadavg"] = snapshot.get("loadavg", {})
    datos["uptime"] = round(snapshot.get("uptime", 0), 2)
    datos["mem_total"] = snapshot["memoria"].get("MemTotal", 0)
    datos["mem_libre"] = snapshot["memoria"].get("MemFree", 0)
    datos["mem_pct"] = round(
        (datos["mem_total"] - datos["mem_libre"]) * 100 / datos["mem_total"],
        2
    ) if datos["mem_total"] else 0.0

    estados = Counter()
    zombies = 0
    for info in snapshot["procesos"].values():
        estado = info["stat"]["state"]
        estados[estado] += 1
        if estado == "Z":
            zombies += 1

    datos["procesos"] = len(snapshot["procesos"])
    datos["por_estado"] = dict(estados)
    datos["zombies"] = zombies

    cpu_pct_map = snapshot.get("cpu_pct", {})
    top_cpu = []
    for pid, cpu_pct in cpu_pct_map.items():
        info = snapshot["procesos"].get(pid)
        if not info:
            continue
        top_cpu.append({
            "pid": pid,
            "cpu_pct": cpu_pct,
            "comando": info["cmdline"] or info["stat"]["comm"],
        })

    top_cpu.sort(key=lambda p: p["cpu_pct"], reverse=True)
    datos["top_cpu"] = top_cpu[:5]

    return datos


def proceso_sistema(snapshot_compartido, intervalos):
    import copy
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior = None
    while True:
        if "snapshot" in snapshot_compartido:
            actual = copy.deepcopy(snapshot_compartido["snapshot"])
            datos = analizar(actual, anterior)
            snapshot_compartido["sistema"] = {"datos": datos, "ts": time()}
            anterior = actual

        sleep(intervalos.get("sistema", 2))