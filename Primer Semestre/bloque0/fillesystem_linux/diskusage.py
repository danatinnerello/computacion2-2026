import os
import argparse
import fnmatch


def parse_exclude(patterns):
    if not patterns:
        return []
    return [p.strip() for p in patterns.split(",")]


def excluded(path, patterns):
    name = os.path.basename(path)
    for p in patterns:
        if fnmatch.fnmatch(name, p):
            return True
    return False


def get_size(path, exclude_patterns):
    total = 0

    if os.path.isfile(path):
        return os.path.getsize(path)

    for root, dirs, files in os.walk(path):
        # filtrar dirs
        dirs[:] = [d for d in dirs if not excluded(d, exclude_patterns)]

        for f in files:
            if excluded(f, exclude_patterns):
                continue

            full = os.path.join(root, f)
            try:
                total += os.path.getsize(full)
            except Exception:
                continue

    return total


def human_size(size):
    if size >= 1024**3:
        return f"{size / (1024**3):.1f}G"
    elif size >= 1024**2:
        return f"{size / (1024**2):.1f}M"
    elif size >= 1024:
        return f"{size / 1024:.1f}K"
    else:
        return f"{size}B"


def main():
    parser = argparse.ArgumentParser(description="Analizador de uso de disco")
    parser.add_argument("ruta")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--top", type=int)
    parser.add_argument("--exclude")

    args = parser.parse_args()

    exclude_patterns = parse_exclude(args.exclude)

    resultados = []

    base_depth = args.ruta.rstrip(os.sep).count(os.sep) #control de produndidad : cuantas /

    for root, dirs, files in os.walk(args.ruta): #recorre el arbol
        current_depth = root.count(os.sep) - base_depth

        if current_depth > args.depth:
            continue

        for name in dirs + files:
            path = os.path.join(root, name)

            if excluded(name, exclude_patterns):
                continue

            size = get_size(path, exclude_patterns)
            resultados.append((path, size))

    # ordenar por tamaño
    resultados.sort(key=lambda x: x[1], reverse=True)

    total = sum(size for _, size in resultados)

    # modo top
    if args.top:
        print(f"Los {args.top} archivos/carpetas más grandes:")
        for i, (path, size) in enumerate(resultados[:args.top], 1):
            print(f"  {i}. {path} ({human_size(size)})")
        return

    # modo normal
    for path, size in resultados:
        print(f"{human_size(size):<8} {path}")

    print("─" * 25)
    print(f"Total: {human_size(total)}")


if __name__ == "__main__":
    main()