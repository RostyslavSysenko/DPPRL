import socket
import pickle
import Clustering


# bit per attribute
#  -> if static
# 	-> pass list of rows like ["010010","01100101"] for each dataset
#   -> "static"
#   -> operation is insert only else return to client error
# -> if dynamic
#   -> "dynamic"
# 	-> operation {insert,modify,delete}
# 		-> if insert/delete pass a list of single row
# 		-> if modification then pass list of 2 rows (old and new)
# in short on each iteration of communication we need to pass following
#
# 1. list of row encodings (that list will represent different thing based on description above)
# 2. type of linkage "static"/"dynamic"
# 3. operation to be done

class Server:
    def __init__(self):
        self.clusterlist = Clustering.ClusterList()
        self.database1 = [] # List of all bloom filters from first database.

    def setUpSocketOnCurrentMachine(self):
        host = ''
        port = 43555
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM

        server_socket = socket.socket(ipv4, tcp)
        print("Socket successfully created")

        server_socket.bind((host, port))  # bind socket to a port
        print("socket binded to %s" % (port))

        server_socket.listen(5)  # put the socket into listening mode
        print("socket is listening")

        return server_socket

    def clientSend(c, message):
        encoded = message.encode()
        c.send(encoded)

    def receive(connection):
        rMessage = connection.recv(1024)
        return rMessage.decode()

    def receive(c, buffer):
        rMessage = c.recv(buffer)
        return rMessage.decode()

    def launchServer(self, server_socket):
        # a forever loop until we interrupt it or an error occurs
        while True:
            # Establish connection with client.
            client_socket, client_addr = server_socket.accept()
            print('Got connection from', client_addr)

            # Notify client of successful connection
            Server.clientSend(client_socket, 'Connection successful')

            # addressing all the queries posed by a client to which we connected
            while True:
                # Loop to receive client messages
                rcvd = Server.receive(client_socket, 1024)

                if not rcvd:
                    continue
                print("RECEIVED:", rcvd)

                # Authenticate new client (example function)
                if rcvd == 'AUTH':
                    Server.clientSend(client_socket, "1")  # Tell the client to use id = 1
                    # Extra functionality (low priority): connection handling for multiple clients

                if rcvd.startswith("STATIC INSERT"):
                    # Receive encoding
                    splitRcvd = rcvd.split(" ")
                    rec = splitRcvd[2]
                    #rec = rec.strip("bitarray('')")
                    print(rec)
                    newRecord = Clustering.Row(rec)
                    self.database1.append(newRecord)
                    """            
                    newCluster = Cluster()
                    newCluster.addOneRowToCluster(newRecord)
                    self.clusters.addClusterStaticly(newCluster)
                    #self.database1.append(Row(splitRcvd[2]))
                    """
                    Server.clientSend(client_socket,"ACK")

                    # Close the connection with the client
                if rcvd.startswith("LIST"):
                    for i in self.database1:
                        print(i)

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