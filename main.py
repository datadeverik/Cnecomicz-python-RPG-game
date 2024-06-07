import sys

import camera_controller   as cc
import collision_detection as cd
import dialogue_builder    as db
import global_constants    as gc
import turn_manager        as tm
import world_map           as wm




camera = cc.Camera(x=wm.player.x, y=wm.player.y)
turntracker = tm.TurnTracker(player_object=wm.player, list_of_entities=wm.ENTITIES)

def quit_game():
	gc.pygame.quit()
	sys.exit()

def draw_to_screen():
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
		for entity in wm.ENTITIES:
			if entity.in_dialogue:
				entity.write_dialogue_in_speech_bubble()
	if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
		turntracker.player_options_box()
	gc.pygame.display.update()

def refresh_formatting_dict_in_dialogue_nodes():
	# By hand, we will need to write every "formatting" value 
	# for any node whose formatting is not the empty dictionary
	# into this function.
	wm.character_creator_node_1.formatting_dict = {
		"charisma" : wm.player.charisma, 
		"constitution" : wm.player.constitution,
		"dexterity" : wm.player.dexterity,
		"intelligence" : wm.player.intelligence,
		"strength" : wm.player.strength,
		"wisdom" : wm.player.wisdom
	}
	wm.character_creator_node_2.formatting_dict = {
		"character_class" : wm.player.character_class
	}
	wm.character_creator_node_3.formatting_dict = {
		"name" : wm.player.name
	}

while True:
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
				dialoguemanager = db.DialogueManager(player_object=wm.player, entity_object=None)
				if dialoguemanager.entity_object is not None:
					dialoguemanager.run()
				# if not wm.player.in_dialogue:
				# 	wm.player.talk()
				# else:
				# 	for entity in wm.ENTITIES:
				# 		if entity.in_dialogue:
				# 			entity.select_response()
				if turntracker.is_actively_tracking:
					if turntracker.current_actor_index == len(turntracker.list_in_turn_order)-1:
							turntracker.current_actor_index = 0
					else:
						turntracker.current_actor_index += 1
					turntracker.current_round_actor = turntracker.list_in_turn_order[turntracker.current_actor_index]
			if event.key in gc.UP:
				# for entity in wm.ENTITIES:
				# 	if entity.in_dialogue:
				# 		entity.current_response_index -= 1
				if turntracker.is_actively_tracking and turntracker.current_round_actor is turntracker.player_object:
					if turntracker.player_selection_index > 0:
						turntracker.player_selection_index -= 1
					else:
						turntracker.player_selection_index = len(turntracker.player_selection_list)-1
			if event.key in gc.DOWN:
				# for entity in wm.ENTITIES:
				# 	if entity.in_dialogue:
				# 		entity.current_response_index += 1
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
	refresh_formatting_dict_in_dialogue_nodes()
	draw_to_screen()
	gc.FPS_CLOCK.tick(gc.FPS)