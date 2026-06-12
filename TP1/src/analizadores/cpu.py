def calcular_cpu(snapshot_anterior, snapshot_actual):

    cpu_total_anterior = sum(
        snapshot_anterior["cpu"].values()
    )

    cpu_total_actual = sum(
        snapshot_actual["cpu"].values()
    )

    delta_cpu_total = (
        cpu_total_actual -
        cpu_total_anterior
    )

    resultados = {}

    for pid, proc_actual in snapshot_actual["procesos"].items():

        if pid not in snapshot_anterior["procesos"]:
            continue

        proc_anterior = snapshot_anterior["procesos"][pid]

        tiempo_actual = (
            proc_actual["stat"]["utime"] +
            proc_actual["stat"]["stime"]
        )

        tiempo_anterior = (
            proc_anterior["stat"]["utime"] +
            proc_anterior["stat"]["stime"]
        )

        delta_proceso = (
            tiempo_actual -
            tiempo_anterior
        )

        cpu_pct = 0.0

        if delta_cpu_total > 0:
            cpu_pct = (
                delta_proceso /
                delta_cpu_total
            ) * 100

        resultados[pid] = round(cpu_pct, 2)

    return resultados