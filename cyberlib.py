# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cyberlib.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/21 09:31:07 by ysabik            #+#    #+#              #
#    Updated: 2024/12/01 02:50:51 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Any


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

	@staticmethod
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

	@staticmethod
	def print(
			*values: object,
			sep: str | None = " ",
			end: str | None = "\n",
			reset: bool = True,
			char: str = DEFAULT_MAGIC_CHAR,
			) -> None:
		s = sep.join(str(value) for value in values)
		if reset:
			print(Color.c(s, char) + Color.RESET, end=end)
		else:
			print(Color.c(s, char), end=end)


def cprint(
		*values: object,
		sep: str | None = " ",
		end: str | None = "\n",
		reset: bool = True,
		char: str = Color.DEFAULT_MAGIC_CHAR,
		) -> None:
	Color.print(*values, sep=sep, end=end, reset=reset, char=char)


class ArgError(Exception):
	pass


class ArgFlag:
	def __init__(self, short: str | None, long: str | None,
			args: list[str] | None, desc: str | None) -> None:
		self.short: str | None			= short
		self.long: str | None			= long
		self.args: list[str] | None		= args
		self.desc: str | None			= desc
		self.values: list[str]			= []

		self.combinable: bool	= len(self.short) == 1 if self.short else False
		self.args_len: int	= sum(len(arg) + 3 for arg in args) if args else 0
		self.short_len: int	= len(short) + 1 + self.args_len if short else 0
		self.long_len: int	= len(long) + 2 + self.args_len if long else 0

	def clear(self) -> None:
		self.values.clear()

	def __str__(self, short_len: int = 0, long_len: int = 0) -> str:
		short = ''
		if self.short:
			f = '{:<' + str(short_len + (2 if self.long else 0)) + '}'
			comma = ', ' if self.long else ''
			if self.args:
				short = f.format(f'-{self.short} <{self.args[0]}>{comma}')
			else:
				short = f.format(f'-{self.short}{comma}')
		long = ''
		if self.long:
			if not self.short:
				short += ' ' * (short_len + 2)
			f = '{:<' + str(long_len) + '}'
			if self.args:
				long = f.format(f'--{self.long} <{self.args[0]}>')
			else:
				long = f.format(f'--{self.long}')
		elif long_len:
			long = ' ' * (long_len + (2 if short else 0))
		return f'{short}{long}  {"" if self.desc is None else self.desc}'

	def __repr__(self) -> str:
		return '<ArgFlag' \
			+ f' short={"None" if self.short is None else repr(self.short)}' \
			+ f' long={"None" if self.long is None else repr(self.long)}' \
			+ f' args={self.args}' \
			+ f' desc={"None" if self.desc is None else repr(self.desc)}' \
			+ f' combinable={self.combinable}' \
			+ f' args_len={self.args_len}' \
			+ f' short_len={self.short_len}' \
			+ f' long_len={self.long_len}' \
			+ f' values={self.values}' \
			+ '>'


