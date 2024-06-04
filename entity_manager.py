import math

import dialogue_builder as db
import global_constants as gc
		

class Behavior:
	def __init__(self):
		pass


class Entity:
	def __init__(self, name, x, y, width, height, dialogue_dict, speed, behavior):
		self.name                     = name
		self.x                        = x
		self.y                        = y
		self.width                    = width
		self.height                   = height
		self.rect                     = gc.pygame.Rect(self.x, self.y, self.width, self.height)
		self.dialogue_dict            = dialogue_dict
		self.current_dialogue_node    = 0
		self.in_dialogue              = False
		self.current_response_index   = 0
		self.current_response_str     = ""
		self.destination_x            = x
		self.destination_y            = y
		self.speed                    = speed
		self.total_path               = []
		self.can_move                 = True
		self.movement_per_turn        = gc.DEFAULT_MOVEMENT_PER_TURN
		self.movement_spent_this_turn = 0
		self.behavior                 = behavior

	def a_star_pathfind(self, target_x, target_y, obstacles):
		start_x = 10 * math.floor(self.x / 10)
		start_y = 10 * math.floor(self.y / 10)
		start_node = (start_x, start_y)
		goal_x  = 10 * math.floor(target_x / 10)
		goal_y  = 10 * math.floor(target_y / 10)
		goal_node = (goal_x, goal_y)

		seen_nodes_set = set() # A set of nodes you have already seen.
		seen_nodes_set.add(start_node)
		unchecked_node_set = set() # A set of nodes yet to be checked.
		unchecked_node_set.add(start_node)
		came_from_dictionary = { } # A dictionary where key: value is "node: cheapest backtrack node."
		cost_dictionary = { } # A dictionary where key: value is "node: cost to reach that node from start_node."
		cost_dictionary[start_node] = 0
		def objective_function(node):
			return cost_dictionary[node] + math.dist(node, goal_node)
		objective_dictionary = { } # A dictionary where key: value is "node: objective_function(node)."
		objective_dictionary[start_node] = objective_function(start_node)
		current_node = start_node
		while unchecked_node_set != set():
			minimal_objective = math.inf
			for node in unchecked_node_set:
				if objective_function(node) < minimal_objective:
					current_node = node
					minimal_objective = objective_function(node)
			if current_node == goal_node:
				return self.reconstruct_path(came_from_dictionary, current_node)

			unchecked_node_set.remove(current_node)
			neighbors = { 
				(current_node[0] - 10, current_node[1] - 10),
				(current_node[0]     , current_node[1] - 10),
				(current_node[0] + 10, current_node[1] - 10),
				(current_node[0] - 10, current_node[1]     ),
			#   (current_node[0]     , current_node[1]     ),	
				(current_node[0] + 10, current_node[1]     ),
				(current_node[0] - 10, current_node[1] + 10),
				(current_node[0]     , current_node[1] + 10),
				(current_node[0] + 10, current_node[1] + 10),
			}
			neighbors_to_be_removed = set()
			for neighbor in neighbors:
				neighbor_rect = gc.pygame.Rect(neighbor[0], neighbor[1], self.width, self.height)
				for obstacle in obstacles:
					if obstacle.colliderect(neighbor_rect) and obstacle != self.rect:
						neighbors_to_be_removed.add(neighbor)
			neighbors -= neighbors_to_be_removed
			for neighbor in neighbors:
				if neighbor not in seen_nodes_set:
					cost_dictionary[neighbor] = math.inf
					seen_nodes_set.add(neighbor)
			for neighbor in neighbors:
				tentative_cost = cost_dictionary[current_node] + math.dist(current_node, neighbor)
				if tentative_cost < cost_dictionary[neighbor]:
					came_from_dictionary[neighbor] = current_node
					cost_dictionary[neighbor] = tentative_cost
					objective_dictionary[neighbor] = objective_function(neighbor)
					if neighbor not in unchecked_node_set:
						unchecked_node_set.add(neighbor)

		print("Failure to pathfind.")


	def reconstruct_path(self, came_from_dictionary, current_node):
		total_path = [ ] # A list listing the nodes in the path in order from start to finish.
		total_path.insert(0, current_node)
		while current_node in came_from_dictionary.keys():
			current_node = came_from_dictionary[current_node]
			total_path.insert(0, current_node)
		self.total_path = total_path
		

	def write_dialogue_in_speech_bubble(self):
		node = self.dialogue_dict[self.current_dialogue_node]
		dialogue = db.DialogueBox(
			frame_rect=gc.SPEECH_BUBBLE_FRAME_RECT, 
			header_rect=gc.SPEECH_BUBBLE_HEADER_RECT, 
			header_text=self.name + ":", 
			main_rect=gc.SPEECH_BUBBLE_MAIN_RECT, 
			main_text=node.text, 
			options_dict=node.responses
		)
		dialogue.run()



	# def write_dialogue_in_speech_bubble(self):
	# 	speech_bubble_rect = gc.pygame.Rect(gc.SPEECH_BUBBLE_LEFT, gc.SPEECH_BUBBLE_TOP, gc.SPEECH_BUBBLE_WIDTH, gc.SPEECH_BUBBLE_HEIGHT)
	# 	gc.pygame.draw.rect(gc.DISPLAY_SURF, gc.BLACK, speech_bubble_rect, 3)
	# 	node = self.dialogue_dict[self.current_dialogue_node]
	# 	db.make_text(
	# 		font = gc.BASIC_FONT,
	# 		text = self.name + ":",
	# 		color = gc.BLACK,
	# 		bgcolor = gc.WHITE,
	# 		top = gc.SPEECH_BUBBLE_TOP + gc.MARGIN,
	# 		left = gc.SPEECH_BUBBLE_LEFT + gc.MARGIN,
	# 		textwidth = gc.SPEECH_BUBBLE_WIDTH - 2 * gc.MARGIN,
	# 	)
	# 	db.make_text(
	# 		font = gc.BASIC_FONT,
	# 		text = node.text, 
	# 		color = gc.BLACK, 
	# 		bgcolor = gc.WHITE, 
	# 		top = gc.SPEECH_BUBBLE_TOP + gc.MARGIN + gc.FONT_SIZE,
	# 		left = gc.SPEECH_BUBBLE_LEFT + gc.MARGIN, 
	# 		textwidth = gc.SPEECH_BUBBLE_WIDTH - 2 * gc.MARGIN,
	# 		formatting_dict = node.formatting_dict
	# 	)
	# 	response_index = 0
	# 	number_of_valid_options = 0

	# 	if not node.is_text_entry_node:
	# 		for i, response in node.responses.items():
	# 			if response.display_bool == True:
	# 				number_of_valid_options += 1
	# 		for i, response in node.responses.items():
	# 			if response.display_bool == True:
	# 				if self.current_response_index != response_index:
	# 					db.make_text(
	# 						font = gc.BASIC_FONT,
	# 						text = node.responses[i].text, 
	# 						color = gc.BLACK, 
	# 						bgcolor = gc.WHITE, 
	# 						top = gc.SPEECH_BUBBLE_BOTTOM - gc.MARGIN + (response_index - number_of_valid_options) * gc.FONT_SIZE, 
	# 						left = gc.SPEECH_BUBBLE_LEFT + gc.MARGIN,
	# 						textwidth = gc.SPEECH_BUBBLE_WIDTH - 2 * gc.MARGIN,
	# 						formatting_dict = node.responses[i].formatting_dict
	# 					)
	# 				else:
	# 					db.make_text(
	# 						font = gc.BASIC_FONT,
	# 						text = "> " + node.responses[i].text, 
	# 						color = gc.BLACK, 
	# 						bgcolor = gc.WHITE, 
	# 						top = gc.SPEECH_BUBBLE_BOTTOM - gc.MARGIN + (response_index - number_of_valid_options) * gc.FONT_SIZE, 
	# 						left = gc.SPEECH_BUBBLE_LEFT + gc.MARGIN,
	# 						textwidth = gc.SPEECH_BUBBLE_WIDTH - 2 * gc.MARGIN,
	# 						formatting_dict = node.responses[i].formatting_dict
	# 					)
	# 					self.current_response_str = i
	# 				response_index += 1
	# 				if self.current_response_index < 0:
	# 					self.current_response_index = number_of_valid_options - 1
	# 				if self.current_response_index > number_of_valid_options - 1:
	# 					self.current_response_index = 0
	# 	else:
	# 		node.assign_user_text_to_variable(db.keylogger())
	# 		self.current_response_str = "A"
	# 		self.select_response()

	def select_response(self):
		selected = self.dialogue_dict[self.current_dialogue_node].responses[self.current_response_str]
		if selected.trigger_list != []:
			for trigger in selected.trigger_list:
				trigger()
		self.current_dialogue_node = selected.next_dialogue_index

		self.current_response_index = 0
		self.current_response_str   = ""
		



	def stop_talking(self):
		self.in_dialogue = False


	def run(self):
		self.rect = gc.pygame.Rect(self.x, self.y, self.width, self.height)
		if self.total_path != []:
			path_node_rect = gc.pygame.Rect(
				self.total_path[0][0] - self.speed / 2,
				self.total_path[0][1] - self.speed / 2,
				self.speed,
				self.speed
			)
			if path_node_rect.collidepoint(self.x, self.y):
				self.total_path.pop(0)
			else:
				self.destination_x = self.total_path[0][0]
				self.destination_y = self.total_path[0][1]
		destination_rect = gc.pygame.Rect(
			self.destination_x - self.speed / 2, 
			self.destination_y - self.speed / 2, 
			self.speed, 
			self.speed
		)
		if not destination_rect.collidepoint(self.x, self.y):
			delta_x = self.x - self.destination_x
			delta_y = self.y - self.destination_y
			if delta_x != 0:
				if self.destination_x < self.x:
					angle_to_target = math.atan(delta_y / delta_x)
				else:
					angle_to_target = math.atan(delta_y / delta_x) + math.pi
			elif delta_y != 0:
				if self.destination_y > self.y:
					angle_to_target = 3/2 * math.pi
				else:
					angle_to_target = 1/2 * math.pi
			if self.can_move:
				self.x -= self.speed * math.cos(angle_to_target)
				self.y -= self.speed * math.sin(angle_to_target)






		
