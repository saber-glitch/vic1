"""
User Interface, Menus, HUD, and Level-Up Cards for Crimson Night.
"""

import math
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_GOLD,
    COLOR_YELLOW, COLOR_RED, COLOR_CRIMSON, COLOR_CYAN, COLOR_BLUE,
    COLOR_GREEN, COLOR_PURPLE, COLOR_GREY, COLOR_DARK_GREY, COLOR_AMBER,
    WEAPON_DATA, PASSIVE_DATA, CHARACTER_DATA, DASH_COOLDOWN
)

class UIManager:
    """Manages HUD rendering, Level-Up cards, and Game Over overlays."""
    def __init__(self, sound_mgr, sprite_mgr):
        self.sound_mgr = sound_mgr
        self.sprite_mgr = sprite_mgr

        # Initialize fonts
        self.font_title = pygame.font.SysFont("georgia", 52, bold=True)
        self.font_header = pygame.font.SysFont("impact", 36)
        self.font_card_title = pygame.font.SysFont("impact", 21)
        self.font_body = pygame.font.SysFont("arial", 15, bold=True)
        self.font_hud = pygame.font.SysFont("impact", 22)
        self.font_hud_sm = pygame.font.SysFont("arial", 13, bold=True)
        self.font_badge = pygame.font.SysFont("impact", 13)

        # Level-Up Selection state
        self.current_choices = []
        self.selected_index = 0

        # Character selection state
        self.selected_char_index = 0

        # Chest Opening state
        self.chest_rewards = []
        self.chest_open_timer = 0.0

    # ----------------------------------------------------
    # IN-GAME HUD
    # ----------------------------------------------------
    def draw_hud(self, surface, player, game_time, kills):
        # 1. Top XP Bar
        bar_w = SCREEN_WIDTH - 40
        bar_h = 16
        bar_x = 20
        bar_y = 12

        pct = max(0.0, min(1.0, player.current_xp / max(1, player.xp_to_next)))

        # XP Bar Background
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        # Filled Progress
        if pct > 0:
            fill_w = int(bar_w * pct)
            pygame.draw.rect(surface, COLOR_CYAN, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
            # Glistening top highlight
            pygame.draw.rect(surface, (200, 245, 255), (bar_x, bar_y, fill_w, 4), border_radius=2)
        pygame.draw.rect(surface, COLOR_GOLD, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)

        # Level Badge
        lvl_str = f"LV {player.level}"
        lvl_surf = self.font_hud_sm.render(lvl_str, True, COLOR_GOLD)
        surface.blit(lvl_surf, (bar_x + 10, bar_y + 1))

        xp_str = f"{player.current_xp} / {player.xp_to_next} XP"
        xp_surf = self.font_hud_sm.render(xp_str, True, COLOR_WHITE)
        surface.blit(xp_surf, (bar_x + bar_w - xp_surf.get_width() - 10, bar_y + 1))

        # 2. Player Health Bar (Top Left below XP bar)
        hp_x = 20
        hp_y = 34
        hp_w = 200
        hp_h = 18
        hp_pct = max(0.0, min(1.0, player.hp / max(1, player.max_hp)))

        pygame.draw.rect(surface, (30, 10, 15), (hp_x, hp_y, hp_w, hp_h), border_radius=4)
        if hp_pct > 0:
            pygame.draw.rect(surface, COLOR_RED, (hp_x, hp_y, int(hp_w * hp_pct), hp_h), border_radius=4)
            pygame.draw.rect(surface, (255, 120, 120), (hp_x, hp_y, int(hp_w * hp_pct), 4), border_radius=2)
        pygame.draw.rect(surface, (120, 40, 50), (hp_x, hp_y, hp_w, hp_h), 2, border_radius=4)

        hp_txt = f"{player.char_name}: {int(player.hp)} / {int(player.max_hp)} HP"
        hp_surf = self.font_hud_sm.render(hp_txt, True, COLOR_WHITE)
        surface.blit(hp_surf, (hp_x + hp_w // 2 - hp_surf.get_width() // 2, hp_y + 2))

        # 3. Dash Indicator (Directly below Health Bar)
        dash_x = 20
        dash_y = 56
        dash_w = 140
        dash_h = 16
        is_ready = (player.dash_cooldown_timer <= 0.0)

        pygame.draw.rect(surface, (22, 26, 38), (dash_x, dash_y, dash_w, dash_h), border_radius=3)
        if not is_ready:
            pct_cd = 1.0 - (player.dash_cooldown_timer / player.dash_cooldown)
            fill_cd = int(dash_w * max(0.0, min(1.0, pct_cd)))
            pygame.draw.rect(surface, (35, 90, 150), (dash_x, dash_y, fill_cd, dash_h), border_radius=3)
            d_txt = f"[Q] DASH: {player.dash_cooldown_timer:.1f}s"
            d_col = COLOR_GREY
        else:
            pygame.draw.rect(surface, COLOR_CYAN, (dash_x, dash_y, dash_w, dash_h), border_radius=3)
            d_txt = "[Q] DASH: READY"
            d_col = COLOR_BLACK
        pygame.draw.rect(surface, COLOR_CYAN if is_ready else (70, 85, 110), (dash_x, dash_y, dash_w, dash_h), 1, border_radius=3)
        dash_surf = self.font_hud_sm.render(d_txt, True, d_col)
        surface.blit(dash_surf, (dash_x + dash_w // 2 - dash_surf.get_width() // 2, dash_y + 1))

        # 3. Clock & Kill Counter (Top Center)
        mins = int(game_time) // 60
        secs = int(game_time) % 60
        time_str = f"{mins:02d}:{secs:02d}"
        time_surf = self.font_hud.render(time_str, True, COLOR_WHITE)
        surface.blit(time_surf, (SCREEN_WIDTH // 2 - time_surf.get_width() // 2, 34))

        kill_str = f"💀 {kills}"
        kill_surf = self.font_hud.render(kill_str, True, COLOR_GOLD)
        surface.blit(kill_surf, (SCREEN_WIDTH // 2 + 80, 34))

        # 4. Equipped Weapons & Passives (Bottom Left)
        inv_y = SCREEN_HEIGHT - 48
        slot_x = 20
        for w in player.weapons:
            w_info = WEAPON_DATA.get(w.name, {})
            icon_key = f"icon_{w_info.get('icon', 'whip')}"
            icon_surf = self.sprite_mgr.get(icon_key)
            if icon_surf:
                surface.blit(icon_surf, (slot_x, inv_y))
                # Level text
                badge = f"L{w.level}" if w.level < w.max_level else "MAX"
                b_surf = self.font_hud_sm.render(badge, True, COLOR_GOLD if badge == "MAX" else COLOR_WHITE)
                surface.blit(b_surf, (slot_x + 2, inv_y + 22))
            slot_x += 42

        # Passives
        for p_name, p_lvl in player.passives.items():
            p_info = PASSIVE_DATA.get(p_name, {})
            icon_key = f"icon_{p_info.get('icon', 'spinach')}"
            icon_surf = self.sprite_mgr.get(icon_key)
            if icon_surf:
                surface.blit(icon_surf, (slot_x, inv_y))
                badge = f"L{p_lvl}" if p_lvl < p_info.get('max_level', 5) else "MAX"
                b_surf = self.font_hud_sm.render(badge, True, COLOR_GREEN if badge == "MAX" else COLOR_WHITE)
                surface.blit(b_surf, (slot_x + 2, inv_y + 22))
            slot_x += 42

        # Mute control hint
        mute_str = "[M] Audio: Muted" if self.sound_mgr.muted else "[M] Audio: On"
        mute_surf = self.font_hud_sm.render(mute_str, True, COLOR_GREY)
        surface.blit(mute_surf, (SCREEN_WIDTH - mute_surf.get_width() - 20, SCREEN_HEIGHT - 30))

    # ----------------------------------------------------
    # LEVEL UP SELECTION CARDS
    # ----------------------------------------------------
    def generate_level_up_choices(self, player):
        """Picks 3 or 4 randomized available upgrades."""
        available = []

        # Available Weapons
        active_weapon_names = [w.name for w in player.weapons]
        for w_name, w_data in WEAPON_DATA.items():
            existing = next((w for w in player.weapons if w.name == w_name), None)
            if existing:
                if existing.level < w_data["max_level"]:
                    available.append({
                        "key": w_name,
                        "type": "weapon",
                        "data": w_data,
                        "current_level": existing.level,
                        "next_level": existing.level + 1
                    })
            else:
                # Can acquire new weapon if fewer than 6 weapons
                if len(player.weapons) < 6:
                    available.append({
                        "key": w_name,
                        "type": "weapon",
                        "data": w_data,
                        "current_level": 0,
                        "next_level": 1
                    })

        # Available Passives
        for p_name, p_data in PASSIVE_DATA.items():
            cur_lvl = player.passives.get(p_name, 0)
            if cur_lvl < p_data["max_level"]:
                if cur_lvl > 0 or len(player.passives) < 6:
                    available.append({
                        "key": p_name,
                        "type": "passive",
                        "data": p_data,
                        "current_level": cur_lvl,
                        "next_level": cur_lvl + 1
                    })

        count = min(3, len(available))
        if count > 0:
            self.current_choices = random.sample(available, count)
        else:
            # Fallback if everything is maxed out: Rich Coins / Meat heal
            self.current_choices = [{
                "key": "HealFull",
                "type": "bonus",
                "data": {
                    "name": "Roast Chicken",
                    "desc": "Restore full HP.",
                    "icon": "heart"
                },
                "current_level": 0,
                "next_level": 1
            }]
        self.selected_index = 0

    def draw_level_up_modal(self, surface, mouse_pos):
        # Dark Dimming Backdrop
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 6, 12, 210))
        surface.blit(overlay, (0, 0))

        # Title Banner
        banner_w = 440
        banner_h = 60
        bx = (SCREEN_WIDTH - banner_w) // 2
        by = 70
        pygame.draw.rect(surface, COLOR_CRIMSON, (bx, by, banner_w, banner_h), border_radius=6)
        pygame.draw.rect(surface, COLOR_GOLD, (bx, by, banner_w, banner_h), 3, border_radius=6)
        
        title_surf = self.font_header.render("LEVEL UP!", True, COLOR_GOLD)
        surface.blit(title_surf, (bx + banner_w // 2 - title_surf.get_width() // 2, by + 10))

        # Render Cards
        card_w = 540
        card_h = 100
        start_y = 160
        spacing = 115

        for i, choice in enumerate(self.current_choices):
            cy = start_y + i * spacing
            cx = (SCREEN_WIDTH - card_w) // 2
            card_rect = pygame.Rect(cx, cy, card_w, card_h)

            # Check mouse hover
            is_hovered = card_rect.collidepoint(mouse_pos)
            if is_hovered:
                self.selected_index = i

            is_selected = (self.selected_index == i)

            # Card background
            bg_col = (45, 38, 62) if is_selected else (28, 24, 38)
            border_col = COLOR_GOLD if is_selected else (85, 75, 105)
            pygame.draw.rect(surface, bg_col, card_rect, border_radius=8)
            pygame.draw.rect(surface, border_col, card_rect, 3 if is_selected else 2, border_radius=8)

            # Hotkey indicator [1], [2], [3]
            hk_surf = self.font_hud.render(f"[{i + 1}]", True, COLOR_GOLD if is_selected else COLOR_GREY)
            surface.blit(hk_surf, (cx + 12, cy + 34))

            # Item Icon
            data = choice["data"]
            icon_key = f"icon_{data.get('icon', 'whip')}"
            icon_surf = self.sprite_mgr.get(icon_key)
            if icon_surf:
                surface.blit(icon_surf, (cx + 52, cy + 32))

            # Item Name & Level Badge
            name_txt = data["name"]
            name_surf = self.font_card_title.render(name_txt, True, COLOR_WHITE)
            surface.blit(name_surf, (cx + 100, cy + 16))

            # Level or NEW badge
            if choice["current_level"] == 0:
                badge_surf = self.font_body.render("NEW!", True, COLOR_CYAN)
            else:
                badge_surf = self.font_body.render(f"Lv {choice['current_level']} -> Lv {choice['next_level']}", True, COLOR_GOLD)
            surface.blit(badge_surf, (cx + 100 + name_surf.get_width() + 14, cy + 18))

            # Type Tag (WEAPON / PASSIVE)
            t_str = choice["type"].upper()
            t_col = COLOR_PURPLE if choice["type"] == "weapon" else COLOR_GREEN
            t_surf = self.font_hud_sm.render(t_str, True, t_col)
            surface.blit(t_surf, (cx + card_w - t_surf.get_width() - 16, cy + 18))

            # Upgrade Benefit Description
            upg_list = data.get("upgrades", [])
            next_idx = choice["next_level"] - 1
            if 0 <= next_idx < len(upg_list):
                desc_txt = upg_list[next_idx]
            else:
                desc_txt = data.get("desc", "")

            desc_surf = self.font_body.render(desc_txt, True, (215, 215, 225))
            surface.blit(desc_surf, (cx + 100, cy + 52))

    def handle_level_up_click(self, mouse_pos):
        card_w = 540
        card_h = 100
        start_y = 160
        spacing = 115

        for i, choice in enumerate(self.current_choices):
            cy = start_y + i * spacing
            cx = (SCREEN_WIDTH - card_w) // 2
            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            if card_rect.collidepoint(mouse_pos):
                return choice
        return None

    # ----------------------------------------------------
    # TITLE SCREEN
    # ----------------------------------------------------
    def draw_title_screen(self, surface, anim_timer):
        surface.fill(COLOR_BLACK)

        # Blood Moon in background
        moon_x = SCREEN_WIDTH // 2
        moon_y = 170
        pygame.draw.circle(surface, (140, 15, 25), (moon_x, moon_y), 90)
        pygame.draw.circle(surface, (190, 25, 35), (moon_x - 10, moon_y - 10), 80)
        pygame.draw.circle(surface, (230, 45, 55), (moon_x - 16, moon_y - 16), 65)

        # Title Text with drop shadow
        t1 = "CRIMSON NIGHT"
        t2 = "VAMPIRE SURVIVORS"
        
        sh1 = self.font_title.render(t1, True, (30, 0, 0))
        tx1 = self.font_title.render(t1, True, COLOR_RED)
        surface.blit(sh1, (SCREEN_WIDTH // 2 - tx1.get_width() // 2 + 3, 233))
        surface.blit(tx1, (SCREEN_WIDTH // 2 - tx1.get_width() // 2, 230))

        sh2 = self.font_header.render(t2, True, (50, 40, 10))
        tx2 = self.font_header.render(t2, True, COLOR_GOLD)
        surface.blit(sh2, (SCREEN_WIDTH // 2 - tx2.get_width() // 2 + 2, 302))
        surface.blit(tx2, (SCREEN_WIDTH // 2 - tx2.get_width() // 2, 300))

        # Instructions Box
        box_w = 480
        box_h = 170
        bx = (SCREEN_WIDTH - box_w) // 2
        by = 380
        pygame.draw.rect(surface, (25, 20, 32), (bx, by, box_w, box_h), border_radius=8)
        pygame.draw.rect(surface, (70, 60, 85), (bx, by, box_w, box_h), 2, border_radius=8)

        instructions = [
            ("WASD / ARROW KEYS", "Move Character"),
            ("AUTO-ATTACK", "Weapons fire on cooldown"),
            ("BLUE / GREEN GEMS", "Earn XP to Level Up"),
            ("CHESTS / DROPS", "Dropped by Elite Vampires")
        ]
        for i, (ctrl, desc) in enumerate(instructions):
            c_surf = self.font_hud_sm.render(ctrl, True, COLOR_GOLD)
            d_surf = self.font_hud_sm.render(desc, True, COLOR_WHITE)
            surface.blit(c_surf, (bx + 30, by + 22 + i * 34))
            surface.blit(d_surf, (bx + 200, by + 22 + i * 34))

        # Flashing "PRESS ENTER TO SURVIVE"
        if int(anim_timer * 2.0) % 2 == 0:
            start_str = "PRESS [ENTER] OR [SPACE] TO BEGIN"
            start_surf = self.font_hud.render(start_str, True, COLOR_YELLOW)
            surface.blit(start_surf, (SCREEN_WIDTH // 2 - start_surf.get_width() // 2, 590))

    # ----------------------------------------------------
    # GAME OVER SCREEN
    # ----------------------------------------------------
    def draw_game_over(self, surface, game_time, kills, level):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 5, 8, 225))
        surface.blit(overlay, (0, 0))

        over_surf = self.font_header.render("YOU HAVE FALLEN TO THE HORDE", True, COLOR_RED)
        surface.blit(over_surf, (SCREEN_WIDTH // 2 - over_surf.get_width() // 2, 170))

        mins = int(game_time) // 60
        secs = int(game_time) % 60
        stats = [
            f"Time Survived: {mins:02d}:{secs:02d}",
            f"Enemies Slain: {kills}",
            f"Level Reached: {level}"
        ]

        for i, st in enumerate(stats):
            st_surf = self.font_hud.render(st, True, COLOR_WHITE)
            surface.blit(st_surf, (SCREEN_WIDTH // 2 - st_surf.get_width() // 2, 270 + i * 45))

        restart_surf = self.font_hud.render("Press [R] to Rise Again  |  [ESC] for Title", True, COLOR_GOLD)
        surface.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, 460))

    # ----------------------------------------------------
    # CHARACTER SELECTION SCREEN
    # ----------------------------------------------------
    def draw_char_select_screen(self, surface, mouse_pos, anim_timer):
        surface.fill(COLOR_BLACK)

        # Header Title
        title_surf = self.font_header.render("CHOOSE YOUR SURVIVOR", True, COLOR_GOLD)
        surface.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 40))

        sub_surf = self.font_body.render("Select a hero to brave the vampire horde", True, COLOR_GREY)
        surface.blit(sub_surf, (SCREEN_WIDTH // 2 - sub_surf.get_width() // 2, 88))

        char_keys = ["vampire", "gunslinger", "hunter", "mage"]
        card_w = 265
        card_h = 480
        spacing = 22
        total_w = 4 * card_w + 3 * spacing
        start_x = (SCREEN_WIDTH - total_w) // 2
        start_y = 125

        for i, key in enumerate(char_keys):
            char_data = CHARACTER_DATA[key]
            cx = start_x + i * (card_w + spacing)
            cy = start_y
            card_rect = pygame.Rect(cx, cy, card_w, card_h)

            is_hovered = card_rect.collidepoint(mouse_pos)
            if is_hovered:
                self.selected_char_index = i
            is_selected = (self.selected_char_index == i)

            # Card background
            card_col = (42, 34, 58) if is_selected else (26, 22, 35)
            border_col = char_data["color"] if is_selected else (65, 58, 80)
            border_w = 3 if is_selected else 2

            pygame.draw.rect(surface, card_col, card_rect, border_radius=10)
            pygame.draw.rect(surface, border_col, card_rect, border_w, border_radius=10)

            # Hotkey badge [1], [2], [3], [4]
            hk_surf = self.font_hud.render(f"[{i + 1}]", True, char_data["color"] if is_selected else COLOR_GREY)
            surface.blit(hk_surf, (cx + 14, cy + 14))

            # Specialty Badge
            badge_txt = char_data.get("badge", "HERO")
            badge_surf = self.font_badge.render(badge_txt, True, char_data["color"])
            surface.blit(badge_surf, (cx + card_w - badge_surf.get_width() - 14, cy + 18))

            # Character Name
            name_surf = self.font_card_title.render(char_data["name"], True, COLOR_WHITE)
            surface.blit(name_surf, (cx + card_w // 2 - name_surf.get_width() // 2, cy + 46))

            # Character Title
            title_txt_surf = self.font_hud_sm.render(char_data["title"], True, COLOR_GOLD)
            surface.blit(title_txt_surf, (cx + card_w // 2 - title_txt_surf.get_width() // 2, cy + 74))

            # Pedestal & Animated Sprite Preview
            pedestal_y = cy + 160
            pygame.draw.ellipse(surface, (18, 14, 25), (cx + card_w // 2 - 45, pedestal_y + 35, 90, 20))
            pygame.draw.ellipse(surface, border_col, (cx + card_w // 2 - 45, pedestal_y + 35, 90, 20), 1)

            frames = self.sprite_mgr.get(f"player_{char_data['sprite_key']}_right")
            if frames:
                frame_idx = int(anim_timer * 4.0) % len(frames)
                spr = frames[frame_idx]
                spr_big = pygame.transform.scale2x(spr)
                surface.blit(spr_big, (cx + card_w // 2 - spr_big.get_width() // 2, pedestal_y - 25))

            # Starting Weapon Box
            wpn_box_y = cy + 235
            wpn_rect = pygame.Rect(cx + 14, wpn_box_y, card_w - 28, 54)
            pygame.draw.rect(surface, (18, 15, 24), wpn_rect, border_radius=6)
            pygame.draw.rect(surface, (55, 48, 70), wpn_rect, 1, border_radius=6)

            wpn_key = char_data["weapon"]
            w_info = WEAPON_DATA.get(wpn_key, {})
            icon_key = f"icon_{w_info.get('icon', 'whip')}"
            icon_surf = self.sprite_mgr.get(icon_key)
            if icon_surf:
                surface.blit(icon_surf, (cx + 20, wpn_box_y + 9))

            w_label = self.font_hud_sm.render("STARTING WEAPON", True, COLOR_GREY)
            w_name = self.font_body.render(w_info.get("name", wpn_key), True, COLOR_GOLD)
            surface.blit(w_label, (cx + 62, wpn_box_y + 8))
            surface.blit(w_name, (cx + 62, wpn_box_y + 26))

            # Character Description
            desc_lines = self._wrap_text(char_data["desc"], self.font_hud_sm, card_w - 28)
            for d_idx, line in enumerate(desc_lines):
                line_surf = self.font_hud_sm.render(line, True, (210, 210, 220))
                surface.blit(line_surf, (cx + 14, cy + 305 + d_idx * 18))

            # Select Button Prompt
            btn_rect = pygame.Rect(cx + 18, cy + card_h - 48, card_w - 36, 32)
            btn_bg = char_data["color"] if is_selected else (45, 38, 55)
            pygame.draw.rect(surface, btn_bg, btn_rect, border_radius=6)
            btn_txt = "PRESS TO SURVIVE" if is_selected else "SELECT HERO"
            btn_col = COLOR_WHITE if is_selected else COLOR_GREY
            btn_surf = self.font_badge.render(btn_txt, True, btn_col)
            surface.blit(btn_surf, (btn_rect.centerx - btn_surf.get_width() // 2, btn_rect.centery - btn_surf.get_height() // 2))

        # Bottom Prompt
        prompt_txt = "Press [1-4], Arrow Keys + Enter, or Click with Mouse to Select Hero"
        prompt_surf = self.font_hud_sm.render(prompt_txt, True, COLOR_YELLOW)
        surface.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, 680))

    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def handle_char_select_click(self, mouse_pos):
        char_keys = ["vampire", "gunslinger", "hunter", "mage"]
        card_w = 265
        card_h = 480
        spacing = 22
        total_w = 4 * card_w + 3 * spacing
        start_x = (SCREEN_WIDTH - total_w) // 2
        start_y = 125

        for i, key in enumerate(char_keys):
            cx = start_x + i * (card_w + spacing)
            cy = start_y
            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            if card_rect.collidepoint(mouse_pos):
                return key
        return None
