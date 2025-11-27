# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2025/11/27 13:36:43 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= arachnida

SPIDER			= spider
SPIDER_MAIN		= spider.py

SCORPION		= scorpion
SCORPION_MAIN	= scorpion.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= requests bs4 exif


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(NAME)


$(NAME): $(SPIDER) $(SCORPION)


$(SPIDER): $(__REQ)
	$(call compile, $(SPIDER), $(SPIDER_MAIN))


$(SCORPION): $(__REQ)
	$(call compile, $(SCORPION), $(SCORPION_MAIN))


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
	rm -rf $(VENVPATH)


fclean: clean
	@echo "[REMV] Removing executables..."
	rm -f $(SPIDER) $(SCORPION)


re: fclean all


define compile
	@echo "Compiling $(1)..."
	@echo "#!/bin/sh" > $(1)
	@if [ -n "$(REQUIREMENTS)" ]; then \
		echo "$(abspath $(VENVPATH))/bin/python $(abspath $(2)) \"\$$@\"" >> $(1); \
	else \
		echo "$$(which $(PYTHON)) $(abspath $(2)) \"\$$@\"" >> $(1); \
	fi
	@chmod +x $(1)
	@echo "[DONE] $(1) compiled."
endef


.PHONY: all clean fclean re
