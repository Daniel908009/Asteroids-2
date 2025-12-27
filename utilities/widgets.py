import pygame
from settings import UI_SCALE

class StartMenuWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Start Game", "High Scores", "Quit"]
    def draw(self, screen):
        screen.fill((0, 0, 0))
        # options
        font = pygame.font.Font(None, int(36 * UI_SCALE))
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                # drawing a triangle next to selected option
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - 80 * UI_SCALE, (screen.get_height() // 2 + i * 40 + 10 * UI_SCALE)),
                                                          (screen.get_width() // 2 - 100 * UI_SCALE, (screen.get_height() // 2 + i * 40 + 5 * UI_SCALE)),
                                                          (screen.get_width() // 2 - 100 * UI_SCALE, (screen.get_height() // 2 + i * 40 + 15 * UI_SCALE))])
            text = font.render(option, True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 + i * 40 * UI_SCALE))
        # title
        font = pygame.font.Font(None, int(74 * UI_SCALE))
        text = font.render("Start Menu", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() * 2))
    def handle_event(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:
                self.game.state = "playing"
            elif self.selected_option == 1:
                self.game.state = "high_scores"
            elif self.selected_option == 2:
                self.game.running = False
            
class GameOverWidget:
    def __init__(self, game):
        self.game = game
    def draw(self, screen):
        screen.fill((0,0,0))
        font = pygame.font.Font(None, int(74 * UI_SCALE))
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()))
        font = pygame.font.Font(None, int(36 * UI_SCALE))
        score_text = font.render(f"Your Score: {self.game.score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 + 10))
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.state = "menu"
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.game.state = "menu"
            self.game.reset()

class HighScoresWidget:
    def __init__(self, game):
        self.game = game
    def draw(self, screen):
        pass
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.state = "menu"

class GameHUD:
    def __init__(self, game):
        self.game = game
    def draw(self):
        font = pygame.font.Font(None, int(36 * UI_SCALE))
        health_text = font.render(f"Health: {self.game.player.health}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        self.game.screen.blit(health_text, (10, 10 * UI_SCALE))
        self.game.screen.blit(score_text, (10, 50 * UI_SCALE))