#!/usr/bin/python
"""
@author: Sonu Jose Parekaden
@Description: This script will help to extract uniquely occuring patterns in a file , by reading through the file 
              separating static and variable parts of a string based on a threshold and then taking the static part
              and getting the occurances of the same throughout the file, configurable parameters are
	      word_length: length of the word we want to tokenize the contents of the file
	      word_repeat_threshold: number of times a word should repeat before we consider it to be a static part
	      ignore_occurance_count: if occurances of a pattern is below a certain count we can ignore it
"""

from sys import argv
from collections import Counter
import operator
    
log_file_path = argv[1]

### Opening one pareq file
with open(log_file_path,'r') as dfop:
    msg_data_in = dfop.readlines()

### Select 1000 messages from the log file and strip date part to avoid anomally in data
msg_data_d = msg_data_in
msg_data = list()
date_time_postion = 5
for msg in msg_data_d:
    msg_split = msg.split()
    msg_dr = msg_split[date_time_postion:]
    msg_cmb = " ".join(msg_dr)
    msg_data.append(msg_cmb)
del(msg_cmb,msg,msg_dr,msg_split,log_file_path,msg_data_d,msg_data_in)

### Tokenizing logic
def word_extractor(string, word_len):
    res_list = list()
    for i in range(len(string)-word_len+1):
        res_list.append(string[i:i+word_len])
    return res_list

### Split each lines into list words of preset size and create a list of them
word_length = 5
words_set = list()
for msg in msg_data:
    if len(msg)<word_length:
        words_set.append([msg])
    else:
         words_set.append(word_extractor(msg,word_len=word_length))

### Merge all the sublists to a single list which will be used for finding repeated occurances of words
words_collection = list()
for lst in words_set:
    words_collection.extend(lst)

### Find the occurances of each word in a file and store them in a dictionary 
words_counter = Counter(words_collection)

### For each line create a list which tells us which part of the string is static and which is dynamic based on a manual threshold
word_bool_list = list()
word_repeat_threshold = 10
for msg in words_set:
    tmp_bool = list()
    for i in range(len(msg)+ word_length -1):
        tmp_bool.append(0)
    for j in range(len(msg)):
        if words_counter[msg[j]] > word_repeat_threshold:
            for k in range(word_length):
                if tmp_bool[j+k]==0:
                    tmp_bool[j+k] = 1
    word_bool_list.append(tmp_bool)
    

### Use the static part and check for the number of occurances of static part, which gives us the occurances
result_holder = list()
for i in range(len(msg_data)):
    tmp_holder = list()
    if len(word_bool_list[i])==0:
        continue
    for j in range(len(msg_data[i])):
          if word_bool_list[i][j] == 1:
		tmp_holder.append(msg_data[i][j])
    result_holder.append("".join(tmp_holder))
    tmp_holder=[]

### Sorting the resulltant dictionary based on the number of occurances of a given pattern
words_counter = Counter(result_holder)
ignore_occurance_count = 1
for word in sorted(words_counter, key=words_counter.get, reverse=True):
    if(words_counter[word] <= ignore_occurance_count):
        continue
    print "PATTERN: ",word
    print "OCCURANCES: ",(words_counter[word])

exit(0)
