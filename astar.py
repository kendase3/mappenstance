#! /usr/bin/env python
"""
	an implementation of the A* algorithm
"""

import math

# locals
from cell import Cell
from coord import Coord 

class Node:
	"""
		self-aware x,y wrapper for cells in a-star
	"""
	CORRIDOR_COST = 1
	ROCK_COST = 3 
	WALL_COST = 1E5 # arbitrarily high number 
	ROOM_COST = 1E5
	DOOR_COST = 1E7
	def __init__(self, map, x, y, dstX, dstY, prev = None):
		self.cell = map[y][x] 
		self.x = x
		self.y = y
		self.prev = prev
		self.prevCost = 0 
		if prev != None:
			self.prevCost = self.prev.cost
		self.cost = self.prevCost + self.getCellCost() 
		self.heuristic = getHeuristic(x, y, dstX, dstY) 
		self.score = self.cost + self.heuristic

	def __repr__(self):
		return 'x=%d,y=%d' % (self.x, self.y)

	def getCellCost(self):
		if self.cell.ascii == Cell.EMPTY_SYMBOL:
			return Node.ROCK_COST
		elif self.cell.ascii == Cell.TOP_CORNER_SYMBOL or (
				self.cell.ascii == Cell.BOTTOM_CORNER_SYMBOL or
				self.cell.ascii == Cell.HORIZONTAL_WALL_SYMBOL or
				self.cell.ascii == Cell.VERTICAL_WALL_SYMBOL):
			return Node.WALL_COST
		elif self.cell.ascii == Cell.FLOOR_SYMBOL:
			return Node.ROOM_COST
		elif self.cell.ascii == Cell.CORRIDOR_SYMBOL:
			return Node.CORRIDOR_COST
		elif self.cell.ascii == Cell.DOOR_SYMBOL:
			return Node.DOOR_COST
		else:
			print "ERROR: unknown symbol %c, assuming wall!" % self.cell.ascii 
			return Node.WALL_COST 
	
	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True	
		else:
			return False

def getLowestScoreNode(lst):
	"""
		precondition: list is not empty
	""" 
	curLowest = lst[0]
	for node in lst:
		if node.score < curLowest.score:
			curLowest = node
	return curLowest

def hasNode(x, y, set):
	for node in set:
		if node.x == x and node.y == y:
			return True
	return False	

def getNode(node, set):
	for curNode in set:
		if node.x == curNode.x and node.y == curNode.y:
			return curNode
	return None	

def addNeighbors(curNode, openSet, closedSet, map, dstX, dstY):
	"""
		add the current node's neighbors to the open list
	"""
	neighbors = []
	if curNode.x != 0:
		x = curNode.x - 1
		y = curNode.y
		neighbors.append(Node(map, x, y, 
				dstX, dstY, curNode))	
	if curNode.x < (len(map[0]) - 1): 
		x = curNode.x + 1
		y = curNode.y
		neighbors.append(Node(map, x, y, 
				dstX, dstY, curNode))	
	if curNode.y != 0:
		x = curNode.x
		y = curNode.y - 1
		neighbors.append(Node(map, x, y, 
				dstX, dstY, curNode))	
	if curNode.y < (len(map) - 1):
		x = curNode.x
		y = curNode.y + 1
		neighbors.append(Node(map, x, y, 
				dstX, dstY, curNode))	
	for neighbor in neighbors:
		if not hasNode(neighbor.x, neighbor.y, closedSet):
			if hasNode(neighbor.x, neighbor.y, openSet):
				oldNode = getNode(neighbor, openSet) 
				# we compare the costs of this new version
				#	to the old version
				if neighbor.cost < oldNode.cost:
					# then we use this version of the neighbor
					openSet.remove(oldNode)
					openSet.append(neighbor) 
			else:
				openSet.append(neighbor)

def aStar(map, srcX, srcY, dstX, dstY):
	openSet = []
	closedSet = [] 	
	startNode = Node(map, srcX, srcY, dstX, dstY, None)
	openSet.append(startNode)  
	itr = 0
	while len(openSet) != 0:
		print "on itr %d!" % itr
		itr += 1
		curCandidate = getLowestScoreNode(openSet) 
		if curCandidate.x == dstX and curCandidate.y == dstY:
			print "success!" 
			path = [] 
			curNode = curCandidate
			while curNode.x != srcX and curNode.y != srcY:
				coord = Coord(curNode.x, curNode.y)
				path.append(coord)
				curNode = curNode.prev
			path.reverse() 
			return path 
		openSet.remove(curCandidate) 
		closedSet.append(curCandidate) 
		# add this node's neighbors to the open list
		addNeighbors(curCandidate, openSet, closedSet, map, dstX, dstY)
	print "oh no!"
		

def getHeuristic(srcX, srcY, dstX, dstY):
	# we return the distance via pythag's 
	deltaX = dstX - srcX
	deltaY = dstY - srcY 
	return math.sqrt(deltaX**2 + deltaY**2)  

#TODO: devise unit test
if __name__ == "__main__":
	print "make a unit test!"
