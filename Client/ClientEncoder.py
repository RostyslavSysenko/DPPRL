from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray
import socket
import pickle

class FieldType(Enum):
    INT_ENCODED = 1
    STR_ENCODED = 2
    NOT_ENCODED = 3
    
class FileEncoder:
    def __init__(self, attributeTypesList, fileLocation, host, port):
        self.attributeTypesList = attributeTypesList
        self.fileLocation = fileLocation
        self.host = "127.0.0.1"
        self.port = 43555
        self.bf = bf
        self.encodings = None

    def connectToServer(self, host, port):
        # Server connection
        ipv4 = socket.AF_INET
        tcp = socket.SOCK_STREAM
        self.host = host
        self.port = port
        

        s = socket.socket(ipv4, tcp)
        print("Client socket successfully created")

        # connecting to the server
        s.connect((host, port))
        print("the socket has successfully connected to server")
        # receive data from the server and decode to get the string.
        print(s.recv(1024).decode())
        # Ask server to authenticate and assign a client ID.

        s.send('AUTH'.encode())
        rcvd = s.recv(1024).decode()
        id = rcvd
        print("Client ID is ", id)

    
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
                print(encodedAttr)
                encodedRecord += encodedAttr + ","

            # add the encoded string of the row to the list of all encoded rows
            allEncodings.append(encodedRecord)

        self.encodings = allEncodings

    def display(self, headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0, headRowNumber):
            print(self.encodings[i])

    def saveEncodings(self):
        # save self.encodings (list of encoded records stored as strings)
        outputFile = "Enc_" + self.fileLocation
        with open(outputFile, "wb") as output:
            pickle.dump(self.encodings, output)
        
    def saveEncoding(self, output):
        # save self.encodings (list of encoded records stored as strings)
        outputFile = output
        with open(outputFile, "wb") as output:
            pickle.dump(self.encodings, output)

    def sendEncodingsStatic(self):         
        # Extra functionality: Offline mode, do this without connecting to server and output to csv
        print("Sample of encoded data:")
        self.display(5)

        # Send the encodings for static linkage
        print("Sending encoded data")
        for r in self.encodings:
            cmd = self.id + " STATIC INSERT " + str(r)
            s.send(cmd.encode())
            AcknowledgedReceive = False
            while True:
                rcvd = s.recv(1024).decode()
                if rcvd.startswith("ACK"):
                    AcknowledgedReceive = True
                if AcknowledgedReceive:
                    break
            # Continue to next record once acknowledged
        #s.send('LIST'.encode())      

    



def main():
    # parameters    
    attributeTypesList = [FieldType.RECORD_ID, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.STR_ENCODED, FieldType.INT_ENCODED] # Test this key with all string types.
    fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'
    # Program parameter: Dynamic or static parameter

    def parameter (attributeTypesList,clientEncoder):

    if attributeTypesList > clientEncoder:
        return attributeTypesList

    else

    return clientEncoder:



    



    # Extra functionality program parameter: -s (save encodings), output encodings to csv


    # Bloom filter configuration settings
    # Extra functionality: Move to a separate configuration file ON SERVER to be received during AUTH request
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
    
    clientEncoder = FileEncoder(attributeTypesList, fileLocation)
    clientEncoder.connectToServer('127.0.0.1', 43555)
    clientEncoder.encodeByAttribute(bf)

    # If -s "File to output"    
    #clientEncoder.saveEncoding("Filename")
    # Else if -s
    clientEncoder.saveEncodings()

    

    # If no -t
    clientEncoder.sendEncodingsStatic()
    # Disconnect after sending encodings to the server
    s.send('QUIT'.encode())
    s.close()


    # If -t
    clientEncoder.continuousDynamicLinkage()
    
if __name__ == "__main__":
    main()