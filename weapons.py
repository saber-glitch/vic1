"""
Weapons and Combat Abilities for Crimson Night:
Holy Whip, Magic Wand, Garlic Aura, Holy Water, King's Bible, and Lightning Ring.
"""

import math
import random
import pygame
from settings import (
    COLOR_CYAN, COLOR_YELLOW, COLOR_WHITE, COLOR_RED, COLOR_BLUE,
    WEAPON_DATA
)

class Weapon:
    """Base class for auto-firing weapons."""
    def __init__(self, name, player, sound_mgr, particle_mgr, sprite_mgr):
        self.name = name
        self.player = player
        self.sound_mgr = sound_mgr
        self.particle_mgr = particle_mgr
        self.sprite_mgr = sprite_mgr
        self.level = 1
        self.max_level = WEAPON_DATA[name]["max_level"]
        self.timer = 0.0

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.on_upgrade()
            return True
        return False

    def on_upgrade(self):
        pass

    def update(self, dt, enemies):
        pass

    def draw(self, surface, camera_x, camera_y):
        pass


class WhipWeapon(Weapon):
    """Slashes in the direction of the mouse cursor (and opposite at higher levels)."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("Whip", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 1.35
        self.base_damage = 22
        self.slashes = []  # active visual slashes

    def update(self, dt, enemies):
        # Update existing slash visual timers
        self.slashes = [s for s in self.slashes if s["timer"] > 0]
        for s in self.slashes:
            s["timer"] -= dt

        cd = self.base_cooldown * self.player.cooldown_multiplier
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.attack(enemies)

    def attack(self, enemies):
        self.sound_mgr.play("whip")
        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.22) * self.player.might)
        area_mult = (1.0 + (self.level - 1) * 0.15) * self.player.area_multiplier
        w = int(145 * area_mult)
        h = int(65 * area_mult)

        aim_ang = self.player.aim_angle
        slash_reach = 65.0 * area_mult

        # 1. Forward Slash towards mouse aim
        self._create_slash(aim_ang, slash_reach, w, h, damage, enemies)

        # 2. Level 3+: Back slash opposite to mouse
        if self.level >= 3:
            back_ang = aim_ang + math.pi
            self._create_slash(back_ang, slash_reach, w, h, damage, enemies)

        # 3. Level 5+: Fan extensions
        if self.level >= 5:
            self._create_slash(aim_ang + 0.35, slash_reach, int(w * 0.9), int(h * 0.9), damage, enemies)
            self._create_slash(aim_ang - 0.35, slash_reach, int(w * 0.9), int(h * 0.9), damage, enemies)

    def _create_slash(self, angle, reach, w, h, damage, enemies):
        cx = self.player.x + math.cos(angle) * reach
        cy = self.player.y + math.sin(angle) * reach

        self.slashes.append({
            "cx": cx,
            "cy": cy,
            "angle": angle,
            "w": w,
            "h": h,
            "timer": 0.16
        })

        # Hit enemies in the direction of the slash
        kx = math.cos(angle) * 190.0
        ky = math.sin(angle) * 190.0
        hit_radius = w * 0.85

        for e in enemies:
            if not e.is_dead:
                dist = math.hypot(e.x - self.player.x, e.y - self.player.y)
                if dist <= (hit_radius + e.radius):
                    # Angle check: is enemy within ~72 degrees of slash direction?
                    edx = e.x - self.player.x
                    edy = e.y - self.player.y
                    e_ang = math.atan2(edy, edx)
                    ang_diff = abs((e_ang - angle + math.pi) % (2 * math.pi) - math.pi)
                    if ang_diff < math.radians(72):
                        is_crit = (self.level >= 8 and random.random() < 0.35)
                        actual_dmg = damage * 2 if is_crit else damage
                        e.take_damage(actual_dmg, knockback_x=kx, knockback_y=ky)
                        self.particle_mgr.add_damage_number(e.x, e.y - 15, actual_dmg, is_crit=is_crit)
                        self.particle_mgr.spawn_blood_burst(e.x, e.y, count=5)
                        self.sound_mgr.play("hit")

    def draw(self, surface, camera_x, camera_y):
        spr = self.sprite_mgr.get("proj_whip")
        if not spr:
            return

        for s in self.slashes:
            w, h = s["w"], s["h"]
            scaled = pygame.transform.scale(spr, (w, h))
            rotated = pygame.transform.rotate(scaled, -math.degrees(s["angle"]))
            rx = int(s["cx"] - camera_x - rotated.get_width() // 2)
            ry = int(s["cy"] - camera_y - rotated.get_height() // 2)
            surface.blit(rotated, (rx, ry))


class MagicBolt:
    """Projectile fired by Magic Wand."""
    def __init__(self, x, y, target_x, target_y, damage, pierce=1):
        self.x = x
        self.y = y
        self.damage = damage
        self.pierce = pierce
        self.speed = 540.0
        self.radius = 8
        self.lifespan = 2.2
        self.hit_enemies = set()

        dx = target_x - x
        dy = target_y - y
        dist = max(0.001, math.hypot(dx, dy))
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

    def update(self, dt, enemies, particle_mgr, sound_mgr):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifespan -= dt

        if random.random() < 0.4:
            particle_mgr.spawn_magic_trail(self.x, self.y, COLOR_CYAN)

        # Check collision with enemies
        for e in enemies:
            if not e.is_dead and id(e) not in self.hit_enemies:
                if math.hypot(e.x - self.x, e.y - self.y) < (e.radius + self.radius):
                    self.hit_enemies.add(id(e))
                    e.take_damage(self.damage, self.vx * 0.2, self.vy * 0.2)
                    particle_mgr.add_damage_number(e.x, e.y - 12, self.damage)
                    particle_mgr.spawn_spark_burst(self.x, self.y, COLOR_CYAN, count=5)
                    sound_mgr.play("hit")
                    self.pierce -= 1
                    if self.pierce <= 0:
                        return False
        return self.lifespan > 0

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        spr = sprite_mgr.get("proj_magic")
        if spr:
            surface.blit(spr, (self.x - camera_x - 10, self.y - camera_y - 10))


class MagicWandWeapon(Weapon):
    """Fires arcane missiles in the direction of the mouse cursor."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("MagicWand", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 1.15
        self.base_damage = 18
        self.projectiles = []

    def update(self, dt, enemies):
        # Update existing bolts
        self.projectiles = [
            p for p in self.projectiles
            if p.update(dt, enemies, self.particle_mgr, self.sound_mgr)
        ]

        cd = self.base_cooldown * self.player.cooldown_multiplier * (1.0 - (self.level - 1) * 0.05)
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.shoot(enemies)

    def shoot(self, enemies):
        proj_count = 1 + (self.level // 2)
        if self.level >= 8:
            proj_count += 1
            
        pierce = 2 if self.level >= 8 else 1
        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.18) * self.player.might)

        base_angle = self.player.aim_angle

        for i in range(proj_count):
            # Spread bolts symmetrically around mouse aim vector
            spread_ang = (i - (proj_count - 1) / 2.0) * 0.16
            bolt_ang = base_angle + spread_ang
            dist = 400.0
            tx = self.player.x + math.cos(bolt_ang) * dist
            ty = self.player.y + math.sin(bolt_ang) * dist

            bolt = MagicBolt(self.player.x, self.player.y, tx, ty, damage, pierce)
            self.projectiles.append(bolt)

        self.sound_mgr.play("magic")

    def draw(self, surface, camera_x, camera_y):
        for p in self.projectiles:
            p.draw(surface, camera_x, camera_y, self.sprite_mgr)


