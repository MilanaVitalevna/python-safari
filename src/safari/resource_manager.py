"""
Инициализация внешних ресурсов: шрифты, пути, кастомные префиксы.
"""

import arcade

from .constants import AVENTURA_FONT_PATH, RESOURCES_PATH, RESOURCES_PREFIX, SAFARI_FONT_PATH


def load_fonts():
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


def setup_resources():
    # Проверяем, что папка существует (для отладки)
    if not RESOURCES_PATH.exists():
        raise FileNotFoundError(f"Папка ресурсов не найдена: {RESOURCES_PATH.resolve()}")

    # Регистрируем собственный префикс для ресурсов
    # Теперь можно использовать пути вида ":slot_machine:/images/..."
    # Это позволяет легко ссылаться на ресурсы без полных путей
    arcade.resources.add_resource_handle(RESOURCES_PREFIX, RESOURCES_PATH)

    load_fonts()
