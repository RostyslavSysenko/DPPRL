import socket


class ClientCommunicator:
    def __init__(self) -> None:
        self.soc = None
        self.host = None
        self.port = None

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
        #print("Client socket successfully created on port", self.port)

        # connecting to the server
        self.soc.connect((self.host, self.port))
        #print("the socket has successfully connected to server")  

    def waitForAcknowledge(self):
        # Wait until server acknowledges before continuing.        
        AcknowledgedReceive = False
        while not AcknowledgedReceive:                
            rcvd = self.receives()
            if rcvd.startswith("ACK"):
                AcknowledgedReceive = True