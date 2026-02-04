import arcade

from ...resource_manager import Textures


class Animal(arcade.TextureAnimationSprite):
    """
    Базовый класс для всех животных.

    Использует TextureAnimation для анимации движения.

    Особенности:
    - Является целью для победы (даёт очки при попадании)
    - При попадании пули исчезает
    - Удаляется при выходе за левую границу экрана
    - Движение справа налево
    """

    def __init__(
        self,
        animation_name: str,  # Имя анимации в Textures (например, "rhino_animation")
        x: int,
        y: int,
        speed: float,
        despawn_x: int,
        y_offset: int = 0,
    ):
        """
        Инициализация животного с анимацией.

        Args:
            animation_name: Имя атрибута анимации в классе Textures
            x: Начальная позиция X
            y: Начальная позиция Y
            speed: Скорость движения (пикселей в секунду)
            despawn_x: X-координата, при которой нужно удалить животное
            y_offset: Y-смещение для центрирования
        """
        # Получаем анимацию по имени
        animation = getattr(Textures, animation_name, None)
        if not animation:
            raise RuntimeError(f"Анимация '{animation_name}' не создана в Textures")

        super().__init__(center_x=x, center_y=y + y_offset, animation=animation)

        # Параметры движения
        self.speed = speed
        self.despawn_x = despawn_x

        # Состояние
        self.is_alive = True

    def on_update(self, delta_time: float = 1 / 60):
        """
        Обновление состояния: движение справа налево и анимация.

        Args:
            delta_time: Время с последнего обновления в секундах
        """
        # Движение справа налево
        self.center_x -= self.speed * delta_time

        # Обновление анимации (автоматически управляет кадрами)
        self.update_animation(delta_time)

    def on_hit(self):
        """Логика при попадании пули."""
        if not self.is_alive:
            return

        # Изменяем состояние
        self.is_alive = False

    def should_be_removed(self) -> bool:
        """
        Проверка, нужно ли удалять объект.

        Returns:
            True если нужно удалить (вышел за границу или убит)
        """
        # Удаляем если вышел за границу ИЛИ убит
        return self.center_x <= self.despawn_x or not self.is_alive
