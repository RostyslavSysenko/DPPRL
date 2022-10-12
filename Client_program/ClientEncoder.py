from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray
import pickle 
import socket
import sys
import json

from Server_program.communication.client import client

class FieldType(Enum):
    INT_ENCODED = 1
    STR_ENCODED = 2
    NOT_ENCODED = 3
    
class FileEncoder:
    def __init__(self, attributeTypesList, fileLocation):        
        self.attributeTypesList = attributeTypesList
        self.fileLocation = fileLocation               
    
        self.host = "127.0.0.1"
        self.port = 43555
        self.soc = None
        self.encodings = []   
        self.attributeNames = []
        self.jsonEncodings = []
        self.recordDict = bf.__read_csv_file__(self.fileLocation, True, 0) 

    def send(self, message):
        encoded = message.encode()
        self.soc.send(encoded)

    def receives(self):
        rMessage = self.soc.recv(1024)
        return rMessage.decode()        

    def connectToServer(self, host, port):
        # Server connection
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM
        self.host = host
        self.port = port        

        self.soc = socket.socket(ipv4, tcp)
        print("Client socket successfully created")

        # connecting to the server
        self.soc.connect((self.host, self.port))
        print("the socket has successfully connected to server")       
    
    def encodeByAttribute(self, bf, rec):       
        # Running inside for record in dictionary loop
        encodedAttributesOfRow = []
        encodedRecord = ""
        # Populate encodedAttributesOfRow using the INT/STR attribute type key
        for attributeIdx in range(0, len(self.attributeTypesList)):
            currentAttribute = self.recordDict[rec][attributeIdx]
            encodedAttribute = None

            # Using the input attributeTypesList (stored in the txt), encode attributes accordingly.
            if (self.attributeTypesList[attributeIdx] == FieldType.INT_ENCODED):
                numerical = int(currentAttribute)
                intValueSet1, intValueSet2 = bf.convert_num_val_to_set(numerical, 0)  # 0 is a magic number
                encodedAttribute = bf.set_to_bloom_filter(intValueSet1) 
            if (self.attributeTypesList[attributeIdx] == FieldType.STR_ENCODED):
                encodedAttribute = bf.set_to_bloom_filter(currentAttribute)
            if (self.attributeTypesList[attributeIdx] == FieldType.NOT_ENCODED):
                encodedAttribute = currentAttribute

            assert encodedAttribute != None, encodedAttribute
            # Format as just a string of binary rather than including "bitarray()"
            formattedEncoding = str(encodedAttribute)
            formattedEncoding = formattedEncoding.strip("bitarray('')")
            encodedAttributesOfRow.append(formattedEncoding)

        # Add attributes to encodedRecord string, delimited with a comma.
        for i in encodedAttributesOfRow:         
            encodedRecord += i + ","

        # add the encoded string of the row to the list of all encoded rows
        self.encodings.append(encodedRecord)
        return encodedAttributesOfRow

    def display(self, headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0, headRowNumber):
            print(self.encodings[i])

    def saveEncodings(self): # NOT WORKING
        # save self.encodings (list of encoded records stored as strings)
        outputFile = "Encodings.csv"
        outputFormatted = self.encodingsToCsvFormat()
        with open(outputFile, "wb") as output:
            pickle.dump(outputFormatted, output)
        pass
    
    def encodingsToCsvFormat(self):
        # Extra functionality for product delivery
        pass

    def sendEncodingsStatic(self, json=True):   
        # Send the encodings for static linkage
        print("Sending encoded data")
        if json == False: # Kept old functionality for debugging purposes.
            for r in self.encodings:
                cmd = "STATIC INSERT " + str(r)
                self.send(cmd)
                self.waitForAcknowledge()
        else:
            for r in self.jsonEncodings:
                cmd = "STATIC INSERT " + str(r)
                self.send(cmd)
                self.waitForAcknowledge()
        
        # Each record is sent as a STATIC INSERT as static linkage does not account for UPDATE or DELETE operations.
        self.send("SAVE") # Tell server to save the received encodings after finished sending.

    def waitForAcknowledge(self):
        # Wait until server acknowledges before continuing.        
        AcknowledgedReceive = False
        while not AcknowledgedReceive:                
            rcvd = self.receives()
            if rcvd.startswith("ACK"):
                AcknowledgedReceive = True

    def continuousDynamicLinkage(self):
        # While True
            # Read CSV
            # Detect changes
            # If there are changes update the linkage unit
        pass    

    def nameAttributes(self, argHandler):
        # Populate self.attributeNames using input format: NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED
        attributeTypes = argHandler.attributeList
        # Count instances of NOT/STR/INT
        notCount = 0
        strCount = 0
        intCount = 0

        # Generate unique field names
        index = 0
        count = 0
        for attribute in attributeTypes:
            attributeName = str(attribute)
            if attribute == "NOT_ENCODED":
                notCount += 1
                count = notCount
                attributeName = "UnencodedAttribute_"
            if attribute == "STR_ENCODED":
                strCount += 1
                count = strCount
                attributeName = "StringAttribute_"
            if attribute == "INT_ENCODED":
                intCount += 1
                count = intCount
                attributeName = "IntegerAttribute_"
            else:
                attribute.join("UNCLASSIFIED")
            
            name = attributeName + str(count)
            self.attributeNames.append(name)
            index += 1

        # Make names lowercase
        for attribute in self.attributeNames:
            attribute = attribute.lower()

    def toJson(self, attributes):
        # Using attributeNames array, assign each attribute to a json value.
        thisRecordJson = {}
        index = 0
        for attribute in self.attributeNames:
            if index < len(attributes):
                thisRecordJson[attribute] = attributes[index]
                index += 1

        thisRecordJson = json.dumps(thisRecordJson, indent=1)
        if type(thisRecordJson) == str: # JSON objects are stored as strings in python.
            self.jsonEncodings.append(thisRecordJson)
        else:
            print("ERROR APPENDING JSON RECORD TO LIST")
        return thisRecordJson

