 # option2_core_SE
  **Optimal Solution** for finding the longest strand of bytes that is identical between two or more files from a large set of binary files.

**Input** : A list of 10 given sample binary files.

**Output** : Longest common substring(strand of bytes) that appears in at least two files.
        - the length of the strand
        - the file names where the largest strand appears
        - the offset where the strand appears in each file  

#   Approach :: 
[Similar to k-common substring problem with minor modification]

**Step#1** : Preprocessing input 
- Reading the binary files as strings of hexadecimal values and storing them into a dictonary with key = filename and value = hex strings for each files. 
 (ref: https://stackoverflow.com/questions/34687516/how-to-read-binary-files-as-hex-in-python)
- Create a single list of hex strings by fetching dictionary values which will be compared with each other to find longest common strand of bytes.
- While concatenating strings a unique endpoint value as a punctuation at the end of each string is inserted to identify strings coming from different files.

**Step#2** : Deciding an optimal algorithmic solution for this comparison of hex strings (ref: https://www.geeksforgeeks.org/longest-common-substring-dp-29/)       
-  **SUFFIX TREE** solution for finding longest common substring from strings of length n and m takes a linear time complexity of O(n+m) where as all other approaches takes polynomial time.
-  (ref: http://en.wikipedia.org/wiki/Longest_common_substring_problem)
-  Building a SUFFIX TREE take O(N) linear time complexity.
-  Traversing this tree for k-common substring problem can be solved in O(NK) linear time.
     
**Step#3** : Build Suffix Tree (ref: https://hollywood.zbh.uni-hamburg.de/uploads/pubs/pdf/GieKur1997.pdf)
- I have used McCreight's algorithm to build the suffix tree in linear time.
- (ref: https://www.cs.helsinki.fi/u/tpkarkka/opetus/13s/spa/lecture10-2x4.pdf)
- Class Node and Class SuffixTree in suffix_tree.py (ref: https://www.youtube.com/watch?v=5dgheXY8IZ0&t=69s)
- A function(identical_strand) that returns the identical longest strand, list of indexes, list of offsets of bytes for identical sub-strings in hex list 
      
**Step#4** : Display output using the preprocessed hex list in **main.py** as input for **suffix_tree.py** will return
- the longest common substring(strand of bytes) that appears in at least two files.
- the length of the strand
- the file names where the largest strand appears
- the offset where the strand appears in each file

# Performance ::
**Run-Time Complexity : O(N)** ; N = Σ n(i) where i=1,2,3,...10  & n(i) = length of string in sample file

**Space Complexity : O(n)** ; n=len(concatenated hex string)

# Files:
**main.py** is the main driver file that imports **suffix_tree.py** and uses **/sample_files/** for input files.
