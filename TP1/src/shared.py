# src/shared.py
from multiprocessing import Manager, Value
import queue as _queue_mod


# --- Intervalos por vista, con multiprocessing.Value (no Manager.dict) ---
# Elegimos Value en vez de Manager.dict porque acá no necesitamos un dict
# arbitrario: son 7 slots numéricos fijos, conocidos de antemano, que se leen
# y escriben todo el tiempo (cada refresco de cada analizador). Value evita
# el overhead de proxy/RPC que tiene Manager para algo tan simple.

MINIMOS = {
    "resumen": 0.5,
    "memoria": 1.0,
    "fds": 2.0,
    "threads": 0.5,
    "senales": 5.0,
    "scheduling": 5.0,
    "sistema": 1.0,
}


class IntervalStore:
    def __init__(self, defaults=None):
        defaults = defaults or {}
        self._valores = {
            vista: Value('d', float(defaults.get(vista, MINIMOS[vista])))
            for vista in MINIMOS
        }

    def get(self, vista, default=None):
        v = self._valores.get(vista)
        return v.value if v is not None else default

    def __getitem__(self, vista):
        return self._valores[vista].value

    def __setitem__(self, vista, valor):
        minimo = MINIMOS.get(vista, 0.5)
        self._valores[vista].value = max(minimo, float(valor))

    def minimo(self, vista):
        return MINIMOS.get(vista, 0.5)

    def update(self, nuevo_dict):
        for vista, valor in nuevo_dict.items():
            if vista in self._valores:
                self[vista] = valor


class SharedState:
    def __init__(self, defaults=None):
        self.manager = Manager()
        self.snapshot = self.manager.dict()
        self.intervalos = IntervalStore(defaults)

    def shutdown(self):
        try:
            self.manager.shutdown()
        except Exception:
            pass


shared_state = SharedState()
snapshot = shared_state.snapshot


def shutdown_manager():
    shared_state.shutdown()

# Elegimos Value en vez de Manager.dict porque acá no necesitamos un dict
# arbitrario: son 7 slots numéricos fijos, conocidos de antemano, que se leen
# y escriben todo el tiempo (cada refresco de cada analizador). Value evita
# el overhead de proxy/RPC que tiene Manager para algo tan simple.

MINIMOS = {
    "resumen": 0.5,
    "memoria": 1.0,
    "fds": 2.0,
    "threads": 0.5,
    "senales": 5.0,
    "scheduling": 5.0,
    "sistema": 1.0,
}


class IntervalStore:
    def __init__(self, defaults=None):
        defaults = defaults or {}
        self._valores = {
            vista: Value('d', float(defaults.get(vista, MINIMOS[vista])))
            for vista in MINIMOS
        }

    def get(self, vista, default=None):
        v = self._valores.get(vista)
        return v.value if v is not None else default

    def __getitem__(self, vista):
        return self._valores[vista].value

    def __setitem__(self, vista, valor):
        minimo = MINIMOS.get(vista, 0.5)
        self._valores[vista].value = max(minimo, float(valor))

    def minimo(self, vista):
        return MINIMOS.get(vista, 0.5)

    def update(self, nuevo_dict):
        for vista, valor in nuevo_dict.items():
            if vista in self._valores:
                self[vista] = valor


def recibir_ultimo(cola, timeout=1.0):
    """Lee de una Queue y se queda con el dato MÁS RECIENTE, descartando
    los que hayan quedado acumulados atrás (si el analizador es más lento
    que el recolector). Devuelve None si no hay nada disponible en `timeout`
    segundos."""
    ultimo = None
    try:
        ultimo = cola.get(timeout=timeout)
    except _queue_mod.Empty:
        return None
    while True:
        try:
            ultimo = cola.get_nowait()
        except _queue_mod.Empty:
            break
    return ultimo