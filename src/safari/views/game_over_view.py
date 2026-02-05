"""
Сцена: экран завершения игры при победе.
"""

import arcade

from ..constants import (
    AVENTURA_FONT_NAME,
    GLARE_EFFECT,
    INPUT_DELAY_SECONDS,
    SAFARI_FONT_NAME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLOT_MACHINE_FRAME,
    TV_BACKGROUND,
)
from .rules_view import RulesView


class GameOverView(arcade.View):
    """Сцена: окно завершения игры при победе."""

    def __init__(self, score_data: dict, shots_fired: int, victory: bool):
        """
        Args:
            score_data: словарь с данными о счете
        """
        super().__init__()

        self.score_data = {
            # Распакуем словарь
            **score_data,
            "shots_fired": shots_fired,
            "victory": victory,
        }

        self.input_enabled = False  # Ввод клавиш запрещён до таймаута

        # Слои фона
        self.background_sprites = arcade.SpriteList()  # ТВ-экран
        self.effect_sprites = arcade.SpriteList()  # Блик
        self.slot_machine_sprite = arcade.SpriteList()  # Рамка автомата

        # Текстовые элементы
        self.title_text = None
        self.result_text = None
        self.stats_text = None
        self.instruction_text = None

        self.setup()

    def setup(self):
        """Загрузка всех спрайтов фона и текста."""
        try:
            # Фон
            tv_sprite = arcade.Sprite(TV_BACKGROUND, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.background_sprites.append(tv_sprite)

            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.effect_sprites.append(glare_sprite)

            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            self.slot_machine_sprite.append(frame_sprite)

            # Тексты
            if self.score_data["victory"]:
                title_text = "ПОБЕДА!"
                result_text = "Все цели поражены!"
                title_color = (50, 200, 50)
                result_color = (255, 255, 255)
            else:
                title_text = "ПОРАЖЕНИЕ"
                result_text = "Цели не достигнуты"
                title_color = (255, 100, 100)
                result_color = (255, 180, 180)

            self.title_text = arcade.Text(
                title_text,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 150,
                title_color,
                48,
                anchor_x="center",
                anchor_y="center",
                font_name=SAFARI_FONT_NAME,
                bold=True,
            )

            self.result_text = arcade.Text(
                result_text,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 220,
                result_color,
                28,
                anchor_x="center",
                anchor_y="center",
                font_name=AVENTURA_FONT_NAME,
            )

            # Статистика
            stats_lines = [
                f"Носорогов убито: {self.score_data.get('rhino_kills', 0)}",
                f"Бизонов убито: {self.score_data.get('bizon_kills', 0)}",
                f"Газелей убито: {self.score_data.get('gazelle_kills', 0)}",
                f"Выстрелов сделано: {self.score_data.get('shots_fired', 0)}",
            ]

            stats_text = "\n".join(stats_lines)

            self.stats_text = arcade.Text(
                stats_text,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 400,
                (255, 255, 0),
                24,
                anchor_x="center",
                anchor_y="center",
                font_name=AVENTURA_FONT_NAME,
                multiline=True,
                width=500,
            )

            # Инструкция
            instruction = 'Нажмите "ПРОБЕЛ" для новой игры\nНажмите "ESC" для выхода'
            self.instruction_text = arcade.Text(
                instruction,
                SCREEN_WIDTH / 2,
                150,
                (200, 200, 200),
                20,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=SCREEN_WIDTH - 100,
                align="center",
                font_name=AVENTURA_FONT_NAME,
            )

            # ⏳ Запланировать включение ввода через INPUT_DELAY_SECONDS секунд
            arcade.schedule_once(self.enable_input, INPUT_DELAY_SECONDS)

        except Exception as e:
            print(f"❌ Ошибка в GameOverView.setup(): {e}")

    def enable_input(self, delta_time: float):
        """Разрешает ввод после задержки."""
        self.input_enabled = True

    def on_draw(self):
        self.clear()

        # Отрисовка фона
        self.background_sprites.draw()
        self.effect_sprites.draw()
        self.slot_machine_sprite.draw()

        # Затемнение фона
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=SCREEN_WIDTH,
            bottom=0,
            top=SCREEN_HEIGHT,
            color=(0, 0, 0, 180),
        )

        # Отрисовка текста
        self.title_text.draw()
        self.result_text.draw()
        self.stats_text.draw()
        self.instruction_text.draw()

    def on_key_press(self, key, _):
        """Обработка нажатия клавиш с задержкой."""
        if not self.input_enabled:
            return False  # Игнорируем нажатия до активации

        if key == arcade.key.ESCAPE:
            arcade.exit()
            return True

        if key == arcade.key.SPACE:
            self.window.show_view(RulesView())
            return True

        return False
