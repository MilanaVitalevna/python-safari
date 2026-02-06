"""
Упрощенная система столкновений.
Проверяет столкновения пуль с различными целями.
"""

import arcade

from ..entities.animals.bizon.bizon import Bizon
from ..entities.animals.gazelle.gazelle import Gazelle
from ..entities.animals.rhino.rhino import Rhino
from ..resource_manager import Textures


class CollisionSystem:
    def __init__(self):
        # Храним ссылки на менеджеры объектов напрямую
        self.bullet_manager = None
        self.rhino_spawner = None
        self.bizon_spawner = None
        self.gazelle_spawner = None
        self.palm_spawner = None
        self.score_manager = None

        # Список пар "пули-цели" для проверки
        self.collision_pairs = []

    def setup(self, bullet_manager, rhino_spawner, bizon_spawner, gazelle_spawner, palm_spawner, score_manager):
        """
        Настройка системы столкновений.

        Args:
            bullet_manager: менеджер пуль
            rhino_spawner: создатель носорогов
            bizon_spawner: создатель бизонов
            gazelle_spawner: создатель газелей
            palm_spawner: создатель пальм
            score_manager: менеджер счёта
        """
        self.bullet_manager = bullet_manager
        self.rhino_spawner = rhino_spawner
        self.bizon_spawner = bizon_spawner
        self.gazelle_spawner = gazelle_spawner
        self.palm_spawner = palm_spawner
        self.score_manager = score_manager

        # Определяем какие типы объектов проверять на столкновения
        self.collision_pairs = [
            (rhino_spawner.active_animals, "rhino"),
            (bizon_spawner.active_animals, "bizon"),
            (gazelle_spawner.active_animals, "gazelle"),
            (palm_spawner.active_palms, "palm"),
        ]

    def update(self):
        """Проверяет все возможные столкновения за кадр."""
        if not self.bullet_manager:
            return

        # Получаем спрайт-лист пуль (это SpriteList!)
        bullet_sprite_list = self.bullet_manager.sprite_list

        if not bullet_sprite_list or len(bullet_sprite_list) == 0:
            return

        # Проверяем каждую пулю на столкновение с каждой целью
        for bullet in bullet_sprite_list:
            if not bullet.is_active:
                continue

            for target_list, _target_type in self.collision_pairs:
                if not target_list or len(target_list) == 0:
                    continue

                # Проверяем столкновения
                collisions = arcade.check_for_collision_with_list(bullet, target_list)

                if collisions:
                    # Обрабатываем первое попадание
                    self._handle_hit(bullet, collisions[0])
                    break  # Пуля поразила цель, дальше не проверяем

    def _handle_hit(self, bullet, target):
        """
        Обрабатывает попадание пули в цель.

        Args:
            bullet: пуля, которая попала
            target: цель, в которую попали
        """
        # 1. Обрабатываем попадание для пули
        bullet.on_hit()

        # 2. Обрабатываем попадание для цели
        if hasattr(target, "on_hit"):
            target.on_hit()

        # 3. Наращиваем счет
        match target:
            case Rhino() if self.rhino_spawner:
                # обработка для Rhino
                self.score_manager.register_kill("rhino")
                Textures.shot_sound.play()
                # Особый случай: если это носорог, сообщаем spawner'у
                self.rhino_spawner.mark_as_hit()
            case Gazelle():
                # обработка для Gazelle
                self.score_manager.register_kill("gazelle")
                Textures.shot_sound.play()
            case Bizon():
                # обработка для Bizon
                self.score_manager.register_kill("bizon")
                Textures.shot_sound.play()

    def _play_shot_sound(self):
        """Воспроизводит звук попадания."""
        if Textures.shot_sound:
            try:
                Textures.shot_sound.play()
            except Exception as e:
                print(f"❌ Ошибка воспроизведения звука попадания: {e}")

    def add_collision_pair(self, target_list, target_type):
        """
        Добавляет новый тип целей для проверки столкновений.

        Args:
            target_list: SpriteList целей
            target_type: тип цели (для отладки)
        """
        self.collision_pairs.append((target_list, target_type))
