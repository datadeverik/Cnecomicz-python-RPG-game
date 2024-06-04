import math

import global_constants as gc
import world_map        as wm

class Player:
	def __init__(self, x, y):
		self.x                        = x
		self.y                        = y
		self.width                    = 30
		self.height                   = 30
		self.rect                     = gc.pygame.Rect(self.x, self.y, self.width, self.height)
		self.speed                    = 5
		self.angle                    = 0
		self.can_move                 = True
		self.in_dialogue              = False

		self.name                     = ""
		self.character_class          = ""
		self.charisma                 = 0
		self.constitution             = 0
		self.dexterity                = 0
		self.intelligence             = 0
		self.strength                 = 0
		self.wisdom                   = 0
		self.max_hp                   = 0
		self.current_hp               = 0
		self.level                    = 0
		self.ac                       = 0
		self.av                       = 0
		self.gold_on_person           = 0
		self.gold_spent_this_level    = 0
		self.inventory                = [ ]
		self.equipment                = { }
		self.movement_per_turn        = gc.DEFAULT_MOVEMENT_PER_TURN
		self.movement_spent_this_turn = 0
		self.last_known_x             = x
		self.last_known_y             = y

	def assign_value_to_variable(self, value, variable):
		variable = value


	def get_direction(self):
		direction = ""
		keys = gc.pygame.key.get_pressed()
		for key in gc.UP:
			if keys[key]:
				direction += "up"
				break
		for key in gc.DOWN:
			if keys[key]:
				direction += "down"
				break
		for key in gc.LEFT:
			if keys[key]:
				direction += "left"
				break
		for key in gc.RIGHT:
			if keys[key]:
				direction += "right"
				break	
		match direction:
			case "upleft": 
				self.angle = 3/4 * math.pi
			case "upright": 
				self.angle = 1/4 * math.pi
			case "downleft": 
				self.angle = 5/4 * math.pi
			case "downright": 
				self.angle = 7/4 * math.pi
			case "up":
				self.angle = 1/2 * math.pi
			case "down":
				self.angle = 3/2 * math.pi
			case "left":
				self.angle = math.pi
			case "right":
				self.angle = 2 * math.pi
		return direction

	def the_thing_youre_about_to_hit(self, angle, x, y, speed):
		result = None
		future_x, future_y = self.next_destination(angle, x, y, speed)
		future_rect = gc.pygame.Rect(future_x, future_y, self.height, self.width)
		for block in wm.BLOCKS:
			if gc.pygame.Rect.colliderect(future_rect, block):
				result = block
		return result
				

	def next_destination(self, angle, x, y, speed):
		return x + speed * math.cos(angle), y - speed * math.sin(angle)

	def player_movement(self):
		if self.get_direction() != "" and self.can_move:
			block = self.the_thing_youre_about_to_hit(self.angle, self.x, self.y, self.speed) 
			if block is None:
				self.x, self.y = self.next_destination(self.angle, self.x, self.y, self.speed)
			else:
				detect_left  = self.the_thing_youre_about_to_hit(math.pi, self.x, self.y, self.speed) 
				detect_right = self.the_thing_youre_about_to_hit(0, self.x, self.y, self.speed) 
				detect_up    = self.the_thing_youre_about_to_hit(1/2 * math.pi, self.x, self.y, self.speed) 
				detect_down  = self.the_thing_youre_about_to_hit(3/2 * math.pi, self.x, self.y, self.speed) 
				match self.get_direction():
					case "upleft":
						if detect_up is None:
							self.y -= self.speed
						elif detect_left is None:
							self.x -= self.speed
					case "upright":
						if detect_up is None:
							self.y -= self.speed
						elif detect_right is None:
							self.x += self.speed
					case "downleft":
						if detect_down is None:
							self.y += self.speed
						elif detect_left is None:
							self.x -= self.speed
					case "downright":
						if detect_down is None:
							self.y += self.speed
						elif detect_right is None:
							self.x += self.speed
		return self.x, self.y

	def talk(self):
		pointing_x, pointing_y = self.next_destination(self.angle, self.x, self.y, self.speed)
		pointing_rect = gc.pygame.Rect(pointing_x, pointing_y, self.height, self.width)
		for entity in wm.ENTITIES:
			if gc.pygame.Rect.colliderect(pointing_rect, entity) and not self.in_dialogue:
				self.in_dialogue   = True
				entity.in_dialogue = True

	def update_dialogue_bool(self):
		self.in_dialogue = False
		for entity in wm.ENTITIES:
			if entity.in_dialogue:
				self.in_dialogue = True
				self.can_move    = False




	def run(self):
		self.player_movement()
		self.update_dialogue_bool()
