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
from copy import deepcopy

from game.constants import *


def initialize_game(num_stacks : int = None) -> list[list]:
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


def process_move(stacks: list[list], source, destination, previous_state = []) -> tuple:
    """
    Moves a letter from the source stack to the destination stack if valid.

    Args:
        stacks: The list of stacks.
        source (int): The source stack.
        destination (int): The destination stack.

    Returns:
        bool: True if the move was successful, False otherwise.
    """
    flag = False
    source_stack = stacks[source]
    destination_stack = stacks[destination]

    if not source_stack or len(destination_stack) == MAX_STACK_SIZE or source == destination:
        return flag, previous_state  # Cannot move from an empty stack or to stack of max length or to the same stack

    initial_state = deepcopy(stacks)

    while ((not destination_stack or source_stack[-1] == destination_stack[-1]) and
           len(destination_stack) != MAX_STACK_SIZE):
        destination_stack.append(source_stack.pop())
        flag = True
        if not source_stack:
            break

    if flag:
        previous_state = initial_state

    return flag, previous_state  # Invalid move if colors don't match


def parse_move(command: str) -> tuple[int, int]:
    """Parses the player's move command."""
    command = list(filter(str.strip, re.split(r'->|[,\-\s]', command)))
    if len(command) != 2:
        raise ValueError("Invalid move format.")

    source, destination = map(int, command)
    source_index = source - 1
    destination_index = destination - 1

    return source_index, destination_index


def check_win_condition(stacks: list[list]) -> bool:
    """Checks if a stack is solved (each stack contains one type of color and is of max length)."""
    return all(all(x == stack[0] for x in stack) and len(stack) == MAX_STACK_SIZE for stack in stacks if stack)


def provide_hint(stacks: list[list]) -> str:
    """Generates a hint for the player based on the current stack configuration."""
    best_moves = best_solve(stacks)
    if best_moves:
        source, destination = best_moves[0]
        return f"\n> Hint: Try moving from stack {source + 1} to stack {destination + 1}.\n"
    return "\n> No valid moves. Consider undoing or restarting.\n"


def best_solve(initial_stacks: list[list]) -> list[tuple[int, int]] | None:
    """
    Finds the best move to solve the game using BFS.
    Args:
        initial_stacks: The stack list

    Returns:
        list: best moves
    """
    from copy import deepcopy
    from collections import deque

    def compress_state(stacks : list[list]) -> tuple:
        return tuple(tuple(stack) for stack in stacks)

    def get_valid_moves(stacks : list[list], previous_move=None) -> list[tuple[int, int]]:
        """
        Checks if the current game state is solvable by identifying valid moves.
        Avoids suggesting moves that would create a loop with the previous move.

        Args:
            stacks (list of lists): The current game state.
            previous_move (tuple, optional): The last move made by the player.
            Defaults to None.
        Returns:
            tuple: A tuple containing the source and destination stack indices for a valid move, or None if no move exists.
        """
        moves = []
        for source_index, source_stack in enumerate(stacks):
            if not source_stack:
                continue  # Skip empty stacks

            clean_stack_flag = all(x == source_stack[0] for x in source_stack)

            for destination_index, destination_stack in enumerate(stacks):
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
                    moves.append((source_index, destination_index))
        return moves

    visited = set()
    queue = deque()
    queue.append((initial_stacks, []))

    while queue:
        stacks, path = queue.popleft()
        state_key = compress_state(stacks)

        if state_key in visited:
            continue
        visited.add(state_key)

        if check_win_condition(stacks):
            return path

        for src, dst in get_valid_moves(stacks):
            new_stacks = deepcopy(stacks)
            if process_move(new_stacks, src, dst)[0]:
                queue.append((new_stacks, path + [(src, dst)]))
    return None

def rate_solution(user_moves, optimal_moves):
    if user_moves <= optimal_moves:
        return 5
    ratio = optimal_moves / user_moves
    stars = 5 * ratio
    return int(max(1.0, round(stars, 1)))  # Ensure at least 1 star


if __name__ == "__main__":
    # Example usage
    stacks = initialize_game()
    for i, stack in enumerate(stacks):
        print(f"Stack {i + 1}: {stack}")

    print("Before move:", stacks)
    process_move(stacks[0], stacks[2])
    print("After move:", stacks)
