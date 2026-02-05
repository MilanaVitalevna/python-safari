import random

import arcade


class AnimalSpawnerBase:
    """
    Базовый класс для создания животных с интервалами.

    Особенности:
    - Первое животное создаётся сразу при старте игры
    - Интервал между появлениями случайный (в диапазоне)
    - Управляет жизненным циклом животных
    """

    def __init__(
        self,
        sprite_list: arcade.SpriteList,
        animal_class: type,
        min_interval_ms: int,
        max_interval_ms: int,
        animal_name: str = "animal",
    ):
        """
        Args:
            sprite_list: Основной список спрайтов для отрисовки
            animal_class: Класс создаваемого животного
            min_interval_ms: Минимальный интервал в миллисекундах
            max_interval_ms: Максимальный интервал в миллисекундах
            animal_name: Имя животного для логов
        """
        self.time_since_last_spawn = 0.0
        self.min_interval_ms = min_interval_ms
        self.max_interval_ms = max_interval_ms
        self.spawn_interval = self._get_random_interval()

        self.active_animals = arcade.SpriteList()
        self.sprite_list = sprite_list
        self.animal_class = animal_class
        self.animal_name = animal_name

        self.number = 0  # Счётчик созданных животных
        self.is_active = True  # Можно ли создавать новых животных
        self.was_killed = False  # Было ли убито животное (для специфичной логики)

    def _get_random_interval(self) -> float:
        """Случайный интервал в секундах."""
        return random.uniform(  # noqa: S311 # nosec
            self.min_interval_ms / 1000,
            self.max_interval_ms / 1000,
        )

    def start(self):
        """Создаёт первое животное при старте игры."""
        if self.is_active:
            self._spawn_animal()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

    def update(self, delta_time: float):
        """Проверяет, нужно ли создать новое животное."""
        if not self.is_active:
            self._update_animals(delta_time)
            return

        self.time_since_last_spawn += delta_time

        # Проверяем интервал
        if self.time_since_last_spawn >= self.spawn_interval:
            self._spawn_animal()
            self.time_since_last_spawn = 0.0
            self.spawn_interval = self._get_random_interval()

        # Обновляем и удаляем старых животных
        self._update_animals(delta_time)

    def _spawn_animal(self):
        """Создаёт новое животное."""
        if not self.is_active:
            return

        animal = self.animal_class()
        self.number += 1
        self.active_animals.append(animal)
        self.sprite_list.append(animal)
        print(f"🦌 Создано {self.animal_name} #{self.number}")

    def _update_animals(self, delta_time: float):
        """Обновляет всех активных животных и удаляет ненужные."""
        animals_to_remove = []

        for animal in self.active_animals:
            animal.on_update(delta_time)

            # Удаляем животное если:
            # 1. Оно вышло за границу ИЛИ
            # 2. В него попали (is_alive = False)
            if animal.should_be_removed():
                animals_to_remove.append(animal)

                # Отслеживаем убийство (если нужно)
                if not animal.is_alive:
                    self._on_animal_killed(animal)

        # Удаляем помеченных животных
        for animal in animals_to_remove:
            self.active_animals.remove(animal)
            self.sprite_list.remove(animal)

    def _on_animal_killed(self, animal):
        """Вызывается при убийстве животного (можно переопределить)."""
        # Базовый класс просто запоминает факт убийства
        self.was_killed = True
        print(f"🎯 {self.animal_name.capitalize()} убит!")

    # Методы для управления состоянием
    def stop_spawning(self):
        """Останавливает создание новых животных."""
        self.is_active = False

    def resume_spawning(self):
        """Возобновляет создание животных."""
        self.is_active = True

    def reset(self):
        """Сбрасывает состояние (для новой игры)."""
        self.was_killed = False
        self.is_active = True
        self.number = 0
        self.time_since_last_spawn = 0.0
        self.spawn_interval = self._get_random_interval()

        # Очищаем списки
        for animal in self.active_animals:
            self.sprite_list.remove(animal)
        self.active_animals.clear()
