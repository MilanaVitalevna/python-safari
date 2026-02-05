"""
Менеджер индикаторов выстрелов.
Управляет отображением лампочек на автомате.
"""

import arcade

from ..constants import SHOT_INDICATOR_POSITIONS
from ..resource_manager import Textures


class ShotIndicatorManager:
    """
    Управляет индикаторами выстрелов.
    Каждый выстрел деактивирует следующую лампочку.
    """

    def __init__(self):
        # Спрайты лампочек (изначально невидимые)
        self.indicators = []
        self.active_indicators = 0
        self.max_indicators = 16  # Фиксированное значение
        self.min_indicators = 0

        # Используем SpriteList для удобной отрисовки
        self.sprite_list = arcade.SpriteList()

        # Флаг инициализации
        self._initialized = False

    def setup(self):
        """Создает спрайты для всех индикаторов из загруженных текстур."""
        if self._initialized:
            return

        # Проверяем, что текстуры загружены
        if (
            not Textures.shot_indicators
            or len(Textures.shot_indicators) != self.max_indicators
        ):
            print(
                f"⚠️ Текстуры индикаторов не загружены или их количество неверное: "
                f"{len(Textures.shot_indicators) if Textures.shot_indicators else 0}/{self.max_indicators}"
            )
            return

        # Создаем спрайты для каждого индикатора
        for i in range(self.max_indicators):
            if i < len(SHOT_INDICATOR_POSITIONS):
                x, y = SHOT_INDICATOR_POSITIONS[i]
            else:
                # Запасной вариант на случай если позиций меньше
                x, y = 100 + i * 50, 588

            try:
                # Используем загруженную текстуру из ResourceManager
                indicator = arcade.Sprite()
                indicator.texture = Textures.shot_indicators[i]
                indicator.center_x = x
                indicator.center_y = y
                indicator.visible = True  # По умолчанию видимы
                self.indicators.append(indicator)
                self.sprite_list.append(indicator)
            except Exception as e:
                print(f"❌ Ошибка создания индикатора {i + 1}: {e}")
                # Создаем пустой спрайт-заглушку
                placeholder = arcade.SpriteSolidColor(10, 10, arcade.color.RED)
                placeholder.center_x = x
                placeholder.center_y = y
                placeholder.visible = False
                self.indicators.append(placeholder)
                self.sprite_list.append(placeholder)

        print(f"✅ Создано {len(self.indicators)} индикаторов выстрелов")
        self._initialized = True

    def update(self, shots_fired: int):
        """
        Обновляет состояние индикаторов на основе количества выстрелов.

        Args:
            shots_fired: Количество произведенных выстрелов (0-16)
        """
        if not self._initialized:
            self.setup()

        # Если еще не инициализировано, выходим
        if not self._initialized or not self.indicators:
            return

        # Ограничиваем значение
        shots_fired = min(max(shots_fired, 0), self.max_indicators)

        # Если количество не изменилось - ничего не делаем
        if shots_fired == self.active_indicators:
            return

        # Обновляем видимость индикаторов
        for i in range(-shots_fired, 0):  # [-1, -2, ..., -shots_fired]
            self.indicators[i].visible = False

    def draw(self):
        """Отрисовывает все активные индикаторы."""
        if not self._initialized or not self.sprite_list:
            return

        # Рисуем спрайт-лист - он отрисует только видимые спрайты
        self.sprite_list.draw()

    def reset(self):
        """Сбрасывает все индикаторы."""
        if not self._initialized:
            return

        for indicator in self.indicators:
            indicator.visible = True
        self.active_indicators = 0
        print("🔄 Индикаторы выстрелов сброшены")
