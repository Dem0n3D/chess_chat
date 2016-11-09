import sys
import socket
import select

from threading import Thread

class ConsoleReader(Thread):

    def __init__(self, sock):
        super(ConsoleReader, self).__init__()

        self.sock = sock

    def run(self):
        while 1:
            # user entered a message
            msg = sys.stdin.readline()
            self.sock.send(msg.encode("utf-8"))
            sys.stdout.write('[Me] ');
            sys.stdout.flush()


def chat_client():
    if (len(sys.argv) < 3):
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ');
    sys.stdout.flush()

    t = ConsoleReader(s)
    t.start()

    while 1:
        socket_list = [s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    try:
                        sys.stdout.write(data.decode("utf-8"))
                    except AttributeError:
                        sys.stdout.write(data)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())
