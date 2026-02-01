import arcade

from src.safari.constants import (
    BIZON_DESPAWN_X,
    BIZON_SPAWN_X,
    BIZON_SPEED,
    BIZON_Y_OFFSET,
    TRACK_Y_BIZON,
)
from src.safari.resource_manager import Textures


class Bizon(arcade.Sprite):
    """
    Животное 'Бизон' на второй дорожке.

    Особенности:
    - Является целью для победы (даёт очки при попадании)
    - При попадании пули исчезает
    - Удаляется при выходе за левую границу экрана
    - Движение справа налево
    - Анимация движения из трёх кадров
    """

    def __init__(self, x: int = BIZON_SPAWN_X, y: int = TRACK_Y_BIZON):
        super().__init__()

        # Позиция
        self.center_x = x
        self.center_y = y + BIZON_Y_OFFSET

        # Инициализация текстур
        self.walk_textures = None

        # Размеры будут установлены в setup()
        self._width = 0
        self._height = 0

        # Скорость движения
        self.speed = BIZON_SPEED

        # Состояние
        self.is_alive = True
        self.walk_frame = 0
        self.walk_frame_timer = 0.0
        self.walk_frame_duration = 0.1  # Время показа каждого кадра анимации

        # Флаг, что текстуры загружены
        self._textures_loaded = False

    def setup(self):
        """Загружает текстуры бизона из менеджера ресурсов."""
        if self._textures_loaded:
            return  # Уже загружено

        self._validate_and_load_textures()
        self._textures_loaded = True

    def _validate_and_load_textures(self):
        """Проверяет и загружает текстуры бизона."""
        if not Textures.bizon:
            raise RuntimeError("Текстуры бизона не загружены (Textures.bizon is None)")

        if len(Textures.bizon) < 3:
            raise RuntimeError(f"Недостаточно текстур бизона. Ожидалось 3, получено {len(Textures.bizon)}")

        self.walk_textures = Textures.bizon
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
        return self.center_x <= BIZON_DESPAWN_X or not self.is_alive
