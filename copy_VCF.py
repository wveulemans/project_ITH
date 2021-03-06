#!/usr/bin/python

import os
import shutil
import glob

def copyfile_VCF(name):
	"""
		Input: every patient_name
		----------
	    	Function: copies all VCF's per patient_name 
		----------
		Output: VCF's are in correct patient_directory

	"""

	source = glob.glob('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter_pyAmpli_validate/*_%s_*/*filter*.vcf'% name)
	destination = '/home/shared_data_core/COLON/subclonality/'+name+'/'
	
	for files in source:
		if files.endswith('.vcf'):
			if not os.path.exists(os.path.join(destination,files.split('/')[7])):
				shutil.copy2(os.path.abspath(files),destination)
				#print ((files.split('/')[7]).split('.')[0]).split('_')
				amt = ((files.split('/')[7]).split('.')[0]).split('_')
				
				if len(amt) == 6:
					os.rename('/home/shared_data_core/COLON/subclonality/'+name+'/'+files.split('/')[7]+'', '/home/shared_data_core/COLON/subclonality/'+name+'/'+(files.split('/')[7]).lower()+'')
				elif len(amt) == 8:
					affix = ((files.split('/')[7]).split('.', 1)[1]).lower()
					#print ('_'.join(amt[:4])+'_'+amt[5]+'_'+amt[7]).lower()+'.'+affix
					os.rename('/home/shared_data_core/COLON/subclonality/'+name+'/'+files.split('/')[7]+'', '/home/shared_data_core/COLON/subclonality/'+name+'/'+('_'.join(amt[:4])+'_'+amt[5]+'_'+amt[7]).lower()+'.'+affix)
					
#			else:
#				logging.info("File: "+files.split('/')[7]+" already exist!")

	print "All VCF's copied for %s!"% name




def copyfile_VCF_all(name, ALL):
	"""
		Input: every patient_name
		----------
	    	Function: copies all VCF's per patient_name 
		----------
		Output: VCF's are in the ALL patient_directory

	"""

	source = glob.glob('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter_pyAmpli_validate/*_%s_*/*filter*.vcf'% name)
	destination = '/home/shared_data_core/COLON/subclonality/'+ALL+'/'
	
	for files in source:
		if files.endswith('.vcf'):
			if not os.path.exists(os.path.join(destination,files.split('/')[7])):
				shutil.copy2(os.path.abspath(files),destination)
				#print ((files.split('/')[7]).split('.')[0]).split('_')
				amt = ((files.split('/')[7]).split('.')[0]).split('_')
				
				if len(amt) == 6:
					os.rename('/home/shared_data_core/COLON/subclonality/'+ALL+'/'+files.split('/')[7]+'', '/home/shared_data_core/COLON/subclonality/'+ALL+'/'+(files.split('/')[7]).lower()+'')
				elif len(amt) == 8:
					affix = ((files.split('/')[7]).split('.', 1)[1]).lower()
					#print ('_'.join(amt[:4])+'_'+amt[5]+'_'+amt[7]).lower()+'.'+affix
					os.rename('/home/shared_data_core/COLON/subclonality/'+ALL+'/'+files.split('/')[7]+'', '/home/shared_data_core/COLON/subclonality/'+ALL+'/'+('_'.join(amt[:4])+'_'+amt[5]+'_'+amt[7]).lower()+'.'+affix)
					
#			else:
#				logging.info("File: "+files.split('/')[7]+" already exist!")

	print "All VCF's copied for %s!"% name
