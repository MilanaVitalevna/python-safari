import arcade

from src.safari.constants import (
    GAZELLE_DESPAWN_X,
    GAZELLE_SPAWN_X,
    GAZELLE_SPEED,
    GAZELLE_Y_OFFSET,
    TRACK_Y_GAZELLE,
)
from src.safari.resource_manager import Textures


class Gazelle(arcade.Sprite):
    """
    Животное 'Газель' на третьей дорожке.

    Особенности:
    - Является целью для победы (даёт очки при попадании)
    - При попадании пули исчезает
    - Удаляется при выходе за левую границу экрана
    - Движение справа налево
    - Анимация движения из трёх кадров
    """

    def __init__(self, x: int = GAZELLE_SPAWN_X, y: int = TRACK_Y_GAZELLE):
        super().__init__()

        # Позиция
        self.center_x = x
        self.center_y = y + GAZELLE_Y_OFFSET

        # Инициализация текстур
        self.walk_textures = None

        # Размеры будут установлены в setup()
        self._width = 0
        self._height = 0

        # Скорость движения
        self.speed = GAZELLE_SPEED

        # Состояние
        self.is_alive = True
        self.walk_frame = 0
        self.walk_frame_timer = 0.0
        self.walk_frame_duration = 0.1  # Время показа каждого кадра анимации

        # Флаг, что текстуры загружены
        self._textures_loaded = False

    def setup(self):
        """Загружает текстуры газели из менеджера ресурсов."""
        if self._textures_loaded:
            return  # Уже загружено

        self._validate_and_load_textures()
        self._textures_loaded = True

    def _validate_and_load_textures(self):
        """Проверяет и загружает текстуры газели."""
        if not Textures.gazelle:
            raise RuntimeError("Текстуры газели не загружены (Textures.gazelle is None)")

        if len(Textures.gazelle) < 3:
            raise RuntimeError(f"Недостаточно текстур газели. Ожидалось 3, получено {len(Textures.gazelle)}")

        self.walk_textures = Textures.gazelle
        self.texture = self.walk_textures[0]

        # Устанавливаем размеры спрайта из текстуры
        self.width = self.texture.width
        self.height = self.texture.height

    def on_update(self, delta_time: float = 1 / 60):
        """Обновление состояния: движение справа налево и анимация."""
        # Проверяем, что текстуры загружены
        if not self._textures_loaded:
            self.setup()

        # Движение справа налево
        self.center_x -= self.speed * delta_time

        # Обновление анимации
        self.walk_frame_timer += delta_time
        if self.walk_frame_timer >= self.walk_frame_duration:
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_textures)
            self.texture = self.walk_textures[self.walk_frame]
            self.walk_frame_timer = 0.0

    def on_hit(self):
        """Логика при попадании пули."""
        if not self.is_alive:
            return

        # Изменяем состояние
        self.is_alive = False

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        # Удаляем если вышел за границу ИЛИ убит
        return self.center_x <= GAZELLE_DESPAWN_X or not self.is_alive
