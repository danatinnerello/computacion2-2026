import os
import argparse


def parse_size(size_str):
    size_str = size_str.upper()

    if size_str.endswith("K"):
        return int(size_str[:-1]) * 1024
    elif size_str.endswith("M"):
        return int(size_str[:-1]) * 1024 * 1024
    elif size_str.endswith("G"):
        return int(size_str[:-1]) * 1024 * 1024 * 1024
    else:
        return int(size_str)  # bytes


def format_size(bytes_size):
    if bytes_size >= 1024 * 1024 * 1024:
        return f"{bytes_size / (1024**3):.1f} GB"
    elif bytes_size >= 1024 * 1024:
        return f"{bytes_size / (1024**2):.1f} MB"
    elif bytes_size >= 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size} B"


def es_tipo_valido(path, tipo):
    if tipo == "f":
        return os.path.isfile(path)
    elif tipo == "d":
        return os.path.isdir(path)
    return True


def main():
    parser = argparse.ArgumentParser(description="Buscar archivos grandes")
    parser.add_argument("ruta", help="Directorio a buscar")
    parser.add_argument("--min-size", required=True, help="Tamaño mínimo (ej: 100K, 1M, 2G)")
    parser.add_argument("--type", choices=["f", "d"], help="Tipo: f=archivo, d=directorio")
    parser.add_argument("--top", type=int, help="Mostrar solo los N más grandes")

    args = parser.parse_args()

    min_size = parse_size(args.min_size)

    resultados = []

    # Recorrido recursivo
    for root, dirs, files in os.walk(args.ruta):
        items = []

        if args.type == "d":
            items = dirs
        elif args.type == "f":
            items = files
        else:
            items = dirs + files

        for item in items:
            path = os.path.join(root, item)

            try:
                size = os.path.getsize(path)
            except (FileNotFoundError, PermissionError):
                continue

            if size >= min_size and es_tipo_valido(path, args.type):
                resultados.append((path, size))

    # Ordenar por tamaño descendente
    resultados.sort(key=lambda x: x[1], reverse=True)

    total_size = 0

    # Si hay --top
    if args.top:
        print(f"Los {args.top} archivos más grandes:")
        resultados = resultados[:args.top]

        for i, (path, size) in enumerate(resultados, 1):
            print(f"{i}. {path} ({format_size(size)})")
            total_size += size
    else:
        for path, size in resultados:
            print(f"{path} ({format_size(size)})")
            total_size += size

        print(f"\nTotal: {len(resultados)} archivos, {format_size(total_size)}")


if __name__ == "__main__":
    main()