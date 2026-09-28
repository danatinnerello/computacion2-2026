import os
import argparse
import hashlib
from datetime import datetime
#hash es como una huella dgital

def hash_file(path):
    h = hashlib.md5() #detecta cambios aunque el tamaño sea igual
    try:
        with open(path, "rb") as f: #rb read binary 
            while chunk := f.read(4096): #lee por partes 4KB
                h.update(chunk)
        return h.hexdigest() #devuelve el hash en formato hexadecimal
    except Exception:
        return None


def formato_fecha(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def listar(ruta, recursive):
    items = {}

    if recursive:
        for root, dirs, files in os.walk(ruta):
            for name in dirs + files:
                path = os.path.join(root, name)
                rel = os.path.relpath(path, ruta)
                items[rel] = path
    else:
        for name in os.listdir(ruta):
            path = os.path.join(ruta, name)
            items[name] = path

    return items


def imprimir_lista(titulo, lista, base):
    print(f"{titulo} {base}:")
    for item in lista:
        if item.endswith(os.sep) or os.path.isdir(os.path.join(base, item)):
            print(f"  {item}/")
        else:
            print(f"  {item}")


def main():
    parser = argparse.ArgumentParser(description="Comparar directorios")
    parser.add_argument("dir1")
    parser.add_argument("dir2")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--checksum", action="store_true")

    args = parser.parse_args()

    print(f"Comparando {args.dir1} con {args.dir2}...\n")

    dir1_items = listar(args.dir1, args.recursive)
    dir2_items = listar(args.dir2, args.recursive)

    set1 = set(dir1_items.keys())
    set2 = set(dir2_items.keys())

    solo1 = sorted(set1 - set2)
    solo2 = sorted(set2 - set1)
    comunes = sorted(set1 & set2)

    imprimir_lista("Solo en", solo1, args.dir1)
    print()
    imprimir_lista("Solo en", solo2, args.dir2)

    mod_size = []
    mod_time = []
    iguales = 0

    for item in comunes:
        p1 = dir1_items[item]
        p2 = dir2_items[item]

        # Solo comparar archivos (no directorios)
        if not os.path.isfile(p1) or not os.path.isfile(p2):
            continue

        try:
            s1 = os.path.getsize(p1)
            s2 = os.path.getsize(p2)

            if s1 != s2:
                mod_size.append((item, s1, s2))
                continue

            if args.checksum:
                h1 = hash_file(p1)
                h2 = hash_file(p2)
                if h1 != h2:
                    mod_size.append((item, s1, s2))
                    continue

            t1 = os.path.getmtime(p1)
            t2 = os.path.getmtime(p2)

            if int(t1) != int(t2):
                mod_time.append((item, t1, t2))
            else:
                iguales += 1

        except Exception:
            continue

    print("\nModificados (tamaño diferente):")
    for f, s1, s2 in mod_size:
        print(f"  {f} ({s1} -> {s2} bytes)")

    print("\nModificados (fecha diferente):")
    for f, t1, t2 in mod_time:
        print(f"  {f} ({formato_fecha(t1)} -> {formato_fecha(t2)})")

    print(f"\nIdénticos: {iguales} archivos")


if __name__ == "__main__":
    main()