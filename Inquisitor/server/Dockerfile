# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/09 15:17:49 by ysabik            #+#    #+#              #
#    Updated: 2024/12/09 19:03:20 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM stilliard/pure-ftpd:hardened

RUN apt-get update \
	&& apt-get install -y net-tools

# /run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P localhost -p 30000:30009
CMD ["/run.sh", "-c", "30", "-C", "10", "-l", "puredb:/etc/pure-ftpd/pureftpd.pdb", "-E", "-j", "-R", "-P", "localhost", "-p", "30000:30009"]
