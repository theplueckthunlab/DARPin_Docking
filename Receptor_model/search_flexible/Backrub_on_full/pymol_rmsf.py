from pymol import *
import numpy as np
import time
 
""" Aligns all renamed models to template structure"""
#arg1 -- template
#arg2 -- number of structures to calculate (use 250 by default)
#arg3 -- residue range (start-stop).

def fit_unbound(arg1, arg2, arg3):
	for i in range (1, int(arg2)+1):
		cmd.pair_fit (str(i) + "///" + arg3 + "/CA", arg1 + "///" + arg3 + "/CA")
cmd.extend("fit_unbound", fit_unbound);

"""Calculates RMSF of protein segments"""
#arg1 -- template
#arg2 -- number of structures to calculate (use 250 by default)
#arg3 -- size of segments to calculate (use 3 by default)
#arg4 -- indentifier of the first residue
#arg5 -- chain name
#arg6 -- length of the fragment to calculate. Calculate separately for stretches if breaks in chain exist.

def dev_fragment(arg1, arg2, arg3, arg4, arg5, arg6):
	start_time = time.time()
	arg3cor = int(arg3)-1 #correction for pymol numbering
	j=0
	while j < int(arg6)-int(arg3cor):
			list = []
			for i in range (1, int(arg2)+1):
				x=cmd.rms_cur ("/" + str(i) + "//" + arg5 + "/" + str(int(arg4)+j) + "-" + str(int(arg4)+int(arg3cor)+j)
				 + "/CA", "/" + arg1 + "//" + arg5 + "/" + str(int(arg4)+j) + "-" + str(int(arg4)+int(arg3cor)+j) + "/CA")
				list.append(x)
				x = None
			dev = np.std(list)
			print "Fragment: " + str(int(arg4)+j) + "-" + str(int(arg4)+int(arg3cor)+j) + " RMSF: " + str(dev)
			j = j + 1
	print("Dev_fragment took %s seconds" % (time.time() - start_time))
		
cmd.extend("dev_fragment", dev_fragment);