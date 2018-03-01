import numpy as np
import os
import shutil
import re

# #############################################################################

# ############### Comandos de interés de Lectura ##############################

# #############################################################################

# Abre archivo en modo lectura
archivo = open('MANN_a9.clq.txt','r')

# Lectura linea por linea | linea[0] == primer caracter
linea = archivo.readline()

# Localizamos la linea que contiene el string deseado
re.search('Graph Size:',linea)

# Partición de linea por caracter
linea = linea.split(',')

# Filtrado por enteros
size = int(re.sub("\D","",linea[0]))

# Devuelve una copia del string eliminando los caracteres indicados. Default espacio.
line = line.rstrip()

# Filtrado mediante expresion regular
re.findall('[0-9]+',line)

# Cierre de fichero
archivo.close()

# #############################################################################

# ############### Comandos de interés de Escritura ############################

# #############################################################################

# In this file we have the methods to parse the input file
def savePFile(filename, sol):
	if not os.path.exists(filename):
		os.makedirs(filename)
		shutil.rmtree(filename)

	f = open(filename, "w+")
	f.write(str(sol[0]) + '\n')
	for split in sol[1]:
        f.write(str(split[0][0]) + ' ' + str(split[0][1]) + ' ' + str(split[1][0]) + ' ' + str(split[1][1]) + '\n')
