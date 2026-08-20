import struct

def recibir_exacto(sock, n):
    """Lee exactamente n bytes, o devuelve None si la conexión se cerró antes."""
    datos = b''
    while len(datos) < n:
        pedazo = sock.recv(n - len(datos))
        if not pedazo:
            return None                  # cerró antes de completar
        datos += pedazo
    return datos

def enviar_mensaje(sock, payload: bytes):
    """Envía longitud (4 bytes, big-endian) seguida del contenido."""
    sock.sendall(struct.pack('!I', len(payload)) + payload)

def recibir_mensaje(sock):
    """Recibe un mensaje con prefijo de longitud."""
    cabecera = recibir_exacto(sock, 4)
    if cabecera is None:
        return None
    (longitud,) = struct.unpack('!I', cabecera)
    return recibir_exacto(sock, longitud)