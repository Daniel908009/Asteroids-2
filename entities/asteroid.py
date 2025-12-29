from entities.entity import Entity
import random

class Asteroid(Entity):
    def __init__(self,game, position, velocity, surface, size):
        super().__init__(position)
        self.game = game
        self.position = position
        self.velocity = velocity
        self.image = surface
        self.size = size
        self.rect = self.image.get_rect(center=self.position)
        self.score_value = {"large": 5, "medium": 10, "small": 15}[size]
        self.damage = {"large": 3, "medium": 2, "small": 1}[size]
        self.parent = None
        self.inheritanceDone = False
    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.rect.center = self.position
        if self.position.x < -100 - self.rect.width or self.position.x > self.game.settings.SCREEN_WIDTH + self.rect.width or \
           self.position.y < -100 - self.rect.height or self.position.y > self.game.settings.SCREEN_HEIGHT + self.rect.height:
            self.game.asteroids.remove(self)
            self.game.all_sprites.remove(self)
            self.kill()
    def inheritanceSplit(self, asteroidSpriteGroup=None, allSpritesGroup=None):
        if self.inheritanceDone:
            return
        self.inheritanceDone = True
        size_map = {
            "large": "medium",
            "medium": "small"
        }
        if self.size in size_map:
            new_size = size_map[self.size]
            for _ in range(2):
                surface = self.game.spawner.createAsteroidSurface(new_size)
                velocity = self.velocity.rotate(random.uniform(-45, 45)) * random.uniform(0.8, 1.2)
                asteroid = Asteroid(self.game, self.position.copy(), velocity, surface, new_size)
                asteroid.parent = self
                if asteroidSpriteGroup is not None and asteroidSpriteGroup is not False:
                    asteroidSpriteGroup.add(asteroid)
                elif asteroidSpriteGroup is not False:
                    self.game.asteroids.add(asteroid)
                if allSpritesGroup is not None and allSpritesGroup is not False:
                    allSpritesGroup.add(asteroid)
                elif allSpritesGroup is not False:
                    self.game.all_sprites.add(asteroid)