import socketserver
import sys
#from Bot_dev import Bot
from Bot import Bot

bot = Bot();

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024);
        bot.processCommand(self.data);

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True;
    allow_reuse_address = True;

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass);

if __name__ == '__main__':
    HOST = '10.0.0.10';
    PORT = 1103;

    server = Server((HOST, PORT), TCPHandler);

    try:
        server.serve_forever();
    except KeyboardInterrupt:
        sys.exit(0);