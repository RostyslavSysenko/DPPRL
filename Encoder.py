from enum import Enum
from logging import exception
from mimetypes import init
from BloomFilter import *;
from enum import Enum
from bitarray import bitarray

class FieldType(Enum):
    INT = 1
    STR = 2

class FileEncoder:
    def __init__(self,attributeTypesList, fileLocation):
        self.attributeTypesList = attributeTypesList
        self.fileLocation = fileLocation
        self.bf = bf
        self.encoding = None

    def encodeByAttribute(self):
        recordDict = bf.__read_csv_file__(self.fileLocation, True, 0)
        allEncodings = []
        
        for rec in recordDict:
            encodedRecord = ""
            encodedAttributesOfRow = bitarray()
            
            #this for loop goes over the row and and encodes each attributes individually
            for attributeIdx in range(0,len(attributeTypesList)):
                currentAttribute = recordDict[rec][attributeIdx]
                encodedAttribute = None
                
                if(self.attributeTypesList[attributeIdx] == FieldType.INT):                    
                    numerical = int(currentAttribute)
                    intValueSet1, intValueSet2 = bf.convert_num_val_to_set(numerical, 0) # This part may be unfinished
                    encodedAttribute = bf.set_to_bloom_filter(intValueSet1)
                if(self.attributeTypesList[attributeIdx] == FieldType.STR):
                    encodedAttribute = bf.set_to_bloom_filter(currentAttribute)                

                assert encodedAttribute != None, encodedAttribute
                encodedAttributesOfRow.extend(encodedAttribute) # This needs to be fixed - doesn't join the bitarrays.

            # Concatenate encoded attributes into a single encoding string
            encodedRecord = "".join(str(encodedAttributesOfRow))

            # add the encoding string of the row to the list of all encoded rows
            allEncodings.append(str(encodedRecord))
        self.encoding = allEncodings

    def display(self,headRowNumber):
        # headRowNumber is the number of rows starting from the top
        for i in range(0,headRowNumber):
            print(self.encoding[i])

# Bloom filter configuration settings
bf_len = 50 #50
bf_num_hash_func = 2 #2
bf_num_inter = 5
bf_step = 1
max_abs_diff = 20
min_val = 0
max_val = 100
q = 2

bf = BF(bf_len, bf_num_hash_func, bf_num_inter, bf_step,
          max_abs_diff, min_val, max_val, q)


"""
attributeTypesList = [FieldType.INT,FieldType.STR,FieldType.STR,FieldType.STR,FieldType.INT]
fileLocation = './datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv'

fileEncoder = FileEncoder(attributeTypesList,fileLocation)

fileEncoder.encodeByAttribute()

"""

