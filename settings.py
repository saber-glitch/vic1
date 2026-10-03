"""
Settings and configuration for Crimson Night: Vampire Survivor.
"""

# Screen & Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "CRIMSON NIGHT: VAMPIRE SURVIVORS"

# Color Palette (Dark Gothic)
COLOR_BLACK = (10, 10, 14)
COLOR_DARK_BG = (18, 16, 26)
COLOR_FLOOR = (28, 25, 38)
COLOR_FLOOR_ALT = (32, 29, 44)
COLOR_GRID = (22, 20, 32)

COLOR_WHITE = (245, 245, 250)
COLOR_GREY = (140, 140, 155)
COLOR_DARK_GREY = (60, 60, 75)

COLOR_RED = (220, 40, 50)
COLOR_CRIMSON = (160, 20, 35)
COLOR_BLOOD = (120, 10, 20)

COLOR_GOLD = (255, 205, 50)
COLOR_YELLOW = (255, 235, 90)
COLOR_AMBER = (230, 140, 30)

COLOR_BLUE = (60, 160, 255)
COLOR_CYAN = (80, 230, 240)
COLOR_PURPLE = (175, 75, 255)
COLOR_VIOLET = (120, 45, 200)

COLOR_GREEN = (50, 215, 90)
COLOR_EMERALD = (30, 170, 70)

# XP & Leveling Constants
BASE_XP_TO_LEVEL = 5
XP_GROWTH_FACTOR = 1.35

# Player Defaults
PLAYER_BASE_HP = 100
PLAYER_BASE_SPEED = 230.0
PLAYER_BASE_MAGNET = 90.0
PLAYER_BASE_REGEN = 0.2
PLAYER_BASE_MIGHT = 1.0
PLAYER_BASE_COOLDOWN = 1.0
PLAYER_BASE_AREA = 1.0
PLAYER_BASE_ARMOR = 0

