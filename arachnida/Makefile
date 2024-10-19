# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/19 13:16:00 by ysabik            #+#    #+#              #
#    Updated: 2024/10/19 13:47:54 by ysabik           ###   ########.fr        #
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


all: $(NAME)


$(NAME): $(VENVPATH) $(SPIDER) $(SCORPION)


$(VENVPATH):
	$(PYTHON) -m venv $(VENVPATH)
	$(VENVPATH)/bin/pip install $(REQUIREMENTS)


$(SPIDER):
	$(call compile, $(SPIDER), $(SPIDER_MAIN))


$(SCORPION):
	$(call compile, $(SCORPION), $(SCORPION_MAIN))


clean:
	rm -rf $(VENVPATH)


fclean: clean
	rm -f $(SPIDER) $(SCORPION)


re: fclean all


define compile
	@echo "Compiling $(1)..."
	@echo "#!/bin/sh" > $(1)
	@echo "$(abspath $(VENVPATH))/bin/python $(abspath $(2)) \$$@" >> $(1)
	@chmod +x $(1)
endef


.PHONY: all clean fclean re
