from ClientCommunicator import ClientCommunicator
# Simple program to maunually close the server application if it is stuck running in the IDE.

def main():
    encoder = ClientCommunicator()
    encoder.connectToServer("127.0.0.1", 43555)
    
    # Connect to server and tell them to:
    encoder.send("QUIT")

if __name__ == "__main__":
    main()