import pygame
from entities.entity import Entity
from entities.laserBullet import LaserBullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(Entity):
    def __init__(self, position, game):
        super().__init__(position)
        self.game = game
        self.original_image = pygame.transform.scale(pygame.image.load("spaceship.png"), (60, 60))
        self.thrust_image = pygame.transform.scale(pygame.image.load("spaceship_thrust.png"), (60, 60))
        self.image = self.original_image
        self.pos = pygame.math.Vector2(position)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.health = 5
        self.angle = 0
        self.movementVector = pygame.math.Vector2(0, 0)
        self.timeSinceLastShot = 0.0
    def update(self, delta_time):
        self.timeSinceLastShot += delta_time
        keys = pygame.key.get_pressed()
        vector = pygame.math.Vector2(0, 0)
        speed = 300
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vector.y = -1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle += 4
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle -= 4
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if vector.length() > 0 :
            vector = vector.rotate(-self.angle)
            vector = vector.normalize() * speed
            self.movementVector += vector
            self.image = pygame.transform.rotate(self.thrust_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.movementVector *= 0.98
        if self.movementVector.length() > speed:
            self.movementVector = self.movementVector.normalize() * speed
        self.pos += self.movementVector * delta_time
        self.rect.center = self.pos
        self.pos.x %= SCREEN_WIDTH
        self.pos.y %= SCREEN_HEIGHT
    def shoot(self):
        if self.timeSinceLastShot >= 0.2:
            bullet = LaserBullet(self.pos, self.angle, self.game)
            self.game.laserBullets.add(bullet)
            self.game.all_sprites.add(bullet)
            self.timeSinceLastShot = 0.0