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
GALLOP_SOUND_PATH = SOUNDS_PATH / "gallop.ogg"
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

# Границы игрового поля по ширине дорожек
GAME_FIELD_LEFT = 208  # Левая граница
GAME_FIELD_RIGHT = 798  # Правая граница

# Координаты дорожек
TRACK_POSITIONS = [
    (GAME_FIELD_LEFT, 609),  # Дорожка 1: носорог ← ВЕРХ ЭКРАНА
    (GAME_FIELD_LEFT, 533),  # Дорожка 2: бизоны
    (GAME_FIELD_LEFT, 459),  # Дорожка 3: газели
    (GAME_FIELD_LEFT, 325),  # Дорожка 4: пальмы
    (GAME_FIELD_LEFT, 258),  # Дорожка 5: охотник ← НИЗ ЭКРАНА
]

# Параметры анимации дорожек
TRACK_WIDTH = 590  # Ширина текстуры дорожки в пикселях
TRACK_ANIMATION_SPEED = 30  # пикселей в секунду
TRACK_ANIMATION_AMPLITUDE = 4  # ±4 пикселя

# Константы для 4 дорожки (пальмы)
TRACK_INDEX_PALM = 3  # 4-я дорожка (индекс 3)
TRACK_Y_PALM = TRACK_POSITIONS[TRACK_INDEX_PALM][1]
PALM_SPAWN_X = GAME_FIELD_RIGHT
PALM_DESPAWN_X = GAME_FIELD_LEFT - 30
PALM_Y_OFFSET = 20  # Y-сдвиг для пальм
PALMDEAD_Y_OFFSET = 12  # Y-сдвиг для сбитых пальм

PALM_SPEED = 50  # пикселей в секунду
PALM_SPAWN_INTERVAL_MIN = 3000  # милисекунды
PALM_SPAWN_INTERVAL_MAX = 6000  # милисекунды
PALM_ALIVE_SPRITE = ":slot_machine:/images/obstacles/palm_alive.png"
PALM_DEAD_SPRITE = ":slot_machine:/images/obstacles/palm_dead.png"

# Константы для 1 дорожки (носороги)
TRACK_INDEX_RHINO = 0  # 1-я дорожка (индекс 0)
TRACK_Y_RHINO = TRACK_POSITIONS[TRACK_INDEX_RHINO][1]
RHINO_SPAWN_X = GAME_FIELD_RIGHT + 30
RHINO_DESPAWN_X = GAME_FIELD_LEFT
RHINO_Y_OFFSET = 20  # Y-сдвиг для носорогов

RHINO_SPEED = 40  # пикселей в секунду
RHINO_SPAWN_INTERVAL_MIN = 13000  # милисекунды
RHINO_SPAWN_INTERVAL_MAX = 19500  # милисекунды
RHINO_1_SPRITE = ":slot_machine:/images/animals/rhino/run_1.png"
RHINO_2_SPRITE = ":slot_machine:/images/animals/rhino/run_2.png"
RHINO_3_SPRITE = ":slot_machine:/images/animals/rhino/run_3.png"

# Константы для 2 дорожки (бизоны)
TRACK_INDEX_BIZON = 1  # 2-я дорожка (индекс 1)
TRACK_Y_BIZON = TRACK_POSITIONS[TRACK_INDEX_BIZON][1]
BIZON_SPAWN_X = GAME_FIELD_RIGHT + 30
BIZON_DESPAWN_X = GAME_FIELD_LEFT
BIZON_Y_OFFSET = 20  # Y-сдвиг для бизонов

BIZON_SPEED = 33  # пикселей в секунду
BIZON_SPAWN_INTERVAL_MIN = 4000  # милисекунды
BIZON_SPAWN_INTERVAL_MAX = 6000  # милисекунды
BIZON_1_SPRITE = ":slot_machine:/images/animals/bizon/run_1.png"
BIZON_2_SPRITE = ":slot_machine:/images/animals/bizon/run_2.png"
BIZON_3_SPRITE = ":slot_machine:/images/animals/bizon/run_3.png"

# Константы для 5 дорожки (охотник и препятствия)
HUNTER_TRACK_INDEX = 4  # 5-я дорожка (индекс 4)

# Константы для охотника
HUNTER_START_X = GAME_FIELD_LEFT + 20
HUNTER_Y_OFFSET = 12  # Y-сдвиг для охотника
HUNTER_Y = TRACK_POSITIONS[HUNTER_TRACK_INDEX][1] + HUNTER_Y_OFFSET
HUNTER_JUMP_DETECTION_DISTANCE = 23  # пикселей
HUNTER_JUMP_Y_OFFSET = 7  # пикселей (визуальное смещение вверх)

HUNTER_SPEED = 2.5  # пикселей в секунду
HUNTER_JUMP_DURATION = 900  # милисекунды
HUNTER_ANIMATION_SPEED = 120  # милисекунды
HUNTER_1_SPRITE = ":slot_machine:/images/hunter/run_1.png"
HUNTER_2_SPRITE = ":slot_machine:/images/hunter/run_2.png"
HUNTER_3_SPRITE = ":slot_machine:/images/hunter/run_3.png"
HUNTER_JUMP_SPRITE = ":slot_machine:/images/hunter/jump.png"

# Константы для барьера
TRACK_Y_BARRIER = TRACK_POSITIONS[HUNTER_TRACK_INDEX][1]
BARRIER_SPAWN_X = GAME_FIELD_RIGHT
BARRIER_DESPAWN_X = GAME_FIELD_LEFT - 30
BARRIER_Y_OFFSET = 3  # Y-сдвиг для барьера

BARRIER_SPEED = 50  # пикселей в секунду
BARRIER_SPAWN_INTERVAL_MIN = 2000  # милисекунды
BARRIER_SPAWN_INTERVAL_MAX = 4000  # милисекунды
BARRIER_SPRITE = ":slot_machine:/images/obstacles/barrier.png"

# Константы для пули
BULLET_SPRITE_PATH = ":slot_machine:/images/bullet/bullet.png"
BULLET_SPEED_X = 100  # пикселей в секунду
BULLET_SPEED_Y = 100  # пикселей в секунду
BULLET_MAX_X = 830  # правый край для удаления
BULLET_MIN_Y = 85  # нижний край для удаления
BULLET_START_OFFSET_X = 25  # смещение от позиции охотника по X
BULLET_START_OFFSET_Y = 10  # смещение от позиции охотника по Y
# Ограничения
MIN_TIME_SINCE_LAST_SHOT = 1.0  # Минимальная задержка между выстрелами
MAX_SHOTS_TOTAL = 16  # Максимум 16 выстрелов за игру

# Звуки
FIRE_SOUND_PATH = SOUNDS_PATH / "fire.ogg"
SHOT_SOUND_PATH = SOUNDS_PATH / "shot.ogg"
