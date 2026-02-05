from .constants import (
    VICTORY_REQUIREMENTS,
)


class ScoreManager:
    """
    Простой менеджер очков - только счётчики убийств.
    """

    def __init__(self):
        # Счётчики убитых животных
        self.gazelle_kills = 0
        self.bizon_kills = 0
        self.rhino_kills = 0

    def setup(self):
        pass

    def register_kill(self, animal_type: str) -> bool:
        """Добавляет убитое животное и включает индикатор."""
        if animal_type == "gazelle":
            self.gazelle_kills += 1
            return True

        elif animal_type == "bizon":
            self.bizon_kills += 1
            return True

        elif animal_type == "rhino":
            self.rhino_kills += 1
            return True

        return False

    def is_victory(self) -> bool:
        """Проверяет, достигнута ли победа."""
        return (
                self.gazelle_kills >= VICTORY_REQUIREMENTS["gazelle"] and
                self.bizon_kills >= VICTORY_REQUIREMENTS["bizon"] and
                self.rhino_kills >= VICTORY_REQUIREMENTS["rhino"]
        )

    def reset(self):
        """Сбрасывает всё."""
        self.gazelle_kills = 0
        self.bizon_kills = 0
        self.rhino_kills = 0
