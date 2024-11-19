# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2024/10/23 12:39:20 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= ft_onion
DOCKER			= docker
DOCKERFILE		= Dockerfile


help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Build and run Docker container"
	@echo "  build    - Build Docker image"
	@echo "  run      - Run Docker container"
	@echo "  stop     - Stop Docker container"
	@echo "  logs     - Show Docker container logs"
	@echo "  shell    - Start shell in Docker container"
	@echo "  clean    - Remove Docker image"
	@echo "  fclean   - Alias for clean"
	@echo "  re       - Alias for fclean all"
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
	$(DOCKER) run -d --name $(NAME) $(NAME)


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


.PHONY: all clean fclean re build run stop logs shell help
