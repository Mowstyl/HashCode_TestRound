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
	pizza = []
	for i in range(r):
		line = f.readline().strip()
		if line == None:
			raise ValueError("Invalid number of rows! Expected " + str(r))
		if len(line) != c:
			raise ValueError("Invalid number of columns! Expected " + str(c) + " Found " + str(len(line)))
		row = []
		for char in line:
			if char == "M":
				row.append(0)
			elif char == "T":
				row.append(1)
			else:
				raise ValueError("Invalid character! Please only use M and T!")
		pizza.append(row)
	return (r, c, l, h, pizza)
