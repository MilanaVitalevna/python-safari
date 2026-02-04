import arcade

from ....constants import RHINO_SPAWN_INTERVAL_MAX, RHINO_SPAWN_INTERVAL_MIN
from ..base_animal_spawner import AnimalSpawnerBase
from .rhino import Rhino


class RhinoSpawner(AnimalSpawnerBase):
    """
    Управляет появлением носорогов на дорожке.

    Особенности:
    - Первый носорог создаётся сразу при старте игры
    - Интервал между появлениями: 13–19.5 секунд
    - Новые носороги не создаются после попадания в предыдущего
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        super().__init__(
            sprite_list=sprite_list,
            animal_class=Rhino,
            min_interval_ms=RHINO_SPAWN_INTERVAL_MIN,
            max_interval_ms=RHINO_SPAWN_INTERVAL_MAX,
            animal_name="rhino",
        )
        # Дополнительный флаг для специфичной логики носорогов
        self.has_been_hit = False

    def update(self, delta_time: float):
        """
        Проверяет, нужно ли создать нового носорога.

        Особенность: если носорог был подбит, новые не создаются.
        """
        if self.has_been_hit:
            # Носорог был подбит - только обновляем существующих
            self._update_animals(delta_time)
            return

        super().update(delta_time)

    def _on_animal_killed(self, animal):
        """Особая логика для носорога: после убийства останавливаем спавн."""
        super()._on_animal_killed(animal)

        # Устанавливаем флаг, что носорог был подбит
        self.has_been_hit = True
        self.stop_spawning()
        print("🦏 Носорог подбит! Больше носорогов не появится")

    def reset(self):
        """Сбрасывает состояние с учетом специфики носорогов."""
        super().reset()
        self.has_been_hit = False

    # Специфичные методы для носорогов
    def mark_as_hit(self):
        """Помечает, что носорог был подбит (можно вызывать извне)."""
        self.has_been_hit = True
        self.stop_spawning()
