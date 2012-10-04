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


def initMap(width, height): 
	"""
		returned list is in [y,x] format
	"""
	cells = [[Cell() for j in range(width)] 
			for i in range(height)]
	return cells
	

def addRoom(map):
	"""
		TODO: make sure there's no room there currently
	"""
	# 2 for walls
	maxStartX = MAP_WIDTH - 2 - MIN_ROOM_WIDTH
	maxStartY = MAP_HEIGHT - 2 - MIN_ROOM_HEIGHT
	startX = random.randint(0, maxStartX)  
	startY = random.randint(0, maxStartY)  
	# 3 because 2 for walls + at least 1 for inside
	endX = random.randint(startX + 3, MAP_WIDTH - 1) 
	endY = random.randint(startY + 3, MAP_HEIGHT - 1) 
	print "decided to make a room between x=%d,y=%d and x=%d,y=%d" % (
			startX, startY, endX, endY)
	# first we draw the walls horizontally
	for j in range(startX, endX + 1):
		map[startY][j].ascii = '+'
		map[endY][j].ascii = '+'
	# then we draw the walls vertically
	for i in range(startY, endY + 1):
		map[i][startX].ascii = '+'
		map[i][endX].ascii = '+' 
	# then we draw the innards
	for i in range(startY + 1, endY):
		for j in range(startX + 1, endX):
			map[i][j].ascii = '_' 

def printMap(map):
	for row in map:
		for cell in row:
			sys.stdout.write(cell.ascii) 
		print

map = initMap(MAP_WIDTH, MAP_HEIGHT) 
printMap(map)
addRoom(map)	
printMap(map)
