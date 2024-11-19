# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/22 15:03:20 by ysabik            #+#    #+#              #
#    Updated: 2024/10/23 12:46:11 by ysabik           ###   ########.fr        #
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


# RUN		mkdir -p 

COPY	./srcs/index.html /var/www/ft_onion/index.html
COPY	./srcs/nginx.conf /etc/nginx/nginx.conf
COPY	./srcs/torrc /etc/tor/torrc
COPY	./srcs/sshd_config /etc/ssh/sshd_config
COPY	./srcs/start.sh /start.sh


RUN		chmod +x /start.sh


ENTRYPOINT	[ "/start.sh" ]

CMD	[ "nginx", "-g", "daemon off;" ]
