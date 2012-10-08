
import os, sys
from cell import Cell
from room import Room

class Mapp:
	"""
		returned list is in [y,x] format
	"""
	DEFAULT_MAP_WIDTH = 80 
	DEFAULT_MAP_HEIGHT = 25 
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	def __init__(self, width = None, height = None): 
		if width == None:
			self.width = Mapp.DEFAULT_MAP_WIDTH
		else:
			self.width = width
		if height == None:
			self.height = Mapp.DEFAULT_MAP_HEIGHT
		else:
			self.height = height 

		self.cells = [[Cell() for j in range(self.width)] 
				for i in range(self.height)]
		self.roomList = [] 
		self.pathList = []

	def reset(self):
		self.roomList = []
		for row in self.cells:
			for cell in row:
				cell.ascii = Cell.EMPTY_SYMBOL

	def prnt(self):
		for row in self.cells:
			for cell in row:
				sys.stdout.write(cell.ascii) 
			print


