import argparse
import json
from pathlib import Path
import sys

archivo_tareas = Path.home() / ".tareas.json"

if archivo_tareas.exists():
    with open(archivo_tareas) as f:
        tareas = json.load(f)
else:
    tareas = []

def guardar():
    with open(archivo_tareas, "w") as f:
        json.dump(tareas, f, indent=4)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="comando")

parser_add = subparsers.add_parser("add")
parser_add.add_argument("descripcion")
parser_add.add_argument("--priority", choices=["baja", "media", "alta"])

parser_list = subparsers.add_parser("list")
parser_list.add_argument("--pending", action="store_true")
parser_list.add_argument("--done", action="store_true")
parser_list.add_argument("--priority", choices=["baja", "media", "alta"])

parser_done = subparsers.add_parser("done")
parser_done.add_argument("id", type=int)

parser_remove = subparsers.add_parser("remove")
parser_remove.add_argument("id", type=int)

args = parser.parse_args()

#comandos
if args.comando == "add":
    nueva = {
        "id": len(tareas) + 1,
        "descripcion": args.descripcion,
        "done": False,
        "priority": args.priority
    }

    tareas.append(nueva)
    guardar()

    if args.priority:
        print(f"Tarea #{nueva['id']} agregada (prioridad: {args.priority})")
        sys.exit(0)
    else:
        print(f"Tarea #{nueva['id']} agregada")
        sys.exit(0)
elif args.comando == "list":
    for t in tareas:

        # filtros
        if args.pending and t["done"]:
            continue
        if args.done and not t["done"]:
            continue
        if args.priority and t["priority"] != args.priority:
            continue

        estado = "[x]" if t["done"] else "[ ]"

        prioridad = ""
        if t["priority"]:
            prioridad = f" [{t['priority'].upper()}]"

        print(f"#{t['id']} {estado} {t['descripcion']}{prioridad}")
elif args.comando == "done":
    for t in tareas:
        if t["id"] == args.id:
            t["done"] = True
            guardar()
            print(f"Tarea #{args.id} completada")
            sys.exit(0)
            break
            
elif args.comando == "remove":
    for t in tareas:
        if t["id"] == args.id:
            confirm = input(f'¿Eliminar "{t["descripcion"]}"? [s/N] ')

            if confirm.lower() == "s":
                tareas.remove(t)
                guardar()
                print(f"Tarea #{args.id} eliminada")
                sys.exit(0)
            break