import argparse
import sys
import secrets
import string

parser = argparse.ArgumentParser(description="creador de contraseñas")

parser.add_argument("-n","--length",nargs="?",type = int,default=12,help="longitud de la contraseña")
parser.add_argument("--no-symbols",action="store_true",help="excluir simbolos especiales")
parser.add_argument("--no-numbers",nargs="?",help="excluir numeros")
parser.add_argument("--count",nargs="?",type=int,default=1,help="cuantas contraseñas generar")

args= parser.parse_args()

if args.length <= 0:
    print(f"Error: la longitud debe ser mayor a 0.")
    sys.exit(1)

if args.count <= 0:
    print(f"Error: count debe ser mayor a 0.")
    sys.exit(1)

caracteres= string.ascii_letters

if not args.no_numbers:
    caracteres= caracteres + string.digits


if not args.no_symbols:
    caracteres= caracteres + string.punctuation

for _ in range(args.count):
    password = ''.join(secrets.choice(caracteres) for _ in range(args.length))
    print(password)

sys.exit(0)