import random

import arcade

from src.safari.constants import PALM_SPAWN_INTERVAL_MAX, PALM_SPAWN_INTERVAL_MIN
from src.safari.entities.obstacles.palm import Palm


class PalmSpawner:
    """
    Управляет появлением пальм на дорожке.
    Производит случайные интервалы 4-6 секунд.
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        self.time_since_last_spawn = 0
        self.spawn_interval = self._get_random_interval()
        self.active_palms: list[Palm] = []
        self.sprite_list = sprite_list

        # Сразу создаем первую пальму при инициализации
        self._spawn_palm()
        self.time_since_last_spawn = 0  # Сбрасываем таймер
        self.spawn_interval = self._get_random_interval()  # Генерируем новый интервал

    def _get_random_interval(self) -> float:
        """Случайный интервал от 4 до 6 секунд (целые значения)."""
        interval = random.uniform(PALM_SPAWN_INTERVAL_MIN / 1000, PALM_SPAWN_INTERVAL_MAX / 1000)  # noqa: S311 # nosec
        return interval

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать новую пальму."""
        self.time_since_last_spawn += delta_time

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_palm()
            self.time_since_last_spawn = 0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старые пальмы
        self._update_palms(delta_time)

    def _spawn_palm(self):
        """Создаёт новую пальму."""
        palm = Palm()

        self.active_palms.append(palm)
        self.sprite_list.append(palm)

    def _update_palms(self, delta_time: float):
        """Обновляет все активные пальмы и удаляет не нужные."""
        palms_to_remove = []

        for palm in self.active_palms:
            palm.on_update(delta_time)

            if palm.should_be_removed():
                palms_to_remove.append(palm)

        # Удаляем помеченные пальмы
        for palm in palms_to_remove:
            self.active_palms.remove(palm)
            self.sprite_list.remove(palm)