class GarlicWeapon(Weapon):
    """Pulsating protective holy aura that damages nearby enemies."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("Garlic", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_damage = 8
        self.tick_interval = 0.38
        self.tick_timer = 0.0
        self.aura_angle = 0.0

    def update(self, dt, enemies):
        self.aura_angle += dt * 2.5
        self.tick_timer += dt

        interval = self.tick_interval * (0.85 if self.level >= 5 else 1.0)
        if self.tick_timer >= interval:
            self.tick_timer = 0.0
            self.pulse(enemies)

    def pulse(self, enemies):
        radius = (65 + self.level * 10) * self.player.area_multiplier
        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.2) * self.player.might)
        knockback = 50.0 + self.level * 10.0

        for e in enemies:
            if not e.is_dead:
                dist = math.hypot(e.x - self.player.x, e.y - self.player.y)
                if dist <= radius:
                    # Apply knockback outward
                    dx = e.x - self.player.x
                    dy = e.y - self.player.y
                    if dist > 0.01:
                        kx = (dx / dist) * knockback
                        ky = (dy / dist) * knockback
                    else:
                        kx, ky = knockback, 0

                    e.take_damage(damage, kx, ky)
                    self.particle_mgr.add_damage_number(e.x, e.y - 10, damage)
                    # Life drain chance at max level
                    if self.level >= 8 and random.random() < 0.15:
                        healed = self.player.heal(1)
                        if healed > 0:
                            self.particle_mgr.add_damage_number(self.player.x, self.player.y - 15, healed, is_heal=True)

    def draw(self, surface, camera_x, camera_y):
        radius = int((65 + self.level * 10) * self.player.area_multiplier)
        px = int(self.player.x - camera_x)
        py = int(self.player.y - camera_y)

        # Translucent pulsing aura circle
        pulse = 0.85 + 0.15 * math.sin(self.aura_angle * 3.0)
        draw_rad = int(radius * pulse)
        
        aura_surf = pygame.Surface((draw_rad * 2 + 4, draw_rad * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (220, 245, 220, 35), (draw_rad + 2, draw_rad + 2), draw_rad)
        pygame.draw.circle(aura_surf, (180, 240, 180, 75), (draw_rad + 2, draw_rad + 2), draw_rad, 2)
        surface.blit(aura_surf, (px - draw_rad - 2, py - draw_rad - 2))

        # Orbiting garlic runes
        clove_count = min(6, 2 + self.level // 2)
        for i in range(clove_count):
            ang = self.aura_angle + i * (math.pi * 2 / clove_count)
            cx = px + int(math.cos(ang) * (radius * 0.9))
            cy = py + int(math.sin(ang) * (radius * 0.9))
            pygame.draw.circle(surface, (240, 245, 230), (cx, cy), 3)


class HolyFirePool:
    """Lingering pool of holy fire created by Holy Water flask."""
    def __init__(self, x, y, radius, damage, duration):
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.duration = duration
        self.timer = duration
        self.tick_timer = 0.0

    def update(self, dt, enemies, particle_mgr, sound_mgr):
        self.timer -= dt
        self.tick_timer += dt
        
        # Damage enemies standing in fire every 0.25s
        if self.tick_timer >= 0.25:
            self.tick_timer = 0.0
            for e in enemies:
                if not e.is_dead and math.hypot(e.x - self.x, e.y - self.y) <= self.radius:
                    e.take_damage(self.damage)
                    particle_mgr.add_damage_number(e.x, e.y - 12, self.damage)
                    particle_mgr.spawn_spark_burst(e.x, e.y, COLOR_CYAN, count=2)

        return self.timer > 0

    def draw(self, surface, camera_x, camera_y):
        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)
        alpha = int(min(180, (self.timer / self.duration) * 220))
        
        pool_surf = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(pool_surf, (60, 180, 255, alpha // 2), (self.radius + 2, self.radius + 2), self.radius)
        pygame.draw.circle(pool_surf, (140, 230, 255, alpha), (self.radius + 2, self.radius + 2), int(self.radius * 0.65))
        pygame.draw.circle(pool_surf, (255, 255, 255, alpha), (self.radius + 2, self.radius + 2), int(self.radius * 0.35))
        surface.blit(pool_surf, (sx - self.radius - 2, sy - self.radius - 2))


class HolyWaterWeapon(Weapon):
    """Throws flasks of holy water creating lingering patches of holy fire."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("HolyWater", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 2.4
        self.base_damage = 14
        self.pools = []

    def update(self, dt, enemies):
        self.pools = [p for p in self.pools if p.update(dt, enemies, self.particle_mgr, self.sound_mgr)]

        cd = self.base_cooldown * self.player.cooldown_multiplier
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.throw(enemies)

    def throw(self, enemies):
        flask_count = 1 + (self.level // 2)
        if self.level >= 8:
            flask_count += 2

        pool_rad = int((50 + self.level * 6) * self.player.area_multiplier)
        dmg = int(self.base_damage * (1.0 + (self.level - 1) * 0.18) * self.player.might)
        duration = 3.2 + (self.level * 0.3)

        for _ in range(flask_count):
            # Target directly near mouse cursor position!
            tx = self.player.aim_x + random.uniform(-45, 45)
            ty = self.player.aim_y + random.uniform(-45, 45)
            self.pools.append(HolyFirePool(tx, ty, pool_rad, dmg, duration))

        self.sound_mgr.play("explosion")
        self.particle_mgr.trigger_shake(3.0)

    def draw(self, surface, camera_x, camera_y):
        for p in self.pools:
            p.draw(surface, camera_x, camera_y)


class KingBibleWeapon(Weapon):
    """Holy scriptures continuously rotating around the player in orbit."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("KingBible", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_damage = 16
        self.orbit_angle = 0.0
        self.hit_cooldowns = {}  # enemy_id -> timestamp cooldown

    def update(self, dt, enemies):
        rot_speed = 3.2 * (1.0 + (self.level - 1) * 0.1)
        self.orbit_angle += rot_speed * dt
        
        # Decay hit cooldowns
        for eid in list(self.hit_cooldowns.keys()):
            self.hit_cooldowns[eid] -= dt
            if self.hit_cooldowns[eid] <= 0:
                del self.hit_cooldowns[eid]

        bible_count = 1 + (self.level // 2)
        if self.level >= 8:
            bible_count += 2

        orbit_radius = (80 + self.level * 5) * self.player.area_multiplier
        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.2) * self.player.might)

        for i in range(bible_count):
            ang = self.orbit_angle + i * (2 * math.pi / bible_count)
            bx = self.player.x + math.cos(ang) * orbit_radius
            by = self.player.y + math.sin(ang) * orbit_radius

            # Check collision with enemies
            for e in enemies:
                if not e.is_dead and id(e) not in self.hit_cooldowns:
                    if math.hypot(e.x - bx, e.y - by) <= (e.radius + 16):
                        self.hit_cooldowns[id(e)] = 0.32
                        kx = math.cos(ang) * 90.0
                        ky = math.sin(ang) * 90.0
                        e.take_damage(damage, kx, ky)
                        self.particle_mgr.add_damage_number(e.x, e.y - 12, damage)
                        self.particle_mgr.spawn_spark_burst(bx, by, COLOR_YELLOW, count=4)
                        self.sound_mgr.play("hit")

    def draw(self, surface, camera_x, camera_y):
        bible_count = 1 + (self.level // 2)
        if self.level >= 8:
            bible_count += 2

        orbit_radius = (80 + self.level * 5) * self.player.area_multiplier
        spr = self.sprite_mgr.get("proj_bible")

        for i in range(bible_count):
            ang = self.orbit_angle + i * (2 * math.pi / bible_count)
            bx = int(self.player.x + math.cos(ang) * orbit_radius - camera_x)
            by = int(self.player.y + math.sin(ang) * orbit_radius - camera_y)
            if spr:
                # Rotate sprite slightly with orbit
                surface.blit(spr, (bx - spr.get_width() // 2, by - spr.get_height() // 2))


class LightningRingWeapon(Weapon):
    """Calls down strikes of holy thunder from above upon foes near the mouse."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("LightningRing", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 2.8
        self.base_damage = 38
        self.active_strikes = []  # visual strike lines

    def update(self, dt, enemies):
        self.active_strikes = [s for s in self.active_strikes if s["timer"] > 0]
        for s in self.active_strikes:
            s["timer"] -= dt

        cd = self.base_cooldown * self.player.cooldown_multiplier * (0.8 if self.level >= 7 else 1.0)
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.strike(enemies)

    def strike(self, enemies):
        alive = [e for e in enemies if not e.is_dead]
        if not alive:
            return

        strike_count = 2 + (self.level // 2)
        if self.level >= 8:
            strike_count += 3

        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.25) * self.player.might)
        splash_rad = 45 * self.player.area_multiplier

        # Target enemies closest to the mouse cursor position!
        alive.sort(key=lambda e: math.hypot(e.x - self.player.aim_x, e.y - self.player.aim_y))
        chosen_targets = alive[:strike_count]
        for t in chosen_targets:
            # Generate jagged lightning bolt points
            pts = [(t.x + random.uniform(-15, 15), self.player.y - 450)]
            segments = 6
            for s in range(1, segments):
                frac = s / segments
                sy = (self.player.y - 450) + (t.y - (self.player.y - 450)) * frac
                sx = t.x + random.uniform(-25, 25)
                pts.append((sx, sy))
            pts.append((t.x, t.y))

            self.active_strikes.append({"points": pts, "timer": 0.18})

            # Area damage around impact
            for e in alive:
                if math.hypot(e.x - t.x, e.y - t.y) <= splash_rad:
                    e.take_damage(damage, 0, 0)
                    self.particle_mgr.add_damage_number(e.x, e.y - 15, damage, is_crit=True)
                    self.particle_mgr.spawn_spark_burst(e.x, e.y, COLOR_YELLOW, count=6)

        self.sound_mgr.play("lightning")
        self.particle_mgr.trigger_shake(5.0)

    def draw(self, surface, camera_x, camera_y):
        for s in self.active_strikes:
            pts = [(int(px - camera_x), int(py - camera_y)) for px, py in s["points"]]
            if len(pts) >= 2:
                pygame.draw.lines(surface, COLOR_YELLOW, False, pts, 4)
                pygame.draw.lines(surface, COLOR_WHITE, False, pts, 2)


