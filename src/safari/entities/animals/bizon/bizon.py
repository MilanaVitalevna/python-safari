from ....constants import (
    BIZON_DESPAWN_X,
    BIZON_SPAWN_X,
    BIZON_SPEED,
    BIZON_Y_OFFSET,
    TRACK_Y_BIZON,
)
from ..base_animal import Animal


class Bizon(Animal):
    """
    Животное 'Бизон' на второй дорожке.

    Наследует всю функциональность от базового класса Animal.
    """

    def __init__(self, x: int = BIZON_SPAWN_X, y: int = TRACK_Y_BIZON):
        """
        Инициализация бизона с анимацией.

        Args:
            x: Начальная позиция X
            y: Начальная позиция Y
        """
        super().__init__(
            animation_name="bizon_animation",
            x=x,
            y=y,
            speed=BIZON_SPEED,
            despawn_x=BIZON_DESPAWN_X,
            y_offset=BIZON_Y_OFFSET,
        )
