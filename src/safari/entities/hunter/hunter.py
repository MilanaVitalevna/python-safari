import arcade

from src.safari.constants import (
    HUNTER_ANIMATION_SPEED,
    HUNTER_JUMP_DURATION,
    HUNTER_SPEED,
    HUNTER_START_X,
    HUNTER_Y,
)
from src.safari.resource_manager import Textures


class Hunter(arcade.Sprite):
    """Спрайт охотника с анимацией бега и прыжка."""

    def __init__(self):
        super().__init__()

        # Позиция
        self.center_x = HUNTER_START_X
        self.center_y = HUNTER_Y

        # Инициализация текстур
        self.run_textures = None
        self.jump_texture = None

        # Физика
        self.speed = HUNTER_SPEED

        # Состояние анимации
        self.is_jumping = False
        self.jump_timer = 0.0
        self.jump_duration = HUNTER_JUMP_DURATION / 1000

        # Анимация бега
        self.run_frame = 0
        self.run_frame_timer = 0.0
        self.run_frame_duration = HUNTER_ANIMATION_SPEED / 1000

        # Флаг, что текстуры загружены
        self._textures_loaded = False

    def setup(self):
        """Загружает текстуры охотника из менеджера ресурсов."""
        if self._textures_loaded:
            return  # Уже загружено

        self._validate_and_load_textures()
        self._textures_loaded = True

    def _validate_and_load_textures(self):
        """Проверяет и загружает текстуры охотника."""
        if not Textures.hunter:
            raise RuntimeError("Текстуры охотника не загружены (Textures.hunter is None)")

        if len(Textures.hunter) < 4:
            raise RuntimeError(f"Недостаточно текстур охотника. Ожидалось 4, получено {len(Textures.hunter)}")

        self.run_textures = Textures.hunter[:3]  # Первые 3 - бег
        self.jump_texture = Textures.hunter[3]  # 4-я - прыжок

        # Устанавливаем начальную текстуру
        self.texture = self.run_textures[0]

    def on_update(self, delta_time: float = 1 / 60):
        """Обновляет позицию и анимацию охотника."""
        # Проверяем, что текстуры загружены
        if not self._textures_loaded:
            self.setup()

        # Движение слева направо
        self.center_x += self.speed * delta_time

        # Обработка прыжка
        if self.is_jumping:
            self.jump_timer += delta_time
            if self.jump_timer >= self.jump_duration:
                self._end_jump()
            return

        # Анимация бега (только если не прыгает)
        self.run_frame_timer += delta_time
        if self.run_frame_timer >= self.run_frame_duration:
            self.run_frame = (self.run_frame + 1) % len(self.run_textures)
            self.texture = self.run_textures[self.run_frame]
            self.run_frame_timer = 0.0

    def jump(self):
        """Начинает прыжок."""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_timer = 0.0
            self.texture = self.jump_texture

    def _end_jump(self):
        """Завершает прыжок и возвращает к бегу."""
        self.is_jumping = False
        self.run_frame = 0
        self.texture = self.run_textures[0]
        self.run_frame_timer = 0.0

    def run(self):
        """Явный переход к анимации бега."""
        self._end_jump()
