#!/usr/bin/python

import TSV_writer

def compare(range_pos_all,variant_info, file_writer, name):
	"""
		Input: parameters from CNV file
		----------
	    	Function: see of the position of the mutation lays in the gene 
		----------
		Output: fills the dictionnary in, 2 def's above (variant_info[mutation_id])

	"""

	for gene_dict in range_pos_all:
		# mutation can fall out of gene range. So extend every gene range with 2500, begin and end
		if gene_dict['begin']-2500 <= variant_info['pos'] and variant_info['pos'] <= gene_dict['end']+2500 and variant_info['chr'] == gene_dict['chr']:	
			variant_info['major_cn'] = gene_dict['cnv_state']		
			#print "Mutation lies in %s"% gene_dict['gene_id'] 
			variant_info['mutation_id'] = name+':'+variant_info['genotype']+':'+gene_dict['gene_id']+':'+variant_info['chr']+':'+str(variant_info['pos'])+':'+variant_info['REF']+':'+str(variant_info['ALT'][0])
			TSV_writer.tsv_writer(variant_info, file_writer)
