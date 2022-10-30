from BloomFilter import *
import socket
import json
import sys
from ClientCommunicator import ClientCommunicator
from argumentHandler import *

class FileEncoder:
    """
    This class is called on a data provider's computer and 
    """
    def __init__(self, bf, communicator, argHandler=argumentHandler(sys.argv)): # Only input to initialise should be the argumentHandler object
        argHandler.handleArguments
        if argHandler.attributeList == None:
            argHandler.defineAttributeTypes()
        self.attributeTypesList = argHandler.attributeList
        self.fileLocation = argHandler.fileLocation          
    
        self.host = "127.0.0.1"
        self.port = 43555
        self.soc = None
        self.encodings = []   
        self.attributeNames = []
        self.jsonEncodings = []
        self.recordDict = bf.__read_csv_file__(self.fileLocation, True, 0)      

        self.communicator = communicator
    
    def encodeByAttribute(self, bf, rec):       
        # Running inside a for record in dictionary loop
        encodedAttributesOfRow = []
        encodedRecord = ""
        # Populate encodedAttributesOfRow using the INT/STR attribute type key
        #print("Attempting to use attributeTypesList of datatype: ",type(self.attributeTypesList))
        for attributeIdx in range(0, len(self.attributeTypesList)):
            currentAttribute = self.recordDict[rec][attributeIdx]         

            encodedAttribute = None
            attributeType = self.attributeTypesList[attributeIdx]
            # Use the input attributeTypesList to encode attributes accordingly.
            if attributeType.name == "INT_ENCODED" and currentAttribute.isnumeric():
                numerical = int(currentAttribute)
                intValueSet1, intValueSet2 = bf.convert_num_val_to_set(numerical, 0)  # 0 is a magic number
                encodedAttribute = bf.set_to_bloom_filter(intValueSet1) 
            elif attributeType.name == "STR_ENCODED":
                encodedAttribute = bf.set_to_bloom_filter(currentAttribute)
            elif attributeType.name == "NOT_ENCODED":
                encodedAttribute = currentAttribute
            else:
                print("FAILED TO ENCODE ATTRIBUTE: ", currentAttribute)
                print("TRIED USING: ", attributeType.name)

            assert encodedAttribute != None
            # Format as just a string of binary rather than including "bitarray()"
            formattedEncoding = str(encodedAttribute)
            formattedEncoding = formattedEncoding.strip("bitarray('')")
            encodedAttributesOfRow.append(formattedEncoding)

        # Add attributes to encodedRecord string, delimited with a comma.
        for i in encodedAttributesOfRow:         
            encodedRecord += i + ","

        # add the encoded string of the row to the list of all encoded rows
        self.encodings.append(encodedRecord)
        return encodedAttributesOfRow

    def display(self, headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0, headRowNumber):
            print(self.jsonEncodings[i])

    def saveEncodings(self):
        jsonFileName = "encodings.json"
        print("Saving JSON list to file: ", jsonFileName)
        with open(jsonFileName, 'w') as file:
            json.dump(self.jsonEncodings, file, indent=1)

        # Currently outputs a bunch of \n newline characters 
        
    def sendEncodingsStatic(self, json=True):   
        # Send the encodings for static linkage
        print("Sending encoded data")
        if json == False: # Kept old functionality for debugging purposes.
            for r in self.encodings:
                cmd = "STATIC INSERT " + str(r)
                self.communicator.send(cmd)
                self.communicator.waitForAcknowledge()
        else:
            for r in self.jsonEncodings:
                cmd = "STATIC INSERT " + str(r)
                self.communicator.send(cmd)
                self.communicator.waitForAcknowledge()
        
        # Each record is sent as a STATIC INSERT as static linkage does not account for UPDATE or DELETE operations.

    def nameAttributes(self, argHandler):
        # Populate self.attributeNames using input format: NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED
        attributeTypes = argHandler.attributeList
        # Count instances of STR/INT
        strCount = 0
        intCount = 0

        # Generate unique field names
        index = 0
        count = 0
        for attribute in attributeTypes:
            attributeName = str(attribute.name)
            attributeIsId = False

            # Determine which attribute type, then decide how to name
            if attributeName == "NOT_ENCODED": # Only 1 value is not encoded so counting is not required (we assume this is the unique identifier)
                attributeIsId = True
                name = "rowId"
            elif attributeName == "STR_ENCODED":
                strCount += 1
                count = strCount
                attributeName = "StringAttribute_"
            elif attributeName == "INT_ENCODED":
                intCount += 1
                count = intCount
                attributeName = "IntegerAttribute_"
            else:
                attributeName=("UNCLASSIFIED")
            
            if attributeIsId:
                self.attributeNames.append(name)
            else:
                name = attributeName + str(count)
                self.attributeNames.append(name)
                index += 1

        # Make names lowercase
        for attribute in self.attributeNames:
            attribute = attribute.lower()

    def toJson(self, attributes):
        # Using attributeNames array, assign each attribute to a json value.
        thisRecordJson = {"encodedAttributes":{}}
        index = 0
        for attribute in self.attributeNames:
            if index < len(attributes):
                if attribute == 'rowId':
                    thisRecordJson[attribute] = attributes[index]
                    index += 1
                else:
                    thisRecordJson["encodedAttributes"][attribute] = attributes[index]
                    index += 1               

        thisRecordJson = json.dumps(thisRecordJson, indent=1)
        if type(thisRecordJson) == str: # JSON objects are stored as strings in python.
            self.jsonEncodings.append(thisRecordJson)
        else:
            print("Error appending json record to list, datatype was not a string!")
        return thisRecordJson

    def sendEncodingsDynamic(self):
        # Send the encodings for dynamic linkage
        print("Sending DYNAMICALLY")
        for r in self.jsonEncodings:
            cmd = "DYNAMIC INSERT " + str(r)
            self.communicator.send(cmd)
            self.communicator.waitForAcknowledge()

    def checkRecordComplete(self, rec):
        for attributeIdx in range(0, len(self.attributeTypesList)):
            currentAttribute = self.recordDict[rec][attributeIdx]
            if currentAttribute == None:
                print("Attribute in record did not exist, record completion check failed.")
                return False
            if currentAttribute == '':
                print("Attribute in record did not exist, record completion check failed.")
                return False
        
        # If runs without returning False,
        return True

