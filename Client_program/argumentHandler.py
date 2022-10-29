import sys
from fieldtype import FieldType
from BloomFilter import BF
from configparser import ConfigParser

class argumentHandler:

    def __init__(self, argv=sys.argv):   
        self.saveOption = False 
        self.dynamicLinkage = False
        self.staticLink = False
        self.host = '127.0.0.1' # Localhost
        self.port = 43555 # Default, can be specified
        self.fileLocation = '' 
        self.attributeList = None
        self.argv = argv
        self.config = None
    
    def handleArguments(self):
        argCount = len(self.argv)        
        optionsExist = self.handleOptions()
        if optionsExist:
            if argCount<3:
                print('Incorrect number of arguments when specifying options')
                sys.exit(1)
        elif argCount < 2:
            print('Requires file path, please specify the csv to be encoded')
            sys.exit(1)
        try:
            if optionsExist:
                self.fileLocation = self.argv[2]
            elif self.argv[1]: # If there are no options then the first parameter will be the file location
                self.fileLocation = self.argv[1]
            print("FileLocation:", self.fileLocation)

            # Find if there is a host argument
            hostArgExists = False
            lastArg = len(self.argv) - 1
            if optionsExist & argCount >= 3:
                hostArgExists = True         
            
            # If specified, set the host and port (otherwise use defaults)
            if hostArgExists:
                hostArg = self.argv[lastArg]
                hostArgSplit = hostArg.split(":")
                self.host = hostArgSplit[0]
                self.port = hostArgSplit[1]
        except:
            print('ClientEncoder.py -options FileToBeEncoded [...] host:port')
            sys.exit(2)

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
                    # Options: s, l, d
                    if char == "s":
                        self.saveOption = True

                    if char == "l":
                        self.staticLink = True

                    if char == "d":
                        self.dynamicLinkage = True  
        return isOptions

    def defineAttributeTypes(self):
        # Read settings from format: NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED
        # Find settings in bloomfilter.ini
        #if self.config == None:
         #   self.findConfig()
        attriTypeList = []
        # Pass txt to a list of FieldTypes (and store self.attributeList for naming purposes)
        attriTypeLocation = "./AttributeTypesList.txt"  
        f = open(attriTypeLocation, 'r')
        typesList = f.readline()
        #typesList = str(self.config["AttributeTypesList"].get('AttributeTypeList'))
        print("Use attribute types:", typesList)
        self.attributeList = typesList.split(', ')
        for i in self.attributeList:   
            field = FieldType[i]
            attriTypeList.append(field)
        
        for i in attriTypeList:
            assert type(i) == FieldType
        assert type(attriTypeList) == list
        self.attributeList = attriTypeList
        return attriTypeList 

    def findConfig(self):
        self.config = ConfigParser()
        self.config.read('bloomfilter.ini')
 

    def findBloomFilterConfig(self):
        # Bloom filter configuration settings in dictionary
        bfs = dict()
        # Initialise default values
        bfs["bf_len"] = 50
        bfs["bf_num_hash_func"] = 2
        bfs["bf_num_inter"] = 5
        bfs["bf_step"] = 1
        bfs["max_abs_diff"] = 20
        bfs["min_val"] = 0
        bfs["max_val"] = 100       
        bfs["q"] = 2

        # Find settings in bloomfilter.ini
        if self.config == None:
            self.findConfig()

        # Use custom settings if they exist
        for setting, value in self.config["bloomfilter"].items():
            bfs[setting] = int(value)

        # Create the bloom filter object and return it.
        bf = BF(bfs['bf_len'], bfs['bf_num_hash_func'], bfs['bf_num_inter'], bfs['bf_step'], bfs['max_abs_diff'], bfs['min_val'], bfs['max_val'], bfs['q'])

        return bf
