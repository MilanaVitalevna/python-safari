import arcade

# Импортируем константы
from .constants import (
    GLARE_EFFECT,
    SCREEN_CENTER,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    SLOT_MACHINE_FRAME,
    START_SOUND_PATH,
    TV_BACKGROUND,
)

# Импортируем UI компоненты
from .ui.rules import RulesManager


class SafariGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Создаем отдельные SpriteList для каждого слоя
        self.background_sprites: arcade.SpriteList = arcade.SpriteList()  # ТВ-экран
        self.effect_sprites: arcade.SpriteList = arcade.SpriteList()  # Блик
        self.slot_machine_sprite: arcade.SpriteList = arcade.SpriteList()  # Автомат

        # Управление окном с правилами
        self.rules_manager: RulesManager = RulesManager(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Загружаем спрайты
        self.load_sprites()

        # 💡 Загружаем и проигрываем стартовый звук
        try:
            if START_SOUND_PATH.exists():
                start_sound = arcade.load_sound(START_SOUND_PATH)
                arcade.play_sound(start_sound)
            else:
                print(f"⚠️ Файл звука не найден: {START_SOUND_PATH}")
        except Exception as e:
            print(f"❌ Ошибка воспроизведения звука: {e}")

    def load_sprites(self):
        """Загрузка всех спрайтов"""
        try:
            # 1. ТВ-экран (самый задний)
            tv_sprite = arcade.Sprite(TV_BACKGROUND, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.background_sprites.append(tv_sprite)

            # 2. Блик экрана (средний)
            glare_sprite = arcade.Sprite(GLARE_EFFECT, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.effect_sprites.append(glare_sprite)

            # 3. Автомат (самый передний)
            frame_sprite = arcade.Sprite(SLOT_MACHINE_FRAME, center_x=SCREEN_CENTER[0], center_y=SCREEN_CENTER[1])
            self.slot_machine_sprite.append(frame_sprite)

        except FileNotFoundError as e:
            print(f"✗ Ошибка загрузки файлов: {e}")

    def on_update(self, delta_time: float):
        """Вызывается каждый кадр."""
        self.rules_manager.update(delta_time)

    def on_draw(self):
        """Ключевой момент: правильный порядок отрисовки!"""
        self.clear()

        # Отрисовка в порядке слоёв
        # 1️⃣ Сначала рисуем ТВ-экран (SpriteList!)
        self.background_sprites.draw()
        # 2️⃣ Потом блик (он будет поверх ТВ-экрана)
        self.effect_sprites.draw()
        # 3️⃣ В конце автомат (будет поверх всего)
        self.slot_machine_sprite.draw()

        # ✅ Рисуем окно с правилами
        self.rules_manager.on_draw()

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        # Сначала обрабатываем окно с правилами
        if self.rules_manager.on_key_press(key, modifiers):
            return

        # Затем основные команды
        if key == arcade.key.ESCAPE:
            arcade.exit()


# Запуск
def main() -> None:
    """Точка входа в игру."""
    SafariGame()
    arcade.run()


if __name__ == "__main__":
    main()
