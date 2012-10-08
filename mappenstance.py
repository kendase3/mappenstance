#! /usr/bin/env python 

import sys
import random

# locals
from cell import Cell
from room import Room
from astar import aStar
from coord import Coord
from roomifier import Roomifier

class Mapp:
	"""
		returned list is in [y,x] format
	"""
	DEFAULT_MAP_WIDTH = 80 
	DEFAULT_MAP_HEIGHT = 24 
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

if __name__=="__main__":
	map = Mapp() 
	roomifier = Roomifier()
	roomifier.addRooms(map) 
	map.prnt()
	#path = aStar(map.cells, 0, 0, 1, 1)
	#print path
