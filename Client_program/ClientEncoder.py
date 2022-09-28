from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray
import socket
import csv

class FieldType(Enum):
    INT_ENCODED = 1
    STR_ENCODED = 2
    NOT_ENCODED = 3
    
class FileEncoder:
    def __init__(self, attributeTypesList, fileLocation):
        self.attributeTypesList = attributeTypesList
        self.fileLocation = fileLocation
        self.fieldnames = []        
        self.host = "127.0.0.1"
        self.port = 43555
        self.soc = None
        self.id = 0
        self.bf = None
        self.encodings = None        

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
        self.soc.connect((host, port))
        print("the socket has successfully connected to server")
        # receive data from the server and decode to get the string.
        print(self.receives())
        # Ask server to authenticate and assign a client ID.

        self.send('AUTH')
        rcvd = self.receives()
        self.id = rcvd
        print("Client ID is ", self.id)

    
    def encodeByAttribute(self, bf):
        recordDict = bf.__read_csv_file__(self.fileLocation, True, 0)
        allEncodings = []

        for rec in recordDict:
            encodedRecord = ""
            encodedAttributesOfRow = []

            # Populate encoded attributes of row array using the INT/STR datatype key
            for attributeIdx in range(0, len(self.attributeTypesList)):
                currentAttribute = recordDict[rec][attributeIdx]
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
            allEncodings.append(encodedRecord)
        # End for record in record dictionary
        self.encodings = allEncodings

    def display(self, headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0, headRowNumber):
            print(self.encodings[i])

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

    def sendEncodingsStatic(self):   
        # Send the encodings for static linkage
        print("Sending encoded data")
        for r in self.encodings:
            # For each record, send as a static insert operation
            cmd = "STATIC INSERT " + str(r)
            self.soc.send(cmd.encode())
            # Wait until server acknowledges record recieved.
            AcknowledgedReceive = False
            while not AcknowledgedReceive:                
                rcvd = self.receives()
                if rcvd.startswith("ACK"):
                    AcknowledgedReceive = True
                
            # Continue to next record once acknowledged
        #s.send('LIST'.encode())      

    def continuousDynamicLinkage():
        # While True
            # Read CSV
            # Detect changes
            # If there are changes update the linkage unit
        pass
'''
    def handleOptions(self,optionArgument):
        # Takes string of letters
        for char in optionArgument:
            if char == "s":
                pass

    def handleArguments(self):
        for i in sys.argv:
            if i.startswith("-"):
                self.handleOptions(i)
            else:
                # If no - at the start set it to the file location
                # To Do: handle last host/port argument (if needed?)
                self.fileLocation = i
'''
    

def main():
    # USAGE:
    # ClientEncoder.py -options FileToBeEncoded host:port
    # Argument defaults / initialisation
    attributeTypesList = [FieldType.NOT_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.INT_ENCODED] # Test this key with all string types.
    fileLocation = '../Client_program/datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'
    dynamicLinkage = False 
    # Extra functionality program parameter: -s (save encodings), output encodings to csv
    saveOption = False 

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
    if saveOption:
        clientEncoder.saveEncodings()
    else:
        # Diplay the first 5 encodings and then attempt to connect to the server
        print("Sample of encoded data:")
        clientEncoder.display(5)
        clientEncoder.connectToServer('127.0.0.1', 43555)    

        # If static    
        clientEncoder.sendEncodingsStatic()
        # clientEncoder.send("STATIC LINK")
        # Disconnect after sending encodings to the server
        clientEncoder.soc.send('QUIT'.encode())
    
    if dynamicLinkage:
        clientEncoder.continuousDynamicLinkage()
    # Stays running, reading the csv file for updates

    # Close the socket and program.
    clientEncoder.soc.close()
    
if __name__ == "__main__":
    main()