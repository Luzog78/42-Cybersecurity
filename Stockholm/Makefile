# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2024/12/09 04:25:40 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= stockholm
MAIN			= stockholm.py
PY_LIB			= ../cyberlib.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= pyinstaller pycryptodome


__REQ			= $(addprefix $(VENVPATH)/.__installed/__, $(REQUIREMENTS))


all: $(NAME)


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
	rm -rf $(VENVPATH)


fclean: clean
	@echo "[REMV] Removing executables..."
	rm -f $(NAME) $(NAME)._sh


re: fclean all


define compile
	@echo "Compiling $(1)..."
	@echo "#!/bin/sh" > $(1)
	@if [ -n "$(REQUIREMENTS)" ]; then \
		echo "$(abspath $(VENVPATH))/bin/python $(abspath $(2)) \$$@" >> $(1); \
	else \
		echo "$$(which $(PYTHON)) $(abspath $(2)) \$$@" >> $(1); \
	fi
	@chmod +x $(1)
	@echo "[DONE] $(1) compiled."
endef


.PHONY: all clean fclean re
