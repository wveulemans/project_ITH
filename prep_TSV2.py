#! /usr/bin/python

import glob, os, vcf
from collections import OrderedDict as OD

def prep_tsv2(name, range_pos_all):
	"""
		Input: 
		----------
	    	Function: 
		----------
		Output: 

	"""

	#print glob.glob('/home/shared_data_core/COLON/subclonality/%s/pyclone*'% name)
	step1_files = glob.glob('/home/shared_data_core/COLON/subclonality/%s/pyclone_*.filtered.vcf.tsv'% (name))
	#print step1_files

	samp = []
	for step1_file in step1_files:
		samp.append(('_'.join((step1_file.split('/')[6]).split('_')[3:7])).split('.')[0])

	distinct_samples = []
	for sa in samp:
		if not sa in distinct_samples:
			distinct_samples.append(sa)

	#print distinct_samples

	
# make dict with all mutations
	global patient_variant_dict
	patient_variant_dict = dict()
	for step1_file in step1_files:
		#print step1_file
		
		filename = ('_'.join((step1_file.split('/')[6]).split('_')[3:7])).split('.')[0]
		#print filename


		with open(step1_file, 'rb') as fopen:
			for line in fopen:
				# skip first line
				if not 'mutation_id' in line:

					if line.split('\t')[0] in patient_variant_dict.keys():
						new_element = {filename:{'ref_cnt':line.split('\t')[1], 'var_cnt':line.split('\t')[2], 'normal_cn':line.split('\t')[3], 'minor_cn':line.split('\t')[4], 'major_cn':line.split('\t')[5], 'var_case':line.split('\t')[6], 'var_freq':line.split('\t')[7], 'geno':line.split('\t')[8]}}
						#print '\n',new_element
						tmp_list = patient_variant_dict[line.split('\t')[0]]
						tmp_list.append(new_element)
						#print tmp_list
						patient_variant_dict[line.split('\t')[0]] = tmp_list

					if not line.split('\t')[0] in patient_variant_dict.keys():
						tmp_list = [{filename:{'ref_cnt':line.split('\t')[1], 'var_cnt':line.split('\t')[2], 'normal_cn':line.split('\t')[3], 'minor_cn':line.split('\t')[4], 'major_cn':line.split('\t')[5], 'var_case':line.split('\t')[6], 'var_freq':line.split('\t')[7], 'geno':line.split('\t')[8]}}]
						patient_variant_dict[line.split('\t')[0]] = tmp_list


	#print patient_variant_dict


