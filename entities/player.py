import pygame
from entities.entity import Entity
from entities.laserBullet import LaserBullet
from entities.shield import Shield

class Player(Entity):
    def __init__(self, position, game):
        super().__init__(position)
        self.game = game
        self.original_image = pygame.transform.scale(pygame.image.load("Assets/spaceship.png"), (int(60 * self.game.settings.ASSETS_SCALE), int(60 * self.game.settings.ASSETS_SCALE)))
        self.thrust_image = pygame.transform.scale(pygame.image.load("Assets/spaceship_thrust.png"), (int(60 * self.game.settings.ASSETS_SCALE), int(60 * self.game.settings.ASSETS_SCALE)))
        self.image = self.original_image
        self.pos = pygame.math.Vector2(position)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.health = self.game.settings.PLAYER_HEALTH
        self.angle = 0
        self.movementVector = pygame.math.Vector2(0, 0)
        self.timeSinceLastShot = 0
        self.sound = pygame.mixer.Sound("Assets/rocketSound.wav")
        pygame.mixer.set_reserved(30)
        pygame.mixer.set_reserved(29)
        self.shield = None
        self.shieldReady = True
        self.shieldCooldown = self.game.settings.SHIELD_COOLDOWN
        self.shieldTimeSinceUsed = 0
    def update(self, delta_time):
        self.timeSinceLastShot += delta_time
        if not self.shieldReady and self.shield is None:
            self.shieldTimeSinceUsed += delta_time
            if self.shieldTimeSinceUsed >= self.shieldCooldown:
                self.shieldReady = True
                self.shieldTimeSinceUsed = 0
        keys = pygame.key.get_pressed()
        vector = pygame.math.Vector2(0, 0)
        speed = self.game.settings.PLAYER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vector.y = -1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle += self.game.settings.TURNING_INTENSITY
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle -= self.game.settings.TURNING_INTENSITY
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if vector.length() > 0 :
            vector = vector.rotate(-self.angle)
            vector = vector.normalize() * speed
            self.movementVector += vector
            self.image = pygame.transform.rotate(self.thrust_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            if not pygame.mixer.Channel(30).get_busy():
                pygame.mixer.Channel(30).play(self.sound, loops=-1)
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            pygame.mixer.Channel(30).stop()
        self.movementVector *= 0.98
        if self.movementVector.length() > speed:
            self.movementVector = self.movementVector.normalize() * speed
        self.pos += self.movementVector * delta_time
        self.rect.center = self.pos
        self.pos.x %= self.game.settings.SCREEN_WIDTH
        self.pos.y %= self.game.settings.SCREEN_HEIGHT
    def shoot(self):
        if self.timeSinceLastShot >= self.game.settings.PLAYER_SHOOT_COOLDOWN:
            bullet = LaserBullet(self.pos, self.angle, self.game, self)
            self.game.laserBullets.add(bullet)
            self.game.all_sprites.add(bullet)
            self.timeSinceLastShot = 0
            pygame.mixer.Sound("Assets/laserShot.wav").play()
    def reduceHealth(self, amount, sound):
        if not self.game.settings.INVINCIBILITY and self.shield is None:
            self.health -= amount
            sound.play()
            if self.health <= 0:
                self.game.state = "game_over"
                pygame.mixer.music.stop()
                pygame.mixer.Channel(30).stop()
            pygame.mixer.Sound("Assets/explosion-spaceship.mp3").play()
        elif self.shield is not None:
            pygame.mixer.Sound("Assets/shield_hit.wav").play()
    def shieldUp(self):
        if self.shield is None and self.shieldReady:
            self.shield = Shield(self.pos, int(100 * self.game.settings.ASSETS_SCALE), self)
            self.game.all_sprites.add(self.shield)
            self.shieldReady = False
            pygame.mixer.Channel(29).play(pygame.mixer.Sound("Assets/shield_hum.mp3"), loops=-1)
    def shieldDown(self):
        if self.shield:
            self.game.all_sprites.remove(self.shield)
            self.shield.kill()
            self.shield = None
            pygame.mixer.Channel(29).stop()
            pygame.mixer.Sound("Assets/shields_down.wav").play()
    def getShieldCooldownRatio(self):
        if self.shieldReady:
            return 1
        elif self.shield is None:
            return self.shieldTimeSinceUsed / self.shieldCooldown
        elif self.shield is not None:
            return (self.shield.elapsed_time / self.shield.duration) * -1 + 1