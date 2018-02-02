#!/usr/bin/python

import sys
import filehandler as fh
import math as m
import numpy as np
from math import sqrt
from itertools import count, islice

exploredNodes = 0

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
		if isPrime(h) and h != 2:
			h -= 1
			print ("H is a prime number. A slice can't have H cells if H is prime (not 2).\nReducing H to " + str(h))
	except Exception as e:
		print (str(e))
		print ("Program ended with errors!")
		return
	sol = splitP(r, c, l, h, pizza)
	print (sol)
	global exploredNodes
	print ("Explored Nodes: " + str(exploredNodes))

def isPrime(n):
	return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

def splitP(r, c, l, h, pizza):
	minSplit = lowerBound(r, c, h)
	maxSplit = upperBound(r, c, l)
	print ("There will be between " + str(minSplit) + " and " + str(maxSplit) + " splits.")
	result = tree(r, c, l, h, pizza, [], minSplit, maxSplit)
	return (len(result[0]), result[0], result[1])

def tree(r, c, l, h, pizza, slices, lbound, ubound):
	global exploredNodes
	exploredNodes += 1
	#print (str(exploredNodes))
	if len(slices) > ubound:
		return (None, None) # Slices, Score
	else:
		result = (slices, validState(slices, pizza, r, c, l, h))
		if result[1] == None:
			return result
		for x1 in range(r):
			for y1 in range(c):
				for x2 in range(x1, min(r, x1+h)):
					for y2 in range(y1, min(c, x2+h)):
						nsli = slices[:] + [((x1,y1),(x2,y2))]
						nres = tree(r, c, l, h, pizza, nsli, lbound, ubound)
						if nres[1] != None and result[1] < nres[1]:
							result = nres
						if result[1] == pizza.size:
							return result
	return result

def validState(slices, pizza, rows, cols, l, h): # Funcion que comprueba colisiones/solapamientos, H y L. Devuelve el score si el estado es válido, None en cualquier otro caso.
	mat = np.zeros(rows*cols).reshape((rows,cols))
	result = 0
	for slice in slices:
		x1, x2 = slice[0][0], slice[1][0]
		y1, y2 = slice[0][1], slice[1][1]
		if x1 > x2:
			x1, x2 = x2, x1
		if y1 > y2:
			y1, y2 = y2, y1
		amat = mat[x1:x2+1, y1:y2+1]
		psli = pizza[x1:x2+1, y1:y2+1]
		tcount = np.sum(psli)
		mcount = psli.size - tcount
		if np.any(amat) or psli.size > h or tcount < l or mcount < l:
			result = None
			break
		result += psli.size
		mat[x1:x2+1, y1:y2+1] += 1
	return result

def upperBound(r, c, l): # Maximo numero de porciones para el que se cumplen las restricciones
	return m.floor(r*c/(2*l))

def lowerBound(r, c, h): # Minimo numero de porciones, optimo
	return m.ceil(r*c/h)

if __name__ == "__main__":
	main(sys.argv[1:])
