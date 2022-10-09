from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray
import socket
import sys
import json

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
        self.id = 0
        self.bf = None
        self.encodings = []   
        self.recordDict = bf.__read_csv_file__(self.fileLocation, True, 0)  
        self.fieldnames = [] #self.recordDict.keys()    

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
        
    def redundantAuthorise(self):
        # receive data from the server and decode to get the string.  
    
        print(self.receives())
        # Ask server to authenticate and assign a client ID.

        self.send('AUTH')
        rcvd = self.receives()
        self.id = rcvd
        print("Client ID is ", self.id)

    
    def encodeByAttribute(self, bf):        
        for rec in self.recordDict:
            encodedRecord = ""
            encodedAttributesOfRow = []

            # Populate encoded attributes of row array using the INT/STR datatype key
            for attributeIdx in range(0, len(self.attributeTypesList)):
                currentAttribute = self.recordDict[rec][attributeIdx]
                encodedAttribute = None

                if (self.attributeTypesList[attributeIdx] == FieldType.INT_ENCODED):
                    numerical = int(currentAttribute)
                    intValueSet1, intValueSet2 = bf.convert_num_val_to_set(numerical, 0)  # This part may be unfinished
                    encodedAttribute = bf.set_to_bloom_filter(intValueSet1)
                if (self.attributeTypesList[attributeIdx] == FieldType.STR_ENCODED):
                    encodedAttribute = bf.set_to_bloom_filter(currentAttribute)
                if (self.attributeTypesList[attributeIdx] == FieldType.NOT_ENCODED):
                    encodedAttribute = currentAttribute

                assert encodedAttribute != None, encodedAttribute
                encodedAttributesOfRow.append(str(encodedAttribute))
                
            # Delimit encoded attributes with a comma into a single string
            for i in encodedAttributesOfRow:
                encodedAttr = i.strip("bitarray('')")
                # print(encodedAttr) # Debugging
                encodedRecord += encodedAttr + ","

            # add the encoded string of the row to the list of all encoded rows
            self.encodings.append(encodedRecord)
        # End of loop: for record in record dictionary        

    def display(self, headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0, headRowNumber):
            print(self.encodings[i])
    """
    def saveEncodings(self): # NOT WORKING
        # save self.encodings (list of encoded records stored as strings)
        outputFile = "Encodings.csv"
        #with open(outputFile, "wb") as output:
        #    pickle.dump(self.encodings, output)
        out = self.encodingsToCsvFormat()
        pass
        
    def saveEncoding(self, output): # NOT WORKING
        # save self.encodings (list of encoded records stored as strings)
        #outputFile = output
        #with open(outputFile, "wb") as output:
        #    pickle.dump(self.encodings, output)
        out = self.encodingsToCsvFormat()

        pass
    
    def encodingsToCsvFormat(self):
        
        pass
    """
    def sendEncodingsStatic(self):   
        # Send the encodings for static linkage
        print("Sending dictionary key: ", self.fieldnames)
        #self.send("KEY " + str(self.fieldnames))
        print("Sending encoded data")
        for r in self.encodings:
            # For each record, send as a static insert operation
            cmd = "STATIC INSERT " + str(r)
            self.send(cmd)
            # Wait until server acknowledges record recieved before sending next one.            
            AcknowledgedReceive = False
            while not AcknowledgedReceive:                
                rcvd = self.receives()
                if rcvd.startswith("ACK"):
                    AcknowledgedReceive = True
                    
        rcvd.send("SAVE") # Tell server to save          
                
        # Continue to next record once acknowledged
        #s.send('LIST'.encode())      

    def continuousDynamicLinkage():
        # While True
            # Read CSV
            # Detect changes
            # If there are changes update the linkage unit
        pass    

class argumentHandler:
    def __init__(self):   
        self.saveOption = False 
        self.dynamicLinkage = False
        self.staticLink = False
        self.host = '127.0.0.1'
        self.port = 43555
        self.fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'        
    
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
        # Read a text file in format: FieldType.NOT_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.INT_ENCODED
        # For different dataset fields, modify "AttributeTypesList.txt"
        
        # attriTypeList = [FieldType.NOT_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.INT_ENCODED] # Default value
        attriTypeList = []
        # Pass string to a list
        attriTypeLocation = "./AttributeTypesList.txt"
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()
        print("Attempting to use attribute types: ", typesList)
        splitList = typesList.split(', ')
        for i in splitList:   
            field = FieldType[i]
            #print(field)
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

    print(fileLocation)
    

    

    # Bloom filter configuration settings
    # To Do: Move to a separate configuration file ON SERVER to be received during AUTH request
    bf_len = 50  # 50
    bf_num_hash_func = 2  # 2
    bf_num_inter = 5
    bf_step = 1
    max_abs_diff = 20
    min_val = 0
    max_val = 100
    q = 2

    bf = BF(bf_len, bf_num_hash_func, bf_num_inter, bf_step,
            max_abs_diff, min_val, max_val, q)
            
    #clientEncoder = new FileEncoder()
    #clientEncoder.handleArguments()
    clientEncoder = FileEncoder(attributeTypesList, fileLocation)    
    clientEncoder.encodeByAttribute(bf)
    # If -s "File to output"    
    #clientEncoder.saveEncoding("Filename")
    # Temporary conditionals for testing
    if argHandler.saveOption:
        clientEncoder.saveEncodings()
    else:
        # Diplay the first 5 encodings and then attempt to connect to the server
        print("Sample of encoded data:")
        clientEncoder.display(5)
        clientEncoder.connectToServer(host, port)    

        # If static    
        clientEncoder.sendEncodingsStatic()
        if argHandler.staticLink:
            clientEncoder.send("STATIC LINK")
    
    if argHandler.dynamicLinkage:
        clientEncoder.continuousDynamicLinkage()
    # Stays running, reading the csv file for updates

    # Close the socket and program.
    clientEncoder.soc.close()
    
if __name__ == "__main__":
    main()