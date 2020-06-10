#Script que toma 2 líneas de un archivo ordenado en formato CSV (comma separated values) y las compara
#usando los valores númericos de las columnas 3 y 4. Si los valores coinciden, no imprime la línea repetida.
#Básicamente es un script para quitar entradas repetidas siempre y cuando sean continuas (o sea, una seguida de la otra)
#Si las entradas repetidas no están seguidas, el script no lo detectar. Lo usé para filtrar trabajos repetidos de RAST
#
#Para usarlo sólo se necesita poner python3 filter.py $NOMBRE_DEL_ARCHIVO

import sys

CSV_FILE = sys.argv[1]

with open(CSV_FILE) as db:
	pieces1 = db.readline().rstrip().split(",")
	for line in db:
		pieces2 = line.rstrip().split(",")
		if int(pieces1[3]) == int(pieces2[3]) and int(pieces1[4]) == int(pieces2[4]): ##Cambia esta línea si quieres modificar los parámetros de comparación
			pieces1 = pieces2
			continue
		else:
			line2print = ",".join(pieces1)
			print(line2print)
			pieces1 = pieces2