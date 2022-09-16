from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray
import socket


class FieldType(Enum):
    INT = 1
    STR = 2


class FileEncoder:
    def __init__(self, attributeTypesList, fileLocation):
        self.attributeTypesList = attributeTypesList
        self.fileLocation = fileLocation
        self.bf = bf
        self.encodings = None

    def encodeByAttribute(self):
        recordDict = bf.__read_csv_file__(self.fileLocation, True, 0)
        allEncodings = []

        for rec in recordDict:
            encodedRecord = ""
            encodedAttributesOfRow = []

            # Populate encoded attributes of row array using the INT/STR datatype key
            for attributeIdx in range(0, len(self.attributeTypesList)):
                currentAttribute = recordDict[rec][attributeIdx]
                encodedAttribute = None

                if (self.attributeTypesList[attributeIdx] == FieldType.INT):
                    numerical = int(currentAttribute)
                    intValueSet1, intValueSet2 = bf.convert_num_val_to_set(numerical, 0)  # This part may be unfinished
                    encodedAttribute = bf.set_to_bloom_filter(intValueSet1)
                if (self.attributeTypesList[attributeIdx] == FieldType.STR):
                    encodedAttribute = bf.set_to_bloom_filter(currentAttribute)

                assert encodedAttribute != None, encodedAttribute
                encodedAttributesOfRow.append(str(encodedAttribute))
                # encodedAttributesOfRow.extend(encodedAttribute)

            # Concatenate encoded attributes into a single encoding string
            # encodedRecord = "".join(str(encodedAttributesOfRow))

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


# Bloom filter configuration settings
# Extra functionality: Move to a separate configuration file
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

# Client encoding script
ipv4 = socket.AF_INET
tcp = socket.SOCK_STREAM
host = '127.0.0.1'
port = 43555

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

# File parameters
attributeTypesList = [FieldType.INT, FieldType.STR, FieldType.STR, FieldType.STR, FieldType.INT] # Test this key with all string types.
fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'

# Encode the csv using bloom filters
Encoder = FileEncoder(attributeTypesList, fileLocation)
Encoder.encodeByAttribute()
# Extra functionality: Offline mode, do this without connecting to server and output to csv
print("Sample of encoded data:")
Encoder.display(5)


# Send the encodings for static linkage
print("Sending encoded data")
for r in Encoder.encodings:
    cmd = "STATIC INSERT " + str(r)
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

# Quit
s.send('QUIT'.encode())
s.close()
