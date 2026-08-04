from collections import Counter
from time import sleep, time


def porcentaje(delta_campo, delta_total):
    # % de CPU = variación de ESTE campo sobre la variación TOTAL de jiffies,
    # no sobre el valor anterior del campo (eso daba un número sin sentido).
    if delta_total <= 0:
        return 0.0
    return round(delta_campo * 100.0 / delta_total, 2)


def analizar(snapshot, anterior):
    datos = {}
    cpu = snapshot["cpu"]
    if anterior and "cpu" in anterior:
        delta_total = sum(cpu.values()) - sum(anterior["cpu"].values())
        datos["cpu_user"] = porcentaje(cpu["user"] - anterior["cpu"]["user"], delta_total)
        datos["cpu_system"] = porcentaje(cpu["system"] - anterior["cpu"]["system"], delta_total)
        datos["cpu_idle"] = porcentaje(cpu["idle"] - anterior["cpu"]["idle"], delta_total)
        datos["cpu_iowait"] = porcentaje(cpu["iowait"] - anterior["cpu"]["iowait"], delta_total)
    else:
        datos["cpu_user"] = datos["cpu_system"] = datos["cpu_idle"] = datos["cpu_iowait"] = 0.0

    datos["loadavg"] = snapshot.get("loadavg", {})
    datos["uptime"] = round(snapshot.get("uptime", 0), 2)
    datos["mem_total"] = snapshot["memoria"].get("MemTotal", 0)
    datos["mem_libre"] = snapshot["memoria"].get("MemFree", 0)
    datos["mem_available"] = snapshot["memoria"].get("MemAvailable", 0)
    datos["mem_buffers"] = snapshot["memoria"].get("Buffers", 0)
    datos["mem_cached"] = snapshot["memoria"].get("Cached", 0)
    datos["swap_total"] = snapshot["memoria"].get("SwapTotal", 0)
    datos["swap_libre"] = snapshot["memoria"].get("SwapFree", 0)
    datos["mem_pct"] = round(
        (datos["mem_total"] - datos["mem_libre"]) * 100 / datos["mem_total"],
        2
    ) if datos["mem_total"] else 0.0
    datos["boot_time"] = snapshot.get("boot_time", 0)

    estados = Counter()
    zombies = 0
    for info in snapshot["procesos"].values():
        estado = info["stat"]["state"]
        estados[estado] += 1
        if estado == "Z":
            zombies += 1

    datos["procesos"] = len(snapshot["procesos"])
    datos["threads_total"] = sum(
        int(info.get("stat", {}).get("num_threads", 0) or 0)
        for info in snapshot["procesos"].values()
    )
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

    top_mem = []
    for pid, info in snapshot["procesos"].items():
        try:
            rss_kb = int(info["status"].get("VmRSS", "0 kB").split()[0])
        except (ValueError, IndexError):
            rss_kb = 0
        top_mem.append({
            "pid": pid,
            "rss_kb": rss_kb,
            "comando": info["cmdline"] or info["stat"]["comm"],
        })

    top_mem.sort(key=lambda p: p["rss_kb"], reverse=True)
    datos["top_mem"] = top_mem[:5]

    return datos


def proceso_sistema(cola_entrada, cola_resultados, intervalos):
    import signal

    from shared import recibir_ultimo

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior = None
    while True:
        intervalo = intervalos.get("sistema", 2)
        actual = recibir_ultimo(cola_entrada, timeout=intervalo)
        if actual is not None:
            datos = analizar(actual, anterior)
            cola_resultados.put(("sistema", datos, time()))
            anterior = actual

        sleep(intervalo)