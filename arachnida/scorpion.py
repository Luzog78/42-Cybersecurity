# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/15 13:13:49 by ysabik            #+#    #+#              #
#    Updated: 2026/01/17 14:17:56 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from math import e
import os
import sys
import ast
from typing import Any
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import cprint as print


def ask_for_num(prompt: str, min_: int, max_: int, /, ln: bool = True) -> int:
	while True:
		try:
			print(prompt, end="")
			num = input()
			if num == 'q':
				raise KeyboardInterrupt(0xe51e2b)
			if num.startswith('0x'):
				num = int(num[2:], 16)
			elif num.startswith('0b'):
				num = int(num[2:], 2)
			else:
				num = int(num)
			if min_ <= num <= max_:
				return num
		except ValueError:
			pass
		print("§4§lInvalid choice")
		if ln:
			print()


class Tag:
	def __init__(self, id: int, name: str, value: Any, *, parent: int | None = None) -> None:
		self.id: int	= id
		self.name: str	= name
		self.value: Any	= value
		self.parent: int | None = parent


class Scorpion:
	def __init__(self, files: list[str]) -> None:
		self.imgs: dict[str, Image.Image]			= {}
		self.errors: list[tuple[str, str]]	= []

		for file in files:
			try:
				self.imgs[file] = Image.open(file)
			except Exception as e:
				self.errors.append((file, f"[{e.__class__.__name__}] {e}"))

		self.current_name: str					= ''
		self.current_image: Image.Image | None	= None
		self.current_exif: Image.Exif | None	= None
		self.current_tags: list[Tag]			= []

	@staticmethod
	def from_argv() -> 'Scorpion':
		for arg in sys.argv[1:]:
			if arg.lower() in ('-h', '--help'):
				def p(*args):
					print('§6§lscorpion:§e', *args, end='§r\n')

				p('Scorpion is an EXIF metadata editor. It takes image files and')
				p(' allows you to view and edit their EXIF metadata.')
				p()
				p('Syntax:')
				p(f'{sys.argv[0]} [flags...] <image> [<images>...]')
				p()
				p('Flags:')
				p('  -h, --help       display this help message')
				sys.exit(0)
		return Scorpion(sys.argv[1:])

	@staticmethod
	def print_header() -> None:
		print("§6§l################################################")
		print("§6§l#                                              #")
		print("§6§l#                   §e§nScorpion§6                   #")
		print("§6§l#                                              #")
		print("§6§l################################################")
		print("\n")

	@staticmethod
	def print_list(metadata_list: list[str]) -> None:
		i_len = len(str(len(metadata_list) + 1))
		for i, metadata in enumerate(metadata_list):
			print(f"§7{i + 1:>{i_len}}.§r {metadata}")

	@staticmethod
	def print_preview(metadata: list[Tag]) -> None:
		i_len = len(str(len(metadata) + 1))
		k_len = 22 - i_len // 2
		v_len = 44 - k_len
		for i, tag in enumerate(metadata):
			key, val = tag.name, tag.value
			try:
				if len(key) > k_len:
					key = key[:k_len - 2] + "§7§o..§r"
				val = str(val)
				if len(val) > v_len:
					val = val[:v_len - 2] + "§7§o..§r"
				print(f"§7{i + 1:>{i_len}}.§r {key:>{k_len}} §7{'(' + str(tag.id) + ')':>7}:§r {val:>{v_len}}")
			except Exception as e:
				print(f"§7{i + 1:>{i_len}}.§r {key:>{k_len}.{k_len}} §7{'(' + str(tag.id) + ')':>7}:§r §c§o{e}")

	@staticmethod
	def print_metadata(id: int, name: str, value: Any = None, *, parent: int | None = None) -> None:
		print(f"§7       ID:: §e{id}" + (f"§7 (IFD: §e{parent}§7)" if parent is not None else ""))
		print(f"§7     Name:: §e{name}")
		print(f"§7     Type:: §r{type(value).__name__}")
		if isinstance(value, bytes):
			print(f"§7      Hex:: §r{value.hex()}")
			print(f"§7  Decoded:: '§r{value.decode('utf-8', errors='replace')}§7'")
		try:
			print(f"§7    Length:: §r{len(value)}")
		except Exception as e:
			pass
		try:
			print(f"§7  __str__:: '§r{str(value)}§7'")
		except Exception as e:
			pass
		try:
			print(f"§7 __repr__:: '§r{repr(value)}§7'")
		except Exception as e:
			pass

	def print_imgs(self) -> None:
		if len(self.imgs) > 0 or len(self.errors) > 0:
			print("§6§l%-25s  §4§l%25s" % (f"Loaded Images: §e{len(self.imgs)}", f"Loading Erors: §c{len(self.errors)}"))
			print()
		if len(self.imgs) == 0:
			if len(self.errors) > 0:
				print()
			print("§e§lNo images loaded !")
			print()
			return
		i_len = len(str(len(self.imgs) + 1))
		for i, (name, img) in enumerate(self.imgs.items()):
			print(f"§7{i + 1:>{i_len}}.§r {name}")

	def print_errors(self) -> None:
		if len(self.errors) == 0:
			print("§c§lNo errors found !")
			return
		for name, error in self.errors:
			print(f"§7-§r {name} §c§o{error}")

	def save_img(self) -> None:
		if self.current_image is None or self.current_exif is None:
			return

		if self.current_image.format in ['JPEG', 'JPG']:
			self.current_image.save(self.current_name, exif=self.current_exif)
		elif self.current_image.format == 'PNG':
			# PNG stores EXIF differently
			pnginfo = self.current_image.info.copy()
			self.current_image.save(self.current_name, pnginfo=pnginfo)
		else:
			# For other formats, try to preserve EXIF if supported
			try:
				self.current_image.save(self.current_name, exif=self.current_exif)
			except:
				# Fallback: save without EXIF
				self.current_image.save(self.current_name)
				print(f"Warning: EXIF may not be preserved for {self.current_image.format} format")

		print(f"§a§lFile §r{self.current_name}§a§l saved!")

	def load_metadata(self) -> None:
		if self.current_exif is None:
			raise ValueError("No EXIF data to load")

		def add_tag(tag_id: int, tag: str, value: Any, *, parent: int | None = None) -> None:
			try:
				# Handle GPS data specially
				if tag == "GPSInfo":
					gps_dict = {}
					for gps_tag_id, gps_value in value.items():
						gps_tag_name = GPSTAGS.get(gps_tag_id, f"GPS_Unknown_{gps_tag_id}")
						gps_dict[gps_tag_name] = gps_value
					value = gps_dict

				# Handle bytes
				elif isinstance(value, bytes):
					try:
						value = value.decode('utf-8')
					except UnicodeDecodeError:
						pass
			except Exception as e:
				print(f"Warning: Could not process {tag}: [{e.__class__.__name__}] {e}")

			self.current_tags.append(Tag(tag_id, tag, value, parent=parent))


		self.current_tags = []
		for tag_id, value in self.current_exif.items():
			add_tag(tag_id, TAGS.get(tag_id, f"Unknown_{tag_id}"), value)
		
		# Get ExifOffset IFD - the main Exif sub-IFD (data like camera settings, etc.)
		ifd_data = self.current_exif.get_ifd(0x8769)
		if ifd_data:
			for tag_id, value in ifd_data.items():
				add_tag(tag_id, TAGS.get(tag_id, f"Exif_Unknown_{tag_id}"), value, parent=0x8769)
		
		# Get GPS IFD
		try:
			gps_ifd = self.current_exif.get_ifd(0x8825)
			if gps_ifd:
				for gps_tag_id, gps_value in gps_ifd.items():
					add_tag(gps_tag_id, GPSTAGS.get(gps_tag_id, f"GPS_Unknown_{gps_tag_id}"), gps_value, parent=0x8825)
		except KeyError:
			pass

		# Get Interoperability IFD
		try:
			interop_ifd = self.current_exif.get_ifd(0xA005)
			if interop_ifd:
				for tag_id, value in interop_ifd.items():
					add_tag(tag_id, TAGS.get(tag_id, f"Interop_Unknown_{tag_id}"), value, parent=0xA005)
		except KeyError:
			pass

	def delete_metadata(self, tag: Tag) -> None:
		if self.current_exif is None:
			return

		del self.current_exif[tag.id]
		self.current_tags.remove(tag)
		print(f"§a§lMetadata §e{tag.name}§a§l deleted!")

	def set_metadata(self, tag: Tag) -> None:
		if self.current_exif is None:
			return

		print("§e§lSetting the value for §n§e" + tag.name)
		print()
		while True:
			print("§7§oValue : ", end="")
			value = input()
			try:
				value = ast.literal_eval(value)
			except Exception:
				pass
			print()
			self.print_metadata(tag.id, tag.name, value, parent=tag.parent)
			print("§7§oIs this correct ? (Y/n) : ", end="")
			choice = input()
			print()
			if choice.lower() == 'y':
				if tag.parent is not None:
					try:
						ifd = self.current_exif.get_ifd(tag.parent)
						if ifd is None:
							ifd = {}
							self.current_exif[tag.parent] = ifd
						ifd[tag.id] = value
					except Exception as e:
						print(f"§4§lError setting value in IFD {tag.parent}: [{e.__class__.__name__}] {e}§r §7§o(Please stop messing around :p)")
				else:
					self.current_exif[tag.id] = value
				tag.value = value
				break

	def see_img(self) -> None:
		if self.current_exif is None:
			return

		print(f"§e[ §l§n{self.current_name}§e ]")
		print()
		if not self.current_tags:
			print("§cThis image has no exif data.")
			print("§7§oPress enter to go back", end="")
			input()
			print()
			self.current_exif = None
			return
		print(f"§6This image has §e{len(self.current_tags)}§6 attributes.")

		while self.current_exif is not None:
			print()
			print("§7§o(P)review (L)ist   (G)et (S)ave")
			print("§7§o(E)dit    (D)elete (N)ew (Q)uit : ", end="")
			choice = input()
			if choice.lower() == 'p':
				print()
				self.print_preview(self.current_tags)
			elif choice.lower() == 'l':
				print()
				self.print_list([tag.name for tag in self.current_tags])
			elif choice.lower() == 'g':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_tags), ln=False)
				tag = self.current_tags[idx - 1]
				print()
				self.print_metadata(tag.id, tag.name, tag.value, parent=tag.parent)
			elif choice.lower() == 's':
				print()
				self.save_img()
			elif choice.lower() == 'e':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_tags), ln=False)
				tag = self.current_tags[idx - 1]
				print()
				self.set_metadata(tag)
			elif choice.lower() == 'd':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_tags), ln=False)
				tag = self.current_tags[idx - 1]
				print()
				self.delete_metadata(tag)
			elif choice.lower() == 'n':
				k = ''
				while not k:
					print("§7§oNew key : ", end="")
					k = input()
				for tid, tname in TAGS.items():
					if tname == k:
						break
				else:
					print("§7§oKey not recognized.", end="")
					tid = ask_for_num("§7§oEnter a custom ID (int): ", 1, 65535, ln=False)
				p = ask_for_num("§7§oParent IFD (0 for none): ", 0, 65535, ln=False)
				print()
				tag = Tag(tid, k, None, parent=(p if p != 0 else None))
				self.current_tags.append(tag)
				self.set_metadata(tag)
			elif choice.lower() == 'q':
				self.current_exif = None
				print()
			else:
				print("§4§lInvalid choice")

	def run(self) -> None:
		self.print_header()
		self.print_imgs()
		try:
			if len(self.imgs) == 0 and len(self.errors) == 0:
				print("\n§7§oPress enter to exit", end="")
				input()
				raise KeyboardInterrupt(0xe51e2b)
			while True:
				print()
				choice = ask_for_num("§7§oChoose an image (0: errors, Q: quit) : ", 0, len(self.imgs))
				if choice == 0:
					self.print_errors()
				else:
					self.current_name, self.current_image = tuple(list(self.imgs.items())[choice - 1])  # type: ignore
					assert self.current_image is not None
					self.current_exif = self.current_image.getexif()
					print(choice, self.current_name, self.current_image, self.current_exif)
					self.load_metadata()
					print()
					print()
					self.see_img()
					self.print_imgs()
		except KeyboardInterrupt as e:
			if 0xe51e2b not in e.args:
				print()
		print("§6§oGoodbye!")


Scorpion.from_argv().run()
