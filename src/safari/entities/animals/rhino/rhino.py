import arcade

from src.safari.constants import (
    RHINO_DESPAWN_X,
    RHINO_SPAWN_X,
    RHINO_SPEED,
    RHINO_Y_OFFSET,
    TRACK_Y_RHINO,
)
from src.safari.resource_manager import Textures


class Rhino(arcade.Sprite):
    """
    Животное 'Носорог' на первой дорожке.

    Особенности:
    - Является целью для победы (даёт очки при попадании)
    - При попадании пули меняет спрайт (заглушка)
    - Удаляется при выходе за левую границу экрана
    - Движение справа налево
    - Анимация движения из трёх кадров
    """

    def __init__(self, x: int = RHINO_SPAWN_X, y: int = TRACK_Y_RHINO):
        super().__init__()
        self.center_x = x
        self.center_y = y + RHINO_Y_OFFSET

        # Получаем текстуры из объекта Textures для анимации
        self.walk_textures = Textures.rhino
        self.texture = self.walk_textures[0]

        # Устанавливаем размеры спрайта из текстуры
        self.width = self.texture.width
        self.height = self.texture.height

        # Скорость движения
        self.speed = RHINO_SPEED

        # Состояние
        self.is_alive = True
        self.walk_frame = 0
        self.walk_frame_timer = 0
        self.walk_frame_duration = 0.1  # Время показа каждого кадра анимации

    def on_update(self, delta_time):
        """Обновление состояния: движение справа налево и анимация."""
        self.center_x -= self.speed * delta_time

        # Обновление анимации
        self.walk_frame_timer += delta_time
        if self.walk_frame_timer >= self.walk_frame_duration:
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_textures)
            self.texture = self.walk_textures[self.walk_frame]
            self.walk_frame_timer = 0

    def on_hit(self):
        """Логика при попадании пули."""
        if not self.is_alive:
            return

        # Заглушка: изменение текстуры при попадании
        self.is_alive = False
        self.texture = self.walk_textures[0]  # Временная заглушка

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        return self.center_x <= RHINO_DESPAWN_X
