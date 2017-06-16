#!/usr/bin/python

import logging
import glob
import os

def prep_bash(name):
	"""
	    	Function: makes a bash_file for every patient_name 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone_bash_patient_name.sh'

	"""
	source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*'% name)
	for files in source:
		if 'PYCLONE' in files:
			#print files
			# check if input file for patient exist
			if not os.path.exists(files):
				logging.info("Input_files do not exist!!")
	
			# if input file exists, make/refresh bash with all necessary lines
			else:				
				w = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name), 'wb')
				w.write('#!/bin/bash\n')
				w.write('#WVeulemans\n\n')
				w.write('WORKING_DIR= "/home/shared_data_core/COLON/subclonality/%s/"\n\n'% name)
				w.write('echo -e "#!/bin/bash\n#PBS -X\t\t\t\t\t\tThe -x option allows the script to be executed in the interactive job and then the job completes\n#PBS -N PyClone$tumor_sample_name\t\tDeclares a name for the job\n#PBS -l nodes=1:ppn=2,mem=4g,walltime=01:00:00\tDefines the resources that are required by the job and establishes a limit to the amount of resource that can be consumed\n#PBS -m ea\t\t\t\t\tmail_options\n#PBS -M ward.veulemans@student.howest.be\tDeclares the list of users to whom mail is sent\n#PBS -q scattergather\t\t\t\tDefines the destination of the job\n#PBS -A onco\t\t\t\t\tDefines the account string associated with the job\n"\n\n')


				w.write('echo "Building yaml files"\n')
				source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*'% name)
				for files in source:
					inputs = files.split('/')[6]
					if 'PYCLONE_input' in inputs:
						if not '.tsv.yaml' in inputs:			
							w.write('echo `PyClone build_mutations_file --in_file '+inputs+' --out_file '+inputs+'.yaml`\n')

				w.write('\necho "Running pipeline analysis for %s"\n'% name)
				w.write('echo `PyClone run_analysis --config_file config_file_%s.yaml`\n'% name)

				w.write('\necho "Building density_plot_%s"\n'% name)
				w.write('echo `PyClone plot_loci --config_file config_file_%s.yaml --plot_file PyClone_density_plot_%s --plot_type density`\n'% (name,name))

				w.write('\necho "Building similarity_matrix_%s"\n'% name)
				w.write('echo `PyClone plot_loci --config_file config_file_%s.yaml --plot_file PyClone_sim_matrix_%s --plot_type similarity_matrix`\n'% (name,name))

				w.write('\necho "Building parallel_coordinates_%s"\n'% name)
				w.write('echo `PyClone plot_clusters --config_file config_file_%s.yaml --plot_file PyClone_parallel_coordinates_%s --plot_type parallel_coordinates`\n'% (name,name))

				w.write('\necho "Building scatter_%s"\n'% name)
				w.write('echo `PyClone plot_clusters --config_file config_file_%s.yaml --plot_file PyClone_cell_prev_scatter_%s --plot_type scatter`\n'% (name,name))

				w.write('\necho "Building vaf_parallel_coordinates_%s"\n'% name)
				w.write('echo `PyClone plot_loci --config_file config_file_%s.yaml --plot_file PyClone_vaf_parallel_coordinates_%s --plot_type vaf_parallel_coordinates`\n'% (name,name))
				
				w.write('\necho "Building vaf_scatter_%s"\n'% name)
				w.write('echo `PyClone plot_loci --config_file config_file_%s.yaml --plot_file PyClone_vaf_scatter_%s --plot_type vaf_scatter`\n'% (name,name))

				w.write('\necho "Building table_%s"\n'% name)
				w.write('echo `PyClone build_table --config_file config_file_%s.yaml --out_file pyclone_table_%s.tsv --table_type loci`\n'% (name,name))

				w.close()
	
	global bash_file
	bash_file = '/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name)

	return 	bash_file

