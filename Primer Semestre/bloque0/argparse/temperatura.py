import argparse
import sys
parser = argparse.ArgumentParser(description="Convierte temperaturas entre Celsius y Fahrenheit.")

parser.add_argument("valor",type = float,help="temperatura a convertir")
parser.add_argument("-t","--to",choices=["celsius","fahrenheit"],help="{celsius,fahrenheit}")

args= parser.parse_args()

if args.to == "celsius":
    salida = (args.valor - 32)* (5/9) 
    print(f"{args.valor}°F = {salida}°C")
    sys.exit(0)
elif args.to == "fahrenheit":
    salida = (args.valor * (9/5)) + 32 
    print(f"{args.valor}°C = {salida}°F")
    sys.exit(0)
