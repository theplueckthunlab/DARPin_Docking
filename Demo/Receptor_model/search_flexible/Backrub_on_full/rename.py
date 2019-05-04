""" A script to rename files according to table provided in rename.txt file. Replace the first column in rename.txt with the name of your receptor"""

import os

file = open('rename.txt', 'r')
lines = file.readlines()

for line in lines:
    words = line.split()

column1 = words[0::2]
column2 = words[1::2]

for old_name in column1:
	index=column1.index(old_name)
	new_name=column2[index]
	old = str(old_name)
	new = str(new_name)+".pdb"
	print new
	os.rename(old, new)