a = [[2, 1, 3, 4], [1, -1, 2, 1], [0, 0, 1, 3]]
b = [2, 4, 1]
c = [-2, 3, 4, -1]

baseTable = [['Basis']]

def initBaseTable():
	for i in range(1, len(c) + 1 + len(a)):
		baseTable[0].append('x' + str(i))
	
	baseTable[0].append('b')
	
	for i in range(1, len(a) + 1):
		baseTable.append(['x' + str(i + len(a) + 1)])
	
	baseTable.append(['c'])
	
	for i in range(1, len(a) + 1):
		baseTable[i] += a[i - 1][:]
		for j in range(len(a)):
			value = 1 if i == j + 1 else 0
			baseTable[i].append(value)
		baseTable[i].append(b[i - 1])
	
	for i in range(len(c)):
		c[i] = -c[i]

	baseTable[len(a) + 1] += c[:]
	
	for _ in range(len(a) + 1):
		baseTable[len(a) + 1].append(0)

def isOptimalPlan():
	indexStr = baseTable[len(baseTable) - 1]

	for i in range(1, len(indexStr)):
		if indexStr[i] > 0: # cos minimization problem
			return False
	return True

def findColumn():
	indexStr = baseTable[len(baseTable) - 1]
	maxVal = -1
	columnIndex = -1

	for i in range(1, len(indexStr)):
		if indexStr[i] > maxVal:
			maxVal = indexStr[i]
			columnIndex = i

	return columnIndex

def findString(column):
	strIndex = -1
	minVal = float('inf')
	bIndex = len(baseTable[0]) - 1

	for i in range(1, len(a) + 1):
		if baseTable[i][column] != 0:
			value = baseTable[i][bIndex] / baseTable[i][column]
			if value < minVal:
				minVal = value
				strIndex = i

	return strIndex

def recalcSimplexTable(string, column):
	elem = baseTable[string][column]
	stringCount = len(baseTable)
	columnCount = len(baseTable[0])
	newTable = baseTable[:][:]

	for i in range(1, columnCount):
		newTable[string][i] /= elem

	for i in range(2, stringCount):
		for j in range(1, columnCount):
			newTable[i][j] = baseTable[i][j] - (baseTable[string][j] * baseTable[i][column]) / elem

	newTable[string][0] = baseTable[0][column]
	return newTable

def simplexMethod():
	while isOptimalPlan() is False:
		column = findColumn()
		string = findString(column)
		baseTable = recalcSimplexTable(string, column)

def printResult():
	result = c[:]
	for i in range(len(c)):
		baseVar = False
		for j in range(len(a)):
			if baseTable[j + 1][0] == ('x' + str(i + 1)):
				baseVar = True
				break
		result[i] = 1 if baseVar else 0
	for i in range(len(result)):
		print('x' + str(i + 1) + ' = ' + str(result[i]))

def Main():
	initBaseTable()

	for i in range(len(baseTable)):
		print(baseTable[i])

	simplexMethod()
	for i in range(len(baseTable)):
		print(baseTable[i])

	printResult()

Main()
