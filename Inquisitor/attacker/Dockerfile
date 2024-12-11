# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/09 15:17:49 by ysabik            #+#    #+#              #
#    Updated: 2024/12/09 18:53:19 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM ubuntu:latest

# FROM python:3.9-slim

# RUN apt-get update \
# 	&& apt-get install -y tcpdump net-tools iputils-ping \
# 	&& pip install scapy

RUN apt-get update \
	&& apt-get install -y tcpdump net-tools iputils-ping

COPY inquisitor /

CMD ["bash"]
