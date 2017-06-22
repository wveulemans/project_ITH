#! /usr/bin/python
import time
import os
import csv
import glob

def to_lower(textfile):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt' & '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
		----------
	    	Function: set all characters to lowercase
		----------
		Output: same file as infile

	"""

	f = open(textfile, 'rw+')
	lines = [line.lower() for line in f]

	with open(textfile, 'w') as out:
     		out.writelines(lines)
	f.close()



def patient_names(paired_samples_all):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
		----------
	    	Function: makes a list with every patient_name
		----------
		Output: list with all patient_names

	"""

	r = open(paired_samples_all, 'rb')
	next(r) # skip header

	result=[]
	for line in r:
		parts = line.split()		
		if len(parts) > 0:
			result.append(parts[4])

	#print result
	
	names = []
	for name in result:
		if name.split('_')[2] not in names:
			names.append(name.split('_')[2])
			
	
	#print names
	return names

	

def index(names, ALL):
	os.chdir('/home/shared_data_core/COLON/subclonality/')
	w = open('index.php', 'wb')
	os.chmod('index.php', 0755)

	w.write('<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
<meta charset="utf-8">\n\
<title>Project Intra Tumour Heterogeneity</title>\n\
<style type="text/css" media="screen">\n\
body {\n\
	background-image: url("background.jpg");\n\
	background-repeat:no-repeat;\n\
	background-size:cover;\n\
	margin: 0;\n\
}\n\
ul {\n\
   	list-style-type: none;\n\
    	margin: 0;\n\
    	padding: 0;\n\
    	width: 8%;\n\
    	background-color: #f1f1f1;\n\
    	position: fixed;\n\
    	height: 100%;\n\
    	overflow: auto;\n\
}\n\
li a {\n\
    	display: block;\n\
    	color: #000;\n\
    	padding: 8px 16px;\n\
    	text-decoration: none;\n\
}\n\
li a.active {\n\
    	background-color: #4CAF50;\n\
    	color: white;\n\
}\n\
li a:hover:not(.active) {\n\
    	background-color: #555;\n\
    	color: white;\n\
}\n\
</style>\n\
</head>\n\
<body>\n\
<ul>\n\
	<li><a class="active" href="http://localhost:8000/index.php">Home</a></li>\n')
	w.write('\t<li><a href="http://localhost:8000/patient_report_'+ALL+'.php">patient_'+ALL+'</a></li>\n')
	w.write('</ul>\n\
<div style="margin-left:8%;padding:1px 16px;height:1000px;">\n\
 <h2>Project: intra tumor heterogeneity</h2>\n\
 <p>This is a website created to share information about the tumour heterogeneity from different patients</p>\n\
</div>\n\
</div>\n\
</body>\n\
</html>\n')
	w.close()


def patient_report(ALL, clin_info, log_file, names):
	os.chdir('/home/shared_data_core/COLON/subclonality/')
	w = open('patient_report_'+ALL+'.php', 'wb')
	os.chmod('patient_report_'+ALL+'.php', 0755)
	
	w.write('<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
<meta charset="utf-8">\n\
<title>Patient report '+ALL+'</title>\n')
	w.write('\t<style type="text/css" media="screen">\n\
.ul_up {\n\
	list-style-type: none;\n\
	margin: 0;\n\
	padding: 0;\n\
	overflow: hidden;\n\
	background-color: #333;\n\
}\n\
.li_up {\n\
	float: left;\n\
}\n\
li a, .dropbtn {\n\
	display: inline-block;\n\
	color: white;\n\
	text-align: center;\n\
	padding: 14px 16px;\n\
	text-decoration: none;\n\
	}\n\
li a:hover, .dropdown:hover .dropbtn {\n\
	background-color: red;\n\
}\n\
li.dropdown {\n\
	display: inline-block;\n\
}\n\
.dropdown-content {\n\
	display: none;\n\
	position: absolute;\n\
	background-color: #f9f9f9;\n\
	min-width: 160px;\n\
	box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n\
	z-index: 1;\n\
}\n\
.dropdown-content a {\n\
	color: black;\n\
	padding: 12px 16px;\n\
	text-decoration: none;\n\
	display: block;\n\
	text-align: left;\n\
}\n\
.dropdown-content a:hover {background-color: #f1f1f1}\n\
.dropdown:hover .dropdown-content {\n\
	display: block;\n\
}\n\
.dropdown_image {\n\
    margin-right: 170px;\n\
    float: right;\n\
    position: relative;\n\
    display: inline-block;\n\
}\n\
.dropdown_content_image {\n\
    display: none;\n\
    position: absolute;\n\
    background-color: #f9f9f9;\n\
    min-width: 160px;\n\
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n\
    z-index: 1;\n\
}\n\
.dropdown_image:hover .dropdown_content_image {\n\
    display: block;\n\
}\n\
.desc {\n\
    padding: 15px;\n\
    text-align: center;\n\
}\n\
h1 {\n\
	margin: 10px 5px;\n\
}\n\
h2 {\n\
	float:left\n\
	margin: 10px 5px;\n\
}\n\
h3 {\n\
	margin: 10px 5px;\n\
}\n\
div {\n\
	margin: 0px  5px;\n\
}\n\
.navlinks {\n\
	list-style-position: outside;\n\
}\n\
img {\n\
	float: left;\n\
	margin: 5px;\n\
}\n\
.img_txt {\n\
	float: left;\n\
	margin: 5px;\n\
	height: 500px;\n\
	width: 500px;\n\
}\n\
.plot {\n\
	float: left;\n\
}\n\
.text {\n\
	float: left;\n\
	margin-top:250px;\n\
	padding:12px;\n\
	margin-bottom:50px;\n\
	width:35%;\n\
	font-size:13px;\n\
}\n\
table, th, td {\n\
    border: 1px solid black;\n\
    border-collapse: collapse;\n\
}\n\
th {\n\
    background-color: #7c7c7c;\n\
}\n\
td {\n\
    text-align: center;\n\
}\n\
tr:nth-child(even){background-color: #cccccc}\n\
#myBtn {\n\
  display: none;\n\
  position: fixed;\n\
  bottom: 20px;\n\
  right: 30px;\n\
  z-index: 99;\n\
  border: none;\n\
  outline: none;\n\
  background-color: red;\n\
  color: white;\n\
  cursor: pointer;\n\
  padding: 15px;\n\
  border-radius: 10px;\n\
}\n\
\n\
#myBtn:hover {\n\
  background-color: #555;\n\
  opacity: 0.5;\n\
}\n\
</style>\n\
</head>\n\
<body>\n\
<button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>\n\
	<div class="ul_up">\n\
  		<li class="li_up"><a href="http://localhost:8000/index.php">Home</a></li>\n\
		<li class="dropdown">\n\
    			<a href="javascript:void(0)" class="dropbtn">Patients</a>\n\
    			<div class="dropdown-content">\n')
	
	w.write('\t\t\t<a href="http://localhost:8000/patient_report_'+ALL+'.php">patient_'+ALL+'</a>\n')
      			
    	w.write('\t\t\t</div>\n\
  		</li>\n\
	</div>\n')

	w.write('<div class="dropdown_image">\n\
  <img src="person.jpg" alt="unknown_person" width="75" height="100">\n\
  <div class="dropdown_content_image">\n\
    <img src="person.jpg" alt="unknown_person" width="225" height="300">\n\
    <div class="desc">Photo: patient '+ALL+'</div>\n\
  </div>\n\
</div>\n')
	w.write('\t<h1>Patient '+ALL+'</h1>\n')
	w.write('\t<div class=geheel>\n\
		<h2>PyClone visual output</h2>\n')

	os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')

	w.write('\t\t<div class="plot">\n\
		<h3>PyClone density plot</h3>\n\
		<img src="/'+ALL+'/PyClone_density_plot_'+ALL+'.png" alt="PyClone density plot '+ALL+'.png">\n\
		<div class="img_txt">\n\
		<pre>Plot of the posterior density of the cellular frequencies use\n\
The loci density is the posterior distribution of cellular prevalence for each mutation (loci).\n\
\n\
The large range in the scatter indicates there is uncertainty in the cellular prevalence of the mutation.\n\
Clusters with one mutation will typically have more uncertainty than those with multiple mutations.\n\
This happens because without clustering PyClone has no idea which possible genotype the mutation has.\n\
However, once several mutations cluster the model can share information\n\
and infer what the common cellular prevalence is and by extension associated genotypes for mutations in the cluster are.</pre>\n\
		</div>\n\
		</div>\n\n')

	source = glob.glob('*')
	
	for files in source:
		if 'PyClone' in files and '.png' in files and not 'density_plot' in files:
			#print files, name
			w.write('\t\t<div class="plot">\n\
		<h3>'+' '.join((files.split('-1')[0]).split('_')[0:3])+'</h3>\n\
		<img src="/'+ALL+'/'+files+'" alt="'+files.split('.')[0]+'" height="700" width="700">\n')

			if 'PyClone_sim_matrix' in files:
				w.write('<div class="img_txt">\n\
			<pre>Similarity matrix.\n\
\n\
The posterior similarity matrix which shows how often mutations\n\
where sampled to be in the same cluster</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'PyClone_parallel_coordinates' in files:
				w.write('<div class="img_txt">\n\
			<pre>Parallel coordinates.\n\
\n\
Plot the mean cellular frequencies of mutations colour coded by cluster ID</pre>\n\
</div>\n\
			</div>\n\n')

			elif 'PyClone_cell_prev_scatter' in files:
				w.write('<div class="img_txt">\n\
			<pre>Cellular prevalence scatter.\n\
\n\
Cellular prevalence scatter</pre>\n\
</div>\n\
			</div>\n\n')

			elif 'PyClone_vaf_scatter' in files:
				w.write('<div class="img_txt">\n\
			<pre>Variant allele frequency scatter.\n\
\n\
Variant allele frequency scatter</pre>\n\
</div>\n\
			</div>\n\n')
		
			elif 'PyClone_vaf_parallel_coordinates' in files:
				w.write('<div class="img_txt">\n\
			<pre>Variant allele frequency parallel coordinates .\n\
\n\
Variant allele frequency parallel coordinates</pre>\n\
			</div>\n\
			</div>\n\n')

#####################################SupraHex visuals#####################################
	w.write('\t\t<h2>SupraHex visual output</h2>\n\n')

	for files in source:
		if 'SupraHex' in files and '.png' in files:
			#print files, name
			#print ' '.join((files.split('.')[0]).split('_')[0:3])
			w.write('\t\t<div class="plot">\n\
		<h3>'+' '.join((files.split('-1')[0]).split('_')[0:3])+'</h3>\n\
		<img src="/'+ALL+'/'+files+'" alt="'+files.split('.')[0]+'" height="700" width="700">\n')

			if 'SupraHex_visHexMulComp' in files:
				w.write('<div class="img_txt">\n\
			<pre>This is the visualisation of multiple component planes of a supra-hexagonal grid.\n\
</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visHexMapping_index' in files:
				w.write('<div class="img_txt">\n\
			<pre>Supra-hexagonal map.\n\
\n\
SupraHex produces a map in which genes with similar data patterns\n\
self-organise to the same or nearby nodes in the map\n\
and the distribution of genes across the 2D map is representive\n\
of the high-dimensional input space\n\
\n\
For easy reference, these hexagons are indexed.\n\
The indexing begins with the centroid/the middle of the supraHexagon.\n\
Then the hexagons of the same step, an anti-clock order starting from the rightmost.\n\
This map can also be easily described by the grid radius\n\
(= maximum steps away from the centroid, r=5 in this case,\n\
or by the xy-dimensions of the map grid \n\
(= maxium number of hexagons horizontally/vertically; xdim = ydim = 9).</pre>\n\
			</div>\n\
			</div>\n\n')
			elif 'SupraHex_visHexMapping_hits' in files:
				w.write('<div class="img_txt">\n\
			<pre>Map hit distribution.\n\
\n\
The function visHexMapping is used to visualise the single-value properties\n\
that are associated with the map.\n\
The number represents how many input data vectors are hitting each hexagon.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visHexMapping_dist' in files:
				w.write('<div class="img_txt">\n\
			<pre>Map Distance visualisation\n\
\n\
The function visHexMapping is used to visualise the single-value properties\n\
that are associated with the map. The map distance visualisation,\n\
which tells how far each hexagon is away rom its neighbors.\n\
So for each hexagon,\n\
its median distances in high-dimensional input space to its neighbors is calculated.\n\
The size of each hexagon is proportional to this distance.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visHexPattern_lines' in files:
				w.write('<div class="img_txt">\n\
			<pre>Line plot of codebook patterns\n\
\n\
The function visHexPattern is used to visualise the vector-based patterns\n\
that are associated with the map using line plots.\n\
If multiple colors are given, the points are also plotted.\n\
When the pattern involves both positive and negative values,\n\
zero horizontal line is also shown.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visHexPattern_bars' in files:
				w.write('<div class="img_txt">\n\
			<pre>Bar plot of codebook patterns\n\
\n\
The function visHexPattern is used to visualise the vector-based patterns\n\
that are associated with the map using bar plots.\n\
When the pattern involves both positive and negative values,\n\
the zero horizontal line is in the middle of the hexagon;\n\
otherwise at the top of the hexagon for all negative values,\n\
and at the bottom for all positive values.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visDmatCluster' in files:
				w.write('<div class="img_txt">\n\
			<pre>Clusters of the trained map.\n\
\n\
Partition the trained map into clusters using region-growing algorithm\n\
to ensure each cluster is conitinuous.\n\
There is also an output.txt (= PyClone_cellular_prevalence.supraHex_base.txt).\n\
This file has 1st column for your input data ID\n\
(an integer; otherwise the row names of input data matrix),\n\
and 2nd column for the corresponding index of best-matching hexagons\n\
(i.e. mutation clusters), and 3rd column for the cluster bases\n\
(i.e. mutation meta-clusters). Each cluster is filled with the same continuous color.\n\
The cluster index is marked in the seed node.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visDmatHeatmap' in files:
				w.write('<div class="img_txt">\n\
			<pre>Function to visualise gene clusters/bases partitioned from a supra-hexagonal grid using heatmap\n\
\n\
heatmap is used to visualise cellular prevalence patterns seen within each meta-cluster/base.\n\
Row side bar indicates the mutation meta-clusters/bases.\n\</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visCompReorder' in  files:
				w.write('<div class="img_txt">\n\
			<pre>This is the visualisation of multiple component planes reorded\n\
within a sheet-shape hexagonal grid.\n\
\n\
Each component illustrates the sample-specific map\n\
and is placed within a two-dimensional rectangular lattice.\n\
within each component, genes with the same or similar expression patters\n\
are mapped to the same or nearby map nodes.\n\
When zooming out to look at between-components/samples relationships,\n\
samples with the similar expression profiles are placed closer to each other.</pre>\n\
			</div>\n\
			</div>\n\n')

			elif 'SupraHex_visTreeBootstrap' in files:
				w.write('<div class="img_txt">\n\
			<pre>Visualises a simple phylogenetic tree\n\
\n\
A neighbour-joining tree is constructed based\n\
on pairwise euclidean distance matrices between samples.\n\
The robustness of tree branching is evaluated using bootstraping.\n\
In internal nodes (also color-coded), the number represents the proportion of bootstrapped trees\n\
that support the observed internal branching.\n\
The higher the number, the more robust the tree branching. \n\
100 means that the internal branching is always observed by resampling characters.</pre>\n\
			</div>\n\
			</div>\n\n')

#####################################Table with information about SupraHex#####################################
	w.write('<h2>Hexagon index information</h2>\n\
		<table style="width:100%">\n')

	os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')
	
	if os.path.exists("/home/shared_data_core/COLON/subclonality/"+ALL+"/PyClone_cellular_prevalence.supraHex_base_2.txt"):
		r = open('PyClone_cellular_prevalence.supraHex_base_2.txt', 'rb')

		w.write('\t\t<tr>\n')
		first_line = r.readline()
		for i in first_line.split('\t'):
			if not i == '\n':
				#print i
				w.write('\t\t\t<th>'+i.split('\n')[0]+'</th>\n')
		w.write('\t\t</tr>\n')


		for lines in r:
			w.write('\t\t<tr>\n')
			for u in lines.split('\t'):
				#print u.split('\n')[0]
				w.write('\t\t\t<td>'+u.split('\n')[0]+'</td>\n')
			w.write('\t\t</tr>\n')
		w.write('</table>\n')


#####################################table#####################################
	w.write('<h2>Cellular prevalence and Variant Allel frequency</h2>\n\
		<table style="width:100%">\n')

	os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')
	
	if os.path.exists("/home/shared_data_core/COLON/subclonality/"+ALL+"/parameters_"+ALL+".tsv"):
		r = open('parameters_'+ALL+'.tsv', 'rb')

		w.write('\t\t<tr>\n')
		first_line = r.readline()
		for i in first_line.split('\t'):
			if not i == '\n':
				#print i
				w.write('\t\t\t<th>'+i.upper()+'</th>\n')
		w.write('\t\t</tr>\n')


		for lines in r:
			w.write('\t\t<tr>\n')
			for u in lines.split('\t'):
				#print u.split('\n')[0]
				w.write('\t\t\t<td>'+u.split('\n')[0]+'</td>\n')
			w.write('\t\t</tr>\n')
		w.write('</table>\n')

	w.write('<script>\n\
// When the user scrolls down 20px from the top of the document, show the button\n\
window.onscroll = function() {scrollFunction()};\n\
\n\
function scrollFunction() {\n\
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {\n\
        document.getElementById("myBtn").style.display = "block";\n\
    } else {\n\
        document.getElementById("myBtn").style.display = "none";\n\
    }\n\
}\n\
\n\
// When the user clicks on the button, scroll to the top of the document\n\
function topFunction() {\n\
    document.body.scrollTop = 0;\n\
    document.documentElement.scrollTop = 0;\n\
}\n\
</script></body>\n\
</html>\n')

def main():

	paired_samples_all = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short_all.txt'
	clin_info = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
	log_file = '/home/shared_data_core/COLON/subclonality/log.txt'
	ALL = 'ALL'

	to_lower(paired_samples_all)
	names = patient_names(paired_samples_all)
	index(names, ALL)
	patient_report(ALL, clin_info, log_file, names)


if __name__ == "__main__":
	main()
