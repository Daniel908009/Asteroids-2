import pygame
from entities.asteroid import Asteroid
import random
from entities.UFO import UFO

class Spawner:
    def __init__(self, game, asteroid_spawn_interval=None, ufo_spawn_interval=None, ufoGroup=None, asteroidGroup=None, allSpritesGroup=None):
        self.game = game
        self.asteroid_spawn_interval = self.game.settings.ASTEROID_SPAWN_INTERVAL if asteroid_spawn_interval is None else asteroid_spawn_interval    
        self.ufo_spawn_interval = self.game.settings.UFO_SPAWN_INTERVAL if ufo_spawn_interval is None else ufo_spawn_interval
        self.asteroid_timer = 0
        self.ufo_timer = 0
        self.ufo_group = ufoGroup
        self.asteroid_group = asteroidGroup
        self.all_sprites = allSpritesGroup
    def update(self, dt):
        self.asteroid_timer += dt
        self.ufo_timer += dt
        if self.asteroid_timer > self.asteroid_spawn_interval and self.asteroid_spawn_interval is not False:
            self.spawn_asteroid()
            self.asteroid_timer = 0
        if self.ufo_timer > self.ufo_spawn_interval and self.ufo_spawn_interval is not False:
            self.spawn_ufo()
            self.ufo_timer = 0
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
        if self.asteroid_group is not None:
            self.asteroid_group.add(asteroid)
        self.all_sprites.add(asteroid)
    def createAsteroidSurface(self, size):
        size_map = {
            "small": int(30 * self.game.settings.ASSETS_SCALE),
            "medium": int(50 * self.game.settings.ASSETS_SCALE),
            "large": int(70 * self.game.settings.ASSETS_SCALE)
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
    def spawn_ufo(self):
        radius = max(self.game.screen.get_width(), self.game.screen.get_height()) / 2 + 100
        center = pygame.Vector2(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2)
        angle = random.uniform(0, 360)
        pos = center + pygame.Vector2(radius, 0).rotate(angle)
        targetLocation = pygame.Vector2(random.uniform(self.game.screen.get_width()//4, self.game.screen.get_width() - self.game.screen.get_width()//4), random.uniform(self.game.screen.get_height()//4, self.game.screen.get_height() - self.game.screen.get_height()//4))
        direction = (targetLocation - pos).normalize()
        velocity = direction * self.game.settings.UFO_SPEED
        ufo = UFO(self.game, pos, velocity)
        self.all_sprites.add(ufo)
        if self.asteroid_group is not None:
            self.ufo_group.add(ufo)
        pygame.mixer.Sound("Assets/ufo-arrival.mp3").play()