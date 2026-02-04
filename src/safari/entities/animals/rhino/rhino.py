from ....constants import (
    RHINO_DESPAWN_X,
    RHINO_SPAWN_X,
    RHINO_SPEED,
    RHINO_Y_OFFSET,
    TRACK_Y_RHINO,
)
from ..base_animal import Animal


class Rhino(Animal):
    """
    Животное 'Носорог' на первой дорожке.

    Наследует всю функциональность от базового класса Animal.
    """

    def __init__(self, x: int = RHINO_SPAWN_X, y: int = TRACK_Y_RHINO):
        """
        Инициализация носорога с анимацией.

        Args:
            x: Начальная позиция X
            y: Начальная позиция Y
        """
        super().__init__(
            animation_name="rhino_animation",
            x=x,
            y=y,
            speed=RHINO_SPEED,
            despawn_x=RHINO_DESPAWN_X,
            y_offset=RHINO_Y_OFFSET,
        )


# import arcade
#
# from ....constants import (
#     RHINO_DESPAWN_X,
#     RHINO_SPAWN_X,
#     RHINO_SPEED,
#     RHINO_Y_OFFSET,
#     TRACK_Y_RHINO,
# )
# from ....resource_manager import Textures
#
#
# class Rhino(arcade.TextureAnimationSprite):
#     """
#     Животное 'Носорог' на первой дорожке.
#
#     Использует TextureAnimation для анимации движения.
#
#     Особенности:
#     - Является целью для победы (даёт очки при попадании)
#     - При попадании пули исчезает
#     - Удаляется при выходе за левую границу экрана
#     - Движение справа налево
#     - Анимацию берем из класса Textures
#     """
#
#     def __init__(self, x: int = RHINO_SPAWN_X, y: int = TRACK_Y_RHINO):
#         """
#         Инициализация носорога с анимацией.
#
#         Args:
#             x: Начальная позиция X
#             y: Начальная позиция Y (центрируется автоматически)
#         """
#         # Получаем анимацию
#         if not Textures.rhino_animation:
#             raise RuntimeError("Анимация носорога не создана")
#
#         super().__init__(
#             center_x=x,
#             center_y=y + RHINO_Y_OFFSET,
#             animation=Textures.rhino_animation
#         )
#
#         # Скорость движения
#         self.speed = RHINO_SPEED
#
#         # Состояние
#         self.is_alive = True
#
#     def on_update(self, delta_time: float = 1 / 60):
#         """
#         Обновление состояния: движение справа налево и анимация.
#
#         Args:
#             delta_time: Время с последнего обновления в секундах
#         """
#         # Движение справа налево
#         self.center_x -= self.speed * delta_time
#
#         # Обновление анимации (автоматически управляет кадрами)
#         self.update_animation(delta_time)
#
#     def on_hit(self):
#         """Логика при попадании пули."""
#         if not self.is_alive:
#             return
#
#         # Изменяем состояние
#         self.is_alive = False
#
#     def should_be_removed(self) -> bool:
#         """
#         Проверка, нужно ли удалять объект.
#
#         Returns:
#             True если нужно удалить (вышел за границу или убит)
#         """
#         # Удаляем если вышел за границу ИЛИ убит
#         return self.center_x <= RHINO_DESPAWN_X or not self.is_alive
