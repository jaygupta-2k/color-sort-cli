"""
This file is part of ColorSort.
Copyright (C) 2024 Jay Gupta.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the GNU General Public License for more details.
"""

from colorama import Back

# Constants for the game
MAX_STACK_SIZE = 4
QUIT_COMMAND = "Q"
RESET_COMMAND = "R"
HINT_COMMAND = "H"
NEW_COMMAND = "N"
INFO_COMMAND = "I"
HELP_COMMAND = "HELP"
COPYRIGHT = "SHOW C"
WARRANTY = "SHOW W"

# Constants for stack generation
MIN_STACKS = 5
MAX_STACKS = 9
COLORS = [
    Back.RED+"   "+Back.RESET,
    Back.GREEN+"   "+Back.RESET,
    Back.BLUE+"   "+Back.RESET,
    Back.CYAN+"   "+Back.RESET,
    Back.MAGENTA+"   "+Back.RESET,
    Back.YELLOW+"   "+Back.RESET,
    Back.WHITE+"   "+Back.RESET
]

# ANSI escape codes for alternate screen
ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"

icon = '''                                                                           
   ______           __                  _____                  __ 
  / ____/  ____    / /  ____    _____  / ___/  ____    _____  / /_
 / /      / __ \  / /  / __ \  / ___/  \__ \  / __ \  / ___/ / __/
/ /___   / /_/ / / /  / /_/ / / /     ___/ / / /_/ / / /    / /_  
\____/   \____/ /_/   \____/ /_/     /____/  \____/ /_/     \__/  

'''