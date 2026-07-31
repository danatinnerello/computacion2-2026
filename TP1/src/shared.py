# src/shared.py

from multiprocessing import Manager


class SharedState:
    def __init__(self, initial_intervalos=None):
        self.manager = Manager()
        self.snapshot = self.manager.dict()
        self.intervalos = self.manager.dict(initial_intervalos or {})

    def shutdown(self):
        try:
            self.manager.shutdown()
        except Exception:
            pass


shared_state = SharedState()
snapshot = shared_state.snapshot
intervalos = shared_state.intervalos


def shutdown_manager():
    shared_state.shutdown()