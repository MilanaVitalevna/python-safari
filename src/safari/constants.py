"""
Центральное хранилище констант, путей и ресурсов.

Содержит:
- Размеры экрана
- Цвета
- Пути к изображениям, звукам, шрифтам
"""

from pathlib import Path

# Определяем корень проекта: src/safari -> src -> project_root
PROJECT_ROOT = Path(__file__).parent.parent.parent
RESOURCES_PATH = PROJECT_ROOT / "resources"
RESOURCES_PREFIX = "slot_machine"

# Пути к ресурсам
SOUNDS_PATH = RESOURCES_PATH / "sounds"
IMAGES_PATH = RESOURCES_PATH / "images"
FONTS_PATH = RESOURCES_PATH / "fonts"

# Пути к конкретным файлам
START_SOUND_PATH = SOUNDS_PATH / "start.ogg"
SAFARI_FONT_PATH = FONTS_PATH / "safari-game-regular.ttf"
AVENTURA_FONT_PATH = FONTS_PATH / "aventura-bold.ttf"

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
SCREEN_TITLE = "САФАРИ - игра из советских игровых автоматов"

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Black
TEXT_COLOR = (255, 255, 255)  # White

# Ресурсы (если нужно, можно вынести и их пути)
TV_BACKGROUND = ":slot_machine:/images/ui/bg_back.png"
GLARE_EFFECT = ":slot_machine:/images/ui/bg_front.png"
SLOT_MACHINE_FRAME = ":slot_machine:/images/ui/slot_machine.png"

# Название шрифта для использования в Text
SAFARI_FONT_NAME = "Safari_game"
AVENTURA_FONT_NAME = "Aventura"

# Координаты дорожек
TRACK_POSITIONS = [
    (208, 609),  # Дорожка 1: носорог ← ВЕРХ
    (208, 533),  # Дорожка 2: быки
    (208, 459),  # Дорожка 3: газели
    (208, 325),  # Дорожка 4: пальмы
    (208, 258),  # Дорожка 5: охотник ← НИЗ
]

# Параметры анимации дорожек
TRACK_WIDTH = 590  # Ширина текстуры дорожки в пикселях
TRACK_ANIMATION_SPEED = 30  # пикселей в секунду
TRACK_ANIMATION_AMPLITUDE = 4  # ±4 пикселя