# Upgrade Definitions
WEAPON_DATA = {
    "Whip": {
        "name": "Holy Whip",
        "desc": "Slashes horizontally, striking all enemies in front.",
        "type": "weapon",
        "icon": "whip",
        "max_level": 8,
        "upgrades": [
            "Deals horizontal slash damage.",
            "+20% Damage & +15% Slash Area.",
            "+1 Extra Slash behind you.",
            "+25% Damage & +10% Slash Area.",
            "+1 Additional Slash in front.",
            "+30% Damage & +15% Slash Area.",
            "+1 Additional Slash behind.",
            "+50% Damage & Critical strike chance."
        ]
    },
    "MagicWand": {
        "name": "Magic Wand",
        "desc": "Fires swift arcane bolts at the nearest foe.",
        "type": "weapon",
        "icon": "wand",
        "max_level": 8,
        "upgrades": [
            "Fires arcane projectiles at closest enemy.",
            "+1 Additional Projectile.",
            "-15% Cooldown reduction.",
            "+1 Additional Projectile.",
            "+25% Damage per bolt.",
            "+1 Additional Projectile.",
            "-20% Cooldown reduction.",
            "+2 Additional Projectiles & Pierce +1."
        ]
    },
    "Garlic": {
        "name": "Garlic Aura",
        "desc": "Damages nearby enemies in a pulsating holy circle.",
        "type": "weapon",
        "icon": "garlic",
        "max_level": 8,
        "upgrades": [
            "Creates a protective damaging aura around player.",
            "+20% Aura Area & +10% Damage.",
            "+20% Knockback force.",
            "+25% Aura Area & +15% Damage.",
            "-15% Tick interval (faster hits).",
            "+30% Aura Area.",
            "+30% Damage.",
            "Maximum aura size & slight life drain chance."
        ]
    },
    "HolyWater": {
        "name": "Holy Water",
        "desc": "Throws blessed vials that create pools of holy fire.",
        "type": "weapon",
        "icon": "holy_water",
        "max_level": 8,
        "upgrades": [
            "Lobs 1 vial creating a pool of holy flame.",
            "+1 Additional Vial thrown.",
            "+25% Pool Duration & +20% Area.",
            "+1 Additional Vial thrown.",
            "+30% Holy Fire Damage.",
            "+1 Additional Vial thrown.",
            "+25% Area & -15% Cooldown.",
            "+2 Additional Vials & Massive inferno."
        ]
    },
    "KingBible": {
        "name": "King's Bible",
        "desc": "Holy grimoires orbit around you, shredding attackers.",
        "type": "weapon",
        "icon": "bible",
        "max_level": 8,
        "upgrades": [
            "1 Holy Bible orbits around player.",
            "+1 Additional Orbiting Bible.",
            "+25% Rotation Speed & +20% Duration.",
            "+1 Additional Orbiting Bible.",
            "+30% Damage & +15% Orbit Area.",
            "+1 Additional Orbiting Bible.",
            "+25% Rotation Speed.",
            "+2 Additional Bibles (Continuous wall!)."
        ]
    },
    "LightningRing": {
        "name": "Lightning Ring",
        "desc": "Calls down divine thunderbolts upon random enemies.",
        "type": "weapon",
        "icon": "lightning",
        "max_level": 8,
        "upgrades": [
            "Strikes 2 random enemies with lightning.",
            "+1 Lightning strike count.",
            "+30% Thunderbolt Damage.",
            "+1 Lightning strike count.",
            "+25% Blast splash radius.",
            "+2 Lightning strike counts.",
            "-20% Cooldown reduction.",
            "+3 Lightning strike counts & catastrophic blast."
        ]
    },
    "DualPistols": {
        "name": "Dual Pistols",
        "desc": "Rapidly fires alternating silver bullets towards your mouse cursor.",
        "type": "weapon",
        "icon": "pistol",
        "max_level": 8,
        "upgrades": [
            "Fires high-velocity silver bullets towards cursor.",
            "+1 Extra bullet per volley & +15% Damage.",
            "-15% Cooldown reduction.",
            "+1 Extra bullet per volley.",
            "+20% Damage & Bullets pierce 1 enemy.",
            "+2 Extra bullets per volley.",
            "-20% Cooldown reduction.",
            "Twin Gilded Revolvers: High-speed barrage with +2 Pierce!"
        ]
    },
    "BloodTear": {
        "name": "Blood Tear",
        "desc": "Slashes crescent blood waves towards mouse with life-steal.",
        "type": "weapon",
        "icon": "blood",
        "max_level": 8,
        "upgrades": [
            "Slashes crimson blood arcs towards your cursor.",
            "+20% Blood Wave Area & +15% Damage.",
            "+1 Additional Blood Arc.",
            "+25% Damage & +10% Life drain chance.",
            "+1 Additional Blood Arc.",
            "+30% Damage & +20% Area.",
            "-15% Cooldown reduction.",
            "Sanguine Tempest: 4 Blood Scythes that pierce all enemies!"
        ]
    }
}

