#Script para imprimir el archivo de alineamiento de aminoácidos cambiando los aa por nucleotidos (excepto en el caso de los MiBIG hits)
#Para eso el script necesita que le indiques el directorio donde están los archivos fasta de RAST (y que se llamen RASTid.fasta)
#y el archivo de alineamiento de aminoácidos. Los MiBIG hits se quedan en blanco
#
#Para correrlo sólo se pone en línea de comando: python3 replace_extract.py $ARCHIVO_DE_ALINEAMIENTO_DE_AA $DIRECTORIO_CON_LOS_FASTA


import os
import sys

ALN_file = sys.argv[1]
DIR = sys.argv[2]

with open(ALN_file) as f:
	for line in f:
		if line.startswith(">gi"):
			broken_line1 = line.split("|")[1]
			new_title = broken_line1.replace(".","_")
			file_name = DIR + new_title.split("_")[0] + "_" + new_title.split("_")[1] + ".fasta"
			position = "." + new_title.split("_")[2] + "\n"
			if os.path.isfile(file_name):
				with open(file_name) as ff:
					data = ff.readlines()
					for single_line in data:
						if position in single_line:
							num_linea = data.index(single_line) + 1
							print(">{}".format(new_title))
							while not(data[num_linea].startswith(">")):
								print(data[num_linea].rstrip())
								num_linea+=1
							break
			else:
				print(line)

		elif line.startswith(">"):
			print(line)


