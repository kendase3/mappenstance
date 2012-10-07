#! /usr/bin/env python 

import sys
import random

# locals
from cell import Cell
from room import Room

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
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

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
				cell.ascii = Cell.EMPTY_SYMBOL

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
		newRoom = Room(len(self.roomList), 
				startX + 1, startY + 1, 
				endX - startX - 2, endY - startY - 2)
		self.roomList.append(newRoom)
		return True

	def getRandomWall(self, startRoomIndex):
		"""
			return the x, y coordinates of a piece on the wall,
					as well as a direction outward from the room
		"""
		startRoom = self.roomList[startRoomIndex] 	
		wall = random.randint(0, 3)
		x = 0
		y = 0
		if wall == Mapp.NORTH: # then north wall
			x = random.randint(startRoom.x, startRoom.x + startRoom.width) 
			y = startRoom.y - 1	
			
		elif wall == Mapp.EAST: # then east wall
			x = startRoom.x + startRoom.width + 1	
			y = random.randint(startRoom.y, startRoom.y + startRoom.height)
		elif wall == Mapp.SOUTH: # then south wall
			x = random.randint(startRoom.x, startRoom.x + startRoom.width)
			y = startRoom.y + startRoom.height + 1
		elif wall == Mapp.WEST: # then west wall
			x = startRoom.x - 1
			y = random.randint(startRoom.y, startRoom.y + startRoom.height)

		return x, y, wall

	def getOutside(self, x, y, wall):
		if wall == Mapp.NORTH:
			return x, y - 1
		elif wall == Mapp.EAST:
			return x + 1, y
		elif wall == Mapp.SOUTH:
			return x, y + 1
		elif wall == Mapp.WEST:
			return x - 1, y
		else:
			print "ERROR: getOutside called with %d" % wall
			exit() 

	def getNextMove(self, deltaX, deltaY):
		# each iteration it's a toss-up between at most two directions
		# we're deciding what our next move will be
		nextMove = Mapp.NORTH
		decision = random.randint(0, abs(deltaX) + abs(deltaY) - 1)
		if decision < abs(deltaX): 
			if deltaX > 0:
				nextMove = Mapp.EAST
			else:
				nextMove = Mapp.WEST
		else:
			if deltaY > 0:
				nextMove = Mapp.SOUTH
			else:	
				nextMove = Mapp.NORTH
		return nextMove

	def getOtherMove(self, deltaX, deltaY, firstMove):
		"""
			a few assumptions here:
				-if delta == 0, will move northeast
				-getNextMove will never move opposite to a delta
		"""
		northSouthMove = Mapp.NORTH
		eastWestMove = Mapp.EAST
		if deltaX < 0:
			eastWestMove = Mapp.WEST
		if deltaY < 0:
			northSouthMove = Mapp.SOUTH 
		if firstMove == northSouthMove:
			return eastWestMove
		else:
			return northSouthMove

	def addPath(self): 
		"""
			add a path between two rooms


			we can find out if the path needs to go
					north, south, east, west
		"""
		if len(self.roomList) == 0:
			print "ERROR: No rooms!  Cannot create path."
			return
		#TODO: keep in mind self-connecting rooms
		"""
		startRoom = random.randint(0, len(self.roomList) - 1) 
		endRoom = random.randint(0, len(self.roomList) - 1) 
		startX, startY, startWall = getRandomWall(startRoom) 
		endX, endY, endWall = getRandomWall(endRoom) 
			# ensure path does not lead to itself 
			while startX == endX and startY == endY:
				endX, endY, wall = getRandomWall(endRoom) 
		self.cells[startY][startX].ascii = Mapp.DOOR_SYMBOL	
		self.cells[endY][endX].ascii = Mapp.DOOR_SYMBOL	
		curX, curY = getOutside(startX, startY, startWall)
		goalX, goalY = getOutside(endX, endY, endWall)  
		while not (curX == goalX and curY == goalY):
			deltaX = goalX - curX
			deltaY = goalY - curY
			nextMove = self.getNextMove(deltaX, deltaY)
			backupMove = self.getOtherMove(deltaX, deltaY, nextMove)
		"""

if __name__=="__main__":
	map = Mapp() 
	map.addRooms() 
	map.prnt()
