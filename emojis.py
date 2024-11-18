from classes import EmojiModes, TerraBotEmojis, Placeholders, NoEmojis
from config import emoji_mode

global emojis
def set_emojis():
    """
    Инициализация эмодзи в соответствии с конфигом.
    :return:
    """
    global emojis
    if emoji_mode == EmojiModes.terra_bot:
        emojis = TerraBotEmojis()

    elif emoji_mode == EmojiModes.placeholder:
        emojis = Placeholders()

    elif emoji_mode == EmojiModes.none:
        emojis = NoEmojis()
