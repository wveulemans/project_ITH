#!/usr/bin/python

import os, logging

def makedir(name):
	"""
		Input: every patient_name
		----------
	    	Function: makes for every patient_name a directory ('/home/shared_data_core/COLON/subclonality/patientname')
		----------
		Output: patientdirectory is made

	"""

	PATH = '/home/shared_data_core/COLON/subclonality/'
	if not os.path.exists(os.path.join(PATH,name)):
		os.mkdir(os.path.join(PATH,name))
		print "Directory: %s is created!"% name
	else:
		print "Directory: %s already exist!"% name
		logging.info("Directory: %s already exist!"% name)
