import random

import arcade

from src.safari.constants import RHINO_SPAWN_INTERVAL_MAX, RHINO_SPAWN_INTERVAL_MIN
from src.safari.entities.animals.rhino.rhino import Rhino


class RhinoSpawner:
    """
    Управляет появлением носорогов на дорожке.

    Особенности:
    - Первый носорог создаётся сразу при старте игры
    - Интервал между появлениями: 13–19.5 секунд
    - Новые носороги не создаются после попадания в предыдущего
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()
        self.active_rhinos = arcade.SpriteList()
        self.sprite_list = sprite_list
        self.number = 0  # Счётчик созданных носорогов
        # self.has_been_hit = False  # Добавляем флаг состояния

    def _get_random_interval(self) -> float:
        """Случайный интервал от 13 до 19.5 секунд."""
        interval = random.uniform(  # noqa: S311 # nosec
            RHINO_SPAWN_INTERVAL_MIN / 1000,  # Конвертируем в секунды
            RHINO_SPAWN_INTERVAL_MAX / 1000,
        )
        return interval

    def start(self):
        """Создаёт первый носорог при старте игры."""
        self._spawn_rhino()
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать нового носорога."""
        self.time_since_last_spawn += delta_time

        # # Проверяем, был ли уже попадание в носорога
        # if self.has_been_hit:
        #     return

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_rhino()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старых носорогов
        self._update_rhinos(delta_time)

    def _spawn_rhino(self):
        """Создаёт нового носорога."""
        rhino = Rhino()
        rhino.setup()  # Явно вызываем setup для загрузки текстур
        self.number += 1

        self.active_rhinos.append(rhino)
        self.sprite_list.append(rhino)

    def _update_rhinos(self, delta_time: float):
        """Обновляет всех активных носорогов и удаляет ненужные."""
        rhinos_to_remove = []

        for rhino in self.active_rhinos:
            rhino.on_update(delta_time)

            # Удаляем носорога если:
            # 1. Он вышел за левую границу ИЛИ
            # 2. В него попали (is_alive = False)
            if rhino.should_be_removed() or not rhino.is_alive:
                rhinos_to_remove.append(rhino)

        # Удаляем помеченных носорогов
        for rhino in rhinos_to_remove:
            self.active_rhinos.remove(rhino)
            self.sprite_list.remove(rhino)
