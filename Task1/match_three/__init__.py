"""
Match-3 Puzzle Game Package

A simple match-3 puzzle game implementation built with Python.
"""

from board import Board, Color, Tile
from match_engine import Match, MatchEngine
from game import Game, GameState
from ui import GameUI

__all__ = [
    "Board",
    "Color",
    "Tile",
    "Match",
    "MatchEngine",
    "Game",
    "GameState",
    "GameUI",
]

__version__ = "1.0.0"
__author__ = "Requirements Engineering Exercise"
