import socket


def pedir_con_reintentos(sock, mensaje, destino, intentos=5, timeout=0.5):
    """Manda y reintenta si no llega respuesta."""

    sock.settimeout(timeout)

    for intento in range(1, intentos + 1):
        print(f"Intento {intento}/{intentos}")

        sock.sendto(mensaje, destino)

        try:
            respuesta, _ = sock.recvfrom(65535)
            return respuesta

        except TimeoutError:
            print("  Timeout")

    return None


HOST = "127.0.0.1"
PUERTO = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    mensaje = b"Hola servidor"

    respuesta = pedir_con_reintentos(
        sock,
        mensaje,
        (HOST, PUERTO),
        intentos=5,
        timeout=1.0
    )

    if respuesta is not None:
        print("Respuesta:", respuesta.decode())
    else:
        print("No se obtuvo respuesta después de todos los intentos")