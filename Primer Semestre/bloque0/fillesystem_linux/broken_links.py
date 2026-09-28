import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Detectar enlaces simbólicos rotos")
    parser.add_argument("ruta", help="Directorio a analizar")
    parser.add_argument("--delete", action="store_true", help="Eliminar enlaces rotos")
    parser.add_argument("--quiet", action="store_true", help="Mostrar solo el conteo")

    args = parser.parse_args()

    broken = []

    if not args.quiet:
        print(f"Buscando enlaces simbólicos rotos en {args.ruta}...\n")

    # Recorrido recursivo
    for root, dirs, files in os.walk(args.ruta):
        for name in dirs + files:
            path = os.path.join(root, name)

            # Es symlink pero no existe el destino
            if os.path.islink(path) and not os.path.exists(path):
                broken.append(path)

    # Modo silencioso
    if args.quiet:
        print(len(broken))
        return

    if not broken:
        print("No se encontraron enlaces rotos")
        return

    print("Enlaces rotos encontrados:")

    for link in broken:
        destino = os.readlink(link)
        print(f"  {link} -> {destino} (no existe)")

    print(f"\nTotal: {len(broken)} enlaces rotos")

    # Opción borrar
    if args.delete:
        print("\nModo eliminación activado:")

        for link in broken:
            while True:
                resp = input(f"¿Eliminar {link}? [s/n]: ").lower()

                if resp == "s":
                    try:
                        os.remove(link)
                        print("  Eliminado")
                    except Exception as e:
                        print(f"  Error: {e}")
                    break
                elif resp == "n":
                    print("  Saltado")
                    break
                else:
                    print("Respuesta inválida (usar 's' o 'n')")


if __name__ == "__main__":
    main()