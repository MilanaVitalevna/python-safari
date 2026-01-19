import arcade

from ..constants import TRACK_ANIMATION_AMPLITUDE, TRACK_ANIMATION_SPEED, TRACK_WIDTH


class Track(arcade.Sprite):
    """
    Дорожки с плавной анимацией движения (±4px).
    Имитирует "живую" дорожку — как в старых автоматах.
    """

    def __init__(self, track_index: int, x: float, y: float, scale: float = 1.0):
        super().__init__()
        self.track_index = track_index
        self.scale = scale

        self.base_center_x = x + TRACK_WIDTH / 2
        self.center_x = self.base_center_x
        self.center_y = y

        # Единая текстура для дорожки
        self.texture = arcade.load_texture(f":slot_machine:/images/tracks/track_{track_index}.png")

        self.offset = 0
        self.direction = 1
        self.speed = TRACK_ANIMATION_SPEED
        self.amplitude = TRACK_ANIMATION_AMPLITUDE

    def on_update(self, delta_time: float):
        self.offset += self.direction * self.speed * delta_time

        if self.offset > self.amplitude:
            self.offset = self.amplitude
            self.direction = -1
        elif self.offset < -self.amplitude:
            self.offset = -self.amplitude
            self.direction = 1

        self.center_x = self.base_center_x + self.offset
