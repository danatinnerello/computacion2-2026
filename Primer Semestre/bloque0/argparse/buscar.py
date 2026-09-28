import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("patron")
parser.add_argument("archivos",nargs="*")

parser.add_argument("-i","--ignore-case", action="store_true")
parser.add_argument("-c","--count",action="store_true")
parser.add_argument("-v","--invert",action="store_true")

args = parser.parse_args()

total = 0
#hay archivos
if args.archivos:
    for archivo in args.archivos:
        try:
            f= open(archivo)
            contador= 0

            for i,linea in enumerate(f,start=1):
                linea = linea.strip() #limpia saltos de lineas

                #aplica ignore-case
                texto = linea
                patron = args.patron

                if args.ignore_case:
                    texto = texto.lower()
                    patron = patron.lower()

                # ver si coincide
                if patron in texto:
                    match = True
                else:
                    match = False

                # invierte si -v
                if args.invert:
                    match = not match

                if match:
                    contador += 1

                    if not args.count:
                        print(f"{archivo}:{i}: {linea}")
            
            if args.count:
                print(f"{archivo}: {contador} coincidencias")
                total += contador

            f.close()

        except:
            print(f"No se pudo abrir {archivo}")
            sys.exit(1)

    if args.count and len(args.archivos) > 1:
        print(f"Total: {total} coincidencias")
        sys.exit(0)

#Si NO hay archivos :stdin
else:
    if not sys.stdin.isatty():
        for linea in sys.stdin:
            linea = linea.strip()

            texto = linea
            patron = args.patron

            if args.ignore_case:
                texto = texto.lower()
                patron = patron.lower()

            if patron in texto:
                match = True
            else:
                match = False

            if args.invert:
                match = not match

            if match:
                print(linea)

#stdin = entrada estandar: es de donde lee datos un programa