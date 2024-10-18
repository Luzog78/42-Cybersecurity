# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/15 13:13:49 by ysabik            #+#    #+#              #
#    Updated: 2024/10/18 19:18:23 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import ast
from exif import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cyberlib import cprint as print


def ask_for_num(prompt: str, min_: int, max_: int, /, ln: bool = True) -> int:
	while True:
		try:
			print(prompt, end="")
			num = input()
			if num == 'q':
				raise KeyboardInterrupt(0xe51e2b)
			num = int(num)
			if min_ <= num <= max_:
				return num
		except ValueError:
			pass
		print("§4§lInvalid choice")
		if ln:
			print()


class Scorpion:
	def __init__(self, files: list[str]) -> None:
		self.imgs: dict[str, Image]			= {}
		self.errors: list[tuple[str, str]]	= []

		for file in files:
			try:
				self.imgs[file] = Image(file)
			except Exception as e:
				self.errors.append((file, f"[{e.__class__.__name__}] {e}"))

		self.current_name: str					= ''
		self.current_exif: Image | None			= None
		self.current_list: list[str]			= []
		self.current_dict: dict[str, object]	= {}

	@staticmethod
	def from_argv() -> 'Scorpion':
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
	def print_preview(metadata: dict[str, object]) -> None:
		i_len = len(str(len(metadata) + 1))
		k_len = 22 - i_len // 2
		v_len = 44 - k_len
		for i, (key, val) in enumerate(metadata.items()):
			try:
				if len(key) > k_len:
					key = key[:k_len - 2] + "§7§o..§r"
				val = str(val)
				if len(val) > v_len:
					val = val[:v_len - 2] + "§7§o..§r"
				print(f"§7{i + 1:>{i_len}}.§r {key:>{k_len}}: {val:>{v_len}}")
			except Exception as e:
				print(f"§7{i + 1:>{i_len}}.§r {key:>{k_len}.{k_len}}: §c§o{e}")

	@staticmethod
	def print_metadata(key: str, value: object) -> None:
		print(f"§7     Name:: §e{key}")
		print(f"§7     Type:: §r{type(value).__name__}")
		print(f"§7  __str__:: '§r{str(value)}§7'")
		print(f"§7 __repr__:: '§r{repr(value)}§7'")

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
		if self.current_exif is None:
			return

		with open(self.current_name, 'wb') as f:
			f.write(self.current_exif.get_file())
		print(f"§a§lFile §r{self.current_name}§a§l saved!")

	def delete_metadata(self, key: str) -> None:
		if self.current_exif is None:
			return

		self.current_exif.delete(key)
		self.current_dict.pop(key)
		self.current_list.remove(key)
		print(f"§a§lMetadata §e{key}§a§l deleted!")

	def set_metadata(self, key: str) -> None:
		if self.current_exif is None:
			return

		print("§e§lSetting the value for §n§e" + key)
		print()
		while True:
			print("§7§oValue : ", end="")
			value = input()
			try:
				value = ast.literal_eval(value)
			except Exception:
				pass
			print()
			self.print_metadata(key, value)
			print("§7§oIs this correct ? (Y/n) : ", end="")
			choice = input()
			print()
			if choice.lower() == 'y':
				self.current_exif.set(key, value)
				self.current_dict[key] = value
				break

	def see_img(self) -> None:
		if self.current_exif is None:
			return

		print(f"§e[ §l§n{self.current_name}§e ]")
		print()
		if not self.current_exif.has_exif:
			print("§cThis image has no exif data.")
			print("§7§oPress enter to go back", end="")
			input()
			print()
			self.current_exif = None
			return
		print(f"§6This image has §e{len(self.current_list)}§6 attributes.")

		while self.current_exif is not None:
			print()
			print("§7§o(P)review (L)ist   (G)et (S)ave")
			print("§7§o(E)dit    (D)elete (N)ew (Q)uit : ", end="")
			choice = input()
			if choice.lower() == 'p':
				print()
				self.print_preview(self.current_dict)
			elif choice.lower() == 'l':
				print()
				self.print_list(self.current_list)
			elif choice.lower() == 'g':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_list), ln=False)
				k, v = list(self.current_dict.items())[idx - 1]
				print()
				self.print_metadata(k, v)
			elif choice.lower() == 's':
				print()
				self.save_img()
			elif choice.lower() == 'e':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_list), ln=False)
				k = self.current_list[idx - 1]
				print()
				self.set_metadata(k)
			elif choice.lower() == 'd':
				idx = ask_for_num("§7§oWhich one ? ", 1, len(self.current_list), ln=False)
				k = self.current_list[idx - 1]
				print()
				self.delete_metadata(k)
			elif choice.lower() == 'n':
				k = ''
				while not k:
					print("§7§oNew key : ", end="")
					k = input()
				print()
				self.set_metadata(k)
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
					self.current_name, self.current_exif = tuple(list(self.imgs.items())[choice - 1])
					self.current_list = self.current_exif.list_all()
					self.current_dict = {}
					for key in self.current_list:
						self.current_dict[key] = self.current_exif.get(key)
					print()
					print()
					self.see_img()
		except KeyboardInterrupt as e:
			if 0xe51e2b not in e.args:
				print()
		print("§6§oGoodbye!")


Scorpion.from_argv().run()
