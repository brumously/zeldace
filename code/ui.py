import pygame
from settings import * 
#from level import Level

class UI:
	def __init__(self):
		#self.level = Level()
		#self.player = self.level.player
		#self.wizard = self.level.wizard
		
		
		# general 
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)


	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg 
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)

	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(80,635,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(magic_surf,magic_rect)

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

		self.show_exp(player.exp)

		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)

	def dialogue(self, current_dialogue):
		# Colors
		BLACK = (0, 0, 0)
		WHITE = (255, 255, 255)

		# Fonts
		FONT_SIZE = 30
		dialogue_font = pygame.font.Font(None, FONT_SIZE)

		# Define the NPC's dialogue
		npc_dialogue = [
			"Hello adventurer",
			"This land is overrun with enemies. You shouldn't be here",
			"If you insist on your quest, I cannot stop you",
			"Although I may provide you with a little help",
			"Let me get a closer look at you",
			"Good luck, and no matter what you do, DO NOT GIVE UP",
		]

		#Game state variables
		dialogue_open = True
		#current_dialogue = 0
		dialogue_finished = False
		text = ""

		# Display the dialogue box if it is open
		#if current_dialogue <= len(npc_dialogue):
		if current_dialogue < len(npc_dialogue):
			if current_dialogue == len(npc_dialogue):
				text = "Press Enter to close"
				dialogue_open = False
			else:
				text = npc_dialogue[current_dialogue]
				#current_dialogue +=1
				#display_dialogue_box(dialogue_text)

				#print dialogue box
			dialogue_box_height = FONT_SIZE + 20
			dialogue_box_rect = pygame.Rect(20, HEIGHT - dialogue_box_height - 10, WIDTH - 40, dialogue_box_height)
			border_rect = pygame.Rect(dialogue_box_rect.left - 2, dialogue_box_rect.top - 2, dialogue_box_rect.width + 4, dialogue_box_rect.height + 4)

			pygame.draw.rect(self.display_surface, WHITE, border_rect)
			pygame.draw.rect(self.display_surface, BLACK, dialogue_box_rect)

			dialogue_text = dialogue_font.render(text, True, WHITE) #dialogue_font.render(text, True, WHITE)
			self.display_surface.blit(dialogue_text, (dialogue_box_rect.x + 5, dialogue_box_rect.y + 5))
		
		#while current_dialogue <= len(npc_dialogue):
			pygame.display.update()
			#if not pygame.key.get_pressed()[pygame.K_t]:
			pygame.time.delay(len(npc_dialogue[current_dialogue])*70)
			if current_dialogue==4:
				print(3)
				# potion = pygame.image.load('../graphics/potions/purple.png').convert_alpha()
				# potion_rect = potion.get_rect(center = self.wizard.rect.center)
				# while potion_rect.center != self.player.rect.center:
				# 	self.display_surface.blit(potion, potion_rect)
				# 	if potion_rect.x < self.player.rect.x:
				# 		potion_rect.x+=5
				# 	else:
				# 		potion_rect.x-=5
				# 	if potion_rect.y < self.player.rect.y:
				# 		potion_rect.y+=5
				# 	else:
				# 		potion_rect.y-=5
				# 	pygame.display.update()

				# score = int(input("score:"))
				# if score <=60:
				# 	pygame.draw.rect(self.display_surface, WHITE, border_rect)
				# 	pygame.draw.rect(self.display_surface, BLACK, dialogue_box_rect)

				# 	dialogue_text = dialogue_font.render("you're ugly", True, WHITE) #dialogue_font.render(text, True, WHITE)
				# 	self.display_surface.blit(dialogue_text, (dialogue_box_rect.x + 5, dialogue_box_rect.y + 5))
				# 	pygame.display.update()
				# 	#if not pygame.key.get_pressed()[pygame.K_t]:
				# 	pygame.time.delay(len(1000))
				# elif score >=60:
				# 	pygame.draw.rect(self.display_surface, WHITE, border_rect)
				# 	pygame.draw.rect(self.display_surface, BLACK, dialogue_box_rect)

				# 	dialogue_text = dialogue_font.render("eh, you're decent", True, WHITE) #dialogue_font.render(text, True, WHITE)
				# 	self.display_surface.blit(dialogue_text, (dialogue_box_rect.x + 5, dialogue_box_rect.y + 5))
				# 	pygame.display.update()
				# 	#if not pygame.key.get_pressed()[pygame.K_t]:
				# 	pygame.time.delay(1000)

	def throw_potion(self, potion, potion_rect):
		self.display_surface.blit(potion, potion_rect)
		print("blit",potion_rect.center)
		pygame.display.update()
		#pygame.time.delay(100)


