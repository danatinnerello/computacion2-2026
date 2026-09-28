import socket
"""
with socket.create_connection(('localhost', 8080)) as s:
    s.sendall(b'hola mundo\n')
    while True:
        pedazo = s.recv(4)          # de a 4 bytes a propósito
        if not pedazo:
            break
        print(f'recv devolvió: {pedazo!r}')"""
with socket.create_connection(('localhost', 8080)) as s:
    s.sendall(b'peticion completa')
    s.shutdown(socket.SHUT_WR)          # avisa que terminó
    respuesta = b''
    while True:
        pedazo = s.recv(4096)
        if not pedazo:
            break
        respuesta += pedazo