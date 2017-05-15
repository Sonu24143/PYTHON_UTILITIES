#!/usr/bin/python
from sys import argv
import json
from collections import Counter

    
df_pth = argv[1]

### Opening one pareq file
with open(df_pth,'r') as dfop:
    msg_data_in = dfop.readlines()

### Select 1000 messages from the log file and strip date part 
msg_data_d = msg_data_in[0:100000]
msg_data = list()
for msg in msg_data_d:
    msg_split = msg.split()
    msg_dr = msg_split[2:]
    msg_cmb = " ".join(msg_dr)
    msg_data.append(msg_cmb)
del(msg_cmb,msg,msg_dr,msg_split,df_pth,msg_data_d,msg_data_in)

def word_extractor(string, word_len):
    res_list = list()
    for i in range(len(string)-word_len+1):
        res_list.append(string[i:i+word_len])
    return res_list

len_of_wrd = 5
words_set = list()
for msg in msg_data:
#    words_lst = list()
    if len(msg)<len_of_wrd:
        words_set.append([msg])
    else:
         words_set.append(word_extractor(msg,word_len=len_of_wrd))

words_collection = list()
for lst in words_set:
    words_collection.extend(lst)
    
words_counter = Counter(words_collection)

with open('temp_res.json','w') as ojf:
    json.dump(words_counter,ojf,indent=4)

word_bool_list = list()
for msg in words_set:
    tmp_bool = list()
    for i in range(len(msg)+ len_of_wrd -1):
        tmp_bool.append(0)
    for j in range(len(msg)):
        if words_counter[msg[j]] > 10:
            for k in range(len_of_wrd):
                if tmp_bool[j+k]==0:
                    tmp_bool[j+k] = 1
    word_bool_list.append(tmp_bool)
    
with open('results5.txt','w') as ofin:    
    for i in range(len(msg_data)):
        ofin.write(msg_data[i])
        ofin.write('\n')
        if len(word_bool_list[i])==0:
            ofin.write('\n')
            continue
        for j in range(len(msg_data[i])):
            if word_bool_list[i][j] == 1:
                ofin.write(" ")
            else:
                ofin.write(msg_data[i][j])
        ofin.write('\n\n')
