import pygame
from pygame.locals import *

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# NPC Dialogue constants
NPC_RADIUS = 100  # The radius within which the player can interact with the NPC
DIALOGUE_BOX_HEIGHT = 100  # Height of the dialogue box at the bottom of the screen
DIALOGUE_BOX_PADDING = 10  # Padding for the dialogue box
DIALOGUE_BOX_COLOR = BLACK
DIALOGUE_BOX_BORDER_COLOR = WHITE
DIALOGUE_FONT_SIZE = 20

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)  # White rectangle as a placeholder for the NPC sprite
        self.rect = self.image.get_rect(center=(x, y))

        self.text_box_image = pygame.Surface((100, 30))  # Size of the text box
        self.text_box_image.fill(BLACK)
        self.text_box_rect = self.text_box_image.get_rect(center=(x, y - 50))  # Position the text box above the NPC
        self.show_text_box = False

    def update(self, player_rect):
        # Check if the player is within interaction radius
        if self.rect.colliderect(player_rect.inflate(NPC_RADIUS, NPC_RADIUS)):
            self.show_text_box = True
            return True
        else:
            self.show_text_box = False
            return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # Draw the text box if active
        if self.show_text_box:
            surface.blit(self.text_box_image, self.text_box_rect)
            font = pygame.font.Font(None, 20)
            text = font.render("Press T to talk", True, WHITE)
            text_rect = text.get_rect(center=self.text_box_rect.center)
            surface.blit(text, text_rect)
    
class DialogueBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, DIALOGUE_BOX_HEIGHT))
        self.image.fill(DIALOGUE_BOX_COLOR)
        self.rect = self.image.get_rect(bottom=HEIGHT, left=0)

    def update(self, dialogue):
        self.image.fill(DIALOGUE_BOX_COLOR)
        pygame.draw.rect(self.image, DIALOGUE_BOX_BORDER_COLOR, self.rect, 3)

        # Render the dialogue text
        font = pygame.font.Font(None, DIALOGUE_FONT_SIZE)
        text = font.render(dialogue, True, WHITE)
        text_rect = text.get_rect(x=self.rect.x + DIALOGUE_BOX_PADDING, centery=self.rect.centery)
        self.image.blit(text, text_rect)