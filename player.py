"""
Player Entity and Progression System for Crimson Night:
Movement physics, weapon management, passive stat scaling, leveling, and Q-Dash.
"""

import math
import pygame
from settings import (
    PLAYER_BASE_HP, PLAYER_BASE_SPEED, PLAYER_BASE_MAGNET,
    PLAYER_BASE_REGEN, PLAYER_BASE_MIGHT, PLAYER_BASE_COOLDOWN,
    PLAYER_BASE_AREA, PLAYER_BASE_ARMOR, BASE_XP_TO_LEVEL,
    XP_GROWTH_FACTOR, WEAPON_DATA, PASSIVE_DATA, COLOR_RED, COLOR_WHITE,
    COLOR_CYAN, DASH_COOLDOWN, DASH_SPEED, DASH_DURATION, CHARACTER_DATA
)
from weapons import (
    WhipWeapon, MagicWandWeapon, GarlicWeapon, HolyWaterWeapon,
    KingBibleWeapon, LightningRingWeapon, DualPistolsWeapon, BloodTearWeapon
)

class Player:
    """The vampire hunter protagonist with selectable character classes and Q-Dash."""
    def __init__(self, x, y, sound_mgr, particle_mgr, sprite_mgr, character_key="hunter"):
        self.x = x
        self.y = y
        self.radius = 12
        self.sound_mgr = sound_mgr
        self.particle_mgr = particle_mgr
        self.sprite_mgr = sprite_mgr

        # Character Configuration
        self.character_key = character_key
        char_info = CHARACTER_DATA.get(character_key, CHARACTER_DATA["hunter"])
        self.sprite_key = char_info.get("sprite_key", "hunter")
        self.char_name = char_info.get("name", "Simon")

        # Base and dynamic stats with character bonuses
        self.max_hp = PLAYER_BASE_HP + char_info.get("hp_bonus", 0)
        self.hp = self.max_hp
        self.base_speed = PLAYER_BASE_SPEED * char_info.get("speed_mult", 1.0)
        self.speed = self.base_speed
        self.base_magnet = PLAYER_BASE_MAGNET
        self.magnet_radius = self.base_magnet
        self.regen = PLAYER_BASE_REGEN + char_info.get("regen_bonus", 0.0)
        self.might = PLAYER_BASE_MIGHT * char_info.get("might_mult", 1.0)
        self.cooldown_multiplier = PLAYER_BASE_COOLDOWN * char_info.get("cooldown_mult", 1.0)
        self.area_multiplier = PLAYER_BASE_AREA
        self.armor = PLAYER_BASE_ARMOR + char_info.get("armor_bonus", 0)
        self.xp_multiplier = 1.0

        # Movement physics
        self.vx = 0.0
        self.vy = 0.0
        self.facing_direction = 1  # 1 for right, -1 for left
        self.is_moving = False
        self.anim_timer = 0.0

        # Dash Mechanics (Q Key)
        self.dash_cooldown = DASH_COOLDOWN
        self.dash_cooldown_timer = 0.0
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_vx = 0.0
        self.dash_vy = 0.0
        self.afterimage_timer = 0.0
        self.afterimages = []

        # Invulnerability & Regen timers
        self.hurt_invuln_timer = 0.0
        self.flash_timer = 0.0

        # Aiming & Facing (Mouse Driven)
        self.aim_x = 0.0
        self.aim_y = 0.0
        self.aim_angle = 0.0
        self.aim_dir_x = 1.0
        self.aim_dir_y = 0.0

        # Progression & Inventory
        self.level = 1
        self.current_xp = 0
        self.xp_to_next = BASE_XP_TO_LEVEL
        self.is_leveling_up = False

        # Active Weapons and Passives
        start_weapon_key = char_info.get("weapon", "Whip")
        start_weapon = self._instantiate_weapon(start_weapon_key)
        self.weapons = [start_weapon] if start_weapon else []
        self.passives = {}

    def _instantiate_weapon(self, weapon_key):
        """Helper to create a weapon instance by key."""
        if weapon_key == "Whip":
            return WhipWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "MagicWand":
            return MagicWandWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "Garlic":
            return GarlicWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "HolyWater":
            return HolyWaterWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "KingBible":
            return KingBibleWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "LightningRing":
            return LightningRingWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "DualPistols":
            return DualPistolsWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        elif weapon_key == "BloodTear":
            return BloodTearWeapon(self, self.sound_mgr, self.particle_mgr, self.sprite_mgr)
        return None

    def get_hitbox(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2)
        )

    def trigger_dash(self):
        """Trigger an invulnerable high-speed dash burst."""
        if self.dash_cooldown_timer <= 0.0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = DASH_DURATION
            self.dash_cooldown_timer = self.dash_cooldown

            # Determine dash vector: movement direction if moving, else mouse aim
            if self.is_moving and (self.vx != 0 or self.vy != 0):
                length = math.hypot(self.vx, self.vy)
                dx = self.vx / length
                dy = self.vy / length
            else:
                dx = self.aim_dir_x
                dy = self.aim_dir_y

            self.dash_vx = dx * DASH_SPEED
            self.dash_vy = dy * DASH_SPEED

            # Grant invulnerability during dash
            self.hurt_invuln_timer = max(self.hurt_invuln_timer, DASH_DURATION + 0.12)

            self.sound_mgr.play("dash")
            self.particle_mgr.trigger_shake(3.5)
            self.particle_mgr.spawn_spark_burst(self.x, self.y, COLOR_CYAN, count=8)
            return True
        return False

    def handle_input(self, dt, camera_x=0.0, camera_y=0.0):
        # 1. Mouse Aiming and Facing
        mx, my = pygame.mouse.get_pos()
        self.aim_x = mx + camera_x
        self.aim_y = my + camera_y
        adx = self.aim_x - self.x
        ady = self.aim_y - self.y
        self.aim_angle = math.atan2(ady, adx)
        self.aim_dir_x = math.cos(self.aim_angle)
        self.aim_dir_y = math.sin(self.aim_angle)

        if adx != 0:
            self.facing_direction = 1 if adx >= 0 else -1

        # 2. Movement keys (WASD / Arrows)
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1.0

        # Check Q key for dash
        if keys[pygame.K_q]:
            self.trigger_dash()

        self.is_moving = (dx != 0 or dy != 0)

        # Normalize 8-directional movement
        if self.is_moving:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

            self.vx = dx * self.speed
            self.vy = dy * self.speed
            self.anim_timer += dt * 10.0
        else:
            self.vx = 0.0
            self.vy = 0.0
            self.anim_timer = 0.0

    def update(self, dt, enemies, camera_x=0.0, camera_y=0.0):
        # 1. Update Dash Cooldown
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer = max(0.0, self.dash_cooldown_timer - dt)

        # 2. Update Movement or Dash
        if self.is_dashing:
            self.dash_timer -= dt
            self.x += self.dash_vx * dt
            self.y += self.dash_vy * dt

            # Spawn afterimage phantom sprites
            self.afterimage_timer += dt
            if self.afterimage_timer >= 0.035:
                self.afterimage_timer = 0.0
                self.afterimages.append({
                    "x": self.x,
                    "y": self.y,
                    "facing": self.facing_direction,
                    "alpha": 180
                })

            if self.dash_timer <= 0:
                self.is_dashing = False
        else:
            self.handle_input(dt, camera_x, camera_y)
            self.x += self.vx * dt
            self.y += self.vy * dt

        # Decay afterimages
        retained = []
        for img in self.afterimages:
            img["alpha"] -= int(500 * dt)
            if img["alpha"] > 0:
                retained.append(img)
        self.afterimages = retained

        # Natural passive HP regeneration
        if self.regen > 0 and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + self.regen * dt)

        # Invulnerability timer decay
        if self.hurt_invuln_timer > 0:
            self.hurt_invuln_timer -= dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Update all active weapons
        for w in self.weapons:
            w.update(dt, enemies)

    def take_damage(self, raw_amount):
        if self.hurt_invuln_timer > 0:
            return
        # Calculate actual damage after armor
        dmg = max(1.0, raw_amount - self.armor)
        self.hp -= dmg
        self.hurt_invuln_timer = 0.2
        self.flash_timer = 0.12
        self.sound_mgr.play("player_hurt")
        self.particle_mgr.trigger_shake(4.0)
        self.particle_mgr.trigger_flash(COLOR_RED, initial_alpha=70)
        self.particle_mgr.add_damage_number(self.x, self.y - 25, int(dmg), is_crit=True)

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return int(self.hp - old_hp)

    def heal_half_hp(self):
        """Instantly restores 50% of maximum HP."""
        heal_amount = max(1, int(self.max_hp * 0.5))
        return self.heal(heal_amount)

    def add_xp(self, amount):
        self.current_xp += amount
        if self.current_xp >= self.xp_to_next:
            self.current_xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * XP_GROWTH_FACTOR)
            self.is_leveling_up = True
            self.sound_mgr.play("levelup")
            self.particle_mgr.trigger_flash(COLOR_WHITE, initial_alpha=160)
            self.particle_mgr.trigger_shake(6.0)

    def apply_upgrade(self, item_key, item_type):
        """Applies a weapon or passive upgrade choice."""
        if item_type == "weapon":
            existing = next((w for w in self.weapons if w.name == item_key), None)
            if existing:
                existing.upgrade()
            else:
                new_weapon = self._instantiate_weapon(item_key)
                if new_weapon:
                    self.weapons.append(new_weapon)

        elif item_type == "passive":
            cur_lvl = self.passives.get(item_key, 0)
            self.passives[item_key] = cur_lvl + 1
            self._recalculate_passives()

    def _recalculate_passives(self):
        """Recalculate dynamic player stats based on passive items."""
        char_info = CHARACTER_DATA.get(self.character_key, CHARACTER_DATA["hunter"])

        # Spinach (+10% might per level)
        spinach_lvl = self.passives.get("Spinach", 0)
        base_might = PLAYER_BASE_MIGHT * char_info.get("might_mult", 1.0)
        self.might = base_might * (1.0 + spinach_lvl * 0.10)

        # Hollow Heart (+20% max HP, heals 20 HP)
        heart_lvl = self.passives.get("HollowHeart", 0)
        prev_max = self.max_hp
        base_hp = PLAYER_BASE_HP + char_info.get("hp_bonus", 0)
        self.max_hp = base_hp * (1.0 + heart_lvl * 0.20)
        if self.max_hp > prev_max:
            self.hp += (self.max_hp - prev_max)

        # Wings (+12% speed per level)
        wings_lvl = self.passives.get("Wings", 0)
        base_sp = PLAYER_BASE_SPEED * char_info.get("speed_mult", 1.0)
        self.speed = base_sp * (1.0 + wings_lvl * 0.12)

        # Crown (+15% XP per level)
        crown_lvl = self.passives.get("Crown", 0)
        self.xp_multiplier = 1.0 + crown_lvl * 0.15

        # Attractorb (+35% magnet range per level)
        orb_lvl = self.passives.get("Attractorb", 0)
        self.magnet_radius = PLAYER_BASE_MAGNET * (1.0 + orb_lvl * 0.35)

        # Armor (+1 reduction per level)
        armor_lvl = self.passives.get("ArmorPlate", 0)
        base_arm = PLAYER_BASE_ARMOR + char_info.get("armor_bonus", 0)
        self.armor = base_arm + armor_lvl

        # Pummarola (+0.4 regen per level)
        pumm_lvl = self.passives.get("Pummarola", 0)
        base_reg = PLAYER_BASE_REGEN + char_info.get("regen_bonus", 0.0)
        self.regen = base_reg + pumm_lvl * 0.4

        # Empty Tome (-8% cooldown per level)
        tome_lvl = self.passives.get("EmptyTome", 0)
        base_cd = PLAYER_BASE_COOLDOWN * char_info.get("cooldown_mult", 1.0)
        self.cooldown_multiplier = max(0.35, base_cd * (1.0 - tome_lvl * 0.08))

    def draw(self, surface, camera_x, camera_y):
        # Draw all weapon visuals first (behind player or around)
        for w in self.weapons:
            w.draw(surface, camera_x, camera_y)

        # Draw dash afterimages
        for img in self.afterimages:
            side = "right" if img["facing"] > 0 else "left"
            frames = self.sprite_mgr.get(f"player_{self.sprite_key}_{side}")
            if frames:
                spr = frames[0].copy()
                spr.set_alpha(img["alpha"])
                surface.blit(spr, (int(img["x"] - camera_x - spr.get_width() // 2),
                                   int(img["y"] - camera_y - spr.get_height() // 2)))

        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)

        # Select character walking or idle sprite
        side = "right" if self.facing_direction > 0 else "left"
        frames = self.sprite_mgr.get(f"player_{self.sprite_key}_{side}")
        if not frames:
            frames = self.sprite_mgr.get(f"player_walk_{side}")

        if (self.is_moving or self.is_dashing) and frames:
            frame_idx = int(self.anim_timer) % len(frames)
            spr = frames[frame_idx]
        else:
            spr = frames[0] if frames else None

        if spr:
            # White flash when hurt
            if self.flash_timer > 0:
                flash_surf = spr.copy()
                flash_surf.fill((255, 255, 255, 200), special_flags=pygame.BLEND_RGBA_ADD)
                surface.blit(flash_surf, (sx - spr.get_width() // 2, sy - spr.get_height() // 2))
            else:
                surface.blit(spr, (sx - spr.get_width() // 2, sy - spr.get_height() // 2))
