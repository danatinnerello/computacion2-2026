# src/agregador.py
import signal


def proceso_agregador(cola_resultados, snapshot_compartido):
    """Único proceso que escribe en el Manager.dict del snapshot global.
    Los 7 analizadores nunca tocan snapshot_compartido directamente: le
    mandan su resultado por cola_resultados. Al ser un solo escritor,
    no hay race condition posible sobre snapshot_compartido (no hace falta
    Lock explícito: multiprocessing.Manager ya serializa cada operación
    individual, y acá además nunca hay dos procesos escribiendo la misma
    clave a la vez)."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        vista, datos, ts = cola_resultados.get()  # bloquea hasta que llegue algo
        snapshot_compartido[vista] = {"datos": datos, "ts": ts}