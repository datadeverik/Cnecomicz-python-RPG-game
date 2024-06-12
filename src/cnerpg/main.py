import sys

import cnerpg.camera_controller   as cc
import cnerpg.collision_detection as cd
import cnerpg.dialogue_builder    as db
import cnerpg.global_constants    as gc
import cnerpg.turn_manager        as tm
import cnerpg.world_map           as wm

def main():
	global camera, collisiondetector, dialoguemanager, turntracker
	camera = cc.Camera(x=wm.player.x, y=wm.player.y)
	collisiondetector = cd.CollisionDetector(player_object=wm.player, blocks_list=wm.BLOCKS, entities_list=wm.ENTITIES)
	dialoguemanager = db.DialogueManager(player_object=wm.player, entity_object=None)
	turntracker = tm.TurnTracker(player_object=wm.player, list_of_entities=wm.ENTITIES)
	while True:
		gc.DISPLAY_SURF.fill(gc.WHITE)
		wm.player.run()
		for entity in wm.ENTITIES:
			entity.run()
		for event in gc.pygame.event.get():
			if event.type == gc.QUIT:
				quit_game()
			if event.type == gc.KEYDOWN:
				if event.key == gc.K_ESCAPE:
					quit_game()
				if event.key in gc.USE:
					if dialoguemanager.entity_object in wm.ENTITIES:
						dialoguemanager.select_response()
					else:
						potential_conversation_partner = collisiondetector.the_thing_youre_about_to_hit()
						if potential_conversation_partner in wm.ENTITIES:
							dialoguemanager = db.DialogueManager(player_object=wm.player, entity_object=potential_conversation_partner)
					if turntracker.is_actively_tracking:
						if turntracker.current_actor_index == len(turntracker.list_in_turn_order)-1:
								turntracker.current_actor_index = 0
						else:
							turntracker.current_actor_index += 1
						turntracker.current_round_actor = turntracker.list_in_turn_order[turntracker.current_actor_index]
				if event.key in gc.UP:
					if dialoguemanager.entity_object is not None:
						dialoguemanager.textbox.option_index -= 1
					if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
						if turntracker.player_selection_index > 0:
							turntracker.player_selection_index -= 1
						else:
							turntracker.player_selection_index = len(turntracker.player_selection_list)-1
				if event.key in gc.DOWN:
					if dialoguemanager.entity_object is not None:
						dialoguemanager.textbox.option_index += 1
					if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
						if turntracker.player_selection_index < len(turntracker.player_selection_list)-1:
							turntracker.player_selection_index += 1
						else:
							turntracker.player_selection_index = 0
				if event.key in [gc.K_RSHIFT, gc.K_LSHIFT]:
					if not turntracker.is_actively_tracking:
						turntracker.begin_tracking_turns()
					else:
						turntracker.end_tracking_turns()
		if turntracker.is_actively_tracking:
			turntracker.run()
		if dialoguemanager.entity_object in wm.ENTITIES:
			dialoguemanager.run()
		draw_to_screen()
		gc.FPS_CLOCK.tick(gc.FPS)

def quit_game():
	gc.pygame.quit()
	sys.exit()

def draw_to_screen():
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
	if not wm.player.in_dialogue:
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
	if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
		turntracker.player_options_box()
	gc.pygame.display.update()
	
