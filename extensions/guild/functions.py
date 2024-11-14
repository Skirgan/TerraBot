from config import master_role_id

def is_master(ctx):
	return ctx.author.get_role(master_role_id) is not None

def create_hit_bar(now_hits: int, more_hits: int, max_hits: int):
	symbols_dict_now_hits = {
		"1l": "<:1l:1304560712126824478>",
		"1p": "<:1p:1304560732695695360>",
		"1r": "<:1r:1304560721303965766>",
		"0l": "<:0l:1304560675787509811>",
		"0p": "<:0p:1304560694775119994>",
		"0r": "<:0r:1304560685459443712>"
		}
	symbols_dict_more_hits = {
		"0": "<:0n:1304563382984376371>",
		"1": "<:1n:1304563392043814922>",
		"2": "<:2n:1304563403875942400>",
		"3": "<:3n:1304563414546382888>",
		"4": "<:4n:1304563422985191464>",
		"5": "<:5n:1304563435157323988>",
		"6": "<:6n:1304563443033968701>",
		"7": "<:7n:1304563451594539148>",
		"8": "<:8n:1304563460201513141>",
		"9": "<:9n:1304563470032699412>"
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
