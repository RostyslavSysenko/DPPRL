# BF - Bloom filter program to convert string, numerical 
# (integer, floating point) and modulus values that have finite range
# (e.g., longitude and latitude with range 0-360 degrees) into Bloom filters to 
# allow privacy-preserving similarity calculations.
#
# DV, Mar 2015
# -----------------------------------------------------------------------------
#
# imports
#

# Standard Python modules
import math
import random
import hashlib
import gzip
import os

random.seed(9318)

from bitarray import bitarray
import matplotlib
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------

class BF():

  def __init__(self, bf_len, bf_num_hash_func, bf_num_inter, bf_step, 
               max_abs_diff, min_val, max_val, q):
    """Initialisation, set class parameters:
       - bf_len            Length of Bloom filters
       - bf_num_hash_func  Number of hash functions
       - bf_num_interval   Number of intervals to use for BF based similarities

       - max_abs_diff      Maximum absolute difference allowed
       - min_val           Minimum value 
       - max_val           Maximum value
       - q                 Length of sub-strings (q-grams)
    """

    self.bf_len =           bf_len
    self.bf_num_hash_func = bf_num_hash_func
    self.bf_num_inter =     bf_num_inter
    self.bf_step = 	    bf_step

    self.max_abs_diff =  max_abs_diff
    self.min_val =       min_val
    self.max_val =       max_val

    self.q = q

    assert max_val > min_val

    # Bloom filter shortcuts
    #
    self.h1 = hashlib.sha1
    self.h2 = hashlib.md5

  # ---------------------------------------------------------------------------

  def set_to_bloom_filter(self, val_set):
    """Convert an input set of values into a Bloom filter.
    """

    k = self.bf_num_hash_func
    l = self.bf_len

    bloom_set = bitarray(l)  # Convert set into a bit array		
    bloom_set.setall(False)
         
    for val in val_set:
      hex_str1 = self.h1(val.encode('utf-8')).hexdigest() #self.h1(val).hexdigest()
      int1 =     int(hex_str1, 16)
      hex_str2 = self.h2(val.encode('utf-8')).hexdigest() #self.h2(val).hexdigest()
      int2 =     int(hex_str2, 16)

      for i in range(k):
        gi = int1 + i*int2
        gi = int(gi % l)
        bloom_set[gi] = True
      
    return bloom_set

  # ---------------------------------------------------------------------------

  def calc_bf_sim(self, bf1, bf2):
    """Calculate Dice coefficient similarity of two Bloom filters.
    """

    bf1_1s = bf1.count()
    bf2_1s = bf2.count()

    common_1s = (bf1 & bf2).count()

    dice_sim = (2.0 * common_1s)/(bf1_1s + bf2_1s)
      
    return dice_sim

  # ---------------------------------------------------------------------------

  def calc_abs_diff(self, val1, val2):
    """Calculate absolute difference similarity between two values based on the
       approach described in:

       Data Matching, P Christen, Springer 2012, page 121, equations (5.28).
    """

    max_abs_diff = self.max_abs_diff

    if (val1 == val2):
      return 1.0

    abs_val_diff = abs(float(val1) - float(val2))

    if (abs_val_diff >= max_abs_diff):
      return 0.0  # Outside allowed maximum difference

    abs_sim = 1.0 - abs_val_diff / max_abs_diff

    assert abs_sim > 0.0 and abs_sim < 1.0, (val1, val2, abs_sim)

    return abs_sim

  # ---------------------------------------------------------------------------

  def calc_str_sim(self, val1, val2):
    """Calculate dice-coefficient similarity between two strings (non-encoded).
    """
    # Length of sub-strings (q-grams) to be extracted from string values
    #
    q = self.q # q-gram length

    val1_set = [val1[i:i+q] for i in range(len(val1) - (q-1))]  
    val2_set = [val2[i:i+q] for i in range(len(val2) - (q-1))]

    num_items_val1 = len(list(set(val1_set)))
    num_items_val2 = len(list(set(val2_set)))
    num_common_items = len(list(set(val1_set) & set(val2_set)))

    dice_sim = (2.0 * num_common_items) / (num_items_val1 + num_items_val2)

    return dice_sim

  # ---------------------------------------------------------------------------

  def calc_cate_sim(self, val1, val2):
    """Calculate similarity between two categorical values (non-encoded).
       - exact matching
    """
    if val1 == val2:
      sim = 1.0
    else:
      sim = 0.0

    return sim

  # ---------------------------------------------------------------------------

  def convert_str_val_to_set(self, val1, val2):
    """Covert string values into lists to be hash-mapped into the Bloom filters.
    """

    # Length of sub-strings (q-grams) to be extracted from string values
    #
    q = self.q # q-gram length

    val1_set = [val1[i:i+q] for i in range(len(val1) - (q-1))]  
    val2_set = [val2[i:i+q] for i in range(len(val2) - (q-1))]  

    return val1_set, val2_set


  # ---------------------------------------------------------------------------

  def convert_num_val_to_set(self, val1, val2):
    """Covert numeric values into lists to be hash-mapped into the Bloom filters.
    """

    # Number of intervals and their sizes (step) to consider
    #
    bf_num_inter = self.bf_num_inter
    bf_step =           self.bf_step

    val1_set = set()
    val2_set = set()

    rem_val1 = val1 % bf_step  # Convert into values within same interval
    if rem_val1 >= bf_step/2:
      use_val1 = val1 + (bf_step - rem_val1)
    else:
      use_val1 = val1 - rem_val1

    rem_val2 = val2 % bf_step
    if rem_val2 >= bf_step/2:
      use_val2 = val2 + (bf_step - rem_val2)
    else:
      use_val2 = val2 - rem_val2

    val1_set.add(str(float(use_val1)))  # Add the actual value
    val2_set.add(str(float(use_val2)))  # Add the actual value

    # Add variations larger and smaller than the actual value
    #
    for i in range(bf_num_inter+1):
      diff_val = (i+1)*bf_step
      val1_set.add(str(use_val1 - diff_val))
      val2_set.add(str(use_val2 - diff_val))

      diff_val = (i)*bf_step
      val1_set.add(str(use_val1 + diff_val))
      val2_set.add(str(use_val2 + diff_val))

    return val1_set, val2_set

  # ---------------------------------------------------------------------------

  def calc_mod_diff(self, val1, val2):
    """Calculate difference similarity between two modulus values that have finite range
       (in contrast to integer and floating point values that have infinite range).
    """

    max_abs_diff = self.max_abs_diff
    min_val = self.min_val
    max_val = self.max_val

    if (val1 == val2):
      return 1.0

    mod_val_diff = float((max_val - max(val1,val2)) + (min(val1,val2)-min_val)+1)
    #print mod_val_diff
    if (mod_val_diff >= max_abs_diff):
      return 0.0  # Outside allowed maximum difference

    mod_sim = 1.0 - mod_val_diff / max_abs_diff

    assert mod_sim > 0.0 and mod_sim < 1.0, (val1, val2, mod_sim)

    return mod_sim

  # ---------------------------------------------------------------------------

  def convert_mod_val_to_set(self, val1, val2):
    """Convert modulus values into sets to be hash-mapped
       into Bloom filters.
    """

    # Number of intervals and their sizes (step) to consider
    #
    bf_num_inter = self.bf_num_inter
    bf_step =           self.bf_step

    min_val = self.min_val
    max_val = self.max_val

    val1_set = set()
    val2_set = set()

    rem_val1 = val1 % bf_step  # Convert into values within same interval
    if rem_val1 >= bf_step/2:
      use_val1 = val1 + (bf_step - rem_val1)
    else:
      use_val1 = val1 - rem_val1

    rem_val2 = val2 % bf_step
    if rem_val2 >= bf_step/2:
      use_val2 = val2 + (bf_step - rem_val2)
    else:
      use_val2 = val2 - rem_val2

    val1_set.add(str(float(use_val1)))  # Add the actual values
    val2_set.add(str(float(use_val2)))  # Add the actual values

    # Add variations larger and smaller than the actual value
    #
    for i in range(bf_num_inter+1):

      diff_val = (i+1)*bf_step
      prev_val1 = use_val1 - diff_val
      if prev_val1 < min_val:
        val1_set.add(str(prev_val1 + (max_val-min_val+1)))
      else:
        val1_set.add(str(prev_val1))
      prev_val2 = use_val2 - diff_val
      if prev_val2 < min_val:
        val2_set.add(str(prev_val2 + (max_val-min_val+1)))
      else:
        val2_set.add(str(prev_val2))

      diff_val = (i)*bf_step
      next_val1 = use_val1 + diff_val
      if next_val1 > max_val:
        val1_set.add(str(next_val1%(max_val-min_val)))
      else:
        val1_set.add(str(next_val1))
      next_val2 = use_val2 + diff_val
      if next_val2 > max_val:
        val2_set.add(str(next_val2%(max_val-min_val)))
      else:
        val2_set.add(str(next_val2))

    return val1_set, val2_set

  # ---------------------------------------------------------------------------

  def __read_csv_file__(self, file_name, header_line, rec_id_col=None):
    """This method reads a comma separated file and returns a dictionary where
       the keys are the unique record identifiers (either taken from the file
       or assigned by the function) and the values are lists that contain the
       actual records.

       Arguments:
       - file_name    The name of the CSV file to read. If the file ends with
                      a '.gz' extension it is assumed it is GZipped.
       - header_line  A flag, True or False, if True then the first line is
                      assumed to contain the column (attribute) names and it
                      is skipped.
       - rec_id_col   The number (starting from 0) of the column that contains
                      unique record identifiers. If no such are available in
                      the file then this value must be set to None (default).
                      In this case each record is given a unique integer
                      number as identifier.
    """

    assert header_line in [True,False]

    rec_dict = {}  # Dictionary to contain the read records

    in_file =  open(file_name, 'r', encoding="utf8")  # Open normal file

    # Skip header line if necessary
    #
    if (header_line == True):
      header_line = in_file.readline()  # Skip over header line
    #print(header_line)
    rec_count = 0

    for rec in in_file:
      rec = rec.lower().strip()
      rec_list = rec.split(',')

      if (rec_id_col == None):
        rec_id = str(rec_count)  # Assign unique number as record identifier
      else:
        rec_id = rec_list[rec_id_col]  # Get record identifier from file

      assert rec_id not in rec_dict, ('Record ID not unique:', rec_id)

      rec_dict[rec_id] = rec_list

      rec_count += 1
    #print rec_dict
    return rec_dict



