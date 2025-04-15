"""
This file is part of ColorSort.
Copyright (C) 2024 Jay Gupta.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the GNU General Public License for more details.
"""

import random
import re
from .constants import *

def initialize_game(num_stacks=None):
    """
    Generates the initial game state with randomized stacks.

    Args:
        num_stacks (int, optional): Number of stacks to generate.
        Defaults to a random number between MIN_STACKS and MAX_STACKS.

    Returns:
        list of lists: A list of stacks representing the game state.
    """
    if num_stacks is None:
        num_stacks = random.randint(MIN_STACKS, MAX_STACKS)

    # Choose a subset of colors based on the number of stacks
    num_colors = num_stacks - 2
    selected_colors = COLORS[:num_colors]

    # Create a pool of colors with each appearing exactly MAX_STACK_SIZE times
    color_pool = selected_colors * MAX_STACK_SIZE
    random.shuffle(color_pool)

    # Generate stacks and ensure no stack is fully uniform
    stacks = []
    while color_pool:
        stack = []
        while len(stack) < MAX_STACK_SIZE and color_pool:
            color = color_pool.pop()
            stack.append(color)

        # Validate stack uniformity
        if len(set(stack)) == 1:
            color_pool.extend(stack)
            random.shuffle(color_pool)
            continue

        stacks.append(stack)

    # Add empty stacks for player moves
    for _ in range(2):
        stacks.append([])

    return stacks


def process_move(stack_list, source, destination):
    """
    Moves a letter from the source stack to the destination stack if valid.

    Args:
        source (list): The source stack.
        destination (list): The destination stack.

    Returns:
        bool: True if the move was successful, False otherwise.
    """
    flag = False
    source_stack = stack_list[source]
    destination_stack = stack_list[destination]

    if not source_stack or len(destination_stack) == MAX_STACK_SIZE or source == destination:
        return flag  # Cannot move from an empty stack or to stack of max length or to the same stack

    while ((not destination_stack or source_stack[-1] == destination_stack[-1]) and
           len(destination_stack) != MAX_STACK_SIZE):
        destination.append(source.pop())
        flag = True
        if not source:
            break

    return flag  # Invalid move if colors don't match


def check_solvability(stack_list, previous_move=None):
    """
    Checks if the current game state is solvable by identifying valid moves.
    Avoids suggesting moves that would create a loop with the previous move.

    Args:
        stack_list (list of lists): The current game state.
        previous_move (tuple, optional): The last move made by the player.
        Defaults to None.
    Returns:
        tuple: A tuple containing the source and destination stack indices for a valid move, or None if no move exists.
    """
    for source_index, source_stack in enumerate(stack_list):
        if not source_stack:
            continue  # Skip empty stacks

        clean_stack_flag = all(x == source_stack[0] for x in source_stack)

        for destination_index, destination_stack in enumerate(stack_list):
            if source_index == destination_index:
                continue  # Skip the same stack

            # Skip moves that would create a loop with the previous move
            if previous_move and previous_move[0] == destination_index and previous_move[1] == source_index:
                continue

            # Skip moving from single-color stacks to empty stacks
            if clean_stack_flag and (not destination_stack or
                                     (MAX_STACK_SIZE - len(destination_stack)) < len(source_stack)):
                continue

            if ((not destination_stack or source_stack[-1] == destination_stack[-1]) and
                    len(destination_stack) < MAX_STACK_SIZE):
                return source_index, destination_index
    return None  # No valid moves


def parse_move(command):
    """Parses the player's move command."""
    command = list(filter(str.strip, re.split(r'->|[,\-\s]',command)))
    if len(command) != 2:
        raise ValueError("Invalid move format.")

    source, destination = map(int, command)
    source_index = source - 1
    destination_index = destination - 1

    return source_index, destination_index


def check_win_condition(stack):
    """Checks if a stack is solved (contains one type of color)."""
    return all(x == stack[0] for x in stack)

def provide_hint(stacks, previous_command=None):
    """Generates a hint for the player based on the current stack configuration."""
    solvable_move = check_solvability(stacks, previous_command)
    if solvable_move:
        source, destination = solvable_move
        return f"\n> Hint: Try moving from stack {source + 1} to stack {destination + 1}.\n"
    return "\n> No valid moves. Consider undoing or restarting.\n"


if __name__ == "__main__":
    # Example usage
    stacks = initialize_game()
    for i, stack in enumerate(stacks):
        print(f"Stack {i + 1}: {stack}")

    print("Before move:", stacks)
    process_move(stacks[0], stacks[2])
    print("After move:", stacks)

    hint = check_solvability(stacks, 4)
    if hint:
        print(f"Hint: Move from stack {hint[0] + 1} to stack {hint[1] + 1}.")
    else:
        print("No valid moves available.")
