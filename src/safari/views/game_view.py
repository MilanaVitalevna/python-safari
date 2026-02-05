import arcade

from .game_over_view import GameOverView
from ..collision.collision_system import CollisionSystem
from ..constants import (
    GALLOP_SOUND_PATH,
    GLARE_EFFECT,
    SCREEN_CENTER,
    SLOT_MACHINE_FRAME,
    TRACK_POSITIONS,
    TV_BACKGROUND,
)
from ..entities.animals.bizon.bizon_spawner import BizonSpawner
from ..entities.animals.gazelle.gazelle_spawner import GazelleSpawner
from ..entities.animals.rhino.rhino_spawner import RhinoSpawner
from ..entities.bullet.bullet_manager import BulletManager
from ..entities.hunter.hunter import Hunter
from ..entities.obstacles.barrier_spawner import BarrierSpawner
from ..entities.obstacles.palm_spawner import PalmSpawner
from ..entities.track import Track
from ..ui.button_animation_manager import ButtonAnimationManager
from ..ui.shot_indicator_manager import ShotIndicatorManager
from ..score_manager import ScoreManager


class GameView(arcade.View):
    """Сцена: основная игра."""

    def __init__(self):
        super().__init__()

        # Используем Scene для управления порядком отрисовки
        self.scene = arcade.Scene()

        # Звук галопа
        self.gallop_sound = None
        self.gallop_player = None

        # Инициализируем охотника, пули и создателей животных с препятствиями
        self.palm_spawner = None
        self.rhino_spawner = None
        self.bizon_spawner = None
        self.gazelle_spawner = None
        self.barrier_spawner = None
        self.hunter_sprite: Hunter | None = None
        self.bullet_manager = None

        self.shot_indicators = None
        # Менеджер анимации кнопки
        self.button_animation = None
        # Менеджер очков
        self.score_manager = None

        # Сначала создаем систему столкновений
        self.collision_system = CollisionSystem()

        # Потом настраиваем игру
        self.setup()
        self.start()

    def start(self):
        """Запускает основные процессы игры."""
        if self.rhino_spawner:
            self.rhino_spawner.start()
        if self.bizon_spawner:
            self.bizon_spawner.start()
        if self.gazelle_spawner:
            self.gazelle_spawner.start()
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

            # 3. Барьеры на пятой дорожке
            self.scene.add_sprite_list("BarrierObstacles")
            self.barrier_spawner = BarrierSpawner(self.scene["BarrierObstacles"])

            # 4. Носороги на первой дорожке
            self.scene.add_sprite_list("RhinoAnimals")
            self.rhino_spawner = RhinoSpawner(self.scene["RhinoAnimals"])

            # 5. Бизоны на второй дорожке
            self.scene.add_sprite_list("BizonAnimals")
            self.bizon_spawner = BizonSpawner(self.scene["BizonAnimals"])

            # 6. Газели на третьей дорожке
            self.scene.add_sprite_list("GazelleAnimals")
            self.gazelle_spawner = GazelleSpawner(self.scene["GazelleAnimals"])

            # 7. Пальмы на четвертой дорожке
            self.scene.add_sprite_list("PalmObstacles")
            self.palm_spawner = PalmSpawner(self.scene["PalmObstacles"])

            # 8. Создаем и добавляем охотника
            self.hunter_sprite: arcade.TextureAnimationSprite = Hunter()

            self.scene.add_sprite_list("Hunter", sprite_list=arcade.SpriteList())
            self.scene["Hunter"].append(self.hunter_sprite)

            # 9. Инициализация менеджера пуль
            self.bullet_manager = BulletManager()
            self.bullet_manager.setup(self.hunter_sprite)
            self.scene.add_sprite_list("Bullets", sprite_list=self.bullet_manager.sprite_list)
            self.bullet_manager.enable_shooting()  # Разрешаем стрельбу

            # 10. Блик (поверх дорожек)
            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Effects")
            self.scene["Effects"].append(glare_sprite)

            # 11. Рамка автомата (самый верхний слой)
            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.scene.add_sprite_list("Frame")
            self.scene["Frame"].append(frame_sprite)

            # 12. Индикаторы выстрелов
            self.shot_indicators = ShotIndicatorManager()
            self.shot_indicators.setup()

            # 13. Инициализация менеджера очков
            self.score_manager = ScoreManager()

            # 14. Анимация кнопки
            self.button_animation = ButtonAnimationManager()
            self.button_animation.setup()

            # 15. Загрузка звука галопа
            try:
                self.gallop_sound = arcade.Sound(GALLOP_SOUND_PATH)
                self.gallop_player = self.gallop_sound.play(loop=True)
            except Exception as e:
                print(f"❌ Ошибка загрузки звука галопа: {e}")

            # 16. Настраиваем систему столкновений
            if self.collision_system:
                self.collision_system.setup(
                    bullet_manager=self.bullet_manager,
                    rhino_spawner=self.rhino_spawner,
                    bizon_spawner=self.bizon_spawner,
                    gazelle_spawner=self.gazelle_spawner,
                    palm_spawner=self.palm_spawner,
                    score_manager=self.score_manager,
                )
            else:
                print("⚠️ collision_system не инициализирован!")

        except Exception as e:
            print(f"❌ Ошибка загрузки фона в GameView: {e}")

    def on_update(self, delta_time: float):
        """Обновление анимаций."""
        # 1. Обновляем дорожки
        self.scene["Tracks"].update()
        for track in self.scene["Tracks"]:
            track.on_update(delta_time)

        # 2. Обновляем создателей
        if self.palm_spawner:
            self.palm_spawner.update(delta_time)
        if self.rhino_spawner:
            self.rhino_spawner.update(delta_time)
        if self.bizon_spawner:
            self.bizon_spawner.update(delta_time)
        if self.gazelle_spawner:
            self.gazelle_spawner.update(delta_time)
        if self.barrier_spawner:
            self.barrier_spawner.update(delta_time)

        # 3. Обновляем охотника
        if self.hunter_sprite and "BarrierObstacles" in self.scene:
            self.hunter_sprite.check_for_obstacles(self.scene["BarrierObstacles"])

        if self.hunter_sprite:
            self.hunter_sprite.on_update(delta_time)

        # 4. Обновляем пули
        if self.bullet_manager:
            self.shot_indicators.update(self.bullet_manager.shots_fired)
            self.bullet_manager.update(delta_time)

        # 5. Обновляем анимацию кнопки
        if self.button_animation:
            self.button_animation.update(delta_time)

        # 6. Проверяем столкновения пуль с объектами
        self.collision_system.update()

        # 7. Проверяем победу
        if self.score_manager and self.score_manager.is_victory():
            print("🎉 ПОБЕДА! Все цели поражены!"                  
                  f"Носорогов: {self.score_manager.rhino_kills}, "
                  f"Бизонов: {self.score_manager.bizon_kills}, "
                  f"Газелей: {self.score_manager.gazelle_kills}")

            # Завершаем игру и переходим на экран победы
            self._end_game_with_victory()
            return  # Прекращаем обновление игры

    def _end_game_with_victory(self):
        """Завершает игру при победе и переходит на экран результатов."""
        print("🔄 Переход на экран победы...")

        # Останавливаем звуки
        if self.gallop_player:
            self.gallop_player.pause()

        # Останавливаем спавн объектов
        if self.rhino_spawner:
            self.rhino_spawner.stop_spawning()
        if self.bizon_spawner:
            self.bizon_spawner.stop_spawning()
        if self.gazelle_spawner:
            self.gazelle_spawner.stop_spawning()
        # if self.barrier_spawner:
        #     self.barrier_spawner.stop_spawning()
        # if self.palm_spawner:
        #     self.palm_spawner.stop_spawning()

        # Подготавливаем данные для передачи
        score_data = {
            'rhino_kills': self.score_manager.rhino_kills if self.score_manager else 0,
            'bizon_kills': self.score_manager.bizon_kills if self.score_manager else 0,
            'gazelle_kills': self.score_manager.gazelle_kills if self.score_manager else 0,
            'shots_fired': self.bullet_manager.shots_fired if self.bullet_manager else 0,
        }

        # Переходим на экран завершения игры
        game_over_view = GameOverView(score_data=score_data)
        self.window.show_view(game_over_view)

    def on_draw(self):
        self.clear()

        # Отрисовка в порядке добавления слоёв: Background → Tracks → Effects → Frame
        self.scene.draw()
        self.shot_indicators.draw()  # Рисуем индикаторы выстрелов поверх всего
        self.button_animation.draw() # Кнопка стрельбы на автомате поверх всего

    def on_key_press(self, key, _):

        if key == arcade.key.ESCAPE:
            if self.gallop_player:
                self.gallop_player.pause()
            arcade.exit()

        if key == arcade.key.SPACE and self.bullet_manager:
            # Пытаемся сделать выстрел и проверяем результат
            shot_successful = self.bullet_manager.fire()

            # Запускаем анимацию кнопки только если выстрел успешен
            if shot_successful and self.button_animation:
                self.button_animation.press()
