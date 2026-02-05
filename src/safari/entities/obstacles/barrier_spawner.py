import random

import arcade

from src.safari.constants import BARRIER_SPAWN_INTERVAL_MAX, BARRIER_SPAWN_INTERVAL_MIN
from src.safari.entities.obstacles.barrier import Barrier


class BarrierSpawner:
    """
    Управляет появлением барьеров на дорожке.
    Производит случайные интервалы 2-3 секунды.
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()
        self.active_barriers: list[Barrier] = []
        self.sprite_list = sprite_list

        # Сразу создаем первый барьер при инициализации
        self.is_active = True  # Можно ли создавать новые препятствия
        self._spawn_barrier()
        self.time_since_last_spawn = 0.0  # Сбрасываем таймер
        self.spawn_interval = self._get_random_interval()  # Генерируем новый интервал

    def _get_random_interval(self) -> float:
        """Случайный интервал от 2 до 3 секунд."""
        interval = random.uniform(  # noqa: S311 # nosec
            BARRIER_SPAWN_INTERVAL_MIN / 1000,  # Конвертируем в секунды
            BARRIER_SPAWN_INTERVAL_MAX / 1000,
        )
        return interval

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать новый барьер."""
        self.time_since_last_spawn += delta_time

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_barrier()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старые барьеры
        self._update_barriers(delta_time)

    def _spawn_barrier(self):
        """Создаёт новый барьер."""
        barrier = Barrier()
        barrier.setup()  # ← Явно вызываем setup для загрузки текстур

        self.active_barriers.append(barrier)
        self.sprite_list.append(barrier)

    def _update_barriers(self, delta_time: float):
        """Обновляет все активные барьеры и удаляет не нужные."""
        barriers_to_remove = []

        for barrier in self.active_barriers:
            barrier.on_update(delta_time)

            if barrier.should_be_removed():
                barriers_to_remove.append(barrier)

        # Удаляем помеченные барьеры
        for barrier in barriers_to_remove:
            self.active_barriers.remove(barrier)
            self.sprite_list.remove(barrier)

    # Методы для управления состоянием
    def stop_spawning(self):
        """Останавливает создание новых препятствий."""
        self.is_active = False
