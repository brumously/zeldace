import pygame, sys
from settings import *
from level import Level
from menu import *
from player import Player
from ui import UI

# Fonts
FONT_SIZE = 30
BLACK = (0,0,0)
WHITE = (255,255,255)



class Game:
	def __init__(self,game):
		self.game=game
		
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.player = self.level.player
		self.wizard = self.level.wizard
		#self.player_pos = self.player.rect.center
		#self.npc_pos = self.wizard.rect.center
		self.talk_radius = 50
		self.menu = Menu(game)
		self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
		self.main_sound.set_volume(0.5)
		self.main_sound.play(loops = -1)

		self.display_surface = pygame.display.get_surface()

	def run(self):
		# Game loop
		#player_pos = self.player.rect.center
		#npc_pos = self.wizard.rect.center
		#distance = player_pos - pygame.math.Vector2(npc_pos)

		index = 0


		while self.game.playing:	
			if self.game.cur_menu:
				self.game.cur_menu.display_menu()
			else:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.game.running, self.game.playing = False, False
						#stop whatever menu is running from being run
						pygame.quit()
						exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_m:
							self.level.toggle_menu()
						if event.key == pygame.K_ESCAPE:						
							self.game.cur_menu = self.game.secret_menu
						if event.key == pygame.K_t and pygame.sprite.collide_rect(self.player,self.wizard):
							UI.dialogue(self, index)
							if index ==4:
								print(self.player.rect.center)
								potion = pygame.image.load('../graphics/potions/purple.png').convert()
								potion_rect = potion.get_rect(center = self.wizard.rect.center)
								while potion_rect.center != self.player.rect.center:
									#if potion_rect.centerx == self.player.rect.centerx and potion_rect.centery < self.player.rect.centery:
									#	break
									print(potion_rect.center)
									UI.throw_potion(self,potion,potion_rect)
									# self.game.screen.blit(potion, potion_rect)
									if potion_rect.centerx < self.player.rect.centerx:
										potion_rect.centerx+=1
									elif potion_rect.centerx > self.player.rect.centerx:
										potion_rect.centerx-=1
									if potion_rect.centery < self.player.rect.centery:
										potion_rect.centery+=1
									elif potion_rect.centery > self.player.rect.centery:
										potion_rect.centery-=1
									# pygame.display.update()
							index +=1
							
							
						
								
				if self.level.dead:
					self.main_sound.stop()
					self.game.cur_menu = self.game.gameover
					self.game.cur_menu.display_menu()
		
				

				self.game.screen.fill(WATER_COLOR)
				self.level.run()
				
				pygame.display.update()
				self.clock.tick(FPS)
			


	