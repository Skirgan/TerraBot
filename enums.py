import enum
from config import emoji_mode

class EmojiModes(enum.Enum):
    terra_bot = 1
    placeholder = 2
    none = 3

# Прошу соблюдать либо алфавитный, либо числовой порядок в названиях аттрибутов.
class TerraBotEmojis(enum.Enum):
    administrator = "<:administrator:1297268078375080036>"
    block = "<:block:1297268337264300094>"
    check = "<:check:1297268217303007314>"
    cross = "<:cross:1297268043667476490>"
    delete = "<:delete:1297268016827858954>"
    manage = "<:manage:1297268323200929842>"
    members = "<:members:1297268054840971265>"
    moderator = "<:moderator:1297268117965377689>"
    mute = "<:mute:1297267954022617279>"
    like = "<:like:1297268354570260611>"
    logs = "<:logs:1297268241105944788>"
    minus = "<:minus:1297268270126338120>"
    plus = "<:plus:1297268385863700603>"
    profile = "<:profile:1297268006468190269>"
    search = "<:search:1297268102089670666>"
    secure = "<:secure:1297268147363123200>"
    staff = "<:staff:1297268197581520926>"
    stats = "<:stats:1297268132666150993>"
    unblock = "<:unblock:1297267969096810567>"

    zero_l = "<:0l:1304560675787509811>"
    zero_p = "<:0p:1304560694775119994>"
    zero_r = "<:0r:1304560685459443712>"
    one_l = "<:1l:1304560712126824478>"
    one_p = "<:1p:1304560732695695360>"
    one_r = "<:1r:1304560721303965766>"

    zero = "<:0n:1304563382984376371>"
    one = "<:1n:1304563392043814922>"
    two = "<:2n:1304563403875942400>"
    three = "<:3n:1304563414546382888>"
    four = "<:4n:1304563422985191464>"
    five = "<:5n:1304563435157323988>"
    six = "<:6n:1304563443033968701>"
    seven = "<:7n:1304563451594539148>"
    eight = "<:8n:1304563460201513141>"
    nine = "<:9n:1304563470032699412>"

class Placeholders(enum.Enum):
    administrator = ":cool:"
    block = ":cool:"
    check = ":cool:"
    cross = ":cool:"
    delete = ":cool:"
    manage = ":cool:"
    members = ":cool:"
    moderator = ":cool:"
    mute = "cool"
    like = ":cool:"
    logs = ":cool:"
    minus = ":cool:"
    plus = ":cool:"
    profile = ":cool:"
    search = ":cool:"
    secure = ":cool:"
    staff = ":cool:"
    stats = ":cool:"
    unblock = ":cool:"

    zero_l = ":cool:"
    zero_p = ":cool:"
    zero_r = ":cool:"
    one_l = ":cool:"
    one_p = ":cool:"
    one_r = ":cool:"

    zero = ":cool:"
    one = ":cool:"
    two = ":cool:"
    three = ":cool:"
    four = ":cool:"
    five = ":cool:"
    six = ":cool:"
    seven = ":cool:"
    eight = ":cool:"
    nine = ":cool:"

class NoEmojis(enum.Enum):
    administrator = ""
    block = ""
    check = ""
    cross = ""
    delete = ""
    manage = ""
    members = ""
    moderator = ""
    mute = ""
    like = ""
    logs = ""
    minus = ""
    plus = ""
    profile = ""
    search = ""
    secure = ""
    staff = ""
    stats = ""
    unblock = ""

    zero_l = ""
    zero_p = ""
    zero_r = ""
    one_l = ""
    one_p = ""
    one_r = ""

    zero = ""
    one = ""
    two = ""
    three = ""
    four = ""
    five = ""
    six = ""
    seven = ""
    eight = ""
    nine = ""

# Инициализация эмодзи в соответствии с конфигом.
if emoji_mode == EmojiModes.terra_bot:
    emojis = TerraBotEmojis

elif emoji_mode == EmojiModes.placeholder:
    emojis = Placeholders

elif emoji_mode == EmojiModes.none:
    emojis = NoEmojis
