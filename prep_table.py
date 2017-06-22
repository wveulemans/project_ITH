#!/usr/bin/python

import glob

def prep_pyclone_table(patient_dir, name):

	source = glob.glob(patient_dir+'/*')
	#print source
	for files in source:
		if 'pyclone_table_' in files:
			print files
			r = open(files, 'rb')
			w = open('/home/shared_data_core/COLON/subclonality/'+name+'/PyClone_table_'+name+'.tsv', 'wb')
			next(r)
			for line in r:
				print line.split('\t')[5].rstrip()
				if line.split('\t')[5].rstrip() == '':
					w.write(line.rstrip()+'\t'+'0.000000000000\n')
					
				else:
					w.write(line)
					
			w.close()

#################################################################################################################################

def prep_pyclone_table_all(patient_dir_all, ALL):

	source = glob.glob(patient_dir_all+'/*')
	#print source
	for files in source:
		if 'pyclone_table_' in files:
			#print files
			r = open(files, 'rb')
			w = open('/home/shared_data_core/COLON/subclonality/'+ALL+'/PyClone_table_'+ALL+'.tsv', 'wb')
			next(r)
			for line in r:
				print line.split('\t')[5].rstrip()
				if line.split('\t')[5].rstrip() == '':
					w.write(line.rstrip()+'\t'+'0.000000000000\n')
					
				else:
					w.write(line)
					
			w.close()
			
