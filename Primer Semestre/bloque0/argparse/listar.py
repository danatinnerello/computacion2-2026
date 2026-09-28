import os
import argparse
import sys

parser = argparse.ArgumentParser(description="lista archivos")

parser.add_argument("directorio",nargs="?",default=".",help="lista archivos")
parser.add_argument("-a","--all",action="store_true")
parser.add_argument("--extension")
args= parser.parse_args()


for archivo in os.listdir(args.directorio):
    if not args.all and archivo.startswith("."):
        continue
    elif args.extension and not archivo.endswith(args.extension):
        continue
    ruta = os.path.join(args.directorio, archivo)
    if os.path.isdir(ruta):
        print(archivo + "/")
        sys.exit(0)
    else:
        print(archivo)
        sys.exit(0)