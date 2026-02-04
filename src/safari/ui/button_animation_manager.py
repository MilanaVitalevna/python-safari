"""
Менеджер анимации нажатия кнопки.
Отображает нажатую кнопку в течение 500 мс при выстреле.
"""

import arcade

from ..constants import BUTTON_POSITION, BUTTON_PRESS_DURATION
from ..resource_manager import Textures


class ButtonAnimationManager:
    """
    Управляет анимацией нажатия кнопки выстрела.
    """

    def __init__(self):
        # Спрайт нажатой кнопки
        self.button_sprite = None

        # SpriteList для отрисовки
        self.sprite_list = arcade.SpriteList()

        # Таймер анимации
        self.press_timer = 0.0
        self.is_pressed = False

        # Флаг инициализации
        self._initialized = False

    def setup(self):
        """Создает спрайт нажатой кнопки."""
        if self._initialized:
            return

        if not Textures.button_pressed:
            print("⚠️ Текстура нажатой кнопки не загружена")
            return

        try:
            # Создаем спрайт нажатой кнопки
            self.button_sprite = arcade.Sprite()
            self.button_sprite.texture = Textures.button_pressed
            self.button_sprite.center_x = BUTTON_POSITION[0]
            self.button_sprite.center_y = BUTTON_POSITION[1]
            self.button_sprite.visible = False  # По умолчанию невидима

            # Добавляем в SpriteList для отрисовки
            self.sprite_list.append(self.button_sprite)

            self._initialized = True
            print("✅ Анимация кнопки инициализирована")
        except Exception as e:
            print(f"❌ Ошибка создания анимации кнопки: {e}")

    def press(self):
        """Запускает анимацию нажатия кнопки."""
        if not self._initialized or not self.button_sprite:
            return

        self.is_pressed = True
        self.press_timer = BUTTON_PRESS_DURATION
        self.button_sprite.visible = True

    def update(self, delta_time: float):
        """Обновляет таймер анимации."""
        if not self.is_pressed:
            return

        self.press_timer -= delta_time

        if self.press_timer <= 0:
            self.is_pressed = False
            if self.button_sprite:
                self.button_sprite.visible = False

    def draw(self):
        """Отрисовывает нажатую кнопку (если она видима)."""
        if self._initialized and self.sprite_list:
            self.sprite_list.draw()

    def reset(self):
        """Сбрасывает анимацию."""
        self.is_pressed = False
        self.press_timer = 0.0
        if self.button_sprite:
            self.button_sprite.visible = False
