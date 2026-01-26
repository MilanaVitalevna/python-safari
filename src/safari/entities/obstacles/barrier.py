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

        # Позиция
        self.center_x = x
        self.center_y = y + BARRIER_Y_OFFSET

        # Инициализация текстуры
        self.barrier_texture = None

        # Размеры будут установлены в setup()
        self._width = 0
        self._height = 0

        # Скорость движения
        self.speed = BARRIER_SPEED

        # Флаг, что текстуры загружены
        self._textures_loaded = False

    def setup(self):
        """Загружает текстуру барьера из менеджера ресурсов."""
        if self._textures_loaded:
            return  # Уже загружено

        self._validate_and_load_textures()
        self._textures_loaded = True

    def _validate_and_load_textures(self):
        """Проверяет и загружает текстуру барьера."""
        if not Textures.barrier:
            raise RuntimeError("Текстура барьера не загружена (Textures.barrier is None)")

        self.barrier_texture = Textures.barrier
        self.texture = self.barrier_texture  # ← Теперь texture устанавливаем ТОЛЬКО здесь

        # Сохраняем размеры для быстрого доступа
        self._width = self.texture.width
        self._height = self.texture.height

    def on_update(self, delta_time: float = 1 / 60):
        """Обновление состояния: движение справа налево."""
        # Проверяем, что текстуры загружены
        if not self._textures_loaded:
            self.setup()
            return  # Выйти, если только что загрузили

        self.center_x -= self.speed * delta_time

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        return self.center_x <= BARRIER_DESPAWN_X
