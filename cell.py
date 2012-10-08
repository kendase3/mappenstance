
class Cell:
	HORIZONTAL_WALL_SYMBOL = '-' 
	VERTICAL_WALL_SYMBOL = '|' 
	TOP_CORNER_SYMBOL = '-' 
	BOTTOM_CORNER_SYMBOL = '-' 
	EMPTY_SYMBOL = ' ' 
	FLOOR_SYMBOL = '.'
	DOOR_SYMBOL = '+'
	def __init__(self):
		self.ascii = Cell.EMPTY_SYMBOL
