from ClientEncoder import FileEncoder
from ClientEncoder import argumentHandler


def main():
    argHandler = argumentHandler()
    argHandler.handleArguments()
    fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'   
    host = argHandler.host
    port = argHandler.port
    attributeTypesList = argHandler.defineAttributeTypes()   
    encoder = FileEncoder(attributeTypesList, fileLocation)
    encoder.connectToServer(host, port) 
    print("QUIT") 
    encoder.send("QUIT")

if __name__ == "__main__":
    main()