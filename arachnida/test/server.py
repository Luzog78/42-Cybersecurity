# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/17 15:44:08 by ysabik            #+#    #+#              #
#    Updated: 2024/10/17 15:57:45 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Flask, send_file, redirect


app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
	return redirect('/index.html')

@app.route('/<path:path>')
def route(path: str):
	filepath = ('./' + path).replace('/../', '')
	try:
		return send_file(filepath)
	except FileNotFoundError:
		return '<h1>404 - NotFound</d1>'

app.run(host='0.0.0.0', port=8000)
