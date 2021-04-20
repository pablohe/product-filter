import os
from os import walk
total = 0
path = "/misc/projectspace/XBAERout/AOD_AC3r06/"

for root, dirs, files in os.walk(path):
    path = root.split(os.sep)
    for file in files:
        my_file = root +"/"+ file
        print (my_file)
        partial = 0 
        for line in open(my_file): 
            if line[0] != "#":
                total += 1
                partial += 1
        print (partial)

print (total)
