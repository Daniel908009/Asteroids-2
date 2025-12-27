from entities.entity import Entity
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Asteroid(Entity):
    def __init__(self,game, position, velocity, surface, size):
        super().__init__(position)
        self.game = game
        self.position = position
        self.velocity = velocity
        self.image = surface
        self.size = size
        self.rect = self.image.get_rect(center=self.position)
    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.rect.center = self.position
        if self.position.x < -100 - self.rect.width or self.position.x > SCREEN_WIDTH + self.rect.width or \
           self.position.y < -100 - self.rect.height or self.position.y > SCREEN_HEIGHT + self.rect.height:
            self.game.asteroids.remove(self)
            self.game.all_sprites.remove(self)
            self.kill()
    def inheritanceSplit(self):
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
                self.game.asteroids.add(asteroid)
                self.game.all_sprites.add(asteroid)