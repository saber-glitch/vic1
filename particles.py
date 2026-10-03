"""
Particle Systems, Floating Damage Numbers, and Screen Shake for Crimson Night.
"""

import math
import random
import pygame
from settings import (
    COLOR_WHITE, COLOR_GOLD, COLOR_YELLOW, COLOR_GREEN, COLOR_RED,
    COLOR_CRIMSON, COLOR_CYAN, COLOR_PURPLE, COLOR_BLOOD
)

class DamageNumber:
    """Floating combat text showing damage, crits, and healing."""
    def __init__(self, x, y, value, is_crit=False, is_heal=False):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-8, 8)
        self.value = int(value)
        self.is_crit = is_crit
        self.is_heal = is_heal
        self.vy = -75.0 if not is_crit else -110.0
        self.vx = random.uniform(-25, 25)
        self.duration = 0.65 if not is_crit else 0.85
        self.timer = self.duration

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 120.0 * dt  # Gravity curve
        self.timer -= dt
        return self.timer > 0

    def draw(self, surface, camera_x, camera_y, font, font_large):
        if self.timer <= 0:
            return
        progress = self.timer / self.duration
        alpha = int(min(255, progress * 320))
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)

        # Choose font and color
        if self.is_heal:
            f = font
            color = COLOR_GREEN
            txt = f"+{self.value}"
        elif self.is_crit:
            f = font_large
            color = COLOR_GOLD
            txt = f"{self.value}!"
        else:
            f = font
            color = COLOR_WHITE
            txt = str(self.value)

        # Render text with drop shadow
        shadow_surf = f.render(txt, True, (0, 0, 0))
        shadow_surf.set_alpha(alpha)
        text_surf = f.render(txt, True, color)
        text_surf.set_alpha(alpha)

        surface.blit(shadow_surf, (screen_x - text_surf.get_width() // 2 + 1, screen_y + 1))
        surface.blit(text_surf, (screen_x - text_surf.get_width() // 2, screen_y))


class Particle:
    """Generic fast particle with decay."""
    def __init__(self, x, y, vx, vy, color, size, duration, gravity=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.initial_size = size
        self.size = size
        self.duration = duration
        self.timer = duration
        self.gravity = gravity

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.vx *= (1.0 - 1.8 * dt)
        self.vy *= (1.0 - 1.8 * dt)
        self.timer -= dt
        ratio = max(0.0, self.timer / self.duration)
        self.size = max(1.0, self.initial_size * ratio)
        return self.timer > 0

    def draw(self, surface, camera_x, camera_y):
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)
        if self.size <= 1.5:
            surface.set_at((sx, sy), self.color)
        else:
            pygame.draw.circle(surface, self.color, (sx, sy), int(self.size))


class ParticleManager:
    """Coordinates all particle bursts, damage text, and camera shake."""
    def __init__(self):
        self.damage_numbers = []
        self.particles = []
        self.shake_trauma = 0.0
        self.flash_alpha = 0.0
        self.flash_color = COLOR_WHITE

        # Cached fonts
        self.font = pygame.font.SysFont("impact", 17)
        self.font_large = pygame.font.SysFont("impact", 23)

    def add_damage_number(self, x, y, value, is_crit=False, is_heal=False):
        self.damage_numbers.append(DamageNumber(x, y, value, is_crit, is_heal))

    def spawn_blood_burst(self, x, y, count=8):
        for _ in range(count):
            ang = random.uniform(0, 2 * math.pi)
            speed = random.uniform(40, 160)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            col = random.choice([COLOR_RED, COLOR_CRIMSON, COLOR_BLOOD])
            size = random.uniform(2.5, 4.5)
            life = random.uniform(0.25, 0.45)
            self.particles.append(Particle(x, y, vx, vy, col, size, life, gravity=40.0))

    def spawn_spark_burst(self, x, y, color=COLOR_CYAN, count=6):
        for _ in range(count):
            ang = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            size = random.uniform(2.0, 3.5)
            life = random.uniform(0.15, 0.3)
            self.particles.append(Particle(x, y, vx, vy, color, size, life))

    def spawn_magic_trail(self, x, y, color=COLOR_CYAN):
        vx = random.uniform(-10, 10)
        vy = random.uniform(-10, 10)
        self.particles.append(Particle(x, y, vx, vy, color, 3.0, 0.2))

    def trigger_shake(self, amount=6.0):
        self.shake_trauma = min(15.0, self.shake_trauma + amount)

    def trigger_flash(self, color=COLOR_WHITE, initial_alpha=180):
        self.flash_color = color
        self.flash_alpha = initial_alpha

    def update(self, dt):
        # Update damage numbers
        self.damage_numbers = [d for d in self.damage_numbers if d.update(dt)]
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        # Decay shake trauma
        if self.shake_trauma > 0:
            self.shake_trauma = max(0.0, self.shake_trauma - 18.0 * dt)
        # Decay screen flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0.0, self.flash_alpha - 380.0 * dt)

    def get_shake_offset(self):
        if self.shake_trauma <= 0:
            return 0, 0
        ox = random.uniform(-self.shake_trauma, self.shake_trauma)
        oy = random.uniform(-self.shake_trauma, self.shake_trauma)
        return int(ox), int(oy)

    def draw(self, surface, camera_x, camera_y):
        for p in self.particles:
            p.draw(surface, camera_x, camera_y)
        for d in self.damage_numbers:
            d.draw(surface, camera_x, camera_y, self.font, self.font_large)

        # Full screen flash overlay if active
        if self.flash_alpha > 5:
            flash_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            r, g, b = self.flash_color
            flash_surf.fill((r, g, b, int(self.flash_alpha)))
            surface.blit(flash_surf, (0, 0))
