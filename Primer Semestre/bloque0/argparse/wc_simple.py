
import argparse
import sys

parser = argparse.ArgumentParser(description="cuenta lineas de un archivo")

parser.add_argument("archivo",nargs="*",help="contar lineas")

args= parser.parse_args()

if len(args.archivo) == 0:
    print(f"Error: debe especificar un archivo")
    sys.exit(1)
else:
    try:
        with open(args.archivo[0]) as f:
             contador = 0
             for linea in f:
                 contador = contador +1 
        print(f"{contador} lineas")
        sys.exit(0)
    except FileNotFoundError:
        print(f"Error: no se puede leer '{args.archivo[0]}'")
        sys.exit(1)


    