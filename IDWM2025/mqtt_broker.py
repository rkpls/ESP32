import usocket as socket
import uselect

class MQTTBroker:
    def __init__(self, port=1883, ws_port=8080, buffer_size=1024):
        self.port = port
        self.ws_port = ws_port
        self.clients = []
        self.buffer_size = buffer_size

    def start(self):
        print(f"Starting MQTT Broker on port {self.port} and WebSocket on {self.ws_port}")
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_sock.bind(('', self.port))
        self.tcp_sock.listen(5)

        self.ws_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ws_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ws_sock.bind(('', self.ws_port))
        self.ws_sock.listen(5)

        self.poll = uselect.poll()
        self.poll.register(self.tcp_sock, uselect.POLLIN)
        self.poll.register(self.ws_sock, uselect.POLLIN)

        while True:
            events = self.poll.poll()
            for sock, event in events:
                if sock == self.tcp_sock:
                    client, addr = self.tcp_sock.accept()
                    print(f"TCP Client connected from {addr}")
                    self.clients.append(client)
                    self.handle_client(client)
                elif sock == self.ws_sock:
                    client, addr = self.ws_sock.accept()
                    print(f"WebSocket Client connected from {addr}")
                    self.clients.append(client)
                    self.handle_client(client)

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(self.buffer_size)
                if not data:
                    break
                print(f"Received data: {data}")
                self.route_message(client, data)
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client.close()
            self.clients.remove(client)

    def route_message(self, client, data):
        # Echo the message to all connected clients
        for c in self.clients:
            if c != client:
                try:
                    c.send(data)
                except Exception as e:
                    print(f"Failed to send message: {e}")

