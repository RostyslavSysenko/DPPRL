import socket
import selectors
import types
import json

# Internal modules
from centralDataStructure import Utilities
#from clustering import staticLinkage
#from clustering import IncrementalClusterInput
#from clustering import DynamicClustering
#from centralDataStructure import ClusterList

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
    def __init__(self, socket, address, server):                
        self.clientId = 0
        self.socket = socket
        self.address = address
        self.connectedServer = server
        self.encodedRecords = [] # Using dictionary instead
        self.dictKey = ['rec_id', 'first_name', 'last_name', 'city', 'zip_code'] # For debugging
        # self.clusterlist = data_structures.ClusterList()
        self.jsonRecords = []
        self.jsonFileName = str(self.clientId) + "_records.json"

    def saveToJson(self):
        jsonfile = open(self.jsonFileName, 'w')
        jsonfile.write(json.dumps(self.jsonRecords))


    def convertToJson(self, input, key):
        assert type(input) == str
        assert type(key) == list

        str(input)
        inputAttributes = input.split(',')

        dict = {}
        counter = 0
        for attribute in key:
            dict[attribute] = inputAttributes[counter]
            counter+=1

            
        jsonString = json.dumps(dict)
        return jsonString

    def interpretMessage(self, rcvd):
        assert type(rcvd) == str

        if rcvd == 'AUTH':
            # Locally assign a client identifier
            id = self.connectedServer.assignId()
            print("New connection was assigned the clientId: ", id)
                                          
        if rcvd.startswith("STATIC INSERT"):
            # Receive encoding into client's encodedRecords List.
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]
            recJson = self.convertToJson(rec, self.dictKey)    
            print(recJson)  
            self.jsonRecords.append(recJson)
            #print(rec) # Debugging
            #newRecord = Utilities.Row(rec)            
            self.encodedRecords.append(#newRecord) 
            rec)                   
            Server.clientSend(self.socket,"ACK")
                                  

        if rcvd.startswith("DYNAMIC INSERT"):
            # Receive encoding
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]     
            recJson = Utilities.convertToJson(rec, self.dictKey)    
            print(recJson)           
            #print(rec) # Debugging
            #newRecord = Utilities.Row.parseFromJson(recJson)
            # self.clusterlist.addRowDynamicNaive(newRecord)

        if rcvd.startswith("DYNAMIC UPDATE"):
            pass

        if rcvd.startswith("DYNAMIC DELETE"):
            pass

        if rcvd.startswith("LIST"):
            for i in self.encodedRecords:
                print(i)
        
        if rcvd.startswith("KEY"):
            # Set the Dict -> JSON key for format conversion
            self.dictKey = rcvd            

        if rcvd.startswith("STATIC LINK"):
            # To do: Controller client on server side that sends this command?
            print("Performing static linkage")
            #self.connectedServer.doStaticLinkage()
            
        if rcvd.startswith("SAVE"):
            # Move this line to reduce amount of writes to disk (especially important for HDD)
            self.saveToJson()  

        # if rcvd.startswith("")
        # More commands to be entered here
        
        if rcvd == 'QUIT':
            # remove the client socket
            self.socket.close()            
            self.connectedServer.run = False # When the client tells the server to shutdown, it will.       
        


class Server:
    def __init__(self, maxConnections):
        self.run = False
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM
        self.server_socket = socket.socket(ipv4, tcp)
        self.selector = selectors.DefaultSelector()
        self.maxConnections = maxConnections
        self.connectedClients = [] # List of client objects
        
        #self.clusterlist = Utilities.ClusterList()
        #self.firstdatabase = [] # List of all bloom filters from first database.
    def shutdown(self):
        self.selector.close()
        self.server_socket.close()

    def setUpSocketOnCurrentMachine(self, port):
        # Initialise socket
        host = ''
        port = port        
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
        # Create new client object            
        newClient = client(client_socket, client_addr, self)
        self.connectedClients.append(newClient)
      
            

    def launchServer(self, server_socket):
        # a forever loop until we interrupt it or an error occurs
        self.run = True        
        while self.run:
            #print("Running") # Debugging
            events = self.selector.select(timeout=200)
            for key, mask in events:
                if key.data is None:
                    self.acceptNewConnection(key.fileobj)
                else:
                    self.serve_client(key, mask)

    def serve_client(self,key, mask):
        connSocket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            rcvd = Server.receive(connSocket, 1024)
            if rcvd:
                print("RECEIVED:", rcvd)
                for connClient in self.connectedClients:
                    if connClient.socket == connSocket:
                        connClient.interpretMessage(rcvd)                        
            else:
                print("Closing connection to: ", mask)
                self.selector.unregister(connSocket)
                connSocket.close()     
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = connSocket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]                             
                
    def assignId(self):
        # connection handling for multiple clients  
        # Find currently assigned IDs

        # NEEDS TO TAKE INTO ACCOUNT CURRENTLY EXISTING JSON FILES AND USE A NAME NOT ALREADY TAKEN
        # also consider the address of the sender, unique address = unique clientId (maybe store this in a log file)

        possibleIds = range(1,self.maxConnections)
        currentlyAssigned = []
        for clients in self.connectedClients:
            currentlyAssigned.append(clients.clientId)
        
        # Find lowest available
        lowestAvailable = self.maxConnections
        for id in possibleIds:
            used = False
            for i in currentlyAssigned:
                if id == i:
                    print("Possible id: ", id, " equal to assigned id: ", i) # Debugging
                    used = True
            if not used & id < lowestAvailable:
                lowestAvailable = id
        return lowestAvailable

    def doStaticLinkage(self):
        # Perform hungarian algorithm on 3 inputs for starting point
        # Default input is any/first 3 clients (temporary)
        # Input should be all clients who have statically inserted.
        foundDb = 0
        for clients in self.connectedClients:
            assert clients.encodedRecords != None
            if foundDb == 0:
                db1 = clients.encodedRecords
                foundDb += 1
            if foundDb == 1:
                db2 = clients.encodedRecords
                foundDb += 1
            if foundDb == 2:
                db3 = clients.encodedRecords
                
            

        # Static linkage with 3 databases
        staticLinkage.staticLinkage(db1, db2, db3)
        pass

    def doDynamicLinkage(self):
        # Update clusters
        pass              
            

def main():
    # Program parameter: maxConnections (default of 5, optional)
    # Program parameter: port
    # Usage: server.py port maxConnections    

    server = Server(15)
    server_socket = server.setUpSocketOnCurrentMachine(43555)
    server.launchServer(server_socket)
    server.shutdown()


if __name__ == "__main__":
    main()