class PistolBullet:
    """High-velocity bullet fired by Dual Pistols."""
    def __init__(self, x, y, angle, damage, pierce=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.pierce = pierce
        self.speed = 760.0
        self.radius = 6
        self.lifespan = 1.6
        self.hit_enemies = set()
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def update(self, dt, enemies, particle_mgr, sound_mgr):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifespan -= dt

        # Collision with enemies
        for e in enemies:
            if not e.is_dead and id(e) not in self.hit_enemies:
                if math.hypot(e.x - self.x, e.y - self.y) < (e.radius + self.radius):
                    self.hit_enemies.add(id(e))
                    e.take_damage(self.damage, self.vx * 0.15, self.vy * 0.15)
                    particle_mgr.add_damage_number(e.x, e.y - 12, self.damage)
                    particle_mgr.spawn_spark_burst(self.x, self.y, COLOR_YELLOW, count=4)
                    sound_mgr.play("hit")
                    self.pierce -= 1
                    if self.pierce <= 0:
                        return False
        return self.lifespan > 0

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        spr = sprite_mgr.get("proj_bullet")
        if spr:
            rotated = pygame.transform.rotate(spr, -math.degrees(self.angle))
            surface.blit(rotated, (self.x - camera_x - rotated.get_width() // 2, self.y - camera_y - rotated.get_height() // 2))


class DualPistolsWeapon(Weapon):
    """Rapidly fires alternating silver bullets towards the mouse cursor."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("DualPistols", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 0.82
        self.base_damage = 19
        self.projectiles = []
        self.barrel_side = 1

    def update(self, dt, enemies):
        self.projectiles = [
            p for p in self.projectiles
            if p.update(dt, enemies, self.particle_mgr, self.sound_mgr)
        ]

        cd = self.base_cooldown * self.player.cooldown_multiplier * (1.0 - (self.level - 1) * 0.05)
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.shoot()

    def shoot(self):
        shots = 2 + (self.level // 2)
        if self.level >= 8:
            shots += 2

        pierce = 2 if self.level >= 5 else 1
        if self.level >= 8:
            pierce = 3

        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.20) * self.player.might)
        base_ang = self.player.aim_angle

        for i in range(shots):
            spread = (i - (shots - 1) / 2.0) * 0.12
            ang = base_ang + spread
            self.barrel_side *= -1
            perp_ang = ang + math.pi / 2
            offset_dist = 8.0 * self.barrel_side
            sx = self.player.x + math.cos(perp_ang) * offset_dist
            sy = self.player.y + math.sin(perp_ang) * offset_dist
            self.projectiles.append(PistolBullet(sx, sy, ang, damage, pierce))

        self.sound_mgr.play("gunshot")
        self.particle_mgr.trigger_shake(2.0)

    def draw(self, surface, camera_x, camera_y):
        for p in self.projectiles:
            p.draw(surface, camera_x, camera_y, self.sprite_mgr)


class BloodWaveProjectile:
    """Piercing crimson blood wave with lifesteal."""
    def __init__(self, x, y, angle, damage, lifesteal_chance=0.20):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.lifesteal_chance = lifesteal_chance
        self.speed = 460.0
        self.radius = 16
        self.lifespan = 1.4
        self.hit_enemies = set()
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def update(self, dt, enemies, player, particle_mgr, sound_mgr):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifespan -= dt

        if random.random() < 0.3:
            particle_mgr.spawn_blood_burst(self.x, self.y, count=2)

        for e in enemies:
            if not e.is_dead and id(e) not in self.hit_enemies:
                if math.hypot(e.x - self.x, e.y - self.y) < (e.radius + self.radius):
                    self.hit_enemies.add(id(e))
                    e.take_damage(self.damage, self.vx * 0.25, self.vy * 0.25)
                    particle_mgr.add_damage_number(e.x, e.y - 12, self.damage, is_crit=True)
                    particle_mgr.spawn_blood_burst(e.x, e.y, count=6)
                    sound_mgr.play("hit")

                    # Lifesteal chance
                    if random.random() < self.lifesteal_chance:
                        healed = player.heal(2)
                        if healed > 0:
                            particle_mgr.add_damage_number(player.x, player.y - 20, healed, is_heal=True)

        return self.lifespan > 0

    def draw(self, surface, camera_x, camera_y, sprite_mgr):
        spr = sprite_mgr.get("proj_blood_tear")
        if spr:
            rotated = pygame.transform.rotate(spr, -math.degrees(self.angle))
            surface.blit(rotated, (self.x - camera_x - rotated.get_width() // 2, self.y - camera_y - rotated.get_height() // 2))


class BloodTearWeapon(Weapon):
    """Slashes piercing crimson blood waves towards the mouse with life-steal."""
    def __init__(self, player, sound_mgr, particle_mgr, sprite_mgr):
        super().__init__("BloodTear", player, sound_mgr, particle_mgr, sprite_mgr)
        self.base_cooldown = 1.3
        self.base_damage = 26
        self.projectiles = []

    def update(self, dt, enemies):
        self.projectiles = [
            p for p in self.projectiles
            if p.update(dt, enemies, self.player, self.particle_mgr, self.sound_mgr)
        ]

        cd = self.base_cooldown * self.player.cooldown_multiplier * (1.0 - (self.level - 1) * 0.05)
        self.timer += dt
        if self.timer >= cd:
            self.timer = 0.0
            self.slash()

    def slash(self):
        waves = 1 + (self.level // 3)
        if self.level >= 8:
            waves = 4

        damage = int(self.base_damage * (1.0 + (self.level - 1) * 0.22) * self.player.might)
        lifesteal = 0.20 + (self.level * 0.03)
        base_ang = self.player.aim_angle

        for i in range(waves):
            spread = (i - (waves - 1) / 2.0) * 0.22
            ang = base_ang + spread
            self.projectiles.append(BloodWaveProjectile(self.player.x, self.player.y, ang, damage, lifesteal))

        self.sound_mgr.play("blood_slash")
        self.particle_mgr.trigger_shake(3.0)

    def draw(self, surface, camera_x, camera_y):
        for p in self.projectiles:
            p.draw(surface, camera_x, camera_y, self.sprite_mgr)
