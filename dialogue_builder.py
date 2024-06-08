import global_constants as gc

def make_text(font, text, color, bgcolor, top, left, textwidth, formatting_dict={}):
	line = 0
	plain_text = text.format(**formatting_dict)
	words = plain_text.split(" ")
	current_line = ""
	for word in words:
		textSurf = font.render(current_line, True, color, bgcolor)
		nextSurf = font.render(current_line + word + " ", True, color, bgcolor)
		if nextSurf.get_width() <= textwidth:
			current_line += word + " "
		else:
			textRect = textSurf.get_rect()
			textRect.topleft = (left, top + line * gc.FONT_SIZE)
			gc.DISPLAY_SURF.blit(textSurf, textRect)
			current_line = "" + word + " "
			line += 1
	# Print the final line.
	textSurf = font.render(current_line, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (left, top + line * gc.FONT_SIZE)
	gc.DISPLAY_SURF.blit(textSurf, textRect)

def keylogger():
	"""Returns the result of the player's keypresses, as a string."""
	user_string = ""
	while True:
		for event in gc.pygame.event.get():
			if event.type == gc.KEYDOWN:
				if event.key == gc.K_RETURN and user_string != "":
					return user_string
				elif event.key == gc.K_BACKSPACE and user_string != "":
					user_string = user_string[:-1]
				elif event.key == gc.K_ESCAPE:
					pass
				else:
					user_string += event.unicode

		make_text(
			font = gc.BASIC_FONT,
			text = "> " + user_string, 
			color = gc.BLACK, 
			bgcolor = gc.WHITE, 
			top = gc.SPEECH_BUBBLE_BOTTOM - 2 * gc.SPEECHBUBBLEMARGIN + gc.FONT_SIZE, 
			left = gc.SPEECH_BUBBLE_LEFT + gc.SPEECHBUBBLEMARGIN,
			textwidth = gc.SPEECH_BUBBLE_WIDTH - 2 * gc.SPEECHBUBBLEMARGIN,
		)
		gc.pygame.display.update()

class Response:
	def __init__(self, text, next_dialogue_index, trigger_list=[], is_end_of_dialogue=False, display_bool=True, formatting_dict={}):
		self.text = text
		self.next_dialogue_index = next_dialogue_index
		self.trigger_list = trigger_list
		self.is_end_of_dialogue = is_end_of_dialogue
		self.display_bool = display_bool
		self.formatting_dict = formatting_dict

class Node:
	def __init__(self, text, responses, formatting_dict={}, is_text_entry_node=False, class_owning_attr=None, attr_to_receive_user_text=None):
		self.text = text
		self.responses = responses
		self.formatting_dict = formatting_dict
		self.is_text_entry_node = is_text_entry_node
		self.class_owning_attr = class_owning_attr
		self.attr_to_receive_user_text = attr_to_receive_user_text

	def assign_user_text_to_variable(self, user_text):
		setattr(self.class_owning_attr, self.attr_to_receive_user_text, user_text)

class TextBox:
	def __init__(
		self, 
		frame_rect, 
		header_rect=None, 
		header_text=None, 
		main_rect=None, 
		main_text=None, 
		main_formatting_dict = {},
		options_rect=None,
		options_dict={},
		option_index=0,
	):
		self.frame_rect              = frame_rect
		self.header_rect             = header_rect
		self.header_text             = header_text
		self.main_rect               = main_rect
		self.main_text               = main_text
		self.main_formatting_dict    = main_formatting_dict
		self.options_rect            = options_rect
		self.options_dict            = options_dict
		self.option_index            = option_index
		self.number_of_valid_options = self.get_number_of_valid_options()

	def get_number_of_valid_options(self):
		value = 0
		for key, response in self.options_dict.items():
			if response.display_bool == True:
				value += 1
		return value

	def run(self):
		gc.pygame.draw.rect(gc.DISPLAY_SURF, gc.BLACK, self.frame_rect, 3)
		if self.header_rect is not None:
			make_text(
				font = gc.BASIC_FONT,
				text = self.header_text,
				color = gc.BLACK,
				bgcolor = gc.WHITE,
				top = self.header_rect.top,
				left = self.header_rect.left,
				textwidth = self.header_rect.width,
			)
		if self.main_rect is not None:
			make_text(
				font = gc.BASIC_FONT,
				text = self.main_text,
				color = gc.BLACK,
				bgcolor = gc.WHITE,
				top = self.main_rect.top,
				left = self.main_rect.left,
				textwidth = self.main_rect.width,
				formatting_dict = self.main_formatting_dict
			)
		if self.options_dict != {}:
			self.generate_options_rect()
			response_index = 0
			for key, response in self.options_dict.items():
				if response.display_bool == True:
					if self.option_index != response_index:
						make_text(
							font = gc.BASIC_FONT,
							text = response.text,
							color = gc.BLACK,
							bgcolor = gc.WHITE,
							top = self.options_rect.top + response_index * gc.FONT_SIZE,
							left = self.options_rect.left,
							textwidth = self.options_rect.width,
						)
					else: 
						make_text(
							font = gc.BASIC_FONT,
							text = "> "+ response.text,
							color = gc.BLACK,
							bgcolor = gc.WHITE,
							top = self.options_rect.top + response_index * gc.FONT_SIZE,
							left = self.options_rect.left,
							textwidth = self.options_rect.width,
						)
						self.option_str = key
					response_index += 1

	def get_option_str(self):
		return 


	def generate_options_rect(self):
		self.options_rect = gc.pygame.Rect(
			self.frame_rect.left + gc.MARGIN,
			self.frame_rect.bottom  - self.number_of_valid_options * gc.FONT_SIZE - 2 * gc.FONT_SIZE, 
			self.frame_rect.width - 2 * gc.MARGIN,
			self.frame_rect.height
		)

class DialogueManager:
	def __init__(self, player_object, entity_object=None):
		self.player_object = player_object
		self.entity_object = entity_object
		self.textbox       = None


	def end_dialogue(self):   
		print(f"print 2: {self.entity_object}")
		self.player_object.in_dialogue = False
		self.entity_object.in_dialogue = False
		self.entity_object             = None

	def select_response(self):
		selected = self.entity_object.dialogue_dict[self.entity_object.current_dialogue_node].responses[self.textbox.option_str]
		if selected.trigger_list != []:
			for trigger in selected.trigger_list:
				print(f"print 1: {self.entity_object}")
				trigger()
		self.entity_object.current_dialogue_node = selected.next_dialogue_index
		self.textbox = None
		self.update_textbox()
		if selected.is_end_of_dialogue:
			self.end_dialogue()

	def update_textbox(self):
		node = self.entity_object.dialogue_dict[self.entity_object.current_dialogue_node]
		if node.is_text_entry_node and self.textbox is None:
			# self.textbox = TextBox(
			# 
			# )
			pass
		elif not node.is_text_entry_node and self.textbox is None:
			self.textbox = TextBox(
				frame_rect=gc.SPEECH_BUBBLE_FRAME_RECT, 
				header_rect=gc.SPEECH_BUBBLE_HEADER_RECT, 
				header_text=self.entity_object.name + ":", 
				main_rect=gc.SPEECH_BUBBLE_MAIN_RECT, 
				main_text=node.text, 
				options_dict=node.responses,
				main_formatting_dict=node.formatting_dict
			)

	def run(self):
		self.player_object.in_dialogue = True
		self.entity_object.in_dialogue = True
		self.update_textbox()
		if self.textbox.options_dict != {}:
			if self.textbox.option_index < 0:
				self.textbox.option_index = self.textbox.number_of_valid_options-1
			elif self.textbox.option_index > self.textbox.number_of_valid_options-1:
				self.textbox.option_index = 0
		self.textbox.run()



			