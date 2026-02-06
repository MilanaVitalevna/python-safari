"""
Менеджер индикаторов убитых животных.
Управляет отображением лампочек: газели, бизоны, носорог.
"""

import arcade

from ..constants import (
    BIZON_INDICATOR_POSITIONS,
    GAZELLE_INDICATOR_POSITIONS,
    RHINO_INDICATOR_POSITIONS,
)
from ..resource_manager import Textures


class AnimalIndicatorManager:
    """
    Управляет индикаторами убитых животных.
    Каждое убийство активирует следующую лампочку в соответствующей группе.
    """

    def __init__(self):
        self.gazelle_indicators: list[arcade.Sprite] = []  # Список спрайтов газелей
        self.bizon_indicators: list[arcade.Sprite] = []  # Список спрайтов бизонов
        self.rhino_indicators: list[arcade.Sprite] = []  # Список спрайтов носорога

        # SpriteLists для удобной отрисовки
        self.gazelle_sprite_list: arcade.SpriteList = arcade.SpriteList()
        self.bizon_sprite_list: arcade.SpriteList = arcade.SpriteList()
        self.rhino_sprite_list: arcade.SpriteList = arcade.SpriteList()

        self._initialized = False

    def setup(self):
        """Создаёт спрайты для всех индикаторов на основе загруженных текстур."""
        if self._initialized:
            return

        success = True

        # Создание индикаторов газелей
        success &= self._create_indicators(
            self.gazelle_indicators,
            self.gazelle_sprite_list,
            Textures.gazelle_indicators,
            GAZELLE_INDICATOR_POSITIONS,
            "Газель",
        )

        # Создание индикаторов бизонов
        success &= self._create_indicators(
            self.bizon_indicators, self.bizon_sprite_list, Textures.bizon_indicators, BIZON_INDICATOR_POSITIONS, "Бизон"
        )

        # Создание индикаторов носорога
        success &= self._create_single_indicator(
            self.rhino_indicators,
            self.rhino_sprite_list,
            Textures.rhino_indicators,
            RHINO_INDICATOR_POSITIONS,
            "Носорог",
        )

        if success:
            print("✅ Индикаторы животных успешно созданы")
        else:
            print("⚠️ Ошибка при создании одного или нескольких индикаторов")

        self._initialized = True

    def _create_indicators(self, indicator_list, sprite_list, textures, positions, name):
        """Вспомогательный метод для создания группы индикаторов."""
        if not textures or len(textures) != len(positions):
            print(f"❌ Не хватает текстур для {name}: {len(textures)} вместо {len(positions)}")
            return False

        for i, (x, y) in enumerate(positions):
            try:
                sprite = arcade.Sprite()
                sprite.texture = textures[i]
                sprite.center_x = x
                sprite.center_y = y
                sprite.visible = False
                indicator_list.append(sprite)
                sprite_list.append(sprite)
            except Exception as e:
                print(f"❌ Ошибка создания индикатора {name} #{i + 1}: {e}")
                return False
        return True

    def _create_single_indicator(self, indicator_list, sprite_list, textures, positions, name):
        """Создание одного индикатора (например, носорог)."""
        if not textures or len(positions) == 0:
            print(f"❌ Нет текстур или позиций для {name}")
            return False

        try:
            sprite = arcade.Sprite()
            sprite.texture = textures[0]  # Только одна текстура
            sprite.center_x = positions[0][0]
            sprite.center_y = positions[0][1]
            sprite.visible = False
            indicator_list.append(sprite)
            sprite_list.append(sprite)
            return True
        except Exception as e:
            print(f"❌ Ошибка создания индикатора {name}: {e}")
            return False

    def update(self, gazelle_kills: int, bizon_kills: int, rhino_kills: int):
        """
        Обновляет состояние индикаторов на основе количества убийств.
        Активирует нужное количество лампочек.
        """
        if not self._initialized:
            self.setup()

        self._update_group(self.gazelle_indicators, gazelle_kills, 8)
        self._update_group(self.bizon_indicators, bizon_kills, 4)
        self._update_group(self.rhino_indicators, rhino_kills, 1)

    def _update_group(self, indicators, kills, max_count):
        """Обновляет видимость индикаторов в группе."""
        count = min(max(kills, 0), max_count)
        for i, ind in enumerate(indicators):
            ind.visible = i < count

    def draw(self):
        """Отрисовывает все активные индикаторы."""
        if not self._initialized:
            return

        self.gazelle_sprite_list.draw()
        self.bizon_sprite_list.draw()
        self.rhino_sprite_list.draw()

    def reset(self):
        """Сбрасывает все индикаторы."""
        if not self._initialized:
            return

        for group in [self.gazelle_indicators, self.bizon_indicators, self.rhino_indicators]:
            for ind in group:
                ind.visible = False
        print("🔄 Индикаторы животных сброшены")
