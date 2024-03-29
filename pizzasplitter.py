#!/usr/bin/python

import sys
import filehandler as fh
import math as m
import numpy as np
from math import sqrt
from itertools import count, islice
from timeit import default_timer as timer

exploredNodes = 0
lastper = 0
#divisions = 0

def main(argv): # We expect to receive input file as first argument and output file second argument (optional). If output not specified, defaults to input+.out
	if len(argv) < 1:
		print("Input file location expected. Output file can be also specified (optional)")
		return
	input = argv[0]
	output = input + ".out"
	maxLevel = 5
	maxSlices = 50
	if len(argv) > 1:
		output = argv[1]
	try:
		if len(argv) > 2:
			maxLevel = int(argv[2])
	except:
		print("maxLevel must be an integer. Default to maxLevel=5")
		maxLevel = 5
	try:
		if len(argv) > 3:
			maxSlices = int(argv[3])
	except:
		print("maxSlices must be an integer. Default to maxSlices=50")
		maxSlices = 50
	try:
		r, c, l, h, pizza, numM, numT = fh.loadPFile(input)
		#if isPrime(h) and h != 2:
		#	h -= 1
		#	print ("H is a prime number. A slice can't have H cells if H is prime (not 2).\nReducing H to " + str(h))
	except Exception as e:
		print (str(e))
		print ("Program ended with errors!")
		return
	start = timer()
	sol = splitP(r, c, l, h, pizza, numM, numT, maxLevel=maxLevel, maxSlices=maxSlices, entropy = True)
	end = timer()
	print("\nTime elapsed: %.4f seconds." % round(end-start, 4))
	print (str(sol[0]) + " slices")
	#print (sol[1])
	print ("Score: " + str(sol[2]) + "/" + str(c*r))
	global exploredNodes
	print ("Explored Nodes: " + str(exploredNodes))
	fh.savePFile(output, sol)

def getEntropy(tupleCounts, total):
	#for i in range(len(tupleCounts)):
	#	aux = tupleCounts[i]/total
	#	if aux != 0:
	#		sum += aux * np.log2(aux)
	#return -sum
	
	sum = 0
	
	auxOne = np.count_nonzero(tupleCounts)
	auxZero = total - auxOne
	sum += abs((auxOne / total) * np.log2(auxOne / total))
	sum += abs((auxZero / total) * np.log2(auxZero / total))
	
	return sum

def calculateCut(r, c, pizza, entropy = False):
	if entropy:
		entropyScore = 0 #getEntropy(pizza,np.size(pizza))
		verticalCut = False
		for provisional_cut in range(1,r-1):
			ent = 0			
			r1 = provisional_cut
			r2 = r - provisional_cut
			c1 = c
			c2 = c
			pizza1 = pizza[:provisional_cut,:]
			total = np.size(pizza1)
			ent += getEntropy(pizza1, total) * (np.size(pizza1)/total)
			pizza2 = pizza[provisional_cut:,:]
			total = np.size(pizza2)
			ent += getEntropy(pizza2, total) * (np.size(pizza2)/total)
			if ent > entropyScore:
				entropyScore = ent
				cut = provisional_cut
		for provisional_cut in range(1,c-1):
			ent = 0			
			r1 = r
			r2 = r
			c1 = provisional_cut
			c2 = c - provisional_cut
			pizza1 = pizza[:,:provisional_cut]
			ent += getEntropy(pizza1, pizza1.size)
			pizza2 = pizza[:,provisional_cut:]
			ent += getEntropy(pizza2, pizza2.size)
			if ent > entropyScore:
				entropyScore = ent
				cut = provisional_cut
				verticalCut = True
	else:
		verticalCut = c > r
		if verticalCut:
			cut = c//2
		else:
			cut = r//2

	if verticalCut:
		pizza1 = pizza[:,:cut]
		pizza2 = pizza[:,cut:]
		r1 = r
		r2 = r
		c1 = cut
		c2 = c - cut
	else:
		pizza1 = pizza[:cut,:]
		pizza2 = pizza[cut:,:]
		r1 = cut
		r2 = r - cut
		c1 = c
		c2 = c
	
	return (r1, c1, pizza1, r2, c2, pizza2, cut, verticalCut)

def countIng(pizza):
	countT = np.sum(pizza)
	return (pizza.size-countT, countT)

def nCr(n, r):
	f = m.factorial
	sol = 0
	if r <= n:
		sol = f(n) // f(r) // f(n-r)
	return sol

def calcComb(n, ms):
	sum = 0
	for i in range(1, ms+1):
		sum += nCr(n, i)
	return sum

