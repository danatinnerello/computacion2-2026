from time import sleep, time

from shared import recibir_ultimo

SIGNALS = {
    1: "SIGHUP", 2: "SIGINT", 3: "SIGQUIT", 4: "SIGILL",
    5: "SIGTRAP", 6: "SIGABRT", 7: "SIGBUS", 8: "SIGFPE",
    9: "SIGKILL", 10: "SIGUSR1", 11: "SIGSEGV", 12: "SIGUSR2",
    13: "SIGPIPE", 14: "SIGALRM", 15: "SIGTERM", 16: "SIGSTKFLT",
    17: "SIGCHLD", 18: "SIGCONT", 19: "SIGSTOP", 20: "SIGTSTP",
    21: "SIGTTIN", 22: "SIGTTOU", 23: "SIGURG", 24: "SIGXCPU",
    25: "SIGXFSZ", 26: "SIGVTALRM", 27: "SIGPROF", 28: "SIGWINCH",
    29: "SIGIO", 30: "SIGPWR", 31: "SIGSYS",
}
# Señales de tiempo real: 34 a 64 (Linux define SIGRTMIN=34..SIGRTMAX=64)
for _n in range(34, 65):
    SIGNALS[_n] = f"SIGRTMIN+{_n - 34}" if _n > 34 else "SIGRTMIN"


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


def proceso_senales(cola_entrada, cola_resultados, intervalos):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        intervalo = intervalos.get("senales", 10)
        actual = recibir_ultimo(cola_entrada, timeout=intervalo)
        if actual is not None:
            resultado = analizar(actual)
            cola_resultados.put(("senales", resultado, time()))

        sleep(intervalo)