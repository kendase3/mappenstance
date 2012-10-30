
import random

from cell import Cell
from room import Room


class Populator:
	DEFAULT_STAIR_NUM = 1  # we default to one up, one down 
	def __init__(self):
		pass

	def hasUnassignedRoom(self, roomList):
		for room in roomList:
			if room.type == None:
				return True
		return False

	def hasUnassignedCell(self, room, mapCells):
		for i, row in enumerate(mapCells[room.y:room.y+room.height]):
			for j, cell in enumerate(row[room.x:room.x+room.width]):
					# then it's in the room	
					if cell.ascii == Cell.FLOOR_SYMBOL:
						return True 
		return False

	def getUnassignedRoom(self, roomList):
		if not self.hasUnassignedRoom(roomList):
			print 'ERROR: insufficient rooms'
			return
		index = None 
		while index == None or roomList[index].type != None:
			index = random.randint(0, len(roomList) - 1)
		return roomList[index]

	def getUnassignedCell(self, room, mapCells):
		if not self.hasUnassignedCell(room, mapCells):
			print 'ERROR: insufficient cells in selected room'
			return
		xOffset = None
		# while there's something in the cell we've selected, get a new one
		while xOffset == None or ( mapCells[room.y + yOffset][room.x + xOffset].ascii != Cell.FLOOR_SYMBOL): 
			xOffset = random.randint(0, room.width - 1)
			yOffset = random.randint(0, room.height - 1)
		return mapCells[room.y + yOffset][room.x + xOffset] 
		
	def addStairs(self, mapp, numStairsUp=None, 
				numStairsDown=None):
		if numStairsUp == None:
			numStairsUp = Populator.DEFAULT_STAIR_NUM
		if numStairsDown == None:
			numStairsDown = Populator.DEFAULT_STAIR_NUM
		for i in range(0, numStairsUp):
			targetRoom = self.getUnassignedRoom(mapp.roomList)	
			targetCell = self.getUnassignedCell(targetRoom, mapp.cells)
			targetCell.ascii = Cell.STAIRS_UP_SYMBOL
			targetRoom.type = 'stairsup' 
		for i in range(0, numStairsDown):
			targetRoom = self.getUnassignedRoom(mapp.roomList)	
			targetCell = self.getUnassignedCell(targetRoom, mapp.cells)
			targetCell.ascii = Cell.STAIRS_DOWN_SYMBOL
			targetRoom.type = 'stairsdown' 
		
