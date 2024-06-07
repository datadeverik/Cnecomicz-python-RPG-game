import world_map as wm

class PlayerCollisionDetector:
	def __init__(self, player_object):
		self.player_object = player_object

	def next_destination(self):
		return self.player_object.x + self.player_object.speed * math.cos(self.player_object.angle), self.player_object.y - self.player_object.speed * math.sin(self.player_object.angle)

	def the_thing_youre_about_to_hit(self):
		result = None
		future_x, future_y = self.next_destination()
		future_rect = gc.pygame.Rect(future_x, future_y, self.player_object.height, self.player_object.width)
		for thing in wm.BLOCKS + wm.ENTITIES:
			if gc.pygame.Rect.colliderect(future_rect, block):
				result = thing
		return result