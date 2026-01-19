# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/22 15:03:20 by ysabik            #+#    #+#              #
#    Updated: 2026/01/19 03:34:43 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM debian:latest


RUN		apt-get update -y \
		&& apt-get install -y nginx \
		&& apt-get install -y openssh-server \
		&& apt-get install -y tor


RUN		rm -rf /etc/nginx/sites-available/* \
		&& rm -rf /etc/nginx/sites-enabled/* \
		&& rm -rf /var/www/html/* \
		&& mkdir -p /var/www/ft_onion \
		&& chown -R www-data:www-data /var/www/ft_onion \
		&& chmod -R 755 /var/www/ft_onion

COPY	./srcs/index.html /var/www/ft_onion/index.html
COPY	./srcs/nginx.conf /etc/nginx/nginx.conf
COPY	./srcs/torrc /etc/tor/torrc
COPY	./srcs/sshd_config /etc/ssh/sshd_config
COPY	./srcs/.ssh/authorized_keys /root/.ssh/authorized_keys
COPY	./srcs/start.sh /start.sh

RUN		chmod +x /start.sh


EXPOSE	80 4242

ENTRYPOINT	[ "/start.sh" ]

CMD	[ "nginx", "-g", "daemon off;" ]
