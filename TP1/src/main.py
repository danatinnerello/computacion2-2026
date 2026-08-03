from multiprocessing import Process, Queue
from time import sleep, time
import json

from recolector import recolector_loop
from agregador import proceso_agregador

from analizadores.sistema import proceso_sistema
from analizadores.threads import proceso_threads
from analizadores.memoria import proceso_memoria
from analizadores.fds import proceso_fds
from analizadores.senales import proceso_senales
from analizadores.scheduling import proceso_scheduling
from analizadores.resumen import proceso_resumen

from display import run_display
from config import cargar_config
from shared import snapshot, shutdown_manager, IntervalStore

import senales


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
    intervalos = IntervalStore(config)

    VISTAS = ["resumen", "memoria", "fds", "threads", "senales", "scheduling", "sistema"]

    # Una Queue por analizador: el recolector le manda a cada uno su propia
    # copia del snapshot crudo (no puede ser UNA sola Queue compartida entre
    # los 7, porque un item de una Queue solo lo puede consumir un proceso).
    colas_analizadores = {vista: Queue(maxsize=3) for vista in VISTAS}

    # Una sola Queue de resultados: los 7 analizadores publican ahí y el
    # agregador es el único consumidor -> único escritor del snapshot global.
    cola_resultados = Queue()

    p_recolector = Process(
        target=recolector_loop,
        args=(colas_analizadores,)
    )

    p_agregador = Process(
        target=proceso_agregador,
        args=(cola_resultados, snapshot)
    )

    p_sistema = Process(
        target=proceso_sistema,
        args=(colas_analizadores["sistema"], cola_resultados, intervalos)
    )

    p_threads = Process(
        target=proceso_threads,
        args=(colas_analizadores["threads"], cola_resultados, intervalos)
    )

    p_memoria = Process(
        target=proceso_memoria,
        args=(colas_analizadores["memoria"], cola_resultados, intervalos)
    )

    p_fds = Process(
        target=proceso_fds,
        args=(colas_analizadores["fds"], cola_resultados, intervalos)
    )

    p_senales = Process(
        target=proceso_senales,
        args=(colas_analizadores["senales"], cola_resultados, intervalos)
    )

    p_scheduling = Process(
        target=proceso_scheduling,
        args=(colas_analizadores["scheduling"], cola_resultados, intervalos)
    )

    p_resumen = Process(
        target=proceso_resumen,
        args=(colas_analizadores["resumen"], cola_resultados, intervalos)
    )

    processes = [
        p_recolector,
        p_agregador,
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