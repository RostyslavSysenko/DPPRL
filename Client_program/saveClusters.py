import ClientCommunicator

encoder = ClientCommunicator()
encoder.connectToServer("127.0.0.1", 43555)
encoder.send("SAVECLUSTERS")
encoder.waitForAcknowledge