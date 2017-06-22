#! /usr/bin/python

import os
import shutil
import glob
import logging

def copyfile_CNV(name):
	"""
		Input: every patient_name
		----------
	    	Function: copies all CNV-files per patient_name 
		----------
		Output: CNV-files are in correct patient_directory

	"""

	source = glob.glob('/home/shared_data_core/COLON/subclonality/CNV/*_%s_*.txt'% name)
	destination = '/home/shared_data_core/COLON/subclonality/'+name+'/'


	dest_files =  glob.glob('/home/shared_data_core/COLON/subclonality/'+name+'/*')
	all_samples = []
	
	for files in dest_files:
		if not 'pyclone' in files:
			if not 'X.home.' in files:
				if 'filtered.vcf' in files:
					#print files
					#print (files.split('/')[6].split('.')[0]).split('_',1)[1]
					all_samples.append(((files.split('/')[6].split('.')[0]).split('_',1)[1]).lower())
		
	dist_samples = list(set(all_samples))
	#print dist_samples
	
	global cnv_file	
	cnv_file = 0

	# check if sample has CNV_file
	for sample in dist_samples:
		matching = [files1 for files1 in source if sample in files1]
		if any(sample in files1 for files1 in source):
			shutil.copy2(os.path.abspath(matching[0]),os.path.abspath(destination))

		 	#print '.'.join((matching[0].split('/')[6]).split('.')[:5])
			prefix =  '.'.join((matching[0].split('/')[6]).split('.')[:5])
			amt = ((matching[0].split('/')[6]).split('.')[5]).split('_')
			sample = '_'.join(amt[:6])			
			affix = matching[0].split('/')[6].split('.', 6)[6]
			#print prefix+'_'+sample+'.'+affix
			
			#if len(amt) == 6:
			#	os.rename('/home/shared_data_core/COLON/subclonality/'+ALL+'/'+matching[0].split('/')[6], '/home/shared_data_core/COLON/subclonality/'+ALL+'/'+matching[0].split('/')[6])
			if len(amt) == 7:
				os.rename('/home/shared_data_core/COLON/subclonality/'+name+'/'+matching[0].split('/')[6], '/home/shared_data_core/COLON/subclonality/'+name+'/'+prefix+'.'+sample+'.'+affix)
							
			print "Transferring CNV file"
			cnv_file = 1
		else:
			#print "No CNV file present for sample: "+sample+""
			#logging.error("Patient %s: CNV file missing for sample: "% name +sample+"!!!")
			cnv_file = 0




def copyfile_CNV_all(name, ALL):
	"""
		Input: every patient_name
		----------
	    	Function: copies all CNV-files per patient_name 
		----------
		Output: CNV-files are in correct patient_directory

	"""

	source = glob.glob('/home/shared_data_core/COLON/subclonality/CNV/*_%s_*.txt'% name)
	destination = '/home/shared_data_core/COLON/subclonality/'+ALL+'/'


	dest_files =  glob.glob('/home/shared_data_core/COLON/subclonality/'+ALL+'/*')
	all_samples = []
	
	for files in dest_files:
		if not 'pyclone' in files:
			if not 'X.home.' in files:
				if 'filtered.vcf' in files:
					#print files
					#print (files.split('/')[6].split('.')[0]).split('_',1)[1]
					all_samples.append(((files.split('/')[6].split('.')[0]).split('_',1)[1]).lower())
		
	dist_samples = list(set(all_samples))
	#print dist_samples
	
	global cnv_file	
	cnv_file = 0

	# check if sample has CNV_file
	for sample in dist_samples:
		matching = [files1 for files1 in source if sample in files1]
		if any(sample in files1 for files1 in source):
			shutil.copy2(os.path.abspath(matching[0]),os.path.abspath(destination))

		 	#print '.'.join((matching[0].split('/')[6]).split('.')[:5])
			prefix =  '.'.join((matching[0].split('/')[6]).split('.')[:5])
			amt = ((matching[0].split('/')[6]).split('.')[5]).split('_')
			sample = '_'.join(amt[:6])			
			affix = matching[0].split('/')[6].split('.', 6)[6]
			#print prefix+'_'+sample+'.'+affix
			
			#if len(amt) == 6:
			#	os.rename('/home/shared_data_core/COLON/subclonality/'+ALL+'/'+matching[0].split('/')[6], '/home/shared_data_core/COLON/subclonality/'+ALL+'/'+matching[0].split('/')[6])
			if len(amt) == 7:
				os.rename('/home/shared_data_core/COLON/subclonality/'+ALL+'/'+matching[0].split('/')[6], '/home/shared_data_core/COLON/subclonality/'+ALL+'/'+prefix+'.'+sample+'.'+affix)
							
			print "Transferring CNV file"
			cnv_file = 1
		else:
			#print "No CNV file present for sample: "+sample+""
			#logging.error("Patient %s: CNV file missing for sample: "% name +sample+"!!!")
			cnv_file = 0	
