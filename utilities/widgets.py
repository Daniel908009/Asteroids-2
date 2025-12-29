import pygame
from settings import Settings
from utilities.spawner import Spawner
from entities.asteroid import Asteroid
from entities.explosionEffect import ExplosionEffect
import math

def OutlinedText(text, font, text_color, outline_color, outline_width, screen, position):
    base = font.render(text, True, text_color)
    size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
    img = pygame.Surface(size, pygame.SRCALPHA)
    for x_offset in range(-outline_width, outline_width + 1):
        for y_offset in range(-outline_width, outline_width + 1):
            if x_offset == 0 and y_offset == 0:
                continue
            img.blit(font.render(text, True, outline_color), (x_offset + outline_width, y_offset + outline_width))
    img.blit(base, (outline_width, outline_width))
    screen.blit(img, (position[0] - img.get_width() // 2, position[1] - img.get_height() // 2))

class StartMenuWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Start Game", "High Scores", "Settings", "Quit"]
        self.all_sprites = pygame.sprite.Group()
        self.explosion_effects = pygame.sprite.Group()
        self.spawner = Spawner(self.game, asteroid_spawn_interval=1, ufo_spawn_interval=False, allSpritesGroup=self.all_sprites)
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        self.explosion_effects.draw(screen)
        # options
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                # drawing a triangle next to selected option
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - 80 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 100 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 100 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE))])
            OutlinedText(option, font, color, (0,0,0), 2, screen, (screen.get_width() // 2, screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE))
        # title
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        OutlinedText("Start Menu", font, (255, 255, 255), (0, 0, 0), 3, screen, (screen.get_width() // 2, 100 * self.game.settings.UI_MENU_SCALE))
    def update(self, dt):
        self.spawner.update(dt)
        self.all_sprites.update(dt)
        self.explosion_effects.update(dt)
        for sprite in self.all_sprites: # temporary, fix this
            hits = pygame.sprite.spritecollide(sprite, self.all_sprites, False)
            for hit in hits:
                if sprite == hit or (hasattr(sprite, 'parent') and hasattr(hit, 'parent') and sprite.parent == hit.parent and hit.parent is not None):
                    continue
                if isinstance(sprite, Asteroid) and isinstance(hit, Asteroid):
                    size_order = {"large": 3, "medium": 2, "small": 1}
                    if size_order[sprite.size] >= size_order[hit.size]:
                        self.all_sprites.remove(hit)
                        hit.kill()
                        self.all_sprites.remove(sprite)
                        sprite.inheritanceSplit(asteroidSpriteGroup=self.all_sprites, allSpritesGroup=self.all_sprites)
                        sprite.kill()
                        self.explosion_effects.add(ExplosionEffect(self.game, "asteroid", hit.position.copy(), max(hit.rect.width, hit.rect.height)))
                    elif size_order[hit.size] > size_order[sprite.size]:
                        self.all_sprites.remove(sprite)
                        self.all_sprites.remove(hit)
                        hit.inheritanceSplit(asteroidSpriteGroup=self.all_sprites, allSpritesGroup=self.all_sprites)
                        sprite.kill()
                        hit.kill()
                        self.explosion_effects.add(ExplosionEffect(self.game, "asteroid", sprite.position.copy(), max(sprite.rect.width, sprite.rect.height)))
                elif isinstance(sprite, Asteroid) and not isinstance(hit, Asteroid):
                    self.all_sprites.remove(sprite)
                    self.all_sprites.remove(hit)
                    hit.kill()
                    sprite.inheritanceSplit(asteroidSpriteGroup=self.all_sprites, allSpritesGroup=self.all_sprites)
                    sprite.kill()
                    self.explosion_effects.add(ExplosionEffect(self.game, "asteroid", sprite.position.copy(), max(sprite.rect.width, sprite.rect.height)))
                elif not isinstance(sprite, Asteroid) and isinstance(hit, Asteroid):
                    self.all_sprites.remove(hit)
                    self.all_sprites.remove(sprite)
                    sprite.kill()
                    hit.inheritanceSplit(asteroidSpriteGroup=self.all_sprites, allSpritesGroup=self.all_sprites)
                    hit.kill()
                    self.explosion_effects.add(ExplosionEffect(self.game, "asteroid", hit.position.copy(), max(hit.rect.width, hit.rect.height)))
    def handle_event(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:
                pygame.mixer.music.stop()
                self.game.state = "playing"
            elif self.selected_option == 1:
                self.game.state = "high_scores"
            elif self.selected_option == 2:
                self.game.state = "settings"
            elif self.selected_option == 3:
                self.game.running = False
            
class GameOverWidget:
    def __init__(self, game):
        self.game = game
    def draw(self, screen):
        screen.fill((0,0,0))
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height() //2 - 50 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        score_text = font.render(f"Your Score: {self.game.score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 + 10))
        font = pygame.font.Font(None, int(24 * self.game.settings.UI_MENU_SCALE))
        text = font.render("Enter name (10 letters) and press enter", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 + 50 * self.game.settings.UI_MENU_SCALE))
        name_text = font.render(f"Name: {self.game.player_name}", True, (255, 255, 255))
        screen.blit(name_text, (screen.get_width()//2 - name_text.get_width()//2, screen.get_height()//2 + 90 * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_RETURN:
            self.game.save_high_score(self.game.player_name, self.game.score)
            self.game.state = "menu"
            self.game.reset()
        elif event.key == pygame.K_BACKSPACE:
            self.game.player_name = self.game.player_name[:-1]
        else:
            if len(self.game.player_name) < 10 and event.unicode.isprintable():
                self.game.player_name += event.unicode

class HighScoresWidget:
    def __init__(self, game):
        self.game = game
    def draw(self, screen):
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        text = font.render("High Scores", True, (255, 255, 255))
        screen.fill((0,0,0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50 * self.game.settings.UI_MENU_SCALE))
        fontsize = self.game.screen.get_height() // 30
        font = pygame.font.Font(None, int(fontsize * self.game.settings.UI_MENU_SCALE))
        high_scores = self.game.load_high_scores()
        for i, (name, score) in enumerate(high_scores):
            score_text = font.render(f"{i+1}. {name} - {score}", True, (255, 255, 255))
            screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, 125 * self.game.settings.UI_MENU_SCALE + i * fontsize * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
            self.game.state = "menu"

class GameHUD:
    def __init__(self, game):
        self.game = game
    def draw(self):
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_GAME_SCALE))
        health_text = font.render(f"Health: {self.game.player.health}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        OutlinedText(f"Health: {self.game.player.health}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + health_text.get_width() // 2, 10 + health_text.get_height() // 2))
        OutlinedText(f"Score: {self.game.score}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + score_text.get_width() // 2, 50 + score_text.get_height() // 2))
        shield_status = "Ready" if self.game.player.shieldReady else "Cooldown"
        shield_text = font.render(f"Shield: {shield_status}", True, (255, 255, 255))
        OutlinedText(f"Shield: {shield_status}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + shield_text.get_width() // 2, 90 + shield_text.get_height() // 2))
        cooldown_ratio = self.game.player.getShieldCooldownRatio()
        pygame.draw.rect(self.game.screen, (255, 0, 0), (10, 130 * self.game.settings.UI_GAME_SCALE, 200 * self.game.settings.UI_GAME_SCALE, 15 * self.game.settings. UI_GAME_SCALE))
        pygame.draw.rect(self.game.screen, (0, 255, 0), (10, 130 * self.game.settings.UI_GAME_SCALE, 200 * cooldown_ratio * self.game.settings.UI_GAME_SCALE, 15 * self.game.settings.UI_GAME_SCALE))

class PauseMenuWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Resume Game", "Quit to Menu"]
    def draw(self, screen):
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        OutlinedText("Paused", font, (255, 255, 255), (0,0,0), 3, screen, (screen.get_width()//2, 100 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - 100 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 120 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 120 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE))])
            OutlinedText(option, font, color, (0,0,0), 2, screen, (screen.get_width() // 2, screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option -1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option +1) %len(self.options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:
                self.game.state = "playing"
                pygame.mixer.music.unpause()
                for channel in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(channel).unpause()
            elif self.selected_option == 1:
                self.selected_option = 0
                self.game.state = "menu"
                self.game.reset()
        
class SettingsWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.settingsList = vars(Settings)
        self.settingsList = {k: v for k, v in self.settingsList.items() if not k.startswith("__") and not callable(v)}
        self.modifying_widget = None
    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE)).render("Settings", True, (255, 255, 255))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        longest_setting_text = max([font.size(f"{setting}: {value}")[0] for setting, value in self.settingsList.items()])
        for i, (setting, value) in enumerate(self.settingsList.items()):
            color = (255, 255, 255)
            if i == self.selected_option:
                color = (255, 0, 0)
            if i == 0:
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - longest_setting_text // 2 - 20 * self.game.settings.UI_MENU_SCALE, (i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE) + screen.get_height()//2),
                                                            (screen.get_width() // 2 - longest_setting_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (i * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE) + screen.get_height()//2),
                                                            (screen.get_width() // 2 - longest_setting_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (i * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE) + screen.get_height()//2)])
            setting_text = font.render(f"{setting}: {value}", True, color)
            screen.blit(setting_text, (screen.get_width() // 2 - setting_text.get_width() // 2,screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE - self.selected_option * 40 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        surface = pygame.Surface((font.size("Settings")[0] + 40 * self.game.settings.UI_MENU_SCALE, font.size("Settings")[1] + 20 * self.game.settings.UI_MENU_SCALE))
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, surface.get_width(), surface.get_height()), 2)
        screen.blit(surface, (screen.get_width() // 2 - surface.get_width() // 2, 20 * self.game.settings.UI_MENU_SCALE))
        text = font.render("Settings", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, text.get_height() // 2))
        if self.modifying_widget:
            self.modifying_widget.draw(screen)
    def handle_event(self, event):
        if self.modifying_widget:
            self.modifying_widget.handle_event(event)
            return
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_BACKSPACE:
            self.game.state = "menu"
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.settingsList)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.settingsList)
        elif event.key == pygame.K_RETURN:
            self.modifying_widget = ModifyingWidget(self.game, list(self.settingsList.keys())[self.selected_option], list(self.settingsList.values())[self.selected_option], self)
        elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            newSettings = Settings()
            for setting, value in self.settingsList.items():
                setattr(newSettings, setting, value)
            self.game.settings = newSettings
            self.game.state = "menu"

class ModifyingWidget:
    def __init__(self, game, setting_name, setting_value, parent):
        self.game = game
        self.setting_name = setting_name
        self.parent = parent
        self.selected_option = 0
        if isinstance(setting_value, bool):
            self.options = ["On", "Off"]
        else:
            self.options = ["+1","+0.1","-0.1","-1"]
    def draw(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        text = font.render(f"Modify {self.setting_name}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, text.get_height() // 2))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        current_value = self.parent.settingsList[self.setting_name]
        value_text = font.render(f"Current Value: {current_value}", True, (255, 255, 255))
        screen.blit(value_text, (screen.get_width() // 2 - value_text.get_width() // 2, text.get_height() * 3))
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected_option:
                color = (255, 0, 0)
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - 100 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + (i + 1) * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 120 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + (i + 1) * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - 120 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + (i + 1) * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE))])
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen.get_width() // 2 - option_text.get_width() // 2, screen.get_height() // 2 + (i + 1) * 40 * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_BACKSPACE:
            self.parent.modifying_widget = None
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            current_value = self.parent.settingsList[self.setting_name]
            if isinstance(current_value, bool):
                new_value = True if self.selected_option == 0 else False
            else:
                change = float(self.options[self.selected_option])
                new_value = math.floor((current_value + change) * 10) / 10
                if isinstance(current_value, int):
                    new_value = int(new_value)
            self.parent.settingsList[self.setting_name] = new_value