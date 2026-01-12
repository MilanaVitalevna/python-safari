"""
Точка входа в игру.
Запускает окно и отображает первую сцену — RulesView.
"""

import arcade

from src.safari.resource_manager import setup_resources

from .constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from .views.rules_view import RulesView


class SafariGame(arcade.Window):
    """Основное окно игры."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.show_view(RulesView())


def main():
    """Запуск приложения."""
    setup_resources()
    SafariGame()
    arcade.run()


if __name__ == "__main__":
    main()
