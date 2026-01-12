"""
UI-компонент: модальное окно с правилами игры.

Отображается поверх игровой сцены. Управляет:
- Затемнением фона
- Плавным появлением окна (fade-in)
- Отрисовкой заголовка и текста правил

Не отвечает за переходы — только за визуализацию.
Переход в игру управляется RulesView.
"""

import arcade
from arcade import Text

from ..constants import AVENTURA_FONT_NAME, SAFARI_FONT_NAME


class RulesManager:
    """Управление окном с правилами игры: затемнение с 0 сек, окно плавно появляется за 2 сек."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.show_rules = True
        # Анимация появления окна правил: от 0 до 2 секунд
        self.elapsed_time = 0.0
        self.fade_duration = 2.0  # Плавное появление окна правил
        self.alpha = 0  # Прозрачность окна и текста (0 = скрыто, 255 = видно)
        self.animation_finished = False

    def update(self, delta_time: float):
        """Обновление: окно правил плавно появляется в течение 2 секунд."""
        if not self.show_rules:
            return

        self.elapsed_time += delta_time
        progress = min(self.elapsed_time / self.fade_duration, 1.0)
        self.alpha = int(255 * progress)

        if progress >= 1.0:
            self.alpha = 255
            self.animation_finished = True

    def on_draw(self):
        """Отрисовка: затемнение фона сразу, окно правил — с fade-in."""
        if not self.show_rules:
            return

        # === 1. Затемнение фона — мгновенно (с 0-й секунды) ===
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=self.width,
            bottom=0,
            top=self.height,
            color=(0, 0, 0, 180),  # Полупрозрачный чёрный фон
        )

        # Если окно ещё не видно — дальше не рисуем
        if self.alpha == 0:
            return

        # Размеры окна правил (фиксированные)
        window_width = 800
        window_height = 540
        center_x = self.width / 2
        center_y = self.height / 2
        x = center_x - window_width / 2
        y = center_y - window_height / 2

        # Цвета с прозрачностью (только для окна правил и текста)
        bg_color = (221, 165, 45, self.alpha)  # Фон окна
        border_color = (166, 36, 31, self.alpha)  # Рамка
        text_color = (166, 36, 31, self.alpha)  # Текст

        # === 2. Окно правил — фон и рамка ===
        arcade.draw_lrbt_rectangle_filled(
            left=x, right=x + window_width, bottom=y, top=y + window_height, color=bg_color
        )
        arcade.draw_lrbt_rectangle_outline(
            left=x + 10,
            right=x + window_width - 10,
            bottom=y + 10,
            top=y + window_height - 10,
            color=border_color,
            border_width=4,
        )

        # === 3. Текст — заголовок и правила ===
        title_y = y + window_height - 60
        rules_y = y + window_height - 100

        # Заголовок "САФАРИ"
        title = Text(
            "САФАРИ",
            center_x,
            title_y,
            text_color,
            42,
            anchor_x="center",
            anchor_y="center",
            font_name=SAFARI_FONT_NAME,
        )
        title.draw()

        # Текст правил
        rules_text = (
            "ЗАДАЧА ИГРЫ - ПОРАЗИТЬ ВСЕ ЦЕЛИ: 8 ГАЗЕЛЕЙ, 4 БУЙВОЛА И 1 НОСОРОГА.\n"
            "ВРЕМЯ ИГРЫ - 2 МИНУТЫ, ВСЕГО - 16 ВЫСТРЕЛОВ.\n\n"
            "ОХОТНИК, УПРАВЛЯЕМЫЙ ИГРОКОМ, СКАЧЕТ ПО НИЖНЕЙ ДОРОЖКЕ, САМОСТОЯТЕЛЬНО ПЕРЕПРЫГИВАЯ ЧЕРЕЗ ПРЕПЯТСТВИЯ. "
            'ВЫСТРЕЛ ПРОИЗВОДИТСЯ С ПОМОЩЬЮ ЩЕЛЧКА НА КНОПКЕ "ВЫСТРЕЛ" ИЛИ НАЖАТИЯ КЛАВИШИ ПРОБЕЛ НА КЛАВИАТУРЕ. '
            "ПУЛЯ ЛЕТИТ С ПОСТОЯННОЙ СКОРОСТЬЮ ПОД УГЛОМ 45 ГРАДУСОВ. "
            "В МОМЕНТ ПРЕОДОЛЕНИЯ ПРЕПЯТСТВИЯ ОСУЩЕСТВЛЕНИЕ ВЫСТРЕЛА НЕВОЗМОЖНО. "
            "ВО ВРЕМЯ СТРЕЛЬБЫ НУЖНО ИЗБЕГАТЬ ПОПАДАНИЯ В ПАЛЬМЫ, ЧТОБЫ НЕ ТРАТИТЬ ПАТРОНЫ. "
            "ЕСЛИ ПУЛЯ ПОПАДАЕТ В ЦЕЛЬ, ЖИВОТНОЕ ИСЧЕЗАЕТ С ЭКРАНА "
            "И ЗАГОРАЕТСЯ СООТВЕТСТВУЮЩАЯ ЛАМПОЧКА НА ПАНЕЛИ АВТОМАТА.\n\n"
            "В СЛУЧАЕ ПОРАЖЕНИЯ ВСЕХ МИШЕНЕЙ, ИГРОКУ ДАЕТСЯ ПРИЗОВАЯ ИГРА.\n\n"
            'ДЛЯ ЗАПУСКА ИГРЫ - НАЖМИТЕ КЛАВИШУ "ПРОБЕЛ".\n'
            'ВЫХОД ИЗ ИГРЫ - С ПОМОЩЬЮ КЛАВИШИ "ESC".'
        )

        rules = Text(
            rules_text,
            center_x,
            rules_y,
            text_color,
            11,
            anchor_x="center",
            anchor_y="top",
            multiline=True,
            width=window_width - 60,
            align="center",
            font_name=AVENTURA_FONT_NAME,
        )
        rules.draw()

    def hide(self):
        """Скрыть окно с правилами."""
        self.show_rules = False
