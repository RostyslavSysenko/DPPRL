import socket;
import sys;
from Encoder import *;
import pickle;

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
attributeTypesList = [FieldType.INT,FieldType.STR,FieldType.STR,FieldType.STR,FieldType.INT]
fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'

# Encode the csv using bloom filters
Encoder = FileEncoder(attributeTypesList,fileLocation)
Encoder.encodeByAttribute()
print("Sample of encoded data:")
Encoder.display(5)

# Send the encodings
print("Sending encoded data")
s.send("ENCODINGS".encode())
serializedEncodings = pickle.dumps(Encoder.encoding) # Serialization
s.send(serializedEncodings)



# Quit
s.send('QUIT'.encode())
s.close()
