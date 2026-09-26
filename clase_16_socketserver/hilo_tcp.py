import socketserver
import threading
from datetime import datetime


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')

        cur_thread = threading.current_thread()
        print("Atendiendo cliente en:", cur_thread.name)

        if data.strip() == "GET":
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            response = bytes(fecha_hora, 'ascii')
        else:
            response = bytes("Comando no reconocido", 'ascii')

        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = True
        server_thread.start()

        print("Server loop running in thread:", server_thread.name)

        server_thread.join()