class argumentHandler:
    def __init__(self):   
        self.saveOption = False 
        self.dynamicLinkage = False
        self.staticLink = False
        self.host = '127.0.0.1'
        self.port = 43555
        self.fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv' 
        self.attributeList = None
    
    def handleArguments(self):
        argCount = len(sys.argv)
        if argCount<2:
            return 1
        optionsExist = self.handleOptions()
        if optionsExist & argCount<3:
            return 1
        try:
            if optionsExist:
                self.fileLocation = sys.argv[2]
            elif sys.argv[1]: # If there are no options then the first parameter will be the file location
                self.fileLocation = sys.argv[1]

            # Find if there is a host argument
            hostArgExists = False
            lastArg = len(sys.argv) - 1
            if optionsExist & argCount == 3:
                hostArgExists = True         
            
            # If specified, set the host and port (otherwise use defaults)
            if hostArgExists:
                hostArg = sys.argv[lastArg]
                hostArgSplit = hostArg.split(":")
                self.host = hostArgSplit[0]
                self.port = hostArgSplit[1]
        except:
            print('ClientEncoder.py -options FileToBeEncoded [...] host:port')
            sys.exit(2)

    def handleOptions(self):
        isOptions = False
        # Arg 1 - Options (optional)            
        for arg in sys.argv:
            if arg.startswith("-"):
                optionArgument = arg
                isOptions = True
                # Handle options 
                for char in optionArgument:
                    # Options: s, l, d
                    if char == "s":
                        self.saveOption = True

                    if char == "l":
                        self.staticLink = True
                        print("Doing static link")

                    if char == "d":
                        self.dynamicLinkage = True  
        return isOptions

    def defineAttributeTypes(self):
        # Read a text file in format: NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED
        # For a different dataset, modify "AttributeTypesList.txt" to your requirements
        
        attriTypeList = []
        # Pass txt to a list of FieldTypes (and store self.attributeList for naming purposes)
        attriTypeLocation = "./AttributeTypesList.txt"  
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()
        print("Use attribute types from", attriTypeLocation ," : ", typesList)
        self.attributeList = typesList.split(', ')
        for i in self.attributeList:   
            field = FieldType[i]
            attriTypeList.append(field)
        
        for i in attriTypeList:
            assert type(i) == FieldType
        
        return attriTypeList 

def main():
    # USAGE:
    # ClientEncoder.py -options FileToBeEncoded host:port 
   
    argHandler = argumentHandler()
    argHandler.handleArguments()
    fileLocation = argHandler.fileLocation
    host = argHandler.host
    port = argHandler.port
    attributeTypesList = argHandler.defineAttributeTypes()       

    # Bloom filter configuration settings
    # To Do: Move to a separate configuration file
    bf_len = 50
    bf_num_hash_func = 2
    bf_num_inter = 5
    bf_step = 1
    max_abs_diff = 20
    min_val = 0
    max_val = 100
    q = 2

    bf = BF(bf_len, bf_num_hash_func, bf_num_inter, bf_step,
            max_abs_diff, min_val, max_val, q)

    clientEncoder = FileEncoder(attributeTypesList, fileLocation)
    clientEncoder.nameAttributes(argHandler)

    for record in clientEncoder.recordDict:
        encodedAttributes = clientEncoder.encodeByAttribute(bf, record)
        #print(encodedAttributes)
        jsonEncodedRecord = clientEncoder.toJson(encodedAttributes)
        print(jsonEncodedRecord)
  
    # If -s then save encodings in CSV (final delivery / D7, not currently working)
    if argHandler.saveOption:
        clientEncoder.saveEncodings()
    else:
        # Diplay the first 5 encodings and then attempt to connect to the server
        print("Sample of encoded data:")
        clientEncoder.display(5)
        clientEncoder.connectToServer(host, port)    

        # If static    
        clientEncoder.sendEncodingsStatic()
        clientEncoder.waitForAcknowledge()

        if argHandler.staticLink: # This is sent on third dataset for demonstration (-l)
            clientEncoder.send("STATIC LINK")
    
    if argHandler.dynamicLinkage:
        clientEncoder.continuousDynamicLinkage()
        # Stays running, reading the csv file for updates

    # Close the socket and program
    clientEncoder.soc.close()
    
if __name__ == "__main__":
    main()