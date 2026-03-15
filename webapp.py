"""Web UI for ColorSort.

This is a lightweight Flask application that reuses the existing
`game.game_logic` implementation and exposes it via a simple web UI.

Run:
    python webapp.py

Then open http://localhost:5000 in your browser.
"""

from __future__ import annotations

import json
from copy import deepcopy

from flask import Flask, render_template, request, session, jsonify

from game.constants import COLORS
from game.game_logic import (
    initialize_game,
    process_move,
    check_win_condition,
    provide_hint,
    best_solve,
    rate_solution,
)

# Secret key for session storage (in-memory). In production, set a strong secret.
SECRET_KEY = "dev-secret"

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_PERMANENT"] = False

# Mapping from the in-game ANSI color representation to a CSS background color.
# This is only used for the web UI; the core game logic continues to use the ANSI strings.
CSS_COLORS = [
    "#e53935",  # red
    "#43a047",  # green
    "#1e88e5",  # blue
    "#00acc1",  # cyan
    "#8e24aa",  # magenta
    "#fdd835",  # yellow
    "#eeeeee",  # white
]

ANSI_TO_CSS = {ansi: css for ansi, css in zip(COLORS, CSS_COLORS)}


def _ensure_state() -> None:
    """Ensure a game state exists in the session (creates one if missing).

    This also ensures `best_solve` is computed and stored for the current puzzle.
    """
    if "stacks" not in session or "best_solve" not in session:
        _reset_state()


def _reset_state() -> list[list]:
    """Reset the game state (used when the UI loads or user explicitly resets)."""
    stacks = initialize_game()
    session["stacks"] = stacks
    session["previous_state"] = deepcopy(stacks)
    session["moves"] = []
    session["best_solve"] = len(best_solve(stacks) or [])
    return stacks


@app.route("/")
def home():
    # Reset on each page load so refreshing starts a new game.
    _reset_state()
    return render_template("index.html")


def _export_stacks(stacks):
    """Convert ANSI color stacks into CSS-friendly color strings."""
    return [[ANSI_TO_CSS.get(cell, "transparent") for cell in stack] for stack in stacks]


def _render_state(extra=None):
    """Render the current session state as a JSON-friendly dict."""
    moves = session.get("moves", [])

    # Use the precomputed best solve for the current game (stored at reset time).
    # Only compute if it somehow does not exist in the session.
    best_solve_count = session.get("best_solve")
    if best_solve_count is None:
        best_moves = best_solve(session["stacks"])
        best_solve_count = None if best_moves is None else len(best_moves)
        session["best_solve"] = best_solve_count

    rating = None if best_solve_count is None else rate_solution(len(moves), best_solve_count)

    payload = {
        "stacks": _export_stacks(session["stacks"]),
        "moves": moves,
        "won": check_win_condition(session["stacks"]),
        "bestSolve": best_solve_count,
        "rating": rating,
    }

    if extra:
        payload.update(extra)

    return payload


@app.route("/api/state", methods=["GET"])
def get_state():
    _ensure_state()
    return jsonify(_render_state())


@app.route("/api/move", methods=["POST"])
def move():
    _ensure_state()
    payload = request.get_json(force=True)
    source = payload.get("source")
    dest = payload.get("destination")

    try:
        processed, previous_state = process_move(session["stacks"], source, dest, session.get("previous_state", []))
    except Exception:
        return jsonify({"ok": False, "error": "Invalid move"}), 400

    if processed:
        session["moves"].append((source, dest))
        session["previous_state"] = deepcopy(previous_state)
        return jsonify(_render_state({"ok": True}))

    return jsonify({"ok": False, "error": "Invalid move"}), 400


@app.route("/api/reset", methods=["POST"])
def reset():
    stacks = initialize_game()
    session["stacks"] = stacks
    session["previous_state"] = deepcopy(stacks)
    session["moves"] = []
    session["best_solve"] = len(best_solve(stacks) or [])
    return jsonify(_render_state({"ok": True}))


@app.route("/api/hint", methods=["GET"])
def hint():
    _ensure_state()
    return jsonify({"hint": provide_hint(session["stacks"])})


if __name__ == "__main__":
    # Disable the reloader so Ctrl+C behaves consistently in all terminals.
    app.run(debug=True, use_reloader=False)
