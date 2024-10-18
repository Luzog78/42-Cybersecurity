class Color:
	BLACK		= '\033[30m'
	RED			= '\033[31m'
	GREEN		= '\033[32m'
	YELLOW		= '\033[33m'
	BLUE		= '\033[34m'
	MAGENTA		= '\033[35m'
	CYAN		= '\033[36m'
	WHITE		= '\033[37m'

	BOLD		= '\033[1m'
	FAINT		= '\033[2m'
	ITALIC		= '\033[3m'
	UNDERLINE	= '\033[4m'
	BLINK		= '\033[5m'
	REVERSE		= '\033[7m'
	HIDDEN		= '\033[8m'
	STRIKE		= '\033[9m'

	BG_BLACK	= '\033[40m'
	BG_RED		= '\033[41m'
	BG_GREEN	= '\033[42m'
	BG_YELLOW	= '\033[43m'
	BG_BLUE		= '\033[44m'
	BG_MAGENTA	= '\033[45m'
	BG_CYAN		= '\033[46m'
	BG_WHITE	= '\033[47m'

	RESET		= '\033[0m'

	COLORS = [
		BLACK,
		RED,
		GREEN,
		YELLOW,
		BLUE,
		MAGENTA,
		CYAN,
		WHITE,
	]

	BG_COLORS = [
		BG_BLACK,
		BG_RED,
		BG_GREEN,
		BG_YELLOW,
		BG_BLUE,
		BG_MAGENTA,
		BG_CYAN,
		BG_WHITE,
	]

	MODIFIERS = [
		BOLD,
		FAINT,
		ITALIC,
		UNDERLINE,
		BLINK,
		REVERSE,
		HIDDEN,
		STRIKE,
	]

	codes = [
		*COLORS,
		*BG_COLORS,
		*MODIFIERS,
		RESET,
	]

	table = {
		'0': RESET + BLACK,
		'1': RESET + BLUE + FAINT,
		'2': RESET + GREEN + FAINT,
		'3': RESET + CYAN + FAINT,
		'4': RESET + RED + FAINT,
		'5': RESET + MAGENTA + FAINT,
		'6': RESET + YELLOW + FAINT,
		'7': RESET + WHITE + FAINT,
		'8': RESET + BLACK + FAINT,
		'9': RESET + BLUE,
		'a': RESET + GREEN,
		'b': RESET + CYAN,
		'c': RESET + RED,
		'd': RESET + MAGENTA,
		'e': RESET + YELLOW,
		'f': RESET + WHITE,
		'l': BOLD,
		'n': UNDERLINE,
		'o': ITALIC,
		'k': BLINK,
		'm': REVERSE,
		'p': HIDDEN,
		's': STRIKE,
		'q': FAINT,
		'r': RESET,

		'G': BG_BLACK,
		'H': BG_BLUE,
		'A': BG_GREEN,
		'B': BG_CYAN,
		'C': BG_RED,
		'D': BG_MAGENTA,
		'E': BG_YELLOW,
		'F': BG_WHITE,
	}

	DEFAULT_MAGIC_CHAR = '§'

	def c(s: str, char: str = DEFAULT_MAGIC_CHAR) -> str:
		string = ''
		s_len = len(s)
		i = 0
		while i < s_len:
			if s[i] == char:
				i += 1
				if i < s_len:
					if s[i] == char:
						string += char
					elif s[i] in Color.table:
						string += Color.table[s[i]]
			else:
				string += s[i]
			i += 1
		return string
