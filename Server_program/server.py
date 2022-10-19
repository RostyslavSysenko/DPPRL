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
        self.clusterlist = ClusterList()

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
        # Perform hungarian algorithm on 3 inputs

        # Purpose of this function is for demonstration, we will be using first 3 
        # databases as a staticly linked starting point then add 2 more dynamically

        # Input should be all 3 clients records who have sent operation STATIC INSERT.
        foundDb = 0
        dbs = []
        if json:
            for clients in self.connectedClients:
                assert clients.jsonRecords != None
                if foundDb < 3:
                    staticRecordList = self.staticLinkageFormatting(clients)
                    dbs.append(staticRecordList)
                    foundDb += 1
                # find 3 clients
                # make a list of records that are stored as format [rowId, concatenated encodings]
                # pass to db1/2/3 parameters
                pass
        else:
            for clients in self.connectedClients:
                assert clients.encodedRecords != None
                if foundDb < 3:
                    dbs.append(clients.encodedRecords)
                    foundDb += 1
        
        dbCount =len(dbs)
        if dbCount > 3:
            print("MORE THAN 3 DATABASES")
            pass
        elif dbCount < 3:
            print("There are only ", dbCount, " databases, 3 are required.")

        # Initialise indexer
        print("Indexer calling")
        listTuples = self.indexerFormatting()
        self.indexer = Indexer(4,listTuples)

        print("Static Linkage Module calling...")

        # Static linkage with 3 databases
        # To-Do: Scalable for more than 3, ie all databases entered statically
        #statLinker = StaticLinker()

        self.clusterlist = ClusterList(indexer=self.indexer)

        self.metric.beginLinkage
        output = staticLinkage(dbs[0],dbs[1],dbs[2])
        self.metric.finishLinkage()
        print("Static Linkage Module finished (Successfully?)")
        for cluster in output:
            assert type(cluster) == Cluster
            self.clusterlist.addClusterStaticly(cluster)
        print("Clusters added to linkage unit")
        #self.clusterlist = output




        # SHUTDOWN AFTER COMPLETION
        self.shutdown()

    def indexerFormatting(self):
        """
        This class takes the json formatted records that are highly compatible and turns them into the random datatype that Indexer takes.
        """     
        return tuple()


    def staticLinkageFormatting(self, clientObj, force=False):  
        """
        This class takes the json formatted records that are highly compatible and turns them into the random datatype that staticLinkage takes.
        """     
        # Check if formatting is required first.
        formatRequired = True


        if formatRequired:
            print("Joining bloom filters")
            staticRecords = []
            # Create format [[rowId, encodedAttributes],[rowId, encodedAttributes], [rowId, encodedAttributes], ... ]
            for record in clientObj.jsonRecords:
                staticRecord = []
                staticRecord.append(record["rowId"]) # Field 1
                concatBloomFilters = "".join(list(record["encodedAttributes"].values())) 
                staticRecord.append(concatBloomFilters) # Field 2

                # Changed format to dictionary to avoid error on staticLinkage.py: 48 (unhashable type 'dict')
                #staticRecordDict = {}
                #staticRecordDict[staticRecord[0]] = staticRecord[1]
                #staticRecords.update(staticRecordDict) # Add to 'dbs'

                staticRecords.append(staticRecord) # If using list input not dictionary
                #print(staticRecord)
            return staticRecords

    def doDynamicLinkage(self):
        # Update clusters
        self.metric.beginLinkage()
        pass              
            
    def saveConnectedClients(self):
        # Save current connections to "previousConnections.txt" for later reloading.
        # Stores each client object by mapping address to clientId
        
        # See 

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