##########################################################

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


#numerical - integer
val1 = 29
val2 = 30
true_sim = bf.calc_abs_diff(val1,val2)
val1_set, val2_set = bf.convert_num_val_to_set(val1,val2)
bf1 = bf.set_to_bloom_filter(val1_set)
bf2 = bf.set_to_bloom_filter(val2_set)
bf_sim = bf.calc_bf_sim(bf1,bf2)
#print(val1,val2,true_sim, bf_sim)

output_file = open('results.csv', 'w')
output_file.write(str(val1)+','+str(val2)+','+str(true_sim)+','+str(bf_sim)+ '\n')

#string
val1 = 'dinusha'
val2 = 'vinusha'
true_sim = bf.calc_str_sim(val1,val2)
val1_set, val2_set = bf.convert_str_val_to_set(val1,val2)
bf1 = bf.set_to_bloom_filter(val1_set)
bf2 = bf.set_to_bloom_filter(val2_set)
bf_sim = bf.calc_bf_sim(bf1,bf2)
#print(val1,val2,true_sim,bf_sim)
output_file.write(str(val1)+','+str(val2)+','+str(true_sim)+','+str(bf_sim)+'\n')


#categorical
val1 = 'female'
val2 = 'female'
true_sim =bf.calc_cate_sim(val1,val2)
val1_set = [val1]
val2_set = [val2]
bf1 = bf.set_to_bloom_filter(val1_set)
bf2 = bf.set_to_bloom_filter(val2_set)
bf_sim = bf.calc_bf_sim(bf1,bf2)
#print(val1,val2,true_sim,bf_sim)

