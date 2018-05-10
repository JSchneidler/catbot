import socketserver
from struct import unpack
from Bot import Bot

bot = Bot();

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(2);
        bot.processCommand(self.data);

if __name__ == '__main__':
    HOST = 'localhost';
    PORT = 1103;

    server = socketserver.TCPServer((HOST, PORT), TCPHandler);

    server.serve_forever();