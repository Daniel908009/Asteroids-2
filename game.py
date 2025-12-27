import pygame
from entities.player import Player
from utilities.widgets import StartMenuWidget, GameOverWidget, HighScoresWidget, GameHUD
from utilities.spawner import Spawner
from entities.explosionEffect import ExplosionEffect
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        self.state = "menu"
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(pygame.image.load("spaceship_thrust.png"))
        self.score = 0
        self.player = Player((self.screen.get_width() // 2, self.screen.get_height() // 2), self)
        self.running = True
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.asteroids = pygame.sprite.Group()
        self.laserBullets = pygame.sprite.Group()
        self.startMenu = StartMenuWidget(self)
        self.gameOverMenu = GameOverWidget(self)
        self.highScoresMenu = HighScoresWidget(self)
        self.spawner = Spawner(self)
        self.game_hud = GameHUD(self)
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handleInputs()
            pygame.display.flip()
            if self.state == "menu":
                self.startMenu.draw(self.screen)
                pygame.display.flip()
            elif self.state == "playing":
                self.play_game(dt)
                self.update(dt)
            elif self.state == "high_scores":
                self.highScoresMenu.draw(self.screen)
            elif self.state == "game_over":
                self.gameOverMenu.draw(self.screen)
    def handleInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.state == "menu":
                    self.startMenu.handle_event(event)
                elif self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                elif self.state == "game_over":
                    self.gameOverMenu.handle_event(event)
                elif self.state == "high_scores":
                    self.highScoresMenu.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "playing" and event.button == 1:
                self.player.shoot()
    def play_game(self, dt):
        self.screen.fill((0, 0, 0))
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)
        self.game_hud.draw()
    def update(self, dt):
        self.all_sprites.update(dt)
        self.spawner.update(dt)
        self.check_collisions()
    def check_collisions(self):
        hit_asteroids = pygame.sprite.spritecollide(self.player, self.asteroids, False)
        if hit_asteroids:
            self.asteroids.remove(hit_asteroids[0])
            self.all_sprites.remove(hit_asteroids[0])
            position = ((hit_asteroids[0].position.x + self.player.pos.x) / 2,
                        (hit_asteroids[0].position.y + self.player.pos.y) / 2)
            exp = ExplosionEffect(self, "player", position, self.player.rect.width//2)
            self.all_sprites.add(exp)
            hit_asteroids[0].kill()
            self.player.health -= 1
            if self.player.health <= 0:
                self.state = "game_over"
        for bullet in self.laserBullets:
            hit_asteroids = pygame.sprite.spritecollide(bullet, self.asteroids, False)
            if hit_asteroids:
                self.laserBullets.remove(bullet)
                self.all_sprites.remove(bullet)
                bullet.kill()
                self.score += len(hit_asteroids) * 10
                for asteroid in hit_asteroids:
                    self.asteroids.remove(asteroid)
                    self.all_sprites.remove(asteroid)
                    if asteroid.size != "small":
                        asteroid.inheritanceSplit()
                    exp = ExplosionEffect(self, "asteroid", asteroid.position, max(asteroid.image.get_size()))
                    self.all_sprites.add(exp)
                    asteroid.kill()
    def reset(self):
        pass