#!/usr/bin/python

import glob

def prep_config_file(name, patient_name, patient_dir):
	"""
	    	Function: makes a configuration_file for every patient_name 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/config_file_patient_name' 

	"""

	w = open('/home/shared_data_core/COLON/subclonality/%s/config_file_%s.yaml'% (name,name), 'wb')	
	#w.write('# Specifies working directory for analysis. All paths in the rest of the file are relative to this.\n')
	w.write('working_dir: /home/shared_data_core/COLON/subclonality/\n\n')
	
	#w.write('\n# Where the trace (output) from the PyClone MCMC analysis will be written.\n')
	w.write('trace_dir: %s/\n\n'% name)

	#w.write('\n# Specifies which density will be used to model read counts. Most people will want pyclone_beta_binomial or pyclone_binomial\n')
	w.write('density: pyclone_beta_binomial\n\n')

	#w.write('\n# Number of iterations of the MCMC chain.\n')
	w.write('num_iters: 2000\n\n')

	#w.write('\n# Specifies parameters in Beta base measure for DP. Most people will want the values below.\n')
	w.write('base_measure_params:\n')
	w.write('  alpha: 1\n')
	w.write('  beta: 1\n\n')

	#w.write('\n# Specifies initial values and prior parameters for the prior on the concentration (alpha) parameter in the DP. If the prior node is not set the concentration will not be estimated and the specified value will be used.\n')
	w.write('concentration:\n')
	
	#w.write('# Initial value if prior is set, or fixed value otherwise for concentration parameter.\n\t')
	w.write('  value: 1.0 \n\n')
	
	#w.write('\n# Specifies the parameters in the Gamma prior over the concentration parameter\n')
	w.write('  prior:\n    shape: 1.0\n    rate: 0.001\n\n')

	#w.write('# Beta-Binomial precision (alpha + beta) prior')
	w.write('beta_binomial_precision_params:\n')
	#w.write('# Starting value')
	w.write('  value: 1000\n\n')

	#w.write('# Parameters for Gamma prior distribution')
	w.write('  prior:\n')
	w.write('    shape: 1.0\n')
	w.write('    rate: 0.0001\n\n')

	#w.write('# Precision of Gamma proposal function for MH step')
	w.write('  proposal:\n')
	w.write('    precision: 0.01\n\n')

	#w.write('\n# Specify the samples for the analysis.\n')
	w.write('samples:\n')

##########################################################################################################for loop

	source = glob.glob(patient_dir+'*')
	for files in source:
		if 'PYCLONE' in files:
			if not '.yaml' in files:
				#print files
				sample_name = (('_'.join(files.split('_')[4:8])).split('.')[0])
				print sample_name
				#w.write('\t# Unique sample ID.\n')
				w.write('  %s: \n'% sample_name)

				#w.write('\t\t# Path where tsv formatted mutations file for the sample is placed.\n')
				w.write('    mutations_file: PYCLONE_input_%s.tsv.yaml\n\n'% sample_name)
			
				w.write('    tumour_content:\n')
				#w.write('\t\t\t# The predicted tumour content for the sample. If you have no estimate set this to 1.0.\n')
				r = open('/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt')
				next(r)
				for line in r:
					if (line.split('\t')[1]).split('_', 2)[2] == sample_name:
						w.write('      value: '+line.split('\t')[7].split('\n')[0]+'\n\n')
						#w.write('\t\t# Expected sequencing error rate for sample.\n')
						w.write('    error_rate: 0.001\n\n')	

	w.close
	

