# DPPRL
Dynamic Privacy Preserving Record Linkage

Our project is a DPPRL Prototype sponsored by Francisco Partners, who provided us with various research papers, a large sample of synthetic datasets, the BloomFilter.py Module and weekly feedback on our prototype. The aim of the program is to link records from different datasets after applying bloom filter encodings to each record to preserve privacy, we are also aiming to achieve this dynamically by first applying a static record linkage method and then using a cluster matching algorithm to add to the existing clusters. The main goals of our project were to implement our code as an object-oriented design and to make it as modular as possible for compatibility with other opensource code. 

## Linkit Team
LinkIt:![alt text](https://github.com/RostyslavSysenko/DPPRL/blob/main/img/linkitlogo.png "LinkIt PACE Team")
* Amanda Manadeniya
* Harry Sackman
* Majied Sobbi
* Rostyslav Sysenko
* Samreet Kaur

## Program design

![alt text](https://github.com/RostyslavSysenko/DPPRL/blob/main/img/systemdiagram.png  "System Diagram")

## Program usage
This project is divided into two distinct program, there is the server program which runs on the linkage unit and performs the static and/or dynamic linkage; and there is the client program which runs wherever the datasets are stored (data provider).

### Configuration
#### AttributeTypesList.txt
This text file tells the Client program how to encode the input dataset, it exists in the Client_program/Modules/ directory. To use this file, the format should be "AttributeType, AttributeType, AttributeType" in a 3 column dataset so there should be as many AttributeTypes as there are columns to be encoded. AttributeType can be one of the following:
1. NOT_ENCODED
2. STR_ENCODED
3. INT_ENODED

If you are intending to view model evaluation metrics there will need to be a record identifier that remains unencoded to calculate true matches, this can be defined using the attribute type NOT_ENCODED. The other two attribute types are STR_ENCODED and INT_ENCODED for alphanumerical and numerical data respectively.

#### bloomfilter.ini
This file allows the user to customise the bloom filter settings used by FileEncoder when initialising a "BF" object from the BloomFilter.py module. The bloom filter settings include length of bloom filter, number of hash functions, number of intervals to use for similarities, maximum absolute difference allowed, minimum and maximum similarities and length of sub-strings (q-grams)

### Program parameters
For each of the following commands, the "python -u" part may be different depending on where you have python installed on your machine.
#### Linkage unit (Server)
Run the server first, if your working directory is the repo ./DPPRL then use the following syntax:
            python -u ./Server_program/server.py -[options] maximumConnections <portNumber>
Maximum connections is an integer that determines the maximum number of client connections that can be made at one time.
Potential options include:
1. "f" tells the linkage unit to load the cluster list back into memory when launching the server. This cluster list will only exist if it is pickled and saved to the disc when the linkage unit receives a "SAVECLUSTERS" request.
2. "o" tells the linkage unit to used the sorted ordering function instead of random when performing static linkage.
3. "t" tells the linkage unit to expect the similarity threshold (static) and comparison threshold (dynamic) as arguments.
If -t is specified, the syntax will instead be:
            python -u ./Server_program/server.py -t[moreoptions] maximumConnections similarityThreshold comparisonThreshold port
Where the similarityThreshold and comparisonThreshold are decimal values between 0 and 1 indicating the percentage of similarity between records there should be for them to be assigned the same cluster.
portNumber is an optional argument.

#### Client Encoder
The client encoder is a program that facilitates use of a set of 5 synthetic datasets, it can be run using the following syntax: you can  and how many should be used for dynamic.
            python -u ./Client_program/ClientEncoder.py staticDatasets totalDatasets corruption bloomfilterLength
staticDatasets defines how many datasets should be used for static linkage.
totalDatasets defines the total number of datasets (should be greater than static), remaining datasets are all dynamically linked.
Corruption defines which level of corruption will be used.
Bloom filter length is an integer value defining the length of the bloom filter (how many bits are used).
Client encoder will always use the default port 43555, to use a custom port you should run the file encoder.

#### File Encoder
The file encoder can be run using the following syntax:
            python -u ./Client_program/Modules/FileEncoder.py -[options] fileLocation port
fileLocation must be a csv file with 1 header line and columns that match those defined in AttributeTypesList.txt.
Potential options include:
"s" will save the bloom filter encodings locally.
"l" tells the linkage unit to perform static linkage on all currently stored rows after receiving this dataset.
"d" will send encodings as dynamic insertions, adding them to the current clusters one by one.

### Demonstration scripts
On windows, the program demonstration can run without needing to use a CLI. Simply follow the below steps:
1. Run demo.bat inside the DPPRL/Server_program/ directory.
2. Run demo.bat inside the DPPRL/Client_program/ directory.
3. Once the program is complete, the program's performance metrics are displayed along with some matplotlib graphs.
In our tests it took 2 minutes to run, this may vary depending on hardware.

## Future additions to the project
### Data storage
Storing the datasets as JSON takes up a lot of storage space and the datasets do not get loaded back into the model since they are already in the pickled clusterlist, they are stored in this format to enable their usage in SecurityTests. SecurityTests.py was created with the intention of attempting a frequency attack on our bloom filter encodings to test and measure the level of privacy that they actually preserve. In practice, the linkage unit should not store this data on disc as it reduces the complexity of an attack of this nature. Regardless, the encoded rows are all stored in memory so all of the original bloom filter encodings could be recovered with some extra steps either way.

### Configuration
Currently the Server program takes in a lot of parameters such as similarity threshold that could be easier to use if they were stored in a configuration file, ie linkageunit.ini.
