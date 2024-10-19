# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2024/10/19 14:16:40 by ysabik           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME			= ft_otp
MAIN			= scorpion.py

PYTHON			= python3
VENVPATH		= venv
REQUIREMENTS	= 


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
		echo "$(abspath $(VENVPATH))/bin/python $(abspath $(2)) \$$@" >> $(1); \
	else \
		echo "$(abspath $(PYTHON)) $(abspath $(2)) \$$@" >> $(1); \
	fi
	@chmod +x $(1)
	@echo "[DONE] $(1) compiled."
endef


.PHONY: all clean fclean re
