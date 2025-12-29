from entities.entity import Entity
import pygame

class LaserBullet(Entity):
    def __init__(self, position, angle, game, owner):
        super().__init__(position)
        self.game = game
        self.original_image = pygame.transform.scale(pygame.image.load("Assets/laserShot.png"), (int(10 * self.game.settings.ASSETS_SCALE), int(30 * self.game.settings.ASSETS_SCALE)))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.pos = pygame.math.Vector2(position)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.angle = angle
        self.speed = self.game.settings.BULLET_SPEED
        self.velocity = pygame.math.Vector2(0, -1).rotate(-self.angle) * self.speed
        self.owner = owner
    def update(self, delta_time):
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos
        if (self.pos.x < 0-self.rect.width or self.pos.x > self.game.settings.SCREEN_WIDTH + self.rect.width or
            self.pos.y < 0-self.rect.height or self.pos.y > self.game.settings.SCREEN_HEIGHT + self.rect.height):
            self.game.laserBullets.remove(self)
            self.game.all_sprites.remove(self)
            self.kill()