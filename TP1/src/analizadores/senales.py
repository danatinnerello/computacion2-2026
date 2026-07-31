from time import sleep, time

SIGNALS = {
    1: "SIGHUP",
    2: "SIGINT",
    3: "SIGQUIT",
    9: "SIGKILL",
    10: "SIGUSR1",
    12: "SIGUSR2",
    15: "SIGTERM",
    17: "SIGCHLD",
    18: "SIGCONT",
    19: "SIGSTOP"
}


def decodificar_mascara(hex_mask):
    try:
        valor = int(hex_mask, 16)
    except Exception:
        return []
    resultado = []
    for numero, nombre in SIGNALS.items():
        bit = numero - 1
        if valor & (1 << bit):
            resultado.append(nombre)
    return resultado


def analizar(snapshot):
    procesos = []
    for pid, info in snapshot["procesos"].items():
        status = info["status"]
        procesos.append({
            "pid": pid,
            "comando": info["cmdline"] or info["stat"]["comm"],
            "SigPnd": decodificar_mascara(status.get("SigPnd", "0")),
            "SigBlk": decodificar_mascara(status.get("SigBlk", "0")),
            "SigIgn": decodificar_mascara(status.get("SigIgn", "0")),
            "SigCgt": decodificar_mascara(status.get("SigCgt", "0")),
            "ShdPnd": decodificar_mascara(status.get("ShdPnd", "0")),
        })
    return procesos


def proceso_senales(snapshot_compartido, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        if "snapshot" in snapshot_compartido:
            resultado = analizar(snapshot_compartido["snapshot"])
            snapshot_compartido["senales"] = {"datos": resultado, "ts": time()}

        sleep(intervalos.get("senales", 10))