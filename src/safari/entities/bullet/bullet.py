"""
Класс Bullet - спрайт пули с физикой движения.
"""

import arcade

from src.safari.constants import (
    BULLET_MAX_X,
    BULLET_MIN_Y,
    BULLET_SPEED_X,
    BULLET_SPEED_Y,
    BULLET_START_OFFSET_X,
    BULLET_START_OFFSET_Y,
)
from src.safari.resource_manager import Textures


class Bullet(arcade.Sprite):
    """
    Пуля охотника с диагональной траекторией (45° вверх-вправо).

    Особенности:
    - Движение по диагонали: change_x, change_y
    - Удаляется при выходе за правую или нижнюю границу
    - Размер спрайта: 7x7 пикселей (берётся из текстуры)
    """

    def __init__(self, hunter_x: float, hunter_y: float):
        """
        Инициализация пули с начальной позицией относительно охотника.

        Args:
            hunter_x: X-координата охотника
            hunter_y: Y-координата охотника
        """
        super().__init__()

        # Начальная позиция относительно охотника
        self.center_x = hunter_x + BULLET_START_OFFSET_X
        self.center_y = hunter_y + BULLET_START_OFFSET_Y

        # Скорость движения (диагональ 45°)
        self.change_x = BULLET_SPEED_X
        self.change_y = BULLET_SPEED_Y

        # Состояние
        self.is_active = True

    def setup(self):
        """Проверяет и загружает текстуру пули."""
        if not Textures.bullet:
            raise RuntimeError("Текстура пули не загружена")

        self.texture = Textures.bullet

    def on_update(self, delta_time: float = 1 / 60):
        """
        Обновление позиции пули.

        Args:
            delta_time: Время с предыдущего кадра в секундах
        """
        # Обновляем позицию на основе скорости
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Проверяем выход за границы
        if self._should_be_removed():
            self.is_active = False

    def _should_be_removed(self) -> bool:
        """
        Проверяет, нужно ли удалять пулю.

        Returns:
            True если пуля вышла за правый или нижний край
        """
        return self.center_x > BULLET_MAX_X or self.center_y < BULLET_MIN_Y

    def check_collision_with_list(self, sprite_list: arcade.SpriteList) -> arcade.Sprite | None:
        """
        Проверяет столкновение пули со списком спрайтов.

        Args:
            sprite_list: Список спрайтов для проверки

        Returns:
            Первый спрайт с которым произошло столкновение или None
        """
        if not self.is_active:
            return None

        collisions = arcade.check_for_collision_with_list(self, sprite_list)
        return collisions[0] if collisions else None

    def on_hit(self):
        """Вызывается при попадании в цель."""
        self.is_active = False
