import socket
from select import select

class Server:
    def __init__(self, port):
        self.inputs = [];
        self.outputs = [];

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.server.setblocking(0);
        self.server.bind(('localhost', port));
        self.server.listen(1);

        self.inputs.append(self.server);

        print('Server listening on port ' + str(port));

    def poll(self):
        result = None;

        if self.server:
            readable, writable, exceptional = select(self.inputs, self.outputs, self.inputs);

            for s in readable:
                if s is self.server:
                    # New connection
                    connection, client_address = s.accept();
                    connection.setblocking(0);
                    self.inputs.append(connection);
                else:
                    # Data from client
                    data = s.recv(2);
                    if data:
                        result = data;
                        if s not in self.outputs:
                            self.outputs.append(s);
                    else:
                        if s in self.outputs:
                            self.outputs.remove(s);
                        self.inputs.remove(s);
                        s.close();

        return result;

        '''
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait();
            except Queue.Empty:
                outputs.remove(s);
            else:
                s.send(next_msg);

        for s in exceptional:
            inputs.remove(s);
            if s in outputs:
                outputs.remove(s);
            s.close();
            del message_queues[s];
        '''
