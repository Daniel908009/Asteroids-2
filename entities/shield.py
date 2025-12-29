import pygame
from entities.entity import Entity

class Shield(Entity):
    def __init__(self, position, size, owner):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load("Assets/ship_shield.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.duration = owner.game.settings.SHIELD_DURATION
        self.elapsed_time = 0
        self.owner = owner
    def update(self, delta_time):
        self.pos = self.owner.pos
        self.rect.center = self.pos
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.duration:
            self.owner.shieldDown()