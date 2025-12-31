from entities.entity import Entity
import pygame
from entities.laserBullet import LaserBullet
import random

class UFO(Entity):
    def __init__(self, game, pos, velocity, shootingAllowed=True):
        super().__init__(pos)
        self.game = game
        self.shoot_timer = 0
        self.velocity = velocity
        self.image = pygame.transform.scale(pygame.image.load("Assets/UFO.png"), (int(70 * self.game.settings.ASSETS_SCALE), int(40 * self.game.settings.ASSETS_SCALE)))
        self.rect = self.image.get_rect(center=self.position)
        self.score_value = 20
        self.damage = 2
        self.shootingAllowed = shootingAllowed
    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        if self.isInScreen():
            self.shoot_timer += dt
        if self.shoot_timer > self.game.settings.UFO_SHOOT_COOLDOWN:
            self.shoot()
            self.shoot_timer = 0
        if (self.position.x < -max(self.game.screen.get_width(), self.game.screen.get_height()) / 2 or self.position.x > self.game.screen.get_width() + max(self.game.screen.get_width(), self.game.screen.get_height()) / 2 or
            self.position.y < -max(self.game.screen.get_width(), self.game.screen.get_height()) / 2 or self.position.y > self.game.screen.get_height() + max(self.game.screen.get_width(), self.game.screen.get_height()) / 2):
            self.game.all_sprites.remove(self)
            self.game.ufos.remove(self)
            self.kill()
    def isInScreen(self):
        return (0 <= self.position.x <= self.game.screen.get_width() and
                0 <= self.position.y <= self.game.screen.get_height())
    def shoot(self):
        if not self.shootingAllowed:
            return
        direction = (self.game.player.pos - self.position).normalize()
        angle = direction.angle_to(pygame.Vector2(0, -1)) + random.uniform(-15, 15)
        bullet = LaserBullet(self.position.copy(), angle, self.game, self)
        self.game.laserBullets.add(bullet)
        self.game.all_sprites.add(bullet)