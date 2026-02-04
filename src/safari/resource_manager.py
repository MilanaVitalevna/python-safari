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
    BUTTON_PRESSED_SPRITE,
    FIRE_SOUND_PATH,
    GAZELLE_1_SPRITE,
    GAZELLE_2_SPRITE,
    GAZELLE_3_SPRITE,
    HUNTER_1_SPRITE,
    HUNTER_2_SPRITE,
    HUNTER_3_SPRITE,
    HUNTER_JUMP_DURATION,
    HUNTER_JUMP_SPRITE,
    PALM_ALIVE_SPRITE,
    PALM_DEAD_SPRITE,
    RESOURCES_PATH,
    RESOURCES_PREFIX,
    RHINO_1_SPRITE,
    RHINO_2_SPRITE,
    RHINO_3_SPRITE,
    SAFARI_FONT_PATH,
    SHOT_INDICATOR_PATHS,
    SHOT_SOUND_PATH,
)


# Простой DateTransferObject для текстур
@dataclass
class Textures:
    """Простой контейнер для всех загруженных текстур, анимаций и звуков."""

    # Анимации животных
    rhino_animation: arcade.TextureAnimation | None = None
    bizon_animation: arcade.TextureAnimation | None = None
    gazelle_animation: arcade.TextureAnimation | None = None

    # Анимации охотника
    hunter_run_animation: arcade.TextureAnimation | None = None
    hunter_jump_animation: arcade.TextureAnimation | None = None

    # Текстуры пальмы
    palm_alive: arcade.Texture = None
    palm_dead: arcade.Texture = None

    # Текстура барьера
    barrier: arcade.Texture = None

    # Текстура пули
    bullet: arcade.Texture = None

    # Текстуры индикаторов выстрелов (список из 16 текстур)
    shot_indicators: list[arcade.Texture] = field(default_factory=list)

    # Текстура кнопки стрельбы
    button_pressed: arcade.Texture = None

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

    # Загружаем текстуру пули
    try:
        Textures.bullet = arcade.load_texture(BULLET_SPRITE_PATH)
        print("✅ Загружена текстура пули")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстуры пули: {e}")

    # Загружаем текстуры индикаторов выстрелов
    try:
        Textures.shot_indicators = []
        for _i, path in enumerate(SHOT_INDICATOR_PATHS):
            texture = arcade.load_texture(path)
            Textures.shot_indicators.append(texture)
        print(f"✅ Загружены {len(Textures.shot_indicators)} текстур индикаторов выстрелов")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстур индикаторов: {e}")
        Textures.shot_indicators = []

    # Загружаем текстуру нажатой кнопки
    try:
        Textures.button_pressed = arcade.load_texture(BUTTON_PRESSED_SPRITE)
        print("✅ Загружена текстура нажатой кнопки")
    except Exception as e:
        print(f"❌ Ошибка загрузки текстуры кнопки: {e}")

    print("🎨 Загрузка текстур завершена")


def load_sounds():
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


def create_animations():
    """Создает все анимации игры."""

    print("🎬 Создание анимаций...")
    # Носорог (прямая загрузка текстур в keyframes)
    try:
        keyframes = [
            arcade.TextureKeyframe(arcade.load_texture(RHINO_1_SPRITE), 120),
            arcade.TextureKeyframe(arcade.load_texture(RHINO_2_SPRITE), 80),
            arcade.TextureKeyframe(arcade.load_texture(RHINO_3_SPRITE), 120),
        ]
        Textures.rhino_animation = arcade.TextureAnimation(keyframes)
        print("✅ Создана анимация носорога")
    except Exception as e:
        print(f"❌ Ошибка создания анимации носорога: {e}")
        Textures.rhino_animation = None

    # Бизон (прямая загрузка текстур в keyframes)
    try:
        keyframes = [
            arcade.TextureKeyframe(arcade.load_texture(BIZON_1_SPRITE), 100),
            arcade.TextureKeyframe(arcade.load_texture(BIZON_2_SPRITE), 100),
            arcade.TextureKeyframe(arcade.load_texture(BIZON_3_SPRITE), 100),
        ]
        Textures.bizon_animation = arcade.TextureAnimation(keyframes)
        print("✅ Создана анимация бизона")
    except Exception as e:
        print(f"❌ Ошибка создания анимации бизона: {e}")
        Textures.bizon_animation = None

    # Газель (прямая загрузка текстур в keyframes)
    try:
        keyframes = [
            arcade.TextureKeyframe(arcade.load_texture(GAZELLE_1_SPRITE), 100),
            arcade.TextureKeyframe(arcade.load_texture(GAZELLE_2_SPRITE), 100),
            arcade.TextureKeyframe(arcade.load_texture(GAZELLE_3_SPRITE), 100),
        ]
        Textures.gazelle_animation = arcade.TextureAnimation(keyframes)
        print("✅ Создана анимация газели")
    except Exception as e:
        print(f"❌ Ошибка создания анимации газели: {e}")
        Textures.gazelle_animation = None

    try:
        # Анимация бега охотника
        hunter_run_keyframes = [
            arcade.TextureKeyframe(arcade.load_texture(HUNTER_1_SPRITE)),
            arcade.TextureKeyframe(arcade.load_texture(HUNTER_2_SPRITE)),
            arcade.TextureKeyframe(arcade.load_texture(HUNTER_3_SPRITE)),
        ]
        Textures.hunter_run_animation = arcade.TextureAnimation(hunter_run_keyframes)
        print("✅ Создана анимация бега охотника")

        # Анимация прыжка охотника (можно сделать из одного кадра)
        hunter_jump_keyframes = [
            arcade.TextureKeyframe(arcade.load_texture(HUNTER_JUMP_SPRITE), HUNTER_JUMP_DURATION),
        ]
        Textures.hunter_jump_animation = arcade.TextureAnimation(hunter_jump_keyframes)
        print("✅ Создана анимация прыжка охотника")

    except Exception as e:
        print(f"❌ Ошибка создания анимаций охотника: {e}")
        Textures.hunter_run_animation = None
        Textures.hunter_jump_animation = None

    print("🎬 Анимации созданы")


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

    # 4. Загружаем звуки
    load_sounds()

    # 4. Создаем анимации
    create_animations()
