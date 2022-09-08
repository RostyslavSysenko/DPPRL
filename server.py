import socket;
import pickle;

class Server:
    def setUpSocketOnCurrentMachine(self):
        host = ''
        port = 43555
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM

        server_socket = socket.socket(ipv4, tcp)
        print("Socket successfully created")

        server_socket.bind((host, port)) # bind socket to a port
        print("socket binded to %s" % (port))

        server_socket.listen(5) # put the socket into listening mode
        print("socket is listening")

        return server_socket

    def clientSend(c,message):
        encoded = message.encode()
        c.send(encoded)

    def receive(connection):
        rMessage = connection.recv(1024)
        return rMessage.decode()

    def receive(c,buffer):
        rMessage = c.recv(buffer)
        return rMessage.decode()

    def launchServer(self,server_socket):
        # a forever loop until we interrupt it or an error occurs
        while True:
            # Establish connection with client.
            client_socket, client_addr = server_socket.accept()
            print('Got connection from', client_addr)

            # Notify client of successful connection
            Server.clientSend(client_socket,'Connection successful')

            # addressing all the queries posed by a client to which we connected
            while True:
                # Loop to receive client messages
                rcvd = Server.receive(client_socket,1024)

                if not rcvd:
                    continue
                print("RECEIVED:", rcvd)

                # Authenticate new client (example function)
                if rcvd == 'AUTH':
                    Server.clientSend(client_socket,"1") # Tell the client to use id = 1
                    # Extra functionality (low priority): connection handling for multiple clients in real time

                if rcvd.startswith("DATA"):
                    data = rcvd.split(" ")
                    print("RECIEVED: ", data)

                if rcvd.startswith("ENCODINGS"):
                    # Identify the size of data being received/sent

                    # Receive encodings
                    pickledEncodings = str(rcvd) # String type conversion is a temporary fix, output not correct!
                    while True:
                        # Receive until no more messages to receive
                        rcvd = client_socket.recv(4096)
                        if not rcvd:
                            break
                        pickledEncodings += str(rcvd)

                    #pickledEncodings = dataRcvd
                    #Encodings = pickle.loads(pickledEncodings) # Fails here
                    print(pickledEncodings)



                # if new condition

                # Close the connection with the client
                if rcvd == 'QUIT':
                    client_socket.close()
                    # Breaking the loop once connection is closed
                    break


def main():
    server = Server()
    server_socket = server.setUpSocketOnCurrentMachine()
    server.launchServer(server_socket)

if __name__ == "__main__":
    main()