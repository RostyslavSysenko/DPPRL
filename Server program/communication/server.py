import socket
import pickle
import Clustering
import metrics

""""
bit per attribute

 -> if static
	-> pass list of rows like ["010010","01100101"] for each dataset
  -> "static"
  -> operation is insert only else return to client error
-> if dynamic
  -> "dynamic"
	-> operation {insert,modify,delete}
		-> if insert/delete pass a list of single row
		-> if modification then pass list of 2 rows (old and new)
in short on each iteration of communication we need to pass following

Attributes that we want to pass
1. dictionary of encodings (that list will represent different thing based on description above)
2. type of linkage "static"/"dynamic"
3. operation to be done (if static linkage is done the operation is "insert")
4. row id in a particular database
5. database/dataset id
6. dictionary of unencoded attributes
""" 
class client:
    # Each client is a data provider / unique dataset
    def __init__(self, id, server):                
        self.clientId = 0
        self.socket = None
        self.address = None
        self.connectedServer = server
        self.encodedRecords = [] # Dictionary instead

    def interpretMessage(self, rcvd):
        if rcvd.startswith("STATIC INSERT"):
            # Receive encoding
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]
            #rec = rec.strip("bitarray('')")
            print(rec)
            newRecord = Clustering.Row(rec)
            self.database1.append(newRecord)                    
            Server.clientSend(self.socket,"ACK")
            # Close the connection with the client

        if rcvd.startswith("DYNAMIC INSERT"):
            # Receive encoding
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]                    
            print(rec)
            newRecord = Clustering.Row(rec)
            self.clusterlist.addRowDynamicNaive(newRecord)

        if rcvd.startswith("DYNAMIC UPDATE"):
            pass

        if rcvd.startswith("DYNAMIC DELETE"):
            pass

        if rcvd.startswith("LIST"):
            for i in self.database1:
                print(i)
        
        if rcvd == 'QUIT':
            self.socket.close()
            # remove the client
            self.connectedServer


class Server:
    def __init__(self, maxConnections):
        self.run = False
        self.maxConnections = maxConnections
        self.assignedIds = []
        self.connectedClients = []
        self.clusterlist = Clustering.ClusterList()
        self.firstdatabase = [] # List of all bloom filters from first database.

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

    def receives(self):
        rMessage = self.connection.recv(1024)
        return rMessage.decode()

    def receive(self, c, buffer):
        rMessage = c.recv(buffer)
        return rMessage.decode()

    def launchServer(self, server_socket):
        # a forever loop until we interrupt it or an error occurs
        self.run = True
        while Run:
            # Establish connection with a client.
            client_socket, client_addr = server_socket.accept()
            print('Got connection from', client_addr)
            self.connectedClients.append(client_socket)

            # Notify client of successful connection
            Server.clientSend(client_socket, 'Connection successful')

            if rcvd == 'AUTH':
                id = self.assignId()                
                Server.clientSend(client_socket, id)  # Tell the client their identifier

                # Send bloom filter settings to the new connection

            # Receive messages from connectedClients
            for client in self.connectedClients:
                rcvd = Server.receive(client, 1024)
                if rcvd:
                    print("RECEIVED:", rcvd)
                    client.interpretMessage(rcvd)
                

            metrics.display()
            # End of run loop                       
                
                
    def assignId(self):
        # connection handling for multiple clients                
        allIds = range(1,self.maxConnections)
        availableIds = []
        id = 1
        # Find the lowest available ID
        for currentId in allIds:      
            lowestId = i            
        self.assignedIds.append(id)
        

def main():
    # Program parameter: maxConnections (default of 5)
    # Program parameter: port

    server = Server(5)
    server_socket = server.setUpSocketOnCurrentMachine()
    server.launchServer(server_socket)


if __name__ == "__main__":
    main()


