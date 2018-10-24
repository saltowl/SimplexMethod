import copy

def initBaseTable(a, b, c, baseTable):
	for i in range(1, len(c) + 1 + len(a)):
		baseTable[0].append('x' + str(i))
	
	baseTable[0].append('b')
	
	for i in range(1, len(a) + 1):
		baseTable.append(['x' + str(i + len(a) + 1)])
	
	baseTable.append(['c'])
	
	for i in range(1, len(a) + 1):
		baseTable[i] += copy.deepcopy(a[i - 1])
		for j in range(len(a)):
			value = 1 if i == j + 1 else 0
			baseTable[i].append(value)
		baseTable[i].append(b[i - 1])
	
	for i in range(len(c)):
		c[i] = -c[i]

	baseTable[len(a) + 1] += copy.deepcopy(c)
	
	for _ in range(len(a) + 1):
		baseTable[len(a) + 1].append(0)

def isOptimalPlan(baseTable, problemType):
	indexStr = baseTable[len(baseTable) - 1]

	for i in range(1, len(indexStr)):
		if ((indexStr[i] > 0) and (problemType == 'min')) or (
			(indexStr[i] < 0) and (problemType == 'max')):
			return False
	return True

def findColumn(baseTable, problemType):
	indexStr = baseTable[len(baseTable) - 1]
	maxVal = -1 if problemType == 'min' else float('inf')
	columnIndex = -1

	for i in range(1, len(indexStr)):
		if ((indexStr[i] > maxVal) and (problemType == 'min')) or (
			(indexStr[i] < maxVal) and (problemType == 'max')):
			maxVal = indexStr[i]
			columnIndex = i

	return columnIndex

def findString(column, baseTable):
	strIndex = -1
	minVal = float('inf')
	bIndex = len(baseTable[0]) - 1

	for i in range(1, len(baseTable) - 1):
		if baseTable[i][column] > 0:
			value = baseTable[i][bIndex] / baseTable[i][column]
			if value < minVal:
				minVal = value
				strIndex = i

	return strIndex

def recalcSimplexTable(string, column, baseTable):
	elem = baseTable[string][column]
	stringCount = len(baseTable)
	columnCount = len(baseTable[0])
	newTable = copy.deepcopy(baseTable)

	for i in range(1, columnCount):
		newTable[string][i] = int((newTable[string][i] / elem) * 100) / 100

	for i in range(1, stringCount):
		if i != string:
			for j in range(1, columnCount):
				newTable[i][j] = int((baseTable[i][j] - (baseTable[string][j] * baseTable[i][column]) / elem) * 100) / 100
			newTable[i][column] = 0

	newTable[string][0] = baseTable[0][column]
	return newTable

def simplexMethod(baseTable, problemType):
	while isOptimalPlan(baseTable, problemType) is False:
		column = findColumn(baseTable, problemType)
		string = findString(column, baseTable)
		baseTable = recalcSimplexTable(string, column, baseTable)
		
	return baseTable

def printResult(baseTable):
	result = []
	for i in range(len(baseTable[0]) - len(baseTable)):
		baseVar = False
		for j in range(len(baseTable) - 2):
			if baseTable[j + 1][0] == ('x' + str(i + 1)):
				baseVar = True
				break
		value = baseTable[j + 1][len(baseTable[0]) - 1] if baseVar else 0
		result.append(value)
	
	for i in range(len(result)):
		print('x' + str(i + 1) + ' = ' + str(result[i]))

def printTable(baseTable):
	for i in range(len(baseTable)):
		for j in range(len(baseTable[i])):
			print('{0:6} |'.format(baseTable[i][j]), end=' ')
		print()

def Main():
	a = [[2, 1, 3, 4], [1, -1, 2, 1], [0, 0, 1, 3]]
	b = [2, 4, 1]
	c = [-2, 3, 4, -1]
	baseTable = [['Basis']]

	initBaseTable(a, b, c, baseTable)

	print('Base table')
	printTable(baseTable)

	problemType = 'max' #'min'
	baseTable = simplexMethod(baseTable, problemType)

	print('\nFinal table')
	printTable(baseTable)

	print('\nResult')
	printResult(baseTable)

Main()
