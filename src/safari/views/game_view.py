"""
Сцена: основная игра.

Отображает фон автомата.
Предназначен для отображения игрового процесса:
- Охотника
- Животных
- Пуль
- Табло
- Дорожек

Использует arcade.Scene для управления порядком слоёв.
"""

import arcade

from ..constants import (
    GLARE_EFFECT,
    SCREEN_CENTER,
    SLOT_MACHINE_FRAME,
    TRACK_POSITIONS,
    TV_BACKGROUND,
)
from ..entities.track import TrackSprite


class GameView(arcade.View):
    """Сцена: основная игра."""

    def __init__(self):
        super().__init__()

        # Используем Scene для управления порядком отрисовки
        self.scene = arcade.Scene()

        # Звук галопа
        self.gallop_sound = None
        self.gallop_player = None

        self.setup()

    def setup(self):
        """Загрузка фона игры и инициализация дорожек."""
        try:
            # 1. ТВ-экран (фон)
            tv_sprite = arcade.Sprite(TV_BACKGROUND, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Background")
            self.scene.get_sprite_list("Background").append(tv_sprite)

            # 2. Дорожки
            self.scene.add_sprite_list("Tracks")
            for i, (x, y) in enumerate(TRACK_POSITIONS):
                track = TrackSprite(track_index=i + 1, x=x, y=y)
                self.scene["Tracks"].append(track)

            # 3. Блик (поверх дорожек)
            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Effects")
            self.scene["Effects"].append(glare_sprite)

            # 4. Рамка автомата (самый верхний слой)
            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Frame")
            self.scene["Frame"].append(frame_sprite)

            # Загрузка звука галопа
            try:
                gallop_sound_path = ":slot_machine:/sounds/gallop.ogg"
                self.gallop_sound = arcade.Sound(gallop_sound_path)
                self.gallop_player = self.gallop_sound.play(loop=True)
            except Exception as e:
                print(f"❌ Ошибка загрузки звука галопа: {e}")

        except Exception as e:
            print(f"❌ Ошибка загрузки фона в GameView: {e}")

    def on_update(self, delta_time: float):
        """Обновление анимаций."""
        self.scene["Tracks"].update()  # Вызываем update только у TrackSprite
        for track in self.scene["Tracks"]:
            track.on_update(delta_time)

    def on_draw(self):
        self.clear()

        # Отрисовка в порядке добавления слоёв: Background → Tracks → Effects → Frame
        self.scene.draw()

    def on_key_press(self, key, _):
        if key == arcade.key.ESCAPE:
            if self.gallop_player:
                self.gallop_player.pause()
            arcade.exit()