def main():
    # USAGE:
    # ClientEncoder.py -options FileToBeEncoded host:port    
    argHandler = argumentHandler(sys.argv)
    argHandler.handleArguments()
    bf = argHandler.findBloomFilterConfig()

    comm = ClientCommunicator()

    clientEncoder = FileEncoder(bf,comm,argHandler=argHandler)
    clientEncoder.nameAttributes(argHandler)

    # Perform encoding
    for record in clientEncoder.recordDict:
        # Only encode records that are complete
        recordContainsAllFields = clientEncoder.checkRecordComplete(record)

        if (record != None) & recordContainsAllFields:
            encodedAttributes = clientEncoder.encodeByAttribute(bf,record)
            #print(encodedAttributes)
            jsonEncodedRecord = clientEncoder.toJson(encodedAttributes)
            #print(jsonEncodedRecord)


    # Diplay the first 5 encodings
    print("Sample of encoded data:")
    clientEncoder.display(5)
    # If -s then save encodings locally in json (final delivery / D7, not currently working)
    if argHandler.saveOption:
        clientEncoder.saveEncodings()
    # Attempt to connect to the server
    clientEncoder.communicator.connectToServer(argHandler.host, argHandler.port)  

    if not argHandler.dynamicLinkage:       
        # Send static insertions
        clientEncoder.sendEncodingsStatic()
        clientEncoder.communicator.send("SAVE") # Tell server to save the received encodings after finished sending.
        clientEncoder.communicator.waitForAcknowledge()

        if argHandler.staticLink: # This is sent on third dataset for demonstration (-l)
            clientEncoder.communicator.send("STATIC LINK")
    
    if argHandler.dynamicLinkage:
        # Send dynamic insertions
        clientEncoder.sendEncodingsDynamic()
        clientEncoder.communicator.send("SAVE") # Tell server to save the received encodings after finished sending.
        clientEncoder.communicator.waitForAcknowledge()

    # Close the socket and exit the program when all encodings have been sent.
    clientEncoder.communicator.soc.close()
    
if __name__ == "__main__":
    main()
