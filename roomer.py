
import random

# local
from util import *
from cell import Cell
from room import Room

class Roomer: 
	DEFAULT_MIN_ROOMS = 3
	DEFAULT_MAX_ROOMS = 10 
	DEFAULT_MIN_ROOM_WIDTH = 5 # all disclude walls 
	DEFAULT_MIN_ROOM_HEIGHT = 3  
	DEFAULT_MAX_ROOM_WIDTH = 8 
	DEFAULT_MAX_ROOM_HEIGHT = 5 
	DEFAULT_MAX_TRIES = 30
	def __init__(self, minRooms = None, maxRooms = None, 
				minRoomWidth = None, maxRoomWidth = None,
				minRoomHeight = None, maxRoomHeight = None,
				maxTries = None):
		self.minRooms = noneSet(minRooms, Roomer.DEFAULT_MIN_ROOMS) 
		self.maxRooms = noneSet(maxRooms, Roomer.DEFAULT_MAX_ROOMS) 
		self.minRoomWidth = noneSet(minRoomWidth, Roomer.DEFAULT_MIN_ROOM_WIDTH) 
		self.minRoomHeight = noneSet(minRoomHeight, Roomer.DEFAULT_MIN_ROOM_HEIGHT) 
		self.maxRoomWidth = noneSet(maxRoomWidth, Roomer.DEFAULT_MAX_ROOM_WIDTH) 
		self.maxRoomHeight = noneSet(maxRoomHeight, Roomer.DEFAULT_MAX_ROOM_HEIGHT) 
		self.maxTries = noneSet(maxTries, Roomer.DEFAULT_MAX_TRIES)

	def addRooms(self, map):  
		ctr = 0
		while True:
			for i in range(0, self.maxRooms):
				ctr = i + 1
				if not self.addRoom(map):
					break 
			if ctr >= self.minRooms:
				break
			else:
				map.reset()

	def addRoom(self, mapp): 
		"""
			returns True if it could add a room with ease,
					False if it got all tuckered out
		"""
		# 2 for walls
		map = mapp.cells
		maxStartX = mapp.width - 2 - self.minRoomWidth 
		maxStartY = mapp.height - 2 - self.minRoomHeight 
		numTries = 0
		while True:
			startX = random.randint(0, maxStartX)  
			startY = random.randint(0, maxStartY)  
			# 3 because 2 for walls + at least 1 for inside
			endX = random.randint(
					min(mapp.width - 1, 
							max(startX + 3, startX + self.minRoomWidth + 1)), 
					min(mapp.width - 1, startX + self.maxRoomWidth + 1)) 
			endY = random.randint(min(mapp.height - 1,
							max(startY + 3, startY + self.minRoomHeight + 1)), 
					min(mapp.height - 1, startY + self.maxRoomHeight + 1)) 
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
			if adjEndX >= mapp.width:
				adjEndX = mapp.width - 1
			if adjEndY >= mapp.height: 
				adjEndY = mapp.height - 1
			for i in range(adjStartY, adjEndY + 1):
				for j in range(adjStartX, adjEndX + 1):
					if map[i][j].ascii != Cell.EMPTY_SYMBOL:
						passes = False
			# if the perimeter is all wall, then we can dig out a room
			if passes:
				break
			else:
				numTries += 1
				#print "numTries = %d" % numTries
			if numTries == self.maxTries:
				return False
		#print "decided to make a room between x=%d,y=%d and x=%d,y=%d" % (
		#		startX, startY, endX, endY)
		# first we draw the walls horizontally
		for j in range(startX, endX + 1):
			map[startY][j].ascii = Cell.HORIZONTAL_WALL_SYMBOL
			map[endY][j].ascii = Cell.HORIZONTAL_WALL_SYMBOL
		# then we draw the walls vertically
		for i in range(startY, endY + 1):
			map[i][startX].ascii = Cell.VERTICAL_WALL_SYMBOL
			map[i][endX].ascii = Cell.VERTICAL_WALL_SYMBOL 
		# then we draw the corners
		map[startY][startX].ascii = Cell.TOP_CORNER_SYMBOL
		map[startY][endX].ascii = Cell.TOP_CORNER_SYMBOL
		map[endY][startX].ascii = Cell.BOTTOM_CORNER_SYMBOL
		map[endY][endX].ascii = Cell.BOTTOM_CORNER_SYMBOL
		# then we draw the innards
		for i in range(startY + 1, endY):
			for j in range(startX + 1, endX):
				map[i][j].ascii = Cell.FLOOR_SYMBOL 
		# then we make this room easier to find
		# rooms should denote their contents though, not the walls
		newRoom = Room(len(mapp.roomList), 
				startX + 1, startY + 1, 
				endX - startX - 2, endY - startY - 2)
		mapp.roomList.append(newRoom)
		return True
