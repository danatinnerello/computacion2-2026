from time import sleep, time

from shared import recibir_ultimo


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "cantidad_fds": len(info["fds"]),
            "fds": info["fds"]
        })

    procesos.sort(key=lambda p: p["cantidad_fds"], reverse=True)
    return procesos


def proceso_fds(cola_entrada, cola_resultados, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        intervalo = intervalos.get("fds", 5)
        actual = recibir_ultimo(cola_entrada, timeout=intervalo)
        if actual is not None:
            resultado = analizar(actual)
            cola_resultados.put(("fds", resultado, time()))

        sleep(intervalo)