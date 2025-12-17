# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/28 09:59:49 by luzog78           #+#    #+#              #
#    Updated: 2025/12/17 05:01:44 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import json
import datetime

from vaccine import Vaccine, print_error


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from cyberlib import cprint, ArgParser, ArgError


def parse(app: Vaccine, args: ArgParser) -> int | None:
	try:
		args.parse()
	except ArgError as e:
		print_error(e, traceback=False, use_cprint=True)
		return 1

	if args.get_value('h'):
		cprint(args)
		return 0

	if len(args.free_args) < 1:
		print_error(ArgError('You must provide an URL.'), traceback=False, use_cprint=True)
		return 1
	elif len(args.free_args) > 1:
		print_error(ArgError('Too many arguments provided.'), traceback=False, use_cprint=True)
		return 1

	app.url = args.free_args[0]

	if (injections_mode := args.get_value('m')) is None:
		injections_mode = 'all'
	if injections_mode not in ['all', 'stacked', 'union', 'blind-bool']:
		print_error(ArgError(f'Injections mode not supported: "{injections_mode}"'), traceback=False, use_cprint=True)
		return 1
	app.injections_mode = injections_mode

	if (injections_file := args.get_value('i')) is None:
		injections_file = Vaccine.DEFAULT_INJECTIONS_FILE

	try:
		with open(injections_file, 'r') as f:
			app.injections = json.load(f)
		assert 'version' in app.injections, 'Missing "version" in injections file'
		assert 'injections' in app.injections, 'Missing "injections" in injections file'
		assert 'errors' in app.injections['injections'], 'Missing "errors" in injections file'
		assert 'error_signatures' in app.injections['injections'], 'Missing "error_signatures" in injections file'
		assert 'exploits' in app.injections['injections'], 'Missing "exploits" in injections file'
		assert 'delimiter' in app.injections['injections'], 'Missing "delimiter" in injections file'
	except Exception as e:
		print_error(e, traceback=False, use_cprint=True)
		return 1

	if (outfile := args.get_value('o')) is None:
		outfile = Vaccine.DEFAULT_OUTFILE
	outfile = datetime.datetime.now().strftime(outfile)

	try:
		os.makedirs(os.path.dirname(outfile), exist_ok=True)
		app.out_file = open(outfile, 'w')
	except Exception as e:
		print_error(e, traceback=False, use_cprint=True)
		return 1

	if (logfile := args.get_value('d')) is None:
		logfile = Vaccine.DEFAULT_LOGFILE
	logfile = datetime.datetime.now().strftime(logfile)

	try:
		os.makedirs(os.path.dirname(logfile), exist_ok=True)
		app.log_file = open(logfile, 'a')
	except Exception as e:
		print_error(e, traceback=False, use_cprint=True)
		return 1

	app.log_colored = args.get_value('c') is not None

	if (method := args.get_value('X')) is None:  # type: ignore
		method = 'GET'
	elif (method := method.upper()) not in ['GET', 'POST']:
		print_error(ArgError(f'HTTP Method not supported: "{method}"'), traceback=False, use_cprint=True)
		return 1
	app.method = method
	
	app.headers = {}
	if (_headers := args.get_value('H')) is None:
		app.headers = {
			'User-Agent': 'Vaccine/1.0 (https://github.com/Luzog78/42-Cybersecurity)',
			'Accept': '*/*',
		}
	else:
		h = ''
		i = 0
		while i < len(_headers):
			if _headers[i] == ';':
				name, value = h.split('=', 1) if '=' in h else (h, '')
				if (name := name.strip()):
					app.headers[name] = value
				h = ''
			elif _headers[i] == '\\':
				i += 1
				if i >= len(_headers) or _headers[i] == '\\':
					h += '\\'
				elif _headers[i] == ';':
					h += ';'
			else:
				h += _headers[i]
			i += 1
		name, value = h.split('=', 1) if '=' in h else (h, '')
		if (name := name.strip()):
			app.headers[name] = value

	app.verbose = args.get_value('v') is not None
