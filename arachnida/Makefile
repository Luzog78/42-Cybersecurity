# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: luzog78 <luzog78@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2026/01/17 12:39:00 by luzog78          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= arachnida

SPIDER			= spider
SPIDER_MAIN		= spider.py

SCORPION		= scorpion
SCORPION_MAIN	= scorpion.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= requests bs4 pillow flask


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(SPIDER) $(SCORPION)


help:
	@echo "Available targets:"
	@echo "  all       - Build all components"
	@echo "  $(SPIDER)    - Build the spider component"
	@echo "  $(SCORPION)  - Build the scorpion component"
	@echo
	@echo "  clean     - Remove build artifacts"
	@echo "  fclean    - Remove all artifacts"
	@echo "  re        - Rebuild all components"
	@echo
	@echo "  test      - Run the test server"
	@echo "  help      - Show this help message"


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


test:
	@echo "Running test server..."
	cd test && python3 server.py


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


.PHONY: all help clean fclean re test
