"""
Enemies and Wave Spawner for Crimson Night:
Bats, Skeletons, Zombies, Wraiths, Gargoyles, Phantom Knights, Hellhounds,
Necromancers, Banshees, Crawlers, Blood Golems, Vampire Lord & Death Reaper Bosses.
"""

import math
import random
import pygame
from settings import (
    COLOR_RED, COLOR_WHITE, COLOR_GOLD, COLOR_PURPLE,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Enemy:
    """Base class for all monster types."""
    def __init__(self, x, y, enemy_type, hp, speed, damage, xp_val, radius):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.xp_val = xp_val
        self.radius = radius
        self.is_dead = False
        self.is_boss = False

        # Physics & Hitbox
        self.vx = 0.0
        self.vy = 0.0
        self.knockback_x = 0.0
        self.knockback_y = 0.0

        # Animation & Visuals
        self.anim_timer = random.uniform(0.0, 10.0)
        self.flash_timer = 0.0
        self.facing_right = True

    def get_hitbox(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2)
        )

    def take_damage(self, amount, knockback_x=0.0, knockback_y=0.0):
        self.hp -= amount
        self.flash_timer = 0.08  # Flash white for 80ms
        self.knockback_x += knockback_x
        self.knockback_y += knockback_y
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True

    def update(self, dt, player):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Direction vector towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dx != 0:
            self.facing_right = dx > 0

        # Base chase movement
        if dist > 1.0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0.0
            self.vy = 0.0

        # Decay knockback
        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        # Check contact damage against player
        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)

        # Retrieve animation frames
        frames = sprite_mgr.get(f"enemy_{self.enemy_type}")
        if not frames:
            # Fallback circle if missing
            pygame.draw.circle(surface, COLOR_RED, (sx, sy), self.radius)
            return

        frame_idx = int(self.anim_timer * 6.0) % len(frames)
        spr = frames[frame_idx]

        # Flip if facing left
        if not self.facing_right:
            spr = pygame.transform.flip(spr, True, False)

        # White flash when damaged
        if self.flash_timer > 0:
            flash_surf = spr.copy()
            flash_surf.fill((255, 255, 255, 200), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(flash_surf, (sx - spr.get_width() // 2, sy - spr.get_height() // 2))
        else:
            surface.blit(spr, (sx - spr.get_width() // 2, sy - spr.get_height() // 2))


# =========================================================
# BASIC ENEMIES
# =========================================================

class BatEnemy(Enemy):
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "bat", int(14 * hp_scale), 185.0, 10.0, xp_val=1, radius=10)


class SkeletonEnemy(Enemy):
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "skeleton", int(40 * hp_scale), 115.0, 14.0, xp_val=2, radius=12)


class ZombieEnemy(Enemy):
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "zombie", int(95 * hp_scale), 80.0, 18.0, xp_val=5, radius=14)


class WraithEnemy(Enemy):
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "wraith", int(65 * hp_scale), 140.0, 16.0, xp_val=6, radius=13)
        self.sway_timer = random.uniform(0, 10)

    def update(self, dt, player):
        self.sway_timer += dt * 4.0
        # Add perpendicular sway
        super().update(dt, player)
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1.0, math.hypot(dx, dy))
        perp_x = -dy / dist
        perp_y = dx / dist
        sway = math.sin(self.sway_timer) * 45.0
        self.x += perp_x * sway * dt
        self.y += perp_y * sway * dt


class GargoyleEnemy(Enemy):
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "gargoyle", int(210 * hp_scale), 105.0, 24.0, xp_val=15, radius=18)


# =========================================================
# NEW ENEMIES
# =========================================================

class PhantomKnightEnemy(Enemy):
    """Ghostly armored knight that periodically charges at the player."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "phantom_knight", int(150 * hp_scale), 95.0, 22.0, xp_val=10, radius=16)
        self.charge_timer = random.uniform(2.0, 5.0)
        self.charge_duration = 0.0
        self.charge_dx = 0.0
        self.charge_dy = 0.0

    def update(self, dt, player):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dx != 0:
            self.facing_right = dx > 0

        # Charge logic
        self.charge_timer -= dt
        if self.charge_duration > 0:
            # Currently charging
            self.charge_duration -= dt
            self.vx = self.charge_dx * self.speed * 3.0
            self.vy = self.charge_dy * self.speed * 3.0
        elif self.charge_timer <= 0:
            # Start a new charge
            self.charge_timer = random.uniform(3.0, 5.0)
            self.charge_duration = 0.3
            if dist > 1.0:
                self.charge_dx = dx / dist
                self.charge_dy = dy / dist
            else:
                self.charge_dx = 0.0
                self.charge_dy = 0.0
        else:
            # Normal chase
            if dist > 1.0:
                self.vx = (dx / dist) * self.speed
                self.vy = (dy / dist) * self.speed
            else:
                self.vx = 0.0
                self.vy = 0.0

        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)


class HellhoundEnemy(Enemy):
    """Fiery demon dog - gets faster when close to player."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "hellhound", int(55 * hp_scale), 210.0, 15.0, xp_val=4, radius=14)

    def update(self, dt, player):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dx != 0:
            self.facing_right = dx > 0

        # Speed boost when close
        speed = self.speed * 1.4 if dist < 150 else self.speed

        if dist > 1.0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)


