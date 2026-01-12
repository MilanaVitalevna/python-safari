"""
Сцена: основная игра.

Отображает тот же фон автомата, что и в правилах.
Предназначен для отображения игрового процесса:
- Охотника
- Животных
- Пуль
- Табло

Пока содержит заглушку. В будущем будет управлять:
- Таймером
- Счётом
- Количеством выстрелов
- Переходом к призовой игре
"""

import arcade

from ..constants import (
    GLARE_EFFECT,
    SCREEN_CENTER,
    SLOT_MACHINE_FRAME,
    TV_BACKGROUND,
)


class GameView(arcade.View):
    """Сцена: основная игра."""

    def __init__(self):
        super().__init__()

        # Те же слои фона — сохраняем стиль автомата
        self.background_sprites = arcade.SpriteList()  # ТВ-экран
        self.effect_sprites = arcade.SpriteList()  # Блик
        self.slot_machine_sprite = arcade.SpriteList()  # Рамка автомата

        self.game_start_text = arcade.Text(
            "ИГРА НАЧАЛАСЬ!\n(Логика в разработке)",
            SCREEN_CENTER[0],
            SCREEN_CENTER[1],
            arcade.color.WHITE,
            28,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400,
            align="center",
        )

        self.setup()

    def setup(self):
        """Загрузка фона игры."""
        try:
            tv_sprite = arcade.Sprite(TV_BACKGROUND, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.background_sprites.append(tv_sprite)

            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.effect_sprites.append(glare_sprite)

            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.slot_machine_sprite.append(frame_sprite)
        except Exception as e:
            print(f"❌ Ошибка загрузки фона в GameView: {e}")

    def on_update(self, delta_time: float):
        # Здесь будет логика игры
        pass

    def on_draw(self):
        self.clear()

        # Отрисовка фона — в том же порядке
        self.background_sprites.draw()
        self.effect_sprites.draw()
        self.slot_machine_sprite.draw()

        # Заглушка Text объект — позже на реальную игру
        self.game_start_text.draw()

    def on_key_press(self, key, _):
        if key == arcade.key.ESCAPE:
            arcade.exit()
