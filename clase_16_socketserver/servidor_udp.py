import socketserver


class EchoUDP(socketserver.BaseRequestHandler):
    def handle(self):
        print("self.request:", self.request)
        print("tipo:", type(self.request))


with socketserver.UDPServer(("localhost", 8080), EchoUDP) as server:
    print("Servidor UDP escuchando en 8080")
    server.serve_forever()