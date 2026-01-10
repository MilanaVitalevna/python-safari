"""
Game constants
"""

from pathlib import Path

import arcade

# Определяем корень проекта: src/safari -> src -> project_root
PROJECT_ROOT = Path(__file__).parent.parent.parent
RESOURCES_PATH = PROJECT_ROOT / "resources"

# Пути к ресурсам
SOUNDS_PATH = RESOURCES_PATH / "sounds"
IMAGES_PATH = RESOURCES_PATH / "images"
FONTS_PATH = RESOURCES_PATH / "fonts"

# Пути к конкретным файлам
START_SOUND_PATH = SOUNDS_PATH / "start.ogg"
SAFARI_FONT_PATH = FONTS_PATH / "safari-game-regular.ttf"
AVENTURA_FONT_PATH = FONTS_PATH / "aventura-bold.ttf"

# Проверяем, что папка существует (для отладки)
if not RESOURCES_PATH.exists():
    raise FileNotFoundError(f"Папка ресурсов не найдена: {RESOURCES_PATH.resolve()}")

# Регистрируем собственный префикс для ресурсов
# Теперь можно использовать пути вида ":slot_machine:/images/..."
# Это позволяет легко ссылаться на ресурсы без полных путей
arcade.resources.add_resource_handle("slot_machine", RESOURCES_PATH)

# 💾 Загружаем особенные шрифты при инициализации констант
# Это гарантирует, что шрифт будет доступен при создании Text
try:
    # Загружаем шрифт Safari
    if SAFARI_FONT_PATH.exists():
        arcade.load_font(SAFARI_FONT_PATH)
    else:
        print(f"⚠️ Шрифт не найден: {SAFARI_FONT_PATH}")

    # Загружаем шрифт Adventura
    if AVENTURA_FONT_PATH.exists():
        arcade.load_font(AVENTURA_FONT_PATH)
    else:
        print(f"⚠️ Шрифт не найден: {AVENTURA_FONT_PATH}")
except Exception as e:
    print(f"❌ Ошибка загрузки шрифта: {e}")


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
