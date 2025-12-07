import pygame
from math import sin
from support import import_folder
from entity import Entity

class Wizard(Entity):
    def __init__(self, pos, groups):
        super().__init__(groups)
        wizard_image = pygame.image.load('../graphics/test/wizard.png').convert_alpha()
        scaled_image = pygame.transform.scale(wizard_image, (int(wizard_image.get_width() / 1000), int(wizard_image.get_height() / 1000)))
        self.image = scaled_image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -6)

        # graphics setup
        self.import_wizard_assets()
        self.status = 'cast_spell'
        self.animation_speed = 0.15

    def import_wizard_assets(self):
        wizard_path = '../graphics/wizard/'
        self.animations = {
            'cast_spell': [],
            'die': [],
            'walk': [],
            'idle': [],
            'run': [],
            'jump': [],
            'whack': []
        }

        for animation in self.animations.keys():
            full_path = wizard_path + animation
            self.animations[animation] = import_folder(full_path)

    

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)



    def update(self):
        self.animate()