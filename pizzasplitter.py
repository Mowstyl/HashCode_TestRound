#!/usr/bin/python

import sys
import filehandler as fh
import math as m
import numpy as np

def main(argv): # We expect to receive input file as first argument and output file second argument (optional). If output not specified, defaults to a.out
	if len(argv) < 1:
		print("Input file location expected. Output file can be also specified (optional)")
		return
	input = argv[0]
	output = "a.out"
	if len(argv) > 1:
		output = argv[1]
	try:
		r, c, l, h, pizza = fh.loadPFile(input)
	except Exception as e:
		print (str(e))
		print ("Program ended with errors!")
		return
	sol = splitP(r, c, l, h, pizza)
	print (sol)

def splitP(r, c, l, h, pizza):
	minSplit = lowerBound(r, c, h)
	maxSplit = upperBound(r, c, l)
	return (minSplit, maxSplit)

def validState(slices, rows, cols): # Funcion que comprueba colisiones/solapamientos
	mat = np.zeros(rows*cols).reshape((rows,cols))
	result = True
	for slice in slices:
		x1, x2 = slice[0][0], slice[1][0]
		y1, y2 = slice[0][1], slice[1][1]
		if x1 > x2:
			x1, x2 = x2, x1
		if y1 > y2:
			y1, y2 = y2, y1
		if np.any(mat[x1:x2+1, y1:y2+1]):
			result = False
			break
		mat[x1:x2+1, y1:y2+1] += 1
	return result

def upperBound(r, c, l): # Maximo numero de porciones para el que se cumplen las restricciones
	return m.floor(r*c/(2*l))

def lowerBound(r, c, h): # Minimo numero de porciones, optimo
	return m.ceil(r*c/h)

if __name__ == "__main__":
	main(sys.argv[1:])