PASSIVE_DATA = {
    "Spinach": {
        "name": "Spinach",
        "desc": "Raises overall damage output.",
        "type": "passive",
        "icon": "spinach",
        "max_level": 5,
        "upgrades": [
            "+10% Damage to all weapons.",
            "+10% Damage to all weapons.",
            "+10% Damage to all weapons.",
            "+10% Damage to all weapons.",
            "+10% Damage to all weapons."
        ]
    },
    "HollowHeart": {
        "name": "Hollow Heart",
        "desc": "Augments maximum health capacity.",
        "type": "passive",
        "icon": "heart",
        "max_level": 5,
        "upgrades": [
            "+20% Max Health & restores 20 HP.",
            "+20% Max Health & restores 20 HP.",
            "+20% Max Health & restores 20 HP.",
            "+20% Max Health & restores 20 HP.",
            "+20% Max Health & restores 20 HP."
        ]
    },
    "Wings": {
        "name": "Wings",
        "desc": "Increases character movement speed.",
        "type": "passive",
        "icon": "wings",
        "max_level": 5,
        "upgrades": [
            "+12% Movement Speed.",
            "+12% Movement Speed.",
            "+12% Movement Speed.",
            "+12% Movement Speed.",
            "+12% Movement Speed."
        ]
    },
    "Crown": {
        "name": "Crown",
        "desc": "Character earns more experience gems.",
        "type": "passive",
        "icon": "crown",
        "max_level": 5,
        "upgrades": [
            "+15% Experience Gain.",
            "+15% Experience Gain.",
            "+15% Experience Gain.",
            "+15% Experience Gain.",
            "+15% Experience Gain."
        ]
    },
    "Attractorb": {
        "name": "Attractorb",
        "desc": "Magnetically pulls pickups from further away.",
        "type": "passive",
        "icon": "magnet",
        "max_level": 5,
        "upgrades": [
            "+35% Pickup Magnet Radius.",
            "+35% Pickup Magnet Radius.",
            "+35% Pickup Magnet Radius.",
            "+35% Pickup Magnet Radius.",
            "+35% Pickup Magnet Radius."
        ]
    },
    "ArmorPlate": {
        "name": "Armor Plate",
        "desc": "Reduces damage taken from all sources.",
        "type": "passive",
        "icon": "armor",
        "max_level": 5,
        "upgrades": [
            "Reduces incoming damage by 1.",
            "Reduces incoming damage by 1.",
            "Reduces incoming damage by 1.",
            "Reduces incoming damage by 1.",
            "Reduces incoming damage by 1."
        ]
    },
    "Pummarola": {
        "name": "Pummarola",
        "desc": "Character slowly regenerates health over time.",
        "type": "passive",
        "icon": "pummarola",
        "max_level": 5,
        "upgrades": [
            "+0.4 HP Regenerated per second.",
            "+0.4 HP Regenerated per second.",
            "+0.4 HP Regenerated per second.",
            "+0.4 HP Regenerated per second.",
            "+0.4 HP Regenerated per second."
        ]
    },
    "EmptyTome": {
        "name": "Empty Tome",
        "desc": "Reduces weapon cooldowns across the board.",
        "type": "passive",
        "icon": "tome",
        "max_level": 5,
        "upgrades": [
            "-8% Cooldown reduction.",
            "-8% Cooldown reduction.",
            "-8% Cooldown reduction.",
            "-8% Cooldown reduction.",
            "-8% Cooldown reduction."
        ]
    }
}

# Dash Mechanics
DASH_COOLDOWN = 2.0
DASH_SPEED = 720.0
DASH_DURATION = 0.18

# Playable Characters
CHARACTER_DATA = {
    "vampire": {
        "id": "vampire",
        "name": "Vlad",
        "title": "Lord of Blood",
        "desc": "Strikes with Blood Tear. Inherent health regeneration & life-steal.",
        "weapon": "BloodTear",
        "sprite_key": "vampire",
        "hp_bonus": 25,
        "speed_mult": 1.0,
        "might_mult": 1.05,
        "cooldown_mult": 1.0,
        "regen_bonus": 0.6,
        "armor_bonus": 0,
        "color": COLOR_RED,
        "badge": "LIFESTEAL"
    },
    "gunslinger": {
        "id": "gunslinger",
        "name": "Drake",
        "title": "Twin Revolver Vigilante",
        "desc": "Fires rapid Dual Pistols with boosted agility and swift movement.",
        "weapon": "DualPistols",
        "sprite_key": "gunslinger",
        "hp_bonus": 0,
        "speed_mult": 1.18,
        "might_mult": 1.10,
        "cooldown_mult": 0.95,
        "regen_bonus": 0.1,
        "armor_bonus": 0,
        "color": COLOR_AMBER,
        "badge": "HIGH SPEED"
    },
    "hunter": {
        "id": "hunter",
        "name": "Simon",
        "title": "Whip Scourge",
        "desc": "Master of the Holy Whip. Sturdy warrior with bonus armor & survivability.",
        "weapon": "Whip",
        "sprite_key": "hunter",
        "hp_bonus": 15,
        "speed_mult": 1.0,
        "might_mult": 1.0,
        "cooldown_mult": 1.0,
        "regen_bonus": 0.3,
        "armor_bonus": 1,
        "color": COLOR_CRIMSON,
        "badge": "BALANCED & ARMOR"
    },
    "mage": {
        "id": "mage",
        "name": "Eldrin",
        "title": "Arcane Spellweaver",
        "desc": "Wields the Magic Wand with rapid spellcasting and cooldown reduction.",
        "weapon": "MagicWand",
        "sprite_key": "mage",
        "hp_bonus": -15,
        "speed_mult": 1.02,
        "might_mult": 1.15,
        "cooldown_mult": 0.82,
        "regen_bonus": 0.2,
        "armor_bonus": 0,
        "color": COLOR_CYAN,
        "badge": "FAST COOLDOWNS"
    }
}

