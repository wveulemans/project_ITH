#!/usr/bin/python

import os
				
def rights(patient_dir):
	"""
		Input: All files in the patient_directory
		----------
	    	Function: give acces to files (chmod 755)
		----------
		Output: All files with rights you need

	"""
	for root, dirs, files in os.walk(patient_dir):
			for d in dirs:
			    os.chmod(os.path.join(root, d), 0755)
			for f in files:
			    os.chmod(os.path.join(root, f), 0755)
