import json
import sys
import time
from datetime import datetime

try:
    import curses
except ModuleNotFoundError:  # pragma: no cover - entorno de pruebas
    curses = None

from config import cargar_config
import senales


VIEW_NAMES = {
    "1": "resumen",
    "2": "memoria",
    "3": "fds",
    "4": "threads",
    "5": "senales",
    "6": "scheduling",
    "7": "sistema",
    "r": "resumen",
    "m": "memoria",
    "f": "fds",
    "t": "threads",
    "s": "senales",
    "p": "scheduling",
    "g": "sistema",
}


def hacer_dump(snapshot_compartido):
    """Vuelca el snapshot compartido a dump_<timestamp>.json (disparado por SIGUSR1)."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"dump_{timestamp}.json"
    try:
        # dict(...) hace una copia "plana" del Manager.dict; lo que cuelga
        # de cada clave ya son objetos Python normales (list/dict/str/int),
        # así que son serializables directamente con json.
        datos = dict(snapshot_compartido)
        with open(nombre, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False, default=str)
        return nombre
    except Exception:
        return None


def render_detalle_proceso(stdscr, estado, selected_item, y, max_y):
    """Panel de detalle real del proceso seleccionado, según la vista activa.

    Siempre se muestra (no depende de verbose): FDs con su destino real,
    threads individuales (LWPs) con su estado, máscaras de señales completas,
    y segmentos de memoria agrupados. El modo verbose (SIGUSR2) solo amplía
    cuántas entradas se listan en fds/threads.
    """
    vista = estado["vista"]
    verbose = estado.get("verbose", False)
    espacio_disponible = max(0, (max_y - 3) - y)
    if espacio_disponible <= 0:
        return

    if vista == "fds":
        fds = selected_item.get("fds", [])
        limite = min(len(fds), espacio_disponible - 1, 15 if verbose else 6)
        safe_addstr(stdscr, y, 0, f"FDs abiertos: {len(fds)} total (mostrando {max(limite, 0)}):")
        for i, fd in enumerate(fds[:limite]):
            linea = f"  fd={fd.get('fd')} -> {fd.get('destino')} [{fd.get('tipo')}]"
            safe_addstr(stdscr, y + 1 + i, 0, linea)

    elif vista == "threads":
        threads = selected_item.get("threads", [])
        limite = min(len(threads), espacio_disponible - 1, 15 if verbose else 6)
        safe_addstr(stdscr, y, 0, f"Threads (LWPs): {len(threads)} total (mostrando {max(limite, 0)}):")
        for i, t in enumerate(threads[:limite]):
            linea = (
                f"  tid={t.get('tid'):<8}{t.get('nombre', ''):<16}"
                f"estado={t.get('estado'):<3}cpu_jiffies={t.get('cpu')}"
            )
            safe_addstr(stdscr, y + 1 + i, 0, linea)

    elif vista == "senales":
        safe_addstr(stdscr, y, 0, "Máscaras completas de señales:")
        campos = [
            ("SigBlk (bloqueadas)", "SigBlk"),
            ("SigIgn (ignoradas)", "SigIgn"),
            ("SigCgt (con handler)", "SigCgt"),
            ("SigPnd (pendientes proc.)", "SigPnd"),
            ("ShdPnd (pendientes grupo)", "ShdPnd"),
        ]
        for i, (etiqueta, clave) in enumerate(campos[:espacio_disponible - 1]):
            valor = ", ".join(selected_item.get(clave, [])) or "-"
            safe_addstr(stdscr, y + 1 + i, 0, f"  {etiqueta}: {valor}")

    elif vista == "memoria":
        segmentos = selected_item.get("segmentos", {})
        safe_addstr(stdscr, y, 0, "Segmentos de memoria (KB, agrupados desde /proc/pid/maps):")
        orden_tipos = ["text", "data", "heap", "stack", "shared", "kernel", "otro"]
        i = 0
        for tipo in orden_tipos:
            if tipo in segmentos and i < espacio_disponible - 1:
                safe_addstr(stdscr, y + 1 + i, 0, f"  {tipo:<8}: {segmentos[tipo]} KB")
                i += 1
        if verbose and i < espacio_disponible - 1:
            safe_addstr(
                stdscr, y + 1 + i, 0,
                f"  minflt={selected_item.get('minflt', 0)}  majflt={selected_item.get('majflt', 0)}"
            )


def safe_addstr(window, y, x, text):
    try:
        max_width = max(0, window.getmaxyx()[1] - x - 1)
        window.addnstr(y, x, text, max_width)
    except curses.error:
        pass


def parse_kb(value):
    try:
        return int(str(value).split()[0])
    except (AttributeError, ValueError, IndexError):
        return 0


def filtrar_y_ordenar(data, estado, snapshot=None):
    filtro = estado.get("filtro", "").strip().lower()
    filtro_usuario = estado.get("filtro_usuario", "").strip().lower()
    resultados = []

    procesos_snapshot = None
    if snapshot is not None:
        # snapshot puede ser un dict comun o el DictProxy que devuelve
        # multiprocessing.Manager().dict() (usado en shared.py). Ese proxy
        # no es instancia de dict aunque soporte .get(), asi que no podemos
        # usar isinstance(snapshot, dict) para decidir si tiene el metodo.
        try:
            snapshot_data = snapshot.get("snapshot")
        except (AttributeError, TypeError):
            snapshot_data = None
        if isinstance(snapshot_data, dict):
            procesos_snapshot = snapshot_data.get("procesos")
            if not isinstance(procesos_snapshot, dict):
                procesos_snapshot = None

    for item in data:
        comando = str(item.get("comando", "")).strip().lower()
        usuario = str(item.get("usuario", "")).strip().lower()
        if not usuario and procesos_snapshot is not None:
            pid = item.get("pid")
            proc_data = procesos_snapshot.get(pid)
            if isinstance(proc_data, dict):
                usuario = str(proc_data.get("usuario", "")).strip().lower()

        if filtro and filtro not in comando:
            continue
        if filtro_usuario and filtro_usuario not in usuario:
            continue
        resultados.append(item)

    if estado.get("orden") == "cpu":
        resultados.sort(key=lambda p: p.get("cpu_pct", 0), reverse=True)
    elif estado.get("orden") == "rss":
        resultados.sort(key=lambda p: parse_kb(p.get("VmRSS", "0 kB")), reverse=True)
    else:
        resultados.sort(key=lambda p: int(p.get("pid", 0)))

    return resultados

def format_row(item, vista):
    if vista == "resumen":
        return f"{item['pid']:<7}{item['usuario']:<10}{item['ppid']:<7}{item['estado']:<5}{item['threads']:<6}{item['cpu_pct']:<7}{item['comando'][:33]}"
    if vista == "memoria":
        return f"{item['pid']:<7}{item['VmRSS']:<10}{item['VmSize']:<10}{item['VmSwap']:<10}{item['comando'][:40]}"
    if vista == "fds":
        return f"{item['pid']:<7}{item['cantidad_fds']:<6}{item['comando'][:50]}"
    if vista == "threads":
        return f"{item['pid']:<7}{item['cantidad']:<7}{item['cpu_pct']:<7}{item['comando'][:35]}"
    if vista == "senales":
        sigign = ", ".join(item["SigIgn"])[:20]
        sigcgt = ", ".join(item["SigCgt"])[:20]
        return f"{item['pid']:<7}{sigign:<22}{sigcgt:<22}{item['comando'][:25]}"
    if vista == "scheduling":
        return f"{item['pid']:<7}{item['priority']:<7}{item['nice']:<7}{item['pgid']:<7}{item['sid']:<7}{item['cpus']:<8}{item['comando'][:20]}"
    return str(item)

def pedir_texto(stdscr, prompt, valor_actual):
    if curses is None or stdscr is None:
        return valor_actual
    curses.echo()
    # El loop principal deja stdscr en modo no bloqueante (nodelay/timeout)
    # para poder refrescar la pantalla sola. Si no lo desactivamos acá,
    # getstr() hereda ese timeout y devuelve vacio antes de que puedas
    # escribir nada. Lo volvemos a activar al salir para no romper el loop.
    stdscr.nodelay(False)
    try:
        stdscr.erase()
        safe_addstr(stdscr, 0, 0, prompt)
        stdscr.refresh()
        texto = stdscr.getstr(0, len(prompt)).decode("utf-8", errors="ignore")
    finally:
        curses.noecho()
        stdscr.nodelay(True)
    return texto

def render_texto_simple(estado):
    vista = estado["vista"]
    data = estado["snapshot"].get(vista, {}).get("datos", [])
    tag_verbose = "  [VERBOSE]" if estado.get("verbose") else ""
    lines = [
        f"TP1 Monitor - Vista: {vista}  intervalo: {estado['intervalo']}s{tag_verbose}",
        f"filtro: {estado['filtro'] or '-'}  usuario: {estado['filtro_usuario'] or '-'}",
    ]

    if vista == "sistema":
        if isinstance(data, dict):
            lines.extend([
                f"Procesos: {data.get('procesos', 0)}",
                f"Memoria total: {data.get('mem_total', 0)} kB",
                f"Memoria libre : {data.get('mem_libre', 0)} kB",
                f"Uso memoria  : {data.get('mem_pct', 0)} %",
                f"Load avg     : {data.get('loadavg', '-')}",
                f"Zombies      : {data.get('zombies', 0)}",
            ])
    else:
        rows = filtrar_y_ordenar(data, estado, estado.get("snapshot"))
        lines.append("Listado de procesos:")
        for item in rows[:8]:
            lines.append(format_row(item, vista))

        if rows and vista in ("fds", "threads", "senales", "memoria"):
            selected_index = max(0, min(estado.get("selected_index", 0), len(rows) - 1))
            selected_item = rows[selected_index]
            verbose = estado.get("verbose", False)
            lines.append(f"--- Detalle PID={selected_item.get('pid')} ---")
            if vista == "fds":
                fds = selected_item.get("fds", [])
                limite = 15 if verbose else 6
                lines.append(f"FDs abiertos: {len(fds)} total (mostrando {min(limite, len(fds))}):")
                for fd in fds[:limite]:
                    lines.append(f"  fd={fd.get('fd')} -> {fd.get('destino')} [{fd.get('tipo')}]")
            elif vista == "threads":
                threads = selected_item.get("threads", [])
                limite = 15 if verbose else 6
                lines.append(f"Threads (LWPs): {len(threads)} total (mostrando {min(limite, len(threads))}):")
                for t in threads[:limite]:
                    lines.append(
                        f"  tid={t.get('tid')} {t.get('nombre')} "
                        f"estado={t.get('estado')} cpu_jiffies={t.get('cpu')}"
                    )
            elif vista == "senales":
                lines.append(f"  SigBlk: {', '.join(selected_item.get('SigBlk', [])) or '-'}")
                lines.append(f"  SigIgn: {', '.join(selected_item.get('SigIgn', [])) or '-'}")
                lines.append(f"  SigCgt: {', '.join(selected_item.get('SigCgt', [])) or '-'}")
                lines.append(f"  SigPnd: {', '.join(selected_item.get('SigPnd', [])) or '-'}")
                lines.append(f"  ShdPnd: {', '.join(selected_item.get('ShdPnd', [])) or '-'}")
            elif vista == "memoria":
                segmentos = selected_item.get("segmentos", {})
                for tipo in ["text", "data", "heap", "stack", "shared", "kernel", "otro"]:
                    if tipo in segmentos:
                        lines.append(f"  {tipo}: {segmentos[tipo]} KB")
                if verbose:
                    lines.append(
                        f"  minflt={selected_item.get('minflt', 0)}  majflt={selected_item.get('majflt', 0)}"
                    )

    sys.stdout.write("\033[2J\033[H")
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


def run_fallback_loop(estado, snapshot, intervalos, senales_module):
    while not estado["salir"] and not senales_module.shutdown:
        estado["snapshot"] = snapshot
        estado["intervalo"] = int(intervalos.get(estado["vista"], estado["intervalo"]))

        if senales_module.reload_requested:
            nueva = cargar_config()
            for clave, valor in nueva.items():
                intervalos[clave] = valor
            senales_module.reload_requested = False
            estado["mensaje"] = "config.json recargado"
            estado["needs_refresh"] = True

        if senales_module.dump_requested:
            nombre = hacer_dump(snapshot)
            senales_module.dump_requested = False
            estado["mensaje"] = f"Dump guardado en {nombre}" if nombre else "Error al guardar el dump"
            estado["needs_refresh"] = True

        if senales_module.verbose != estado.get("verbose"):
            estado["verbose"] = senales_module.verbose
            estado["mensaje"] = f"Modo verbose {'activado' if estado['verbose'] else 'desactivado'}"
            estado["needs_refresh"] = True

        now = time.monotonic()
        if estado.get("needs_refresh", True) or (now - estado.get("last_refresh", 0.0)) >= max(0.5, estado["intervalo"]):
            render_texto_simple(estado)
            estado["last_refresh"] = now
            estado["needs_refresh"] = False

        try:
            import select
            if select.select([sys.stdin], [], [], 0.0)[0]:
                ch = sys.stdin.read(1)
                if ch:
                    procesar_tecla(ch, estado, intervalos, None)
        except Exception:
            pass

        time.sleep(0.1)


def dibujar_pantalla(stdscr, estado):
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    tag_verbose = "  [VERBOSE]" if estado.get("verbose") else ""
    safe_addstr(
        stdscr, 0, 0,
        f"TP1 Monitor - Vista: {estado['vista']}  intervalo: {estado['intervalo']}s"
        f"  q=salir  h=help{tag_verbose}"
    )
    safe_addstr(stdscr, 1, 0, "-" * (max_x - 1))

    if estado["mensaje"]:
        safe_addstr(stdscr, 2, 0, f"[INFO] {estado['mensaje']}")
    else:
        safe_addstr(stdscr, 2, 0, f"filtro: {estado['filtro'] or '-'}  usuario: {estado['filtro_usuario'] or '-'}")

    data = estado["snapshot"].get(estado["vista"], {}).get("datos", [])
    if estado["vista"] == "sistema":
        if isinstance(data, dict):
            safe_addstr(stdscr, 4, 0, f"Procesos: {data.get('procesos', 0)}")
            safe_addstr(stdscr, 5, 0, f"Memoria total: {data.get('mem_total', 0)} kB")
            safe_addstr(stdscr, 6, 0, f"Memoria libre : {data.get('mem_libre', 0)} kB")
            safe_addstr(stdscr, 7, 0, f"Uso memoria  : {data.get('mem_pct', 0)} %")
            safe_addstr(stdscr, 8, 0, f"Load avg     : {data.get('loadavg', '-')}")
            safe_addstr(stdscr, 9, 0, f"CPU user     : {data.get('cpu_user', 0.0)} %")
            safe_addstr(stdscr, 10, 0, f"CPU system   : {data.get('cpu_system', 0.0)} %")
            safe_addstr(stdscr, 11, 0, f"CPU idle     : {data.get('cpu_idle', 0.0)} %")
            safe_addstr(stdscr, 12, 0, f"CPU iowait   : {data.get('cpu_iowait', 0.0)} %")
            safe_addstr(stdscr, 14, 0, "Top procesos por CPU:")
            for idx, proc in enumerate(data.get("top_cpu", [])[:5]):
                safe_addstr(stdscr, 15 + idx, 0, f"{proc['pid']:<7}{proc['cpu_pct']:<7}{proc['comando'][:40]}")
            safe_addstr(stdscr, 21, 0, f"Zombies      : {data.get('zombies', 0)}")
    else:
        headers = {
            "resumen": "PID     USUARIO   PPID   EST   HILOS  CPU%   COMANDO",
            "memoria": "PID     RSS       VSIZE     SWAP      COMANDO",
            "fds": "PID     FDS     COMANDO",
            "threads": "PID     TIDS    CPU%    COMANDO",
            "senales": "PID     SIGIGN                SIGCGT                COMANDO",
            "scheduling": "PID     PRI     NICE    PGID    SID     CPUS     COMANDO",
        }
        safe_addstr(stdscr, 4, 0, headers.get(estado["vista"], "Listado de procesos:"))
        rows = filtrar_y_ordenar(data, estado, estado.get("snapshot"))
        if not rows:
            safe_addstr(stdscr, 6, 0, "No hay procesos que coincidan con el filtro.")
        else:
            # Reservamos espacio fijo abajo para el panel de detalle (fds/threads/
            # senales/memoria) y el footer, y el resto se lo damos a la lista.
            filas_reservadas_pie = 10
            max_lista = max(3, min(18, max_y - 6 - filas_reservadas_pie))

            selected_index = max(0, min(estado.get("selected_index", 0), len(rows) - 1))
            estado["selected_index"] = selected_index
            for index, item in enumerate(rows[:max_lista]):
                line = format_row(item, estado["vista"])
                if index == selected_index:
                    line = f"> {line}"
                safe_addstr(stdscr, 6 + index, 0, line)

            selected_item = rows[selected_index]
            estado["selected_pid"] = selected_item.get("pid")

            y_info = 6 + min(len(rows), max_lista) + 1
            safe_addstr(stdscr, y_info, 0, f"PID={selected_item.get('pid')} CMD={str(selected_item.get('comando', ''))[:80]}")
            safe_addstr(stdscr, y_info + 1, 0, f"Usuario={selected_item.get('usuario', '-')} Orden={estado.get('orden', 'pid')}")

            if estado["vista"] in ("fds", "threads", "senales", "memoria"):
                render_detalle_proceso(stdscr, estado, selected_item, y_info + 3, max_y)

    safe_addstr(stdscr, max_y - 3, 0, "-" * (max_x - 1))
    safe_addstr(stdscr, max_y - 2, 0, "Teclas: 1-7/r/m/f/t/s/p/g  ↑/↓ navegar  Enter pin  / filtrar  u usuario  c ordenar x limpiar filtro +/- intervalo  h=help")
    stdscr.refresh()


def procesar_tecla(ch, estado, intervalos, stdscr):
    if ch in (ord("q"), 27):
        estado["salir"] = True
        senales.shutdown = True
        return

    if isinstance(ch, str):
        key = ch.lower()
    else:
        key = chr(ch).lower() if 0 <= ch < 256 else ""

    if key in VIEW_NAMES:
        estado["vista"] = VIEW_NAMES[key]
        estado["mensaje"] = f"Vista {estado['vista']} seleccionada."
        estado["selected_index"] = 0
        estado["needs_refresh"] = True
        return

    if curses is not None and ch == curses.KEY_UP:
        estado["selected_index"] = max(0, estado.get("selected_index", 0) - 1)
        estado["mensaje"] = "Selección arriba"
        estado["needs_refresh"] = True
        return

    if curses is not None and ch == curses.KEY_DOWN:
        estado["selected_index"] = min(17, estado.get("selected_index", 0) + 1)
        estado["mensaje"] = "Selección abajo"
        estado["needs_refresh"] = True
        return

    if ch in (10, 13):
        selected_pid = estado.get("selected_pid")
        if selected_pid is None:
            selected_pid = estado.get("pinned_pid")
        estado["pinned_pid"] = selected_pid
        estado["mensaje"] = f"Pin activado para PID {selected_pid}" if selected_pid is not None else "No hay proceso seleccionado"
        estado["needs_refresh"] = True
        return

    if key == "+":
        nuevo = max(1, int(intervalos.get(estado["vista"], 2)) - 1)
        intervalos[estado["vista"]] = nuevo
        estado["intervalo"] = nuevo
        estado["mensaje"] = f"Intervalo {estado['vista']} = {nuevo}s"
        estado["needs_refresh"] = True
        return

    if key == "-":
        nuevo = int(intervalos.get(estado["vista"], 2)) + 1
        intervalos[estado["vista"]] = nuevo
        estado["intervalo"] = nuevo
        estado["mensaje"] = f"Intervalo {estado['vista']} = {nuevo}s"
        estado["needs_refresh"] = True
        return

    if key == "c":
        ordenes = ["pid", "cpu", "rss"]
        actual = ordenes.index(estado.get("orden", "pid"))
        estado["orden"] = ordenes[(actual + 1) % len(ordenes)]
        estado["mensaje"] = f"Ordenado por {estado['orden']}"
        estado["needs_refresh"] = True
        return

    if key == "x":
        estado["filtro"] = ""
        estado["filtro_usuario"] = ""
        estado["mensaje"] = "Filtros limpiados"
        estado["needs_refresh"] = True
        return

    if key == "/":
        texto = pedir_texto(stdscr, "Filtro comando: ", estado.get("filtro", ""))
        estado["filtro"] = texto
        estado["mensaje"] = f"Filtro comando: {texto or '-'}"
        estado["needs_refresh"] = True
        return

    if key == "u":
        texto = pedir_texto(stdscr, "Filtro usuario: ", estado.get("filtro_usuario", ""))
        estado["filtro_usuario"] = texto
        estado["mensaje"] = f"Filtro usuario: {texto or '-'}"
        estado["needs_refresh"] = True
        return

    if key == "h" or key == "?":
        estado["mensaje"] = "Ayuda: 1-7/r/m/... q, +/-, / filtra por comando, u por usuario, x limpiar filtro, c ordena"
        estado["needs_refresh"] = True
        return


def run_display(snapshot, intervalos):
    estado = {
        "vista": "sistema",
        "filtro": "",
        "filtro_usuario": "",
        "orden": "pid",
        "intervalo": int(intervalos.get("sistema", 2)),
        "salir": False,
        "snapshot": snapshot,
        "mensaje": "",
        "selected_index": 0,
        "pinned_pid": None,
        "needs_refresh": True,
        "last_refresh": 0.0,
        "verbose": senales.verbose,
    }

    def main(stdscr):
        if curses is None or not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            run_fallback_loop(estado, snapshot, intervalos, senales)
            return

        stdscr.nodelay(True)
        stdscr.timeout(150)

        while not estado["salir"] and not senales.shutdown:
            estado["snapshot"] = snapshot
            estado["intervalo"] = int(intervalos.get(estado["vista"], estado["intervalo"]))

            if senales.reload_requested:
                nueva = cargar_config()
                for clave, valor in nueva.items():
                    intervalos[clave] = valor
                senales.reload_requested = False
                estado["mensaje"] = "config.json recargado"
                estado["needs_refresh"] = True

            if senales.dump_requested:
                nombre = hacer_dump(snapshot)
                senales.dump_requested = False
                estado["mensaje"] = f"Dump guardado en {nombre}" if nombre else "Error al guardar el dump"
                estado["needs_refresh"] = True

            if senales.verbose != estado.get("verbose"):
                estado["verbose"] = senales.verbose
                estado["mensaje"] = f"Modo verbose {'activado' if estado['verbose'] else 'desactivado'}"
                estado["needs_refresh"] = True

            if senales.resize_requested:
                curses.resize_term(*stdscr.getmaxyx())
                senales.resize_requested = False
                estado["needs_refresh"] = True

            now = time.monotonic()
            if estado.get("needs_refresh", True) or (now - estado.get("last_refresh", 0.0)) >= max(0.5, estado["intervalo"]):
                dibujar_pantalla(stdscr, estado)
                estado["last_refresh"] = now
                estado["needs_refresh"] = False

            ch = stdscr.getch()
            if ch != -1:
                procesar_tecla(ch, estado, intervalos, stdscr)

            time.sleep(0.1)

    if curses is None:
        print("DEBUG: curses no está disponible.")
        run_fallback_loop(estado, snapshot, intervalos, senales)
        return

    try:
        print("DEBUG: Entrando a curses.wrapper()")
        curses.wrapper(main)
        print("DEBUG: Salió normalmente de curses.wrapper()")
    except Exception as e:
        import traceback

        print("\n================ ERROR EN CURSES ================\n")
        traceback.print_exc()
        print("\n===============================================\n")

        raise