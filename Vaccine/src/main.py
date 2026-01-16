# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/28 10:17:18 by luzog78           #+#    #+#              #
#    Updated: 2025/12/21 15:59:32 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import json
from datetime import datetime

from vaccine import Vaccine, format_datetime, print, print_error
from parser import parse
from analysis import analyze
from exploitation import exploit


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from cyberlib import cescape, ArgParser


def start(app: Vaccine):
	print('§7####################################################')
	print('§7##§r                                                §7##')
	print('§7##§r                    §e§l§nVaccine§r                     §7##')
	print('§7##§r                                                §7##')
	print('§7####################################################')
	print()
	print(f'§7Method: ........§r {app.method}')
	print(f'§7Headers (§r{len(app.headers):>2}§7): ..§r {"§4None" if len(app.headers) == 0 else ""}', end='\n' if len(app.headers) == 0 else '')
	for i, (name, value) in enumerate(app.headers.items()):
		s = f'§7 - [§r{cescape(name)}§7: §r{cescape(value)}§7]'
		if i == 0:
			print(s, prefix=False)
		else:
			print(f'                 {s}')
	print(f'§7URL: ...........§r §9§l§n{cescape(app.url)}')
	print(f'§7Out file: ......§r {cescape(app.out_file.name) if app.out_file is not None else "§4None"}')
	print(f'§7Log file: ......§r {cescape(app.log_file.name) if app.log_file is not None else "§4None"}')
	print(f'§7Verbose: .......§r {"§aEnabled" if app.verbose else "§4Disabled"}')
	print()
	print()

	app.start_time = datetime.now()
	analyze(app)
	app.analysis_time = datetime.now()
	exploit(app)
	app.exploitation_time = datetime.now()


def stop(app: Vaccine):
	print()
	print('~~~ Dumping results and cleaning up ~~~')
	print()
	if app.out_file is not None:
		json.dump(app.dump_results(), app.out_file, indent='\t')
	print(f'Start: {format_datetime(app.start_time)}'
		+ f'  |  Analysis: {format_datetime(app.analysis_time, app.start_time)}s'
		+ f'  |  Exploitation: {format_datetime(app.exploitation_time, app.analysis_time)}s'
		+ f'  |  Requests: {app.request_count}')
		
	
	print()
	print(f'§7~~~~~~~~~~~~~~~~~~§r §e§oEnd of Vaccine §7~~~~~~~~~~~~~~~~~~')
	print()
	print()

	if app.log_file is not None:
		app.log_file.close()
	if app.out_file is not None:
		app.out_file.close()


if __name__ == '__main__':
	ap = ArgParser(sys.argv[1:]) \
			.add_pre_desc('42-Cybersecurity - Vaccine | SQL Injector') \
			.add_pre_desc() \
			.add_pre_desc('Auto SQL Injector supporting:') \
			.add_pre_desc('  - Servers: MySQL, MariaDB, PostgreSQL, SQLite;') \
			.add_pre_desc('  - Injections: Stacked, Union, Blind, Boolean;') \
			.add_pre_desc('  - Auto-adapt limit: Yes') \
			.add_pre_desc() \
			.add_pre_desc('Given an url, it will search for every form and try to send') \
			.add_pre_desc(' suspicious payloads to find the injectable fields.') \
			.add_pre_desc('Once the fields discovered, try to exploit them using the') \
			.add_pre_desc(' configured injection.json file.') \
			.add_pre_desc() \
			.add_pre_desc('NOTE: Some server can be more "tricky" to inject. For these') \
			.add_pre_desc(' servers, you need to edit (use a custom) injection.json file.') \
			.add_pre_desc() \
			.add_pre_desc('Usage: ./vaccine [FLAGS] <URL>') \
			.add_flag('o', 'out', ['file'], f'Dump the data in an output file (\'w\' mode). Default: {Vaccine.DEFAULT_OUTFILE}') \
			.add_flag('d', 'logfile', ['file'], f'Dump the logs in a log file (\'a\' mode). Default: {Vaccine.DEFAULT_LOGFILE}') \
			.add_flag('c', 'colored', None, 'Enable ANSI colored output in the log file.') \
			.add_flag('X', 'method', ['method'], 'HTTP Method (either GET or POST). Default: GET') \
			.add_flag('H', 'headers', ['name=value[;...]'], 'HTTP Headers') \
			.add_flag('i', 'injections', ['file'], f'List of injection payloads to use. Default: {Vaccine.DEFAULT_INJECTIONS_FILE}') \
			.add_flag('m', 'mode', ['mode'], 'Injection type (stacked, union, blind-bool or all). Default: all') \
			.add_flag('v', 'verbose', None, 'Enable logging of sent payloads') \
			.add_flag('h', 'help', None, 'Print this help message') \
			.add_post_desc() \
			.add_post_desc('Example:') \
			.add_post_desc('  ./vaccine http://localhost:3000/login') \
			.add_post_desc('  ./vaccine http://testphp.vulnweb.com/search.php -v -m union -i injection-x.x.json -H \'User-Agent=Vaccine;Accept=*/*\'') \
			.add_post_desc() \
			.add_post_desc('Credits: ysabik (https://github.com/Luzog78)')

	app = Vaccine.instance()

	try:
		if (code := parse(app, ap)) is not None:
			sys.exit(code)

		start(app)
	except (Exception, KeyboardInterrupt) as e:
		print_error(e)
		stop(app)
		sys.exit(1)

	stop(app)
