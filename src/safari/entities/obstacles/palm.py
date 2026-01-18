import arcade

from src.safari.constants import (
    PALM_ALIVE_SPRITE,
    PALM_DEAD_SPRITE,
    PALM_DESPAWN_X,
    PALM_SPAWN_X,
    PALM_SPEED,
    PALM_Y_OFFSET,
    TRACK_Y_PALM,
)


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
        self.center_x = x
        self.center_y = y + PALM_Y_OFFSET

        # Загрузка текстур
        self.alive_texture = arcade.load_texture(PALM_ALIVE_SPRITE)
        self.dead_texture = arcade.load_texture(PALM_DEAD_SPRITE)
        self.texture = self.alive_texture

        # Устанавливаем размеры спрайта из текстуры
        self.width = self.texture.width
        self.height = self.texture.height

        # Флаг состояния
        self.is_alive = True

        # Скорость движения
        self.speed = PALM_SPEED

    def on_update(self, delta_time):
        """Обновление состояния: движение справа налево."""
        self.center_x -= self.speed * delta_time

    def on_hit(self):
        """Логика при попадании пули."""
        if not self.is_alive:
            return

        self.texture = self.dead_texture
        self.is_alive = False

    def should_be_removed(self) -> bool:
        """Проверка, нужно ли удалять объект."""
        return self.center_x <= PALM_DESPAWN_X
