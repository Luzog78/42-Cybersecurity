# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    analysis.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/28 08:26:09 by luzog78           #+#    #+#              #
#    Updated: 2025/12/15 19:07:10 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Literal
from bs4 import BeautifulSoup as BS

from vaccine import Vaccine, VaccineError, Form, InputField, print, print_error, request


def analyze(
		app: Vaccine,
		stop_analysis_on: Literal['first_vulnerability', 'db_identification', 'complete'] = 'db_identification',
		compute_every_form: bool = True,
		) -> None:
	print(f'~~~ Starting analysis phase ~~~')
	print()

	app.forms = scrape_forms(app.url, app.headers)
	print(f'[+] Found {len(app.forms)} forms')
	for form in app.forms:
		print(f' - Form action: {repr(form.action)}, method: {repr(form.method)}, inputs: {len(form.inputs)}')
		for input in form.inputs:
			print(f'    - Input name: {repr(input.name)}, type: {repr(input.type)}, required: {input.required}')
	print()

	for form in app.forms:
		vulnerability_found, db_identified = inject_form(
			headers=app.headers,
			errors_injections=app.injections['injections']['errors'],
			error_signatures=app.injections['injections']['error_signatures'],
			form=form,
			stop_on=stop_analysis_on,
		)
		if vulnerability_found and not compute_every_form:
			if stop_analysis_on == 'db_identification':
				if db_identified:
					break
			else:
				break

	print()


def scrape_forms(url: str, headers: dict[str, str]) -> list[Form]:
	response = request('GET', url, headers=headers, raise_for_status=True)
	soup = BS(response.text, 'html.parser')
	forms = [
		Form(
			form,
			inputs=[
				InputField(input) for input in form.find_all('input')
			],
			url=url,
		) for form in soup.find_all('form')
	]
	return list(filter(lambda f: len(f.inputs) > 0, forms))


def inject_form(
		headers: dict[str, str],
		errors_injections: list[str],
		error_signatures: dict[str, str | None],
		form: Form,
		stop_on: Literal['first_vulnerability', 'db_identification', 'complete'],
		) -> tuple[bool, bool]:
	print(f'[*] Injecting form {repr(form.action_url)} with method {repr(form.method)}')
	vulnerability_found = False
	db_identified = False

	for injection in errors_injections:
		for input in form.inputs:
			try:
				print(f'  [*] Testing on input {repr(input.name)} injection {repr(injection)}')
				response = request(
					method=form.method,
					url=form.action_url,
					headers=headers,
					data=form.get_inputs_dict() | {input.name: injection},
					raise_for_status=True,
				)
				for signature, db in error_signatures.items():
					if signature in response.text.lower():
						print(f'    [+] Found signature: {repr(signature)}' + (f' (DB: {repr(db)})' if db is not None else ''))
						form.vulnerabilities.append((input, signature, db))
						vulnerability_found = True
						db_identified = db is not None
						if stop_on == 'first_vulnerability' or (db_identified and stop_on == 'db_identification'):
							return vulnerability_found, db_identified
						break
			except VaccineError as e:
				print(f'    [!] Error: [{e.__class__.__name__}] {e}')
				print_error(e)

	return vulnerability_found, db_identified
