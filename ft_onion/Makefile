# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2026/01/19 03:29:28 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= ft_onion
DOCKER			= docker
DOCKERFILE		= Dockerfile


help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  all      - Build, run and then tell the hostname"
	@echo
	@echo "  build    - Build Docker image"
	@echo "  run      - Build and Run Docker container"
	@echo "  stop     - Stop Docker container"
	@echo
	@echo "  logs     - Show Docker container logs"
	@echo "  shell    - Start shell in Docker container"
	@echo "  tor      - Get Tor hidden service hostname"
	@echo
	@echo "  clean    - Stop and Remove Docker image"
	@echo "  fclean   - Alias for clean"
	@echo "  re       - Alias for fclean all"
	@echo
	@echo "  help     - Show this help message"


all: $(NAME)


$(NAME): build run tor


tor:
	@echo "[EXEC] Getting Tor hostname..."
	$(DOCKER) exec -it $(NAME) cat /tor-hostname


build:
	@echo "[BUIL] Building Docker image..."
	$(DOCKER) build -t $(NAME) .


run: build
	@echo "[RUNN] Running Docker container..."
	$(DOCKER) run -d --name $(NAME) -p 8080:80 -p 4242:4242 $(NAME)
	@echo "http://localhost:8080"
	@echo "ssh root@localhost -p 4242"


stop:
	@echo "[STOP] Stopping Docker container..."
	-$(DOCKER) stop $(NAME)


logs:
	@echo "[LOGS] Showing Docker container logs..."
	$(DOCKER) logs $(NAME)


shell:
	@echo "[EXEC] Starting shell in Docker container..."
	$(DOCKER) exec -it $(NAME) /bin/bash


clean: stop
	@echo "[REMV] Removing Docker image..."
	-$(DOCKER) rm $(NAME)
	-$(DOCKER) rmi $(NAME)


fclean: clean


re: fclean all


.PHONY: all tor clean fclean re build run stop logs shell help
