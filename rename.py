#Quick script to replace the name of fasta files from RAST with the
#jobID. To work, the files' first line should look like this:
#>fig|6666666.119578.peg.1 and then the filename would look like this: 6666666_119578.fasta
#
#The files also need to have the .fasta extension
#
#To run the script just put it on the same directory as the fasta files and run it with python3 rename.py

import glob, os

list_files = [f for f in glob.glob("*.fasta")]

for file in list_files:
	with open(file) as f:
		first = f.readline()
	new_file_name = first.replace(">fig|","").replace(".peg.1\n","").replace(".","_") + ".fasta"
	os.rename(file,new_file_name)
	print("replaced {} with {}".format(file,new_file_name))