class NecromancerEnemy(Enemy):
    """Dark caster that stays at range and damages from afar."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "necromancer", int(120 * hp_scale), 60.0, 12.0, xp_val=12, radius=14)
        self.ranged_tick = 0.0

    def update(self, dt, player):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dx != 0:
            self.facing_right = dx > 0

        # Stay at ~250px distance - approach if far, retreat if too close
        if dist > 300:
            # Move towards player
            if dist > 1.0:
                self.vx = (dx / dist) * self.speed
                self.vy = (dy / dist) * self.speed
        elif dist < 180:
            # Back away
            if dist > 1.0:
                self.vx = -(dx / dist) * self.speed * 0.8
                self.vy = -(dy / dist) * self.speed * 0.8
        else:
            # Strafe sideways
            if dist > 1.0:
                self.vx = (-dy / dist) * self.speed * 0.4
                self.vy = (dx / dist) * self.speed * 0.4

        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        # Ranged damage tick every 1.5 seconds if within 300px
        self.ranged_tick += dt
        if self.ranged_tick >= 1.5 and dist < 300:
            self.ranged_tick = 0.0
            player.take_damage(self.damage * 0.5)

        # Still does contact damage
        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)


class BansheeEnemy(Enemy):
    """Screaming ghost with zigzag movement pattern."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "banshee", int(45 * hp_scale), 175.0, 20.0, xp_val=7, radius=13)
        self.zigzag_timer = random.uniform(0, 10)

    def update(self, dt, player):
        self.anim_timer += dt
        self.zigzag_timer += dt * 6.0
        if self.flash_timer > 0:
            self.flash_timer -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dx != 0:
            self.facing_right = dx > 0

        if dist > 1.0:
            # Base direction towards player
            base_vx = (dx / dist) * self.speed
            base_vy = (dy / dist) * self.speed
            # Add strong zigzag perpendicular movement
            perp_x = -dy / dist
            perp_y = dx / dist
            zigzag = math.sin(self.zigzag_timer) * 120.0
            self.vx = base_vx + perp_x * zigzag
            self.vy = base_vy + perp_y * zigzag
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)


class CrawlerEnemy(Enemy):
    """Fast spider creature - low HP but ultra fast, swarms in groups."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "crawler", int(30 * hp_scale), 230.0, 8.0, xp_val=2, radius=10)


class BloodGolemEnemy(Enemy):
    """Massive blood construct - very tanky, splits into crawlers on death."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "blood_golem", int(350 * hp_scale), 55.0, 30.0, xp_val=25, radius=20)
        self.spawns_on_death = True  # Flag for EnemyManager to check


# =========================================================
# BOSSES
# =========================================================

