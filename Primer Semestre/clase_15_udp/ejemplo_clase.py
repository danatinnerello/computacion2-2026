import socket


def pedir_con_reintentos(sock, mensaje, destino, intentos=3, timeout=1.0):
    """Manda un mensaje y espera respuesta, reintentando si se pierde."""

    sock.settimeout(timeout)

    for intento in range(1, intentos + 1):
        sock.sendto(mensaje, destino)

        try:
            respuesta, _ = sock.recvfrom(65535)
            return respuesta

        except TimeoutError:
            print(f"Intento {intento}: sin respuesta, reintento")

    return None

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    mensaje = b"Hola, servidor"
    destino = ("localhost", 12345)

    respuesta = pedir_con_reintentos(sock, mensaje, destino)

    if respuesta:
        print(f"Respuesta recibida: {respuesta.decode()}")
    else:
        print("No se recibió respuesta después de varios intentos.")
