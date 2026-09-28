import os
import argparse
import shutil
import fnmatch
from datetime import datetime


def parse_exclude(patterns):
    if not patterns:
        return []
    return [p.strip() for p in patterns.split(",")]


def excluded(path, patterns):
    name = os.path.basename(path)
    return any(fnmatch.fnmatch(name, p) for p in patterns)


def listar_archivos(base, exclude_patterns):
    archivos = {}

    for root, dirs, files in os.walk(base):
        # evitar entrar en dirs excluidos
        dirs[:] = [d for d in dirs if not excluded(d, exclude_patterns)]

        for f in files:
            if excluded(f, exclude_patterns):
                continue

            full = os.path.join(root, f)
            rel = os.path.relpath(full, base)
            archivos[rel] = full

    return archivos


def formato_fecha(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="Sincronizar directorios")
    parser.add_argument("origen")
    parser.add_argument("destino")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--exclude")

    args = parser.parse_args()

    exclude_patterns = parse_exclude(args.exclude)

    print("Analizando diferencias...\n")

    src = listar_archivos(args.origen, exclude_patterns)
    dst = listar_archivos(args.destino, exclude_patterns)

    set_src = set(src.keys())
    set_dst = set(dst.keys())

    nuevos = sorted(set_src - set_dst)
    eliminados = sorted(set_dst - set_src)
    comunes = sorted(set_src & set_dst)

    modificados = []

    for f in comunes:
        s1 = os.path.getsize(src[f])
        s2 = os.path.getsize(dst[f])

        t1 = os.path.getmtime(src[f])
        t2 = os.path.getmtime(dst[f])

        if s1 != s2 or int(t1) != int(t2):
            modificados.append(f)

    # --- Mostrar cambios ---
    print("Cambios detectados:")

    for f in nuevos:
        size = os.path.getsize(src[f])
        print(f"  NUEVO:      {f} ({size} bytes)")

    for f in modificados:
        fecha = formato_fecha(os.path.getmtime(src[f]))
        print(f"  MODIFICADO: {f} (cambiado {fecha})")

    if args.delete:
        for f in eliminados:
            print(f"  ELIMINADO:  {f} (existe en destino pero no en origen)")

    print(f"\nResumen: {len(nuevos)} nuevos, {len(modificados)} modificados, {len(eliminados) if args.delete else 0} eliminados")

    # --- Confirmación ---
    if args.dry_run:
        return

    resp = input("\n¿Proceder con la sincronización? [s/N] ").lower()
    if resp != "s":
        print("Cancelado.")
        return

    # --- Aplicar cambios ---
    for f in nuevos:
        src_path = src[f]
        dst_path = os.path.join(args.destino, f)

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        print(f"Copiando {f}...", end=" ")
        try:
            shutil.copy2(src_path, dst_path)
            print("OK")
        except Exception as e:
            print(f"Error: {e}")

    for f in modificados:
        src_path = src[f]
        dst_path = os.path.join(args.destino, f)

        print(f"Actualizando {f}...", end=" ")
        try:
            shutil.copy2(src_path, dst_path)
            print("OK")
        except Exception as e:
            print(f"Error: {e}")

    if args.delete:
        for f in eliminados:
            dst_path = os.path.join(args.destino, f)

            print(f"Eliminando {f}...", end=" ")
            try:
                os.remove(dst_path)
                print("OK")
            except Exception as e:
                print(f"Error: {e}")

    print("\nCompletado.")


if __name__ == "__main__":
    main()