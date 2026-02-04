import arcade

from ....constants import BIZON_SPAWN_INTERVAL_MAX, BIZON_SPAWN_INTERVAL_MIN
from ..base_animal_spawner import AnimalSpawnerBase
from .bizon import Bizon


class BizonSpawner(AnimalSpawnerBase):
    """
    Управляет появлением бизонов на дорожке.

    Особенности:
    - Первый бизон создаётся сразу при старте игры
    - Интервал между появлениями: 2–4 секунд
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        super().__init__(
            sprite_list=sprite_list,
            animal_class=Bizon,
            min_interval_ms=BIZON_SPAWN_INTERVAL_MIN,
            max_interval_ms=BIZON_SPAWN_INTERVAL_MAX,
            animal_name="bizon",
        )
