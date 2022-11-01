# DPPRL
Dynamic Privacy Preserving Record Linkage

Our project was a DPPRL Prototype sponsored by Francisco Partners, who provided us with various research papers, a large sample of synthetic datasets, the BloomFilter.py Module and weekly feedback on our prototype. The aim of the program is to link records from different datasets after applying bloom filter encodings to each record to preserve privacy, we are also aiming to achieve this dynamically by first applying a static record linkage method and then using and indexed cluster matching algorithm to add to the existing list of clusters, stored in a custom ClusterList object. The main goals of our project assigned by our team were to implement our code as an object-oriented design and as modular as possible for compatibility with other opensource code. 




## Program breakdown


### Configuration
#### AttributeTypesList.txt

#### bloomfilter.ini

#### Program parameters

### Classes

### Demonstration scripts


## Future additions to the project
### Data storage
JSON takes up a lot of storage space and the datasets do not get loaded back into the model since they are already in the pickled clusterlist, they are stored in this format to enable the use in SecurityTests which consisted of a frequency attack however there has not yet been a successful implementation. In practice, the linkage unit should not store this data on disc as it cuts out steps for an attacker to acquire the sensitive encoded if they intend to attempt decoding. Though there may be some extra steps to decode, the encoded rows are all stored in the clusterlist object so all of the original bloom filter encodings could be recovered.

### Independent Encoder module that can save encodings and work with multiple datasets
A new encoder class that can work with multiple datasets and optionally without a linkage unit, takes in a naming scheme such as the one used for our synthetic datasets.
