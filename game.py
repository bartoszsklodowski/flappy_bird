import pygame
from pygame.locals import *
import random
from settings import GameSettings
from sprites import Pipe, RestartButton, MenuButton, Bird


class Game:
	def __init__(self):
		pygame.init()
		self.game_settings = GameSettings()
		self.clock = pygame.time.Clock()
		self.last_pipe = pygame.time.get_ticks() - self.game_settings.PIPE_FREQUENCY
		self.flying = False
		self.game_over = False
		self.game_paused = True
		self.pass_pipe = False
		self.score = 0
		self.ground_scroll = 0
		self.menu_state = "start"

		self.screen = pygame.display.set_mode((self.game_settings.SCREEN_WIDTH, self.game_settings.SCREEN_HEIGHT))
		pygame.display.set_caption('Flappy Bird')

        #define font
		self.font = pygame.font.SysFont('Bauhaus 93', 60)

        #define colours
		self.white = (255, 255, 255)
		
        #music
		self.music = pygame.mixer.Sound('data/sounds/music.wav')
		self.music.set_volume(0.2)
		self.music.play(loops = -1)

        #load images
		self.bg = pygame.image.load('data/img/bg.png')
		self.ground_img = pygame.image.load('data/img/ground.png')
		self.restart_button_img = pygame.image.load('data/img/restart.png')
		self.resume_button_img = pygame.image.load('data/img/resume.png').convert_alpha()
		self.start_button_img = pygame.image.load('data/img/start.png').convert_alpha()
		self.quit_button_img = pygame.image.load('data/img/quit.png').convert_alpha()

		self.pipe_group = pygame.sprite.Group()
		self.bird_group = pygame.sprite.Group()

		self.flappy = Bird(100, int(self.game_settings.SCREEN_HEIGHT / 2))

		self.bird_group.add(self.flappy)

		#create button instances
		self.restart_button = RestartButton(self.game_settings.SCREEN_WIDTH // 2 - 50, self.game_settings.SCREEN_HEIGHT // 2 - 100, self.restart_button_img)
		self.resume_button = MenuButton(344, 125, self.resume_button_img, 1)
		self.start_button = MenuButton(344, 125, self.start_button_img, 1)
		self.quit_button = MenuButton(380, 250, self.quit_button_img, 1)


    #function for outputting text onto the screen
	def draw_text(self, text, text_col, x, y):
		img = self.font.render(text, True, text_col)
		self.screen.blit(img, (x, y))

	def reset_game(self):
		self.pipe_group.empty()
		self.flappy.rect.x = 100
		self.flappy.rect.y = int(self.game_settings.SCREEN_HEIGHT / 2)
		self.score = 0
		return self.score

	def run_game(self):
		self.run = True

		while self.run:

			self.clock.tick(self.game_settings.FPS)

			if self.game_paused == True:
				self.screen.fill((52, 78, 91))
				if self.menu_state == "start":
					if self.start_button.draw(self.screen):
						self.game_paused = False
						self.menu_state = "pause"
					if self.quit_button.draw(self.screen):
						self.run = False			
				if self.menu_state == "pause":
					if self.resume_button.draw(self.screen):
						self.game_paused = False
					if self.quit_button.draw(self.screen):
						self.run = False

			if self.game_paused == False:
				#draw background
				self.screen.blit(self.bg, (0,0))

				self.pipe_group.draw(self.screen)
				self.bird_group.draw(self.screen)
				self.bird_group.update(self.flying, self.game_over)

				#draw and scroll the ground
				self.screen.blit(self.ground_img, (self.ground_scroll, 768))

				#check the score
				if len(self.pipe_group) > 0:
					if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
						and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right\
						and self.pass_pipe == False:
						self.pass_pipe = True
					if self.pass_pipe == True:
						if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
							self.score += 1
							self.pass_pipe = False
				self.draw_text(str(self.score), self.white, int(self.game_settings.SCREEN_WIDTH / 2), 20)


				#look for collision
				if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
					self.game_over = True
				#once the bird has hit the ground it's game over and no longer flying
				if self.flappy.rect.bottom >= 768:
					self.game_over = True
					self.flying = False


				if self.flying == True and self.game_over == False:
					#generate new pipes
					self.time_now = pygame.time.get_ticks()
					if self.time_now - self.last_pipe > self.game_settings.PIPE_FREQUENCY:
						self.pipe_height = random.randint(-100, 100)
						self.btm_pipe = Pipe(self.game_settings.SCREEN_WIDTH, int(self.game_settings.SCREEN_HEIGHT / 2) + self.pipe_height, -1)
						self.top_pipe = Pipe(self.game_settings.SCREEN_WIDTH, int(self.game_settings.SCREEN_HEIGHT / 2) + self.pipe_height, 1)
						self.pipe_group.add(self.btm_pipe)
						self.pipe_group.add(self.top_pipe)
						self.last_pipe = self.time_now

					self.pipe_group.update()

					self.ground_scroll -= self.game_settings.SCROLL_SPEED
					if abs(self.ground_scroll) > 35:
						self.ground_scroll = 0
				

				#check for game over and reset
				if self.game_over == True:
					if self.restart_button.draw(self.screen):
						self.game_over = False
						self.score = self.reset_game()


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.game_paused = True
				if event.type == pygame.MOUSEBUTTONDOWN and self.flying == False and self.game_over == False:
					self.flying = True

			pygame.display.update()

		pygame.quit()


if __name__ == '__main__':
	game = Game()
	game.run_game()
	