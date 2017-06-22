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
		#os.system('qsub pyclone_bash_%s.sh' % name)
		subprocess.call('./pyclone_bash_%s.sh'% name)
		os.stat('pyclone_bash_%s.sh'% name)
		logging.info("Patient: "+name+" is analyzed!")



def exe_supraHex(name, R_script):
	os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
	os.system('/opt/software/R/3.3.2/bin/Rscript '+R_script+' supraHex_input_%s.tsv'% name)

def exe_patient_report(report_script):
	os.chdir('/home/shared_data_core/COLON/subclonality/')
	subprocess.call('./report.py')
	os.stat('report.py')

################################################################################################################################################

def exe_bash_all(ALL):
	"""
	    	Function: executes bash_file per patient_name (converts TSV to YAML and runs PyClone)
		----------
		Output:	- converted TSV '/home/shared_data_core/COLON/subclonality/patient_name/PYCLONE_input_patient_sample.tsv.yaml'
			- outfile '...'

	"""
	
	if os.path.exists('/home/shared_data_core/COLON/subclonality/'+ALL+'/pyclone_bash_'+ALL+'.sh'):
		os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')
		# change rights from bash file
		os.chmod('pyclone_bash_'+ALL+'.sh', 0755)
		subprocess.call('./pyclone_bash_'+ALL+'.sh')
		os.stat('pyclone_bash_'+ALL+'.sh')
		logging.info("Patient: "+ALL+" is analyzed!")



def exe_supraHex_all(R_script, ALL):
	os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')
	os.system('/opt/software/R/3.3.2/bin/Rscript '+R_script+' supraHex_input_'+ALL+'.tsv')
