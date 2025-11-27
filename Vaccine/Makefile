# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2025/11/27 13:35:28 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= vaccine
MAIN			= vaccine.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= beautifulsoup4


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(NAME)


$(NAME): $(__REQ)
	$(call compile, $(NAME), $(MAIN))


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
	rm -f $(NAME)


re: fclean all


define compile
	@echo "[COMP] Compiling $(1)..."
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