class ArgParser:
	def __init__(self, args: list[str], case_sensitive: bool = True) -> None:
		'''Create a new ArgParser object

		:param args: The arguments to parse (usually `sys.argv[1:]` --> `sys.argv` without the script name)
		:type args: list[str]
		:param case_sensitive: Whether the parser should be case sensitive or not ONLY for flags
		:type case_sensitive: bool

		:Example: ::
			ArgParser(sys.argv)
				.add_flag('v', 'verbose', None, 'Print more information')
				.add_flag('q', 'quiet', None, 'Print less information')
				.parse()

			# If the script is called with `./script.py -v abc --quiet def`
			# The flags will be:
			#   - verbose: ['0']
			#   - quiet: ['2']
			# And the free_args will be: ['abc', 'def']
		'''
		self.args: list[str]		= args
		self.case_sensitive: bool	= case_sensitive
		self.pre_desc: list[str]	= []
		self.post_desc: list[str]	= []
		self.flags: list[ArgFlag]	= []
		self.free_args: list[str]	= []

	def add_pre_desc(self, *desc: Any, sep: str = ' ') -> 'ArgParser':
		'''Set the description to display before the flags

		:param desc: The description to display before the flags
		:type desc: str

		:return: The current ArgParser object
		:rtype: ArgParser
		'''
		self.pre_desc.append(sep.join(str(d) for d in desc))
		return self

	def add_post_desc(self, *desc: str, sep: str = ' ') -> 'ArgParser':
		'''Set the description to display after the flags

		:param desc: The description to display after the flags
		:type desc: str

		:return: The current ArgParser object
		:rtype: ArgParser
		'''
		self.post_desc.append(sep.join(str(d) for d in desc))
		return self

	def add_flag(self, short: str | None, long: str | None,
			args: list[str] | None, desc: str | None) -> 'ArgParser':
		'''Add a flag (new instance of :class:`ArgFlag`) to the parser

		:param short: The short name of the flag (not including the '-')
		:type short: str
		:param long: The long name of the flag (not including the '--')
		:type long: str
		:param args: The arguments the flag requires
		:type args: list[str]
		:param desc: The description of the flag
		:type desc: str

		:return: The current ArgParser object
		:rtype: ArgParser
		'''
		self.flags.append(ArgFlag(short, long, args, desc))
		return self

	def parse(self) -> 'ArgParser':
		'''Parse the arguments and fill the flags and free_args lists

		:raises ArgError: If an unknown flag is found or if a flag requires more arguments

		:return: The current ArgParser object
		:rtype: ArgParser
		'''
		self.free_args.clear()
		(flag.clear() for flag in self.flags)
		i = 0
		free_only = False
		while i < len(self.args):
			arg = self.args[i] if self.case_sensitive else self.args[i].lower()
			if not free_only and arg == '--':
				free_only = True
			elif not free_only and arg.startswith('-') and arg != '-':
				for flag in self.flags:
					short, long = f'-{flag.short}', f'--{flag.long}'
					if not self.case_sensitive:
						short, long = short.lower(), long.lower()
					if arg == short or arg == long:
						if flag.args:
							flag.values.clear()
							i += 1
							while len(flag.values) < len(flag.args) \
									and i < len(self.args) \
									and not self.args[i].startswith('-'):
								flag.values.append(self.args[i])
								i += 1
							i -= 1
							if len(flag.values) != len(flag.args):
								raise ArgError(f'Not enough arguments for flag {arg}')
						else:
							flag.values.append(f'{i}')
						break
				else:
					if arg[1] == '-':
						raise ArgError(f'Unknown flag {arg}')
					for j, c in enumerate(arg[1:]):
						for flag in self.flags:
							if not flag.combinable:
								continue
							sh = flag.short if self.case_sensitive else flag.short.lower()
							if c == sh:
								if flag.args:
									flag.values.clear()
									i += 1
									while len(flag.values) < len(flag.args) \
											and i < len(self.args) \
											and not self.args[i].startswith('-'):
										flag.values.append(self.args[i])
										i += 1
									i -= 1
									if len(flag.values) != len(flag.args):
										raise ArgError(f'Not enough arguments for flag -{c} (at position {j} in {arg})')
								else:
									flag.values.append(f'{i}.{j}')
								break
						else:
							raise ArgError(f'Unknown flag -{c} (at position {j} in {arg})')
			else:
				self.free_args.append(self.args[i])
			i += 1
		return self

	def get_flag(self, identifier: int | str) -> ArgFlag | None:
		'''Get a flag by its identifier

		:param identifier: The identifier of the flag (either the index, the short or the long name)
		:type identifier: int | str

		:return: The flag if found, None otherwise
		:rtype: ArgFlag | None
		'''
		if isinstance(identifier, int):
			if identifier >= 0 and identifier < len(self.flags):
				return list(self.flags)[identifier]
		identifier = str(identifier)
		for flag in self.flags:
			short, long = f'-{flag.short}', f'--{flag.long}'
			if not self.case_sensitive:
				short, long = short.lower(), long.lower()
			if identifier == short or identifier == long:
				return flag
		for flag in self.flags:
			short, long = flag.short, flag.long
			if not self.case_sensitive:
				short, long = short.lower(), long.lower()
			if identifier == short or identifier == long:
				return flag
		return None

	def get_value(self, identifier: int | str, default: Any | None = None) -> str | None:
		'''Get the UNIQUE (first) value of a flag by its identifier

		:param identifier: The identifier of the flag (either the index, the short or the long name)
		:type identifier: int | str

		:raises ArgError: If the flag is unknown

		:return: The UNIQUE (first) value of the flag has a value, else default if specified, None otherwise
		:rtype: Any | None
		'''
		flag = self.get_flag(identifier)
		if flag is None:
			raise ArgError(f'Unknown flag `{identifier}` (as identifier)')
		return flag.values[0] if flag.values else default

	def get_values(self, identifier: int | str) -> list[str]:
		'''Get the values of a flag by its identifier

		:param identifier: The identifier of the flag (either the index, the short or the long name)
		:type identifier: int | str

		:raises ArgError: If the flag is unknown

		:return: The values of the flag
		:rtype: list[str]
		'''
		flag = self.get_flag(identifier)
		if flag is None:
			raise ArgError(f'Unknown flag `{identifier}` (as identifier)')
		return flag.values

	def __str__(self) -> str:
		'''Return a string representation of the ArgParser object

		:return: The string representation of the ArgParser object
		:rtype: str

		:Example: ::
			parser = ArgParser(sys.argv)
				.add_flag('v',  'verbose', None,    'Print more information')
				.add_flag('q',  'quiet',   None,    'Print less information')
				.add_flag(None, 'foo',     ['foo'], 'A foo flag')
				.add_flag('b',  None,      ['bar'], 'A bar flag')
				.add_flag('q',  'quux',    ['fb'],  'A quux flag')
				.parse()
			print(parser)

			# Output:
			# Flags:
			#             --foo <foo>  A foo flag
			#   -v,       --verbose    Print more information
			#   -x <fb>,  --quux <fb>  A quux flag
			#   -q,       --quiet      Print less information
			#   -b <bar>               A bar flag
		'''
		short_len = max((flag.short_len for flag in self.flags), default=0)
		long_len = max((flag.long_len for flag in self.flags), default=0)
		lines = '\n'.join('  ' + flag.__str__(short_len, long_len) for flag in self.flags)
		string = ''
		if self.pre_desc is not None:
			string += '\n'.join(self.pre_desc) + '\n\n'
		string += 'Flags:\n' + lines
		if self.post_desc is not None:
			string += '\n\n' + '\n'.join(self.post_desc)
		return string

	def __repr__(self) -> str:
		return '<ArgParser' \
			+ f' args={self.args}' \
			+ f' case_sensitive={self.case_sensitive}' \
			+ f' pre_desc={self.pre_desc}' \
			+ f' post_desc={self.post_desc}' \
			+ f' free_args={self.free_args}' \
			+ f' flags={self.flags}' \
			+ '>'
