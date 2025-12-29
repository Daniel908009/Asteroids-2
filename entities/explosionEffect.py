from entities.entity import Entity
import pygame
import random
import math

class ExplosionEffect(Entity):
    def __init__(self, game, effect_type, position, size, sound = None):
        super().__init__(position)
        self.game = game
        self.explosion_time = 0.5
        self.current_time = 0.0
        if effect_type == "asteroid":
            self.image = self.createExplosionSprite(size, (255, 50, 0))
        elif effect_type == "player":
            self.image = self.createExplosionSprite(size, (0, 50, 255))
        elif effect_type == "ufo":
            self.image = self.createExplosionSprite(size, (50, 255, 50))
        self.rect = self.image.get_rect(center=self.position)
        if sound:
            sound.play()
    def update(self, delta_time):
        self.current_time += delta_time
        if self.current_time >= self.explosion_time:
            self.game.all_sprites.remove(self)
            self.kill()
    def createExplosionSprite(self,size, color):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        numPoints = random.randint(8, 12)
        if numPoints % 2 != 0:
            numPoints += 1
        points = 360//numPoints
        angle = 0
        minRadius = size // 4
        maxRadius = size // 2
        pointList = []
        for i in range(numPoints):
            if i % 2 == 0:
                radius = random.randint(minRadius, maxRadius)
                x = size // 2 + int(radius * math.cos(math.radians(angle)))
                y = size // 2 + int(radius * math.sin(math.radians(angle)))
                pointList.append((x, y))
            else:
                x = size // 2 + int(size * math.cos(math.radians(angle)))
                y = size // 2 + int(size * math.sin(math.radians(angle)))
                pointList.append((x, y))
            angle += points
        pygame.draw.polygon(surface, color, pointList)
        return surface