"""
Procedural Retro Audio Synthesizer for Crimson Night.
Generates 16-bit PCM retro sounds in-memory without external asset dependencies.
"""

import io
import math
import random
import wave
import pygame

class SoundManager:
    def __init__(self):
        self.muted = False
        self.volume = 0.6
        self.sounds = {}
        self.initialized = False
        
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.initialized = True
            self._generate_all_sounds()
        except Exception as e:
            print(f"[SoundManager] Warning: Audio init failed ({e}), continuing muted.")
            self.initialized = False

    def _create_wav_sound(self, sample_rate, duration, sample_generator):
        """Build a pygame.mixer.Sound from a math sample generator."""
        total_samples = int(sample_rate * duration)
        raw_bytes = bytearray()
        
        for i in range(total_samples):
            t = i / float(sample_rate)
            # Generator should return float in range [-1.0, 1.0]
            val = sample_generator(t, i, total_samples)
            val = max(-1.0, min(1.0, val))
            sample_val = int(val * 28000)
            # Mono 16-bit signed
            raw_bytes += sample_val.to_bytes(2, byteorder='little', signed=True)
            
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            w.writeframes(raw_bytes)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_all_sounds(self):
        sr = 22050

        # 1. Gem Pickup: Clean ascending crystal chime (high pitch)
        def gem_gen(t, i, n):
            env = math.exp(-t * 12.0)
            f = 880.0 + 880.0 * (i / n)
            return (math.sin(2 * math.pi * f * t) * 0.6 + 
                    math.sin(2 * math.pi * f * 2 * t) * 0.3) * env
        self.sounds["gem"] = self._create_wav_sound(sr, 0.14, gem_gen)

        # 2. Whip Whoosh: Fast sweeping noise with snap
        def whip_gen(t, i, n):
            env = math.sin(math.pi * (i / n))
            # mix of swoosh sine and noise
            noise = (random.random() * 2.0 - 1.0) * 0.4
            freq = 400.0 - 250.0 * (i / n)
            sine = math.sin(2 * math.pi * freq * t) * 0.6
            return (sine + noise) * env
        self.sounds["whip"] = self._create_wav_sound(sr, 0.18, whip_gen)

        # 3. Magic Wand Bolt: Arcane spark chirp
        def magic_gen(t, i, n):
            env = math.exp(-t * 10.0)
            freq = 1100.0 - 600.0 * (i / n)
            s = math.sin(2 * math.pi * freq * t)
            harm = math.sin(2 * math.pi * freq * 1.5 * t) * 0.4
            return (s + harm) * env * 0.7
        self.sounds["magic"] = self._create_wav_sound(sr, 0.12, magic_gen)

        # 4. Enemy Hit: Short thud/crunch
        def hit_gen(t, i, n):
            env = math.exp(-t * 22.0)
            freq = 160.0 - 80.0 * (i / n)
            noise = (random.random() * 2.0 - 1.0) * 0.35
            return (math.sin(2 * math.pi * freq * t) * 0.7 + noise) * env
        self.sounds["hit"] = self._create_wav_sound(sr, 0.09, hit_gen)

        # 5. Player Hurt: Low impact grunt
        def player_hurt_gen(t, i, n):
            env = math.exp(-t * 14.0)
            freq = 120.0 - 50.0 * (i / n)
            noise = (random.random() * 2.0 - 1.0) * 0.3
            return (math.sin(2 * math.pi * freq * t) * 0.8 + noise) * env
        self.sounds["player_hurt"] = self._create_wav_sound(sr, 0.22, player_hurt_gen)

        # 6. Level Up Fanfare: 4-note ascending chord arpeggio
        def levelup_gen(t, i, n):
            step = int(t * 8.0)
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            freq = notes[min(step, len(notes) - 1)]
            env = math.exp(-(t % 0.125) * 6.0)
            return (math.sin(2 * math.pi * freq * t) * 0.6 + 
                    math.sin(2 * math.pi * freq * 2 * t) * 0.2) * env
        self.sounds["levelup"] = self._create_wav_sound(sr, 0.55, levelup_gen)

        # 7. Explosion / Holy Fire: Deep rumbling burst
        def explode_gen(t, i, n):
            env = math.exp(-t * 5.0)
            noise = (random.random() * 2.0 - 1.0)
            sub = math.sin(2 * math.pi * (90.0 - 50.0 * (i / n)) * t) * 0.7
            return (noise * 0.6 + sub) * env
        self.sounds["explosion"] = self._create_wav_sound(sr, 0.35, explode_gen)

        # 8. Lightning Strike: Electrifying thunder crack
        def lightning_gen(t, i, n):
            env = math.exp(-t * 7.0)
            noise = (random.random() * 2.0 - 1.0) * 0.7
            buzz = math.sin(2 * math.pi * 180.0 * t) * 0.4
            return (noise + buzz) * env
        self.sounds["lightning"] = self._create_wav_sound(sr, 0.28, lightning_gen)

        # 9. Chest Fanfare: Sparkling victory chime
        def chest_gen(t, i, n):
            notes = [440, 554, 659, 880, 1108, 1318]
            idx = min(int(t * 10), len(notes) - 1)
            f = notes[idx]
            env = math.exp(-(t % 0.1) * 8.0)
            return math.sin(2 * math.pi * f * t) * 0.5 * env
        self.sounds["chest"] = self._create_wav_sound(sr, 0.7, chest_gen)

        # 10. Rosary: Divine radiant flash sweep
        def rosary_gen(t, i, n):
            env = math.exp(-t * 3.5)
            f = 300.0 + 1200.0 * math.sin(t * 10.0)
            return math.sin(2 * math.pi * f * t) * 0.6 * env
        self.sounds["rosary"] = self._create_wav_sound(sr, 0.6, rosary_gen)

        # 11. UI Click: Snappy blip
        def click_gen(t, i, n):
            env = math.exp(-t * 40.0)
            return math.sin(2 * math.pi * 950.0 * t) * 0.6 * env
        self.sounds["click"] = self._create_wav_sound(sr, 0.05, click_gen)

        # 12. Gunshot: Punchy crack + powder burst
        def gun_gen(t, i, n):
            env = math.exp(-t * 28.0)
            noise = (random.random() * 2.0 - 1.0) * 0.8
            crack = math.sin(2 * math.pi * 320.0 * t) * 0.5
            return (noise + crack) * env
        self.sounds["gunshot"] = self._create_wav_sound(sr, 0.12, gun_gen)

        # 13. Dash Whoosh: Phasing spectral gust
        def dash_gen(t, i, n):
            env = math.sin(math.pi * (i / n))
            f = 450.0 + 350.0 * math.sin(t * 30.0)
            noise = (random.random() * 2.0 - 1.0) * 0.4
            return (math.sin(2 * math.pi * f * t) * 0.6 + noise) * env
        self.sounds["dash"] = self._create_wav_sound(sr, 0.16, dash_gen)

        # 14. Blood Slash: Visceral sanguine slice
        def blood_gen(t, i, n):
            env = math.exp(-t * 14.0)
            f = 240.0 - 100.0 * (i / n)
            noise = (random.random() * 2.0 - 1.0) * 0.45
            return (math.sin(2 * math.pi * f * t) * 0.7 + noise) * env
        self.sounds["blood_slash"] = self._create_wav_sound(sr, 0.15, blood_gen)

        # Set default sound volumes
        self.set_volume(self.volume)

    def play(self, sound_name):
        """Play a registered sound effect if not muted."""
        if self.muted or not self.initialized:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()

    def toggle_mute(self):
        """Toggle mute status."""
        self.muted = not self.muted
        return self.muted

    def set_volume(self, vol):
        """Set volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, vol))
        for snd in self.sounds.values():
            snd.set_volume(self.volume)
