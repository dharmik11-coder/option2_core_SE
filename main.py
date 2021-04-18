import suffix_tree    # to get linear time complexity for better performance
import os

sample_files = ['sample.1', 'sample.2', 'sample.3', 'sample.4', 'sample.5',
                  'sample.6', 'sample.7', 'sample.8', 'sample.9', 'sample.10']

my_dict = {}   #to store filenames and respective hex strings

# Fetching sample files from different directory
active_dir = os.getcwd()
file_path = active_dir + '/sample_files/'

#  populating dictionary with key = filename and value = hex data for every sample file
for file in sample_files:
    with open(file_path + file, 'rb') as f:
        hex_val = f.read().hex()
        my_dict[file] = hex_val
hexdata = list(my_dict.values())

# Building the Suffix Tree and retrieving identical strand with its occurrence in atleast 2 files
suffixTree = suffix_tree.SuffixTree(hexdata)
extracted_strand, indexes, offset = suffixTree.identical_strand()

print("Longest identical strand of bytes found = ", extracted_strand)
print("Length of this strand = ", len(extracted_strand), "units")

# Fetching the offset for extracted strand  in each file
file_names = list(my_dict.keys())
pin_offset = iter(offset)

temp_list = []
for file_number in indexes:
    file = file_names[file_number]
    temp_list.append(file)

file_length = 0
for file in file_names:
    if file in temp_list:
        print("Strand found  at offset = ", next(pin_offset) - file_length, "in file", file)
    file_length += len(my_dict[file]) + 1