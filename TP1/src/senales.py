import os
import signal

shutdown = False
verbose = False
dump_requested = False
reload_requested = False
resize_requested = False
_signal_pipe_r = None
_signal_pipe_w = None


def reset_state():
    global shutdown, verbose, dump_requested, reload_requested, resize_requested
    shutdown = False
    verbose = False
    dump_requested = False
    reload_requested = False
    resize_requested = False


def _write_signal_event(sig_name):
    global _signal_pipe_w
    if _signal_pipe_w is not None:
        os.write(_signal_pipe_w, (sig_name + "\n").encode("utf-8"))


def handler_sigint(signum, frame):
    global shutdown
    shutdown = True
    _write_signal_event("SIGINT")


def handler_sigterm(signum, frame):
    global shutdown
    shutdown = True
    _write_signal_event("SIGTERM")


def handler_sigusr1(signum, frame):
    global dump_requested
    dump_requested = True
    _write_signal_event("SIGUSR1")


def handler_sigusr2(signum, frame):
    global verbose
    verbose = not verbose
    _write_signal_event("SIGUSR2")


def handler_sighup(signum, frame):
    global reload_requested
    reload_requested = True
    _write_signal_event("SIGSIGHUP")


def handler_sigwinch(signum, frame):
    global resize_requested
    resize_requested = True
    _write_signal_event("SIGWINCH")


def setup_signal_pipe():
    global _signal_pipe_r, _signal_pipe_w
    if _signal_pipe_r is not None and _signal_pipe_w is not None:
        return
    r_fd, w_fd = os.pipe()
    _signal_pipe_r = r_fd
    _signal_pipe_w = w_fd
    os.set_blocking(r_fd, False)
    os.set_blocking(w_fd, False)
    signal.set_wakeup_fd(w_fd)


def consume_signal_events():
    if _signal_pipe_r is None:
        return []
    try:
        data = os.read(_signal_pipe_r, 4096)
    except BlockingIOError:
        return []
    if not data:
        return []
    return [chunk.decode("utf-8", errors="ignore").strip() for chunk in data.splitlines() if chunk.strip()]


def apply_signal_event(evento):
    if evento == "SIGUSR1":
        globals()["dump_requested"] = True
    elif evento == "SIGUSR2":
        globals()["verbose"] = not globals()["verbose"]
    elif evento == "SIGHUP":
        globals()["reload_requested"] = True
    elif evento == "SIGWINCH":
        globals()["resize_requested"] = True
    elif evento in {"SIGINT", "SIGTERM"}:
        globals()["shutdown"] = True


def registrar_handlers():
    setup_signal_pipe()
    signal.signal(signal.SIGINT, handler_sigint)
    signal.signal(signal.SIGTERM, handler_sigterm)
    signal.signal(signal.SIGUSR1, handler_sigusr1)
    signal.signal(signal.SIGUSR2, handler_sigusr2)
    signal.signal(signal.SIGHUP, handler_sighup)
    signal.signal(signal.SIGWINCH, handler_sigwinch)