# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/16 03:01:05 by luzog78           #+#    #+#              #
#    Updated: 2025/12/17 05:40:51 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

DOCKER_COMPOSE := docker compose


all: help


help:
	@echo "Available targets:"
	@echo "  help         - Show this help message"
	@echo
	@echo "  up           - Build and run the project"
	@echo "  down         - Stop the project containers"
	@echo "  clean        - Remove containers, keeping volumes and images"
	@echo "  fclean       - Remove containers and volumes, keeping images"
	@echo "  prune        - Remove everything, not keeping any artifacts"
	@echo
	@echo "  ps           - Show status of containers, images, volumes and stats"
	@echo "  logs         - Show all service logs"
	@echo "  logs-db      - Show database service logs"
	@echo "  logs-ui      - Show database UI service logs"
	@echo "  logs-web     - Show webapp service logs"


up:
	$(DOCKER_COMPOSE) up --build -d
	@echo "Project is up and running."


down:
	$(DOCKER_COMPOSE) down
	$(call RETURN,Project containers have been stopped.)



clean:
	$(DOCKER_COMPOSE) rm --force --stop
	$(call RETURN,Project containers have been removed.)


fclean:
	$(DOCKER_COMPOSE) rm --force --stop --volumes
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	$(call RETURN,Project containers and volumes have been removed.)


prune:
	$(DOCKER_COMPOSE) rm --force --stop --volumes
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	$(call RETURN,All build artifacts have been cleaned up.)


ps:
	$(DOCKER_COMPOSE) ps
	@echo
	$(DOCKER_COMPOSE) images
	@echo
	$(DOCKER_COMPOSE) volumes
	@echo
	$(DOCKER_COMPOSE) stats --no-stream


logs:
	$(DOCKER_COMPOSE) logs -f || true


logs-db:
	@echo "SQLite runs inside the web container"


logs-ui:
	@echo "SQLite does not have a separate UI container"


logs-web:
	docker compose logs -f webapp_sqlite || true


define RETURN
	@if [ $$? -eq 0 ]; then \
	    echo "$(1)"; \
	else \
	    echo "Operation failed."; \
	fi
endef


.PHONY: all help up down clean fclean prune ps logs logs-db logs-ui logs-web
