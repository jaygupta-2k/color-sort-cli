"""
This file is part of ColorSort.
Copyright (C) 2024 Jay Gupta.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the GNU General Public License for more details.
"""

import os
import random

from tabulate import tabulate
from colorama import Fore
from game.constants import MAX_STACK_SIZE, icon

def welcome():
    """
    Displays the welcome message for the game.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.LIGHTYELLOW_EX+icon+Fore.WHITE)
    print("Welcome to the Color Sort Game!\n")
    how_to_play()
    player_name = input("> Enter your name\n> ")
    print(f"\n> Hello, {player_name}! Let's begin.\n")
    return player_name


def how_to_play():
    """
    Displays the "how to play?" message
    """
    print("How to play?")
    print("The goal is to sort colors into uniform stacks.")
    print(f"Each stack can contain a maximum of {MAX_STACK_SIZE} letters.")
    print("You can only move the top colors of a stack.")
    print("""The letter can be moved to a stack with the same 
colors on top or to an empty stack.\n""")
    print("You can enter your move in one of these formats")
    print("  1-2 or 1,2 or 1 2 or 1->2\n")
    print("Or you can enter a command")
    print("  H, hint    : Get a hint.")
    print("  I, help    : Display this message.")
    print("  U, undo    : Undo last move.")
    print("  R, reset   : Reset the game.")
    print("  N, new     : Start a new game.")
    print("  Q, quit    : Quit the game.\n")


def show_stacks(stacks):
    """
    Displays the current state of the stacks in a tabular format.

    Args:
        stacks (list of lists): The current state of the game stacks.
    """
    max_height = max(len(stack) for stack in stacks)
    table = []

    for i in range(max_height - 1, -1, -1):
        row = []
        for stack in stacks:
            row.append(stack[i] if i < len(stack) else " ")
        table.append(row)

    stack_labels = [i + 1 for i in range(len(stacks))]
    sep = ["---" for i in range(len(stacks))]
    table.append(sep)
    table.append(stack_labels)

    print(tabulate(table, tablefmt="rounded_outline", stralign="center", numalign="center"))


def prompts(context="error") -> str:
    """
    Returns a random prompt from a predefined list based on the context.

    Args:
        context (str): The type of prompt to return. Options are 'error', 'restart', 'transition'.

    Returns:
        str: A randomly selected prompt.
    """
    prompt_pool = {
        "error": [
            "Oops! That move didn't work. Try again.",
            "Invalid move! Think carefully.",
            "Hmm, that didn't go as planned. Give it another shot.",
            "Not quite right! Let's focus and retry.",
            "Mistakes happen! Reevaluate your strategy and try again."
        ],
        "restart": [
            "Fresh start! Let's see if this time works better.",
            "Game reset. Focus and plan ahead!",
            "Restarting the game. You got this!",
            "Here we go again! Time to crack the puzzle.",
            "Reset complete. Take a deep breath and dive in!"
        ],
        "transition": [
            "Let's make the next move count!",
            "Great effort! Ready for the next step?",
            "Take your time and think about your next move.",
            "You're doing well! Keep the momentum going.",
            "Progress is progress. Let's aim for the solution!"
        ],
        "new":[
            "All the best!",
            "Best of luck!",
            "Break a leg!"
        ],
        "repeat":[
            "Ready for a rematch?",
            "Fancy another game?",
            "Up for another round?",
            "How about another go?",
            "Wanna play again?",
			"Another round?",
			"Care for another game?",
			"Want another round?",
			"How about a rematch?",
			"Up for it again?",
			"Ready for another round?"
		],
    }

    return random.choice(prompt_pool.get(context, ["Keep going!"]))

def show_copyright():
    print("\n"+Fore.GREEN+"ColorSort  Copyright (C) 2024  Jay Gupta."+Fore.RESET+"\n")

def show_warranty():
    print("\n"+Fore.GREEN+"""This is free software; see the source code for copying 
conditions. There is ABSOLUTELY NO WARRANTY; not even for 
MERCHANTABILITY  or FITNESS FOR A PARTICULAR PURPOSE."""+Fore.RESET+"\n")

if __name__ == "__main__":
    # Example usage
    example_stacks = [
        ["A", "B", "C"],
        ["B", "C"],
        ["A"],
        []
    ]
    show_stacks(example_stacks)
    print(prompts(context="error"))
    print(prompts(context="restart"))
    print(prompts(context="transition"))
    print(prompts(context="repeat"))
