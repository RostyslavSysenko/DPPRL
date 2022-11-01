import sys

class argumentHandler:
    def __init__(self, argv):   
        self.argv = argv
        self.port = 43555 # Default
        self.maxConnections = 15 # Default
        self.loadFromFile = False
        self.sortedOrdering = False
        self.thresholdSpecified = False
        self.simThresh = 0.8
        self.compThresh = 0.8
        
    
    def handleArguments(self):
        argCount = len(self.argv)        
        optionsExist = self.handleOptions()
        if optionsExist:
            if argCount<2:
                print('Incorrect number of arguments when specifying options')
                sys.exit(1)
        elif argCount < 1:
            print('Please specify maximum number of connections')
            sys.exit(1)
    
        # No compulsory arguments other than server.py
        if(argCount == 1):
            # There are no user arguments
            return

        if optionsExist:
            self.maxConnections = int(self.argv[2])
        elif self.argv[1]: # If there are no options then the first parameter will be the maxConnections
            self.maxConnections = int(self.argv[1])

        if optionsExist & self.thresholdSpecified:
            self.simThresh = float(self.argv[3])
            self.compThresh = float(self.argv[4])

        elif self.thresholdSpecified:
            self.simThresh = float(self.argv[2])
            self.compThresh = float(self.argv[3])

        # Find if there is a port argument # NEEDS UPDATING FOR IF THRESHOLD VALS
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
                
        #except: "python -u ./Server_program" + ordFunc + 15 + " " + str(statThres) + " " + str(dynThresh) + " " + 43555
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
                    if char == "f":
                        self.loadFromFile = True

                    if char == "o":
                        self.sortedOrdering = True

                    if char == "t":
                        self.thresholdSpecified = True

                    


        return isOptions

    def definePreviousConnections(self):
        """
        Future
        """

        # THIS FUNCTION CAN BE ADAPTED FOR previousConnections
        # Before: storage of connection address to match to clientId/jsonFile
        # And: Load clients from local json files
        
        attriTypeList = []
        # Pass txt to a list of FieldTypes (and store self.attributeList for naming purposes)
        attriTypeLocation = "./AttributeTypesList.txt"  
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()

        pass 

