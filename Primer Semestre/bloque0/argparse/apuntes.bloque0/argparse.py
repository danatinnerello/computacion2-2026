"""
import sys

print(sys.argv)

"""

"""
import sys

if len(sys.argv) < 2:
    print("Uso: python script.py <nombre>")
    sys.exit(1)

nombre = sys.argv[1]
print(f"Hola, {nombre}")

"""


import argparse

parser = argparse.ArgumentParser(description="Procesa un archivo de texto")
"""
parser.add_argument("archivo", help="Archivo a procesar")
parser.add_argument("-v", "--verbose", action="store_true", help="Modo detallado")
parser.add_argument("-n", "--lineas", type=int, default=10, help="Número de líneas")

args = parser.parse_args()

print(f"Procesando {args.archivo}")
print(f"Verbose: {args.verbose}")
print(f"Líneas: {args.lineas}")
"""

"""
parser.add_argument("entrada", help="Archivo de entrada")
parser.add_argument("salida", help="Archivo de salida")

args = parser.parse_args() 

print("Entrada", args.entrada)
print("Salida", args.salida)


"""
"""

parser.add_argument("-o", "--output", default="salida.txt", help="Archivo de salida")
parser.add_argument("-n", "--numero", type=int, default=10, help="Cantidad")


args = parser.parse_args() 

print("Output:", args.output)
print("Número:", args.numero)

"""
"""
parser.add_argument("-v", "--verbose", action="store_true", help="Modo detallado")

args = parser.parse_args() 

print("entrada", args.verbose)

"""

"""
parser.add_argument("--formato", choices=["json", "csv", "xml"], default="json")

args = parser.parse_args() 

print("formato: ", args.formato)

"""
import sys
"""

parser.add_argument(    # permite leer mediante la entrada stdin lo que viene por pipe
    "entrada",
    nargs="?",  # opcional
    type=argparse.FileType('r'),
    default=sys.stdin,
    help="Archivo de entrada (default: stdin)"
)

args = parser.parse_args() 

for linea in args.entrada:
    print(linea)

"""
"""
parser.add_argument(  #define donde va a escribir tu programa
    "-o", "--output",
    type=argparse.FileType('w'),
    default=sys.stdout,
    help="Archivo de salida (default: stdout)"
)


args = parser.parse_args()

args.output.write("Hola mundo\n")

"""
"""
parser = argparse.ArgumentParser()

parser.add_argument(  #para mostrar distintos niveles d einformacion, aumento incremental
    "-v", "--verbose",
    action="count",
    default=0,
    help="Aumentar verbosidad (-v, -vv, -vvv)"
)

args = parser.parse_args()
# Después:
if args.verbose >= 2:
    print("Debug: detalle fino")
elif args.verbose >= 1:
    print("Info: operación normal")

"""

"""
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args = parser.parse_args()

print(args.verbose)
print(args.quiet)

"""
"""

parser = argparse.ArgumentParser(prog="mi-herramienta")
subparsers = parser.add_subparsers(dest="comando")

# Subcomando: init
parser_init = subparsers.add_parser("init", help="Inicializar proyecto")
parser_init.add_argument("nombre", help="Nombre del proyecto")

# Subcomando: build
parser_build = subparsers.add_parser("build", help="Compilar")
parser_build.add_argument("--release", action="store_true")

args = parser.parse_args()

if args.comando == "init":
    print(f"Inicializando {args.nombre}")
elif args.comando == "build":
    print(f"Compilando en modo {'release' if args.release else 'debug'}")

    
    
"""

#!/usr/bin/env python3
"""
Descripción breve de qué hace el script.
"""
import argparse
import sys


def crear_parser():
    """Configura el parser de argumentos."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("archivo", help="Archivo a procesar")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--output", default="salida.txt")

    return parser


def procesar(args):
    """Lógica principal del programa."""
    if args.verbose:
        print(f"Procesando {args.archivo}...")

    # Tu código acá

    return True  # éxito


def main():
    parser = crear_parser()
    args = parser.parse_args()

    try:
        exito = procesar(args)
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\nInterrumpido", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()