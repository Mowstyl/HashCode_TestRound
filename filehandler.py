#!/usr/bin/python

import numpy as np

# In this file we have the methods to parse the input file
def loadPFile(filename):
	f = open(filename, "r")
	if f == None:
		raise ValueError("File not found!")
	first = f.readline().split()
	if len(first) != 4:
		raise ValueError('Bad formatted file! First line must contain "R C L H"')
	try:
		r, c, l, h = [int(x) for x in first]
	except:
		raise ValueError('R, C, L and H must be integers!')
	if r < 1 or r > 1000 or c < 1 or c > 1000 or l < 1 or l > 1000 or h < 1 or h > 1000:
		raise ValueError('R, C, L, H must be between 1 and 1000 included!')
	if 2*l > h:
		raise ValueError("Maximum number of cells per slice can't be smaller than 2 x number of cells of each type")
	pizza = []
	countT = 0
	countM = 0
	for i in range(r):
		line = f.readline()
		if line == None:
			raise ValueError("Invalid number of rows! Expected " + str(r))
		line = line.strip()
		if len(line) != c:
			raise ValueError("Invalid number of columns! Expected " + str(c) + " Found " + str(len(line)))
		row = []
		for char in line:
			if char == "M":
				row.append(0)
				countM += 1
			elif char == "T":
				row.append(1)
				countT += 1
			else:
				raise ValueError("Invalid character! Please only use M and T!")
		pizza.append(row)
	return (r, c, l, h, np.array(pizza), countM, countT)

# In this file we have the methods to parse the input file
def savePFile(filename, sol):
	f = open(filename, "w+")
	f.write(str(sol[0]) + '\n')
	for split in sol[1]:
		f.write(str(split[0][0]) + ' ' + str(split[0][1]) + ' ' + str(split[1][0]) + ' ' + str(split[1][1]) + '\n')
