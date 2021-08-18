import pygame
import sys
import random

HEIGHT = 600
WIDTH  = 400

class Bird():
	def __init__(self, display):
		self.display = display

		self.image = pygame.image.load("up.png")
		self.upImg = pygame.image.load("up.png")
		self.downImg = pygame.image.load("down.png")

		self.width = 40
		self.height = 29
		self.x = 90
		self.y = (HEIGHT + self.height)//2
		self.speed = 0
		self.lift = -13
		self.gravity = 0.7

		self.alive = True
		self.hitBottom = False

	def draw(self):
		if self.speed < 0: 
			self.image = self.upImg
		else:
			self.image = self.downImg

		self.display.blit(self.image, (self.x, self.y))

	def update(self):
		self.speed += self.gravity
		self.speed *= 0.9
		self.y += self.speed

		if (self.y + self.height) > HEIGHT:
			self.hitBottom = True
		elif (self.y + self.speed) <= 0:
			self.y = 0
			self.speed = 0

	def jump(self):
		self.speed = self.lift

class Pipe(object):
	def __init__(self, display):
		self.display = display
		self.bottomPart = pygame.image.load("bottom.png")
		self.topPart = pygame.image.load("top.png")
		self.gap = 120
		self.speed = -2.0
		self.width = self.bottomPart.get_width()
		self.height = self.topPart.get_height()
		self.x = WIDTH
		self.y = random.randint(70, HEIGHT-self.gap-70)

	def show(self):
		self.display.blit(self.topPart, (self.x, self.y-self.height))
		self.display.blit(self.bottomPart, (self.x, self.y+self.gap))

	def update(self):
		self.x += self.speed

	def hits(self, bird):
		margin = 3.5
		if(self.x < (bird.x+bird.width-margin)) and ((self.x+self.width) > bird.x+margin):
			if bird.y+margin < self.y or (bird.y + bird.height-margin)> (self.y+self.gap):
				return True
		return False


class flappyBird:
	def __init__(self):
		#Initializing sreen
		pygame.init()
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Flappy birds")
		self.display = pygame.display.set_mode((WIDTH, HEIGHT))#Width and hieght of display
		#Initializing background
		self.background = pygame.image.load("background.png")
		#Creating a bird object
		self.bird = Bird(self.display)
		#Creating pipes
		self.pipes = [Pipe(self.display)]
		self.score = 0

	def update_screen(self):
		self.display.blit(self.background, (0, 0))
		for pipe in self.pipes:
			pipe.show()
		self.bird.draw()
		self.update_score()
		pygame.display.update()

	def update_score(self):
		white = pygame.Color(255,255,255)
		black = pygame.Color(0,0,0)
		def draw_text(x, y, string, col, size):
			font = pygame.font.SysFont("Impact", size)
			text = font.render(string, True, col)
			textbox = text.get_rect()
			textbox.center = (x, y)
			self.display.blit(text, textbox)
		x = 50
		y = 60
		offset = 3
		draw_text(x + offset, y-offset , str(self.score), white, 64)
		draw_text(x +offset, y+offset ,str(self.score), white, 64)
		draw_text(x -offset, y +offset , str(self.score), white, 64)
		draw_text(x-offset, y -offset , str(self.score), white, 64) 
		draw_text(x, y , str(self.score), black, 64)

	def run_game(self):	
		frame = 0
		closestPipe = None
		prevClosest = None
		while not self.bird.hitBottom:
			if frame == 120:
				newPipe = Pipe(self.display)
				self.pipes.append(newPipe)
				frame = 0

			for pipe in self.pipes:
				if self.bird.x < (pipe.x+pipe.width):
					prevClosest = closestPipe
					closestPipe = pipe
					break
			#Looping through all the current events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:#User wants to exit of the program
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.unicode == ' ' and self.bird.alive:#Here bird has to jump
						self.bird.jump()

			#Update the coordinates of the pipes
			if self.bird.alive:
				pipe = self.pipes[0]
				if pipe.hits(self.bird):
					self.bird.lift = -18
					self.bird.jump()
					self.bird.alive = False
				for pipe in self.pipes:
					pipe.update()
					if (pipe.x+pipe.width) < 0:
						self.pipes.remove(pipe)
			
			if prevClosest and closestPipe:
				if prevClosest.x != closestPipe.x:
					self.score += 1

			self.bird.update()
			self.update_screen()
			self.clock.tick(60)
			frame += 1

if __name__ == "__main__":
	flappyBird().run_game()