import pygame
from entities.player import Player
from utilities.widgets import StartMenuWidget, GameOverWidget, HighScoresWidget

class Game:
    def __init__(self):
        self.state = "menu"
        self.screen = pygame.display.set_mode((800, 600))
        self.score = 0
        self.player = Player((self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.running = True
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.asteroids = pygame.sprite.Group()
        self.startMenu = StartMenuWidget(self)
        self.gameOverMenu = GameOverWidget(self)
        self.highScoresMenu = HighScoresWidget(self)
        pygame.display.set_caption("Asteroids")
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
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
                    pass
                elif self.state == "game_over":
                    self.gameOverMenu.handle_event(event)
                elif self.state == "high_scores":
                    self.highScoresMenu.handle_event(event)
    def play_game(self, dt):
        self.all_sprites.update(dt)
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
    def update(self, dt):
        self.all_sprites.update(dt)