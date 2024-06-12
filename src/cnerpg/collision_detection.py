import math

import cnerpg.global_constants as gc

class CollisionDetector:
	def __init__(self, player_object, blocks_list, entities_list):
		self.player_object = player_object
		self.blocks_list   = blocks_list
		self.entities_list = entities_list

	def next_destination(self):
		return self.player_object.x + self.player_object.speed * math.cos(self.player_object.angle), self.player_object.y - self.player_object.speed * math.sin(self.player_object.angle)

	def the_thing_youre_about_to_hit(self):
		result = None
		future_x, future_y = self.next_destination()
		future_rect = gc.pygame.Rect(future_x, future_y, self.player_object.height, self.player_object.width)
		for thing in self.blocks_list + self.entities_list:
			if gc.pygame.Rect.colliderect(future_rect, thing):
				return thing