
import random

# locals
from cell import Cell
from mapp import Mapp
from coord import Coord
from astar import aStar
class Pather:
	#TODO: constants to adjust
	def __init__(self ):
		"""
			the initial goal is simply full connectivity between rooms
	
			eventually redundant paths between all rooms will be necessary
				but that is as simple as creating a full circuit
		"""

	def getRandomWall(self, map, startRoomIndex):
		"""
			return the x, y coordinates of a piece on the wall,
					as well as a direction outward from the room
		"""
		startRoom = map.roomList[startRoomIndex] 	
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

	def addPath(self, mapp, startRoomIndex, endRoomIndex): 
		"""
			add a path between two rooms


			we can find out if the path needs to go
					north, south, east, west
	
			TODO: should be able to specify startX/Y, endX/Y
				or less specifically start wall and end wall
		"""
		if len(mapp.roomList) == 0:
			print "ERROR: No rooms!  Cannot create path."
			return
		#TODO: keep in mind self-connecting rooms
		startWallX, startWallY, startWall = self.getRandomWall(
				mapp, startRoomIndex) 
		endWallX, endWallY, endWall = self.getRandomWall(mapp, endRoomIndex) 
			# ensure path does not lead to itself 
		while startWallX == endWallX and startWallY == endWallY:
			endWallX, endWallY, wall = getRandomWall(endRoom) 
		mapp.cells[startWallY][startWallX].ascii = Cell.DOOR_SYMBOL	
		mapp.cells[endWallY][endWallX].ascii = Cell.DOOR_SYMBOL	
		beginX, beginY = self.getOutside(startWallX, startWallY, startWall)
		goalX, goalY = self.getOutside(endWallX, endWallY, endWall)  
		path = aStar(mapp.cells, beginX, beginY, goalX, goalY) 
		for coord in path:
			mapp.cells[coord.y][coord.x].ascii = Cell.CORRIDOR_SYMBOL	
		#TODO: include door cells? 
		mapp.pathList.append(path) 
