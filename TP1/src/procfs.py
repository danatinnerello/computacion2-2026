import os
from pathlib import Path
import pwd
import time

PROC = Path("/proc")


def obtener_usuario(uid):
    try:
        return pwd.getpwuid(int(uid)).pw_name
    except (KeyError, TypeError, ValueError):
        return str(uid)


def obtener_pids():
    return sorted(
        int(p.name)
        for p in PROC.iterdir()
        if p.is_dir() and p.name.isdigit()
    )


def leer_meminfo():
    info = {}
    with open("/proc/meminfo", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.split()
            clave = partes[0].rstrip(":")
            valor = int(partes[1])
            info[clave] = valor
    return info


def leer_cpu_global():
    with open("/proc/stat", "r", encoding="utf-8") as archivo:
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
        "steal": int(campos[8]) if len(campos) > 8 else 0,
    }


def leer_loadavg():
    with open("/proc/loadavg", "r", encoding="utf-8") as archivo:
        campos = archivo.readline().split()
    return {
        "one": campos[0],
        "five": campos[1],
        "fifteen": campos[2],
    }


def leer_uptime():
    with open("/proc/uptime", "r", encoding="utf-8") as archivo:
        linea = archivo.readline().split()
    uptime = float(linea[0])
    boot_time = int(time.time() - uptime)
    return uptime, boot_time


def leer_stat(pid):
    ruta = f"/proc/{pid}/stat"
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    campos = contenido.split()

    return {
        "pid": int(campos[0]),
        "comm": campos[1].strip("()"),
        "state": campos[2],
        "ppid": int(campos[3]),
        "pgrp": int(campos[4]),
        "session": int(campos[5]),
        "minflt": int(campos[9]),
        "cminflt": int(campos[10]),
        "majflt": int(campos[11]),
        "cmajflt": int(campos[12]),
        "utime": int(campos[13]),
        "stime": int(campos[14]),
        "priority": int(campos[17]),
        "nice": int(campos[18]),
        "num_threads": int(campos[19]),
        "vsize": int(campos[22]),
        "rss": int(campos[23]),
        "policy": int(campos[41]) if len(campos) > 41 else -1,
        "processor": int(campos[38]) if len(campos) > 38 else -1,
    }


def leer_status(pid):
    ruta = f"/proc/{pid}/status"
    datos = {}
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if ":" not in linea:
                continue
            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip()
    return datos


def leer_cmdline(pid):
    ruta = f"/proc/{pid}/cmdline"
    with open(ruta, "rb") as archivo:
        contenido = archivo.read()
    return contenido.replace(b"\0", b" ").decode(errors="ignore").strip()


def leer_fds(pid):
    ruta = f"/proc/{pid}/fd"
    resultado = []
    try:
        for fd in os.listdir(ruta):
            try:
                destino = os.readlink(f"{ruta}/{fd}")
                if destino.startswith("socket:"):
                    tipo = "socket"
                elif destino.startswith("pipe:"):
                    tipo = "pipe"
                elif "/pts/" in destino or "/tty" in destino:
                    tipo = "tty"
                else:
                    tipo = "file"
                resultado.append({
                    "fd": fd,
                    "destino": destino,
                    "tipo": tipo
                })
            except Exception:
                pass
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        pass
    return resultado


def leer_thread_status(pid, tid):
    ruta = f"/proc/{pid}/task/{tid}/status"
    datos = {}
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if ":" not in linea:
                    continue
                clave, valor = linea.split(":", 1)
                datos[clave.strip()] = valor.strip()
    except (FileNotFoundError, PermissionError):
        pass
    return datos


def leer_threads(pid):
    ruta = f"/proc/{pid}/task"
    resultado = []
    try:
        for tid in os.listdir(ruta):
            try:
                with open(f"{ruta}/{tid}/stat", "r", encoding="utf-8") as archivo:
                    campos = archivo.read().split()
                status = leer_thread_status(pid, tid)
                voluntary = 0
                nonvoluntary = 0
                try:
                    voluntary = int(status.get("voluntary_ctxt_switches", "0") or 0)
                except ValueError:
                    voluntary = 0
                try:
                    nonvoluntary = int(status.get("nonvoluntary_ctxt_switches", "0") or 0)
                except ValueError:
                    nonvoluntary = 0

                resultado.append({
                    "tid": int(tid),
                    "nombre": campos[1].strip("()"),
                    "estado": campos[2],
                    "cpu": int(campos[13]) + int(campos[14]),
                    "voluntary": voluntary,
                    "nonvoluntary": nonvoluntary,
                })
            except (FileNotFoundError, PermissionError, IndexError):
                pass
    except (FileNotFoundError, PermissionError):
        pass
    return resultado


def leer_maps(pid):
    ruta = f"/proc/{pid}/maps"
    resultado = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.split()
                direcciones = partes[0]
                perms = partes[1]
                path = partes[-1] if len(partes) >= 6 else ""
                inicio, fin = direcciones.split("-")
                size_kb = (int(fin, 16) - int(inicio, 16)) // 1024
                tipo = "otro"
                if "[heap]" in path:
                    tipo = "heap"
                elif "[stack]" in path:
                    tipo = "stack"
                elif "[vdso]" in path or "[vsyscall]" in path:
                    tipo = "kernel"
                elif path.endswith(".so") or perms[2] == "x":
                    tipo = "text"
                elif "rw" in perms:
                    tipo = "data"
                elif "r-" in perms:
                    tipo = "shared"
                resultado.append({
                    "range": direcciones,
                    "perms": perms,
                    "path": path,
                    "size_kb": size_kb,
                    "tipo": tipo
                })
    except (FileNotFoundError, PermissionError):
        pass
    return resultado


def resumir_segmentos(pid):
    """Agrupa los mapeos de /proc/<pid>/maps por tipo (heap/stack/text/data/shared/
    kernel/otro) y suma el tamaño en KB de cada grupo. Devuelve un dict tipo->KB."""
    resumen = {}
    for seg in leer_maps(pid):
        tipo = seg["tipo"]
        resumen[tipo] = resumen.get(tipo, 0) + seg["size_kb"]
    return resumen