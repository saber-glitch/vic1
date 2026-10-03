"""
Procedural Pixel Art and Sprite Generation for Crimson Night.
Generates all characters, monsters, weapons, pickups, and tiles with retro gothic aesthetics.
"""

import math
import random
import pygame
from settings import (
    COLOR_RED, COLOR_CRIMSON, COLOR_BLOOD, COLOR_GOLD, COLOR_YELLOW,
    COLOR_BLUE, COLOR_CYAN, COLOR_PURPLE, COLOR_VIOLET, COLOR_GREEN,
    COLOR_EMERALD, COLOR_WHITE, COLOR_GREY, COLOR_DARK_GREY, COLOR_BLACK,
    COLOR_FLOOR, COLOR_FLOOR_ALT, COLOR_GRID
)

class SpriteManager:
    """Generates and caches all procedural 2D sprites."""
    
    def __init__(self):
        self.cache = {}
        self._init_player_sprites()
        self._init_enemy_sprites()
        self._init_pickup_sprites()
        self._init_weapon_sprites()
        self._init_terrain_tiles()
        self._init_ui_icons()

    def get(self, key):
        return self.cache.get(key)

    # ----------------------------------------------------
    # PLAYER SPRITES (4 PLAYABLE CHARACTERS)
    # ----------------------------------------------------
    def _init_player_sprites(self):
        w, h = 32, 42

        # 1. HUNTER (Simon - Belmont style)
        hunter_r = []
        for frame_idx in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            bob = 1 if frame_idx in (1, 3) else 0
            leg_offset = 3 if frame_idx == 1 else (-3 if frame_idx == 3 else 0)

            # Cape
            cape_pts = [(10, 16 + bob), (4 - frame_idx, 36), (18, 34), (16, 18 + bob)]
            pygame.draw.polygon(surf, COLOR_CRIMSON, cape_pts)
            # Legs
            pygame.draw.rect(surf, (40, 30, 25), (10 - leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (40, 30, 25), (17 + leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (20, 15, 12), (9 - leg_offset, 37, 7, 5))
            pygame.draw.rect(surf, (20, 15, 12), (16 + leg_offset, 37, 7, 5))
            # Torso
            pygame.draw.rect(surf, (80, 50, 40), (10, 15 + bob, 12, 14))
            pygame.draw.rect(surf, (140, 100, 70), (12, 17 + bob, 8, 10))
            pygame.draw.rect(surf, COLOR_GOLD, (11, 27 + bob, 10, 2))
            # Head
            pygame.draw.rect(surf, (240, 205, 180), (12, 6 + bob, 8, 9))
            pygame.draw.rect(surf, (35, 20, 15), (11, 4 + bob, 10, 4))
            pygame.draw.rect(surf, COLOR_RED, (11, 7 + bob, 10, 2))
            pygame.draw.rect(surf, (20, 20, 25), (17, 9 + bob, 2, 2))
            # Arms
            pygame.draw.rect(surf, (80, 50, 40), (7, 17 + bob, 4, 8))
            pygame.draw.rect(surf, (80, 50, 40), (21, 17 + bob, 4, 8))
            pygame.draw.rect(surf, (240, 205, 180), (22, 24 + bob, 3, 3))
            hunter_r.append(surf)

        # 2. VAMPIRE (Vlad - Aristocratic Blood Lord)
        vampire_r = []
        for frame_idx in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            bob = 1 if frame_idx in (1, 3) else 0
            leg_offset = 3 if frame_idx == 1 else (-3 if frame_idx == 3 else 0)

            # Elegant flowing midnight cape with scarlet interior
            pygame.draw.polygon(surf, (20, 15, 25), [(10, 15 + bob), (2 - frame_idx, 38), (16, 36), (14, 18 + bob)])
            pygame.draw.polygon(surf, COLOR_RED, [(10, 16 + bob), (4 - frame_idx, 36), (12, 35)])
            # Dark trousers & patent boots
            pygame.draw.rect(surf, (25, 20, 30), (10 - leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (25, 20, 30), (17 + leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (10, 8, 12), (9 - leg_offset, 37, 7, 5))
            pygame.draw.rect(surf, (10, 8, 12), (16 + leg_offset, 37, 7, 5))
            # Obsidian coat & crimson vest
            pygame.draw.rect(surf, (30, 20, 35), (10, 15 + bob, 12, 14))
            pygame.draw.rect(surf, COLOR_CRIMSON, (13, 17 + bob, 6, 9))
            pygame.draw.rect(surf, COLOR_GOLD, (12, 26 + bob, 8, 2))
            # Pale aristocratic face & glowing red eyes
            pygame.draw.rect(surf, (245, 240, 245), (12, 6 + bob, 8, 9))
            pygame.draw.rect(surf, (15, 10, 20), (11, 4 + bob, 10, 4))   # Slick dark hair
            pygame.draw.rect(surf, (15, 10, 20), (10, 7 + bob, 2, 7))
            pygame.draw.rect(surf, COLOR_RED, (16, 9 + bob, 2, 2))         # Glowing red eye
            # Regal cuffs & pale hands
            pygame.draw.rect(surf, (30, 20, 35), (7, 17 + bob, 4, 8))
            pygame.draw.rect(surf, (30, 20, 35), (21, 17 + bob, 4, 8))
            pygame.draw.rect(surf, (245, 240, 245), (22, 24 + bob, 3, 3))
            vampire_r.append(surf)

        # 3. GUNSLINGER (Drake - Twin Revolver Inquisitor)
        gunslinger_r = []
        for frame_idx in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            bob = 1 if frame_idx in (1, 3) else 0
            leg_offset = 3 if frame_idx == 1 else (-3 if frame_idx == 3 else 0)

            # Leather Duster Coat tails
            pygame.draw.polygon(surf, (75, 48, 30), [(10, 20 + bob), (5, 36), (12, 34)])
            pygame.draw.polygon(surf, (75, 48, 30), [(18, 20 + bob), (23, 36), (17, 34)])
            # Denim trousers & rider boots with spurs
            pygame.draw.rect(surf, (40, 45, 60), (10 - leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (40, 45, 60), (17 + leg_offset, 28, 5, 12))
            pygame.draw.rect(surf, (45, 30, 20), (9 - leg_offset, 37, 7, 5))
            pygame.draw.rect(surf, (45, 30, 20), (16 + leg_offset, 37, 7, 5))
            # Leather vest & ammunition bandolier
            pygame.draw.rect(surf, (95, 60, 40), (10, 15 + bob, 12, 14))
            pygame.draw.line(surf, COLOR_GOLD, (11, 16 + bob), (20, 26 + bob), 2)  # Bandolier
            # Face & Wide-Brimmed Cowboy/Inquisitor Hat
            pygame.draw.rect(surf, (235, 195, 170), (12, 7 + bob, 8, 8))
            pygame.draw.rect(surf, (30, 20, 15), (17, 10 + bob, 2, 2))  # Eye
            # Hat: Crown and wide brim
            pygame.draw.rect(surf, (55, 35, 25), (11, 2 + bob, 10, 5))
            pygame.draw.ellipse(surf, (40, 25, 18), (6, 5 + bob, 20, 4))
            # Dual Revolvers in hands!
            # Left pistol
            pygame.draw.rect(surf, (190, 190, 200), (4, 21 + bob, 5, 3))
            pygame.draw.rect(surf, (60, 40, 25), (7, 23 + bob, 2, 3))
            # Right pistol
            pygame.draw.rect(surf, (190, 190, 200), (23, 21 + bob, 6, 3))
            pygame.draw.rect(surf, (60, 40, 25), (22, 23 + bob, 2, 3))
            gunslinger_r.append(surf)

        # 4. MAGE (Eldrin - Arcane Spellweaver)
        mage_r = []
        for frame_idx in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            bob = 1 if frame_idx in (1, 3) else 0

            # Flowing Arcane Robe
            robe_pts = [(10, 16 + bob), (5, 38), (27, 38), (22, 16 + bob)]
            pygame.draw.polygon(surf, (35, 45, 95), robe_pts)
            pygame.draw.polygon(surf, COLOR_GOLD, [(15, 16 + bob), (13, 38), (17, 38)])  # Gold trim
            # Wizard Face & Beard
            pygame.draw.rect(surf, (240, 210, 185), (12, 9 + bob, 8, 7))
            pygame.draw.polygon(surf, (230, 230, 235), [(12, 14 + bob), (16, 21 + bob), (20, 14 + bob)])  # Silver beard
            pygame.draw.rect(surf, COLOR_CYAN, (17, 11 + bob, 2, 2))  # Glowing eye
            # Pointed Wizard Hat
            pygame.draw.polygon(surf, (25, 35, 80), [(16, 0 + bob), (8, 9 + bob), (24, 9 + bob)])
            pygame.draw.ellipse(surf, (20, 28, 65), (6, 8 + bob, 20, 4))
            pygame.draw.rect(surf, COLOR_GOLD, (12, 7 + bob, 8, 2))   # Hat buckle
            # Arcane Staff with Glowing Blue Orb
            pygame.draw.line(surf, (120, 75, 40), (25, 8 + bob), (25, 36), 2)
            pygame.draw.circle(surf, COLOR_CYAN, (25, 7 + bob), 4)
            pygame.draw.circle(surf, COLOR_WHITE, (25, 7 + bob), 2)
            mage_r.append(surf)

        # Cache all directional variations
        for key, r_frames in [
            ("hunter", hunter_r),
            ("vampire", vampire_r),
            ("gunslinger", gunslinger_r),
            ("mage", mage_r)
        ]:
            l_frames = [pygame.transform.flip(f, True, False) for f in r_frames]
            self.cache[f"player_{key}_right"] = r_frames
            self.cache[f"player_{key}_left"] = l_frames

        # Default legacy aliases
        self.cache["player_walk_right"] = hunter_r
        self.cache["player_walk_left"] = [pygame.transform.flip(f, True, False) for f in hunter_r]
        self.cache["player_idle"] = hunter_r[0]

    # ----------------------------------------------------
    # ENEMY SPRITES
    # ----------------------------------------------------
    def _init_enemy_sprites(self):
        # 1. BAT (Fast Swarm) - 3 animation frames
        bat_frames = []
        for i in range(3):
            surf = pygame.Surface((28, 22), pygame.SRCALPHA)
            wing_y = 2 if i == 0 else (9 if i == 1 else 16)
            # Wings
            wing_color = (60, 40, 65)
            pygame.draw.polygon(surf, wing_color, [(14, 11), (2, wing_y), (8, 14)])
            pygame.draw.polygon(surf, wing_color, [(14, 11), (26, wing_y), (20, 14)])
            # Bat Body
            pygame.draw.ellipse(surf, (30, 20, 35), (9, 7, 10, 10))
            # Ears
            pygame.draw.polygon(surf, (30, 20, 35), [(10, 7), (10, 3), (12, 7)])
            pygame.draw.polygon(surf, (30, 20, 35), [(16, 7), (18, 3), (18, 7)])
            # Glowing Red Eyes
            pygame.draw.rect(surf, COLOR_RED, (11, 10, 2, 2))
            pygame.draw.rect(surf, COLOR_RED, (15, 10, 2, 2))
            bat_frames.append(surf)
        self.cache["enemy_bat"] = bat_frames

        # 2. SKELETON (Standard Marcher)
        skel_frames = []
        for leg_frame in (0, 1):
            surf = pygame.Surface((28, 38), pygame.SRCALPHA)
            leg_dx = 3 if leg_frame == 1 else -3
            # Legs
            pygame.draw.line(surf, (220, 220, 220), (11, 24), (9 - leg_dx, 36), 2)
            pygame.draw.line(surf, (220, 220, 220), (17, 24), (19 + leg_dx, 36), 2)
            # Spine & Ribcage
            pygame.draw.line(surf, (210, 210, 210), (14, 15), (14, 25), 3)
            for ry in (16, 19, 22):
                pygame.draw.line(surf, (230, 230, 230), (10, ry), (18, ry), 2)
            # Skull
            pygame.draw.rect(surf, (240, 240, 240), (9, 4, 10, 10))
            # Cyan Eye Sockets
            pygame.draw.rect(surf, COLOR_CYAN, (11, 8, 2, 2))
            pygame.draw.rect(surf, COLOR_CYAN, (15, 8, 2, 2))
            # Arms
            pygame.draw.line(surf, (220, 220, 220), (10, 16), (6, 25), 2)
            pygame.draw.line(surf, (220, 220, 220), (18, 16), (22, 25), 2)
            skel_frames.append(surf)
        self.cache["enemy_skeleton"] = skel_frames

        # 3. ZOMBIE (Tanky Shambler)
        zomb_frames = []
        for f in (0, 1):
            surf = pygame.Surface((32, 40), pygame.SRCALPHA)
            sway = 2 if f == 1 else -2
            # Rotten legs
            pygame.draw.rect(surf, (55, 65, 50), (10, 26, 5, 12))
            pygame.draw.rect(surf, (50, 60, 45), (17, 26, 5, 12))
            # Shambling Body
            pygame.draw.rect(surf, (60, 80, 60), (9, 13, 14, 14))
            pygame.draw.rect(surf, (85, 115, 75), (10, 5, 12, 10))  # Head
            # Hollow Red Eyes
            pygame.draw.rect(surf, COLOR_RED, (12 + sway // 2, 8, 2, 2))
            pygame.draw.rect(surf, COLOR_RED, (17 + sway // 2, 8, 2, 2))
            # Outstretched Zombie Arms
            pygame.draw.rect(surf, (85, 115, 75), (20, 15, 10, 4))
            zomb_frames.append(surf)
        self.cache["enemy_zombie"] = zomb_frames

        # 4. WRAITH (Spectral Ghost)
        wraith_frames = []
        for i in range(3):
            surf = pygame.Surface((34, 44), pygame.SRCALPHA)
            tail_x = 17 + int(math.sin(i * 2.0) * 4)
            # Spectral shroud
            poly = [
                (17, 4), (28, 14), (26, 32), (tail_x, 42), (8, 32), (6, 14)
            ]
            pygame.draw.polygon(surf, (80, 120, 180, 180), poly)
            pygame.draw.polygon(surf, (140, 190, 240, 210), [(17, 8), (24, 16), (22, 30), (tail_x, 38), (12, 30), (10, 16)])
            # Glowing Face
            pygame.draw.circle(surf, (220, 245, 255), (14, 14), 2)
            pygame.draw.circle(surf, (220, 245, 255), (20, 14), 2)
            wraith_frames.append(surf)
        self.cache["enemy_wraith"] = wraith_frames

        # 5. GARGOYLE (Heavy Attacker)
        garg_frames = []
        for f in (0, 1):
            surf = pygame.Surface((44, 48), pygame.SRCALPHA)
            wy = 6 if f == 0 else 12
            # Stone Wings
            pygame.draw.polygon(surf, (90, 95, 105), [(22, 22), (2, wy), (8, 30)])
            pygame.draw.polygon(surf, (90, 95, 105), [(22, 22), (42, wy), (36, 30)])
            # Stone Torso
            pygame.draw.rect(surf, (115, 120, 130), (14, 16, 16, 18), border_radius=4)
            # Horned Head
            pygame.draw.rect(surf, (100, 105, 115), (16, 6, 12, 12))
            pygame.draw.polygon(surf, (60, 65, 75), [(15, 6), (12, 1), (17, 4)])  # Left Horn
            pygame.draw.polygon(surf, (60, 65, 75), [(27, 4), (32, 1), (29, 6)])  # Right Horn
            # Amber Glowing Eyes
            pygame.draw.rect(surf, COLOR_YELLOW, (18, 10, 2, 2))
            pygame.draw.rect(surf, COLOR_YELLOW, (24, 10, 2, 2))
            # Heavy Claws
            pygame.draw.rect(surf, (80, 85, 95), (14, 34, 6, 10))
            pygame.draw.rect(surf, (80, 85, 95), (24, 34, 6, 10))
            garg_frames.append(surf)
        self.cache["enemy_gargoyle"] = garg_frames

        # 6. VAMPIRE LORD (BOSS)
        boss_frames = []
        for f in (0, 1):
            surf = pygame.Surface((64, 76), pygame.SRCALPHA)
            glow_rad = 34 if f == 0 else 32
            # Crimson Boss Aura
            aura = pygame.Surface((64, 76), pygame.SRCALPHA)
            pygame.draw.circle(aura, (180, 20, 40, 45), (32, 38), glow_rad)
            surf.blit(aura, (0, 0))

            # Giant Demon Wings
            wy = 8 if f == 0 else 14
            pygame.draw.polygon(surf, (40, 10, 20), [(32, 34), (4, wy), (14, 48)])
            pygame.draw.polygon(surf, (40, 10, 20), [(32, 34), (60, wy), (50, 48)])
            # Vampire Regal Cape
            pygame.draw.polygon(surf, COLOR_CRIMSON, [(32, 22), (12, 62), (52, 62)])
            pygame.draw.polygon(surf, COLOR_GOLD, [(32, 22), (20, 62), (22, 62)])
            pygame.draw.polygon(surf, COLOR_GOLD, [(32, 22), (44, 62), (42, 62)])

            # Regal Torso & Clothes
            pygame.draw.rect(surf, (20, 15, 25), (24, 24, 16, 24))
            pygame.draw.rect(surf, COLOR_GOLD, (28, 26, 8, 16))   # Gold cravat
            # Vampire Head & Fangs
            pygame.draw.rect(surf, (240, 235, 240), (25, 10, 14, 15))
            pygame.draw.rect(surf, (20, 10, 25), (23, 7, 18, 6))  # Slick black hair
            # Fiery Red Piercing Eyes
            pygame.draw.rect(surf, COLOR_RED, (27, 15, 3, 2))
            pygame.draw.rect(surf, COLOR_RED, (34, 15, 3, 2))
            # Fangs
            pygame.draw.rect(surf, COLOR_WHITE, (29, 21, 2, 3))
            pygame.draw.rect(surf, COLOR_WHITE, (33, 21, 2, 3))

            boss_frames.append(surf)
        self.cache["enemy_vampire_boss"] = boss_frames

        # 7. PHANTOM KNIGHT (Ghostly Armored Knight)
        pk_frames = []
        for f in (0, 1):
            surf = pygame.Surface((38, 48), pygame.SRCALPHA)
            bob = 2 if f == 1 else 0
            # Spectral body glow
            aura = pygame.Surface((38, 48), pygame.SRCALPHA)
            pygame.draw.ellipse(aura, (60, 80, 180, 50), (4, 8, 30, 36))
            surf.blit(aura, (0, 0))
            # Armor torso
            pygame.draw.rect(surf, (70, 80, 140, 200), (11, 18 + bob, 16, 16), border_radius=2)
            pygame.draw.rect(surf, (90, 100, 170, 210), (13, 20 + bob, 12, 12))
            # Helmet
            pygame.draw.rect(surf, (80, 90, 150, 220), (12, 6 + bob, 14, 14), border_radius=3)
            pygame.draw.rect(surf, (40, 50, 100), (14, 12 + bob, 10, 2))  # Visor slit
            # Glowing eyes through visor
            pygame.draw.rect(surf, COLOR_CYAN, (15, 12 + bob, 3, 2))
            pygame.draw.rect(surf, COLOR_CYAN, (21, 12 + bob, 3, 2))
            # Spectral legs (translucent)
            pygame.draw.rect(surf, (60, 80, 160, 140), (12, 34 + bob, 5, 10))
            pygame.draw.rect(surf, (60, 80, 160, 140), (21, 34 + bob, 5, 10))
            # Ghostly sword
            pygame.draw.line(surf, (160, 180, 255, 200), (30, 10 + bob), (34, 38 + bob), 3)
            pygame.draw.line(surf, (200, 220, 255), (28, 22 + bob), (36, 22 + bob), 2)
            # Shoulder pauldrons
            pygame.draw.ellipse(surf, (80, 90, 150, 200), (7, 16 + bob, 8, 6))
            pygame.draw.ellipse(surf, (80, 90, 150, 200), (23, 16 + bob, 8, 6))
            pk_frames.append(surf)
        self.cache["enemy_phantom_knight"] = pk_frames

        # 8. HELLHOUND (Fiery Demon Dog)
        hh_frames = []
        for i in range(3):
            surf = pygame.Surface((36, 30), pygame.SRCALPHA)
            leg_phase = i
            # Fire trail behind
            for fx in range(3):
                alpha = 120 - fx * 35
                pygame.draw.circle(surf, (255, 120, 20, alpha), (6 - fx * 3, 20), 4 - fx)
            # Body
            pygame.draw.ellipse(surf, (80, 20, 15), (8, 10, 20, 14))
            pygame.draw.ellipse(surf, (120, 40, 20), (10, 12, 16, 10))
            # Head
            pygame.draw.ellipse(surf, (90, 25, 15), (24, 8, 10, 10))
            pygame.draw.polygon(surf, (90, 25, 15), [(32, 8), (34, 4), (30, 8)])  # Ear
            # Glowing orange eyes
            pygame.draw.rect(surf, (255, 160, 30), (28, 11, 2, 2))
            pygame.draw.rect(surf, (255, 160, 30), (31, 11, 2, 2))
            # Jaw
            pygame.draw.rect(surf, (60, 15, 10), (30, 15, 4, 2))
            pygame.draw.rect(surf, COLOR_WHITE, (31, 16, 1, 1))  # Fang
            # Legs (animated)
            ly1 = 24 + (2 if leg_phase == 0 else (-2 if leg_phase == 2 else 0))
            ly2 = 24 + (-2 if leg_phase == 0 else (2 if leg_phase == 2 else 0))
            pygame.draw.line(surf, (60, 15, 10), (12, 22), (10, ly1), 2)
            pygame.draw.line(surf, (60, 15, 10), (18, 22), (16, ly2), 2)
            pygame.draw.line(surf, (60, 15, 10), (22, 22), (24, ly1), 2)
            pygame.draw.line(surf, (60, 15, 10), (26, 22), (28, ly2), 2)
            # Flaming mane
            for mx in range(14, 26, 3):
                fh = 5 + (i * 2 if (mx % 6 == 0) else 0)
                pygame.draw.polygon(surf, (255, 100 + mx, 20, 180), [(mx, 10), (mx + 2, 10 - fh), (mx + 4, 10)])
            hh_frames.append(surf)
        self.cache["enemy_hellhound"] = hh_frames

        # 9. NECROMANCER (Dark Caster)
        necro_frames = []
        for f in (0, 1):
            surf = pygame.Surface((30, 44), pygame.SRCALPHA)
            bob = 1 if f == 1 else 0
            # Dark flowing robe
            robe_pts = [(10, 14 + bob), (3, 42), (27, 42), (20, 14 + bob)]
            pygame.draw.polygon(surf, (20, 15, 30), robe_pts)
            pygame.draw.polygon(surf, (30, 20, 45), [(12, 16 + bob), (8, 40), (22, 40), (18, 16 + bob)])
            # Hood
            pygame.draw.polygon(surf, (15, 10, 25), [(15, 2 + bob), (6, 14 + bob), (24, 14 + bob)])
            # Skull face under hood
            pygame.draw.rect(surf, (220, 210, 200), (11, 8 + bob, 8, 7))
            pygame.draw.rect(surf, (10, 10, 10), (13, 10 + bob, 2, 2))  # Eye socket
            pygame.draw.rect(surf, (10, 10, 10), (16, 10 + bob, 2, 2))  # Eye socket
            pygame.draw.rect(surf, COLOR_GREEN, (13, 10 + bob, 2, 2))   # Green glow
            pygame.draw.rect(surf, COLOR_GREEN, (16, 10 + bob, 2, 2))   # Green glow
            pygame.draw.rect(surf, (10, 10, 10), (14, 13 + bob, 2, 1))  # Nose hole
            # Glowing green hands
            glow_r = 4 if f == 0 else 5
            pygame.draw.circle(surf, (30, 180, 50, 100), (5, 28 + bob), glow_r)
            pygame.draw.circle(surf, COLOR_GREEN, (5, 28 + bob), 3)
            pygame.draw.circle(surf, (30, 180, 50, 100), (25, 28 + bob), glow_r)
            pygame.draw.circle(surf, COLOR_GREEN, (25, 28 + bob), 3)
            necro_frames.append(surf)
        self.cache["enemy_necromancer"] = necro_frames

        # 10. BANSHEE (Screaming Ghost)
        banshee_frames = []
        for i in range(3):
            surf = pygame.Surface((32, 42), pygame.SRCALPHA)
            hair_sway = int(math.sin(i * 2.5) * 5)
            # Ghostly body (translucent)
            body_pts = [(16, 8), (26, 18), (24, 34), (16, 40), (8, 34), (6, 18)]
            pygame.draw.polygon(surf, (200, 190, 220, 150), body_pts)
            pygame.draw.polygon(surf, (230, 225, 245, 180), [(16, 10), (22, 18), (20, 32), (16, 36), (12, 32), (10, 18)])
            # Pale face
            pygame.draw.ellipse(surf, (245, 240, 250, 220), (10, 6, 12, 12))
            # Hollow dark eyes
            pygame.draw.ellipse(surf, (20, 10, 30), (12, 10, 3, 4))
            pygame.draw.ellipse(surf, (20, 10, 30), (17, 10, 3, 4))
            # Screaming mouth
            mouth_h = 3 + i
            pygame.draw.ellipse(surf, (20, 10, 30), (13, 15, 6, mouth_h))
            # Flowing hair
            for hx in range(8, 24, 3):
                pygame.draw.line(surf, (180, 170, 200, 180), (hx, 6), (hx + hair_sway, -2 - (hx % 5)), 2)
            # Wispy trail at bottom
            for wx in range(10, 22, 3):
                wy = 38 + int(math.sin(i + wx) * 2)
                pygame.draw.line(surf, (200, 190, 220, 100), (wx, 36), (wx, wy + 4), 1)
            banshee_frames.append(surf)
        self.cache["enemy_banshee"] = banshee_frames

        # 11. CRAWLER (Spider Creature)
        crawler_frames = []
        for f in (0, 1):
            surf = pygame.Surface((34, 20), pygame.SRCALPHA)
            leg_off = 2 if f == 1 else -2
            # Dark body
            pygame.draw.ellipse(surf, (40, 30, 25), (10, 6, 14, 10))
            pygame.draw.ellipse(surf, (55, 40, 30), (12, 7, 10, 8))
            # Head
            pygame.draw.ellipse(surf, (45, 35, 28), (21, 7, 8, 7))
            # Multiple red eyes (4 pairs)
            for ex, ey in [(23, 9), (25, 8), (27, 9), (25, 11)]:
                pygame.draw.rect(surf, COLOR_RED, (ex, ey, 1, 1))
            # Legs (8 total, 4 per side)
            for lx, side in [(12, -1), (15, -1), (18, -1), (21, -1),
                             (12, 1), (15, 1), (18, 1), (21, 1)]:
                ly = 10
                end_y = 18 + (leg_off if lx % 6 == 0 else -leg_off)
                end_x = lx + (6 * side)
                pygame.draw.line(surf, (35, 25, 20), (lx, ly), (end_x, end_y), 1)
            # Fangs/mandibles
            pygame.draw.line(surf, (200, 180, 160), (28, 11), (30, 14), 1)
            pygame.draw.line(surf, (200, 180, 160), (27, 12), (29, 15), 1)
            crawler_frames.append(surf)
        self.cache["enemy_crawler"] = crawler_frames

        # 12. BLOOD GOLEM (Massive Blood Construct)
        bg_frames = []
        for f in (0, 1):
            surf = pygame.Surface((40, 50), pygame.SRCALPHA)
            bob = 1 if f == 1 else 0
            # Dripping blood aura
            aura = pygame.Surface((40, 50), pygame.SRCALPHA)
            pygame.draw.ellipse(aura, (120, 10, 20, 60), (4, 6, 32, 40))
            surf.blit(aura, (0, 0))
            # Massive body
            pygame.draw.rect(surf, (150, 20, 30), (10, 14 + bob, 20, 22), border_radius=4)
            pygame.draw.rect(surf, (180, 30, 40), (12, 16 + bob, 16, 18), border_radius=3)
            # Head (small on big body)
            pygame.draw.rect(surf, (160, 25, 35), (14, 6 + bob, 12, 10), border_radius=3)
            # Glowing eyes
            pygame.draw.rect(surf, COLOR_YELLOW, (16, 10 + bob, 3, 2))
            pygame.draw.rect(surf, COLOR_YELLOW, (22, 10 + bob, 3, 2))
            # Huge arms
            pygame.draw.rect(surf, (140, 18, 25), (2, 16 + bob, 9, 16), border_radius=3)
            pygame.draw.rect(surf, (140, 18, 25), (29, 16 + bob, 9, 16), border_radius=3)
            # Fists
            pygame.draw.rect(surf, (170, 25, 35), (3, 30 + bob, 7, 6), border_radius=2)
            pygame.draw.rect(surf, (170, 25, 35), (30, 30 + bob, 7, 6), border_radius=2)
            # Thick legs
            pygame.draw.rect(surf, (130, 15, 22), (12, 36 + bob, 7, 12))
            pygame.draw.rect(surf, (130, 15, 22), (21, 36 + bob, 7, 12))
            # Blood drip effects
            drip_positions = [(8, 20), (32, 22), (15, 35), (25, 34)]
            for dx, dy in drip_positions:
                drip_len = 4 + (f * 2) + (dx % 3)
                pygame.draw.line(surf, (200, 30, 40, 180), (dx, dy + bob), (dx, dy + bob + drip_len), 2)
            bg_frames.append(surf)
        self.cache["enemy_blood_golem"] = bg_frames

        # 13. DEATH REAPER (MEGA BOSS)
        reaper_frames = []
        for f in (0, 1):
            surf = pygame.Surface((72, 84), pygame.SRCALPHA)
            bob = 2 if f == 1 else 0
            # Purple soul aura
            aura = pygame.Surface((72, 84), pygame.SRCALPHA)
            aura_rad = 38 if f == 0 else 36
            pygame.draw.circle(aura, (120, 40, 180, 50), (36, 42), aura_rad)
            surf.blit(aura, (0, 0))
            # Massive black robe
            robe_pts = [(36, 16 + bob), (8, 78), (64, 78)]
            pygame.draw.polygon(surf, (15, 10, 20), robe_pts)
            pygame.draw.polygon(surf, (25, 18, 35), [(36, 20 + bob), (14, 74), (58, 74)])
            # Tattered robe edges
            for tx in range(12, 60, 6):
                ty = 74 + (tx % 8) - 4
                pygame.draw.polygon(surf, (15, 10, 20), [(tx, 74), (tx + 3, ty + 4), (tx + 6, 74)])
            # Hood
            pygame.draw.polygon(surf, (10, 8, 15), [(36, 4 + bob), (20, 20 + bob), (52, 20 + bob)])
            # Skull face
            pygame.draw.rect(surf, (240, 235, 230), (28, 10 + bob, 16, 14), border_radius=2)
            # Glowing purple eyes
            pygame.draw.rect(surf, COLOR_PURPLE, (30, 15 + bob, 4, 3))
            pygame.draw.rect(surf, COLOR_PURPLE, (38, 15 + bob, 4, 3))
            pygame.draw.rect(surf, (220, 150, 255), (31, 16 + bob, 2, 1))
            pygame.draw.rect(surf, (220, 150, 255), (39, 16 + bob, 2, 1))
            # Nose and teeth
            pygame.draw.rect(surf, (180, 175, 170), (34, 19 + bob, 4, 2))
            for tx in range(30, 42, 2):
                pygame.draw.rect(surf, (220, 215, 210), (tx, 22 + bob, 1, 2))
            # Giant scythe
            # Handle
            pygame.draw.line(surf, (100, 80, 60), (54, 6 + bob), (54, 70 + bob), 3)
            # Blade
            pygame.draw.polygon(surf, (180, 190, 200), [(54, 6 + bob), (70, 14 + bob), (66, 20 + bob), (54, 16 + bob)])
            pygame.draw.polygon(surf, (220, 230, 240), [(56, 8 + bob), (66, 14 + bob), (64, 18 + bob), (56, 14 + bob)])
            # Blade edge glow
            pygame.draw.line(surf, COLOR_PURPLE, (56, 8 + bob), (68, 15 + bob), 1)
            # Skeletal hand gripping scythe
            pygame.draw.rect(surf, (230, 225, 220), (50, 30 + bob, 8, 5))
            # Soul wisps floating around
            for sx_w, sy_w in [(14, 30), (58, 50), (20, 60)]:
                wisp_off = (f * 3)
                pygame.draw.circle(surf, (160, 80, 220, 80), (sx_w + wisp_off, sy_w + bob), 4)
                pygame.draw.circle(surf, (200, 140, 255, 120), (sx_w + wisp_off, sy_w + bob), 2)
            reaper_frames.append(surf)
        self.cache["enemy_death_reaper"] = reaper_frames

    # ----------------------------------------------------
    # PICKUPS & DROPS
    # ----------------------------------------------------
    def _init_pickup_sprites(self):
        # XP Gems (Faceted Diamond Shape)
        gem_colors = {
            "gem_blue": (COLOR_CYAN, COLOR_BLUE),
            "gem_green": (COLOR_GREEN, COLOR_EMERALD),
            "gem_red": (COLOR_YELLOW, COLOR_RED),
            "gem_gold": (COLOR_WHITE, COLOR_GOLD)
        }
        for key, (c_hi, c_base) in gem_colors.items():
            surf = pygame.Surface((18, 22), pygame.SRCALPHA)
            pts = [(9, 1), (16, 8), (9, 20), (2, 8)]
            pygame.draw.polygon(surf, c_base, pts)
            # Highlights
            hi_pts = [(9, 2), (14, 8), (9, 9), (4, 8)]
            pygame.draw.polygon(surf, c_hi, hi_pts)
            pygame.draw.polygon(surf, (255, 255, 255, 180), [(9, 2), (11, 5), (9, 7), (7, 5)])
            self.cache[key] = surf

        # Meat (Roast on bone)
        meat_surf = pygame.Surface((24, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(meat_surf, (160, 60, 40), (4, 4, 16, 12))
        pygame.draw.ellipse(meat_surf, (190, 80, 50), (6, 5, 10, 7))
        # Bone
        pygame.draw.circle(meat_surf, COLOR_WHITE, (3, 7), 2)
        pygame.draw.circle(meat_surf, COLOR_WHITE, (3, 11), 2)
        pygame.draw.circle(meat_surf, COLOR_WHITE, (21, 8), 2)
        self.cache["drop_meat"] = meat_surf

        # Vacuum / Magnet
        mag_surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Horseshoe arc
        pygame.draw.arc(mag_surf, COLOR_RED, (4, 3, 16, 16), 0, 3.1415, 5)
        pygame.draw.rect(mag_surf, COLOR_RED, (4, 11, 5, 7))
        pygame.draw.rect(mag_surf, COLOR_BLUE, (15, 11, 5, 7))
        # Silver tips
        pygame.draw.rect(mag_surf, COLOR_WHITE, (4, 16, 5, 3))
        pygame.draw.rect(mag_surf, COLOR_WHITE, (15, 16, 5, 3))
        self.cache["drop_magnet"] = mag_surf

        # Rosary (Golden Crucifix)
        ros_surf = pygame.Surface((24, 28), pygame.SRCALPHA)
        # Radiant aura
        pygame.draw.circle(ros_surf, (255, 240, 120, 80), (12, 14), 11)
        # Cross
        pygame.draw.rect(ros_surf, COLOR_GOLD, (10, 3, 4, 22), border_radius=1)
        pygame.draw.rect(ros_surf, COLOR_GOLD, (4, 8, 16, 4), border_radius=1)
        pygame.draw.rect(ros_surf, COLOR_YELLOW, (11, 4, 2, 20))
        self.cache["drop_rosary"] = ros_surf

        # Treasure Chest
        chest_surf = pygame.Surface((32, 26), pygame.SRCALPHA)
        # Chest Body
        pygame.draw.rect(surf:=chest_surf, (110, 65, 35), (4, 8, 24, 16), border_radius=2)
        pygame.draw.rect(chest_surf, (80, 45, 25), (6, 10, 20, 12))
        # Metal Bands & Trim
        pygame.draw.rect(chest_surf, COLOR_GOLD, (4, 6, 24, 4), border_radius=1)
        pygame.draw.rect(chest_surf, COLOR_GOLD, (8, 6, 3, 18))
        pygame.draw.rect(chest_surf, COLOR_GOLD, (21, 6, 3, 18))
        # Golden Keyhole Lock
        pygame.draw.circle(chest_surf, COLOR_GOLD, (16, 14), 3)
        pygame.draw.circle(chest_surf, COLOR_BLACK, (16, 14), 1)
        self.cache["drop_chest"] = chest_surf

    # ----------------------------------------------------
    # WEAPON SPRITES & PROJECTILES
    # ----------------------------------------------------
    def _init_weapon_sprites(self):
        # 1. Whip Slash Arc
        whip_surf = pygame.Surface((120, 48), pygame.SRCALPHA)
        for i in range(5):
            alpha = 255 - i * 40
            color = (255, 255, 255, alpha) if i == 0 else (240, 60, 70, alpha)
            rect = pygame.Rect(10 + i * 2, 4 + i * 3, 100 - i * 8, 38 - i * 6)
            pygame.draw.arc(whip_surf, color, rect, 0.2, 3.1, 4)
        self.cache["proj_whip"] = whip_surf

        # 2. Magic Wand Bolt
        bolt_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(bolt_surf, (100, 180, 255, 100), (10, 10), 9)
        pygame.draw.circle(bolt_surf, COLOR_BLUE, (10, 10), 6)
        pygame.draw.circle(bolt_surf, COLOR_CYAN, (10, 10), 4)
        pygame.draw.circle(bolt_surf, COLOR_WHITE, (10, 10), 2)
        self.cache["proj_magic"] = bolt_surf

        # 3. King's Bible (Spinning Grimoire)
        bible_surf = pygame.Surface((24, 28), pygame.SRCALPHA)
        # Leather cover
        pygame.draw.rect(bible_surf, (80, 20, 100), (3, 3, 18, 22), border_radius=2)
        pygame.draw.rect(bible_surf, COLOR_GOLD, (3, 3, 18, 22), 2, border_radius=2)
        # Book pages
        pygame.draw.rect(bible_surf, (245, 240, 225), (5, 5, 14, 18))
        # Holy Cross on cover
        pygame.draw.rect(bible_surf, COLOR_GOLD, (11, 7, 2, 14))
        pygame.draw.rect(bible_surf, COLOR_GOLD, (7, 10, 10, 2))
        self.cache["proj_bible"] = bible_surf

        # 4. Holy Water Flask
        flask_surf = pygame.Surface((18, 22), pygame.SRCALPHA)
        pygame.draw.ellipse(flask_surf, COLOR_CYAN, (3, 8, 12, 12))
        pygame.draw.rect(flask_surf, (200, 240, 255), (7, 3, 4, 6))
        pygame.draw.rect(flask_surf, (150, 100, 50), (6, 2, 6, 2))  # Cork
        self.cache["proj_holy_water"] = flask_surf

        # 5. Cross (Spinning Throwing Cross)
        cross_surf = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.rect(cross_surf, COLOR_GOLD, (10, 2, 6, 22), border_radius=1)
        pygame.draw.rect(cross_surf, COLOR_GOLD, (2, 7, 22, 6), border_radius=1)
        pygame.draw.rect(cross_surf, COLOR_YELLOW, (11, 3, 4, 20))
        pygame.draw.rect(cross_surf, COLOR_YELLOW, (3, 8, 20, 4))
        pygame.draw.circle(cross_surf, COLOR_RED, (13, 10), 2)  # Central ruby
        self.cache["proj_cross"] = cross_surf

        # 6. Silver Pistol Bullet
        bullet_surf = pygame.Surface((18, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(bullet_surf, (255, 235, 120), (0, 2, 16, 6))
        pygame.draw.ellipse(bullet_surf, COLOR_WHITE, (2, 3, 10, 4))
        pygame.draw.circle(bullet_surf, (255, 180, 50), (14, 5), 3)
        self.cache["proj_bullet"] = bullet_surf

        # 7. Blood Tear Crescent Arc
        blood_surf = pygame.Surface((44, 26), pygame.SRCALPHA)
        pygame.draw.arc(blood_surf, COLOR_RED, (2, 2, 40, 22), 0.4, 3.2, 5)
        pygame.draw.arc(blood_surf, (255, 110, 130), (4, 4, 36, 18), 0.5, 3.0, 3)
        pygame.draw.circle(blood_surf, COLOR_BLOOD, (22, 13), 3)
        self.cache["proj_blood_tear"] = blood_surf

    # ----------------------------------------------------
    # TERRAIN & ENVIRONMENT TILES
    # ----------------------------------------------------
    def _init_terrain_tiles(self):
        tile_size = 64
        # Tile 1: Gothic Crypt Cobblestone
        t1 = pygame.Surface((tile_size, tile_size))
        t1.fill(COLOR_FLOOR)
        # Draw stones
        stones = [
            (2, 2, 28, 18), (32, 2, 30, 22),
            (2, 22, 24, 24), (28, 26, 34, 18),
            (2, 48, 36, 14), (40, 46, 22, 16)
        ]
        for sx, sy, sw, sh in stones:
            pygame.draw.rect(t1, COLOR_FLOOR_ALT, (sx, sy, sw, sh), border_radius=2)
            pygame.draw.rect(t1, COLOR_GRID, (sx, sy, sw, sh), 1, border_radius=2)
            # Subtle stone speckle
            pygame.draw.rect(t1, (45, 40, 58), (sx + 3, sy + 3, sw - 6, 2))
        self.cache["tile_cobble"] = t1

        # Tile 2: Dark Graveyard Soil with Grass & Skulls
        t2 = pygame.Surface((tile_size, tile_size))
        t2.fill((20, 18, 28))
        # Patches of dark soil
        pygame.draw.rect(t2, (26, 24, 36), (6, 8, 24, 20), border_radius=4)
        pygame.draw.rect(t2, (26, 24, 36), (34, 32, 26, 24), border_radius=4)
        # Dead grass tufts
        for gx, gy in [(12, 14), (44, 40), (22, 50), (50, 16)]:
            pygame.draw.line(t2, (50, 65, 45), (gx, gy), (gx - 2, gy - 6), 1)
            pygame.draw.line(t2, (60, 80, 55), (gx, gy), (gx + 1, gy - 8), 1)
            pygame.draw.line(t2, (50, 65, 45), (gx, gy), (gx + 4, gy - 5), 1)
        self.cache["tile_soil"] = t2

        # Prop: Gravestones
        grave_surf = pygame.Surface((28, 36), pygame.SRCALPHA)
        # Tombstone shape
        pygame.draw.rect(grave_surf, (80, 85, 95), (4, 10, 20, 24), border_top_left_radius=8, border_top_right_radius=8)
        pygame.draw.rect(grave_surf, (105, 110, 120), (6, 12, 16, 20), border_top_left_radius=6, border_top_right_radius=6)
        # Chiseled Cross
        pygame.draw.rect(grave_surf, (50, 55, 65), (13, 16, 2, 10))
        pygame.draw.rect(grave_surf, (50, 55, 65), (9, 19, 10, 2))
        # Ground base
        pygame.draw.ellipse(grave_surf, (25, 20, 30), (0, 30, 28, 6))
        self.cache["prop_gravestone"] = grave_surf

    # ----------------------------------------------------
    # UI ICONS
    # ----------------------------------------------------
    def _init_ui_icons(self):
        size = 36
        # Generate 36x36 bordered icon cards for HUD and Level-Up
        icon_defs = {
            "whip": (COLOR_RED, [(6, 26), (18, 12), (30, 8)]),
            "wand": (COLOR_CYAN, [(8, 28), (28, 8)]),
            "garlic": (COLOR_GREEN, [(18, 18)]),
            "holy_water": (COLOR_BLUE, [(18, 20)]),
            "bible": (COLOR_PURPLE, [(18, 18)]),
            "lightning": (COLOR_YELLOW, [(18, 18)]),
            "spinach": (COLOR_EMERALD, [(18, 18)]),
            "heart": (COLOR_CRIMSON, [(18, 18)]),
            "wings": (COLOR_CYAN, [(18, 18)]),
            "crown": (COLOR_GOLD, [(18, 18)]),
            "magnet": (COLOR_BLUE, [(18, 18)]),
            "armor": (COLOR_GREY, [(18, 18)]),
            "pummarola": (COLOR_RED, [(18, 20)]),
            "tome": (COLOR_VIOLET, [(18, 18)]),
            "pistol": (COLOR_GOLD, [(18, 18)]),
            "blood": (COLOR_RED, [(18, 18)])
        }

        for name in icon_defs:
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            # Background
            pygame.draw.rect(surf, (35, 30, 48), (2, 2, size - 4, size - 4), border_radius=4)
            pygame.draw.rect(surf, (80, 70, 100), (2, 2, size - 4, size - 4), 2, border_radius=4)
            
            # Draw specific mini-symbol
            if name == "whip":
                pygame.draw.arc(surf, COLOR_RED, (6, 6, 24, 24), 0.5, 3.8, 3)
            elif name == "wand":
                pygame.draw.line(surf, (140, 90, 50), (6, 28), (24, 10), 3)
                pygame.draw.circle(surf, COLOR_CYAN, (26, 8), 4)
            elif name == "garlic":
                pygame.draw.circle(surf, (240, 245, 230), (18, 20), 8)
                pygame.draw.line(surf, COLOR_GREEN, (18, 12), (18, 6), 2)
            elif name == "holy_water":
                pygame.draw.ellipse(surf, COLOR_CYAN, (10, 12, 16, 16))
                pygame.draw.rect(surf, COLOR_WHITE, (16, 6, 4, 8))
            elif name == "bible":
                pygame.draw.rect(surf, (100, 30, 130), (8, 6, 20, 24), border_radius=2)
                pygame.draw.rect(surf, COLOR_GOLD, (17, 10, 2, 16))
                pygame.draw.rect(surf, COLOR_GOLD, (12, 14, 12, 2))
            elif name == "lightning":
                pts = [(20, 4), (12, 18), (18, 18), (14, 32), (24, 14), (18, 14)]
                pygame.draw.polygon(surf, COLOR_YELLOW, pts)
            elif name == "heart":
                pygame.draw.circle(surf, COLOR_CRIMSON, (13, 14), 6)
                pygame.draw.circle(surf, COLOR_CRIMSON, (23, 14), 6)
                pygame.draw.polygon(surf, COLOR_CRIMSON, [(7, 16), (29, 16), (18, 28)])
            elif name == "spinach":
                pygame.draw.ellipse(surf, COLOR_GREEN, (10, 8, 16, 22))
                pygame.draw.line(surf, COLOR_EMERALD, (18, 30), (18, 10), 2)
            elif name == "wings":
                pygame.draw.polygon(surf, COLOR_WHITE, [(6, 22), (18, 8), (14, 24)])
                pygame.draw.polygon(surf, COLOR_WHITE, [(30, 22), (18, 8), (22, 24)])
            elif name == "crown":
                pts = [(6, 24), (8, 10), (13, 18), (18, 8), (23, 18), (28, 10), (30, 24)]
                pygame.draw.polygon(surf, COLOR_GOLD, pts)
            elif name == "magnet":
                pygame.draw.arc(surf, COLOR_RED, (8, 6, 20, 20), 0, 3.1415, 4)
                pygame.draw.rect(surf, COLOR_RED, (8, 16, 4, 8))
                pygame.draw.rect(surf, COLOR_BLUE, (24, 16, 4, 8))
            elif name == "armor":
                pygame.draw.polygon(surf, COLOR_GREY, [(10, 6), (26, 6), (24, 24), (18, 30), (12, 24)])
            elif name == "pummarola":
                pygame.draw.circle(surf, COLOR_RED, (18, 20), 9)
                pygame.draw.line(surf, COLOR_GREEN, (18, 11), (18, 6), 2)
            elif name == "tome":
                pygame.draw.rect(surf, (60, 40, 100), (8, 8, 20, 22), border_radius=2)
                pygame.draw.circle(surf, COLOR_CYAN, (18, 19), 4)
            elif name == "pistol":
                pygame.draw.line(surf, (200, 200, 210), (9, 26), (25, 10), 3)
                pygame.draw.line(surf, (200, 200, 210), (11, 10), (27, 26), 3)
                pygame.draw.circle(surf, COLOR_GOLD, (18, 18), 3)
            elif name == "blood":
                pts = [(18, 6), (26, 20), (24, 26), (18, 29), (12, 26), (10, 20)]
                pygame.draw.polygon(surf, COLOR_RED, pts)
                pygame.draw.circle(surf, (255, 140, 160), (16, 17), 2)

            self.cache[f"icon_{name}"] = surf
