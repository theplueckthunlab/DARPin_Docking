"""Script to calculate p2gs scores"""

import numpy as np

#Make a list of clusters
cluster_no = int(raw_input("Number of clusters to calculate: "))
x = range(cluster_no)
clusters = []
for item in x:
	z = "c." + str(item)
	clusters.append(z)

p2gs_list = {}

for c in clusters:
	#Load data from InterfaceAnalyzer
	data = np.loadtxt('Interface_' + c + '.txt', dtype=tuple, skiprows=1)
	
	#Find index
	ind_dG_separated = np.where(data == 'dG_separated')
	ind_packstat = np.where(data == 'packstat')
	ind_sc_value = np.where(data == 'sc_value')
	
	#Find column
	col_dG_separated = ind_dG_separated[1]
	col_packstat = ind_packstat[1]
	col_sc_value = ind_sc_value[1]
	
	#Select values and convert to float
	dG_separated = data[1:,col_dG_separated]
	dG_separeted_float = dG_separated.astype(np.float)
	packstat = data[1:,col_packstat]
	packstat_float = packstat.astype(np.float)
	sc_value = data[1:,col_sc_value]
	sc_value_float = sc_value.astype(np.float)
	
	#Compute means
	mean_dG_separated = np.mean(dG_separeted_float)
	mean_packstat = np.mean(packstat_float)
	mean_sc_value = np.mean(sc_value_float)
	
	#Compute p2gs score
	p2gs = mean_dG_separated * mean_packstat**2 * mean_sc_value
	p2gs_list[c] = p2gs
	print "p2gs score for cluster " + c + " is: " + str(p2gs)
	
print('---------------------------------------------')
print "The best cluster is: " + min(p2gs_list, key=p2gs_list.get)


