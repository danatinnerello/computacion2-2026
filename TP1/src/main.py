from recolector import recolectar

from analizadores.memoria import analizar as analizar_memoria
from analizadores.threads import analizar as analizar_threads
from analizadores.fds import analizar as analizar_fds
from analizadores.senales import analizar as analizar_senales
from analizadores.scheduling import analizar as analizar_scheduling

from display import (
    mostrar_memoria,
    mostrar_threads,
    mostrar_fds,
    mostrar_senales,
    mostrar_scheduling
)

snapshot = recolectar()

print()
print("1 - Memoria")
print("2 - Threads")
print("3 - File Descriptors")
print("4 - Señales")
print("5 - Scheduling")
opcion = input("\nOpcion: ")

if opcion == "1":

    procesos = analizar_memoria(snapshot)
    mostrar_memoria(procesos)

elif opcion == "2":

    procesos = analizar_threads(snapshot)
    mostrar_threads(procesos)

elif opcion == "3":

    procesos = analizar_fds(snapshot)
    mostrar_fds(procesos)

elif opcion == "4":

    procesos = analizar_senales(snapshot)
    mostrar_senales(procesos)

elif opcion == "5":

    procesos = analizar_scheduling(snapshot)
    mostrar_scheduling(procesos)

else:

    print("Opcion invalida")