from ....constants import (
    GAZELLE_DESPAWN_X,
    GAZELLE_SPAWN_X,
    GAZELLE_SPEED,
    GAZELLE_Y_OFFSET,
    TRACK_Y_GAZELLE,
)
from ..base_animal import Animal


class Gazelle(Animal):
    """
    Животное 'Газель' на третьей дорожке.

    Наследует всю функциональность от базового класса Animal.
    """

    def __init__(self, x: int = GAZELLE_SPAWN_X, y: int = TRACK_Y_GAZELLE):
        """
        Инициализация газели с анимацией.

        Args:
            x: Начальная позиция X
            y: Начальная позиция Y
        """
        super().__init__(
            animation_name="gazelle_animation",
            x=x,
            y=y,
            speed=GAZELLE_SPEED,
            despawn_x=GAZELLE_DESPAWN_X,
            y_offset=GAZELLE_Y_OFFSET,
        )
