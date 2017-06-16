#!/usr/bin/python

import logging
import glob
from collections import OrderedDict as OD

def read_cnv(name, variant_info):
	"""
		Input: CNV files
		----------
	    	Function: extract parameters out of CNV file
		----------
		Output: fills the dictionnary in, 2 def's above

	"""

	range_pos_all = list()	
	range_pos = dict()
	
	source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/X.home.*%s*'% (name, variant_info['origin']))
	#print source
	for files in source:
		#print files
		present = open(files, 'rb')			
		next(present)	# skip header

		for line in present:
			if float(line.split('\t')[4]) <= 8:
				range_pos = OD([
					('gene_id', str()),
					('chr', str()),
					('begin', int()),
					('end', int()),
					('cnv_state', str())
					])						
				range_pos['gene_id'] = str(line.split('\t')[0])
				range_pos['chr'] = str(line.split('\t')[1])
				range_pos['begin'] = int(line.split('\t')[2])
				range_pos['end'] = int(line.split('\t')[3])
				if '.' in line.split('\t')[4]:
					if line.split('\t')[4] < "2":
						range_pos['cnv_state'] = (line.split('\t')[4]).split('.')[0]
						range_pos_all.append(range_pos)
					else:
						cn_one = str(1 + float(line.split('\t')[4]))
						range_pos['cnv_state'] = (cn_one).split('.')[0]
						range_pos_all.append(range_pos)
				else:
					range_pos['cnv_state'] = str(line.split('\t')[4])
					range_pos_all.append(range_pos)
			else:
				logging.warning("Patient %s: major_cn: "% name+line.split('\t')[4]+" !ARTEFACT!-----"+str(line.split('\t')[0:5]))

	return range_pos_all
