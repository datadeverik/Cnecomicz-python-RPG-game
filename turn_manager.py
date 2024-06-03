import math
import random

import dice_roller      as dr
import global_constants as gc
import world_map        as wm

class TurnTracker:
	def __init__(self, player_object, list_of_entities):
		self.is_actively_tracking = False
		self.turn_number          = 1
		self.current_round_actor  = None
		self.last_round_actor     = None
		self.current_actor_index  = 0
		self.player_object        = player_object
		self.list_of_entities     = list_of_entities
		self.list_in_turn_order   = [player_object] + list_of_entities

	def begin_tracking_turns(self):
		self.is_actively_tracking = True
		for entity in self.list_in_turn_order:
			entity.can_move = False
			entity.movement_spent_this_turn = 0
			entity.last_known_x = entity.x
			entity.last_known_y = entity.y
		random.shuffle(self.list_of_entities)
		initiative_bool = dr.roll_below(self.player_object.dexterity)
		if initiative_bool:
			self.list_in_turn_order = [self.player_object] + self.list_of_entities
			print(self.list_in_turn_order)
		else:
			self.list_in_turn_order = self.list_of_entities + [self.player_object]
			print(self.list_in_turn_order)
		self.current_actor_index = 0
		self.current_round_actor = self.list_in_turn_order[self.current_actor_index]
		self.last_round_actor = self.list_in_turn_order[self.current_actor_index]

	def start_of_turn(self, entity):
		entity.movement_spent_this_turn = 0
		entity.last_known_x = entity.x
		entity.last_known_y = entity.y

	def end_tracking_turns(self):
		self.is_actively_tracking = False
		for entity in self.list_in_turn_order:
			entity.can_move = True


	def move_allotment(self, entity):
		print(entity.name, entity.movement_spent_this_turn)
		if entity.movement_spent_this_turn == 0:
			entity.can_move = True
		if entity.movement_spent_this_turn >= entity.movement_per_turn:
			entity.can_move = False
			return print("Out of movement.")
		if (entity.x, entity.y) != (entity.last_known_x, entity.last_known_y):
			entity.movement_spent_this_turn += math.dist((entity.x, entity.y), (entity.last_known_x, entity.last_known_y))
			entity.last_known_x = entity.x
			entity.last_known_y = entity.y
		


	def run(self):
		print(self.current_round_actor)
		if self.current_round_actor.name != self.last_round_actor.name:
			self.start_of_turn(self.current_round_actor)
			self.last_round_actor = self.current_round_actor

		self.move_allotment(self.current_round_actor)
		if self.current_round_actor != self.player_object:
			destination_x = self.current_round_actor.behavior.target_location[0]
			destination_y = self.current_round_actor.behavior.target_location[1]
			if self.current_round_actor.total_path == []:
				self.current_round_actor.a_star_pathfind(destination_x, destination_y, wm.BLOCKS)
					







