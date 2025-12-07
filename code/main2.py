import pygame, sys
from settings import *
from menu import *
from level import Level
from game import *
from menu2 import *


class Start:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Zelda')
        pygame.display.set_icon(pygame.image.load('icon.png'))

        self.sound = pygame.mixer.Sound('../audio/fallendown.ogg')
        self.volume = 0.3
        self.sound.set_volume(self.volume)
        self.sound.play(loops = -1)

        self.running,self.playing = True, False 
        

        #running true when game is on, #playing true when player playing game
        self.UP, self.DOWN, self.START, self.BACK = False, False, False, False
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font_name = 'DTM-Sans.otf'
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        #game is going to pass itself into the main menu class
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.controls = ControlsMenu(self)
        self.gameover = GameOverMenu(self)

        self.secret_menu = SecretMenu(self)
        self.options2 = SecretOptions(self)
        self.controls2 = SecretControls(self)
        self.cur_menu = self.main_menu #can change depending on which menu selected

    def game(self): 
        while self.playing:
            self.sound.stop()
            self.check_events()
            start = Game(self)
            start.run()    
        self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                #stop whatever menu is running from being run
                self.cur_menu.run_display = False
                pygame.quit()
                exit()
            if event.type ==pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    self.START = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK = True
                if event.key == pygame.K_DOWN:
                    self.DOWN = True
                if event.key == pygame.K_UP:
                    self.UP = True
                
    
    def reset_keys(self):
        self.UP, self.DOWN, self.START, self.BACK = False, False, False, False
        

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
        
if __name__ == '__main__':
    g = Start()
    while g.running:
        g.cur_menu.display_menu()
        g.game()

        