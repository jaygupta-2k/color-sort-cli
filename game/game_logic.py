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
    Finds the best move sequence to solve the game using heuristic-based A* search.
    Args:
        initial_stacks: The initial game stacks
    Returns:
        list: best moves, or None if unsolvable
    """
    from copy import deepcopy
    from heapq import heappush, heappop

    def compress_state(stacks: list[list]) -> tuple:
        return tuple(tuple(stack) for stack in stacks)

    def heuristic_score(stacks: list[list]) -> int:
        score = 0
        for stack in stacks:
            if not stack:
                continue
            if len(set(stack)) > 1:
                score += len(set(stack))  # More mixed colors, worse
            if len(stack) < MAX_STACK_SIZE:
                score += 1  # Penalize incomplete tubes
        return score

    def get_valid_moves(stacks: list[list], previous_move=None) -> list[tuple[int, int]]:
        moves = []
        for source_index, source_stack in enumerate(stacks):
            if not source_stack:
                continue
            clean_stack_flag = all(x == source_stack[0] for x in source_stack)
            for destination_index, destination_stack in enumerate(stacks):
                if source_index == destination_index:
                    continue
                if previous_move and previous_move[0] == destination_index and previous_move[1] == source_index:
                    continue
                if clean_stack_flag and (not destination_stack or
                                         (MAX_STACK_SIZE - len(destination_stack)) < len(source_stack)):
                    continue
                if ((not destination_stack or source_stack[-1] == destination_stack[-1]) and
                        len(destination_stack) < MAX_STACK_SIZE):
                    moves.append((source_index, destination_index))
        return moves

    visited = set()
    heap = []
    initial_score = heuristic_score(initial_stacks)
    heappush(heap, (initial_score, 0, initial_stacks, []))

    while heap:
        score, depth, stacks, path = heappop(heap)
        state_key = compress_state(stacks)

        if state_key in visited:
            continue
        visited.add(state_key)

        if check_win_condition(stacks):
            return path

        for move in get_valid_moves(stacks, path[-1] if path else None):
            src, dst = move
            new_stacks = deepcopy(stacks)
            success, _ = process_move(new_stacks, src, dst)
            if success:
                new_score = heuristic_score(new_stacks)
                heappush(heap, (new_score + depth + 1, depth + 1, new_stacks, path + [move]))

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
