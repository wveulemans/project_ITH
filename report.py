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



def patient_names(paired_samples):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
		----------
	    	Function: makes a list with every patient_name
		----------
		Output: list with all patient_names

	"""

	r = open(paired_samples, 'rb')
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

	

def index(names):
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
	for name in names:
		w.write('\t<li><a href="http://localhost:8000/patient_report_'+name+'.php">patient_'+name+'</a></li>\n')
	w.write('</ul>\n\
<div style="margin-left:8%;padding:1px 16px;height:1000px;">\n\
 <h2>Project: intra tumor heterogeneity</h2>\n\
 <p>This is a website created to share information about the tumour heterogeneity from different patients</p>\n\
</div>\n\
</div>\n\
</body>\n\
</html>\n')
	w.close()


def patient_report(name, clin_info, log_file, names):
	os.chdir('/home/shared_data_core/COLON/subclonality/')
	w = open('patient_report_%s.php'% name, 'wb')
	os.chmod('patient_report_%s.php'% name, 0755)
	
	w.write('<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
<meta charset="utf-8">\n\
<title>Patient report %s</title>\n'% name)
	w.write('\t<style type="text/css" media="screen">\n\
ul {\n\
	list-style-type: none;\n\
	margin: 0;\n\
	padding: 0;\n\
	overflow: hidden;\n\
	background-color: #333;\n\
}\n\
li {\n\
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
.a {\n\
    float: right;\n\
    position: relative;\n\
    display: inline-block;\n\
}\n\
.b {\n\
    display: none;\n\
    position: absolute;\n\
    background-color: #f9f9f9;\n\
    min-width: 160px;\n\
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n\
    z-index: 1;\n\
}\n\
.c:hover .b {\n\
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
	margin: 10px 5px;\n\
}\n\
h3 {\n\
	margin: 10px 5px;\n\
}\n\
.header {\n\
	float: left;\n\
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
	height: 750px;\n\
	width: 750px;\n\
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
</style>\n\
</head>\n\
<body>\n\
	<ul>\n\
  		<li><a href="http://localhost:8000/index.php">Home</a></li>\n\
		<li class="dropdown">\n\
    			<a href="javascript:void(0)" class="dropbtn">Dropdown</a>\n\
    			<div class="dropdown-content">\n')
	for i in names:
		w.write('\t\t\t<a href="http://localhost:8000/patient_report_'+i+'.php">patient_'+i+'</a>\n')
      			
    	w.write('\t\t\t</div>\n\
  		</li>\n\
	</ul>\n')

	w.write('<div class="a">\n\
  <img src="person.jpg" alt="unknown_person" width="50" height="100">\n\
  <div class="b">\n\
    <img src="person.jpg" alt="unknown_person" width="200" height="300">\n\
    <div class="desc">Photo: patient '+name+'</div>\n\
  </div>\n\
</div>\n')
	w.write('\t<h1>Patient %s</h1>\n'% name.upper())
	w.write('\t<div class=geheel>\n\
		<h2>Information</h2>\n\
		<div class="navlinks">\n')
	
	r = open(clin_info, 'rb')
	reader = csv.reader(r, delimiter=',')
	next(reader)	# skip header
	for line in reader:
		if line[0] == name:
			w.write('\t\t<h3>General information</h3>\n\
		<ul>\n\
			<li>Gender: '+str(line[6]).upper()+'</li>\n\
			<li>Date of birth: '+line[3]+'</li>\n\
			<li>Date of death: '+line[4]+'</li>\n\
		</ul>\n\n\
		<h3>Diagnosis + primary tumor</h3>\n\
		<ul>\n\
			<li>Diagnosis: '+line[1]+'</li>\n\
			<li>Date diagnosis: '+line[2]+'</li>\n\
			<li>Date of biopsy (Primary Tumor): '+line[7]+'</li>\n\
			<li>Amount of primary tumors: '+line[8]+'</li>\n\
			<li>Age when sample taken: '+line[9]+'</li>\n\
			<li>Chemo before biopsy: '+line[11]+'</li>\n\
		</ul>\n\n\
		<h3>Metastasis</h3>\n\
		<ul>\n\
			<li>Biopsy metastasis: '+line[12]+'</li>\n\
			<li>Amount of metastasis: '+line[13]+'</li>\n\
			<li>Places of metastasis: '+line[14]+'</li>\n\
			<li>Date diagnosis metassatis: '+line[15]+'</li>\n\
			<li>Age when sample taken: '+line[16]+'</li>\n\
			<li>Chemo before biopsy: '+line[18]+'</li>\n\
		</ul>\n\n\
		<h3>Mutation information</h3>\n\
		<ul>\n\
			<li>Mutation test: '+line[22]+'</li>\n\
			<li>Estimates amount of tumorcells: '+line[23]+'</li>\n\
			<li>Gene + codon: '+line[24]+'</li>\n\
			<li>Method + sensitivity: '+line[25]+'</li>\n\
			<li>Mutation: '+line[26]+'</li>\n\
			<li>tested for MSI: '+line[27]+'</li>\n\
			<li>MSI result: '+line[28]+'</li>\n\
			<li>pTNM: '+line[29]+'</li>\n\
			<li>Differentationdegree: '+line[30]+'</li>\n\
			<li>Chemotype: '+line[31]+'</li>\n\
		</ul>\n\n\
		<h3>Other</h3>\n\
		<ul>\n\
			<li>Smoker: '+line[19]+'</li>\n\
			<li>Alcohol use: '+line[21]+'</li>\n\
			<li>Familial oncological background: '+line[32]+'</li>\n\
			<li>Comment: '+line[33]+'</li>\n\
			<li>Patient state: '+line[34]+'</li>\n\
		</ul>\n\
		</div>\n\n\
		<h2>PyClone visual output</h2>\n')

	os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
	source = glob.glob('*')
	
	for files in source:
		if 'PyClone' in files and '.png' in files:
			#print files
			#print ' '.join((files.split('.')[0]).split('_')[0:3])
			w.write('\t\t<div class="plot">\n\
		<h3>'+' '.join((files.split('.')[0]).split('_')[0:3])+'</h3>\n\
		<img src="/%s/'% name +files+'" alt="'+files.split('.')[0]+'">\n\
		<div class="img_txt">\n\
		<pre>This is text</pre>\n\
		</div>\n\
		</div>\n\n')

	w.write('\t\t<h2>SupraHex visual output</h2>\n\n')

	for files in source:
		if 'SupraHex' in files and '.png' in files:
			#print files
			#print ' '.join((files.split('.')[0]).split('_')[0:3])
			w.write('\t\t<div class="plot">\n\
		<h3>'+' '.join((files.split('.')[0]).split('_')[0:3])+'</h3>\n\
		<img src="/%s/'% name +files+'" alt="'+files.split('.')[0]+'">\n\
		<div class="img_txt">\n\
		<pre>This is text</pre>\n\
		</div>\n\
		</div>\n\n')
	
	w.write('\t\t<div class="header">\n\
		<h2>Comments</h2>\n\
		<pre>\n')
	major_cn = 0
	r = open(log_file, 'rb')
	next(r)
	for line in r:
		if 'Patient %s:'% name in line and 'major_cn' in line and '!ARTEFACT!' in line:
			#print line
			major_cn += 1
		elif 'Patient %s: '% name in line:
			w.write('\t\tFile: '+(line.split('\t')[6]).split(' ')[4]+' is empty!\n')
				 

	#print major_cn
	w.write('\t\tPatient %s has in '%name + str(major_cn) +' cases a major copy number above 6!\n\
		</pre>\n\
		</div>\n\
		</div>\n\
</body>\n\
</html>\n')
	

def main():
	paired_samples = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
	clin_info = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
	log_file = '/home/shared_data_core/COLON/subclonality/log.txt'

	to_lower(paired_samples)
	names = patient_names(paired_samples)
	index(names)
	for name in names:
		patient_report(name, clin_info, log_file, names)


if __name__ == "__main__":
	main()
