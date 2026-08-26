import socket
import struct
import random

HOST = "127.0.0.1"
PUERTO = 5000

contador_trabajo = 0

# Guarda las respuestas de los pedidos que ya fueron procesados
respuestas_guardadas = {}


def empaquetar(seq, payload):
    return struct.pack("!I", seq) + payload


def desempaquetar(datos):
    (seq,) = struct.unpack("!I", datos[:4])
    return seq, datos[4:]


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, PUERTO))

    print(f"Servidor escuchando en {HOST}:{PUERTO}")

    while True:
        datos, direccion = sock.recvfrom(65535)

        seq, mensaje = desempaquetar(datos)

        print(f"\nPedido recibido - seq={seq}: {mensaje.decode()}")

        # Verificar si ya se procesó este pedido
        if seq in respuestas_guardadas:

            print(f"Duplicado detectado: seq={seq}")
            print("No se vuelve a ejecutar el trabajo.")

            respuesta = respuestas_guardadas[seq]

        else:

            # Trabajo real
            contador_trabajo += 1

            print(f"Trabajo ejecutado. Total: {contador_trabajo}")

            # Ejemplo de trabajo: convertir a mayúsculas
            respuesta = mensaje.upper()

            # Guardar respuesta para futuros duplicados
            respuestas_guardadas[seq] = respuesta

        # Simular pérdida de respuestas
        if random.random() < 0.6:
            print("Respuesta perdida")
            continue

        # Mandar respuesta con el mismo seq
        respuesta_empaquetada = empaquetar(seq, respuesta)

        sock.sendto(respuesta_empaquetada, direccion)

        print("Respuesta enviada")