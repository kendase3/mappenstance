#! /usr/bin/env python
"""
	an implementation of the a star algorithm

"""

import math

# locals
from cell import Cell

class Node:
	"""
		self-aware x,y wrapper for cells in a-star
	"""
	ROCK_CELL = ' '
	WALL_CELL = 'W'
	ROOM_CELL = '.'
	ROCK_COST = 1
	WALL_COST = 1E5
	ROOM_COST = 1E5
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

	def getCellCost(self):
		if self.cell == Node.ROCK_CELL:
			return Node.ROCK_COST
		elif self.cell == Node.WALL_CELL:
			return Node.WALL_COST
		elif self.cell == Node.ROOM_CELL:
			return Node.ROOM_COST
		else:
			print "oh heavens me!  assume a wall!"
			return Node.WALL_COST 
	
	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True	
		else:
			return False

def getLowestCostNode(lst):
	"""
		precondition: list is not empty
	""" 
	curLowest = lst[0] 	
	for node in lst:
		if node.cost < curLowest.cost:
			curLowest = node
	return curLowest

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
	while len(openSet) != 0:
		curCandidate = getLowestScoreNode(openSet) 
		if curCandidate.x == dstX and curCandidate.y == dstY:
			print "success!" #TODO: print path taken
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

if __name__ == "__main__":
	print "what."
