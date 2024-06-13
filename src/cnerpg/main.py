import pygame
import sys


import cnerpg.camera_controller   as cc
import cnerpg.collision_detection as cd
import cnerpg.dialogue_builder    as db
import cnerpg.global_constants    as gc
import cnerpg.player_character    as pc
import cnerpg.turn_manager        as tm
import cnerpg.world_map           as wm

pygame.init()  # moved from global constants because it's not a constant

clock = pygame.time.Clock()  # also moved from global constants

# may not need this
# DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
# as we can access .display from pygame

def terminate():
	pygame.quit()
	sys.exit()

# design uncertainty: how to handle the difference between
# events that happen in response to a keydown, like selections in dialogue
# and things that continue on key hold, like movement

class Game:
	def __init__(self):
		self.player            = pc.Player(x=0, y=0)
		self.entities_list     = wm.ENTITIES
		self.blocks_list       = wm.BLOCKS
		self.camera            = cc.Camera(x=self.player_object.x, y=self.player_object.y)
		self.collisiondetector = cd.CollisionDetector(player_object=self.player_object, blocks_list=self.blocks_list, entities_list=self.entities_list)
		self.dialoguemanager   = db.DialogueManager(player_object=self.player_object, entity_object=None)
		self.turntracker       = tm.TurnTracker(player_object=self.player_object, list_of_entities=self.entities_list)
		self.state             = "Overworld" # "Dialogue", "In combat", ...

	def run(self):
		self.handle_events()
		self.update()
		self.draw()
		pygame.display.update()
		clock.tick(gc.FPS)



	def handle_events(self):
		for event in gc.pygame.event.get():
			if event.type == gc.QUIT:
				terminate()
			if event.type == gc.KEYDOWN:
				if event.key == gc.K_ESCAPE:
					terminate()
				if event.key in gc.USE:
					if self.state == "Overworld":
						self.state = "Dialogue"
					elif self.state == "Dialogue":  # other conditions needed?
						self.state = "Overworld"
			

	def update(self):
		if self.state == "Overworld":
			self.player.player_movement(self.blocks_list)
		elif self.state == "Dialogue":

			# this area needs help
			dialoguemanager.run()
			potential_conversation_partner = self.collisiondetector.the_thing_youre_about_to_hit()
			if potential_conversation_partner in wm.ENTITIES:
				dialoguemanager = db.DialogueManager(player_object=wm.player, entity_object=potential_conversation_partner)
			dialoguemanager.select_response()
	

	def draw(self):
		camera = self.camera
		gc.DISPLAY_SURF.fill(gc.WHITE)
		cam_player_x, cam_player_y = camera.camera_coordinates(wm.player.x, wm.player.y)
		gc.pygame.draw.rect(gc.DISPLAY_SURF, gc.BLUE, gc.pygame.Rect(cam_player_x, cam_player_y, wm.player.width, wm.player.height), 0)
		for block in wm.BLOCKS:
			cam_block_x, cam_block_y = camera.camera_coordinates(block.left, block.top)
			cam_block_rect = gc.pygame.Rect(cam_block_x, cam_block_y, block.width, block.height)
			gc.pygame.draw.rect(gc.DISPLAY_SURF, gc.BLACK, cam_block_rect, 0)
		for entity in wm.ENTITIES:
			cam_entity_x, cam_entity_y = camera.camera_coordinates(entity.rect.left, entity.rect.top)
			cam_entity_rect = gc.pygame.Rect(cam_entity_x, cam_entity_y, entity.width, entity.height)
			gc.pygame.draw.rect(gc.DISPLAY_SURF, gc.GREEN, cam_entity_rect, 0)
		if self.state is not "Dialogue":
			camera.pan(
				wm.player.x,
				wm.player.y,
				220
			)
		else:
			camera.pan(
				wm.player.x + 2/5 * gc.WINDOW_WIDTH,
				wm.player.y - 2/5 * gc.WINDOW_HEIGHT,
				220
			)
		# if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
		# 	turntracker.player_options_box()
		# gc.pygame.display.update()


	


# game = Game(blah, blah, blah)

# while True:
# 	event = game.handle_events()
# 	game.update(event)
# 	game.draw()

# def main():
# 	while True:
		
		
		# for entity in wm.ENTITIES:
		# 	entity.run()
		# for event in gc.pygame.event.get():
			# if event.type == gc.QUIT:
			# 	quit_game()
			# if event.type == gc.KEYDOWN:
				# if event.key == gc.K_ESCAPE:
					# quit_game()
				# if event.key in gc.USE:
					# if dialoguemanager.entity_object in wm.ENTITIES:
						# dialoguemanager.select_response()
					# else:
						# potential_conversation_partner = collisiondetector.the_thing_youre_about_to_hit()
						# if potential_conversation_partner in wm.ENTITIES:
						# 	dialoguemanager = db.DialogueManager(player_object=wm.player, entity_object=potential_conversation_partner)
					
					# not attempting to include turntracker at this stage
		# 			if turntracker.is_actively_tracking:
		# 				if turntracker.current_actor_index == len(turntracker.list_in_turn_order)-1:
		# 						turntracker.current_actor_index = 0
		# 				else:
		# 					turntracker.current_actor_index += 1
		# 				turntracker.current_round_actor = turntracker.list_in_turn_order[turntracker.current_actor_index]
		# 		if event.key in gc.UP:
		# 			if dialoguemanager.entity_object is not None:
		# 				dialoguemanager.textbox.option_index -= 1
		# 			if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
		# 				if turntracker.player_selection_index > 0:
		# 					turntracker.player_selection_index -= 1
		# 				else:
		# 					turntracker.player_selection_index = len(turntracker.player_selection_list)-1
		# 		if event.key in gc.DOWN:
		# 			if dialoguemanager.entity_object is not None:
		# 				dialoguemanager.textbox.option_index += 1
		# 			if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
		# 				if turntracker.player_selection_index < len(turntracker.player_selection_list)-1:
		# 					turntracker.player_selection_index += 1
		# 				else:
		# 					turntracker.player_selection_index = 0
		# 		if event.key in [gc.K_RSHIFT, gc.K_LSHIFT]:
		# 			if not turntracker.is_actively_tracking:
		# 				turntracker.begin_tracking_turns()
		# 			else:
		# 				turntracker.end_tracking_turns()
		# if turntracker.is_actively_tracking:
		# 	turntracker.run()
		# if dialoguemanager.entity_object in wm.ENTITIES:
			
		# draw_to_screen()
		# gc.FPS_CLOCK.tick(gc.FPS)

# def quit_game():
# 	gc.pygame.quit()
# 	sys.exit()


	