# compare if  mutation is present, if not all 0
	for var_id in patient_variant_dict:
		sample_list_ids = list()
		for sample in patient_variant_dict[var_id]:
				sample_list_ids.append(sample.keys()[0])
		#print sample_list_ids

		for step1_file in step1_files:
			#print step1_file
			filename = ('_'.join((step1_file.split('/')[6]).split('_')[3:7])).split('.')[0]
			var_case = ('_'.join((step1_file.split('/')[6]).split('_')[3]))

			if not filename in sample_list_ids:
				#print var_id
				gene = var_id.split(':')[2]
				chrom = var_id.split(':')[3]
				pos = var_id.split(':')[4]
				ref = var_id.split(':')[5]
				alt = var_id.split(':')[6]
				
				if len(ref) > 1 or len(alt) > 1:
					vcf_file_sample = '/home/shared_data_core/COLON/subclonality/'+name+'/ith_'+('_'.join((step1_file.split('/')[6]).split('_')[2:7])).split('.')[0]+'.varscan2.pair.indel.filtered.vcf'
					snp_indel = 'indel'
				else:
					vcf_file_sample = '/home/shared_data_core/COLON/subclonality/'+name+'/ith_'+('_'.join((step1_file.split('/')[6]).split('_')[2:7])).split('.')[0]+'.varscan2.pair.snp.filtered.vcf'
					snp_indel = 'snp'

				check_var = 0
				vcf_reader = vcf.Reader(open(vcf_file_sample, 'r'))
				for record in vcf_reader:
					var_filter_id = record.FILTER[0]
					variant_info_chrom = record.CHROM
					variant_info_pos = int(record.POS)
					variant_info_ref = record.REF
					variant_info_alt = record.ALT[0]
					variant_info_rd = record.samples[1]['RD']
					variant_info_ad = record.samples[1]['AD']

					if int(pos) == variant_info_pos and chrom == variant_info_chrom and ref == variant_info_ref and alt == variant_info_alt:

						# ref_count
						ref_count = record.samples[1]['RD']
						# alt_count
						alt_count = record.samples[1]['AD']
						# normal_cn
						if chrom == 'chrX' or chrom == 'chrY':		# Checks if sexchromosome then check the gender
							r = open('/home/shared_data_core/COLON/subclonality/info_file.txt', 'rb')
							next(r)	#skip header

							for row in r:
								#print row.split()[8]
								if row.split()[8] == 'm':
									normal_cn = '1'
									#print '1, because male and sex chr'						
								else:
									normal_cn = '1'
							r.close()
	
						else:
							normal_cn = '2'
						# variant_frequency
						os.chdir('/home/shared_data_core/COLON/subclonality/'+name+'/')
						run = ('_'.join((step1_file.split('/')[6]).split('_')[2:7])).split('.')[0]
						#print run
						r = open('X.home.shared_data_core.COLON.ITH_nele_BAMs.ith_'+run+'.real.recal.summary.txt', 'rb')
						next(r)

						for line in r:
							if gene in line:
								if float(line.split('\t')[4]) <= 8:
									range_dict = OD([
										('gene_id', str()),
										('chr', str()),
										('begin', int()),
										('end', int()),
										('cnv_state', str())
										])						
									range_dict['gene_id'] = str(line.split('\t')[0])
									range_dict['chr'] = str(line.split('\t')[1])
									range_dict['begin'] = int(line.split('\t')[2])
									range_dict['end'] = int(line.split('\t')[3])
									if '.' in line.split('\t')[4]:
										if line.split('\t')[4] < "2":
											range_dict['cnv_state'] = (line.split('\t')[4]).split('.')[0]
										else:
											cn_one = str(1 + float(line.split('\t')[4]))
											range_dict['cnv_state'] = (cn_one).split('.')[0]
									else:
										range_dict['cnv_state'] = str(line.split('\t')[4])
						#print range_dict

						if range_dict['begin']-2500 <= pos and int(pos) <= range_dict['end']+2500 and chrom == range_dict['chr']:
							major_cn = range_dict['cnv_state']
							#print 'In gene'
						else:
							minor_cn = 'not in gene'
							print '##################	not in gene'
						# variant_frequency
						var_freq = format((1 - (float(record.samples[1]['RD'])/(record.samples[1]['RD'] + record.samples[1]['AD']))), '.12f')
						# genotype
						binary_GT = record.samples[1]['GT'].replace('|', '/').split('/')
						if binary_GT[0] != binary_GT[1]:
							genotype = str('AB')
						if binary_GT[0] == binary_GT[1]:
							genotype = str('BB')
				
						new_element = {filename:{'ref_cnt':ref_count, 'var_cnt':alt_count, 'normal_cn':normal_cn, 'minor_cn':0, 'major_cn':major_cn, 'var_case': name, 'var_freq':var_freq, 'geno':genotype}}
						#print new_element
						tmp_list = patient_variant_dict[var_id]
						tmp_list.append(new_element)
						patient_variant_dict[var_id] = tmp_list
						check_var = 1

				if not check_var:
					############ check position	
					os.chdir('/home/shared_data_core/COLON/subclonality/'+name+'/')
					#print os.getcwd()
					run = ('_'.join((step1_file.split('/')[6]).split('_')[2:7])).split('.')[0]
					#print run
					r = open('X.home.shared_data_core.COLON.ITH_nele_BAMs.ith_'+run+'.real.recal.summary.txt', 'rb')
					next(r)

					for line in r:
						if gene in line:
							if float(line.split('\t')[4]) <= 8:
								range_dict = OD([
									('gene_id', str()),
									('chr', str()),
									('begin', int()),
									('end', int()),
									('cnv_state', str())
									])						
								range_dict['gene_id'] = str(line.split('\t')[0])
								range_dict['chr'] = str(line.split('\t')[1])
								range_dict['begin'] = int(line.split('\t')[2])
								range_dict['end'] = int(line.split('\t')[3])
								if '.' in line.split('\t')[4]:
										if line.split('\t')[4] < "2":
											range_dict['cnv_state'] = (line.split('\t')[4]).split('.')[0]
										else:
											cn_one = str(1 + float(line.split('\t')[4]))
											range_dict['cnv_state'] = (cn_one).split('.')[0]
								else:
									range_dict['cnv_state'] = str(line.split('\t')[4])
					#print range_dict
	
					if range_dict['begin']-2500 <= pos and int(pos) <= range_dict['end']+2500 and chrom == range_dict['chr']:
						major_cn = range_dict['cnv_state']
						#print 'In gene'
					else:
						minor_cn = 'not in gene'
						print '##################	not in gene'

	############ check normal cn for chrX and chrY for men 1, women 2
					if chrom == 'chrX' or chrom == 'chrY':		# Checks if sexchromosome then check the gender
						r = open('/home/shared_data_core/COLON/subclonality/info_file.txt', 'rb')
						next(r)	#skip header

						for row in r:
							#print row.split()[8]
							if row.split()[8] == 'm':
								normal_cn = '1'
								#print '1, because male and sex chr'						
							else:
								normal_cn = '1'
						r.close()
		
					else:
						normal_cn = '2'

					new_element = {filename:{'ref_cnt':0, 'var_cnt':0, 'normal_cn':normal_cn, 'minor_cn':0, 'major_cn':major_cn, 'var_case': name, 'var_freq':0, 'geno':'AA'}}
					#print new_element
					tmp_list = patient_variant_dict[var_id]
					tmp_list.append(new_element)
					patient_variant_dict[var_id] = tmp_list

	#print patient_variant_dict
	return patient_variant_dict, distinct_samples
				



