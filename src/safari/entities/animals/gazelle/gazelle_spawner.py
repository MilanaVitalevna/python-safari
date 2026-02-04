import arcade

from ....constants import GAZELLE_SPAWN_INTERVAL_MAX, GAZELLE_SPAWN_INTERVAL_MIN
from ..base_animal_spawner import AnimalSpawnerBase
from .gazelle import Gazelle


class GazelleSpawner(AnimalSpawnerBase):
    """
    Управляет появлением газелей на дорожке.

    Особенности:
    - Первая газель создаётся сразу при старте игры
    - Интервал между появлениями: 2–4 секунд
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        super().__init__(
            sprite_list=sprite_list,
            animal_class=Gazelle,
            min_interval_ms=GAZELLE_SPAWN_INTERVAL_MIN,
            max_interval_ms=GAZELLE_SPAWN_INTERVAL_MAX,
            animal_name="gazelle",
        )
