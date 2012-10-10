
import random

# locals
from cell import Cell
from mapp import Mapp
from coord import Coord
from astar import aStar

#BIG_PATHS= True
#BIG_PATHS= False 
BIG_PATH_PERCENTAGE = 50 

class Pather:
	"""
		a pather makes paths between rooms in a map with rooms.

		those rooms could have been created manually or with a roomer
	"""
	#TODO: constants to adjust
	def __init__(self ):
		"""
			the initial goal is simply full connectivity between rooms
	
			eventually redundant paths between all rooms will be necessary
				but that is as simple as creating a full circuit
		"""

	def getRandomWall(self, mapp, roomIndex):
		"""
			return the x, y coordinates of a piece on the wall,
					as well as a direction outward from the room

			this method will now not return cells that are on the map border
		"""
		room = mapp.roomList[roomIndex] 	
		haveValidWall = False
		while not haveValidWall:
			wall = random.randint(0, 3)
			x = 0
			y = 0
			if wall == Mapp.NORTH: # then north wall
				x = random.randint(room.x, room.x + room.width) 
				y = room.y - 1	
			elif wall == Mapp.EAST: # then east wall
				x = room.x + room.width + 1	
				y = random.randint(room.y, room.y + room.height)
			elif wall == Mapp.SOUTH: # then south wall
				x = random.randint(room.x, room.x + room.width)
				y = room.y + room.height + 1
			elif wall == Mapp.WEST: # then west wall
				x = room.x - 1
				y = random.randint(room.y, room.y + room.height)
			if x != 0 and x != (mapp.width - 1) and (
					y != 0 and (y != mapp.height - 1)):
				haveValidWall = True 
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

	def withinBounds(self, mapp, x, y):
		if x < 0 or x >= mapp.width:
			return False 
		if y < 0 or y >= mapp.height:
			return False
		return True

	def addPaths(self, mapp):
		"""
			ensure rooms are fully connected

			add paths until edges = rooms - 1
		"""
		connectedRooms = []
		unconnectedRooms = mapp.roomList[:] 
		connectedRooms.append(unconnectedRooms.pop(0)) 
		while len(unconnectedRooms) > 0:
			startRoomIndex = random.randint(0, len(connectedRooms) - 1) 
			endRoomIndex = random.randint(0, len(unconnectedRooms) - 1)
			bigPath = False
			# we decide if this path will be big
			#TODO: medium path that only checks north and east
			if random.randint(0, 100) <= BIG_PATH_PERCENTAGE:
				bigPath = True
			self.addPath(mapp, connectedRooms[startRoomIndex].id, 
					unconnectedRooms[endRoomIndex].id, bigPath) 
			connectedRooms.append(unconnectedRooms.pop(endRoomIndex))

	def getStartLocation(self, mapp, startRoomIndex, endRoomIndex): 
		startWallX, startWallY, startWall = self.getRandomWall(
				mapp, startRoomIndex) 
		endWallX, endWallY, endWall = self.getRandomWall(mapp, endRoomIndex) 
			# ensure path does not lead to itself 
		while startWallX == endWallX and startWallY == endWallY:
			endWallX, endWallY, wall = self.getRandomWall(mapp, endRoomIndex) 
		mapp.cells[startWallY][startWallX].ascii = Cell.DOOR_SYMBOL	
		mapp.cells[endWallY][endWallX].ascii = Cell.DOOR_SYMBOL	
		beginX, beginY = self.getOutside(startWallX, startWallY, startWall)
		# we need to check bounds on our outside cells 
		goalX, goalY = self.getOutside(endWallX, endWallY, endWall)  
		return beginX, beginY, goalX, goalY

	def addPath(self, mapp, startRoomIndex, endRoomIndex, bigPath): 
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
		#REM: keep in mind self-connecting rooms
		beginX, beginY, goalX, goalY = self.getStartLocation(
				mapp, startRoomIndex, endRoomIndex)
		"""
		while not (
				self.withinBounds(mapp, beginX, beginY) and
				self.withinBounds(mapp, goalX, goalY)):
			beginX, beginY, goalX, goalY = self.getStartLocation(mapp, 
					startRoomIndex, endRoomIndex)
		"""
		path = aStar(mapp.cells, beginX, beginY, goalX, goalY) 
		for coord in path:
			mapp.cells[coord.y][coord.x].ascii = Cell.CORRIDOR_SYMBOL	
			if bigPath:
				self.bigPath(coord.x, coord.y, mapp)
		#TODO: include door cells?  or src and dst room id's? 
		mapp.pathList.append(path) 

	def bigPath(self, x, y, mapp):
		neighbors = []
		# we'll check north
		neighbors.append(Coord(x, y - 1))
		# then east
		neighbors.append(Coord(x + 1, y))
		# then south
		neighbors.append(Coord(x, y + 1))
		# finally west	
		neighbors.append(Coord(x - 1, y))
		for neighbor in neighbors:
			if self.withinBounds(mapp, neighbor.x, neighbor.y) and (
					mapp.cells[neighbor.y][neighbor.x].ascii == (
					Cell.EMPTY_SYMBOL)): 
				mapp.cells[neighbor.y][neighbor.x].ascii = Cell.CORRIDOR_SYMBOL	

