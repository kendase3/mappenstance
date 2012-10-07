#! /usr/bin/env python 

import sys
import random

class Cell:
	def __init__(self):
		self.ascii = Mapp.EMPTY_SYMBOL

class Room:
	def __init__(self, x, y, width, height):
		self.x = x 
		self.y = y 
		self.width = width 
		self.height = height 

class Mapp:
	"""
		returned list is in [y,x] format
	"""
	DEFAULT_MAP_WIDTH = 80 
	DEFAULT_MAP_HEIGHT = 24 
	DEFAULT_MIN_ROOMS = 3
	DEFAULT_MAX_ROOMS = 10 
	DEFAULT_MIN_ROOM_WIDTH = 5 # all disclude walls 
	DEFAULT_MIN_ROOM_HEIGHT = 3  
	DEFAULT_MAX_ROOM_WIDTH = 8 
	DEFAULT_MAX_ROOM_HEIGHT = 5 
	DEFAULT_MAX_TRIES = 30
	HORIZONTAL_WALL_SYMBOL = '-' 
	VERTICAL_WALL_SYMBOL = '|' 
	TOP_CORNER_SYMBOL = '-' 
	BOTTOM_CORNER_SYMBOL = '-' 
	EMPTY_SYMBOL = ' ' 
	FLOOR_SYMBOL = '.'

	def __init__(self, width = None, height = None, minRooms = None, 
				maxRooms = None, minRoomWidth = None, maxRoomWidth = None, 
				minRoomHeight = None, maxRoomHeight = None, maxTries = None):
		if width == None:
			self.width = Mapp.DEFAULT_MAP_WIDTH
		else:
			self.width = width
		if height == None:
			self.height = Mapp.DEFAULT_MAP_HEIGHT
		else:
			self.height = height 
		if minRooms == None:
			self.minRooms = Mapp.DEFAULT_MIN_ROOMS
		else:
			self.minRooms = minRooms
		if maxRooms == None:
			self.maxRooms = Mapp.DEFAULT_MAX_ROOMS
		else:
			self.maxRooms = maxRooms
		if minRoomWidth == None:
			self.minRoomWidth = Mapp.DEFAULT_MIN_ROOM_WIDTH
		else:
			self.minRoomWidth = minRoomWidth 
		if maxRoomWidth == None:
			self.maxRoomWidth = Mapp.DEFAULT_MAX_ROOM_WIDTH 
		else:
			self.maxRoomWidth = maxRoomWidth 
		if minRoomHeight == None:
			self.minRoomHeight = Mapp.DEFAULT_MIN_ROOM_HEIGHT
		else:
			self.minRoomHeight = minRoomHeight 
		if maxRoomHeight == None: 
			self.maxRoomHeight = Mapp.DEFAULT_MAX_ROOM_HEIGHT
		else:
			self.maxRoomHeight = maxRoomHeight 
		if maxTries == None:
			self.maxTries = Mapp.DEFAULT_MAX_TRIES 
		else:
			self.maxTries = maxTries

		self.cells = [[Cell() for j in range(self.width)] 
				for i in range(self.height)]
		self.roomList = [] 

	def reset(self):
		self.roomList = []
		for row in self.cells:
			for cell in row:
				cell.ascii = Mapp.EMPTY_SYMBOL

	def prnt(self):
		for row in self.cells:
			for cell in row:
				sys.stdout.write(cell.ascii) 
			print

	def addRooms(self):
		ctr = 0
		#TODO: appraise this
		while True:
			for i in range(0, self.maxRooms):
				ctr = i + 1
				if not self.addRoom():
					break 
			if ctr >= self.minRooms:
				break
			else:
				self.reset()

	def addRoom(self):
		"""
			returns True if it could add a room with ease,
					False if it got all tuckered out
		"""
		# 2 for walls
		map = self.cells
		maxStartX = self.width - 2 - self.minRoomWidth 
		maxStartY = self.height - 2 - self.minRoomHeight
		numTries = 0
		while True:
			startX = random.randint(0, maxStartX)  
			startY = random.randint(0, maxStartY)  
			# 3 because 2 for walls + at least 1 for inside
			endX = random.randint(
					min(self.width - 1, 
							max(startX + 3, startX + self.minRoomWidth + 1)), 
					min(self.width - 1, startX + self.maxRoomWidth + 1)) 
			endY = random.randint(min(self.height - 1,
							max(startY + 3, startY + self.minRoomHeight + 1)), 
					min(self.height - 1, startY + self.maxRoomHeight + 1)) 
			# we ensure it does not collide with existing rooms
			# by checking entire proposed innards
			passes = True
			# adjust values to ensure we leave spaces between rooms
			adjStartX = startX - 1
			adjStartY = startY - 1
			adjEndX = endX + 1
			adjEndY = endY + 1
			if adjStartX < 0:
				adjStartX = 0
			if adjStartY < 0:
				adjStartY = 0
			if adjEndX >= self.width:
				adjEndX = self.width - 1
			if adjEndY >= self.height: 
				adjEndY = self.height - 1
			for i in range(adjStartY, adjEndY + 1):
				for j in range(adjStartX, adjEndX + 1):
					if map[i][j].ascii != Mapp.EMPTY_SYMBOL:
						passes = False
			# if the perimeter is all wall, then we can dig out a room
			if passes:
				break
			else:
				numTries += 1
				#print "numTries = %d" % numTries
			if numTries == self.maxTries:
				return False
		print "decided to make a room between x=%d,y=%d and x=%d,y=%d" % (
				startX, startY, endX, endY)
		# first we draw the walls horizontally
		for j in range(startX, endX + 1):
			map[startY][j].ascii = Mapp.HORIZONTAL_WALL_SYMBOL
			map[endY][j].ascii = Mapp.HORIZONTAL_WALL_SYMBOL
		# then we draw the walls vertically
		for i in range(startY, endY + 1):
			map[i][startX].ascii = Mapp.VERTICAL_WALL_SYMBOL
			map[i][endX].ascii = Mapp.VERTICAL_WALL_SYMBOL 
		# then we draw the corners
		map[startY][startX].ascii = Mapp.TOP_CORNER_SYMBOL
		map[startY][endX].ascii = Mapp.TOP_CORNER_SYMBOL
		map[endY][startX].ascii = Mapp.BOTTOM_CORNER_SYMBOL
		map[endY][endX].ascii = Mapp.BOTTOM_CORNER_SYMBOL
		# then we draw the innards
		for i in range(startY + 1, endY):
			for j in range(startX + 1, endX):
				map[i][j].ascii = Mapp.FLOOR_SYMBOL 
		# then we make this room easier to find
		# rooms should denote their contents though, not the walls
		newRoom = Room(startX + 1, startY + 1, 
				endX - startX - 2, endY - startY - 2)
		self.roomList.append(newRoom)
		return True

map = Mapp() 
map.prnt() 
map.addRooms() 
map.prnt()
for room in map.roomList:
	map.cells[room.y][room.x].ascii = 's' 
	map.cells[room.y + room.height][room.x + room.width].ascii = 'e' 
map.prnt()
