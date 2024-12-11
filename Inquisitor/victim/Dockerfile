# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/09 15:17:49 by ysabik            #+#    #+#              #
#    Updated: 2024/12/09 19:06:10 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM ubuntu:latest

RUN apt-get update \
	&& apt-get install -y net-tools lftp

ENTRYPOINT ["bash"]
