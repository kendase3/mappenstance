#! /usr/bin/env python 

import sys
import random

MAP_WIDTH = 10
MAP_HEIGHT = 10
MIN_ROOM_WIDTH = 2   
MIN_ROOM_HEIGHT = 2 
MAX_ROOM_WIDTH = 8
MAX_ROOM_HEIGHT = 8

class Cell:
	def __init__(self):
		self.ascii = '~'


def makeRoom():
	"""
		TODO: make sure there's no room there currently
	"""
	# 2 for walls
	maxStartX = MAP_WIDTH - 2 - MIN_ROOM_WIDTH
	maxStartY = MAP_HEIGHT - 2 - MIN_ROOM_HEIGHT
	startX = random.randint(0, maxStartX)  
	startY = random.randint(0, maxStartY)  
	endX = random.randint(startX + 2, MAP_WIDTH - 1) 

cells = [[Cell() for j in range(MAP_WIDTH)] 
			for i in range(MAP_HEIGHT)]

for row in cells:
	for cell in row:
		sys.stdout.write(cell.ascii) 
	print
