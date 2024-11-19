from classes import EmojiModes, TerraBotEmojis, Placeholders, NoEmojis
from config import config

emoji_mode = config["Параметры"]["emoji_mode"]

global emojis
def set_emojis():
    """Ничего не возвращает.
    Инициализация эмодзи в соответствии с конфигом.
    """
    global emojis
    if emoji_mode == EmojiModes.terra_bot:
        emojis = TerraBotEmojis()

    elif emoji_mode == EmojiModes.placeholder:
        emojis = Placeholders()

    elif emoji_mode == EmojiModes.none:
        emojis = NoEmojis()

set_emojis()
