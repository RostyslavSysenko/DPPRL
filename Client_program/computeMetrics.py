#from ClientEncoder import FileEncoder
#from ClientEncoder import argumentHandler
from ClientCommunicator import ClientCommunicator
# 

def main():
    encoder = ClientCommunicator()
    encoder.connectToServer("127.0.0.1", 43555)
    
    # Connect to server and tell them to:
    encoder.send("METRICS")

if __name__ == "__main__":
    main()