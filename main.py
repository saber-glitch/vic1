"""
CRIMSON NIGHT: VAMPIRE SURVIVORS
Main Game Entry Point and State Controller.
Features 4 playable characters with unique weapons/stats and Q-Dash mechanics.
"""

import sys
import math
import random
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BLACK
)
from sound import SoundManager
from sprites import SpriteManager
from particles import ParticleManager
from drops import DropManager
from enemies import EnemyManager
from player import Player
from ui import UIManager

# Game States
STATE_TITLE = "TITLE"
STATE_CHAR_SELECT = "CHAR_SELECT"
STATE_PLAYING = "PLAYING"
STATE_LEVEL_UP = "LEVEL_UP"
STATE_GAME_OVER = "GAME_OVER"
STATE_PAUSED = "PAUSED"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Systems
        self.sound_mgr = SoundManager()
        self.sprite_mgr = SpriteManager()
        self.particle_mgr = ParticleManager()
        self.ui_mgr = UIManager(self.sound_mgr, self.sprite_mgr)

        # Game State
        self.state = STATE_TITLE
        self.title_anim_timer = 0.0
        self.game_time = 0.0
        self.selected_character = "hunter"

        # Entities
        self.player = None
        self.drop_mgr = None
        self.enemy_mgr = None

        # Camera
        self.camera_x = 0.0
        self.camera_y = 0.0

    def start_new_game(self, character_key="hunter"):
        """Initializes a fresh game session with the chosen character."""
        self.selected_character = character_key
        self.game_time = 0.0
        self.particle_mgr = ParticleManager()
        self.player = Player(0, 0, self.sound_mgr, self.particle_mgr, self.sprite_mgr, character_key=character_key)
        self.drop_mgr = DropManager(self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        self.enemy_mgr = EnemyManager(self.sound_mgr, self.particle_mgr, self.sprite_mgr, self.drop_mgr)
        self.state = STATE_PLAYING
        self.sound_mgr.play("levelup")

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # Cap delta time to prevent tunneling

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                # Global mute toggle
                if event.key == pygame.K_m:
                    self.sound_mgr.toggle_mute()

                # Title Screen -> Character Select
                if self.state == STATE_TITLE:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = STATE_CHAR_SELECT
                        self.sound_mgr.play("click")

                # Character Selection Screen
                elif self.state == STATE_CHAR_SELECT:
                    char_keys = ["vampire", "gunslinger", "hunter", "mage"]
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.start_new_game("vampire")
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.start_new_game("gunslinger")
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        self.start_new_game("hunter")
                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        self.start_new_game("mage")
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.ui_mgr.selected_char_index = (self.ui_mgr.selected_char_index - 1) % 4
                        self.sound_mgr.play("click")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.ui_mgr.selected_char_index = (self.ui_mgr.selected_char_index + 1) % 4
                        self.sound_mgr.play("click")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_new_game(char_keys[self.ui_mgr.selected_char_index])
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_TITLE
                        self.sound_mgr.play("click")

                # Playing State
                elif self.state == STATE_PLAYING:
                    # Dash on Q key
                    if event.key == pygame.K_q and self.player:
                        self.player.trigger_dash()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                # Paused State
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING

                # Level Up Card Selection
                elif self.state == STATE_LEVEL_UP:
                    chosen = None
                    if event.key == pygame.K_1 and len(self.ui_mgr.current_choices) >= 1:
                        chosen = self.ui_mgr.current_choices[0]
                    elif event.key == pygame.K_2 and len(self.ui_mgr.current_choices) >= 2:
                        chosen = self.ui_mgr.current_choices[1]
                    elif event.key == pygame.K_3 and len(self.ui_mgr.current_choices) >= 3:
                        chosen = self.ui_mgr.current_choices[2]
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if 0 <= self.ui_mgr.selected_index < len(self.ui_mgr.current_choices):
                            chosen = self.ui_mgr.current_choices[self.ui_mgr.selected_index]
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.ui_mgr.selected_index = max(0, self.ui_mgr.selected_index - 1)
                        self.sound_mgr.play("click")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.ui_mgr.selected_index = min(len(self.ui_mgr.current_choices) - 1, self.ui_mgr.selected_index + 1)
                        self.sound_mgr.play("click")

                    if chosen:
                        self._apply_level_up_choice(chosen)

                # Game Over State
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.start_new_game(self.selected_character)
                    elif event.key in (pygame.K_c, pygame.K_SPACE):
                        self.state = STATE_CHAR_SELECT
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_TITLE

            # Mouse Click Handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == STATE_TITLE:
                    self.state = STATE_CHAR_SELECT
                    self.sound_mgr.play("click")
                elif self.state == STATE_CHAR_SELECT:
                    chosen_char = self.ui_mgr.handle_char_select_click(mouse_pos)
                    if chosen_char:
                        self.start_new_game(chosen_char)
                elif self.state == STATE_LEVEL_UP:
                    choice = self.ui_mgr.handle_level_up_click(mouse_pos)
                    if choice:
                        self._apply_level_up_choice(choice)
                elif self.state == STATE_GAME_OVER:
                    self.state = STATE_CHAR_SELECT

    def _apply_level_up_choice(self, choice):
        self.sound_mgr.play("click")
        if choice["type"] == "bonus":
            self.player.heal(100)
        else:
            self.player.apply_upgrade(choice["key"], choice["type"])

        # Check if more level-ups are queued
        if self.player.current_xp >= self.player.xp_to_next:
            self.player.current_xp -= self.player.xp_to_next
            self.player.level += 1
            self.player.xp_to_next = int(self.player.xp_to_next * 1.35)
            self.ui_mgr.generate_level_up_choices(self.player)
            self.sound_mgr.play("levelup")
        else:
            self.player.is_leveling_up = False
            self.state = STATE_PLAYING

    def _on_chest_opened(self):
        """Treasure Chest opened by player."""
        self.ui_mgr.generate_level_up_choices(self.player)
        self.state = STATE_LEVEL_UP

    def update(self, dt):
        if self.state in (STATE_TITLE, STATE_CHAR_SELECT):
            self.title_anim_timer += dt

        elif self.state == STATE_PLAYING:
            self.game_time += dt

            # Update entities
            self.player.update(dt, self.enemy_mgr.enemies, self.camera_x, self.camera_y)
            self.enemy_mgr.update(dt, self.player, self.game_time)
            self.drop_mgr.update(dt, self.player, self.enemy_mgr, self._on_chest_opened)
            self.particle_mgr.update(dt)

            # Check Level Up
            if self.player.is_leveling_up:
                self.ui_mgr.generate_level_up_choices(self.player)
                self.state = STATE_LEVEL_UP

            # Check Death
            if self.player.hp <= 0:
                self.state = STATE_GAME_OVER
                self.sound_mgr.play("player_hurt")
                self.particle_mgr.trigger_shake(14.0)

            # Smooth Camera following player with screen shake
            shake_x, shake_y = self.particle_mgr.get_shake_offset()
            target_cx = self.player.x - SCREEN_WIDTH // 2 + shake_x
            target_cy = self.player.y - SCREEN_HEIGHT // 2 + shake_y
            self.camera_x += (target_cx - self.camera_x) * 12.0 * dt
            self.camera_y += (target_cy - self.camera_y) * 12.0 * dt

    def draw_world_background(self):
        """Renders infinite repeating gothic cobblestone and graveyard props."""
        tile_size = 64
        start_col = int(self.camera_x // tile_size) - 1
        end_col = int((self.camera_x + SCREEN_WIDTH) // tile_size) + 1
        start_row = int(self.camera_y // tile_size) - 1
        end_row = int((self.camera_y + SCREEN_HEIGHT) // tile_size) + 1

        cobble_tile = self.sprite_mgr.get("tile_cobble")
        soil_tile = self.sprite_mgr.get("tile_soil")
        grave_prop = self.sprite_mgr.get("prop_gravestone")

        for col in range(start_col, end_col):
            for row in range(start_row, end_row):
                wx = col * tile_size
                wy = row * tile_size
                sx = int(wx - self.camera_x)
                sy = int(wy - self.camera_y)

                # Deterministic tile variation
                h = (col * 73856093 ^ row * 19349663) & 0xFFFFFF
                tile = cobble_tile if (h % 3 != 0) else soil_tile
                if tile:
                    self.screen.blit(tile, (sx, sy))

                # Occasional gravestone props
                if (h % 29) == 0 and grave_prop:
                    self.screen.blit(grave_prop, (sx + 16, sy + 14))

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == STATE_TITLE:
            self.ui_mgr.draw_title_screen(self.screen, self.title_anim_timer)

        elif self.state == STATE_CHAR_SELECT:
            self.ui_mgr.draw_char_select_screen(self.screen, mouse_pos, self.title_anim_timer)

        elif self.state in (STATE_PLAYING, STATE_LEVEL_UP, STATE_PAUSED, STATE_GAME_OVER):
            # 1. World Background
            self.draw_world_background()

            # 2. Pickups & Collectibles
            self.drop_mgr.draw(self.screen, self.camera_x, self.camera_y)

            # 3. Enemies
            self.enemy_mgr.draw(self.screen, self.camera_x, self.camera_y)

            # 4. Player & Weapons
            self.player.draw(self.screen, self.camera_x, self.camera_y)

            # 5. Particles, Damage text, and Screen Flash
            self.particle_mgr.draw(self.screen, self.camera_x, self.camera_y)

            # 6. HUD
            self.ui_mgr.draw_hud(
                self.screen, self.player, self.game_time, self.enemy_mgr.total_kills
            )

            # 7. Modals / Overlays
            if self.state == STATE_LEVEL_UP:
                self.ui_mgr.draw_level_up_modal(self.screen, mouse_pos)

            elif self.state == STATE_PAUSED:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((10, 8, 14, 180))
                self.screen.blit(overlay, (0, 0))
                p_surf = self.ui_mgr.font_header.render("PAUSED", True, (255, 205, 50))
                self.screen.blit(p_surf, (SCREEN_WIDTH // 2 - p_surf.get_width() // 2, 320))
                h_surf = self.ui_mgr.font_hud_sm.render("Press [ESC] to Resume", True, (245, 245, 250))
                self.screen.blit(h_surf, (SCREEN_WIDTH // 2 - h_surf.get_width() // 2, 380))

            elif self.state == STATE_GAME_OVER:
                self.ui_mgr.draw_game_over(
                    self.screen, self.game_time, self.enemy_mgr.total_kills, self.player.level
                )

            # 8. Mouse Aim Crosshair
            if self.state == STATE_PLAYING:
                mx, my = mouse_pos
                pygame.draw.circle(self.screen, (220, 40, 50), (mx, my), 9, 1)
                pygame.draw.circle(self.screen, (255, 205, 50), (mx, my), 2)
                pygame.draw.line(self.screen, (220, 40, 50), (mx - 13, my), (mx - 4, my), 1)
                pygame.draw.line(self.screen, (220, 40, 50), (mx + 4, my), (mx + 13, my), 1)
                pygame.draw.line(self.screen, (220, 40, 50), (mx, my - 13), (mx, my - 4), 1)
                pygame.draw.line(self.screen, (220, 40, 50), (mx, my + 4), (mx, my + 13), 1)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
