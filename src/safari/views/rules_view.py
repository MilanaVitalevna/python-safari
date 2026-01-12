"""
Сцена: экран с правилами игры.

Отображает фон автомата и поверх — модальное окно с правилами.
Запускает стартовый звук и позволяет игроку:
- Пропустить анимацию по нажатию Пробел
- Перейти к игре
- Выйти по ESC

После перехода — звук останавливается.
"""

import arcade

from ..constants import (
    GLARE_EFFECT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLOT_MACHINE_FRAME,
    START_SOUND_PATH,
    TV_BACKGROUND,
)
from ..ui.rules_window import RulesManager


class RulesView(arcade.View):
    """Сцена: окно с правилами игры с анимацией появления и стартовым звуком."""

    def __init__(self):
        super().__init__()

        # Слои фона
        self.background_sprites = arcade.SpriteList()  # ТВ-экран
        self.effect_sprites = arcade.SpriteList()  # Блик
        self.slot_machine_sprite = arcade.SpriteList()  # Рамка автомата

        # UI: окно правил
        self.rules_manager = RulesManager(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Звук
        self.start_sound_player = None

        # Загружаем спрайты и запускаем звук
        self.setup()

    def setup(self):
        """Загрузка всех спрайтов фона."""
        try:
            tv_sprite = arcade.Sprite(TV_BACKGROUND, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.background_sprites.append(tv_sprite)

            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.effect_sprites.append(glare_sprite)

            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.slot_machine_sprite.append(frame_sprite)

            # Запускаем стартовый звук
            self.play_start_sound()
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайтов в RulesView: {e}")

    def play_start_sound(self):
        """Проигрываем стартовый звук."""
        try:
            if START_SOUND_PATH.exists():
                sound = arcade.load_sound(START_SOUND_PATH)
                self.start_sound_player = arcade.play_sound(sound)
            else:
                print(f"⚠️ Файл звука не найден: {START_SOUND_PATH}")
        except Exception as e:
            print(f"❌ Ошибка воспроизведения звука: {e}")

    def on_update(self, delta_time: float):
        self.rules_manager.update(delta_time)

    def on_draw(self):
        self.clear()

        # Отрисовка в порядке слоёв
        self.background_sprites.draw()
        self.effect_sprites.draw()
        self.slot_machine_sprite.draw()

        # Правила поверх всего
        self.rules_manager.on_draw()

    def on_key_press(self, key, _):
        """Обработка нажатия клавиш."""
        if key == arcade.key.ESCAPE:
            arcade.exit()
            return True

        if key == arcade.key.SPACE:
            # Пропускаем анимацию — мгновенно устанавливаем состояние
            self.rules_manager.hide()
            self.rules_manager.alpha = 255  # чтобы не ждать fade-in

            # Останавливаем звук
            if self.start_sound_player:
                arcade.stop_sound(self.start_sound_player)
                self.start_sound_player = None

            # Переход в игру
            from .game_view import GameView

            self.window.show_view(GameView())
            return True

        return False
