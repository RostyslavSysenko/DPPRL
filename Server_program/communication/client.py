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
from data_structures.Utilities import *
from clustering.DynamicClustering import DynamicClusterer

#from server import *

parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)

# Internal imports
from data_structures.Utilities import *

class client:
    # Each client is a data provider / unique dataset
    def __init__(self, soc:socket, address, connserver, clientIdentifier = 0):    
        # Initialise values
        self.clientId = clientIdentifier
        self.socket = soc
        self.address = address
        self.connectedServer = connserver
        self.rowList = []
        self.jsonRecords = []
        self.jsonFileName = str(self.clientId) + "_records.json"
        print("New client with json filename: ", self.jsonFileName)

        self.staticNotDone = False # Used to only print error message once per client who attempts dynamic.

    def send(self, message):
        message = str(message)
        encoded = message.encode()   
        self.socket.send(encoded)

    def saveToJson(self):
        print("Saving JSON list to file: ", self.jsonFileName)
        with open(self.jsonFileName, 'w') as file:
            json.dump(self.jsonRecords, file, indent=1)


    def interpretMessage(self, rcvd):
        assert type(rcvd) == str
                                          
        if rcvd.startswith("STATIC INSERT"):
            # Receive encoding into client's encodedRecords List.
            rec = rcvd.strip("STATIC INSERT ")
            # Load as json to assign a value to DBId
            recJson = json.loads(rec)
            recJson["DBId"] = self.clientId

            self.jsonRecords.append(recJson)
            dumpedJson = json.dumps(recJson)
            newRow = Row.parseFromJson(dumpedJson)
            self.rowList.append(newRow) 
          
            # Acknowledge received so the client can continue. 
            self.send("ACK")
                                  

        if rcvd.startswith("DYNAMIC INSERT"):
            # Receive encoding
            rec = rcvd.strip("DYNAMIC INSERT ")
            recJson = json.loads(rec)
            recJson["DBId"] = self.clientId

            self.jsonRecords.append(recJson)
            dumpedJson = json.dumps(recJson)
            newRow = Row.parseFromJson(dumpedJson)

            # Check if there are cluster aggregations from successful static linkage.
            if self.connectedServer.clusterlist.clusterAggregations:
                self.staticNotDone = False
                #print("CLUSTER AGGREGATIONS:",self.connectedServer.clusterlist.clusterAggregations)
                self.connectedServer.metric.startDynamicInsert()
                self.connectedServer.clusterlist.addRowDynamic(newRow, DynamicClusterer())
                self.connectedServer.metric.finishDynamicInsert()
            elif self.staticNotDone:
                pass
            else:
                self.staticNotDone = True
                print("ERROR UNABLE TO DYNAMICALLY LINK: No cluster aggregations, please complete static linkage first.")

            # Acknowledge received so the client can continue. 
            self.send("ACK")

        if rcvd.startswith("DYNAMIC UPDATE"):
            pass

        if rcvd.startswith("DYNAMIC DELETE"):
            pass

        if rcvd.startswith("LIST"):
            for i in self.encodedRecords:
                print(i)      

        if rcvd.startswith("STATIC LINK"):
            # To do: Controller client on server side that sends this command?
            print("Performing static linkage")
            self.connectedServer.doStaticLinkage()
            
        if rcvd.startswith("SAVE"):
            self.saveToJson() # Move this function call if needed to reduce amount of writes to disk (optimise)
            self.send("ACK") 

        if rcvd.startswith("TRUTH"):
            # Command should be better named
            # Find ground truth using rec_ids
            print("Ground truth requested.")
            self.connectedServer.findGroundTruth()
            self.send("ACK")

        if rcvd.startswith("METRICS"):
            print("Metrics requested")
            self.connectedServer.displayMetrics()

        # if rcvd.startswith("")
        # More commands to be entered here
        
        if rcvd == 'QUIT':
            # Should save everything (clusters, json objects) before shutting down
            # remove the client socket
            self.socket.close()            
            self.connectedServer.run = False # When the client tells the server to shutdown, it will.       
        

