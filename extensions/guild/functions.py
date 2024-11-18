from config import master_role_id
from emojis import emojis


def is_master(ctx):
	return ctx.author.get_role(master_role_id) is not None

def create_hit_bar(now_hits: int, more_hits: int, max_hits: int):
	# Нет, мне лень стирать кавычки.
	symbols_dict_now_hits = {
		"1l": f"{emojis.one_l}",
		"1p": f"{emojis.one_p}",
		"1r": f"{emojis.one_r}",
		"0l": f"{emojis.zero_l}",
		"0p": f"{emojis.zero_p}",
		"0r": f"{emojis.zero_r}"
		}
	symbols_dict_more_hits = {
		"0": f"{emojis.zero}",
		"1": f"{emojis.one}",
		"2": f"{emojis.two}",
		"3": f"{emojis.three}",
		"4": f"{emojis.four}",
		"5": f"{emojis.five}",
		"6": f"{emojis.six}",
		"7": f"{emojis.seven}",
		"8": f"{emojis.eight}",
		"9": f"{emojis.nine}"
		}
	bar_segment = max_hits / 10
	if now_hits <= max_hits:
		try:
			filled_segments = int(round(now_hits / bar_segment))
		except ZeroDivisionError:
			filled_segments = 0
	else:
		filled_segments = 10
	raw = ("1" * filled_segments) + ("0" * (10 - filled_segments))
	bar = []
	for symbol in raw:
		bar.append(f"{symbol}p")
	bar[0] = "1l" if bar[0] == "1p" else "0l"
	bar[9] = "1r" if bar[9] == "1p" else "0r"
	for position in range(0,10):
		bar[position] = symbols_dict_now_hits[bar[position]]
	bar = "".join(bar)
	if more_hits > 0:
		more_hits_for_bar = []
		for symbol in str(more_hits):
			more_hits_for_bar.append(symbols_dict_more_hits[symbol])
		bar += (" " + "".join(more_hits_for_bar))
	return bar
