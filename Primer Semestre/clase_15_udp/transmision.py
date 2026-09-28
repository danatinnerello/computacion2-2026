import socket
import platform

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.bind(('', 8082))

print("Servidor escuchando en el puerto 8082...")

while True:
    datos, origen = s.recvfrom(4096)

    print(f"Recibido de {origen}: {datos!r}")

    if datos == b'DISCOVER?':
        nombre = platform.node().encode()
        s.sendto(nombre, origen)