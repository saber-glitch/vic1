"""
Pickups and Collectibles for Crimson Night:
XP Gems, Roast Meat, Vacuum Magnets, Rosary Bombs, and Treasure Chests.
"""

import math
import random
import pygame
from settings import COLOR_CYAN, COLOR_GOLD, COLOR_WHITE

class Drop:
    """Base class for dropped ground items."""
    def __init__(self, x, y, drop_type, value=1):
        self.x = x
        self.y = y
        self.drop_type = drop_type
        self.value = value
        self.is_attracted = False
        self.vx = 0.0
        self.vy = 0.0
        self.bob_timer = random.uniform(0, math.pi * 2)

    def update(self, dt, player):
        self.bob_timer += dt * 4.0
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        # Check magnet attraction trigger
        if not self.is_attracted and dist <= player.magnet_radius:
            self.is_attracted = True

        # If attracted, fly towards player
        if self.is_attracted:
            if dist > 0.001:
                speed = max(380.0, 750.0 - dist * 0.4)
                self.vx = (dx / dist) * speed
                self.vy = (dy / dist) * speed
                self.x += self.vx * dt
                self.y += self.vy * dt
            # Collect threshold
            if dist < 18:
                return True  # Collected!
        return False

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        bob_y = math.sin(self.bob_timer) * 2.0
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y + bob_y)

        # Select sprite based on type
        if self.drop_type == "gem":
            if self.value >= 100:
                spr = sprite_mgr.get("gem_gold")
            elif self.value >= 25:
                spr = sprite_mgr.get("gem_red")
            elif self.value >= 5:
                spr = sprite_mgr.get("gem_green")
            else:
                spr = sprite_mgr.get("gem_blue")
        elif self.drop_type == "meat":
            spr = sprite_mgr.get("drop_meat")
        elif self.drop_type == "magnet":
            spr = sprite_mgr.get("drop_magnet")
        elif self.drop_type == "rosary":
            spr = sprite_mgr.get("drop_rosary")
        elif self.drop_type == "chest":
            spr = sprite_mgr.get("drop_chest")
        else:
            spr = sprite_mgr.get("gem_blue")

        if spr:
            surface.blit(spr, (sx - spr.get_width() // 2, sy - spr.get_height() // 2))


class DropManager:
    """Manages spawning, updating, and collecting ground drops."""
    def __init__(self, sound_mgr, particle_mgr, sprite_mgr):
        self.drops = []
        self.sound_mgr = sound_mgr
        self.particle_mgr = particle_mgr
        self.sprite_mgr = sprite_mgr

    def spawn_gem(self, x, y, value=1):
        self.drops.append(Drop(x, y, "gem", value))

    def spawn_meat(self, x, y, heal_amount=30):
        self.drops.append(Drop(x, y, "meat", heal_amount))

    def spawn_magnet(self, x, y):
        self.drops.append(Drop(x, y, "magnet", 0))

    def spawn_rosary(self, x, y):
        self.drops.append(Drop(x, y, "rosary", 0))

    def spawn_chest(self, x, y):
        self.drops.append(Drop(x, y, "chest", 0))

    def attract_all_gems(self):
        """Vacuum effect: pulls all gems towards player."""
        for d in self.drops:
            if d.drop_type == "gem":
                d.is_attracted = True

    def update(self, dt, player, enemy_mgr, on_chest_opened_callback):
        retained = []
        for drop in self.drops:
            collected = drop.update(dt, player)
            if collected:
                self._handle_collection(drop, player, enemy_mgr, on_chest_opened_callback)
            else:
                retained.append(drop)
        self.drops = retained

    def _handle_collection(self, drop, player, enemy_mgr, on_chest_opened_callback):
        if drop.drop_type == "gem":
            actual_xp = int(drop.value * player.xp_multiplier)
            player.add_xp(actual_xp)
            self.sound_mgr.play("gem")
            self.particle_mgr.spawn_spark_burst(drop.x, drop.y, COLOR_CYAN, count=4)

        elif drop.drop_type == "meat":
            healed = player.heal(drop.value)
            self.sound_mgr.play("gem")
            self.particle_mgr.add_damage_number(player.x, player.y - 20, healed, is_heal=True)

        elif drop.drop_type == "magnet":
            self.attract_all_gems()
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_flash(COLOR_CYAN, initial_alpha=120)

        elif drop.drop_type == "rosary":
            self.sound_mgr.play("rosary")
            self.particle_mgr.trigger_flash(COLOR_WHITE, initial_alpha=240)
            self.particle_mgr.trigger_shake(12.0)
            enemy_mgr.kill_all_visible(self)

        elif drop.drop_type == "chest":
            self.sound_mgr.play("chest")
            self.particle_mgr.trigger_flash(COLOR_GOLD, initial_alpha=200)
            self.particle_mgr.trigger_shake(8.0)
            if on_chest_opened_callback:
                on_chest_opened_callback()

    def draw(self, surface, camera_x, camera_y):
        for drop in self.drops:
            drop.draw(surface, camera_x, camera_y, self.sprite_mgr)
