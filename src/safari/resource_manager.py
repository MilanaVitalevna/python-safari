"""
Инициализация внешних ресурсов: шрифты, пути, кастомные префиксы.
"""

from dataclasses import dataclass, field

import arcade

from .constants import (
    AVENTURA_FONT_PATH,
    BARRIER_SPRITE,
    BIZON_1_SPRITE,
    BIZON_2_SPRITE,
    BIZON_3_SPRITE,
    BULLET_SPRITE_PATH,
    FIRE_SOUND_PATH,
    HUNTER_1_SPRITE,
    HUNTER_2_SPRITE,
    HUNTER_3_SPRITE,
    HUNTER_JUMP_SPRITE,
    PALM_ALIVE_SPRITE,
    PALM_DEAD_SPRITE,
    RESOURCES_PATH,
    RESOURCES_PREFIX,
    RHINO_1_SPRITE,
    RHINO_2_SPRITE,
    RHINO_3_SPRITE,
    SAFARI_FONT_PATH,
    SHOT_SOUND_PATH,
)


# Простой DateTransferObject для текстур
@dataclass
class Textures:
    """Простой контейнер для всех загруженных текстур."""

    # Текстуры носорога
    rhino: list[arcade.Texture] = field(default_factory=list)

    # Текстуры пальмы
    palm_alive: arcade.Texture = None
    palm_dead: arcade.Texture = None

    # Текстура барьера
    barrier: arcade.Texture = None

    # Текстуры охотника
    hunter: list[arcade.Texture] = field(default_factory=list)

    # Текстура пули
    bullet: arcade.Texture = None

    # Звуки
    fire_sound: arcade.Sound = None
    shot_sound: arcade.Sound = None


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


def load_textures():
    """Загрузка всех текстур в Textures."""
    print("🎨 Загрузка текстур...")

    # Загружаем текстуры носорога
    try:
        Textures.rhino = [
            arcade.load_texture(RHINO_1_SPRITE),
            arcade.load_texture(RHINO_2_SPRITE),
            arcade.load_texture(RHINO_3_SPRITE),
        ]
        print(f"✅ Загружены {len(Textures.rhino)} текстур носорога")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур носорога: {e}")
        Textures.rhino = []

    # Загружаем текстуры бизона
    try:
        Textures.bizon = [
            arcade.load_texture(BIZON_1_SPRITE),
            arcade.load_texture(BIZON_2_SPRITE),
            arcade.load_texture(BIZON_3_SPRITE),
        ]
        print(f"✅ Загружены {len(Textures.bizon)} текстур бизона")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур бизона: {e}")
        Textures.bizon = []

    # Загружаем текстуры пальмы
    try:
        Textures.palm_alive = arcade.load_texture(PALM_ALIVE_SPRITE)
        Textures.palm_dead = arcade.load_texture(PALM_DEAD_SPRITE)
        print("✅ Загружены текстуры пальмы")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур пальмы: {e}")

    # Загружаем текстуру барьера
    try:
        if BARRIER_SPRITE is not None:
            Textures.barrier = arcade.load_texture(BARRIER_SPRITE)
            print("✅ Загружена текстура барьера")
        else:
            print("⚠️ BARRIER_SPRITE не определен")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстуры барьера: {e}")

    # Загружаем текстуры охотника
    try:
        Textures.hunter = [
            arcade.load_texture(HUNTER_1_SPRITE),
            arcade.load_texture(HUNTER_2_SPRITE),
            arcade.load_texture(HUNTER_3_SPRITE),
            arcade.load_texture(HUNTER_JUMP_SPRITE),
        ]
        print(f"✅ Загружены {len(Textures.hunter)} текстур охотника")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур охотника: {e}")
        Textures.hunter = []

    # Загружаем текстуру пули
    try:
        Textures.bullet = arcade.load_texture(BULLET_SPRITE_PATH)
        print("✅ Загружена текстура пули")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстуры пули: {e}")

    # Загружаем звуки для стрельбы
    try:
        if FIRE_SOUND_PATH.exists():
            Textures.fire_sound = arcade.load_sound(FIRE_SOUND_PATH)
            print("✅ Загружен звук выстрела")
    except Exception as e:
        print(f"❌ Ошибка загрузки звука выстрела: {e}")

    try:
        if SHOT_SOUND_PATH.exists():
            Textures.shot_sound = arcade.load_sound(SHOT_SOUND_PATH)
            print("✅ Загружен звук попадания")
    except Exception as e:
        print(f"❌ Ошибка загрузки звука попадания: {e}")

    print("🎨 Загрузка текстур завершена")


def setup_resources():
    # Проверяем, что папка существует (для отладки)
    if not RESOURCES_PATH.exists():
        raise FileNotFoundError(f"Папка ресурсов не найдена: {RESOURCES_PATH.resolve()}")

    # 1. Регистрируем собственный префикс для ресурсов
    # Теперь можно использовать пути вида ":slot_machine:/images/..."
    # Это позволяет легко ссылаться на ресурсы без полных путей
    arcade.resources.add_resource_handle(RESOURCES_PREFIX, RESOURCES_PATH)

    # 2. Загружаем шрифты
    load_fonts()

    # 3. Загружаем текстуры
    load_textures()
