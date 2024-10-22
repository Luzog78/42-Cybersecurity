# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 14:21:46 by ysabik            #+#    #+#              #
#    Updated: 2024/10/22 13:57:32 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import io
import sys
import hmac
import qrcode
import base64
import easygui
from time import time
from hashlib import sha1


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import cprint, ArgParser, ArgError


print = cprint


def hmac_sha1(key: bytes, msg: bytes) -> bytes:
	return hmac.new(key, msg, sha1).digest()


def hotp(key: bytes, counter: int) -> int:
	hs = hmac_sha1(key, counter.to_bytes(8, 'big'))

	offset = hs[-1] & 0xf
	bin_code = (hs[offset] & 0x7f) << 24 \
				| hs[offset + 1] << 16 \
				| hs[offset + 2] << 8 \
				| hs[offset + 3]
	
	return bin_code % 10 ** 6


def totp(key: bytes, period: int) -> int:
	return hotp(key, int(time() / period))


def generate_key(filename: str, length: int = 256, verbose: bool = False) -> bytes:
	try:
		key = os.urandom(length)
		with open(filename, 'w') as f:
			f.write(key.hex() + '\n')
		if verbose:
			print(f'§aKey generated and saved in {filename}')
		return key
	except Exception as e:
		if verbose:
			print(f'§c[{e.__class__.__name__}] §4{e}')
		return b''


def create_qrcode_ascii(key: bytes) -> str:
	try:
		secret = base64.b32encode(key)
		url = f'otpauth://totp/42-Cybersecurity?secret={str(secret)[2:-1]}&issuer=42-Cybersecurity&digits=6'
		qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L)
		qr.add_data(url)
		f = io.StringIO()
		qr.print_ascii(out=f)
		f.seek(0)
		return f.read()
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}')


def create_qrcode(key: bytes):
	try:
		secret = base64.b32encode(key)
		url = f'otpauth://totp/42-Cybersecurity?secret={str(secret)[2:-1]}&issuer=42-Cybersecurity&digits=6'
		qrcode.make(url, error_correction=qrcode.ERROR_CORRECT_L).save('__qrcode__.png')
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}')


def get_secret(filename: str, verbose: bool = False) -> bytes | None:
	try:
		with open(filename, 'r') as f:
			key = f.read().strip()
		if key.startswith('0x'):
			key = key[2:]
		key = bytes.fromhex(key)
		if len(key) < 64:
			raise ValueError('Key must be at least 64 hexa chars')
		return key
	except Exception as e:
		if verbose:
			print(f'§c[{e.__class__.__name__}] §4{e}')
		return None


def get_code(filename: str, period: int = 30, verbose: bool = False) -> int:
	try:
		key = get_secret(filename, verbose=verbose)
		if key is None:
			return 0
		return totp(key, period)
	except Exception as e:
		if verbose:
			print(f'§c[{e.__class__.__name__}] §4{e}')
		return 0


def open_gui(verbose: bool = False):
	while True:
		try:
			choice = easygui.buttonbox('Choose an action', '42-Cybersecurity - ft_otp', ['Generate key', 'Use key', 'Quit'])
			if choice == 'Generate key':
				g_file = easygui.filesavebox('Choose where to save the key', '42-Cybersecurity - ft_otp', 'key.key')
				if g_file:
					create_qrcode(generate_key(g_file, verbose=verbose))
					easygui.msgbox(f'Key generated and saved in {g_file}', '42-Cybersecurity - ft_otp', image='__qrcode__.png')
				continue
			elif choice == 'Use key':
				k_file = easygui.fileopenbox('Choose the key to use', '42-Cybersecurity - ft_otp', 'key.key')
				if k_file:
					code = get_code(k_file, verbose=verbose)
					easygui.msgbox(f'The code is {code:0>6}', '42-Cybersecurity - ft_otp')
				continue
		except Exception as e:
			if verbose:
				print(f'§c[{e.__class__.__name__}] §4{e}')
		break


if __name__ == '__main__':
	ap = ArgParser(sys.argv[1:]) \
			.add_pre_desc('42-Cybersecurity - ft_otp | TOTP generator') \
			.add_pre_desc('> (RFC 6238)[https://tools.ietf.org/html/rfc6238]') \
			.add_pre_desc('> (RFC 4226)[https://tools.ietf.org/html/rfc4226]') \
			.add_pre_desc() \
			.add_pre_desc('Usage: ./ft_otp [FLAGS]') \
			.add_flag('g', 'generate', ['file.key'], 'Generate a new key, and save it in <file.key>') \
			.add_flag('G', 'generate-qr', ['file.key'], 'Generate a new key, save it in <file.key>, and show it in the console') \
			.add_flag('k', 'key', ['file.key'], 'Takes the key in <file.key> (minimum 64 hexa chars) and give the TOTP') \
			.add_flag('s', 'time-step', ['seconds'], 'Set the time step to <seconds> (default 30)') \
			.add_flag(None, 'qr', ['file.key'], 'Show the qrcode of the secret file') \
			.add_flag(None, 'gui', None, 'Use GUI instead of terminal') \
			.add_flag('v', 'verbose', None, 'Print always in terminal (with GUI)') \
			.add_flag('h', 'help', None, 'Print this help message') \
			.add_post_desc('Credits: ysabik (https://github.com/Luzog78)')

	try:
		ap.parse()
	except ArgError as e:
		print(f'§c[{e.__class__.__name__}] §4{e}')
		exit(1)

	if ap.get_value('h'):
		print(ap)
		exit(0)

	verbose = ap.get_value('v', False)
	time_step = ap.get_value('s', 30)

	g_file = ap.get_value('g')
	if g_file:
		key = generate_key(g_file, verbose=True)
		if verbose and key is not None:
			print(key.hex(), reset=False)

	G_file = ap.get_value('G')
	if G_file:
		key = generate_key(G_file, verbose=verbose)
		if verbose and key is not None:
			print(key.hex(), reset=False)
		if key is not None:
			print(create_qrcode_ascii(key))
	
	k_file = ap.get_value('k')
	if k_file:
		code = get_code(k_file, time_step, verbose=True)
		print(f'{code:0>6}')

	qr_flag = ap.get_value('qr')
	if qr_flag:
		key = get_secret(qr_flag, verbose=True)
		if verbose and key is not None:
			print(key.hex(), reset=False)
		if key is not None:
			print(create_qrcode_ascii(key))
	
	gui_flag = ap.get_value('gui')
	if gui_flag:
		open_gui(verbose)
	
	if not (g_file or G_file or k_file or qr_flag or gui_flag):
		print('§cNo arguments given\nTry ./ft_otp --help for help')
		exit(1)
