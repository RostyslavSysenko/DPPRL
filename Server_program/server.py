from ast import And
from pydoc import cli
import sys
#sys.path.append('...')
sys.path.append('..')
#sys.path.insert(0, '..')
#from Server_program.centralDataStructure.ClusterList import ClusterList
#from Server_program.data_structures.ClusterList import *
#from Server_program import centralDataStructure
from centralDataStructure import Utilities
import socket



""""
Attributes that we want to store
1. dictionary of encodings (that list will represent different thing based on description above)
        Now JSON not dictionary - to-do
2. type of linkage "static"/"dynamic"
3. operation to be done (if static linkage is done the operation is "insert")
4. row id in a particular database
5. database/dataset id
6. dictionary of unencoded attributes
""" 
class client:
    # Each client is a data provider / unique dataset
    def __init__(self, id, socket, address, server):                
        self.clientId = 0
        self.socket = None
        self.address = None
        self.connectedServer = server
        self.encodedRecords = [] # Using dictionary instead
        # self.clusterlist = data_structures.ClusterList()

    def interpretMessage(self, rcvd):
        assert type(rcvd) == str
        if rcvd.startswith("STATIC INSERT"):
            # Receive encoding into client's encodedRecords List.
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]
            print(rec)
            newRecord = Utilities.Row(rec)
            self.encodedRecords.append(newRecord)                    
            Server.clientSend(self.socket,"ACK")            

        if rcvd.startswith("DYNAMIC INSERT"):
            # Receive encoding
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]                    
            print(rec)
            newRecord = Utilities.Row(rec)
            # self.clusterlist.addRowDynamicNaive(newRecord)

        if rcvd.startswith("DYNAMIC UPDATE"):
            pass

        if rcvd.startswith("DYNAMIC DELETE"):
            pass

        if rcvd.startswith("LIST"):
            for i in self.encodedRecords:
                print(i)
        
        if rcvd.startswith("INFO"):
            # Print info about client.
            print(self.clientId + " ")
            print(self.address + " ")
        
        if rcvd == 'QUIT':
            self.socket.close()
            # remove the client
            self.connectedServer
        
    def encodedDictionary(self):
        recordDict = {}

        return recordDict     


class Server:
    def __init__(self, maxConnections):
        self.run = False
        self.maxConnections = maxConnections
        self.connectedClients = []
        #self.clusterlist = Clustering.ClusterList()
        self.firstdatabase = [] # List of all bloom filters from first database.

    def setUpSocketOnCurrentMachine(self, port):
        host = ''
        port = port
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
        message = str(message)
        encoded = message.encode()
        c.send(encoded)

    def receives(c):
        rMessage = c.recv(1024)
        return rMessage.decode()

    def receive(c, buffer):
        rMessage = c.recv(buffer)
        return rMessage.decode()

    def launchServer(self, server_socket):
        # a forever loop until we interrupt it or an error occurs
        self.run = True
        while self.run:
            # Establish connection with a client.
            client_socket, client_addr = server_socket.accept()
            print('Got connection from', client_addr)
            # Notify client of successful connection
            Server.clientSend(client_socket, 'Connection successful')

            # Client should attempt to authorise            
            rcvd = Server.receive(client_socket, 1024)

            if rcvd == 'AUTH':
                id = self.assignId()                
                Server.clientSend(client_socket, id)  # Tell the client their identifier

                # Create new client object
                newClient = client(id, client_socket, client_addr, self)

                self.connectedClients.append(newClient)

                # Send bloom filter settings here instead of hard coding them.
                # Server.clientSend(client_socket, BF_CONFIG)
                break
            

            # Receive messages from connectedClients
            for clients in self.connectedClients:
                rcvd = Server.receive(clients.socket, 1024)
                if rcvd:
                    print("RECEIVED:", rcvd)
                    client.interpretMessage(rcvd)
                

            #metrics.display()
            # End of run loop                       
                
                
    def assignId(self):
        # connection handling for multiple clients  
        # find currently assigned IDs
        possibleIds = range(1,self.maxConnections)
        currentAssigned = []
        for client in self.connectedClients:
            currentAssigned.append(client.clientId)
        
        # Find lowest available
        lowestAvailable = self.maxConnections
        for id in possibleIds:
            used = False
            for i in currentAssigned:
                if id == i:
                    used = True
            if not used & id < lowestAvailable:
                lowestAvailable = id
        return lowestAvailable


                
            
        
        

def main():
    # Program parameter: maxConnections (default of 5)
    # Program parameter: port

    server = Server(5)
    server_socket = server.setUpSocketOnCurrentMachine(43555)
    server.launchServer(server_socket)


if __name__ == "__main__":
    main()


