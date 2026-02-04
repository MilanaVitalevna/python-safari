import random

import arcade

from src.safari.constants import GAZELLE_SPAWN_INTERVAL_MAX, GAZELLE_SPAWN_INTERVAL_MIN
from src.safari.entities.animals.gazelle.gazelle import Gazelle


class GazelleSpawner:
    """
    Управляет появлением газелей на дорожке.

    Особенности:
    - Первый газель создаётся сразу при старте игры
    - Интервал между появлениями: 2–4 секунд
    """

    def __init__(self, sprite_list: arcade.SpriteList):
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()
        self.active_gazelles = arcade.SpriteList()
        self.sprite_list = sprite_list
        self.number = 0  # Счётчик созданных газелей
        # self.has_been_hit = False  # Добавляем флаг состояния

    def _get_random_interval(self) -> float:
        """Случайный интервал от 2 до 4 секунд."""
        interval = random.uniform(  # noqa: S311 # nosec
            GAZELLE_SPAWN_INTERVAL_MIN / 1000,  # Конвертируем в секунды
            GAZELLE_SPAWN_INTERVAL_MAX / 1000,
        )
        return interval

    def start(self):
        """Создаёт первую газель при старте игры."""
        self._spawn_gazelle()
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать новую газель."""
        self.time_since_last_spawn += delta_time

        # # Проверяем, был ли уже попадание в газель
        # if self.has_been_hit:
        #     return

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_gazelle()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старых бизонов
        self._update_gazelles(delta_time)

    def _spawn_gazelle(self):
        """Создаёт нового бизона."""
        gazelle = Gazelle()
        gazelle.setup()  # Явно вызываем setup для загрузки текстур
        self.number += 1

        self.active_gazelles.append(gazelle)
        self.sprite_list.append(gazelle)

    def _update_gazelles(self, delta_time: float):
        """Обновляет всех активных газелей и удаляет ненужные."""
        gazelles_to_remove = []

        for gazelle in self.active_gazelles:
            gazelle.on_update(delta_time)

            # Удаляем газель если:
            # 1. Он вышел за левую границу ИЛИ
            # 2. В него попали (is_alive = False)
            if gazelle.should_be_removed() or not gazelle.is_alive:
                gazelles_to_remove.append(gazelle)

        # Удаляем помеченных носорогов
        for gazelle in gazelles_to_remove:
            self.active_gazelles.remove(gazelle)
            self.sprite_list.remove(gazelle)
