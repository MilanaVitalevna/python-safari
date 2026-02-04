import arcade

from ...constants import (
    HUNTER_JUMP_DETECTION_DISTANCE,
    HUNTER_JUMP_DURATION,
    HUNTER_JUMP_Y_OFFSET,
    HUNTER_SPEED,
    HUNTER_START_X,
    HUNTER_Y,
)
from ...resource_manager import Textures


class Hunter(arcade.TextureAnimationSprite):
    """Современный спрайт охотника с анимациями на основе TextureAnimation."""

    def __init__(self):
        # Проверяем, что анимации созданы
        if not Textures.hunter_run_animation:
            raise RuntimeError("Анимация бега охотника не создана в Textures")
        if not Textures.hunter_jump_animation:
            raise RuntimeError("Анимация прыжка охотника не создана в Textures")

        # Инициализируем с анимацией бега
        super().__init__(center_x=HUNTER_START_X, center_y=HUNTER_Y, animation=Textures.hunter_run_animation)

        # Сохраняем ссылки на анимации для быстрого доступа
        self.run_animation = Textures.hunter_run_animation
        self.jump_animation = Textures.hunter_jump_animation

        # Физика и состояние
        self.speed = HUNTER_SPEED
        self.is_jumping = False
        self.jump_timer = 0.0
        self.jump_duration = HUNTER_JUMP_DURATION / 1000.0  # в секундах
        self.normal_y = HUNTER_Y  # Нормальная позиция Y
        self.jump_y = HUNTER_Y + HUNTER_JUMP_Y_OFFSET  # Позиция в прыжке

    def on_update(self, delta_time: float = 1 / 60):
        """Обновляет позицию и анимацию охотника."""
        # Движение слева направо
        self.center_x += self.speed * delta_time

        # Обработка прыжка
        if self.is_jumping:
            self.jump_timer += delta_time

            # Проверяем завершение прыжка
            if self.jump_timer >= self.jump_duration:
                self._end_jump()
            else:
                # Обновляем анимацию прыжка
                self.update_animation(delta_time)
        else:
            # Обновляем анимацию бега
            self.update_animation(delta_time)

    def jump(self):
        """Начинает прыжок."""
        if self.is_jumping:
            return  # Уже прыгаем

        self.is_jumping = True
        self.jump_timer = 0.0
        self.center_y = self.jump_y

        # Переключаем на анимацию прыжка
        self.animation = self.jump_animation
        self.time = 0.0  # Сбрасываем время анимации к началу

    def _end_jump(self):
        """Завершает прыжок и возвращает к бегу."""
        self.is_jumping = False
        self.center_y = self.normal_y

        # Возвращаем анимацию бега
        self.animation = self.run_animation
        self.time = 0.0  # Сбрасываем время анимации

    def run(self):
        """Явный переход к анимации бега."""
        self._end_jump()

    def check_for_obstacles(self, barriers):
        """Проверяет препятствия и прыгает при необходимости."""
        if self.is_jumping:
            return

        for barrier in barriers:
            # Проверяем на препятствие впереди
            if barrier.center_x - self.center_x < HUNTER_JUMP_DETECTION_DISTANCE and barrier.center_x > self.center_x:
                self.jump()
                return
