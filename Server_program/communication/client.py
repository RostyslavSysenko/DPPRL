""""
Attributes that we want to store per client
1. JSON array with JSON objects per record containing encoded fields
2. type of linkage "static"/"dynamic"
3. operation to be done (if static linkage is done the operation is "insert")
4. row id in a particular database
5. database/dataset id
6. dictionary of unencoded attributes
""" 
import json
import socket
import sys, os

parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)

# Internal imports
from centralDataStructure.Utilities import *
import server

class client:
    # Each client is a data provider / unique dataset
    def __init__(self, soc, address, connserver):   
        # Check correct initialisers
        assert type(soc) == socket.socket 
        # assert type(address) == tuple
        assert type(connserver) == server

        # Initialise values
        self.clientId = 0
        self.socket = soc
        self.address = address
        self.connectedServer = connserver
        self.encodedRecords = [] # Using dictionary instead
        self.dictKey = ['rec_id', 'first_name', 'last_name', 'city', 'zip_code'] # For debugging, receive as json instead.
        # self.clusterlist = data_structures.ClusterList()
        self.jsonRecords = []
        self.jsonFileName = str(self.clientId) + "_records.json"

    def send(self, message):
        message = str(message)
        encoded = message.encode()   
        self.socket.send(encoded)

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
            # Acknowledge received so the client can continue. 
            self.send(self.socket,"ACK")
                                  

        if rcvd.startswith("DYNAMIC INSERT"):
            # Receive encoding
            splitRcvd = rcvd.split(" ")
            rec = splitRcvd[2]
            recJson = self.convertToJson(rec, self.dictKey)    
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
            # This functionality might be superceded by the QUIT command.
            
            # Move this line to reduce amount of writes to disk (especially important for HDD)
            self.saveToJson()  

        # if rcvd.startswith("")
        # More commands to be entered here
        
        if rcvd == 'QUIT':
            # Should save everything (clusters, json objects) before shutting down
            # remove the client socket
            self.socket.close()            
            self.connectedServer.run = False # When the client tells the server to shutdown, it will.       
        

