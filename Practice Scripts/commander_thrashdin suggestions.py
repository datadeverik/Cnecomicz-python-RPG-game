from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, event, player, wm):
        if self._next_handler:
            return self._next_handler.handle(event, player, wm)
        return None

      
# you probably have this      
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

class GenericHandler(Handler):
    def __init__(self, condition, action):
        super().__init__()
        self.condition = condition
        self.action = action

    def handle(self, event, player, wm):
        if self.condition(event):
            self.action(event, player, wm)
            return True
        return super().handle(event, player, wm)

      
      
def is_quit_event(event):
    return event.type == QUIT

def quit_action(event, player, wm):
    quit_game()

def is_escape_event(event):
    return event.type == KEYDOWN and event.key == K_ESCAPE

def is_use_event(event):
    return event.type == KEYDOWN and event.key in gc.USE

def use_action(event, player, wm):
    if not player.in_dialogue:
        player.talk()
    else:
        for entity in wm.ENTITIES:
            if entity.in_dialogue:
                entity.select_response()

def is_direction_event(direction_keys):
    return lambda event: event.type == KEYDOWN and event.key in direction_keys

def move_response_action(delta):
    def action(event, player, wm):
        for entity in wm.ENTITIES:
            if entity.in_dialogue:
                entity.current_response_index += delta
    return action

  
  
# This is an actual setup
quit_handler = GenericHandler(is_quit_event, quit_action)
escape_handler = GenericHandler(is_escape_event, quit_action)
use_handler = GenericHandler(is_use_event, use_action)
up_handler = GenericHandler(is_direction_event(gc.UP), move_response_action(-1))
down_handler = GenericHandler(is_direction_event(gc.DOWN), move_response_action(1))

quit_handler.set_next(escape_handler).set_next(use_handler).set_next(up_handler).set_next(down_handler)

# Here is your event loop
while True:
    player.run()
    for event in pygame.event.get():
        quit_handler.handle(event, player, wm)
    draw_to_screen()
    gc.FPSCLOCK.tick(gc.FPS)

  
  
  