# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/15 13:17:06 by ysabik            #+#    #+#              #
#    Updated: 2026/01/17 14:22:06 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import time
from typing import Any
import requests
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urlparse, ParseResult, urljoin


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import Color


def error(*values: object,
		  color: str | None = Color.RED,
		  start: str | None = 'spider:',
		  sep: str | None = " ",
		  end: str | None = "\n"):
	messages: list[str] = []
	reset: str = Color.RESET
	if color is None:
		color, reset = '', ''
	if sep is None:
		sep = ''
	if start:
		messages.append(color + start + reset)
	for v in values:
		messages.append(color + str(v) + reset)
	if messages or end:
		print(sep.join(messages), end='' if end is None else end)
	return 1


HEADERS = {'User-Agent': 'Spider/1.0 (dummy@spider.org) Arachnida/1.00'}


class File:
	def __init__(self, url: str, path: str):
		self.url: str			= url
		self.path: str			= path
		self.downloaded: bool	= False

	def __repr__(self):
		return 'File(' \
			+ f"url='{self.url}', " \
			+ f"path='{self.path}', " \
			+ f"downloaded={self.downloaded}" \
			+ ')'

	def download(self) -> 'File':
		try:
			response = requests.get(self.url, headers=HEADERS)
			if response.status_code not in (200, 201, 302, 304):
				error(f'{self.url} returned status code {response.status_code}')
			try:
				os.makedirs('/'.join(self.path.split('/')[:-1]))
			except FileExistsError:
				pass
			with open(self.path, 'wb') as file:
				file.write(response.content)
			self.downloaded = True
		except Exception as e:
			error(f'[{e.__class__.__name__}]', e)
		return self


# ---------------------------------------------------------------------------- #
# ---------------------------------  Crawler  -------------------------------- #
# ---------------------------------------------------------------------------- #

class Spider:
	EXTENSIONS: set[str] = {
		'jpg', 'jpeg', 'png', 'gif', 'bmp'
	}

	@staticmethod
	def get_url_base(url: str | ParseResult) -> str | None:
		parsed: ParseResult = urlparse(url) if isinstance(url, str) else url
		if not parsed.netloc:
			return None
		return f'{parsed.scheme}://{parsed.netloc}/'

	@staticmethod
	def is_searched_file(uri: str | ParseResult) -> bool:
		if isinstance(uri, str):
			uri = urlparse(uri)
		uri = uri.path.lower()
		if uri.endswith('/'):
			uri = str(uri[:-1])
		for ext in Spider.EXTENSIONS:
			if uri.endswith(ext.lower()):
				return True
		return False

	def __init__(self):
		self.url: str | None		= None
		self.path: str				= './data/'
		self.is_recursive: bool		= False
		self.recursion_limit: int	= 5
		self.sleep: float			= 0.0

		self.url_base: str
		self.url_netloc: str

		self.urls: set[tuple[str, int]]	= set()
		self.visited: set[str]			= set()
		self.files: set[File]			= set()
		self.viewed: set[str]			= set()

	def __repr__(self):
		return 'Spider(' \
			+ f"url='{self.url}', " \
			+ f"path='{self.path}', " \
			+ f"is_recursive={self.is_recursive}, " \
			+ f"recursion_limit={self.recursion_limit}" \
			+ f"urls={self.urls}, " \
			+ f"visited={self.visited}, " \
			+ f"files={self.files}, " \
			+ f"viewed={self.viewed}" \
			+ ')'

	def __str__(self):
		s = f"§7§l§nSpider '§r§o§n{self.url}§7§l§n':§r\n"
		s += f"  §7Path:§r {self.path}\n"
		s += f"  §7Recursive:§r {'§aYes' if self.is_recursive else '§cNo'}§r\n"
		s += f"  §7Recursion limit:§r §9{self.recursion_limit}§r\n"
		s += f"\n"
		s += f"  §7Visited: §o(§b§o{len(self.visited)}§7§o)§r\n"
		i_len = len(str(len(self.visited) + 1))
		for i, v in enumerate(self.visited):
			s += f"    §7{i + 1:>{i_len}}.§r §o{v}§r\n"
		s += f"\n"
		s += f"  §7Files: §o(§b§o{len(self.files)}§7§o)§r\n"
		i_len = len(str(len(self.files) + 1))
		for i, f in enumerate(self.files):
			s += f"    §7{i + 1:>{i_len}}.§r §o{f.url}§r\n"
		return Color.c(s)

	def clean(self):
		try:
			files, dirs = [], []
			for root, ddirs, ffiles in os.walk(self.path):
				for f in ffiles:
					files.append(os.path.join(root, f))
				for d in ddirs:
					dirs.append(os.path.join(root, d))
			for f in files:
				try:
					os.remove(f)
				except Exception:
					pass
			for d in dirs[::-1]:
				try:
					os.rmdir(d)
				except Exception:
					pass
		except Exception:
			pass

	def normalize_url(self, url: str, current: str | None) -> tuple[str, bool]:
		if url.startswith('http://') or url.startswith('https://'):
			return url, Spider.get_url_base(url) == self.url_base
		if url.startswith('/') and not url.startswith('//'):
			return self.url_base + url[1:], True
		if current is None or not (parsed := urlparse(current)).scheme:
			return self.url_base + '/' + url, True
		if url.startswith('//'):
			return f'{parsed.scheme}:{url}', Spider.get_url_base(parsed) == self.url_base
		return urljoin(current, url), Spider.get_url_base(parsed) == self.url_base

	def crawl(self) -> int:
		assert self.url is not None, "URL is not set"
		url_base = Spider.get_url_base(self.url)
		if not url_base:
			error(f"Bad URL format. ('{self.url}')")
			return 1
		self.url_base = url_base
		self.url_netloc = urlparse(self.url).netloc

		self.urls = { (self.url, 0) }

		while self.urls:
			url, depth = self.urls.pop()
			self.visited.add(url)
			print(f"{Color.FAINT}Analysis of depth [ {Color.RESET}{Color.CYAN}{Color.BOLD}{depth}{Color.RESET}{Color.FAINT} ] - '{Color.RESET}{Color.ITALIC}{url}{Color.RESET}{Color.FAINT}'... {Color.RESET}")
			try:
				response = requests.get(url, headers=HEADERS)
				if response.status_code != 200:
					error(f'{url} returned status code {response.status_code}')
					continue
				soup = BeautifulSoup(response.text, 'html.parser')
				for file in soup.find_all(src=True):
					src = file.get('src')
					if src is None:
						continue
					src, _ = self.normalize_url(src, url)  # type: ignore
					parsed_src = urlparse(src)
					if Spider.is_searched_file(parsed_src):
						if src in self.viewed:
							continue

						path = parsed_src.netloc + parsed_src.path
						if parsed_src.query:
							path += '?' + parsed_src.query
						if parsed_src.fragment:
							path += '#' + parsed_src.fragment
						path = path.replace(f'{self.url_netloc}/', '').replace('/', '__')
						path = f'{self.path}/{self.url_netloc}/{path}'
						if (too_long := len(path) > 140):
							path = path[:137] + '...'
						if too_long or parsed_src.query or parsed_src.fragment:
							path += '.' + parsed_src.path.split('.')[-1]

						f = File(src, path)
						f.download()
						if self.sleep:
							time.sleep(self.sleep)
						self.files.add(f)
						self.viewed.add(src)

				if not self.is_recursive or depth >= self.recursion_limit >= 0:
					continue
				for link in soup.find_all(href=True):
					href = link.get('href')
					if href is None:
						continue
					href, same = self.normalize_url(href, url)  # type: ignore
					if same and href not in self.visited:
						self.urls.add((href, depth + 1))
			except Exception as e:
				error(f'[{e.__class__.__name__}]', e)
		return 0


