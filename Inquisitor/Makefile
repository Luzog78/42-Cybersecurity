# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2024/12/11 03:15:44 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= inquisitor
MAIN			= inquisitor.py
PY_LIB			= ../cyberlib.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= pyinstaller scapy getmac


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(NAME)


docker-up:
	cp $(NAME) ./attacker/
	docker compose -f ./docker-compose.yml up -d --build


docker-down:
	docker compose -f ./docker-compose.yml down


docker-top:
	docker ps
	@echo
	docker top $$(docker ps -qa)


server:
	docker exec -it server bash


victim:
	docker exec -it victim bash


attack:
	docker exec -it attacker bash


ftp:
	docker exec -it victim lftp ftp://server -u testuser,password


docker-clean:
	rm -f ./attacker/$(NAME)
	$(call exec, docker stop $$(docker ps -qa), $$(docker ps -qa))
	$(call exec, docker rm $$(docker ps -qa), $$(docker ps -qa))
	$(call exec, docker rmi -f $$(docker images -qa), $$(docker images -qa))
	$(call exec, docker volume rm $$(docker volume ls -q), $$(docker volume ls -q))
	$(call exec, docker network rm $$(docker network ls | grep testnet | awk '{print $$1}'), $$(docker network ls | grep testnet | awk '{print $$1}'))


define exec
	@if [ -n "$$(echo $(2) | awk '{$$1=$$1};1')" ]; then \
		echo "$$> $$(echo -n $(1) | tr '\n' ' ')"; \
		$(1); \
		if [ $$? -eq 0 ]; then \
			echo "OK"; \
		else \
			echo "Error"; \
		fi; \
		echo; \
	fi;
endef


$(NAME)._sh: $(__REQ)
	$(call compile, $(NAME)._sh, $(MAIN))


$(NAME): $(MAIN) $(PY_LIB) $(__REQ)
	$(VENVPATH)/bin/pyinstaller --onefile --clean --distpath . $(MAIN) $(PY_LIB)


$(VENVPATH):
	@echo "[VENV] Creating virtual environment..."
	$(PYTHON) -m venv $(VENVPATH)


$(VENVPATH)/.__installed/__%: $(VENVPATH)
	@echo "[LIBS] Installing $*..."
	$(VENVPATH)/bin/pip install $*
	@mkdir -p $(dir $@)
	@touch $@


clean:
	@echo "[REMV] Removing virtual environment..."
	rm -rf $(VENVPATH) ./build $(NAME).spec


fclean: clean
	@echo "[REMV] Removing executables..."
	rm -f $(NAME) $(NAME)._sh


re: fclean all


define compile
	@echo "[COMP] Compiling $(1)..."
	@echo "#!/bin/sh" > $(1)
	@if [ -n "$(REQUIREMENTS)" ]; then \
		echo "$(abspath $(VENVPATH))/bin/python $(abspath $(2)) \$$@" >> $(1); \
	else \
		echo "$$(which $(PYTHON)) $(abspath $(2)) \$$@" >> $(1); \
	fi
	@chmod +x $(1)
	@echo "[DONE] $(1) compiled."
endef


.PHONY: all clean fclean re docker-up docker-down docker-top server victim attack ftp docker-clean