output_file.write(str(val1)+','+str(val2)+','+str(true_sim)+','+str(bf_sim)+'\n')


#numerical - modulus that has a finite range between 0 and 100 only
val1 = 99
val2 = 1
true_sim = bf.calc_mod_diff(val1,val2)
val1_set, val2_set = bf.convert_mod_val_to_set(val1,val2)
bf1 = bf.set_to_bloom_filter(val1_set)
bf2 = bf.set_to_bloom_filter(val2_set)
bf_sim = bf.calc_bf_sim(bf1,bf2)
#print(val1,val2,true_sim, bf_sim)

output_file.write(str(val1)+','+str(val2)+','+str(true_sim)+','+str(bf_sim)+'\n')


#numerical - integer
val1 = 99
val2 = 1
true_sim = bf.calc_abs_diff(val1,val2)
val1_set, val2_set = bf.convert_num_val_to_set(val1,val2)
bf1 = bf.set_to_bloom_filter(val1_set)
bf2 = bf.set_to_bloom_filter(val2_set)
bf_sim = bf.calc_bf_sim(bf1,bf2)
#print(val1,val2,true_sim, bf_sim)





'''
sim_thresh = 0.8
matches = []
rec_dict_Alice = bf.__read_csv_file__('1730_50_overlap_alice.csv',True, 0)
#rec_dict_Bob = bf.__read_csv_file__('1730_50_overlap_bob_mod_0.csv',True, 0)
rec_dict_Bob = bf.__read_csv_file__('1730_50_overlap_bob_mod_1.csv',True, 0)


for rec in rec_dict_Alice:
  val1 = rec_dict_Alice[rec][1] #fname - use [2] for lname, [3] for city, [4] for postcode
  val1_set = [val1]
  bf1 = bf.set_to_bloom_filter(val1_set)
  for recB in rec_dict_Bob:
    val2 = rec_dict_Bob[recB][1] #fname
    true_sim = bf.calc_str_sim(val1,val2)
    val2_set = [val2]
    bf2 = bf.set_to_bloom_filter(val2_set)
    bf_sim_fname = bf.calc_bf_sim(bf1,bf2)
    #bf_sim_lname = xxxx
    #bf_sim_age = xxxx
    #overall_sim = (bf_sim_fname + bf_sim_lname + bf_sim_age)/3.0
    #if overall_sim > sim_thresh:
    # xxxx
    if bf_sim_fname > sim_thresh:
      matches.append([rec,recB])
      print(val1,val2,bf_sim_fname,true_sim)
      output_file.write(recA+','+recB+','+bf1.to01()+','+bf2.to01()+','+str(overall_sim)+os.linesep)


    
num_matches_found = len(matches)
num_true_matches = 1730/2
num_true_matches_found = 0
for mm in matches:
  if mm[0] == mm[1]: #check if the rec IDs are the same
    num_true_matches_found += 1

precision = num_true_matches_found/num_matches_found
recall = num_true_matches_found/num_true_matches
f1 = 2* precision * recall / (precision + recall)

print(precision, recall, f1)


#read and plot results
in_res_file = open('results.csv','r', encoding="utf8")

Y_values = []
match_sims = []
nmatch_sims = []
X_values = []
num_recs = 0
for line in in_res_file:
  num_recs += 1
  line_list = line.split(',')
  Y_values.append(float(line_list[-1])) #[0.8, 0.4, 0.7, 0.9, 0.3,...]
  X_values.append(num_recs) #[1,2,3,4,5,6,7,8,9,10]
  if line_list[0] == line_list[1]:
    match_sims.append(float(line_list[-1]))
  else:
    nmatch_sims.append(float(line_list[-1]))

X_vlaue_m = [x for x in range(len(match_sims))]
X_vlaue_n = [x for x in range(len(nmatch_sims))]

plt.plot(X_vlaue_m, match_sims, label='matches')
plt.plot(X_vlaue_n, nmatch_sims, label='nmatches')


plt.plot(X_values, Y_values, label='female')

plt.savefig('sim_dist.eps')
plt.show()
'''
