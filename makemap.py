#! /usr/bin/env python 

import sys

WIDTH = 10
HEIGHT = 10

class Cell:
	def __init__(self):
		self.ascii = '~'

cells = [[Cell() for j in range(WIDTH)] 
			for i in range(HEIGHT)]

for row in cells:
	for cell in row:
		sys.stdout.write(cell.ascii) 
	print
