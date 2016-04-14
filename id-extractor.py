'''
Created on Apr 14, 2016

@author: rv279r
'''
import re
import os
import json

PRINT_NAME = False
PRINT_COUNT = False
LIMIT_COUNT = 200
COUNT = 0
DIR = os.path.dirname(os.path.realpath(__file__))


def read_extnload(data_file):

    global COUNT
    return_list = []
    read_path = os.path.join(DIR,data_file)

    f = open(read_path,'r')

    for line in f:
        if COUNT == LIMIT_COUNT:
            print "Data Read Limited \n"
            break
        id = re.search('[.*\][a-z]{32}', line)
        name = re.search(r'\[(.*?)\]', line)
        COUNT += 1
        temp_dict = {}
        if id:
            temp_dict['_id'] = id.group(0)
        if name:
            temp_dict['name'] = name.group(1)
        if temp_dict:
            return_list.append(temp_dict)

    return return_list

    f.close()

#idlist.txt OR extn_load.md

raw_data = read_extnload("idlist.txt")
json_data = json.dumps(raw_data)


for id, name in enumerate(d["_id"] for d in raw_data):
    print name

f = open(os.path.join(DIR,'extns.json'),'w')
f.write(json_data)
f.close()
