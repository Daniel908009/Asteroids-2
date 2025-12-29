import pygame
from entities.player import Player
from utilities.widgets import StartMenuWidget, GameOverWidget, HighScoresWidget, GameHUD, PauseMenuWidget, SettingsWidget
from utilities.spawner import Spawner
from entities.explosionEffect import ExplosionEffect
from settings import Settings
import json
import random

class Game:
    def __init__(self):
        self.state = "menu"
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(pygame.image.load("Assets/spaceship_thrust.png"))
        self.score = 0
        self.player = Player((self.screen.get_width() // 2, self.screen.get_height() // 2), self)
        self.running = True
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.asteroids = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.laserBullets = pygame.sprite.Group()
        self.startMenu = StartMenuWidget(self)
        self.gameOverMenu = GameOverWidget(self)
        self.highScoresMenu = HighScoresWidget(self)
        self.spawner = Spawner(self, ufoGroup=self.ufos, asteroidGroup=self.asteroids, allSpritesGroup=self.all_sprites)
        self.game_hud = GameHUD(self)
        self.paused_menu = PauseMenuWidget(self)
        self.settings_menu = SettingsWidget(self)
        self.player_name = ""
        pygame.mixer.set_num_channels(32)
        self.gameMusicList = ["Assets/music1.mp3","Assets/music2.mp3","Assets/music3.mp3"]
        random.shuffle(self.gameMusicList)
        self.menuMusicList = ["Assets/menu_music_1.mp3","Assets/menu_music_2.mp3","Assets/menu_music_3.mp3","Assets/menu_music_4.mp3", "Assets/menu_music_5.mp3"]
        random.shuffle(self.menuMusicList)
        self.currentGameMusic = 0
        self.currentMenuMusic = 0
    def run(self):
        while self.running:
            dt = self.clock.tick(self.settings.FPS) / 1000
            self.handleInputs()
            pygame.display.flip()
            if self.state == "menu":
                self.startMenu.draw(self.screen)
                self.startMenu.update(dt)
                if not pygame.mixer.music.get_busy() and self.state == "menu" and self.settings.MUSIC_ON:
                    pygame.mixer.music.set_volume(self.settings.MUSIC_VOLUME)
                    pygame.mixer.music.load(self.menuMusicList[self.currentMenuMusic])
                    pygame.mixer.music.play()
                    self.currentMenuMusic = (self.currentMenuMusic + 1) % len(self.menuMusicList)
                    if self.currentMenuMusic == len(self.menuMusicList):
                        currentlyPlayingName = self.menuMusicList[self.currentMenuMusic -1]
                        self.currentMenuMusic = 0
                        while True:
                            random.shuffle(self.menuMusicList)
                            if currentlyPlayingName != self.menuMusicList[0]:
                                break
            elif self.state == "playing":
                self.play_game(dt)
                self.update(dt)
                if not pygame.mixer.music.get_busy() and self.state == "playing" and self.settings.MUSIC_ON:
                    pygame.mixer.music.set_volume(self.settings.MUSIC_VOLUME)
                    pygame.mixer.music.load(self.gameMusicList[self.currentGameMusic])
                    pygame.mixer.music.play()
                    self.currentGameMusic = (self.currentGameMusic + 1) % len(self.gameMusicList)
                    if self.currentGameMusic == len(self.gameMusicList):
                        currentlyPlayingName = self.gameMusicList[self.currentGameMusic -1]
                        self.currentGameMusic = 0
                        while True:
                            random.shuffle(self.gameMusicList)
                            if currentlyPlayingName != self.gameMusicList[0]:
                                break
                if not self.settings.SOUND_ON:
                    for channel in range(pygame.mixer.get_num_channels()):
                        pygame.mixer.Channel(channel).set_volume(0)
                else:
                    for channel in range(pygame.mixer.get_num_channels()):
                        pygame.mixer.Channel(channel).set_volume(self.settings.SOUND_VOLUME)
            elif self.state == "high_scores":
                self.highScoresMenu.draw(self.screen)
            elif self.state == "game_over":
                self.gameOverMenu.draw(self.screen)
            elif self.state == "paused":
                self.screen.fill((0, 0, 0))
                self.all_sprites.draw(self.screen)
                self.paused_menu.draw(self.screen)
            elif self.state == "settings":
                self.settings_menu.draw(self.screen)
                
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
                    elif event.key == pygame.K_s or event.key == pygame.K_RALT:
                        self.player.shieldUp()
                    elif event.key == pygame.K_p:
                        pygame.mixer.music.pause()
                        for channel in range(pygame.mixer.get_num_channels()):
                            pygame.mixer.Channel(channel).pause()
                        self.state = "paused"
                elif self.state == "game_over":
                    self.gameOverMenu.handle_event(event)
                elif self.state == "high_scores":
                    self.highScoresMenu.handle_event(event)
                elif self.state == "paused":
                    self.paused_menu.handle_event(event)
                elif self.state == "settings":
                    self.settings_menu.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "playing":
                if event.button == 1:
                    self.player.shoot()
                if event.button == 3:
                    self.player.shieldUp()
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
        everything_hits = pygame.sprite.spritecollide(self.player, self.all_sprites, False)
        for hit in everything_hits:
            if hit != self.player:
                if hit in self.asteroids:
                    self.score += hit.score_value
                    position = (self.player.pos.x, self.player.pos.y)
                    exp = ExplosionEffect(self, "player", position, self.player.rect.width//2, pygame.mixer.Sound("Assets/explosion.wav"))
                    self.all_sprites.add(exp)
                    self.asteroids.remove(hit)
                    self.all_sprites.remove(hit)
                    hit.kill()
                    self.player.reduceHealth(hit.damage, pygame.mixer.Sound("Assets/ship_impact.mp3"))
                elif hit in self.ufos:
                    self.score += hit.score_value
                    position = (self.player.pos.x, self.player.pos.y)
                    exp = ExplosionEffect(self, "player", position, hit.rect.width//2, pygame.mixer.Sound("Assets/explosion2.wav"))
                    self.all_sprites.add(exp)
                    self.ufos.remove(hit)
                    self.all_sprites.remove(hit)
                    hit.kill()
                    self.player.reduceHealth(hit.damage, pygame.mixer.Sound("Assets/ship_impact.mp3"))
        for ufo in self.ufos:
            ufo_hits = pygame.sprite.spritecollide(ufo, self.asteroids, False)
            for hit in ufo_hits:
                position = (ufo.position.x, ufo.position.y)
                exp = ExplosionEffect(self, "ufo", position, ufo.rect.width//2, pygame.mixer.Sound("Assets/explosion2.wav"))
                self.all_sprites.add(exp)
                self.ufos.remove(ufo)
                self.all_sprites.remove(ufo)
                ufo.kill()
                self.all_sprites.remove(hit)
                self.asteroids.remove(hit)
                hit.inheritanceSplit()
                hit.kill()
        for bullet in self.laserBullets:
            all_hits = pygame.sprite.spritecollide(bullet, self.all_sprites, False)
            for hit in all_hits:
                if hit != bullet and hit != bullet.owner:
                    if hit in self.asteroids:
                        if bullet.owner == self.player:
                            self.score += hit.score_value
                        position = (bullet.pos.x, bullet.pos.y)
                        exp = ExplosionEffect(self, "asteroid", position, hit.rect.width//2, pygame.mixer.Sound("Assets/explosion.wav"))
                        self.all_sprites.add(exp)
                        hit.inheritanceSplit()
                        self.asteroids.remove(hit)
                        self.all_sprites.remove(hit)
                        hit.kill()
                        self.laserBullets.remove(bullet)
                        self.all_sprites.remove(bullet)
                        bullet.kill()
                    elif hit in self.ufos:
                        if bullet.owner == self.player:
                            self.score += hit.score_value
                        position = (bullet.pos.x, bullet.pos.y)
                        exp = ExplosionEffect(self, "ufo", position, hit.rect.width//2, pygame.mixer.Sound("Assets/explosion2.wav"))
                        self.all_sprites.add(exp)
                        self.ufos.remove(hit)
                        self.all_sprites.remove(hit)
                        hit.kill()
                        self.laserBullets.remove(bullet)
                        self.all_sprites.remove(bullet)
                        bullet.kill()
                    elif hit == self.player:
                        self.laserBullets.remove(bullet)
                        self.all_sprites.remove(bullet)
                        bullet.kill()
                        self.player.reduceHealth(1, pygame.mixer.Sound("Assets/ship_impact.mp3"))
                        exp = ExplosionEffect(self, "player", (self.player.pos.x, self.player.pos.y), self.player.rect.width//2, None)
                        self.all_sprites.add(exp)
    def reset(self):
        pass
    def save_high_score(self, name, score):
        name = name.strip()
        if not name:
            name = "No Name"
        with open("high_scores.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append({"name": name, "score": score})
            file.close()
        with open("high_scores.json", "w") as file:
            json.dump(data, file)
            file.close()
    def load_high_scores(self):
        high_scores = []
        try:
            with open("high_scores.json", "r") as file:
                data = json.load(file)
                processed_data = []
                for entry in data:
                    processed_data.append((entry["name"], entry["score"]))
                high_scores = sorted(processed_data, key=lambda x: x[1], reverse=True)[:10]
                file.close()
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return high_scores