def isPrime(n):
	return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

def splitP(r, c, l, h, pizza, numM, numT, maxLevel=5, maxSlices=50, percentage=100, offset=0, entropy = False):
	# El numero de combinaciones posibles sera de 1 + pslices!/((pslices-1)! * 1!) + ... + pslices!/(0!*pslices!)
	# Para 34 sera de 17179869182, que con el metodo definido es computacionalmente asumible gracias a la poda.
	# Habiendo calculado la cota superior del numero maximo posible de splits que puede tener una combinacion valida,
	# dicho numero se reduce a el sumatorio de numeros combinatorios pslices C i, donde i va desde 1 hasta maxSplit.
	# Asi tenemos que hay 6579 combinaciones validas (sin comprobar colisiones) distintas.
	# Sin embargo, ya para el caso small con 100 slices diferentes y como mucho las configuraciones pueden tener 18,
	# tenemos mas de 38 * 10^18 combinaciones distintas posibles. Para el caso big, ni siquiera se puede calcular
	# el numero de diferentes slices posibles, tarda demasiado.
	# Así vemos que este caso no es computacionalmente asumible. Por ello, dado que no podremos obtener el óptimo
	# cuando el tamaño del problema sea muy grande, procederemos a tratar de alcanzar una solucion subóptima,
	# dividiendo la pizza en partes mas pequeñas hasta que dichas partes sean de un tamaño para el que podamos
	# calcular sin problemas el óptimo, y agregar las soluciones óptimas para alcanzar el subóptimo.
	maxSplit = upperBound(numM, numT, l)
	#print ("At most you can made " + str(maxSplit) + " splits.")
	# Ahora, en el caso de que la profundidad máxima del árbol sea mayor que un umbral, dividiremos la pizza en dos partes
	# y obtendremos la solución para cada parte.
	if maxSplit <= maxLevel:
		#entropy = getEntropy((numM, numT), pizza.size)
		#print ("Entropy of the pizza: " + str(entropy) + " bits.")
		pslices = possibleSlices(r, c, l, h, pizza)
		#print ("There are " + str(len(pslices)) + " different posible slices")
		if len(pslices) <= maxSlices and len(pslices) > 0:
			#ncomb = calcComb(len(pslices), maxSplit)
			#print ("There are " + str(ncomb) + " different nodes")

			result = tree(r, c, l, h, pizza, pslices, [], maxSplit, [])
			sol = (len(result[0]), result[0], result[1])
		elif len(pslices) == 0:
			sol = (0, [], 0)
	if maxSplit > maxLevel or len(pslices) > maxSlices:
		#global divisions
		#divisions += 1
		#print (str(divisions) + " hard splits done.")
		(r1, c1, pizza1, r2, c2, pizza2, cut, verticalCut) = calculateCut(r, c, pizza, entropy = entropy)
		num1 = countIng(pizza1)
		num2 = (numM-num1[0], numT-num1[0])
		sol1 = splitP(r1, c1, l, h, pizza1, num1[0], num1[1], maxLevel=maxLevel, maxSlices=maxSlices, percentage=percentage/2, offset=offset, entropy = entropy)
		global lastper
		if (m.floor(percentage/2+offset) != lastper):
			lastper = m.floor(percentage/2+offset)
			print(str(lastper) + "%")
		sol2 = splitP(r2, c2, l, h, pizza2, num2[0], num2[1], maxLevel=maxLevel, maxSlices=maxSlices, percentage=percentage/2, offset=offset+percentage/2, entropy = entropy)
		if (m.floor(percentage+offset) != lastper):
			lastper = m.floor(percentage+offset)
			print(str(lastper) + "%")
		for i in range(len(sol2[1])):
			if verticalCut:
				sol2[1][i] = ((sol2[1][i][0][0], sol2[1][i][0][1] + cut), (sol2[1][i][1][0], sol2[1][i][1][1] + cut))
			else:
				sol2[1][i] = ((sol2[1][i][0][0] + cut, sol2[1][i][0][1]), (sol2[1][i][1][0] + cut, sol2[1][i][1][1]))
		try:
			sol = (sol1[0] + sol2[0], sol1[1] + sol2[1], sol1[2] + sol2[2])
		except:
			if sol1[2] == None:
				sol = sol2
			else:
				sol = sol1
	return sol

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
	dnodes.append(slices)
	if len(slices) > ubound:
		result = (slices, None) # Slices, Score
	else:
		result = (slices, validState(slices, pizza, r, c, l, h))
		if result[1] != None and len(slices) < ubound:
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
