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
from pather import Pather
from populator import Populator 

if __name__=="__main__":
	map = Mapp() 
	roomer = Roomer()
	roomer.addRooms(map) 
	map.prnt()
	pather = Pather() 	
	pather.addPaths(map)
	print "\n\n"
	map.prnt()
	populator = Populator()
	populator.addStairs(map, 4, 4) 	
	map.prnt()
