import arcade

from src.safari.constants import (
    BARRIER_DESPAWN_X,
    BARRIER_SPAWN_X,
    BARRIER_SPEED,
    BARRIER_Y_OFFSET,
    TRACK_Y_BARRIER,
)
from src.safari.resource_manager import Textures


class Barrier(arcade.Sprite):
    """
    Препятствие 'Барьер' на пятой дорожке.

    Особенности:
    - Удаляется при выходе за левую границу экрана
    """

    def __init__(self, x: int = BARRIER_SPAWN_X, y: int = TRACK_Y_BARRIER):
        super().__init__()
        self.center_x = x
        self.center_y = y + BARRIER_Y_OFFSET

        # Получаем текстуры из объекта Textures для анимации
        self.texture = Textures.barrier

        # Устанавливаем размеры спрайта из текстуры
        self.width = self.texture.width
        self.height = self.texture.height

        # Скорость движения
        self.speed = BARRIER_SPEED

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        return self.center_x <= BARRIER_DESPAWN_X

    def on_update(self, delta_time):
        """Обновление состояния: движение справа налево."""
        self.center_x -= self.speed * delta_time
