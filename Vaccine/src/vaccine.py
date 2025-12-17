# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    vaccine.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/02 09:16:15 by ysabik            #+#    #+#              #
#    Updated: 2025/12/17 04:32:18 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import html
import datetime
import requests
from bs4 import Tag
from io import TextIOWrapper
from typing import Self, Any, TypeVar
from urllib.parse import urljoin


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from cyberlib import cprint, Color, cstrip


def format_datetime(
		dt: datetime.datetime | None,
		start: datetime.datetime | None = None,
		) -> str | float | None:
	if dt is None:
		return None
	if start is None:
		return dt.isoformat()
	return (dt - start).total_seconds()


T = TypeVar('T')


class VaccineError(Exception):
	pass


class InputField:
	def __init__(self, obj: Tag) -> None:
		self.name = str(obj.get('name', ''))
		self.type = str(obj.get('type', 'text'))
		self.value = str(obj.get('value', ''))
		self.required = obj.has_attr('required')
		self.obj = obj

	def __repr__(self) -> str:
		return 'InputField(' \
			+ f'name={repr(self.name)}, ' \
			+ f'type={repr(self.type)}, ' \
			+ f'value={repr(self.value)}, ' \
			+ f'required={self.required})'


class Form:
	def __init__(self, obj: Tag, inputs: list[InputField] = [], url: str = '') -> None:
		self.action = str(obj.get('action', ''))
		self.method = str(obj.get('method', 'POST')).upper()

		pathname = str(obj.get('action', url))
		self.action_url = urljoin(url, pathname)

		self.inputs: list[InputField] = [
			input
			for input in inputs
			if input.name != '' and input.type.lower() not in ['submit', 'button', 'reset']
		]
		self.vulnerabilities: list[tuple[InputField, str, str | None]] = []
	
	def get_inputs_dict(self) -> dict[str, str]:
		return {
			input.name: input.value
			for input in self.inputs
		}

	def __repr__(self) -> str:
		return 'Form(' \
			+ f'action={repr(self.action)}, ' \
			+ f'method={repr(self.method)}, ' \
			+ f'inputs={repr(self.inputs)})'


class Table:
	def __init__(self, name: str) -> None:
		self.name = name
		self.columns: list[str] = []
		self.rows: list[list[Any]] = []

	def dump(self) -> dict[str, Any]:
		return {
			'name': self.name,
			'columns': self.columns,
			'rows': self.rows,
		}


class Database:
	def __init__(self, name: str) -> None:
		self.name = name
		self.current: bool = False
		self.tables: list[Table] = []

	def get_table(self, name: str, default: T = None) -> Table | T:
		for table in self.tables:
			if table.name == name:
				return table
		return default

	def dump(self) -> dict[str, Any]:
		return {
			'name': self.name,
			'current': self.current,
			'tables': [table.dump() for table in self.tables],
		}


class DBServer:
	def __init__(self) -> None:
		self.kind: str | None = None
		self.version: str | None = None
		self.user: str | None = None
		self.dbs: list[Database] = []

	def get_db(self, name: str, default: T = None) -> Database | T:
		for db in self.dbs:
			if db.name == name:
				return db
		return default

	def dump(self) -> dict[str, Any]:
		return {
			'kind': self.kind,
			'version': self.version,
			'user': self.user,
			'dbs': [db.dump() for db in self.dbs],
		}


class Vaccine:
	DEFAULT_OUTFILE = './out/out_%Y-%m-%d_%H-%M-%S_%f.json'
	DEFAULT_LOGFILE = './logs/log_%Y-%m-%d.log'
	DEFAULT_INJECTIONS_FILE = './payloads/injections-1.0.json'
	_instance: Self | None = None

	@classmethod
	def instance(cls) -> Self:
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self,
			out_file: TextIOWrapper | None = None,
			log_file: TextIOWrapper | None = None,
			log_colored: bool = False,
			url: str = '',
			method: str = '',
			headers: dict[str, str] = {},
			injections: dict[str, Any] = {},
			injections_mode: str = 'all',
			verbose: bool = False,
			) -> None:
		self.out_file = out_file
		self.log_file = log_file
		self.log_colored = log_colored
		self.url = url
		self.method = method
		self.headers = headers
		self.injections = injections
		self.injections_mode = injections_mode
		self.verbose = verbose

		self.forms: list[Form] = []
		self.server: DBServer = DBServer()
		self.request_count: int = 0

		self.start_time: datetime.datetime | None = None
		self.analysis_time: datetime.datetime | None = None
		self.exploitation_time: datetime.datetime | None = None

	def __repr__(self) -> str:
		return 'Vaccine(' \
			+ f'url={repr(self.url)}, ' \
			+ f'method={repr(self.method)}, ' \
			+ f'headers={repr(self.headers)}, ' \
			+ f'injections={self.injections.get('version')}, ' \
			+ f'forms={repr(self.forms)})'

	def dump_results(self) -> dict[str, Any]:
		def get_inputs(form: Form) -> list[dict[str, Any]]:
			inputs = {
				input.name: {
					'name': input.name,
					'type': input.type,
					'value': input.value,
					'required': input.required,
				} for input in form.inputs
			}
			for input, signature, db_name in form.vulnerabilities:
				if input.name in inputs:
					if 'signatures' not in inputs[input.name]:
						vulns = []
						inputs[input.name]['vulnerabilities'] = vulns
					else:
						vulns = inputs[input.name]['vulnerabilities']
					vulns.append({
						'signature': signature,
						'database': db_name,
					})
			return list(inputs.values())

		return {
			'start_time': format_datetime(self.start_time),
			'analysis_time': format_datetime(self.analysis_time, self.start_time),
			'exploitation_time': format_datetime(self.exploitation_time, self.analysis_time),
			'total_requests': self.request_count,
			'presets': {
				'url': self.url,
				'method': self.method,
				'headers': self.headers,
				'injections_version': self.injections.get('version'),
			},
			'forms': [
				{
					'vulnerable': len(form.vulnerabilities) > 0,
					'action_url': form.action_url,
					'method': form.method,
					'inputs': get_inputs(form),
				}
				for form in self.forms
			],
			'server': self.server.dump(),
		}


