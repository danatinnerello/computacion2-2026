# src/procfs.py

import os
from pathlib import Path


PROC = Path("/proc")


def obtener_pids():
    """
    Devuelve una lista de PIDs existentes.
    """
    return sorted(
        int(p.name)
        for p in PROC.iterdir()
        if p.is_dir() and p.name.isdigit()
    )


def leer_meminfo():
    """
    Lee /proc/meminfo y devuelve un diccionario.
    """
    info = {}

    with open("/proc/meminfo", "r") as archivo:
        for linea in archivo:
            partes = linea.split()
            clave = partes[0].rstrip(":")
            valor = int(partes[1])
            info[clave] = valor

    return info


def leer_cpu_global():
    """
    Lee la línea CPU global de /proc/stat.
    """
    with open("/proc/stat", "r") as archivo:
        primera_linea = archivo.readline()

    campos = primera_linea.split()

    return {
        "user": int(campos[1]),
        "nice": int(campos[2]),
        "system": int(campos[3]),
        "idle": int(campos[4]),
        "iowait": int(campos[5]),
        "irq": int(campos[6]),
        "softirq": int(campos[7]),
    }


def leer_stat(pid):
    """
    Lee /proc/[pid]/stat.
    """
    ruta = f"/proc/{pid}/stat"

    with open(ruta, "r") as archivo:
        contenido = archivo.read()

    campos = contenido.split()

    return {
        "pid": int(campos[0]),
        "comm": campos[1].strip("()"),
        "state": campos[2],
        "ppid": int(campos[3]),
        "utime": int(campos[13]),
        "stime": int(campos[14]),
        "num_threads": int(campos[19]),
        "vsize": int(campos[22]),
        "rss": int(campos[23]),
    }


def leer_status(pid):
    """
    Lee /proc/[pid]/status.
    """
    ruta = f"/proc/{pid}/status"

    datos = {}

    with open(ruta, "r") as archivo:
        for linea in archivo:
            if ":" not in linea:
                continue

            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip()

    return datos


def leer_cmdline(pid):
    """
    Lee el comando completo utilizado para lanzar el proceso.
    """
    ruta = f"/proc/{pid}/cmdline"

    with open(ruta, "rb") as archivo:
        contenido = archivo.read()

    return contenido.replace(b"\0", b" ").decode(errors="ignore").strip()

def contar_fds(pid):
    """
    Cuenta los file descriptors abiertos por un proceso.
    """

    ruta = f"/proc/{pid}/fd"

    try:
        return len(os.listdir(ruta))

    except (
        FileNotFoundError,
        PermissionError,
        ProcessLookupError
    ):
        return 0