import fileinput

# A single cell in a SuDoKu table
class Cell(object):
	size = 9
	# x = x position in SuDoKu table starting from 0 on left (Row)
	# y = y position in SuDoKu table starting from 0 on top (Col)
	# subBox (see SubBox class)
	def __init__(self, x, y):
		self._x = x
		self._y = y
		self.subBox = 3 * (y/3) + x/3
		self.values = []
		self._cellValueUnknown = True
		for i in range(Cell.size):
			self.values.append(1)

	def __str__(self):
		st = ""
		if self.cellValueUnknown:
			for i in range(Cell.size):
				if self.values[i]:
					st += str(i+1)
				else:
					st += "-"
		else:
			return "    "+str(self.cellValue())+"    "
		return st
	
	@staticmethod
	def get_subbox(x, y):
		return 3 * (y/3) + (x/3)

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def cellValueUnknown(self):
		return self._cellValueUnknown

	@cellValueUnknown.setter
	def cellValueUnknown(self, value):
		self._cellValueUnknown = value

	# Returns the value of this Cell if sole value has been found, otherwise returns 0
	def cellValue(self):
		count = 0
		value = 0
		for i in range(Cell.size):
			if self.values[i]:
				count += 1
				value = i + 1
		if count == 1:
			return value
		else:
			return 0

	# Sets value to 0 in this cell and checks it this cell has a sole value found.
	# Returns sole value if one is found, otherwise returns 0
	def removeValue(self, value):
		self.values[value-1] = 0
		return self.cellValue()

	# Is called when a value has been found, and checks off all other cells in the subsections
	def valueFound(self, value):
		# If no value has been found yet
		if self.cellValueUnknown:
			print "Value Found "+" "+str(value)+ " at "+str(self.x)+", "+str(self.y)
			self.cellValueUnknown = False

			# update each subsection removing the rows and columns
			rows[self.x].updateSection(self, value)
			cols[self.y].updateSection(self, value)
			subboxes[self.subBox].updateSection(self, value)
			

	# same as valueFound except, also set this value as true
	def setValueFound(self, value):
		#for v in self.values: # (A note for later) This bit doesn't work for some reason.
		#	v = 0
		for i in range(Cell.size):
			self.values[i] = 0
		self.values[value - 1] = 1
		self.valueFound(value)
	

class SubSection(object):
	def __init__(self):
		self.Cells = []

	def __str__(self):
		st = ""
		for v in self.Cells:
			st += str(v) + "|"
		return st

	# Add cell to subsection - during initialisation of data structures only
	def add_cell(self, cell):
		self.Cells.append(cell)

	# Update all cells in subsection, and check if this is the last value in sub section
	def updateSection(self, cell, value):
		# Iterate through all cells in sub-section, except for 'cell'
		for c in self.Cells:
			#s = "c = "+str(c)+" cell = "+str(cell)+" NOT SAME ="+str(c != cell)
			#print s
			try:
				if c != cell:

					if c.cellValueUnknown:
						# Remove 'value' from possible values of this cell
						# Store the result of whether a sole value of this cell has been found as a result of this
						val = c.removeValue(value)

						# If a sole value has been found, check other corresponding subections recursively.
						# (Note for later) Might be able to move this bit into removeValue itself.
						if val:
							#print "Test Value Found "+" "+str(val)+ " at "+str(c.x)+", "+str(c.y)
							c.valueFound(val)

			except RuntimeError as re:
				if re.args[0] != 'maximum recursion depth exceeded':
				# different type of runtime error
					print('Sorry but this was not able to finish {}'.format(re.args[0]))

	def get_cell(self, index):
		return self.Cells[index]

# A row in a SuDoKu table starting from 0 at the top
class Row(SubSection):
	def __init__(self, values):
		super(Row, self).__init__(values)

# A column in a SuDoKu table starting from 0 on the left
class Col(SubSection):
	def __init__(self, values):
		super(Col, self).__init__(values)

# A sub box (square) in a SuDoKu table starting from 0 on the top left
# then coounting from left to right, top to bottom
class SubBox(SubSection):
	def __init__(self, values):
		super(SubBox, self).__init__(values)

# Create and initialise cell, row, col and subbox data structures
global size, rows, cols, subboxes, allCells
rows = []
cols = []
subboxes = []
allCells = []


# Initialise sub section variables
for i in range(Cell.size):
	rows.append(SubSection())
	cols.append(SubSection())
	subboxes.append(SubSection())

# Initialise cells and add to sub section variables, and fill allCells
for i in range(Cell.size):
	columns = [] # temporary variable used to fill allCells
	for j in range(Cell.size):
		cell = Cell(i,j)
		rows[i].add_cell(cell)
		cols[j].add_cell(cell)
		subboxes[Cell.get_subbox(i,j)].add_cell(cell)
		columns.append(cell)
	allCells.append(columns)

i = 0
for line in fileinput.input():
	j = 0
	while j < len(line) and j < Cell.size:
		if line[j] != "-":
			#s = "x = "+str(i)+", y = "+str(j)+", value = "+str(line[j])
			#print s
			Cell.recursiveCount = 0
			allCells[i][j].setValueFound(int(line[j]))
		j += 1
	i += 1

print "\n\n"

# Print out SuDoKu table
for i in range(Cell.size):
	for j in range(Cell.size):
		s = str(allCells[i][j])+" |"
		print s,
	print " "

#for r in rows:
#	print r
#	print " "
