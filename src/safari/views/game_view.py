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
    GALLOP_SOUND_PATH,
    GLARE_EFFECT,
    SCREEN_CENTER,
    SLOT_MACHINE_FRAME,
    TRACK_POSITIONS,
    TV_BACKGROUND,
)
from ..entities.animals.rhino.rhino_spawner import RhinoSpawner
from ..entities.hunter.hunter import Hunter
from ..entities.obstacles.barrier_spawner import BarrierSpawner
from ..entities.obstacles.palm_spawner import PalmSpawner
from ..entities.track import Track


class GameView(arcade.View):
    """Сцена: основная игра."""

    def __init__(self):
        super().__init__()

        # Используем Scene для управления порядком отрисовки
        self.scene = arcade.Scene()

        # Звук галопа
        self.gallop_sound = None
        self.gallop_player = None

        # Инициализируем охотника и создателей животных и препятствий
        self.palm_spawner = None
        self.rhino_spawner = None
        self.barrier_spawner = None
        self.hunter_sprite = None

        self.setup()
        self.start()

    def start(self):
        """Запускает основные процессы игры."""
        if self.rhino_spawner:
            self.rhino_spawner.start()
        if self.barrier_spawner:
            self.barrier_spawner._spawn_barrier()

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
                track = Track(track_index=i + 1, x=x, y=y)
                self.scene["Tracks"].append(track)

            # 3. Пальмы
            self.scene.add_sprite_list("PalmObstacles")
            self.palm_spawner = PalmSpawner(self.scene["PalmObstacles"])

            # 4. Барьеры на пятой дорожке
            self.scene.add_sprite_list("BarrierObstacles")
            self.barrier_spawner = BarrierSpawner(self.scene["BarrierObstacles"])

            # 5. Носороги на первой дорожке
            self.scene.add_sprite_list("RhinoAnimals")
            self.rhino_spawner = RhinoSpawner(self.scene["RhinoAnimals"])

            # 6. Создаем и добавляем охотника
            self.hunter_sprite = Hunter()
            self.hunter_sprite.setup()

            self.scene.add_sprite_list("Hunter", sprite_list=arcade.SpriteList())
            self.scene["Hunter"].append(self.hunter_sprite)
            self.hunter_sprite.run()

            # 7. Блик (поверх дорожек)
            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Effects")
            self.scene["Effects"].append(glare_sprite)

            # 8. Рамка автомата (самый верхний слой)
            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Frame")
            self.scene["Frame"].append(frame_sprite)

            # 9. Загрузка звука галопа
            try:
                self.gallop_sound = arcade.Sound(GALLOP_SOUND_PATH)
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

        # Обновляем создателей
        if self.palm_spawner:
            self.palm_spawner.update(delta_time)
        if self.rhino_spawner:
            self.rhino_spawner.update(delta_time, self)
        if self.barrier_spawner:
            self.barrier_spawner.update(delta_time)

        # Обновляем охотника
        if self.hunter_sprite and "BarrierObstacles" in self.scene:
            # Простая проверка каждый кадр
            self.hunter_sprite.check_for_obstacles(self.scene["BarrierObstacles"])

        if self.hunter_sprite:
            self.hunter_sprite.on_update(delta_time)

    def on_draw(self):
        self.clear()

        # Отрисовка в порядке добавления слоёв: Background → Tracks → Effects → Frame
        self.scene.draw()

    def on_key_press(self, key, _):
        if key == arcade.key.ESCAPE:
            if self.gallop_player:
                self.gallop_player.pause()
            arcade.exit()
