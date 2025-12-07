import pygame
import random
from settings import *




class Menu():
    def __init__(self,game):
        self.game = game
        self.run_display = True
        self.mid_w, self.mid_h = WIDTH/2, HEIGHT/2
        self.cursor_rect = pygame.Rect(0,0,20,20) #cursor
        self.offset = -220 #to the left of text

    def draw_cursor(self): #asterisk
        self.game.draw_text('*', 35, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys() #reset keys in every frame

class SecretMenu(Menu): #inherit base class menu
    def __init__(self,game):
        Menu.__init__(self, game)
        self.state = "Start" #cursor points to 'start game'
        #position for lines of text
        self.startx, self.starty = self.mid_w, self.mid_h+30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h+90
        self.creditsx, self.creditsy = self.mid_w, self.mid_h+150
        #put asterisk next to start game
        self.cursor_rect.midtop=(self.startx+self.offset, self.starty)

    def display_menu(self):
        BG_COLOR = (0, 0, 0)
        STATIC_COLOR = (128, 128, 128)
        NUM_NOISE_POINTS = 500
        NOISE_INTENSITY = 100
        noise_points = []
        for _ in range(NUM_NOISE_POINTS):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            noise_points.append((x, y))
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BG_COLOR)
            for x, y in noise_points:
                noise_value = random.randint(-NOISE_INTENSITY, NOISE_INTENSITY)
                color = tuple(max(0, min(255, c + noise_value)) for c in STATIC_COLOR)
                self.game.display.set_at((x, y), color)

            self.game.draw_text('Secret Mission Unlocked', 60, WIDTH/2,HEIGHT/2-100)
            self.game.draw_text('Start Game', 40, self.startx,self.starty)
            self.game.draw_text('Options',40,self.optionsx,self.optionsy)
            self.game.draw_text('Controls',40,self.creditsx,self.creditsy)

            self.game.draw_text('ENTER to select',15,WIDTH/2,HEIGHT-50)
            self.game.draw_text('UP DOWN to move',15,WIDTH/2,HEIGHT-30)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN:
            if self.state =='Start':
                self.cursor_rect.midtop = (self.optionsx+self.offset,self.optionsy)
                self.state = 'Options'
            elif self.state =='Options':
                self.cursor_rect.midtop = (self.creditsx+self.offset,self.creditsy)
                self.state = 'Credits'
            elif self.state =='Credits':
                self.cursor_rect.midtop = (self.startx+self.offset,self.starty)
                self.state = 'Start'
        elif self.game.UP:
            if self.state =='Start':
                self.cursor_rect.midtop = (self.creditsx+self.offset,self.creditsy)
                self.state = 'Credits'
            elif self.state =='Options':
                self.cursor_rect.midtop = (self.startx+self.offset,self.starty)
                self.state = 'Start'
            elif self.state =='Credits':
                self.cursor_rect.midtop = (self.optionsx+self.offset,self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START:
            if self.state == 'Start':
                self.game.cur_menu=None
                self.run_display=False
            elif self.state =='Credits':
                self.game.cur_menu = self.game.controls2
            elif self.state =='Options':
                self.game.cur_menu=self.game.options2

            self.run_display=False
            

class SecretOptions(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'KillWizard'
        self.volx,self.voly=self.mid_w,self.mid_h+20
        self.controlsx,self.controlsy = self.mid_w,self.mid_h+60
        self.cursor_rect.midtop = (self.volx+self.offset,self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Secret Mission -- Kill The Wizard', 40, WIDTH/2,HEIGHT/2-30)
            self.game.draw_text('Accept', 30, self.volx,self.voly)
            self.game.draw_text('Decline',30,self.controlsx,self.controlsy)

            self.game.draw_text('ENTER to select',15,WIDTH/2,HEIGHT-70)
            self.game.draw_text('UP / DOWN to move',15,WIDTH/2,HEIGHT-50)
            self.game.draw_text('BACKSPACE to go back',15,WIDTH/2,HEIGHT-30)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK:
            self.game.secret_menu.display_menu()
            self.run_display = False
        elif self.game.UP or self.game.DOWN:
            if self.state =='KillWizard':
                self.cursor_rect.midtop = (self.controlsx+self.offset,self.controlsy)
                self.state = 'NoKilling'
            elif self.state =='NoKilling':
                self.cursor_rect.midtop = (self.volx+self.offset,self.voly)
                self.state = 'KillWizard'
        elif self.game.START:
            #to-do:create a volume menu and a controls menu
            if self.state == 'KillWizard':
                while self.run_display:
                    self.game.reset_keys()
                    self.game.check_events()
          
                    if self.game.START or self.game.BACK:
                        self.game.cur_menu=self.game.secret_menu
                        self.run_display=False
                        
                    self.game.display.fill(self.game.BLACK)
                    self.game.draw_text('Defeat wizard to win the game', 40, WIDTH/2,HEIGHT/2-30)
                    self.game.draw_text('Good luck', 40, WIDTH/2,HEIGHT/2+30)
                    self.game.draw_text('ENTER / BACKSPACE to go back',15,WIDTH/2,HEIGHT-30)
                    self.blit_screen()
            elif self.state == 'NoKilling':
                while self.run_display:
                    self.game.reset_keys()
                    self.game.check_events()
          
                    if self.game.START or self.game.BACK:
                        self.game.cur_menu=self.game.options2
                        self.run_display=False
                        
                    self.game.display.fill(self.game.BLACK)
                    self.game.draw_text('Choose wisely', 40, WIDTH/2,HEIGHT/2)
                    self.game.draw_text('ENTER / BACKSPACE to go back',15,WIDTH/2,HEIGHT-30)
                    self.blit_screen()


class SecretControls(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START or self.game.BACK:
                self.game.cur_menu = self.game.secret_menu
                self.run_display=False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('[ Arrow keys ] -- move',30,WIDTH/2,HEIGHT/2-150)
            self.game.draw_text('[ space ] -- attack',30,WIDTH/2,HEIGHT/2-100)
            self.game.draw_text('[ m ] -- open upgrade menu',30,WIDTH/2,HEIGHT/2-50)
            self.game.draw_text('[ q ] -- switch weapons',30,WIDTH/2,HEIGHT/2)
            self.game.draw_text('[ e ] -- switch magic effect',30,WIDTH/2,HEIGHT/2+50)
            self.game.draw_text('[ left ctrl ] -- cast magic spell',30,WIDTH/2,HEIGHT/2+100)
            self.game.draw_text('[ esc ] -- exit back to start menu',30,WIDTH/2,HEIGHT/2+150)
            self.game.draw_text('ENTER / BACKSPACE to go back',15,WIDTH/2,HEIGHT-30)
            self.blit_screen()