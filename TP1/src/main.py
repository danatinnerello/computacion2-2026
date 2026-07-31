from multiprocessing import Process
from time import sleep, time
import json
from recolector import recolectar

from analizadores.cpu import calcular_cpu
from analizadores.sistema import proceso_sistema
from analizadores.threads import proceso_threads
from analizadores.memoria import proceso_memoria
from analizadores.fds import proceso_fds
from analizadores.senales import proceso_senales
from analizadores.scheduling import proceso_scheduling
from analizadores.resumen import proceso_resumen

from display import run_display
from config import cargar_config
from shared import snapshot, shutdown_manager, intervalos as shared_intervalos

import senales


def recolector_loop(snapshot_compartido):
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    anterior_snapshot = None

    while True:
        nuevo_snapshot = recolectar()

        if anterior_snapshot is not None:
            nuevo_snapshot["cpu_pct"] = calcular_cpu(anterior_snapshot, nuevo_snapshot)
        else:
            nuevo_snapshot["cpu_pct"] = {}

        snapshot_compartido["snapshot"] = nuevo_snapshot
        snapshot_compartido["snapshot_ts"] = time()
        anterior_snapshot = nuevo_snapshot

        sleep(1)


def terminate_process(proc, timeout=0.5):
    if proc is None:
        return

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout)

    if proc.is_alive():
        proc.kill()
        proc.join(timeout)


if __name__ == "__main__":

    senales.registrar_handlers()

    config = cargar_config()
    intervalos = shared_intervalos
    intervalos.update(config)

    p_recolector = Process(
        target=recolector_loop,
        args=(snapshot,)
    )

    p_sistema = Process(
        target=proceso_sistema,
        args=(snapshot, intervalos)
    )

    p_threads = Process(
        target=proceso_threads,
        args=(snapshot, intervalos)
    )

    p_memoria = Process(
        target=proceso_memoria,
        args=(snapshot, intervalos)
    )

    p_fds = Process(
        target=proceso_fds,
        args=(snapshot, intervalos)
    )

    p_senales = Process(
        target=proceso_senales,
        args=(snapshot, intervalos)
    )

    p_scheduling = Process(
        target=proceso_scheduling,
        args=(snapshot, intervalos)
    )

    p_resumen = Process(
        target=proceso_resumen,
        args=(snapshot, intervalos)
    )

    processes = [
        p_recolector,
        p_sistema,
        p_threads,
        p_memoria,
        p_fds,
        p_senales,
        p_scheduling,
        p_resumen
    ]

    for p in processes:
        p.start()

    try:
        run_display(snapshot, intervalos)
    finally:
        for p in processes:
            terminate_process(p)

        shutdown_manager()
        print("\nMonitor finalizado.")
        exit(0)