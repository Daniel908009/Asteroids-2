import pygame
from settings import Settings
from utilities.spawner import Spawner
from entities.asteroid import Asteroid
from entities.explosionEffect import ExplosionEffect
from entities.UFO import UFO
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
        self.options = ["Start Game", "High Scores", "Settings","Manual", "Quit"]
        self.all_sprites = pygame.sprite.Group()
        self.explosion_effects = pygame.sprite.Group()
        self.spawner = Spawner(self.game, asteroid_spawn_interval=0.2, ufo_spawn_interval=5, allSpritesGroup=self.all_sprites, shootingAllowed=False)
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
        OutlinedText("Asteroids", font, (255, 255, 255), (0, 0, 0), 3, screen, (screen.get_width() // 2, 100 * self.game.settings.UI_MENU_SCALE))
    def update(self, dt):
        self.spawner.update(dt)
        self.all_sprites.update(dt)
        self.explosion_effects.update(dt)
        collision = pygame.sprite.groupcollide(self.all_sprites, self.all_sprites, False, False)
        for sprite1 in collision:
            for sprite2 in collision[sprite1]:
                if sprite1 != sprite2:
                    if isinstance(sprite1, Asteroid) and isinstance(sprite2, Asteroid):
                        if sprite1.parent == sprite2.parent and sprite1.parent is not None:
                            continue
                        if max(sprite1.rect.width, sprite1.rect.height) < max(sprite2.rect.width, sprite2.rect.height):
                            larger, smaller = sprite2, sprite1
                        else:
                            larger, smaller = sprite1, sprite2
                        explosion = ExplosionEffect(self.game, "asteroid", smaller.position.copy(), max(smaller.rect.width, smaller.rect.height))
                        self.explosion_effects.add(explosion)
                        self.all_sprites.remove(smaller)
                        larger.inheritanceSplit(asteroidSpriteGroup=False, allSpritesGroup=self.all_sprites)
                        self.all_sprites.remove(larger)
                        smaller.kill()
                        larger.kill()
                    elif (isinstance(sprite1, Asteroid) and not isinstance(sprite2, Asteroid)) or (isinstance(sprite2, Asteroid) and not isinstance(sprite1, Asteroid)):
                        asteroid = sprite1 if isinstance(sprite1, Asteroid) else sprite2
                        not_asteroid = sprite2 if asteroid == sprite1 else sprite1
                        explosion = ExplosionEffect(self.game, "asteroid", asteroid.position.copy(), max(asteroid.rect.width, asteroid.rect.height))
                        self.explosion_effects.add(explosion)
                        self.all_sprites.remove(asteroid)
                        if isinstance(not_asteroid, UFO):
                            explosion = ExplosionEffect(self.game, "ufo", not_asteroid.position.copy(), max(not_asteroid.rect.width, not_asteroid.rect.height))
                            self.explosion_effects.add(explosion)
                        self.all_sprites.remove(not_asteroid)
                        not_asteroid.kill()
                        asteroid.inheritanceSplit(asteroidSpriteGroup=False, allSpritesGroup=self.all_sprites)
                        asteroid.kill()
                    else:
                        explosion = ExplosionEffect(self.game, "ufo", sprite1.position.copy(), max(sprite1.rect.width, sprite1.rect.height))
                        self.explosion_effects.add(explosion)
                        self.all_sprites.remove(sprite1)
                        self.all_sprites.remove(sprite2)
                        sprite1.kill()
                        sprite2.kill()
    def handle_event(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:
                pygame.mixer.music.stop()
                self.game.reset()
                self.game.state = "playing"
            elif self.selected_option == 1:
                self.game.state = "high_scores"
            elif self.selected_option == 2:
                self.game.state = "settings"
            elif self.selected_option == 3:
                self.game.state = "manual"
            elif self.selected_option == 4:
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
        self.selected_option = 0
    def draw(self, screen):
        screen.fill((0,0,0))
        fontsize = self.game.screen.get_height() // 30
        font = pygame.font.SysFont("monospace", int(fontsize * self.game.settings.UI_MENU_SCALE))
        high_scores = self.game.load_high_scores()
        high_scores = self.process_high_scores(high_scores)
        self.options = high_scores
        for i in range(len(high_scores)):
            color = (255, 255, 255)
            if i == self.selected_option:
                color = (255, 0, 0)
            score_text = font.render(high_scores[i], True, color)
            screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, self.game.screen.get_height()//2 + i * fontsize * self.game.settings.UI_MENU_SCALE - self.selected_option * fontsize * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        text = font.render("High Scores", True, (255, 255, 255))
        rectangle = pygame.Surface((text.get_width() + 40 * self.game.settings.UI_MENU_SCALE, text.get_height() + 55 * self.game.settings.UI_MENU_SCALE))
        rectangle.fill((0,0,0))
        pygame.draw.rect(rectangle, (255, 255, 255), (0, 0, rectangle.get_width(), rectangle.get_height()), 2)
        screen.blit(rectangle, (screen.get_width()//2 - rectangle.get_width()//2, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 40 * self.game.settings.UI_MENU_SCALE))
    def process_high_scores(self, high_scores):
        scores = []
        prepadding_scores = []
        maxNumberLength = len(str(high_scores[0][1])) if high_scores else 0
        for i, entry in enumerate(high_scores):
            numberPadding = maxNumberLength - len(str(entry[1]))
            frontPadding = 0 if i+1 == 100 else 1 if i+1 >=10 else 2
            prepadding_scores.append(f"{" " * frontPadding}{i+1}. {entry[0]} -{" " * numberPadding} {entry[1]}")
        max_length = max([len(s) for s in prepadding_scores]) if prepadding_scores else 0
        for i, entry in enumerate(high_scores):
            numberPadding = maxNumberLength - len(str(entry[1]))
            frontPadding = 0 if i+1 == 100 else 1 if i+1 >=10 else 2
            scores.append(f"{" " * frontPadding}{i+1}. {" " * (max_length - len(prepadding_scores[i]))}{entry[0]} -{" "* numberPadding} {entry[1]}")
        return scores
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
            self.game.state = "menu"
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)

class GameHUD:
    def __init__(self, game):
        self.game = game
    def draw(self):
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_GAME_SCALE))
        health_text = font.render(f"Health: {int(self.game.player.health)}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        OutlinedText(f"Health: {int(self.game.player.health)}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + health_text.get_width() // 2, 10 + health_text.get_height() // 2))
        OutlinedText(f"Score: {self.game.score}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + score_text.get_width() // 2, 50 + score_text.get_height() // 2))
        shield_status = "Ready" if self.game.player.shieldReady else "Cooldown"
        shield_text = font.render(f"Shield: {shield_status}", True, (255, 255, 255))
        OutlinedText(f"Shield: {shield_status}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (10 + shield_text.get_width() // 2, 90 + shield_text.get_height() // 2))
        cooldown_ratio = self.game.player.getShieldCooldownRatio()
        pygame.draw.rect(self.game.screen, (255, 0, 0), (10, 130 * self.game.settings.UI_GAME_SCALE, 200 * self.game.settings.UI_GAME_SCALE, 15 * self.game.settings. UI_GAME_SCALE))
        pygame.draw.rect(self.game.screen, (0, 255, 0), (10, 130 * self.game.settings.UI_GAME_SCALE, 200 * cooldown_ratio * self.game.settings.UI_GAME_SCALE, 15 * self.game.settings.UI_GAME_SCALE))
        difficulty_text = font.render(f"Difficulty Scale: {math.floor(self.game.time_diff * 10)/10}x", True, (255, 255, 255))
        OutlinedText(f"Difficulty Scale: {math.floor(self.game.time_diff * 10)/10}x", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (self.game.screen.get_width() - difficulty_text.get_width() // 2 - 10, 10 + difficulty_text.get_height() // 2))
        asteroids_text = font.render(f"Asteroids: {len(self.game.asteroids)}", True, (255, 255, 255))
        OutlinedText(f"Asteroids: {len(self.game.asteroids)}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (self.game.screen.get_width() - asteroids_text.get_width() // 2 - 10, 50 + asteroids_text.get_height() // 2))
        ufos_text = font.render(f"UFOs: {len(self.game.ufos)}", True, (255, 255, 255))
        OutlinedText(f"UFOs: {len(self.game.ufos)}", font, (255, 255, 255), (0,0,0), 2, self.game.screen, (self.game.screen.get_width() - ufos_text.get_width() // 2 - 10, 90 + ufos_text.get_height() // 2))
class PauseMenuWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Resume Game","End Current Game", "Quit to Menu"]
    def draw(self, screen):
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        OutlinedText("Paused", font, (255, 255, 255), (0,0,0), 3, screen, (screen.get_width()//2, 100 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        longest_option_text = max([font.size(option)[0] for option in self.options])
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - longest_option_text // 2 - 20 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - longest_option_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - longest_option_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE))])
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
                pygame.mixer.music.stop()
                self.game.state = "game_over"
            elif self.selected_option == 2:
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
        surface = pygame.Surface((font.size("Settings")[0] + 40 * self.game.settings.UI_MENU_SCALE, font.size("Settings")[1] + 40 * self.game.settings.UI_MENU_SCALE))
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, surface.get_width(), surface.get_height()), 2)
        screen.blit(surface, (screen.get_width() // 2 - surface.get_width() // 2, 0))
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
            self.rewriteSettingsFile()
            self.game.state = "menu"
    def rewriteSettingsFile(self):
        with open("settings.py", "w") as f:
            f.write("class Settings:\n")
            for setting, value in self.settingsList.items():
                if isinstance(value, str):
                    f.write(f'    {setting} = "{value}"\n')
                else:
                    f.write(f'    {setting} = {value}\n')

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
                # for some reason the rounding has to be done twice like this otherwise it doesnt work when adding 0.1 to 0.7
                new_value = math.floor((current_value + change) * 100) /100
                new_value = math.floor((new_value) * 10)/10
            self.parent.settingsList[self.setting_name] = new_value
class ManualSelectionWidget:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.subwidget = None
        self.options = ["Menu Controls", "Settings Controls", "Gameplay Controls"]
    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.subwidget:
            self.subwidget.draw(screen)
            return
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        OutlinedText("Controls Manual Selection", font, (255, 255, 255), (0,0,0), 3, screen, (screen.get_width()//2, 100 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        longest_option_text = max([font.size(option)[0] for option in self.options])
        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected_option:
                color = (255, 0, 0)
                pygame.draw.polygon(screen, (255, 0, 0), [(screen.get_width() // 2 - longest_option_text // 2 - 20 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - longest_option_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 5 * self.game.settings.UI_MENU_SCALE)),
                                                          (screen.get_width() // 2 - longest_option_text // 2 - 40 * self.game.settings.UI_MENU_SCALE, (screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 15 * self.game.settings.UI_MENU_SCALE))])
            OutlinedText(option, font, color, (0,0,0), 2, screen, (screen.get_width() // 2, screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE + 10 * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if self.subwidget:
            self.subwidget.handle_event(event)
            return
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_BACKSPACE:
            self.game.state = "menu"
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option -1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option +1) %len(self.options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:
                self.subwidget = ControlsManualWidget(self.game, self, "menu")
            elif self.selected_option == 1:
                self.subwidget = ControlsManualWidget(self.game, self, "settings")
            elif self.selected_option == 2:
                self.subwidget = ControlsManualWidget(self.game, self, "gameplay")
class ControlsManualWidget:
    def __init__(self, game, parent, category):
        self.game = game
        self.parent = parent
        self.category = category
        self.controlsList = ["W / Up Arrow: Move Up",
                             "S / Down Arrow: Move Down",
                             "Enter / Space: Select Option",
                             "Backspace: Go Back",
                             "Escape: Quit Game"] if category == "menu" else None
        self.controlsList = ["W / Up Arrow: Move Up",
                             "S / Down Arrow: Move Down",
                             "Enter / Space: Select Option",
                             "Backspace: Go Back",
                             "Left Shift / Right Shift: Save Settings(On the Page with the settings listed)",
                             "Escape: Quit Game"] if category == "settings" else self.controlsList
        self.controlsList = ["W / Up Arrow: Move Up",
                             "A / Left Arrow: Angle Left",
                             "D / Right Arrow: Angle Right",
                             "Space / Left click: Shoot",
                             "S / Right Click / Right alt: Activate Shield",
                             "P : Pause Game",
                             "Escape: Quit Game"] if category == "gameplay" else self.controlsList
    def draw(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, int(74 * self.game.settings.UI_MENU_SCALE))
        OutlinedText(f"{self.category.capitalize()} Controls Manual", font, (255, 255, 255), (0,0,0), 3, screen, (screen.get_width()//2, 100 * self.game.settings.UI_MENU_SCALE))
        font = pygame.font.Font(None, int(36 * self.game.settings.UI_MENU_SCALE))
        for i, control in enumerate(self.controlsList):
            OutlinedText(control, font, (255, 255, 255), (0,0,0), 2, screen, (screen.get_width() // 2, screen.get_height() // 2 + i * 40 * self.game.settings.UI_MENU_SCALE))
    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_BACKSPACE:
            self.parent.subwidget = None