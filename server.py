import re
import sys
import socket
import select

from board import Board

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    board = Board()

    votes = {}

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                sockfd.send(str(board).encode("utf-8"))

                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        s = data.decode("utf-8")
                        print("\r" + '[' + str(sock.getpeername()) + '] ' + s)

                        if(re.match("[a-h][1-8]-[a-h][1-8]", s.lower())):
                            s = s.lower().strip()
                            if(s in votes):
                                votes[s] += 1
                            else:
                                votes[s] = 1

                            broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + str(votes) + "\n")

                            if(sum(votes.values()) >= 4):
                                board.turn(votes)
                                broadcast(server_socket, sock, str(board))
                                votes = {}
                        else:
                            broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + s)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                        # exception
                except Exception as e:
                    print(e)
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket:
            try:
                socket.send(message.encode("utf-8"))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


if __name__ == "__main__":
    sys.exit(chat_server())