def print(
		*values: object,
		sep: str = ' ',
		end: str = '\n',
		prefix: bool = True,
		reset: bool = True,
		char: str = Color.DEFAULT_MAGIC_CHAR,
		) -> None:
	if prefix:
		t = f'§f[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]§r'
		s = f'§7[§eVaccine§7]§r'
		values = (t, s, *values)
	cprint(*values, sep=sep, end=end, reset=reset, char=char)
	if Vaccine.instance().log_file is not None:
		cprint(*values, sep=sep, end=end, reset=reset, char=char,
				strip=not Vaccine.instance().log_colored,
				file=Vaccine.instance().log_file, flush=True)


def custom_traceback(
		e: BaseException,
		traceback: bool = True,
		colored: bool = True,
		) -> list[str]:
	lines = [ f'§c§l[{e.__class__.__name__}]§c {e}' ]
	tb = e.__traceback__
	last = None
	while tb is not None:
		last = f'at {tb.tb_frame.f_code.co_name} ({os.path.relpath(tb.tb_frame.f_code.co_filename)}:{tb.tb_lineno})'
		if traceback:
			lines.append(f'§c§l[{e.__class__.__name__}]§c§o     {last}')
		tb = tb.tb_next
	if not traceback and last is not None:
		lines[0] += f'  [{last}]'
	if e.__cause__ is not None:
		for line in custom_traceback(e.__cause__, traceback=traceback, colored=colored):
			lines.append(f'§c§l[{e.__class__.__name__}]§c {line}')
	if not colored:
		for i in range(len(lines)):
			lines[i] = cstrip(lines[i])
	return lines


def print_error(
		e: BaseException,
		traceback: bool = True,
		colored: bool = True,
		use_cprint: bool = False,
		) -> None:
	p = cprint if use_cprint else print
	for line in custom_traceback(e, traceback=traceback, colored=colored):
		p(line, reset=True, char='§')


def request(
		method: str,
		url: str,
		headers: dict[str, str] = {},
		data: dict[str, Any] = {},
		timeout: int = 10,
		raise_for_status: bool = False,
		) -> requests.Response:
	try:
		if method.lower() in ['get', 'head', 'delete', 'options', 'trace']:
			response = requests.request(
				method=method,
				url=url,
				headers=headers,
				params=data,
				timeout=timeout,
			)
		else:
			response = requests.request(
				method=method,
				url=url,
				headers=headers,
				data=data,
				timeout=timeout,
			)
		if Vaccine._instance:
			Vaccine._instance.request_count += 1
		if raise_for_status:
			response.raise_for_status()
		return response
	except Exception as e:
		raise VaccineError(f'HTTP request failed: {repr(method + " " + url)}') from e
	

def extract_data(
		text: str,
		delimiter: str,
		data: str = '',
		unescape: bool = True,
		) -> tuple[list[str], bool]:
	if unescape:
		data = html.unescape(data)
		text = html.unescape(text)
	splitted = text.split(delimiter)
	length = len(splitted)
	if length >= 3:
		splitted = splitted[1:]
		list_data = []
		while length >= 2:
			if splitted[0] != data:
				list_data.append(splitted[0])
			splitted = splitted[2:]
			length = len(splitted)
		return list_data, not not list_data
	return [], False


def extract_unique_data(
		text: str,
		delimiter: str,
		data: str = '',
		unescape: bool = True,
		) -> str | None:
	if unescape:
		data = html.unescape(data)
		text = html.unescape(text)
	splitted = text.split(delimiter)
	if len(splitted) >= 3:
		splitted = splitted[1:]
		while len(splitted) >= 2:
			if splitted[0] != data:
				return splitted[0]
			splitted = splitted[2:]
	return None
