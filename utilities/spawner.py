import pygame
from entities.asteroid import Asteroid
import random

class Spawner:
    def __init__(self, game):
        self.game = game
        self.timer = 0
    def update(self, dt):
        self.timer += dt
        if self.timer > 1.5:
            self.spawn_asteroid()
            self.timer = 0
    def spawn_asteroid(self):
        radius = max(self.game.screen.get_width(), self.game.screen.get_height()) / 2 + 100
        center = pygame.Vector2(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)
        angle = random.uniform(0, 360)
        pos = center + pygame.Vector2(radius, 0).rotate(angle)
        direction = (center - pos).normalize()
        velocity = direction.rotate(random.uniform(-30, 30)) * random.randint(50, 150)
        size = random.choice(["small", "medium", "large"])
        surface = self.createAsteroidSurface(size)
        asteroid = Asteroid(self.game, pos, velocity, surface, size)
        self.game.asteroids.add(asteroid)
        self.game.all_sprites.add(asteroid)
    def createAsteroidSurface(self, size):
        size_map = {
            "small": 30,
            "medium": 50,
            "large": 70
        }
        pixel_size = size_map[size]
        surface = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
        points = []
        num_points = random.randint(7, 12)
        if num_points%2 == 0:
            num_points += 1
        for i in range(num_points):
            angle = i * (360 / num_points)
            distance = random.randint(pixel_size//3, pixel_size//2)
            point = (pixel_size//2 + distance * pygame.math.Vector2(1, 0).rotate(angle).x,
                     pixel_size//2 + distance * pygame.math.Vector2(1, 0).rotate(angle).y)
            points.append(point)
        pygame.draw.polygon(surface, (255,255,255), points)
        return surface