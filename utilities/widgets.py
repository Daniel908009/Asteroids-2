import pygame

class StartMenuWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Start Game", "High Scores", "Quit"]
    def draw(self, screen):
        screen.fill((0, 0, 0))
        # options
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                # drawing a triangle next to selected option
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - 80, screen.get_height() // 2 + i * 40 + 10),
                                                          (screen.get_width() // 2 - 100, screen.get_height() // 2 + i * 40 + 5),
                                                          (screen.get_width() // 2 - 100, screen.get_height() // 2 + i * 40 + 15)])
            text = font.render(option, True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 + i * 40))
        # title
        font = pygame.font.Font(None, 74)
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
        pass

class HighScoresWidget:
    def __init__(self, game):
        self.game = game
    def draw(self, screen):
        pass