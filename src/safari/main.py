"""
Main entry point for Safari Arcade Game
"""

import arcade

from .constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH


class SafariGame(arcade.Window):
    """Main game window"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""
        self.clear()

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here."""
        pass

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        pass

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        pass


def main():
    """Main function"""
    window = SafariGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
