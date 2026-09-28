def recibir_lineas(sock):
    """Generador que produce líneas completas desde un socket."""
    buffer = b''
    while True:
        pedazo = sock.recv(4096)
        if not pedazo:
            # Conexión cerrada: si quedó algo sin terminar, se descarta
            if buffer:
                print(f'Advertencia: datos incompletos {buffer!r}')
            return
        buffer += pedazo
        # Puede haber varias líneas completas en el buffer
        while b'\n' in buffer:
            linea, buffer = buffer.split(b'\n', 1)
            yield linea