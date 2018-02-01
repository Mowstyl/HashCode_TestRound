#!/usr/bin/python

import sys
import filehandler as fh
import math as m

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

def upperBound(r, c, l): # Maximo numero de porciones para el que se cumplen las restricciones
	return m.floor(r*c/(2*l))

def lowerBound(r, c, h): # Minimo numero de porciones, optimo
	return m.ceil(r*c/h)

if __name__ == "__main__":
	main(sys.argv[1:])
