import pygame, sys, random, math

from pygame.locals import *

pygame.init()

FPS = 30
FPSCLOCK = pygame.time.Clock()
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
RED =   (255,   0,   0)
GREEN = (  0, 255,   0)

score = 0

class ball:
	def __init__(self, color, x, y, radius, speed, angle):
		self.color  = color
		self.x      = x
		self.y      = y
		self.radius = radius
		self.speed  = speed
		self.angle  = angle

	def move(self, angle, x, y, speed):
		return (self.x + self.speed * math.cos(self.angle), self.y - self.speed * math.sin(self.angle))

	def bounce(self, angle, x, y, speed):
		if 0 < self.x < WINDOWWIDTH and 0 < self.y < WINDOWHEIGHT:
			(self.x,self.y) = self.move(self.angle,self.x,self.y,self.speed)
		elif self.y < 0 or self.y > WINDOWHEIGHT: # Top or bottom of screen
			self.angle = -self.angle
			(self.x,self.y) = self.move(self.angle,self.x,self.y,self.speed)
		elif self.x < 0 or self.x > WINDOWWIDTH: # Left or right of screen
			self.angle = math.pi - self.angle
			(self.x,self.y) = self.move(self.angle,self.x,self.y,self.speed)
		else:
			self.angle = 2*math.pi*random.random()
			(self.x,self.y) = (200,500)
		return (self.angle, self.x, self.y)

	def player_movement(self, x, y):
		keys = pygame.key.get_pressed()
		if keys[K_w] and keys[K_a]: 
			self.angle = 3/4 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] > 0\
			and self.move(self.angle, self.x, self.y, self.speed)[1] > 0:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_w] and keys[K_d]: 
			self.angle = 1/4 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] < WINDOWWIDTH\
			and self.move(self.angle, self.x, self.y, self.speed)[1] > 0:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_s] and keys[K_a]: 
			self.angle = 5/4 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] > 0\
			and self.move(self.angle, self.x, self.y, self.speed)[1] < WINDOWHEIGHT:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_s] and keys[K_d]: 
			self.angle = 7/4 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] < WINDOWWIDTH\
			and self.move(self.angle, self.x, self.y, self.speed)[1] < WINDOWHEIGHT:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_w]:
			self.angle = 1/2 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[1] > 0:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_s]:
			self.angle = 3/2 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[1] < WINDOWHEIGHT:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_a]:
			self.angle = math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] > 0:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		elif keys[K_d]:
			self.angle = 2 * math.pi
			if self.move(self.angle, self.x, self.y, self.speed)[0] < WINDOWWIDTH:
				(self.x,self.y) = self.move(self.angle, self.x, self.y, self.speed)
		return (self.x, self.y)

blue_radius  = 20
red_radius   = 20
green_radius = 20

blue_x  = 100
blue_y  = 200
red_x   = 200
red_y   = 500
green_x = 600
green_y = 100

blue_speed  = 10
red_speed   = 10
green_speed =  5

red_angle = 2*math.pi*random.random()
green_angle = 2*math.pi*random.random()

def quit_game():
	pygame.quit()
	sys.exit()

def make_text(text, color, bgcolor, top, left):
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)

def collision_check(x1, x2, y1, y2, r1, r2) -> bool:
	return math.sqrt( (x1 - x2)**2 + (y1 - y2)**2 ) < r1 + r2

pygame.display.set_caption("Hello world")

redballs = [ball(RED, 200, 500, 20, 10, 2*math.pi*random.random())]
greenballs = [ball(GREEN, 600, 100, 20, 10, 2*math.pi*random.random())]
blueball = ball(BLUE, 100, 200, 20, 10, 0)

balls = [redballs, greenballs, blueball]

while True:
	DISPLAYSURF.fill(WHITE)
	for event in pygame.event.get():
		if event.type == QUIT:
			quit_game()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				quit_game()
	blueball.x, blueball.y = blueball.player_movement(blueball.x,blueball.y)
	pygame.draw.circle(DISPLAYSURF, BLUE, (blueball.x,blueball.y), blue_radius, 0)
	for redball in redballs:
		(redball.angle, redball.x, redball.y) = redball.bounce(redball.angle, redball.x, redball.y, redball.speed)
		pygame.draw.circle(DISPLAYSURF, redball.color, (redball.x, redball.y), redball.radius, 0)
		if collision_check(redball.x, blueball.x, redball.y, blueball.y, redball.radius, blueball.radius):
			quit_game()
	for greenball in greenballs:
		(greenball.angle, greenball.x, greenball.y) = greenball.bounce(greenball.angle,greenball.x,greenball.y,greenball.speed)
		pygame.draw.circle(DISPLAYSURF, greenball.color, (greenball.x, greenball.y), greenball.radius, 0)
		if collision_check(greenball.x, blueball.x, greenball.y, blueball.y, greenball.radius, blueball.radius):
			score += 1
			greenball.x = random.randint(0,WINDOWWIDTH)
			greenball.y = random.randint(0,WINDOWHEIGHT)
			greenball.angle = 2*math.pi*random.random()
			greenball.speed += 1
	SCORE_SURF, SCORE_RECT = make_text(f"Score: {score}", BLACK, WHITE, WINDOWWIDTH - 120, 30)
	DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)
	pygame.display.update()
	FPSCLOCK.tick(FPS)