import random

class Behavior:
	def __init__(self, target_location):
		self.target_location = target_location
		# also will need action AI


randommovement = Behavior(target_location = (random.randint(-1000,1000), random.randint(-1000,1000)))