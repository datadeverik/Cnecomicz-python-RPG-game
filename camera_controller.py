import math

import global_constants as gc

class Camera:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.zoom_scale = 1

	def camera_coordinates(self, obj_x, obj_y):
		"""Input: gameworld coordinates.
		Output: on-screen coordinates."""
		return obj_x - self.x + gc.WINDOW_WIDTH//2, obj_y - self.y + gc.WINDOW_HEIGHT//2

	def pan(self, target_x, target_y, speed):
		delta_x = self.x - target_x
		delta_y = self.y - target_y
		if delta_x != 0:
			if target_x > self.x:
				angle_to_target = math.atan(delta_y / delta_x)
			else:
				angle_to_target = math.atan(delta_y / delta_x) + math.pi
		else:
			if target_y > self.y:
				angle_to_target = 3/2 * math.pi
			else:
				angle_to_target = 1/2 * math.pi

		if abs(delta_x) > speed:
			self.x += speed * math.cos(angle_to_target)
		else:
			self.x = target_x
		if abs(delta_y) > speed:
			self.y += speed * math.sin(angle_to_target)
		else:
			self.y = target_y
