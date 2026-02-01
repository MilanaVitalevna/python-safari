import random

import arcade

from src.safari.constants import BIZON_SPAWN_INTERVAL_MAX, BIZON_SPAWN_INTERVAL_MIN
from src.safari.entities.animals.bizon.bizon import Bizon


class BizonSpawner:
    """
    Управляет появлением бизонов на дорожке.

    Особенности:
    - Первый бизон создаётся сразу при старте игры
    - Интервал между появлениями: 2–4 секунд
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()
        self.active_bizons = arcade.SpriteList()
        self.sprite_list = sprite_list
        self.number = 0  # Счётчик созданных бизонов
        # self.has_been_hit = False  # Добавляем флаг состояния

    def _get_random_interval(self) -> float:
        """Случайный интервал от 2 до 4 секунд."""
        interval = random.uniform(  # noqa: S311 # nosec
            BIZON_SPAWN_INTERVAL_MIN / 1000,  # Конвертируем в секунды
            BIZON_SPAWN_INTERVAL_MAX / 1000,
        )
        return interval

    def start(self):
        """Создаёт первый бизон при старте игры."""
        self._spawn_bizon()
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать нового бизона."""
        self.time_since_last_spawn += delta_time

        # # Проверяем, был ли уже попадание в бизона
        # if self.has_been_hit:
        #     return

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_bizon()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старых бизонов
        self._update_bizons(delta_time)

    def _spawn_bizon(self):
        """Создаёт нового бизона."""
        bizon = Bizon()
        bizon.setup()  # Явно вызываем setup для загрузки текстур
        self.number += 1

        self.active_bizons.append(bizon)
        self.sprite_list.append(bizon)

    def _update_bizons(self, delta_time: float):
        """Обновляет всех активных бизонов и удаляет ненужные."""
        bizons_to_remove = []

        for bizon in self.active_bizons:
            bizon.on_update(delta_time)

            # Удаляем бизона если:
            # 1. Он вышел за левую границу ИЛИ
            # 2. В него попали (is_alive = False)
            if bizon.should_be_removed() or not bizon.is_alive:
                bizons_to_remove.append(bizon)

        # Удаляем помеченных носорогов
        for bizon in bizons_to_remove:
            self.active_bizons.remove(bizon)
            self.sprite_list.remove(bizon)
