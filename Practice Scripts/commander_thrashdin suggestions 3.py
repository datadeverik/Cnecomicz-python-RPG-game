import pygame
import math
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()

    
class Player:
    direction_mapping = {
        Direction.UP: [pygame.K_w, pygame.K_UP],
        Direction.DOWN: [pygame.K_s, pygame.K_DOWN],
        Direction.LEFT: [pygame.K_a, pygame.K_LEFT],
        Direction.RIGHT: [pygame.K_d, pygame.K_RIGHT]
    }

    angle_mapping = {
        frozenset({Direction.UP, Direction.LEFT}): 3/4 * math.pi,
        frozenset({Direction.UP, Direction.RIGHT}): 1/4 * math.pi,
        frozenset({Direction.DOWN, Direction.LEFT}): 5/4 * math.pi,
        frozenset({Direction.DOWN, Direction.RIGHT}): 7/4 * math.pi,
        frozenset({Direction.UP}): 1/2 * math.pi,
        frozenset({Direction.DOWN}): 3/2 * math.pi,
        frozenset({Direction.LEFT}): math.pi,
        frozenset({Direction.RIGHT}): 0  # same as 2 * math.pi btw
    }

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5
        self.angle = 0
        self.can_move = True
        self.in_dialogue = False

    def get_direction(self):
        keys = pygame.key.get_pressed()
        direction = set()

        for dir_enum, key_list in self.direction_mapping.items():
            if any(keys[key] for key in key_list):
                direction.add(dir_enum)

        self.angle = self.angle_mapping.get(frozenset(direction), self.angle)
        
        return direction


