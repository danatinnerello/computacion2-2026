import argparse
import sys
import json

parser = argparse.ArgumentParser()

parser.add_argument("archivo")
parser.add_argument("--keys", action="store_true")
parser.add_argument("--get")
parser.add_argument("--pretty", action="store_true")
parser.add_argument("--set", nargs=2)
parser.add_argument("-o", "--output")

args = parser.parse_args()

#Leer JSON
if args.archivo == "-":
    data = json.load(sys.stdin)
else:
    try:
        f = open(args.archivo)
        data = json.load(f)
        f.close()
    except:
        print("Error al abrir el archivo")
        sys.exit(1)

#Funcion simple para navegar con puntos
def obtener_valor(data, ruta):
    partes = ruta.split(".")

    actual = data
    for p in partes:
        if p.isdigit():
            actual = actual[int(p)]
        else:
            actual = actual[p]
    return actual

#imprime claves de nivel principal
if args.keys:
    for k in data:
        print(k)

#usando la funcion anterior busca un valor navegando dentro del archivo
elif args.get:
    valor = obtener_valor(data, args.get)
    print(json.dumps(valor, indent=4))

#lo deja formateado
elif args.pretty:
    print(json.dumps(data, indent=4))

#modifica un valor dentro del archivo
elif args.set:
    ruta = args.set[0]
    nuevo_valor = args.set[1]

    partes = ruta.split(".")
    actual = data

    #navega hasta el ultimo
    for p in partes[:-1]:
        if p.isdigit():
            actual = actual[int(p)]
        else:
            actual = actual[p]

    ultima = partes[-1]

    # convertir valor
    if nuevo_valor.lower() == "true":
        nuevo_valor = True
    elif nuevo_valor.lower() == "false":
        nuevo_valor = False
    elif nuevo_valor.isdigit():
        nuevo_valor = int(nuevo_valor)

    if ultima.isdigit():
        actual[int(ultima)] = nuevo_valor
    else:
        actual[ultima] = nuevo_valor

    salida = json.dumps(data, indent=4)

    if args.output:
        with open(args.output, "w") as f:
            f.write(salida)
        print(f"Guardado en {args.output}")
    else:
        print(salida)


# echo '{"a": 1}' | python jsonproc.py - --get "a"
#se crea un json  lo pasa como entrada  le dice al programa lee desde stdin