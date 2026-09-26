import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost", 9999))

sock.sendall(b"GET")

respuesta = sock.recv(4096).decode()

print("Respuesta del servidor:", respuesta)

sock.close()