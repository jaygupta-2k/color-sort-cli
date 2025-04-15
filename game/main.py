"""
This file is part of ColorSort.
Copyright (C) 2024 Jay Gupta.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the GNU General Public License for more details.
"""

import sys
from time import sleep
from .display import *
from .game_logic import *
from .constants import *

def main():
    """Main function to run the game."""
    try:
        # Enable alternate screen buffer
        sys.stdout.write(ALT_SCREEN_ON)
        sys.stdout.flush()
        player_name=welcome()

        # Game initialization
        new = True
        stack_list = initialize_game()
        original_stack_list = [stack.copy() for stack in stack_list]
        previous_command = None

        while True:
            show_stacks(stack_list)

            if all(check_win_condition(stack) for stack in stack_list if stack):
                print(f"\n> Congratulations, {player_name}! You solved the game.")
                new = input(f"\n> {prompts(context='repeat')}[Y/n]\n> ")
                if new not in ['Y', '']:
                    break
                else:
                    new = True
                    stack_list = initialize_game()
                    original_stack_list = [stack.copy() for stack in stack_list]
                    print("\n> New game!\n")
                    continue

            if new:
                print(f"\n> {prompts(context='new')}")
                new = False
            else:
                print(f"\n> {prompts(context='transition')}")

            command = input("> Enter your move or a command\n> ").strip().upper()

            if command == QUIT_COMMAND:
                break
            elif command == RESET_COMMAND:
                stack_list = [stack.copy() for stack in original_stack_list]
                print("\n> Game reset!")
                print(f"> {prompts(context='restart')}\n")
            elif command == HINT_COMMAND:
                hint = provide_hint(stack_list, previous_command)
                print(hint)
                sleep(1)
            elif command == NEW_COMMAND:
                new = True
                stack_list = initialize_game()
                original_stack_list = [stack.copy() for stack in stack_list]
                print("\n> New game!\n")
            elif command == INFO_COMMAND or command == HELP_COMMAND:
                print()
                how_to_play()
                sleep(3)
            elif command == COPYRIGHT:
                show_copyright()
            elif command == WARRANTY:
                show_warranty()
            else:
                try:
                    source, destination = parse_move(command)
                    previous_command = (source, destination)
                    if process_move(stack_list, source, destination):
                        print(f"\n> Moved from stack {source + 1} to stack {destination + 1}.\n")
                    else:
                        print(f"\n> Invalid move. Please try again.\n> {prompts(context='error')}\n")
                except Exception:
                    print(f"\n> Invalid input. Please use the right format or a valid command.\n> "
                          f"{prompts(context='error')}\n")

    finally:
        # Restore the main screen buffer
        print("\nPress Enter to exit.")
        input()
        sys.stdout.write(ALT_SCREEN_OFF)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
