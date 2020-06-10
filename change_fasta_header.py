#Script para cambiar el header de los fasta que empiecen con >gi (los que salen de los genomas)
#en el alineamiento de aminoacidos. Lo cambia de >gi|RASTid (numero.numero)|... a 
#                                                >RASTid (numero_numero)
#
#Para usarlo se pone en la terminal python3 change_fasta_header.py $ARCHIVO_DE_ALINEAMIENTO
#

import sys

ARCHIVO_DE_ALINEAMIENTO_DE_AA_DE_EVOMINING = sys.argv[1]

with open(ARCHIVO_DE_ALINEAMIENTO_DE_AA_DE_EVOMINING) as f:
	for line in f:
		if line.startswith(">gi"):
			uno = line.split("|")[1]
			dos = uno.replace(".", "_")
			print(">{}".format(dos))
		else:
			print(line)