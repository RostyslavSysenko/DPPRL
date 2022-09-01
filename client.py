import socket;
import sys;
from Encoder import *;

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
fileLocation = '/datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'

# Encode and send to server
Encodings = FileEncoder(attributeTypesList,fileLocation)
FileEncoder.encodeByAttribute(Encodings)
print("Sample of encoded data:")
fileEncoder.display(5)
print("Sending encoded data")
s.send(Encodings.encode())



# Quit
s.send('QUIT'.encode())
s.close()
