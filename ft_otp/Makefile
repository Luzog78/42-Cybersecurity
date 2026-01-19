# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2026/01/19 01:48:16 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= ft_otp
MAIN			= ft_otp.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= easygui pillow qrcode qrcode[pil]


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(NAME)


help:
	@echo "Available targets:"
	@echo "  all       - Build all components"
	@echo "  $(NAME)    - Build the ft_otp component"
	@echo
	@echo "  clean     - Remove cache artifacts"
	@echo "  fclean    - Remove all artifacts"
	@echo "  re        - Rebuild all components"
	@echo
	@echo "  help      - Show this help message"


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
	@echo "[REMV] Removing every __pycache__ and .pyc files..."
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +


fclean: clean
	@echo "[REMV] Removing __qrcode__ temp files..."
	rm -rf __qrcode__*
	@echo "[REMV] Removing virtual environment..."
	rm -rf $(VENVPATH)
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


.PHONY: all help clean fclean re
