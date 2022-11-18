# DPPRL

## What skills this project demonstrates in Rostyslav
- Ability to produce a significant end-end software development/data science project in a team environment and evaluate its performance
- Understanding of key data science algorithms (KNN), evaluation metrics (custom created purity score, time to run), distance measure (cosine similarity), plotting libraries (Matplotlib)
## Project Summary
This project is an open-source functional prototype of DPPRL system where DPPRL stands for dynamic privacy preserving record linkage.  Anyone is welcome to use/adopt this system for any purpose as long as it is done for the good of the world.
## Big picture of our system

Firstly, record linkage is a process in which data from multiple sources is connected together in a way that same entities across different datasets/databases get grouped together. This is relevant because multiple organizations/departments may want to pool certain data together to allow for analytics that is not possible without such pooling. 

Main challenges in record linkage come from the following facts:
 1. Different databases/datasets do not generally identify records with a common unique ID and so we generally can not do the linkage based on the common id
 2. Attributes that are stored across different databases tend to have errors, misspellings and corruptions so matching based on the exact value of some attributes may be problematic.

Despite those challenges, useful record linkage systems already exist, yet our contribution was in building a system that could do the linkage in real time (dynamically) and while preserving the privacy of sensitive attributes based on which the linkage is done. The dynamic property of the system refers to the fact that as new records are entered into source datasets/databases, our DPPRL could quickly and efficiently link those new records to the rest of the records that have already been linked.

At the core of this system are the following ideas:
1. All entities are represented by clusters
2. Similarity based algorithms are used to determine which row from which dataset/database should belong to which cluster
3. bloom filters are used to encode sensitive attributes while preserving the property of similar unencoded attributes having similar similar blum filter encodings.
4. Blocking indexing is used to make things faster

The value of this prototype is in laying the groundwork for next generation DPPRL system and on it own this system as of now is not ready for the real world. More specifically our contributions to the future generation DPPRL systems are outlined below:
- This project produced many reusable classes/modules which can be reused or built up on as part of other DPPRL systems
- This project discovered what things seem to work well and what things don't seem to work well
- This project produced a functional system along with feedback and system evaluation mechanism and suggestions for improvement so that anyone who is willing to work on those, may end up producing something that is practically usable.

## Whats inside the box?
### Static Linkage
The first step in this process was designing a static clustering algorithm that would create initial clusters. Our static algorithm uses early mapping based incremental clustering which was chosen because it ensures that every record is assigned to only one cluster and that there are no clusters with records from the same party. The algorithm graphs each record and calculates the similarity between Bloom filter encodings. Records with similarities above a certain threshold are converged into one, ultimately forming the initial clusters which new records will be dynamically inserted into. 

### Dynamic Linkage
The dynamic linkage was developed with a few tricks in mind:
1. The new row gets inserted into a cluster with the most similar rows assuming the most similar cluster is similar enough. To find the cluster with the most similar rows, we got an aggregate of all rows within a cluster by finding an average of all rows first, second and so on items and then comparing the newly inserted row with such cluster aggregates to see which cluster gets the highest similarity. Our hope here is that cluster aggregate that has highest similarity to newly inserted row will be be the cluster with all of its rows being similar to newly inserted row. If the most similar cluster is not similar enough to the newly inserted row, then newly inserted row gets assigned its own new cluster.
2. Speeding it up: To help speed up the dynamic insertion we used blocking indexing

### client-server architecture
Our communication modules acted as infrastructure for our prototype to simulate the different systems within the distributed computer system described to us. On the client side we processed the data in the following order:
BloomFilter.py module reads the csv file and converts to a python dictionary
FileEncoder module performs bloom filter encoding with the configured settings.
FileEncoder converts the encoded records to JSON and sends them to the server.
On the server side, we maintain a message queue from connecting clients that are handled in order of first received. Some examples of the messages

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
This file allows the user to customize the bloom filter settings used by FileEncoder when initializing a "BF" object from the BloomFilter.py module. The bloom filter settings include length of bloom filter, number of hash functions, number of intervals to use for similarities, maximum absolute difference allowed, minimum and maximum similarities and length of sub-strings (q-grams)

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


## Evaluation of outcomes
To evaluate the system we utilized purity scores (we created a new score and called it purity score even though such metric already exists and means something else) and record of time each dynamic insertion takes. Roughly speaking, what we called purity score is a score that measures the similarity between each cluster our algorithm produced and the most similar cluster in ground truth dataset.

We ran grid search on a reasonable set of parameters and found optimal parameter values for each corruption level

Then we used those best parameter to run on multiple test datasets with 5000 records each on different corruption levels and on the slides are the results we observed.

![image info](./img/0%25%20corruption.png)
![image info](./img/20%25%20corruption.png)
![image info](./img/40%25%20corruption.png)

As can be seen from the first plot, as the number of rows in a cluster list increases, the time it takes the next dynamic insertion to be done growth linearly so the system is quite scalable with respect to number of rows being inserted when there is no corruption. Yet, when there is corruption the system doesn't perform well because then the indexing doesn't quite work. I believe this problems can be fixed easily by increasing the number of attributes on which indexing is done (for multi stage indexing) and once that is done i believe we will have reasonable linear increase in time as more rows are inserted.
Also we can see that across all corruption levels, we are getting a lot of cluster linked perfectly after doing all dynamic insertions but also we are getting a significant amount of clusters very wrong, showing that we are getting some things right, but many things wrong and before this system is usable, major improvements are needed. So while we are getting some utility out of this, it is probably not enough for the system to be deployed in a real world.

Ultimately, we have layed some groundwork in area of DPPRL area , yet as of now the linkage quality isn’t good for real world usage. Ideally we would have liked to have conducted more experimentation to investigate what works well within our system so to improve it, yet we ran out of time. Although there was merit to designing client server architecture, this approach required additional effort that diverted attention away from the core algorithm design and delayed testing and only if we focused more on the core algorithm, maybe we would achieve superior outcome.

## Future Recommendations
### Improving the quality of linkage
To further improve the current version of the prototype we can do the following things:
- We could evaluate the results of running just the static linkage without doing dynamic linkage  to see how good it is on its own so that we can build some understanding of why the performance of the algorithm is low and whether further work needs to be done on improving static or dynamic linkage
- We could check more parameters for Bloom filters and try larger Blume filter lengths to see if that improves the performance because currently our hyper-parameter selection has been limited in scope.
- We could redo the static linkage every once in a while when the system is not being used (at night for example), with the hope that this can improve the performance of the algorithm.
### Further optimizations
Before implementing any of the below recommendations, the system needs to prove itself first since there is no point optimizing the system when it is not useful on the first place.
- Relational Database can be used for persisting cluster lists in memory to help with useful properties like atomicity, isolation, durability and consistency which are not necessarily enforced through the current pickle approach to storing.
Dynamic record update and delete functionalities can be implemented
- GUI can be set up to make the system easier to interact with
We could make the code more modular, documentation clearer and code can be cleaner.
- Configuration: Currently the Server program takes in a lot of parameters such as similarity threshold that could be easier to use if they were stored in a configuration file, ie linkageunit.ini.
- Data Storage: Storing the datasets as JSON takes up a lot of storage space and the datasets do not get loaded back into the model since they are already in the pickled clusterlist, they are stored in this format to enable their usage in SecurityTests. SecurityTests.py was created with the intention of attempting a frequency attack on our bloom filter encodings to test and measure the level of privacy that they actually preserve. In practice, the linkage unit should not store this data on disc as it reduces the complexity of an attack of this nature. Regardless, the encoded rows are all stored in memory so all of the original bloom filter encodings could be recovered with some extra steps either way.