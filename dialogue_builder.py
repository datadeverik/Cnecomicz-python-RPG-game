import global_constants as gc

class Response:
	def __init__(self, text, next_dialogue_index, trigger_list=[], display_bool=True, formatting_dict={}):
		self.text = text
		self.next_dialogue_index = next_dialogue_index
		self.trigger_list = trigger_list
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
			textRect.topleft = (left, top + line * gc.FONTSIZE)
			gc.DISPLAYSURF.blit(textSurf, textRect)
			current_line = "" + word + " "
			line += 1
	# Print the final line.
	textSurf = font.render(current_line, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (left, top + line * gc.FONTSIZE)
	gc.DISPLAYSURF.blit(textSurf, textRect)

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
			font = gc.BASICFONT,
			text = "> " + user_string, 
			color = gc.BLACK, 
			bgcolor = gc.WHITE, 
			top = gc.SPEECHBUBBLEBOTTOM - 2 * gc.SPEECHBUBBLEMARGIN + gc.FONTSIZE, 
			left = gc.SPEECHBUBBLELEFT + gc.SPEECHBUBBLEMARGIN,
			textwidth = gc.SPEECHBUBBLEWIDTH - 2 * gc.SPEECHBUBBLEMARGIN,
		)
		gc.pygame.display.update()

	