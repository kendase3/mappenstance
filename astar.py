#! /usr/bin/env python
"""
	an implementation of the a star algorithm

"""

import math

class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def heuristic(src, dst):
	# we return the distance via pythag's 
	deltaX = dst.x - src.x
	deltaY = dst.y - src.y
	return math.sqrt(deltaX**2 + deltaY**2)  

if __name__ == "__main__":
	src = Cell(0, 0)
	dst = Cell(3, 4)
	print heuristic(src, dst)
