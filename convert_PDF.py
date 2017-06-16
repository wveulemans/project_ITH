#!/usr/bin/python

import os
import glob

def convert_pdf_images(name):
	"""
		Input: PDF images from SupraHex
		----------
	    	Function: convert PDF images to PNG for patient_report
		----------
		Output: PNG files acquired and PDF deleted

	"""
	source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*'% name)
	for files in source:
		if 'SupraHex' in files and '.pdf' in files:
			#print (files.split('/')[6]).split('.')[0]
			m = "pdftoppm -png %s /home/shared_data_core/COLON/subclonality/%s/%s"% (files.split('/')[6], name, files.split('/')[6].split('.')[0])
			print m
			os.system(m)
			os.system("rm %s"% files.split('/')[6])
	

