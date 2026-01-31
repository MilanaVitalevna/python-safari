"""
Управление пулями с ограничениями:
- Максимум 16 выстрелов за игру
- Блокировка выстрела при определенных условиях
"""

import arcade

from src.safari.constants import (
    MAX_SHOTS_TOTAL,
    MIN_TIME_SINCE_LAST_SHOT,
)
from src.safari.entities.bullet.bullet import Bullet
from src.safari.resource_manager import Textures


class BulletManager:
    """
    Менеджер пуль с ограничениями по количеству и состоянию.
    """

    def __init__(self):
        # Ограничения
        self.max_shots_total = MAX_SHOTS_TOTAL
        self.time_since_last_shot = MIN_TIME_SINCE_LAST_SHOT  # Сколько времени прошло с последнего выстрела

        # Состояние
        self.shots_fired = 0  # Количество сделанных выстрелов
        self.game_started = False  # Флаг начала игры

        # Пули
        self.active_bullets = []  # Список активных пуль
        self.sprite_list = arcade.SpriteList()  # Список для отрисовки

        # Ссылка на охотника
        self.hunter = None

    def setup(self, hunter):
        """
        Инициализация менеджера пуль.

        Args:
            hunter: Спрайт охотника для определения позиции выстрела
        """
        self.hunter = hunter

    def fire(self) -> bool:
        """
        Производит выстрел, если условия позволяют.

        Returns:
            True если выстрел произведен, False если заблокирован
        """
        # Проверяем условия блокировки
        if not self._can_fire():
            return False

        # Создаем новую пулю
        bullet = Bullet(self.hunter.center_x, self.hunter.center_y)
        bullet.setup()

        # Добавляем пулю в списки
        self.active_bullets.append(bullet)
        self.sprite_list.append(bullet)

        # Обновляем состояние
        self.shots_fired += 1
        # После успешного выстрела
        self.time_since_last_shot = 0.0

        # Воспроизводим звук выстрела
        self._play_fire_sound()

        print(f"🔫 Выстрел #{self.shots_fired}/{self.max_shots_total}")
        return True

    def _can_fire(self) -> bool:
        """
        Проверяет, можно ли произвести выстрел.

        Returns:
            True если выстрел разрешен
        """
        # Блокировка: задержка
        if self.time_since_last_shot < MIN_TIME_SINCE_LAST_SHOT:
            print(f"⚠️  Не могу выстрелить: задержка {self.time_since_last_shot:.1f}/{MIN_TIME_SINCE_LAST_SHOT}s")
            return False

        # Блокировка: закончились патроны
        if self.shots_fired >= self.max_shots_total:
            print("⚠️  Не могу выстрелить: закончились патроны")
            return False

        # Блокировка: игра не начата
        if not self.game_started:
            print("⚠️  Не могу выстрелить: игра не начата")
            return False

        # Блокировка: охотник в состоянии прыжка
        if self.hunter and hasattr(self.hunter, "is_jumping") and self.hunter.is_jumping:
            print("⚠️  Не могу выстрелить: охотник прыгает")
            return False

        return True

    def update(self, delta_time: float):
        """
        Обновляет все активные пули.

        Args:
            delta_time: Время с предыдущего кадра в секундах
        """
        bullets_to_remove = []
        self.time_since_last_shot += delta_time

        # Обновляем каждую пулю
        for bullet in self.active_bullets:
            bullet.on_update(delta_time)

            # Проверяем, нужно ли удалить пулю
            if not bullet.is_active or bullet._should_be_removed():
                bullets_to_remove.append(bullet)

        # Удаляем неактивные пули
        for bullet in bullets_to_remove:
            self._remove_bullet(bullet)

    def _remove_bullet(self, bullet: Bullet):
        """
        Удаляет пулю из всех списков.

        Args:
            bullet: Пуля для удаления
        """
        if bullet in self.active_bullets:
            self.active_bullets.remove(bullet)

        if bullet in self.sprite_list:
            self.sprite_list.remove(bullet)

    def _play_fire_sound(self):
        """Воспроизводит звук выстрела."""
        if Textures.fire_sound:
            try:
                Textures.fire_sound.play()
            except Exception as e:
                print(f"❌ Ошибка воспроизведения звука выстрела: {e}")

    def enable_shooting(self):
        """Активирует возможность стрельбы."""
        self.game_started = True
        print("🎮 Игра начата - стрельба разрешена")

    def reset(self):
        """Сбрасывает состояние менеджера пуль."""
        # Очищаем все пули
        for bullet in self.active_bullets[:]:  # Копируем список для безопасного удаления
            self._remove_bullet(bullet)

        # Сбрасываем состояние
        self.shots_fired = 0
        self.game_started = False
        print("🔄 Менеджер пуль сброшен")
