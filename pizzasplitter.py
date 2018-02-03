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
		r, c, l, h, pizza, numM, numT = fh.loadPFile(input)
		if isPrime(h) and h != 2:
			h -= 1
			print ("H is a prime number. A slice can't have H cells if H is prime (not 2).\nReducing H to " + str(h))
	except Exception as e:
		print (str(e))
		print ("Program ended with errors!")
		return
	sol = splitP(r, c, l, h, pizza, numM, numT)
	print (sol)
	global exploredNodes
	print ("Explored Nodes: " + str(exploredNodes))

def isPrime(n):
	return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

def splitP(r, c, l, h, pizza, numM, numT):
	pslices = possibleSlices(r, c, l, h, pizza)
	print ("There are " + str(len(pslices)) + " different posible slices")
	maxSplit = upperBound(numM, numT, l)
	print ("At most you can made " + str(maxSplit) + " splits.")
	result = tree(r, c, l, h, pizza, pslices, [], maxSplit, [])
	return (len(result[0]), result[0], result[1])

def possibleSlices(r, c, l, h, pizza):
	slices = []
	for x1 in range(r):
		for y1 in range(c):
			for x2 in range(x1, min(r, x1+h)):
				for y2 in range(y1, min(c, x2+h)):
					if x1 != x2 or y1 != y2:
						slice = ((x1,y1),(x2,y2))
						if validSlice(pizza, slice, l, h):
							slices.append(slice)
	sorted(slices, key=sliceSize, reverse=True)
	return slices

def getSlice(pizza, slice):
	x1, x2 = slice[0][0], slice[1][0]
	y1, y2 = slice[0][1], slice[1][1]
	if x1 > x2:
		x1, x2 = x2, x1
	if y1 > y2:
		y1, y2 = y2, y1
	return pizza[x1:x2+1, y1:y2+1]

def validSlice(pizza, slice, l, h):
	psli = getSlice(pizza, slice)
	size = psli.size
	nTom = np.sum(psli)
	nMush = size-nTom
	return size <= h and nTom >= l and nMush >= l

def sliceSize(slice):
	x1, x2 = slice[0][0], slice[1][0]
	y1, y2 = slice[0][1], slice[1][1]
	return abs(x2-x1) * abs(y2-y1)

def tree(r, c, l, h, pizza, pslices, slices, ubound, dnodes):
	# PSlices son todos las posibles porciones que se pueden tener siguiendo las reglas en la pizza dada.
	# Slices es una lista de cortes, los realizados por este nodo.
	# UBound es la cota superior para el numero posible de slices maximo que puede haber. No hay soluciones con mas slices. Es imposible.
	# DNodes es una lista con los nodos ya explorados, incluyendo el actual mejor.
	global exploredNodes
	exploredNodes += 1
	#if dnodes == []:
	#	print ("vacuo")
	#print (str(exploredNodes))
	if len(slices) > ubound:
		result = (slices, None) # Slices, Score
	else:
		result = (slices, validState(slices, pizza, r, c, l, h))
		if result[1] != None:
			for i in range(len(pslices)):
				nsli = slices[:] + [pslices[i]]
				nsli.sort()
				if nsli not in dnodes:
					npslices = pslices[:]
					del npslices[i]
					nres = tree(r, c, l, h, pizza, npslices, nsli, ubound, dnodes)
					if nres[1] != None and result[1] < nres[1]:
						result = nres
					if result[1] == pizza.size:
						break
	dnodes.append(slices)
	return result

def validState(slices, pizza, rows, cols, l, h): # Funcion que comprueba colisiones/solapamientos. Devuelve el score si el estado es válido, None en cualquier otro caso.
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
		if np.any(amat):
			result = None
			break
		result += amat.size
		mat[x1:x2+1, y1:y2+1] += 1
	return result

def upperBound(numM, numT, l): # Maximo numero de porciones para el que se cumplen las restricciones de numero de ingredientes sin tener en cuenta la posicion
	return m.floor(min(numM, numT)/l)

if __name__ == "__main__":
	main(sys.argv[1:])
