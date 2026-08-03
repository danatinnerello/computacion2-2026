from time import sleep, time

from procfs import leer_threads


def _delta_cpu_global(cpu_actual, cpu_anterior):
    if not cpu_anterior:
        return 0
    return sum(cpu_actual.values()) - sum(cpu_anterior.values())


def analizar(snapshot, jiffies_anteriores=None, delta_cpu_total=0):
    """jiffies_anteriores: dict {(pid, tid): jiffies} de la lectura previa de
    ESTE analizador (no del snapshot crudo del recolector, que no trae threads).
    Devuelve (procesos, jiffies_actuales) para que el caller los guarde."""
    jiffies_actuales = {}
    procesos = []

    for pid, info in snapshot["procesos"].items():
        threads = leer_threads(pid)
        for t in threads:
            tid = t.get("tid")
            if tid is None:
                continue
            clave = (pid, tid)
            jiffies_actuales[clave] = t["cpu"]
            cpu_previo = jiffies_anteriores.get(clave, t["cpu"])
            delta_thread = t["cpu"] - cpu_previo
            t["cpu_jiffies_delta"] = delta_thread
            t["cpu_pct"] = (
                round(delta_thread * 100.0 / delta_cpu_total, 2)
                if delta_cpu_total > 0 else 0.0
            )

        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "cantidad": len(threads),
            "cpu_pct": snapshot.get("cpu_pct", {}).get(pid, 0.0),
            "threads": sorted(threads, key=lambda t: t["cpu_pct"], reverse=True),
        })

    procesos.sort(key=lambda p: p["cantidad"], reverse=True)
    return procesos, jiffies_actuales


def proceso_threads(cola_entrada, cola_resultados, intervalos):
    import signal

    from shared import recibir_ultimo

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    jiffies_anteriores = {}
    cpu_global_anterior = None

    while True:
        intervalo = intervalos.get("threads", 2)
        snapshot = recibir_ultimo(cola_entrada, timeout=intervalo)
        if snapshot is not None:
            delta_total = _delta_cpu_global(snapshot["cpu"], cpu_global_anterior)

            resultado, jiffies_anteriores = analizar(
                snapshot, jiffies_anteriores, delta_total
            )
            cola_resultados.put(("threads", resultado, time()))
            cpu_global_anterior = snapshot["cpu"]

        sleep(intervalo)