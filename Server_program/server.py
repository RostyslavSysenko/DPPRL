import socket
import selectors
import types
import time
import sys

from clustering.staticLinkage import *
from data_structures.ClusterList import ClusterList
from communication.client import client
from communication.serverArgHandler import argumentHandler
from communication.metrics import metrics
from data_structures.Indixer import Indexer

#from clustering import IncrementalClusterInput
#from clustering import DynamicClustering
#from centralDataStructure import ClusterList


class Server:
    def __init__(self, maxConnections):
        self.run = False
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM
        self.server_socket = socket.socket(ipv4, tcp)
        self.selector = selectors.DefaultSelector()
        self.maxConnections = maxConnections
        self.connectedClients = []
        self.indexer = None
        self.clusterlist = ClusterList(certaintyThreshold = 0.8,clusterAggrFunction = AggrFunct.MEAN,indexer = self.indexer)

        self.metric = metrics(self)
        self.startTime = 0

    def runtime(self):
        return time.time() - self.startTime

    def shutdown(self):
        self.selector.close()
        self.server_socket.close() # Will forcefully disconnect clients if still connected
        self.run = False

    def setUpSocketOnCurrentMachine(self, port):
        # Initialise socket
        host = ''
        port = int(port)
        print("Socket successfully created")

        # Bind the socket to a port
        self.server_socket.bind((host, port))
        print("socket binded to %s" % (port))

        # put the socket into listening mode
        self.server_socket.listen(self.maxConnections)  
        print("socket is listening")
        self.server_socket.setblocking(False)
        self.selector.register(self.server_socket, selectors.EVENT_READ, data=None)

        return self.server_socket
        # Local socket setup complete

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
        
    def acceptNewConnection(self, socket):
        # Establish connection with a client.
        client_socket, client_addr = socket.accept()
        print('Got connection from', client_addr)
        # Disable blocking to preventthe server waiting until socket returns data.
        client_socket.setblocking(False)
        data = types.SimpleNamespace(addr=client_addr,inb=b"",outb=b"")        
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # Pass socket and events mask to register
        self.selector.register(client_socket, events, data=data)
        # Create new client object with a unique id     
        id = self.assignId(client_addr)
        if id:
            newClient = client(client_socket, client_addr, self, clientIdentifier=id)
        else:
            newClient = client(client_socket, client_addr, self)
        self.connectedClients.append(newClient)

    def launchServer(self):
        # a forever loop until we interrupt it or an error occurs
        self.run = True        
        self.startTime = time.time()

        while self.run:
            events = self.selector.select(timeout=200) # Select a read or write event on the socket to execute
            for key, mask in events:
                if key.data is None: # This is only true when the event is a new connection
                    self.acceptNewConnection(key.fileobj)
                else:
                    self.serve_client(key, mask)

    def serve_client(self,key, mask):
        connSocket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            rcvd = Server.receive(connSocket, 1024)
            if rcvd: # If a read event was requested on the socket there will be a client message here.
                for connClient in self.connectedClients:
                    if connClient.socket == connSocket:
                        connClient.interpretMessage(rcvd)                        
            else: # If 
                print("Closing connection to: ", mask)
                self.selector.unregister(connSocket)
                connSocket.close()     
        if mask & selectors.EVENT_WRITE: # If a write event was requested, send the message.
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = connSocket.send(data.outb)  # Send message
                data.outb = data.outb[sent:]                             
                
    def assignId(self, clientaddress, checkPreviousConnections=False):
        # assign a number to the client based on it's address
        # Priority 1: Assign a new number to every new connection
        # Priority 2: Store a list that correlates connection address and identifier to reuse identifier - can store in txt for now
        id = 0
        foundPrevious = False
        if checkPreviousConnections:            
            # Use connections.txt (storing in format of "address:clientId \n")

            # for lines in previousConn.txt
                # previousConnection = readline(previousConnections.txt)
                # storedAddress, storedClientId = previousConnection.split(":")
                # looking for a previous connection with the same address
                # if clientaddress == storedAddress
                    # id = storedClientId
                    # foundPrevious = True
            pass
        if not foundPrevious:
            id = self.findHighestId()
        print("ASSIGNED ID:",id)
        return id

    def findHighestId(self):
        highestId = 0 
        # Check id's currently in use and find the highest one.
        for c in self.connectedClients:
            if c.clientId > highestId:
                highestId = c.clientId
        # Found highest id, now add 1 to it and assign it to the new connection.
        highestId += 1
        id = highestId
        return id


    def doStaticLinkage(self, json=True):
        self.clusterlist = ClusterList(indexer=self.indexer)
        # Perform blossom algorithm on 3 inputs

        # Purpose of this function is for demonstration, we will be using first 3 
        # databases as a staticly linked starting point then add 2 more dynamically

        # Input should be all 3 clients records who have sent operation STATIC INSERT.
        foundDb = 0
        dbs = []
        for clients in self.connectedClients:
            assert clients.rowList != None # This indicates static data, if static is done after dynamic this will fail.
            if foundDb < 3:
                #staticRecordList = self.staticLinkageFormatting(clients)
                dbs.append(clients.rowList)
                foundDb += 1
        
        # Static linkage with 3 databases
        # To-Do: Scalable for more than 3, ie any databases entered statically before a static link is called (-l)

        dbCount =len(dbs)
        if dbCount > 3:
            print("MORE THAN 3 DATABASES")
            pass
        elif dbCount < 3:
            print("There are only ", dbCount, " databases, 3 are required.")

        # Initialise indexer
        print("Initialising Indexer")
        listTuples = self.indexerFormatting()
        self.indexer = Indexer(50,listTuples) # Using 50 bit length hardcoded
        self.clusterlist.__indexer = self.indexer

        print("Static Linkage Module calling...")
        # Initialise staticLinker
        staticLink = staticLinker(indexer=self.indexer, metricsIn=self.metric)

        self.metric.beginLinkage
        output = staticLink.staticLinkage(dbs)
        self.metric.finishLinkage()
        print("Static Linkage Module finished")
        for cluster in output:
            assert type(cluster) == Cluster
            self.clusterlist.addClusterStaticly(cluster)
        print("Static Clusters added to linkage unit")


    def indexerFormatting(self):
        """
        This function returns the input required for Indexer module. 
        Hardcoded to use the first encoded integer attribute which is zipcode.
        """     
        returnVal = list()
        city = tuple(("StringAttribute_3",2))
        returnVal.append(city)
        zipcode = tuple(("IntegerAttribute_1",3))
        returnVal.append(zipcode)
        return returnVal
      
    def saveConnectedClients(self):
        # Save current connections to "previousConnections.txt" for later reloading.
        # Stores each client object by mapping address to clientId

        pass

    def findGroundTruth(self):
        rowListInput = []
        for clients in self.connectedClients:
            assert clients.rowList != None
            rowListInput.append(clients.rowList)

        self.metric.findGroundTruth(rowListInput)
        pass

def main():
    # USAGE:
    # server.py -options maxConnections port
    argHandler = argumentHandler(sys.argv)
    argHandler.handleArguments()
    maxConns = argHandler.maxConnections
    port = argHandler.port

    server = Server(maxConns)
    server_socket = server.setUpSocketOnCurrentMachine(port)
    server.launchServer()
    server.shutdown()

if __name__ == "__main__":
    main()
