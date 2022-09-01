import socket;

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

            # send a thank you message to the client. encoding to send byte type.
            clientSend(client_socket,'Thank you for connecting')

            # addressing all the queries posed by a client to which we connected
            while True:
                # Loop to receive client messages
                rcvd = client_socket.recieve(client_socket)
                if not rcvd:
                    continue
                print("RECEIVED:", rcvd)

                # Authenticate new client (example function)
                if rcvd == 'AUTH':
                    client_socket.send(client_socket,"1") # Tell the client to use id = 1
                # Close the connection with the client

                if rcvd.startswith("DATA"):
                    data = rcvd.split(" ")
                    print("RECIEVED: ", data)

                # if new condition
            
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