# ---------------------------------------------------------------------------- #
# ---------------------------------  Parsing  -------------------------------- #
# ---------------------------------------------------------------------------- #

def parsing() -> Spider | int:
	spider = Spider()
	clean = False


	def limit_parsing_error(l: Any) -> int:
		error("'-l' attribute must be followed by a number (<0 for no limit)")
		if l is not None:
			return error(f"'{l}' isn't a number")
		return 1


	def syntax_error(code: int = 1, color: str | None = Color.RED) -> int:
		error('Spider is a web crawler. It takes a URL and crawls it for links and files.', color=color)
		error('Its goal is to find and download certain files (.jpg, .jpeg, .png, .gif and .bmp).', color=color)
		error(color=color)
		error('Syntax:', color=color)
		error(f'{sys.argv[0]} [flags...] <URL>', color=color)
		error(color=color)
		error('Flags:', color=color)
		error('  -r               recursively downloads the files', color=color)
		error('  -l <limit>       recursion limit (default: 5)', color=color)
		error('  -p <save_path>   path to save files (default: "./data/")', color=color)
		error('  -c               clear files in "save_path" before crawling', color=color)
		error('  -s <sleep_time>  time (in sec) to wait between requests (default: 0)', color=color)
		error('  -h, --help       display this help message', color=color)
		return code


	i = 1
	while i < len(sys.argv):
		if sys.argv[i].startswith('-') and sys.argv[i] != '--':
			for c in sys.argv[i][1:]:
				if c == 'r':
					spider.is_recursive = True
				elif c == 'l':
					if i + 1 < len(sys.argv):
						i += 1
						try:
							spider.recursion_limit = int(sys.argv[i])
						except ValueError:
							return limit_parsing_error(sys.argv[i])
					else:
						return limit_parsing_error(None)
				elif c == 'p':
					if i + 1 < len(sys.argv):
						i += 1
						spider.path = sys.argv[i]
					else:
						return error("'-p' attribute must be followed by a path")
				elif c == 'c':
					clean = True
				elif c == 's':
					if i + 1 < len(sys.argv):
						i += 1
						try:
							spider.sleep = float(sys.argv[i])
						except ValueError:
							return error(f"'{sys.argv[i]}' isn't a number")
					else:
						return error("'-s' attribute must be followed by a number")
				elif c == 'h':
					return syntax_error(code=0, color=Color.CYAN)
				else:
					return syntax_error()
		elif sys.argv[i] == '--help':
			return syntax_error(code=0, color=Color.CYAN)
		elif spider.url is None:
			spider.url = sys.argv[i]
		else:
			return error('Multiple URLs')
		i += 1

	if clean:
		spider.clean()

	if spider.url is None:
		if clean:
			return 0
		return error('No URL specified')

	return spider


if __name__ == '__main__':
	spider: Spider | int = parsing()

	if isinstance(spider, int):
		sys.exit(spider)

	assert isinstance(spider, Spider)
	result = 0
	try:
		result = spider.crawl()
	except KeyboardInterrupt:
		error('>>> Stopped by user <<<', start='\r  \r', color=Color.YELLOW)
	except Exception as e:
		if e.__class__.__name__ == ConnectionError.__name__:
			error('>>> Cannot access to server <<<', start='\r  \r')
		else:
			error(f'[{e.__class__.__name__}]', e)
			print(Color.RED + Color.FAINT, end='')
			traceback.print_exc()
			print(Color.RESET)
	if not result:
		print()
		print(spider)
