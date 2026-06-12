def analizar(snapshot):

    mem = snapshot["memoria"]

    total = mem.get("MemTotal", 0)
    libre = mem.get("MemFree", 0)

    usada = total - libre

    porcentaje = 0

    if total > 0:
        porcentaje = round(
            usada * 100 / total,
            2
        )

    return {
        "mem_total": total,
        "mem_libre": libre,
        "mem_usada": usada,
        "mem_pct": porcentaje,
        "procesos": len(snapshot["procesos"])
    }