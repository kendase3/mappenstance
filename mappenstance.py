#! /usr/bin/env python 

import sys
import random

MAP_WIDTH = 80 
MAP_HEIGHT = 24 
MIN_ROOM_WIDTH = 2   
MIN_ROOM_HEIGHT = 2 
MAX_ROOM_WIDTH = 8 
MAX_ROOM_HEIGHT = 2 
MAX_TRIES = 30

WALL_SYMBOL = '+' 
EMPTY_SYMBOL = '~' 
FLOOR_SYMBOL = '_'

class Cell:
	def __init__(self):
		self.ascii = EMPTY_SYMBOL


def initMap(width, height): 
	"""
		returned list is in [y,x] format
	"""
	cells = [[Cell() for j in range(width)] 
			for i in range(height)]
	return cells

def min(a, b):
	if a < b:
		return a
	else:
		return b	

def addRoom(map):
	"""
		returns True if it could add a room with ease,
				False if it got all tuckered out
	"""
	#TODO: could add wrapper function to ensure min/max # of rooms and just restart
	#		level creation if it's a wash 

	# 2 for walls
	maxStartX = MAP_WIDTH - 2 - MIN_ROOM_WIDTH
	maxStartY = MAP_HEIGHT - 2 - MIN_ROOM_HEIGHT
	numTries = 0
	while True:
		startX = random.randint(0, maxStartX)  
		startY = random.randint(0, maxStartY)  
		# 3 because 2 for walls + at least 1 for inside
		endX = random.randint(startX + 3, min(MAP_WIDTH - 1, startX + MAX_ROOM_WIDTH + 1)) 
		endY = random.randint(startY + 3, min(MAP_HEIGHT - 1, startY + MAX_ROOM_HEIGHT + 1)) 
		# we ensure it does not collide with existing rooms
		passes = True
		# we check each perimeter cell along the two vertical sides
		for i in range(startY, endY + 1):
			if map[i][startX].ascii != EMPTY_SYMBOL or map[i][endX].ascii != EMPTY_SYMBOL:
				passes = False
		# we check each perimeter cell along the two horizontal sides 
		for i in range(startX, endX + 1):
			if map[startY][i].ascii != EMPTY_SYMBOL or map[endY][i].ascii != EMPTY_SYMBOL:
				passes = False
		# if the perimeter is all wall, then we can dig out a room
		if passes:
			break
		else:
			numTries += 1
			#print "numTries = %d" % numTries
		if numTries == MAX_TRIES:
			return False
	print "decided to make a room between x=%d,y=%d and x=%d,y=%d" % (
			startX, startY, endX, endY)
	# first we draw the walls horizontally
	for j in range(startX, endX + 1):
		map[startY][j].ascii = WALL_SYMBOL
		map[endY][j].ascii = WALL_SYMBOL
	# then we draw the walls vertically
	for i in range(startY, endY + 1):
		map[i][startX].ascii = WALL_SYMBOL
		map[i][endX].ascii = WALL_SYMBOL 
	# then we draw the innards
	for i in range(startY + 1, endY):
		for j in range(startX + 1, endX):
			map[i][j].ascii = FLOOR_SYMBOL 
	return True

def printMap(map):
	for row in map:
		for cell in row:
			sys.stdout.write(cell.ascii) 
		print

map = initMap(MAP_WIDTH, MAP_HEIGHT) 
printMap(map)
while addRoom(map):
	pass	
printMap(map)