class VampireBoss(Enemy):
    """Mini-Boss and Major Boss with massive HP and drops Treasure Chest."""
    def __init__(self, x, y, hp_scale=1.0):
        super().__init__(x, y, "vampire_boss", int(1200 * hp_scale), 125.0, 32.0, xp_val=100, radius=26)
        self.is_boss = True
        self.roar_timer = 0.0

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        super().draw(surface, camera_x, camera_y, sprite_mgr)
        # Boss Health Bar above head
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y - 42)
        bw = 64
        bh = 7
        pct = max(0.0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (20, 20, 20), (sx - bw // 2, sy, bw, bh), border_radius=2)
        pygame.draw.rect(surface, COLOR_RED, (sx - bw // 2 + 1, sy + 1, int((bw - 2) * pct), bh - 2), border_radius=1)
        pygame.draw.rect(surface, COLOR_GOLD, (sx - bw // 2, sy, bw, bh), 1, border_radius=2)


class DeathReaperBoss(Enemy):
    """MEGA BOSS - The Death Reaper with 50x normal enemy HP.
    Has soul wave attack, periodic speed bursts, and a massive health bar."""
    def __init__(self, x, y, hp_scale=1.0):
        # 50x a normal enemy (~95 HP) = 4750 base HP
        super().__init__(x, y, "death_reaper", int(4750 * hp_scale), 90.0, 45.0, xp_val=500, radius=30)
        self.is_boss = True
        self.soul_wave_timer = 5.0
        self.speed_burst_timer = 8.0
        self.speed_burst_duration = 0.0
        self.base_speed = 90.0

    def update(self, dt, player):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dx != 0:
            self.facing_right = dx > 0

        # Speed burst logic - every 8s, burst for 1s at 2.5x speed
        self.speed_burst_timer -= dt
        if self.speed_burst_duration > 0:
            self.speed_burst_duration -= dt
            current_speed = self.base_speed * 2.5
        elif self.speed_burst_timer <= 0:
            self.speed_burst_timer = 8.0
            self.speed_burst_duration = 1.0
            current_speed = self.base_speed * 2.5
        else:
            current_speed = self.base_speed

        if dist > 1.0:
            self.vx = (dx / dist) * current_speed
            self.vy = (dy / dist) * current_speed
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.x += (self.vx + self.knockback_x) * dt
        self.y += (self.vy + self.knockback_y) * dt
        self.knockback_x *= (1.0 - 6.0 * dt)
        self.knockback_y *= (1.0 - 6.0 * dt)

        # Soul wave attack every 5 seconds - damages player within 200px
        self.soul_wave_timer -= dt
        if self.soul_wave_timer <= 0:
            self.soul_wave_timer = 5.0
            if dist < 200:
                player.take_damage(15.0)

        # Contact damage
        if dist <= (self.radius + player.radius):
            player.take_damage(self.damage * dt)

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        super().draw(surface, camera_x, camera_y, sprite_mgr)

        # Soul wave visual pulse (purple ring when timer is low)
        if self.soul_wave_timer < 1.0:
            sx = int(self.x - camera_x)
            sy = int(self.y - camera_y)
            pulse_r = int(200 * (1.0 - self.soul_wave_timer))
            alpha = int(80 * self.soul_wave_timer)
            pulse_surf = pygame.Surface((pulse_r * 2, pulse_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(pulse_surf, (*COLOR_PURPLE[:3], alpha), (pulse_r, pulse_r), pulse_r, 3)
            surface.blit(pulse_surf, (sx - pulse_r, sy - pulse_r))

        # Large Boss Health Bar
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y - 52)
        bw = 80
        bh = 8
        pct = max(0.0, self.hp / self.max_hp)
        # Background
        pygame.draw.rect(surface, (20, 20, 20), (sx - bw // 2, sy, bw, bh), border_radius=2)
        # HP fill (gradient from red to purple based on HP)
        fill_w = int((bw - 2) * pct)
        if fill_w > 0:
            pygame.draw.rect(surface, COLOR_PURPLE, (sx - bw // 2 + 1, sy + 1, fill_w, bh - 2), border_radius=1)
        # Gold border
        pygame.draw.rect(surface, COLOR_GOLD, (sx - bw // 2, sy, bw, bh), 1, border_radius=2)
        # Boss name label
        font = pygame.font.Font(None, 16)
        name_surf = font.render("DEATH REAPER", True, COLOR_GOLD)
        surface.blit(name_surf, (sx - name_surf.get_width() // 2, sy - 12))


# =========================================================
# ENEMY MANAGER (Wave Spawner & Director)
# =========================================================

class EnemyManager:
    """Handles spawning waves, enemy crowds, collision separation, and drops."""
    def __init__(self, sound_mgr, particle_mgr, sprite_mgr, drop_mgr):
        self.enemies = []
        self.sound_mgr = sound_mgr
        self.particle_mgr = particle_mgr
        self.sprite_mgr = sprite_mgr
        self.drop_mgr = drop_mgr

        self.spawn_timer = 0.0
        self.swarm_event_timer = 90.0  # triggers every 90s
        self.boss_spawned_2min = False
        self.boss_spawned_5min = False
        self.boss_spawned_10min = False
        self.boss_spawned_15min = False
        self.total_kills = 0

    def get_random_spawn_pos(self, player):
        """Pick a point just offscreen around the player."""
        margin = 100
        side = random.choice(["top", "bottom", "left", "right"])
        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2

        if side == "top":
            x = player.x + random.uniform(-half_w - margin, half_w + margin)
            y = player.y - half_h - margin
        elif side == "bottom":
            x = player.x + random.uniform(-half_w - margin, half_w + margin)
            y = player.y + half_h + margin
        elif side == "left":
            x = player.x - half_w - margin
            y = player.y + random.uniform(-half_h - margin, half_h + margin)
        else:
            x = player.x + half_w + margin
            y = player.y + random.uniform(-half_h - margin, half_h + margin)
        return x, y

    def spawn_circle_swarm(self, player, count=35):
        """Event: Swarm of bats encircles player from all sides."""
        self.sound_mgr.play("rosary")
        self.particle_mgr.trigger_flash(COLOR_RED, initial_alpha=100)
        radius = 550.0
        for i in range(count):
            ang = i * (2 * math.pi / count)
            sx = player.x + math.cos(ang) * radius
            sy = player.y + math.sin(ang) * radius
            self.enemies.append(BatEnemy(sx, sy, hp_scale=0.85))

    def _spawn_enemy_for_phase(self, sx, sy, hp_scale, game_time):
        """Pick an enemy type based on current game phase."""
        r = random.random()

        if game_time < 60:
            # Early game: Bats, Skeletons, Crawlers
            if r < 0.40:
                return BatEnemy(sx, sy, hp_scale)
            elif r < 0.70:
                return SkeletonEnemy(sx, sy, hp_scale)
            else:
                return CrawlerEnemy(sx, sy, hp_scale)

        elif game_time < 180:
            # Mid-early: Add Zombies and Hellhounds
            if r < 0.20:
                return BatEnemy(sx, sy, hp_scale)
            elif r < 0.45:
                return SkeletonEnemy(sx, sy, hp_scale)
            elif r < 0.65:
                return ZombieEnemy(sx, sy, hp_scale)
            elif r < 0.85:
                return HellhoundEnemy(sx, sy, hp_scale)
            else:
                return CrawlerEnemy(sx, sy, hp_scale)

        elif game_time < 300:
            # Mid-game: Full roster minus Blood Golems
            if r < 0.12:
                return SkeletonEnemy(sx, sy, hp_scale)
            elif r < 0.24:
                return ZombieEnemy(sx, sy, hp_scale)
            elif r < 0.38:
                return WraithEnemy(sx, sy, hp_scale)
            elif r < 0.52:
                return HellhoundEnemy(sx, sy, hp_scale)
            elif r < 0.66:
                return PhantomKnightEnemy(sx, sy, hp_scale)
            elif r < 0.78:
                return BansheeEnemy(sx, sy, hp_scale)
            elif r < 0.90:
                return NecromancerEnemy(sx, sy, hp_scale)
            else:
                return CrawlerEnemy(sx, sy, hp_scale)

        else:
            # Late game: Everything including Blood Golems and Gargoyles
            if r < 0.10:
                return ZombieEnemy(sx, sy, hp_scale)
            elif r < 0.22:
                return WraithEnemy(sx, sy, hp_scale)
            elif r < 0.34:
                return GargoyleEnemy(sx, sy, hp_scale)
            elif r < 0.48:
                return PhantomKnightEnemy(sx, sy, hp_scale)
            elif r < 0.58:
                return BansheeEnemy(sx, sy, hp_scale)
            elif r < 0.68:
                return NecromancerEnemy(sx, sy, hp_scale)
            elif r < 0.78:
                return BloodGolemEnemy(sx, sy, hp_scale)
            elif r < 0.88:
                return HellhoundEnemy(sx, sy, hp_scale)
            else:
                return BatEnemy(sx, sy, hp_scale * 1.5)

    def update(self, dt, player, game_time):
        # 1. Update Spawning Director based on run time
        self.spawn_timer += dt
        spawn_interval = max(0.22, 1.2 - (game_time / 300.0) * 0.9)
        hp_scale = 1.0 + (game_time / 180.0) * 0.85

        # ---- Boss Milestones ----
        # 2 min: Vampire Boss
        if game_time >= 120.0 and not self.boss_spawned_2min:
            self.boss_spawned_2min = True
            bx, by = self.get_random_spawn_pos(player)
            self.enemies.append(VampireBoss(bx, by, hp_scale=1.0))
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_shake(10.0)
            self.particle_mgr.trigger_flash(COLOR_RED, initial_alpha=160)

        # 5 min: Stronger Vampire Boss
        if game_time >= 300.0 and not self.boss_spawned_5min:
            self.boss_spawned_5min = True
            bx, by = self.get_random_spawn_pos(player)
            self.enemies.append(VampireBoss(bx, by, hp_scale=2.2))
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_shake(12.0)
            self.particle_mgr.trigger_flash(COLOR_RED, initial_alpha=180)

        # 10 min: DEATH REAPER MEGA BOSS
        if game_time >= 600.0 and not self.boss_spawned_10min:
            self.boss_spawned_10min = True
            bx, by = self.get_random_spawn_pos(player)
            self.enemies.append(DeathReaperBoss(bx, by, hp_scale=1.0))
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_shake(16.0)
            self.particle_mgr.trigger_flash(COLOR_PURPLE, initial_alpha=200)

        # 15 min: Scaled DEATH REAPER
        if game_time >= 900.0 and not self.boss_spawned_15min:
            self.boss_spawned_15min = True
            bx, by = self.get_random_spawn_pos(player)
            self.enemies.append(DeathReaperBoss(bx, by, hp_scale=2.0))
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_shake(20.0)
            self.particle_mgr.trigger_flash(COLOR_PURPLE, initial_alpha=220)

        # Swarm events every 75-90s
        self.swarm_event_timer -= dt
        if self.swarm_event_timer <= 0:
            self.swarm_event_timer = 85.0
            self.spawn_circle_swarm(player, count=40)

        # Regular Wave Spawning
        max_enemies = min(300, 45 + int(game_time * 0.6))
        if self.spawn_timer >= spawn_interval and len(self.enemies) < max_enemies:
            self.spawn_timer = 0.0
            sx, sy = self.get_random_spawn_pos(player)
            e = self._spawn_enemy_for_phase(sx, sy, hp_scale, game_time)
            self.enemies.append(e)

        # 2. Update and Separate Enemies
        retained = []
        new_spawns = []  # For Blood Golem death splits
        for e in self.enemies:
            e.update(dt, player)
            if e.is_dead:
                self.total_kills += 1
                self.particle_mgr.spawn_blood_burst(e.x, e.y, count=8)

                # Blood Golem splits into 2 Crawlers on death
                if hasattr(e, 'spawns_on_death') and e.spawns_on_death:
                    for offset in [(-15, 0), (15, 0)]:
                        crawler = CrawlerEnemy(e.x + offset[0], e.y + offset[1], hp_scale=1.0)
                        new_spawns.append(crawler)
                    self.particle_mgr.spawn_blood_burst(e.x, e.y, count=14)

                # Drops
                if e.is_boss:
                    self.drop_mgr.spawn_chest(e.x, e.y)
                    self.drop_mgr.spawn_gem(e.x, e.y, value=e.xp_val)
                else:
                    self.drop_mgr.spawn_gem(e.x, e.y, value=e.xp_val)
                    # Special drop chances
                    drop_roll = random.random()
                    if drop_roll < 0.025:
                        self.drop_mgr.spawn_meat(e.x, e.y, 35)
                    elif drop_roll < 0.035:
                        self.drop_mgr.spawn_magnet(e.x, e.y)
                    elif drop_roll < 0.040:
                        self.drop_mgr.spawn_rosary(e.x, e.y)
            else:
                # Remove if drifted absurdly far away (> 1600 px) to prevent memory leak
                if math.hypot(e.x - player.x, e.y - player.y) < 1700:
                    retained.append(e)

        # Add any spawned enemies from Blood Golem splits
        retained.extend(new_spawns)
        self.enemies = retained

        # 3. Soft Flocking / Separation (avoids 100% clump)
        # Check against a small subset for efficiency
        for i in range(len(self.enemies)):
            e1 = self.enemies[i]
            # check next 3 neighbours in list
            for j in range(i + 1, min(i + 5, len(self.enemies))):
                e2 = self.enemies[j]
                dx = e2.x - e1.x
                dy = e2.y - e1.y
                min_dist = e1.radius + e2.radius
                dist_sq = dx * dx + dy * dy
                if 0.001 < dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq)
                    overlap = (min_dist - dist) * 0.5
                    push_x = (dx / dist) * overlap
                    push_y = (dy / dist) * overlap
                    e1.x -= push_x * 0.8
                    e1.y -= push_y * 0.8
                    e2.x += push_x * 0.8
                    e2.y += push_y * 0.8

    def kill_all_visible(self, drop_mgr):
        """Rosary activation: kills all visible standard enemies."""
        for e in self.enemies:
            if not e.is_boss:
                e.is_dead = True

    def draw(self, surface, camera_x, camera_y):
        for e in self.enemies:
            # Simple culling: only draw if roughly on screen
            sx = e.x - camera_x
            sy = e.y - camera_y
            if -80 <= sx <= SCREEN_WIDTH + 80 and -80 <= sy <= SCREEN_HEIGHT + 80:
                e.draw(surface, camera_x, camera_y, self.sprite_mgr)
