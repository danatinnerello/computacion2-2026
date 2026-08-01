# Trabajo Práctico N° 1 - Monitor de Procesos y Threads

## Descripción general

Este proyecto implementa un monitor de procesos en Python para Linux que lee información del sistema directamente desde `/proc`, la procesa en múltiples componentes y muestra una interfaz de usuario basada en terminal.

La aplicación central funciona con:

- recolección de snapshots del sistema y procesos
- análisis independiente de vistas específicas
- un TUI interactivo con `curses`
- manejo de señales para recarga, volcado y modo verbose
- estado compartido entre procesos mediante `multiprocessing.Manager`

## Estructura del proyecto

```
TP1/
├── config.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   ├── config.py
│   ├── display.py
│   ├── procfs.py
│   ├── recolector.py
│   ├── shared.py
│   ├── senales.py
│   └── analizadores/
│       ├── cpu.py
│       ├── fds.py
│       ├── memoria.py
│       ├── resumen.py
│       ├── scheduling.py
│       ├── senales.py
│       ├── sistema.py
│       └── threads.py
└── tests/
    ├── test_config.py
    ├── test_display.py
    ├── test_display_extra.py
    ├── test_analizadores.py
    ├── test_procfs.py
    ├── test_recolector.py
    ├── test_senales.py
    ├── test_senales_extra.py
    └── test_shared.py
```

## Archivos principales

- `src/main.py`: punto de entrada. Arranca los procesos de recolector y analizadores, y lanza la interfaz de usuario.
- `src/config.py`: carga la configuración de intervalos desde `config.json`.
- `src/procfs.py`: lee datos desde `/proc` para procesos, memoria, CPU, fds, hilos y mapas de memoria.
- `src/recolector.py`: construye el snapshot global de sistema y procesos.
- `src/shared.py`: define el estado compartido entre procesos con `Manager().dict()`.
- `src/senales.py`: gestiona señales del sistema y pipe de notificación.
- `src/display.py`: renderiza la TUI, procesa teclas y muestra las distintas vistas.
- `src/analizadores/`: contiene la lógica de cada vista del monitor.

## Vistas disponibles

El monitor soporta las siguientes vistas:

- `resumen`: procesos ordenados por CPU, con información básica de PID, usuario, PPID, estado, hilos y comando.
- `memoria`: uso de memoria RSS/VSIZE/SWAP por proceso.
- `fds`: cantidad de descriptores abiertos por proceso.
- `threads`: hilos (LWPs) por proceso.
- `senales`: máscaras de señales por proceso.
- `scheduling`: prioridad, nice, grupo de proceso y CPU permitidas.
- `sistema`: métricas globales de CPU, memoria, loadavg y top procesos por CPU.

## Controles y teclas

- `1` o `r`: vista `resumen`
- `2` o `m`: vista `memoria`
- `3` o `f`: vista `fds`
- `4` o `t`: vista `threads`
- `5` o `s`: vista `senales`
- `6` o `p`: vista `scheduling`
- `7` o `g`: vista `sistema`
- `↑` / `↓`: navegar procesos
- `Enter`: fijar PID seleccionado
- `/`: filtrar por comando
- `u`: filtrar por usuario
- `c`: cambiar orden entre `pid`, `cpu`, `rss`
- `x`: limpiar filtros
- `+` / `-`: ajustar intervalo de actualización
- `h` o `?`: ayuda
- `q` o `Esc`: salir

## Señales soportadas

El proceso principal maneja eventos de señales para:

- `SIGUSR1`: generar dump JSON del snapshot compartido
- `SIGUSR2`: alternar modo verbose
- `SIGHUP`: recargar `config.json`
- `SIGWINCH`: detectar cambio de tamaño de terminal
- `SIGINT` / `SIGTERM`: terminar la aplicación

## Configuración

El archivo `config.json` define el intervalo de actualización para cada vista:

```json
{
  "resumen": 2,
  "memoria": 3,
  "fds": 5,
  "threads": 2,
  "senales": 10,
  "scheduling": 10,
  "sistema": 2
}
```

## Requisitos

- Python 3.11+ (o Python 3.12 compatible)
- Linux con `/proc` disponible
- `curses` en el entorno para la interfaz TUI

## Instalación

```bash
cd TP1
python3 -m pip install -r requirements.txt
```

Si no se usa `requirements.txt`, solo se necesita Python estándar.

## Ejecución local

```bash
cd TP1
python3 src/main.py
```

## Ejecución en Docker

```bash
cd TP1
docker compose run --rm monitor
```

El contenedor monta el directorio actual en `/app` y arranca `python3 src/main.py`.

## Pruebas unitarias

El proyecto incluye una suite de pruebas para:

- carga de configuración
- lectura de `/proc`
- recolección de snapshots
- análisis de vistas
- TUI y procesamiento de teclas
- manejo de señales
- estado compartido

Ejecutar la suite completa:

```bash
cd TP1
python3 -m unittest discover -s tests -p 'test_*.py'
```

Ejecutar un archivo específico:

```bash
python3 -m unittest tests.test_display
```

## Notas

- El proyecto está pensado para Linux, ya que usa `/proc` y señales POSIX.
- En entornos sin `curses`, el proyecto tiene una ruta de fallback que imprime texto simple.
- La configuración de intervalos puede recargarse en caliente con `SIGHUP`.

## Buenas prácticas

- Ejecuta siempre desde el directorio `TP1` para que las rutas relativas funcionen.
- Usa un terminal real para la interfaz `curses`, no un entorno no interactivo.
- Si agregas nuevas vistas, incluye tests en `tests/test_analizadores.py` y la lógica de render en `src/display.py`.
