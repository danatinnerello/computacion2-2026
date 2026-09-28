import sys

if len(sys.argv) < 2:
    print("Uso: saludo.py <nombre>")
    sys.exit(1)

nombre = sys.argv[1]
print(f"Hola, {nombre}!")

#para manejar nombres como maria elena podemos usar 

if len(sys.argv) < 2:
    print("Uso: saludo.py <nombre>")
    sys.exit(1)
elif len(sys.argv) == 3:
    nombre = sys.argv[1] + sys.argv[2]
    print(f"Hola, {nombre}!")
    sys.exit(1)
elif  len(sys.argv) == 2:
    nombre = sys.argv[1] 
    print(f"Hola, {nombre}!")
    sys.exit(0)