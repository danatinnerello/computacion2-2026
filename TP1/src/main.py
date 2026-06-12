from recolector import recolectar
from analizadores.resumen import analizar

snapshot = recolectar()

procesos = analizar(snapshot)

print(f"Cantidad de procesos: {len(procesos)}\n")

for proceso in procesos[:10]:

    print(
        f"PID={proceso['pid']} "
        f"PPID={proceso['ppid']} "
        f"ESTADO={proceso['estado']} "
        f"THREADS={proceso['threads']} "
        f"CMD={proceso['comando']}"
    )