import enum
from config import emoji_mode

class EmojiModes(enum.Enum):
    terra_bot = 1
    placeholder = 2
    none = 3

# Прошу соблюдать либо алфавитный, либо числовой порядок в названиях аттрибутов.
class TerraBotEmojis:
    administrator = "<:administrator:1297268078375080036>"
    block = "<:block:1297268337264300094>"
    check = "<:check:1297268217303007314>"
    cross = "<:cross:1297268043667476490>"
    delete = "<:delete:1297268016827858954>"
    dislike = "<:dislike:1297275987012358165>"
    mail = "<:mail:1297268371263586367>"
    manage = "<:manage:1297268323200929842>"
    member = "<:member:1297268091197067396>"
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
    write = "<:write:1297267979402084402>"

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

class Placeholders:
    __ph = ":cool:"    #  (PlaceHolder); Два нижних подчёркивания в начале делают переменную приватной (её не вызвать через Placeholders.__ph)
    administrator = __ph
    block = __ph
    check = __ph
    cross = __ph
    delete = __ph
    dislike = __ph
    mail = __ph
    manage = __ph
    member = __ph
    members = __ph
    moderator = __ph
    mute = __ph
    like = __ph
    logs = __ph
    minus = __ph
    plus = __ph
    profile = __ph
    search = __ph
    secure = __ph
    staff = __ph
    stats = __ph
    unblock = __ph
    write = __ph

    zero_l = __ph
    zero_p = __ph
    zero_r = __ph
    one_l = __ph
    one_p = __ph
    one_r = __ph

    zero = __ph
    one = __ph
    two = __ph
    three = __ph
    four = __ph
    five = __ph
    six = __ph
    seven = __ph
    eight = __ph
    nine = __ph

class NoEmojis:
    administrator = ""
    block = ""
    check = ""
    cross = ""
    delete = ""
    dislike = ""
    mail = ""
    manage = ""
    member = ""
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
