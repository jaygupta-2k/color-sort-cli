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
from game.display import *
from game.game_logic import *
from game.constants import *


def main():
    """Main function to run the game."""
    from copy import deepcopy

    def initialize():
        stacks = initialize_game()

        return stacks, deepcopy(stacks), deepcopy(stacks), len(best_solve(stacks)), [], True

    try:
        # Enable alternate screen buffer
        sys.stdout.write(ALT_SCREEN_ON)
        sys.stdout.flush()
        player_name=welcome()

        stacks, original_stacks, previous_state, best_solve_count, moves, new = initialize()

        while True:
            show_stacks(stacks)
            if check_win_condition(stacks):
                print(f"\n> Congratulations, {player_name}! You solved the game.")
                print(f"\n> Best solve: {best_solve_count}")
                print(f"> Your solve: {len(moves)}")
                print('\n',Fore.YELLOW+(rate_solution(len(moves),best_solve_count) * '⭐')+Fore.WHITE)
                new = input(f"\n> {prompts(context='repeat')}[Y/n]\n> ").strip().upper()
                if new not in ['Y', '']:
                    break
                else:
                    stacks, original_stacks, previous_state, best_solve_count, moves, new = initialize()
                    print("\n> New game!\n")
                    continue

            if new:
                print(f"\n> {prompts(context='new')}")
                new = False
            else:
                print(f"\n> {prompts(context='transition')}")

            command = input("> Enter your move or a command\n> ").strip().upper()

            if command in QUIT_COMMAND:
                break
            elif command in RESET_COMMAND:
                stacks = deepcopy(original_stacks)
                print("\n> Game reset!")
                print(f"> {prompts(context='restart')}\n")
            elif command in HINT_COMMAND:
                hint = provide_hint(stacks)
                print(hint)
                sleep(1)
            elif command in NEW_COMMAND:
                stacks, original_stacks, previous_state, best_solve_count, moves, new = initialize()
                print("\n> New game!\n")
            elif command in INFO_COMMAND:
                print()
                how_to_play()
                sleep(3)
            elif command in UNDO_COMMAND:
                print()
                if moves:
                    moves.pop()
                    stacks = deepcopy(previous_state)
            elif command == COPYRIGHT:
                show_copyright()
            elif command == WARRANTY:
                show_warranty()
            else:
                try:
                    source, destination = parse_move(command)
                    processed, previous_state = process_move(stacks, source, destination, previous_state)
                    if processed:
                        moves.append((source, destination))
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
