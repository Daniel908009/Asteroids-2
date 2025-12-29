import pygame
class Entity(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position