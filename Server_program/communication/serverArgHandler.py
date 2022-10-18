import sys

class argumentHandler:
    def __init__(self, argv):   
        self.argv = argv
        self.port = 43555 # Default
        self.maxConnections = 15 # Default
        
    
    def handleArguments(self):
        argCount = len(self.argv)        
        optionsExist = self.handleOptions()
        if optionsExist:
            if argCount<3:
                print('Incorrect number of arguments when specifying options')
                sys.exit(1)
        elif argCount < 1:
            print('Please specify maximum number of connections')
            sys.exit(1)
        

        # No compulsory arguments other than server.py
        #try:
        if optionsExist:
            self.maxConnections = int(self.argv[2])
        elif self.argv[1]: # If there are no options then the first parameter will be the maxConnections
            self.maxConnections = int(self.argv[1])

        # Find if there is a port argument
        portArgExists = False
        lastArg = len(self.argv) - 1
        if optionsExist & argCount >= 3:
            portArgExists = True     
        elif argCount >= 3:
            portArgExists = True

        # If specified, set the port (otherwise use defaults)
        if portArgExists:
            portArg = self.argv[lastArg]
            self.port = portArg
                
        #except:
        #    print('server.py -options maxConnections port')
        #    sys.exit(2)

    def handleOptions(self):
        isOptions = False
        # Arg 1 - Options (optional)            
        for arg in self.argv:
            if arg.startswith("-"):
                print("Found options argument: ", arg)
                optionArgument = arg
                isOptions = True
                # Handle options 
                for char in optionArgument:
                    # Options: NOT DECIDED/SPECIFIED YET
                    if char == "s":
                        pass

                    if char == "l":
                        pass

                    if char == "d":
                        pass
        return isOptions

    def definePreviousConnections(self):
        # THIS FUNCTION CAN BE ADAPTED FOR previousConnections
        # Before: storage of connection address to match to clientId/jsonFile
        # And: Load clients from local json files
        
        attriTypeList = []
        # Pass txt to a list of FieldTypes (and store self.attributeList for naming purposes)
        attriTypeLocation = "./AttributeTypesList.txt"  
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()

        pass 

