#!/usr/bin/python

import os, logging
import subprocess

def exe_bash(name):
	"""
	    	Function: executes bash_file per patient_name (converts TSV to YAML and runs PyClone)
		----------
		Output:	- converted TSV '/home/shared_data_core/COLON/subclonality/patient_name/PYCLONE_input_patient_sample.tsv.yaml'
			- outfile '...'

	"""
	
	if os.path.exists('/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name)):
		os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
		# change rights from bash file
		os.chmod('pyclone_bash_%s.sh'% name, 0755)
		subprocess.call('./pyclone_bash_%s.sh'% name)
		os.stat('pyclone_bash_%s.sh'% name)
		logging.info("Patient: "+name+" is analyzed!")



def exe_supraHex(name, R_script):
	os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
	os.system('/opt/software/R/3.3.2/bin/Rscript '+R_script+' supraHex_input_%s.tsv'% name)
