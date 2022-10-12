import sys
from ClientEncoder import FieldType

class argumentHandler:
    def __init__(self):   
        self.saveOption = False 
        self.dynamicLinkage = False
        self.staticLink = False
        self.host = '127.0.0.1'
        self.port = 43555
        self.fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv' 
        self.attributeList = None
    
    def handleArguments(self):
        argCount = len(sys.argv)
        if argCount<2:
            return 1
        optionsExist = self.handleOptions()
        if optionsExist & argCount<3:
            return 1
        try:
            if optionsExist:
                self.fileLocation = sys.argv[2]
            elif sys.argv[1]: # If there are no options then the first parameter will be the file location
                self.fileLocation = sys.argv[1]

            # Find if there is a host argument
            hostArgExists = False
            lastArg = len(sys.argv) - 1
            if optionsExist & argCount == 3:
                hostArgExists = True         
            
            # If specified, set the host and port (otherwise use defaults)
            if hostArgExists:
                hostArg = sys.argv[lastArg]
                hostArgSplit = hostArg.split(":")
                self.host = hostArgSplit[0]
                self.port = hostArgSplit[1]
        except:
            print('ClientEncoder.py -options FileToBeEncoded [...] host:port')
            sys.exit(2)

    def handleOptions(self):
        isOptions = False
        # Arg 1 - Options (optional)            
        for arg in sys.argv:
            if arg.startswith("-"):
                optionArgument = arg
                isOptions = True
                # Handle options 
                for char in optionArgument:
                    # Options: s, l, d
                    if char == "s":
                        self.saveOption = True

                    if char == "l":
                        self.staticLink = True
                        print("Doing static link")

                    if char == "d":
                        self.dynamicLinkage = True  
        return isOptions

    def defineAttributeTypes(self):
        # Read a text file in format: NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED
        # For a different dataset, modify "AttributeTypesList.txt" to your requirements
        
        attriTypeList = []
        # Pass txt to a list of FieldTypes (and store self.attributeList for naming purposes)
        attriTypeLocation = "./AttributeTypesList.txt"  
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()
        print("Use attribute types from", attriTypeLocation ," : ", typesList)
        self.attributeList = typesList.split(', ')
        for i in self.attributeList:   
            field = FieldType[i]
            attriTypeList.append(field)
        
        for i in attriTypeList:
            assert type(i) == FieldType
        
        return attriTypeList 

    def findBloomFilterConfig(self):
        pass
