
class Room:
	def __init__(self, id, x, y, width, height):
		self.id = id
		self.x = x 
		self.y = y 
		self.width = width 
		self.height = height 
	
	def __repr__(self):
		return "Room: id=%d, x=%d, y=%d, width=%d, height=%d" % (
				self.id, self.x, self.y, self.width, self.height) 
