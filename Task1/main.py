#!/usr/bin/env python3
"""
Main entry point for the Match-3 Puzzle Game.

Usage:
    python main.py
"""

import sys
import os

# Add the script directory to the Python path so we can import the game modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, "match_three"))

from ui import GameUI


def main():
    """
    Main function to start the game.
    
    Initializes the GameUI and runs the game.
    """
    try:
        game_ui = GameUI()
        game_ui.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
