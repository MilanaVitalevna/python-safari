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

# Пути к конкретным файлам
START_SOUND_PATH = SOUNDS_PATH / "start.ogg"

# Проверяем, что папка существует (для отладки)
if not RESOURCES_PATH.exists():
    raise FileNotFoundError(f"Папка ресурсов не найдена: {RESOURCES_PATH.resolve()}")

# Регистрируем кастомный префикс для ресурсов
# Теперь можно использовать пути вида ":slot_machine:/images/..."
# Это позволяет легко ссылаться на ресурсы без полных путей
arcade.resources.add_resource_handle("slot_machine", RESOURCES_PATH)


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
