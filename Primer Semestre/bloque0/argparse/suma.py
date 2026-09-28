
import argparse
import sys

parser = argparse.ArgumentParser(description="Suma numeros")

parser.add_argument("numeros",nargs="*",help="numeros a sumar")

args= parser.parse_args()

suma = 0

for i in args.numeros:
    try:
        suma = suma + float(i)
    except ValueError:
        print(f"{i} no es un numero")
        sys.exit(1)

print(f"suma:{suma}")
sys.exit(0)