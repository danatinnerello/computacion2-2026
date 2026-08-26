import socket
import struct


def empaquetar(seq, payload):
    return struct.pack("!I", seq) + payload


def desempaquetar(datos):
    (seq,) = struct.unpack("!I", datos[:4])
    return seq, datos[4:]


def pedir_con_reintentos(
    sock,
    mensaje,
    destino,
    seq,
    intentos=5,
    timeout=0.5
):
    """Manda y reintenta si no llega la respuesta correcta."""

    sock.settimeout(timeout)

    # Agregar número de secuencia al mensaje
    pedido = empaquetar(seq, mensaje)

    for intento in range(1, intentos + 1):

        print(f"Intento {intento}/{intentos} - seq={seq}")

        sock.sendto(pedido, destino)

        try:
            datos, _ = sock.recvfrom(65535)

            # Separar seq y respuesta
            seq_respuesta, respuesta = desempaquetar(datos)

            # Verificar que sea la respuesta del pedido actual
            if seq_respuesta != seq:

                print(
                    f"Respuesta descartada: "
                    f"seq={seq_respuesta}, esperaba={seq}"
                )

                continue

            return respuesta

        except TimeoutError:
            print("Timeout")

    return None


HOST = "127.0.0.1"
PUERTO = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    mensaje = input("Ingrese un mensaje: ").encode()

    # Número de secuencia del pedido
    seq = 1

    respuesta = pedir_con_reintentos(
        sock,
        mensaje,
        (HOST, PUERTO),
        seq,
        intentos=5,
        timeout=0.6
    )

    if respuesta is not None:
        print("\nRespuesta del servidor:", respuesta.decode())
    else:
        print("\nNo se recibió respuesta después de todos los intentos.")