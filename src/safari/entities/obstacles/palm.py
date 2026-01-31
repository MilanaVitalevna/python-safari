import arcade

from src.safari.constants import (
    PALM_DESPAWN_X,
    PALM_SPAWN_X,
    PALM_SPEED,
    PALM_Y_OFFSET,
    PALMDEAD_Y_OFFSET,
    TRACK_Y_PALM,
)
from src.safari.resource_manager import Textures


class Palm(arcade.Sprite):
    """
    Препятствие 'Пальма' на четвёртой дорожке.

    Особенности:
    - Не является целью для победы (не даёт очков)
    - При попадании меняет спрайт на мёртвую пальму
    - Удаляется при выходе за левую границу экрана
    """

    def __init__(self, x: int = PALM_SPAWN_X, y: int = TRACK_Y_PALM):
        super().__init__()

        # Позиция
        self.center_x = x
        self.center_y = y + PALM_Y_OFFSET

        # Инициализация текстур
        self.alive_texture = None
        self.dead_texture = None

        # Размеры будут установлены в setup()
        self._width = 0
        self._height = 0

        # Флаг состояния
        self.is_alive = True

        # Скорость движения
        self.speed = PALM_SPEED

        # Флаг, что текстуры загружены
        self._textures_loaded = False

    def setup(self):
        """Загружает текстуры пальмы из менеджера ресурсов."""
        if self._textures_loaded:
            return  # Уже загружено

        self._validate_and_load_textures()
        self._textures_loaded = True

    def _validate_and_load_textures(self):
        """Проверяет и загружает текстуры пальмы."""
        if not Textures.palm_alive or not Textures.palm_dead:
            raise RuntimeError("Текстуры пальмы не загружены")

        self.alive_texture = Textures.palm_alive
        self.dead_texture = Textures.palm_dead

        # Устанавливаем начальную текстуру (живая пальма)
        self.texture = self.alive_texture

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

    def on_hit(self):
        """Логика при попадании пули."""
        if not self.is_alive or not self._textures_loaded:
            return

        self.texture = self.dead_texture
        self.center_y = TRACK_Y_PALM + PALMDEAD_Y_OFFSET
        self.is_alive = False

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        return self.center_x <= PALM_DESPAWN_X
