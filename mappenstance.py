#! /usr/bin/env python 

import sys
import random

# locals
from cell import Cell
from room import Room
from mapp import Mapp
from astar import aStar
from coord import Coord
from roomer import Roomer


if __name__=="__main__":
	map = Mapp() 
	roomer = Roomer()
	roomer.addRooms(map) 
	map.prnt()
	#pather = Pather() 	
	#path = aStar(map.cells, 0, 0, 1, 1)
	#print path
